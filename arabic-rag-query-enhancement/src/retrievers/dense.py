"""
Dense Retriever using mDPR
GPU-accelerated implementation for fast query encoding
"""

import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from pyserini.search.faiss import FaissSearcher
from typing import List, Dict, Tuple
from tqdm import tqdm


class mDPRRetriever:
    """
    mDPR Dense Retriever with GPU acceleration
    """
    
    def __init__(
        self,
        index_name: str = "miracl-v1.0-ar-mdpr-tied-pft-msmarco",
        encoder_name: str = "castorini/mdpr-tied-pft-msmarco",
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        batch_size: int = 64
    ):
        """
        Initialize mDPR retriever
        
        Args:
            index_name: Pyserini prebuilt index name
            encoder_name: HuggingFace model name
            device: "cuda" or "cpu"
            batch_size: Batch size for encoding
        """
        self.index_name = index_name
        self.encoder_name = encoder_name
        self.device = torch.device(device)
        self.batch_size = batch_size
        
        print(f"Using device: {self.device}")
        
        # Load encoder on GPU
        print(f"Loading encoder: {encoder_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(encoder_name)
        self.model = AutoModel.from_pretrained(encoder_name).to(self.device)
        self.model.eval()
        print("✓ Encoder loaded")
        
        # Load FAISS index
        print(f"Loading FAISS index: {index_name}")
        print("⚠️ First run: downloading ~6GB (may take 5-10 minutes)")
        temp_searcher = FaissSearcher.from_prebuilt_index(index_name, encoder_name)
        self.index = temp_searcher.index
        self.docid_map = temp_searcher.docids
        print(f"✓ Index loaded: {self.index.ntotal:,} documents")
    
    @torch.no_grad()
    def encode_queries(self, queries: List[str], show_progress: bool = True) -> np.ndarray:
        """
        Encode queries on GPU in batches
        
        Args:
            queries: List of query texts
            show_progress: Show progress bar
            
        Returns:
            Numpy array of query embeddings (normalized)
        """
        all_embeddings = []
        
        iterator = range(0, len(queries), self.batch_size)
        if show_progress:
            iterator = tqdm(iterator, desc="Encoding queries")
        
        for i in iterator:
            batch = queries[i:i+self.batch_size]
            
            # Tokenize and move to GPU
            inputs = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors='pt'
            ).to(self.device)
            
            # Encode on GPU
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :]  # CLS token
            
            # Normalize for cosine similarity
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            
            all_embeddings.append(embeddings.cpu().numpy())
        
        return np.vstack(all_embeddings)
    
    def search(
        self,
        queries: List[str],
        k: int = 100,
        show_progress: bool = True
    ) -> Dict[int, List[Tuple[str, float]]]:
        """
        Search for multiple queries
        
        Args:
            queries: List of query texts
            k: Number of results per query
            show_progress: Show progress bar
            
        Returns:
            Dict mapping query_index -> [(docid, score), ...]
        """
        # Encode queries
        query_embeddings = self.encode_queries(queries, show_progress=show_progress)
        
        # Search FAISS index
        if show_progress:
            print("Searching FAISS index...")
        scores, indices = self.index.search(query_embeddings.astype('float32'), k)
        
        # Format results
        results = {}
        for i in range(len(queries)):
            results[i] = []
            for idx, score in zip(indices[i], scores[i]):
                if idx != -1:  # Valid result
                    docid = self.docid_map[idx]
                    results[i].append((docid, float(score)))
        
        return results
    
    def search_single(self, query: str, k: int = 100) -> List[Tuple[str, float]]:
        """
        Search for a single query
        
        Args:
            query: Query text
            k: Number of results
            
        Returns:
            List of (docid, score) tuples
        """
        results = self.search([query], k=k, show_progress=False)
        return results[0]


# Example usage
if __name__ == "__main__":
    # Initialize retriever
    retriever = mDPRRetriever()
    
    # Test single query
    test_query = "من هو رئيس مصر؟"
    results = retriever.search_single(test_query, k=10)
    
    print(f"\nQuery: {test_query}")
    print(f"Top 3 results:")
    for i, (docid, score) in enumerate(results[:3], 1):
        print(f"  {i}. {docid} (score: {score:.4f})")
