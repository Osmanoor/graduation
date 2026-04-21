"""
Contrastive Dense Retriever
Performs contrastive scoring using positive and negative hypothetical documents
"""

import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from typing import List, Dict, Tuple
from tqdm import tqdm


class ContrastiveDenseRetriever:
    """
    Dense retriever with contrastive scoring
    
    Score(D) = α * sim(Query, D) + β * sim(PosHyDE, D) - γ * sim(NegHyDE, D)
    """
    
    def __init__(
        self,
        index,
        docid_map,
        encoder_name: str = "castorini/mdpr-tied-pft-msmarco",
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        batch_size: int = 64,
        alpha: float = 0.4,
        beta: float = 0.4,
        gamma: float = 0.2
    ):
        """
        Initialize contrastive retriever
        
        Args:
            index: FAISS index
            docid_map: Document ID mapping
            encoder_name: HuggingFace model name
            device: "cuda" or "cpu"
            batch_size: Batch size for encoding
            alpha: Weight for query-document similarity
            beta: Weight for positive HyDE-document similarity
            gamma: Weight for negative HyDE-document similarity (subtracted)
        """
        self.index = index
        self.docid_map = docid_map
        self.encoder_name = encoder_name
        self.device = torch.device(device)
        self.batch_size = batch_size
        
        # Contrastive weights
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        
        print(f"Using device: {self.device}")
        print(f"Contrastive weights: α={alpha}, β={beta}, γ={gamma}")
        
        # Load encoder
        print(f"Loading encoder: {encoder_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(encoder_name)
        self.model = AutoModel.from_pretrained(encoder_name).to(self.device)
        self.model.eval()
        print("✓ Encoder loaded")
    
    @torch.no_grad()
    def encode_texts(self, texts: List[str], show_progress: bool = True, desc: str = "Encoding") -> np.ndarray:
        """
        Encode texts on GPU in batches
        
        Args:
            texts: List of texts
            show_progress: Show progress bar
            desc: Progress bar description
            
        Returns:
            Numpy array of embeddings (normalized)
        """
        all_embeddings = []
        
        iterator = range(0, len(texts), self.batch_size)
        if show_progress:
            iterator = tqdm(iterator, desc=desc)
        
        for i in iterator:
            batch = texts[i:i+self.batch_size]
            
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
    
    def contrastive_search(
        self,
        queries: List[str],
        positive_docs: List[str],
        negative_docs: List[str],
        k: int = 100,
        show_progress: bool = True
    ) -> Dict[int, List[Tuple[str, float]]]:
        """
        Perform contrastive retrieval
        
        Args:
            queries: List of query texts
            positive_docs: List of positive hypothetical documents
            negative_docs: List of negative hypothetical documents
            k: Number of results per query
            show_progress: Show progress bar
            
        Returns:
            Dict mapping query_index -> [(docid, score), ...]
        """
        # Encode all components
        print("\nEncoding queries and hypothetical documents...")
        query_embeddings = self.encode_texts(queries, show_progress, "Encoding queries")
        pos_embeddings = self.encode_texts(positive_docs, show_progress, "Encoding positive docs")
        neg_embeddings = self.encode_texts(negative_docs, show_progress, "Encoding negative docs")
        
        # Retrieve candidate documents using query embeddings
        # Get more candidates than k to allow for re-ranking
        candidate_k = min(k * 3, 1000)  # 3x candidates for re-ranking
        
        if show_progress:
            print(f"\nRetrieving {candidate_k} candidates per query...")
        
        candidate_scores, candidate_indices = self.index.search(
            query_embeddings.astype('float32'), 
            candidate_k
        )
        
        # Perform contrastive re-ranking
        if show_progress:
            print("\nPerforming contrastive re-ranking...")
        
        results = {}
        
        iterator = range(len(queries))
        if show_progress:
            iterator = tqdm(iterator, desc="Re-ranking")
        
        for i in iterator:
            # Get candidate document embeddings from index
            valid_indices = candidate_indices[i][candidate_indices[i] != -1]
            
            if len(valid_indices) == 0:
                results[i] = []
                continue
            
            # Get document embeddings from FAISS index
            doc_embeddings = np.array([
                self.index.reconstruct(int(idx)) 
                for idx in valid_indices
            ])
            
            # Normalize document embeddings
            doc_embeddings = doc_embeddings / np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
            
            # Compute contrastive scores
            query_sim = np.dot(doc_embeddings, query_embeddings[i])
            pos_sim = np.dot(doc_embeddings, pos_embeddings[i])
            neg_sim = np.dot(doc_embeddings, neg_embeddings[i])
            
            # Contrastive scoring formula
            contrastive_scores = (
                self.alpha * query_sim + 
                self.beta * pos_sim - 
                self.gamma * neg_sim
            )
            
            # Sort by contrastive score
            sorted_idx = np.argsort(-contrastive_scores)[:k]
            
            # Format results
            results[i] = [
                (self.docid_map[valid_indices[idx]], float(contrastive_scores[idx]))
                for idx in sorted_idx
            ]
        
        return results
    
    def search_single(
        self,
        query: str,
        positive_doc: str,
        negative_doc: str,
        k: int = 100
    ) -> List[Tuple[str, float]]:
        """
        Search for a single query with contrastive scoring
        
        Args:
            query: Query text
            positive_doc: Positive hypothetical document
            negative_doc: Negative hypothetical document
            k: Number of results
            
        Returns:
            List of (docid, score) tuples
        """
        results = self.contrastive_search(
            [query], 
            [positive_doc], 
            [negative_doc], 
            k=k, 
            show_progress=False
        )
        return results[0]
