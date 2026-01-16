"""
Data Loader for MIRACL Dataset
Handles loading topics, qrels, and corpus from Pyserini
"""

from pyserini.search import get_topics, get_qrels
from typing import Dict, Tuple


class MIRACLDataLoader:
    """Load MIRACL Arabic dataset"""
    
    def __init__(self, language: str = "ar", split: str = "dev"):
        """
        Initialize data loader
        
        Args:
            language: Language code (default: "ar" for Arabic)
            split: Dataset split ("dev" or "test")
        """
        self.language = language
        self.split = split
        self.dataset_name = f"miracl-v1.0-{language}-{split}"
        
        self.topics = None
        self.qrels = None
    
    def load_topics(self) -> Dict[str, Dict[str, str]]:
        """
        Load query topics
        
        Returns:
            Dict mapping query_id -> {'title': query_text, ...}
        """
        if self.topics is None:
            print(f"Loading topics from {self.dataset_name}...")
            self.topics = get_topics(self.dataset_name)
            print(f"✓ Loaded {len(self.topics)} queries")
        
        return self.topics
    
    def load_qrels(self) -> Dict[str, Dict[str, int]]:
        """
        Load relevance judgments
        
        Returns:
            Dict mapping query_id -> {doc_id: relevance_score}
        """
        if self.qrels is None:
            print(f"Loading qrels from {self.dataset_name}...")
            self.qrels = get_qrels(self.dataset_name)
            print(f"✓ Loaded qrels for {len(self.qrels)} queries")
        
        return self.qrels
    
    def load_all(self) -> Tuple[Dict, Dict]:
        """
        Load both topics and qrels
        
        Returns:
            Tuple of (topics, qrels)
        """
        topics = self.load_topics()
        qrels = self.load_qrels()
        return topics, qrels
    
    def get_query_text(self, query_id: str) -> str:
        """Get query text by ID"""
        if self.topics is None:
            self.load_topics()
        return self.topics[query_id]['title']
    
    def get_relevant_docs(self, query_id: str) -> Dict[str, int]:
        """Get relevant documents for a query"""
        if self.qrels is None:
            self.load_qrels()
        return self.qrels.get(query_id, {})


# Example usage
if __name__ == "__main__":
    loader = MIRACLDataLoader(language="ar", split="dev")
    topics, qrels = loader.load_all()
    
    # Show sample
    sample_qid = list(topics.keys())[0]
    print(f"\nSample Query:")
    print(f"  ID: {sample_qid}")
    print(f"  Text: {topics[sample_qid]['title']}")
    print(f"  Relevant docs: {len(qrels.get(sample_qid, {}))}")
