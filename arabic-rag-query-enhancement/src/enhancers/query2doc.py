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
    """
    
    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-3B-Instruct",
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
        device: str = "auto"
    ):
        """
        Initialize Query2Doc enhancer
        
        Args:
            model_name: HuggingFace model identifier
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature (lower = more focused)
            top_p: Nucleus sampling parameter
            device: Device placement ("auto", "cuda", "cpu")
        """
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.top_p = top_p
        
        print(f"Loading {model_name} in float16...")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Load model in float16 for efficiency
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map=device
        )
        
        print(f"✓ Model loaded on {self.model.device}")
        
        # System prompt from Query2Doc paper
        self.system_prompt = (
            "You are asked to write a passage that answers the given query. "
            "Do not ask the user for further clarification"
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
                top_p=self.top_p
            )
        
        # Decode response
        generated_ids = [
            output_ids[len(input_ids):] 
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        pseudo_doc = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # Combine: original query + pseudo-document
        # For dense retrieval, simple concatenation works
        enhanced = f"{query} {pseudo_doc}"
        
        return enhanced
    
    def enhance_batch(
        self, 
        queries: List[str], 
        query_ids: Optional[List[str]] = None,
        show_progress: bool = True
    ) -> List[str]:
        """
        Enhance batch of queries
        
        Note: Processes sequentially due to generation requirements
        
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
                iterator = tqdm(queries, desc="Enhancing queries")
            except ImportError:
                iterator = queries
                print(f"Enhancing {len(queries)} queries...")
        else:
            iterator = queries
        
        enhanced = []
        for i, query in enumerate(iterator):
            qid = query_ids[i] if query_ids else None
            enhanced_query = self.enhance(query, qid)
            enhanced.append(enhanced_query)
        
        return enhanced
