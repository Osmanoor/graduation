"""
Evaluation Metrics for Retrieval
Computes Recall@K, NDCG@K, MRR
"""

import pytrec_eval
from typing import Dict, List, Tuple
import json


class RetrievalEvaluator:
    """Evaluate retrieval results using standard IR metrics"""
    
    def __init__(self, qrels: Dict[str, Dict[str, int]]):
        """
        Initialize evaluator
        
        Args:
            qrels: Relevance judgments {query_id: {doc_id: relevance}}
        """
        # Convert to string keys for pytrec_eval
        self.qrels = {
            str(qid): {str(docid): int(rel) for docid, rel in docs.items()}
            for qid, docs in qrels.items()
        }
    
    def evaluate(
        self,
        results: Dict[str, Dict[str, float]],
        metrics: List[str] = None
    ) -> Dict[str, float]:
        """
        Evaluate retrieval results
        
        Args:
            results: Search results {query_id: {doc_id: score}}
            metrics: List of metrics to compute (default: recall_10, recall_100, ndcg_cut_10, recip_rank)
            
        Returns:
            Dict of aggregated metrics
        """
        if metrics is None:
            metrics = ['recall_10', 'recall_100', 'ndcg_cut_10', 'recip_rank']
        
        # Convert results to string keys
        results_str = {
            str(qid): {str(docid): float(score) for docid, score in docs.items()}
            for qid, docs in results.items()
        }
        
        # Evaluate
        evaluator = pytrec_eval.RelevanceEvaluator(self.qrels, set(metrics))
        eval_results = evaluator.evaluate(results_str)
        
        # Aggregate
        num_queries = len(eval_results)
        aggregated = {metric: 0.0 for metric in metrics}
        
        for qid in eval_results:
            for metric in metrics:
                aggregated[metric] += eval_results[qid][metric]
        
        # Average
        avg_metrics = {
            metric: score / num_queries 
            for metric, score in aggregated.items()
        }
        avg_metrics['num_queries'] = num_queries
        
        return avg_metrics
    
    def evaluate_per_query(
        self,
        results: Dict[str, Dict[str, float]],
        metrics: List[str] = None
    ) -> Dict[str, Dict[str, float]]:
        """
        Evaluate per-query (for error analysis)
        
        Args:
            results: Search results
            metrics: List of metrics
            
        Returns:
            Dict {query_id: {metric: score}}
        """
        if metrics is None:
            metrics = ['recall_10', 'recall_100', 'ndcg_cut_10', 'recip_rank']
        
        # Convert to string keys
        results_str = {
            str(qid): {str(docid): float(score) for docid, score in docs.items()}
            for qid, docs in results.items()
        }
        
        # Evaluate
        evaluator = pytrec_eval.RelevanceEvaluator(self.qrels, set(metrics))
        return evaluator.evaluate(results_str)


def save_results(
    results: Dict[str, Dict[str, float]],
    output_path: str,
    run_name: str = "run"
):
    """
    Save results in TREC format
    
    Args:
        results: Search results {query_id: {doc_id: score}}
        output_path: Output file path
        run_name: Run identifier
    """
    with open(output_path, 'w') as f:
        for qid, docs in results.items():
            # Sort by score (descending)
            sorted_docs = sorted(docs.items(), key=lambda x: x[1], reverse=True)
            
            for rank, (docid, score) in enumerate(sorted_docs, 1):
                f.write(f"{qid} Q0 {docid} {rank} {score:.6f} {run_name}\n")
    
    print(f"✓ Results saved to {output_path}")


def save_metrics(metrics: Dict[str, float], output_path: str):
    """
    Save metrics as JSON
    
    Args:
        metrics: Dict of metric values
        output_path: Output file path
    """
    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"✓ Metrics saved to {output_path}")


def print_metrics(metrics: Dict[str, float], title: str = "Results"):
    """
    Pretty print metrics
    
    Args:
        metrics: Dict of metric values
        title: Title to display
    """
    print("\n" + "="*60)
    print(title)
    print("="*60)
    
    # Order metrics
    metric_order = ['recall_10', 'recall_100', 'ndcg_cut_10', 'recip_rank', 'num_queries']
    
    for metric in metric_order:
        if metric in metrics:
            if metric == 'num_queries':
                print(f"Queries:    {int(metrics[metric])}")
            else:
                # Format metric name
                name = metric.replace('_', '@').replace('cut@', '@').replace('recip@rank', 'MRR')
                name = name.replace('recall', 'Recall').replace('ndcg', 'NDCG')
                print(f"{name:15s}: {metrics[metric]:.4f}")
    
    print("="*60)


# Example usage
if __name__ == "__main__":
    # Mock data for testing
    qrels = {
        "1": {"doc1": 1, "doc2": 1},
        "2": {"doc3": 1}
    }
    
    results = {
        "1": {"doc1": 0.9, "doc2": 0.8, "doc99": 0.7},
        "2": {"doc99": 0.9, "doc3": 0.8}
    }
    
    evaluator = RetrievalEvaluator(qrels)
    metrics = evaluator.evaluate(results)
    
    print_metrics(metrics, "Test Results")
