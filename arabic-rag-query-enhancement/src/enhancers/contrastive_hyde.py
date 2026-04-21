"""
Contrastive HyDE Query Enhancer
Generates both positive and negative hypothetical documents for contrastive retrieval
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import List, Optional, Tuple
from .base import QueryEnhancer


class ContrastiveHyDEEnhancer(QueryEnhancer):
    """
    Contrastive HyDE enhancer using Qwen 2.5
    
    Generates:
    1. Positive hypothetical document (answers the query)
    2. Negative hypothetical document (related but doesn't answer)
    
    Used for contrastive retrieval scoring.
    """
    
    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-3B-Instruct",
        max_new_tokens: int = 128,
        temperature: float = 0.7,
        top_p: float = 0.9,
        device: str = "auto",
        batch_size: int = 8
    ):
        """
        Initialize Contrastive HyDE enhancer
        
        Args:
            model_name: HuggingFace model identifier
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            device: Device placement ("auto", "cuda", "cpu")
            batch_size: Number of queries to process in parallel
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
        
        # Set left padding for decoder-only models
        self.tokenizer.padding_side = 'left'
        
        # Load model in float16
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map=device
        )
        
        self.model.eval()
        
        print(f"✓ Model loaded on {self.model.device}")
        print(f"✓ Batch size: {batch_size}")
        print(f"✓ Max tokens: {max_new_tokens}")
        
        # Prompts for positive and negative generation
        self.positive_system_prompt = (
            "You are asked to write a passage that answers the given query. "
            "Do not ask the user for further clarification. "
            "Respond in Arabic only."
        )
        
        self.negative_system_prompt = (
            "You are asked to write a passage that is semantically related to the query "
            "but does NOT answer it. The passage should discuss related topics or concepts "
            "without providing the information requested in the query. "
            "Respond in Arabic only."
        )
    
    def generate_positive(self, query: str) -> str:
        """Generate positive hypothetical document (answers query)"""
        messages = [
            {"role": "system", "content": self.positive_system_prompt},
            {"role": "user", "content": query}
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
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
        
        generated_ids = [
            output_ids[len(input_ids):] 
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    def generate_negative(self, query: str) -> str:
        """Generate negative hypothetical document (related but doesn't answer)"""
        messages = [
            {"role": "system", "content": self.negative_system_prompt},
            {"role": "user", "content": query}
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
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
        
        generated_ids = [
            output_ids[len(input_ids):] 
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    def enhance(self, query: str, query_id: str = None) -> Tuple[str, str]:
        """
        Generate both positive and negative hypothetical documents
        
        Args:
            query: Original query text
            query_id: Optional query identifier
            
        Returns:
            Tuple of (positive_doc, negative_doc)
        """
        pos_doc = self.generate_positive(query)
        neg_doc = self.generate_negative(query)
        return pos_doc, neg_doc
    
    def enhance_batch_parallel(
        self,
        queries: List[str],
        doc_type: str = "positive"
    ) -> List[str]:
        """
        Generate hypothetical documents for a batch in parallel
        
        Args:
            queries: List of query texts
            doc_type: "positive" or "negative"
            
        Returns:
            List of generated documents
        """
        system_prompt = (
            self.positive_system_prompt if doc_type == "positive" 
            else self.negative_system_prompt
        )
        
        # Format all prompts
        all_messages = [
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
            for query in queries
        ]
        
        # Apply chat template
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
        
        # Generate
        with torch.no_grad():
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id
            )
        
        # Decode
        input_lengths = model_inputs.input_ids.shape[1]
        docs = self.tokenizer.batch_decode(
            generated_ids[:, input_lengths:],
            skip_special_tokens=True
        )
        
        return docs
    
    def enhance_batch(
        self,
        queries: List[str],
        query_ids: Optional[List[str]] = None,
        show_progress: bool = True
    ) -> Tuple[List[str], List[str]]:
        """
        Generate positive and negative documents for all queries
        
        Args:
            queries: List of query texts
            query_ids: Optional list of query identifiers
            show_progress: Show progress bar
            
        Returns:
            Tuple of (positive_docs, negative_docs)
        """
        if show_progress:
            try:
                from tqdm import tqdm
                use_tqdm = True
            except ImportError:
                use_tqdm = False
                print(f"Generating documents for {len(queries)} queries...")
        else:
            use_tqdm = False
        
        positive_docs = []
        negative_docs = []
        
        num_batches = (len(queries) + self.batch_size - 1) // self.batch_size
        
        # Generate positive documents
        if use_tqdm:
            iterator = tqdm(range(num_batches), desc="Generating positive docs")
        else:
            iterator = range(num_batches)
            print("Generating positive documents...")
        
        for batch_idx in iterator:
            start_idx = batch_idx * self.batch_size
            end_idx = min(start_idx + self.batch_size, len(queries))
            batch_queries = queries[start_idx:end_idx]
            
            batch_docs = self.enhance_batch_parallel(batch_queries, doc_type="positive")
            positive_docs.extend(batch_docs)
        
        # Generate negative documents
        if use_tqdm:
            iterator = tqdm(range(num_batches), desc="Generating negative docs")
        else:
            iterator = range(num_batches)
            print("Generating negative documents...")
        
        for batch_idx in iterator:
            start_idx = batch_idx * self.batch_size
            end_idx = min(start_idx + self.batch_size, len(queries))
            batch_queries = queries[start_idx:end_idx]
            
            batch_docs = self.enhance_batch_parallel(batch_queries, doc_type="negative")
            negative_docs.extend(batch_docs)
        
        return positive_docs, negative_docs
