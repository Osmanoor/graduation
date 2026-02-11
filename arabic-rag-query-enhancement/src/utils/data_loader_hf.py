"""
Data Loader for MIRACL Dataset from HuggingFace
Loads topics and qrels directly from HuggingFace URLs
"""

import requests
from typing import Dict, Tuple


class MIRACLDataLoader:
    """Load MIRACL Arabic dataset from HuggingFace"""
    
    def __init__(self, language: str = "ar", split: str = "dev"):
        """
        Initialize data loader
        
        Args:
            language: Language code (default: "ar" for Arabic)
            split: Dataset split ("dev" or "test")
        """
        self.language = language
        self.split = split
        
        # HuggingFace URLs
        base_url = "https://huggingface.co/datasets/miracl/miracl/resolve/main"
        self.topics_url = f"{base_url}/miracl-v1.0-{language}/topics/topics.miracl-v1.0-{language}-{split}.tsv"
        self.qrels_url = f"{base_url}/miracl-v1.0-{language}/qrels/qrels.miracl-v1.0-{language}-{split}.tsv"
        
        self.topics = None
        self.qrels = None
    
    def load_topics(self) -> Dict[str, Dict[str, str]]:
        """
        Load query topics from HuggingFace
        
        Returns:
            Dict mapping query_id -> {'title': query_text}
        """
        if self.topics is None:
            print(f"Loading topics from HuggingFace...")
            response = requests.get(self.topics_url)
            response.raise_for_status()
            
            self.topics = {}
            for line in response.text.strip().split('\n'):
                qid, query = line.strip().split('\t')
                self.topics[qid] = {'title': query}
            
            print(f"✓ Loaded {len(self.topics)} queries")
        
        return self.topics
    
    def load_qrels(self) -> Dict[str, Dict[str, int]]:
        """
        Load relevance judgments from HuggingFace
        
        Returns:
            Dict mapping query_id -> {doc_id: relevance_score}
        """
        if self.qrels is None:
            print(f"Loading qrels from HuggingFace...")
            response = requests.get(self.qrels_url)
            response.raise_for_status()
            
            self.qrels = {}
            for line in response.text.strip().split('\n'):
                parts = line.strip().split('\t')
                qid, _, docid, rel = parts
                if qid not in self.qrels:
                    self.qrels[qid] = {}
                self.qrels[qid][docid] = int(rel)
            
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
