"""
BM25S Retriever - Pure Python Implementation
No Java dependencies required
"""

import bm25s
import Stemmer
import pickle
import os
from typing import List, Dict, Tuple
from tqdm import tqdm


class BM25SRetriever:
    """
    BM25S Retriever using pre-built index
    """
    
    def __init__(
        self,
        index_path: str = "data/miracl_ar/bm25s_index",
        corpus_ids_path: str = "data/miracl_ar/corpus_ids.pkl",
        stemmer_lang: str = "arabic"
    ):
        """
        Initialize BM25S retriever from saved index
        
        Args:
            index_path: Path to saved BM25S index directory
            corpus_ids_path: Path to pickled corpus IDs
            stemmer_lang: Language for stemming (default: arabic)
        """
        self.index_path = index_path
        self.corpus_ids_path = corpus_ids_path
        
        # Verify paths exist
        if not os.path.exists(index_path):
            raise FileNotFoundError(
                f"Index not found at {index_path}. "
                "Please run indexing first or mount Google Drive."
            )
        
        if not os.path.exists(corpus_ids_path):
            raise FileNotFoundError(
                f"Corpus IDs not found at {corpus_ids_path}. "
                "Please run indexing first or mount Google Drive."
            )
        
        # Load index
        print(f"Loading BM25S index from {index_path}...")
        self.retriever = bm25s.BM25.load(index_path, load_corpus=True)
        
        # Load corpus IDs
        print(f"Loading corpus IDs from {corpus_ids_path}...")
        with open(corpus_ids_path, 'rb') as f:
            self.corpus_ids = pickle.load(f)
        
        print(f"✓ Index loaded: {len(self.corpus_ids):,} documents")
        
        # Setup stemmer
        self.stemmer = Stemmer.Stemmer(stemmer_lang)
        
        # Setup stopwords (will be loaded when needed)
        self.stopwords = None
    
    def _get_stopwords(self):
        """Lazy load stopwords"""
        if self.stopwords is None:
            import nltk
            from nltk.corpus import stopwords
            
            # Download if needed
            try:
                self.stopwords = stopwords.words('arabic')
            except LookupError:
                print("Downloading Arabic stopwords...")
                nltk.download('stopwords', quiet=True)
                self.stopwords = stopwords.words('arabic')
        
        return self.stopwords
    
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
        # Tokenize queries
        if show_progress:
            print(f"Tokenizing {len(queries)} queries...")
        
        query_tokens = bm25s.tokenize(
            queries,
            stopwords=self._get_stopwords(),
            stemmer=self.stemmer,
            show_progress=show_progress
        )
        
        # Retrieve
        if show_progress:
            print(f"Retrieving top {k} documents per query...")
        
        results_indices, scores = self.retriever.retrieve(
            query_tokens,
            k=k,
            show_progress=show_progress
        )
        
        # Format results
        results = {}
        for i in range(len(queries)):
            results[i] = []
            doc_indices = results_indices[i]
            doc_scores = scores[i]
            
            for doc_idx, score in zip(doc_indices, doc_scores):
                docid = self.corpus_ids[doc_idx]
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
    retriever = BM25SRetriever()
    
    # Test single query
    test_query = "من هو رئيس مصر؟"
    results = retriever.search_single(test_query, k=10)
    
    print(f"\nQuery: {test_query}")
    print(f"Top 3 results:")
    for i, (docid, score) in enumerate(results[:3], 1):
        print(f"  {i}. {docid} (score: {score:.4f})")
