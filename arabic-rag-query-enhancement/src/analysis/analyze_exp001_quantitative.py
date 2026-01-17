"""
Quantitative Error Analysis for Experiment 001 (Dense Baseline)

Analyzes:
1. Per-query metrics (NDCG@10, Recall@10, MRR)
2. Query length distribution and correlation
3. Score gaps (confidence analysis)
4. Rank distribution of relevant documents
5. Failure segmentation

No GPU required - runs locally.
"""

import json
import os
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict, Counter


def compute_per_query_metrics(topics: Dict, qrels: Dict, results: Dict) -> Dict:
    """
    Compute NDCG@10, Recall@10, MRR for each query
    
    Args:
        topics: Query texts
        qrels: Relevance judgments
        results: Retrieval results
        
    Returns:
        Dict mapping query_id -> {ndcg_10, recall_10, mrr, ...}
    """
    print("Computing per-query metrics...")
    
    per_query = {}
    
    for qid in topics.keys():
        if qid not in results or qid not in qrels:
            continue
        
        retrieved = results[qid][:10]  # Top-10
        relevant_docs = set(qrels[qid].keys())
        
        # Recall@10
        retrieved_ids = {doc['doc_id'] for doc in retrieved}
        relevant_retrieved = retrieved_ids & relevant_docs
        recall_10 = len(relevant_retrieved) / len(relevant_docs) if relevant_docs else 0.0
        
        # MRR
        mrr = 0.0
        for i, doc in enumerate(retrieved, 1):
            if doc['doc_id'] in relevant_docs:
                mrr = 1.0 / i
                break
        
        # NDCG@10 (simplified - binary relevance)
        dcg = 0.0
        for i, doc in enumerate(retrieved, 1):
            if doc['doc_id'] in relevant_docs:
                dcg += 1.0 / np.log2(i + 1)
        
        # IDCG (ideal DCG)
        idcg = sum(1.0 / np.log2(i + 1) for i in range(1, min(len(relevant_docs), 10) + 1))
        ndcg_10 = dcg / idcg if idcg > 0 else 0.0
        
        per_query[qid] = {
            'ndcg_10': ndcg_10,
            'recall_10': recall_10,
            'mrr': mrr,
            'num_relevant': len(relevant_docs),
            'num_retrieved_relevant': len(relevant_retrieved)
        }
    
    print(f"✓ Computed metrics for {len(per_query)} queries")
    return per_query


def analyze_query_length(topics: Dict, per_query_metrics: Dict) -> Dict:
    """
    Analyze query length distribution and correlation with performance
    
    Args:
        topics: Query texts
        per_query_metrics: Per-query metrics
        
    Returns:
        Dict with length statistics and correlations
    """
    print("Analyzing query length...")
    
    lengths = []
    ndcg_by_length = defaultdict(list)
    
    for qid, query_text in topics.items():
        if qid not in per_query_metrics:
            continue
        
        # Simple whitespace tokenization (good enough for Arabic)
        length = len(query_text.split())
        lengths.append(length)
        
        ndcg = per_query_metrics[qid]['ndcg_10']
        ndcg_by_length[length].append(ndcg)
    
    # Statistics
    stats = {
        'min': int(np.min(lengths)),
        'max': int(np.max(lengths)),
        'mean': float(np.mean(lengths)),
        'median': float(np.median(lengths)),
        'std': float(np.std(lengths))
    }
    
    # Correlation (Pearson)
    lengths_array = []
    ndcg_array = []
    for qid in per_query_metrics.keys():
        if qid in topics:
            lengths_array.append(len(topics[qid].split()))
            ndcg_array.append(per_query_metrics[qid]['ndcg_10'])
    
    correlation = float(np.corrcoef(lengths_array, ndcg_array)[0, 1])
    
    # Average NDCG by length bucket
    length_buckets = {
        'short (1-3)': [],
        'medium (4-8)': [],
        'long (9+)': []
    }
    
    for qid, query_text in topics.items():
        if qid not in per_query_metrics:
            continue
        
        length = len(query_text.split())
        ndcg = per_query_metrics[qid]['ndcg_10']
        
        if length <= 3:
            length_buckets['short (1-3)'].append(ndcg)
        elif length <= 8:
            length_buckets['medium (4-8)'].append(ndcg)
        else:
            length_buckets['long (9+)'].append(ndcg)
    
    avg_ndcg_by_bucket = {
        bucket: float(np.mean(ndcgs)) if ndcgs else 0.0
        for bucket, ndcgs in length_buckets.items()
    }
    
    result = {
        'statistics': stats,
        'correlation_with_ndcg': correlation,
        'avg_ndcg_by_length_bucket': avg_ndcg_by_bucket,
        'num_queries_by_bucket': {
            bucket: len(ndcgs) for bucket, ndcgs in length_buckets.items()
        }
    }
    
    print(f"✓ Length analysis complete")
    print(f"  Mean length: {stats['mean']:.1f} tokens")
    print(f"  Correlation with NDCG: {correlation:.3f}")
    
    return result


def analyze_score_gaps(results: Dict, per_query_metrics: Dict) -> Dict:
    """
    Analyze score gaps (top-1 vs top-2) as confidence indicator
    
    Args:
        results: Retrieval results
        per_query_metrics: Per-query metrics
        
    Returns:
        Dict with score gap statistics
    """
    print("Analyzing score gaps...")
    
    score_gaps = []
    gaps_by_performance = {
        'failed': [],
        'mediocre': [],
        'successful': []
    }
    
    for qid, docs in results.items():
        if qid not in per_query_metrics or len(docs) < 2:
            continue
        
        # Score gap = top-1 score - top-2 score
        gap = docs[0]['score'] - docs[1]['score']
        score_gaps.append(gap)
        
        # Categorize by performance
        ndcg = per_query_metrics[qid]['ndcg_10']
        if ndcg < 0.3:
            gaps_by_performance['failed'].append(gap)
        elif ndcg < 0.7:
            gaps_by_performance['mediocre'].append(gap)
        else:
            gaps_by_performance['successful'].append(gap)
    
    # Statistics
    stats = {
        'mean': float(np.mean(score_gaps)),
        'median': float(np.median(score_gaps)),
        'std': float(np.std(score_gaps)),
        'min': float(np.min(score_gaps)),
        'max': float(np.max(score_gaps))
    }
    
    # Average gap by performance category
    avg_gap_by_category = {
        category: float(np.mean(gaps)) if gaps else 0.0
        for category, gaps in gaps_by_performance.items()
    }
    
    result = {
        'statistics': stats,
        'avg_gap_by_performance': avg_gap_by_category,
        'num_queries_by_performance': {
            category: len(gaps) for category, gaps in gaps_by_performance.items()
        }
    }
    
    print(f"✓ Score gap analysis complete")
    print(f"  Mean gap: {stats['mean']:.4f}")
    
    return result


def analyze_rank_distribution(qrels: Dict, results: Dict) -> Dict:
    """
    Analyze where relevant documents land in rankings
    
    Args:
        qrels: Relevance judgments
        results: Retrieval results
        
    Returns:
        Dict with rank distribution statistics
    """
    print("Analyzing rank distribution...")
    
    first_relevant_ranks = []
    all_relevant_ranks = []
    
    queries_with_relevant_in_top_k = {
        10: 0,
        20: 0,
        50: 0,
        100: 0
    }
    
    for qid, relevant_docs in qrels.items():
        if qid not in results:
            continue
        
        retrieved = results[qid]
        relevant_set = set(relevant_docs.keys())
        
        # Find ranks of relevant documents
        relevant_ranks_this_query = []
        first_relevant_rank = None
        
        for doc in retrieved:
            if doc['doc_id'] in relevant_set:
                rank = doc['rank']
                relevant_ranks_this_query.append(rank)
                all_relevant_ranks.append(rank)
                
                if first_relevant_rank is None:
                    first_relevant_rank = rank
                    first_relevant_ranks.append(rank)
        
        # Count queries with relevant in top-k
        if relevant_ranks_this_query:
            for k in [10, 20, 50, 100]:
                if any(r <= k for r in relevant_ranks_this_query):
                    queries_with_relevant_in_top_k[k] += 1
    
    # Statistics
    total_queries = len([qid for qid in qrels if qid in results])
    
    result = {
        'first_relevant_rank': {
            'mean': float(np.mean(first_relevant_ranks)) if first_relevant_ranks else 0.0,
            'median': float(np.median(first_relevant_ranks)) if first_relevant_ranks else 0.0,
            'min': int(np.min(first_relevant_ranks)) if first_relevant_ranks else 0,
            'max': int(np.max(first_relevant_ranks)) if first_relevant_ranks else 0
        },
        'percent_with_relevant_in_top_k': {
            k: float(count / total_queries * 100) if total_queries > 0 else 0.0
            for k, count in queries_with_relevant_in_top_k.items()
        },
        'total_queries_analyzed': total_queries
    }
    
    print(f"✓ Rank distribution analysis complete")
    print(f"  Queries with relevant in top-10: {result['percent_with_relevant_in_top_k'][10]:.1f}%")
    
    return result


def segment_by_performance(per_query_metrics: Dict, topics: Dict) -> Dict:
    """
    Segment queries by performance level
    
    Args:
        per_query_metrics: Per-query metrics
        topics: Query texts
        
    Returns:
        Dict with segmented query IDs and statistics
    """
    print("Segmenting queries by performance...")
    
    failed = []
    mediocre = []
    successful = []
    
    for qid, metrics in per_query_metrics.items():
        ndcg = metrics['ndcg_10']
        
        if ndcg < 0.3:
            failed.append(qid)
        elif ndcg < 0.7:
            mediocre.append(qid)
        else:
            successful.append(qid)
    
    # Sort by NDCG (worst first for failed, best first for successful)
    failed.sort(key=lambda qid: per_query_metrics[qid]['ndcg_10'])
    successful.sort(key=lambda qid: per_query_metrics[qid]['ndcg_10'], reverse=True)
    
    result = {
        'failed': {
            'query_ids': failed,
            'count': len(failed),
            'percent': float(len(failed) / len(per_query_metrics) * 100),
            'avg_ndcg': float(np.mean([per_query_metrics[qid]['ndcg_10'] for qid in failed])) if failed else 0.0
        },
        'mediocre': {
            'query_ids': mediocre,
            'count': len(mediocre),
            'percent': float(len(mediocre) / len(per_query_metrics) * 100),
            'avg_ndcg': float(np.mean([per_query_metrics[qid]['ndcg_10'] for qid in mediocre])) if mediocre else 0.0
        },
        'successful': {
            'query_ids': successful,
            'count': len(successful),
            'percent': float(len(successful) / len(per_query_metrics) * 100),
            'avg_ndcg': float(np.mean([per_query_metrics[qid]['ndcg_10'] for qid in successful])) if successful else 0.0
        }
    }
    
    print(f"✓ Performance segmentation complete")
    print(f"  Failed (NDCG<0.3): {result['failed']['count']} ({result['failed']['percent']:.1f}%)")
    print(f"  Mediocre (0.3≤NDCG<0.7): {result['mediocre']['count']} ({result['mediocre']['percent']:.1f}%)")
    print(f"  Successful (NDCG≥0.7): {result['successful']['count']} ({result['successful']['percent']:.1f}%)")
    
    return result


def run_quantitative_analysis(topics: Dict, qrels: Dict, results: Dict, output_dir="results/baseline_dense"):
    """
    Run complete quantitative analysis
    
    Args:
        topics: Query texts
        qrels: Relevance judgments
        results: Retrieval results
        output_dir: Where to save analysis results
        
    Returns:
        Dict with all analysis results
    """
    print("\n" + "="*60)
    print("QUANTITATIVE ERROR ANALYSIS - EXPERIMENT 001")
    print("="*60 + "\n")
    
    # 1. Per-query metrics
    per_query_metrics = compute_per_query_metrics(topics, qrels, results)
    
    # 2. Query length analysis
    length_analysis = analyze_query_length(topics, per_query_metrics)
    
    # 3. Score gap analysis
    score_gap_analysis = analyze_score_gaps(results, per_query_metrics)
    
    # 4. Rank distribution
    rank_analysis = analyze_rank_distribution(qrels, results)
    
    # 5. Performance segmentation
    segmentation = segment_by_performance(per_query_metrics, topics)
    
    # Compile results
    analysis_results = {
        'experiment': 'exp_001_baseline_dense',
        'total_queries': len(topics),
        'queries_analyzed': len(per_query_metrics),
        'per_query_metrics': per_query_metrics,
        'length_analysis': length_analysis,
        'score_gap_analysis': score_gap_analysis,
        'rank_distribution': rank_analysis,
        'performance_segmentation': segmentation
    }
    
    # Save results
    os.makedirs(output_dir, exist_ok=True)
    
    # Full analysis
    output_path = os.path.join(output_dir, "exp_001_quantitative_analysis.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Full analysis saved to {output_path}")
    
    # Failed queries (for qualitative analysis)
    failed_queries_data = {
        qid: {
            'query_text': topics[qid],
            'ndcg_10': per_query_metrics[qid]['ndcg_10'],
            'recall_10': per_query_metrics[qid]['recall_10'],
            'mrr': per_query_metrics[qid]['mrr'],
            'num_relevant': per_query_metrics[qid]['num_relevant']
        }
        for qid in segmentation['failed']['query_ids']
    }
    
    failed_path = os.path.join(output_dir, "exp_001_failed_queries.json")
    with open(failed_path, 'w', encoding='utf-8') as f:
        json.dump(failed_queries_data, f, ensure_ascii=False, indent=2)
    print(f"✓ Failed queries saved to {failed_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total queries analyzed: {len(per_query_metrics)}")
    print(f"\nQuery Length:")
    print(f"  Mean: {length_analysis['statistics']['mean']:.1f} tokens")
    print(f"  Correlation with NDCG: {length_analysis['correlation_with_ndcg']:.3f}")
    print(f"\nScore Gaps:")
    print(f"  Mean: {score_gap_analysis['statistics']['mean']:.4f}")
    print(f"  Failed queries: {score_gap_analysis['avg_gap_by_performance']['failed']:.4f}")
    print(f"  Successful queries: {score_gap_analysis['avg_gap_by_performance']['successful']:.4f}")
    print(f"\nRank Distribution:")
    print(f"  Relevant in top-10: {rank_analysis['percent_with_relevant_in_top_k'][10]:.1f}%")
    print(f"  Relevant in top-100: {rank_analysis['percent_with_relevant_in_top_k'][100]:.1f}%")
    print(f"\nPerformance Segmentation:")
    print(f"  Failed (NDCG<0.3): {segmentation['failed']['count']} ({segmentation['failed']['percent']:.1f}%)")
    print(f"  Mediocre: {segmentation['mediocre']['count']} ({segmentation['mediocre']['percent']:.1f}%)")
    print(f"  Successful (NDCG≥0.7): {segmentation['successful']['count']} ({segmentation['successful']['percent']:.1f}%)")
    print("="*60 + "\n")
    
    return analysis_results


# Example usage
if __name__ == "__main__":
    from load_exp001_data import load_experiment_data
    
    # Load data
    topics, qrels, results = load_experiment_data()
    
    # Run analysis
    analysis = run_quantitative_analysis(topics, qrels, results)
