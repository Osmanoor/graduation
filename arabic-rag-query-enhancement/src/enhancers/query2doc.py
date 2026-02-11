"""
Query2Doc Query Enhancer
Based on: Wang et al. (2023) "Query2doc: Query Expansion with Large Language Models"

Uses LLM to generate pseudo-documents that expand the original query.
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import List, Optional
from .base import QueryEnhancer


class Query2DocEnhancer(QueryEnhancer):
    """
    Query2Doc enhancer using Qwen 2.5 3B Instruct
    
    Generates pseudo-documents using LLM prompting to expand queries
    with relevant context, synonyms, and information.
    
    OPTIMIZED for speed with batch processing and reduced token generation.
    """
    
    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-3B-Instruct",
        max_new_tokens: int = 128,  # Reduced from 256 for 2x speed
        temperature: float = 0.7,
        top_p: float = 0.9,
        device: str = "auto",
        batch_size: int = 8  # Process multiple queries at once
    ):
        """
        Initialize Query2Doc enhancer
        
        Args:
            model_name: HuggingFace model identifier
            max_new_tokens: Maximum tokens to generate (lower = faster)
            temperature: Sampling temperature (lower = more focused)
            top_p: Nucleus sampling parameter
            device: Device placement ("auto", "cuda", "cpu")
            batch_size: Number of queries to process in parallel (higher = faster)
        """
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.batch_size = batch_size
        
        print(f"Loading {model_name} in float16...")
        
        # Load tokenizer with padding support
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # IMPORTANT: Set left padding for decoder-only models
        self.tokenizer.padding_side = 'left'
        
        # Load model in float16 for efficiency
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map=device
        )
        
        # Set to eval mode and disable gradients for faster inference
        self.model.eval()
        
        print(f"✓ Model loaded on {self.model.device}")
        print(f"✓ Batch size: {batch_size} (processing {batch_size} queries at once)")
        print(f"✓ Max tokens: {max_new_tokens} (shorter = faster)")
        
        # System prompt from Query2Doc paper
        self.system_prompt = (
            "You are asked to write a passage that answers the given query. "
            "Do not ask the user for further clarification. "
            "Respond in Arabic only."
        )
    
    def enhance(self, query: str, query_id: str = None) -> str:
        """
        Enhance single query using Query2Doc approach
        
        Args:
            query: Original query text
            query_id: Optional query identifier
            
        Returns:
            Enhanced query (original + generated pseudo-document)
        """
        # Format prompt
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": query}
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        # Generate pseudo-document
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id
            )
        
        # Decode response
        generated_ids = [
            output_ids[len(input_ids):] 
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        pseudo_doc = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # Combine: original query + pseudo-document
        enhanced = f"{query} {pseudo_doc}"
        
        return enhanced
    
    def enhance_batch_parallel(
        self,
        queries: List[str],
        query_ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Enhance a batch of queries in parallel (FAST)
        
        Args:
            queries: List of query texts
            query_ids: Optional list of query identifiers
            
        Returns:
            List of enhanced queries
        """
        # Format all prompts
        all_messages = [
            [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": query}
            ]
            for query in queries
        ]
        
        # Apply chat template to all
        texts = [
            self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            for messages in all_messages
        ]
        
        # Tokenize with padding
        model_inputs = self.tokenizer(
            texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.model.device)
        
        # Generate for all queries at once
        with torch.no_grad():
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id
            )
        
        # Decode all responses
        input_lengths = model_inputs.input_ids.shape[1]
        pseudo_docs = self.tokenizer.batch_decode(
            generated_ids[:, input_lengths:],
            skip_special_tokens=True
        )
        
        # Combine original queries with pseudo-documents
        enhanced = [f"{q} {doc}" for q, doc in zip(queries, pseudo_docs)]
        
        return enhanced
    
    def enhance_batch(
        self, 
        queries: List[str], 
        query_ids: Optional[List[str]] = None,
        show_progress: bool = True
    ) -> List[str]:
        """
        Enhance batch of queries with parallel processing
        
        Processes queries in batches for optimal speed/memory tradeoff.
        
        Args:
            queries: List of query texts
            query_ids: Optional list of query identifiers
            show_progress: Show progress bar
            
        Returns:
            List of enhanced queries
        """
        if show_progress:
            try:
                from tqdm import tqdm
                use_tqdm = True
            except ImportError:
                use_tqdm = False
                print(f"Enhancing {len(queries)} queries in batches of {self.batch_size}...")
        else:
            use_tqdm = False
        
        enhanced = []
        
        # Process in batches
        num_batches = (len(queries) + self.batch_size - 1) // self.batch_size
        
        if use_tqdm:
            iterator = tqdm(range(num_batches), desc="Enhancing batches")
        else:
            iterator = range(num_batches)
        
        for batch_idx in iterator:
            start_idx = batch_idx * self.batch_size
            end_idx = min(start_idx + self.batch_size, len(queries))
            
            batch_queries = queries[start_idx:end_idx]
            batch_qids = query_ids[start_idx:end_idx] if query_ids else None
            
            # Process batch in parallel
            batch_enhanced = self.enhance_batch_parallel(batch_queries, batch_qids)
            enhanced.extend(batch_enhanced)
        
        return enhanced
