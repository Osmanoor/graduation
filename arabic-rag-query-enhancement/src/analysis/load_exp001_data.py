"""
Data Loader for Experiment 001 Error Analysis

Loads topics, qrels, and results from HuggingFace and local files.
No Pyserini/Java required - pure Python.
"""

import json
import os
import requests
from typing import Dict, Tuple
from collections import defaultdict


def download_miracl_topics(language="ar", split="dev", output_dir="data/processed"):
    """
    Download MIRACL topics (queries) from HuggingFace
    
    Args:
        language: Language code (default: "ar")
        split: Dataset split (default: "dev")
        output_dir: Where to save the JSON file
        
    Returns:
        Dict mapping query_id -> query_text
    """
    os.makedirs(output_dir, exist_ok=True)
    
    url = f"https://huggingface.co/datasets/miracl/miracl/resolve/main/miracl-v1.0-{language}/topics/topics.miracl-v1.0-{language}-{split}.tsv"
    
    print(f"Downloading topics from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    
    # Parse TSV
    topics = {}
    for line in response.text.strip().split('\n'):
        qid, query = line.split('\t')
        topics[qid] = query
    
    # Save to JSON
    output_path = os.path.join(output_dir, f"exp001_topics.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Loaded {len(topics)} queries")
    print(f"✓ Saved to {output_path}")
    
    return topics


def download_miracl_qrels(language="ar", split="dev", output_dir="data/processed"):
    """
    Download MIRACL qrels (relevance judgments) from HuggingFace
    
    Args:
        language: Language code (default: "ar")
        split: Dataset split (default: "dev")
        output_dir: Where to save the JSON file
        
    Returns:
        Dict mapping query_id -> {doc_id: relevance_score}
    """
    os.makedirs(output_dir, exist_ok=True)
    
    url = f"https://huggingface.co/datasets/miracl/miracl/resolve/main/miracl-v1.0-{language}/qrels/qrels.miracl-v1.0-{language}-{split}.tsv"
    
    print(f"Downloading qrels from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    
    # Parse TSV
    qrels = defaultdict(dict)
    for line in response.text.strip().split('\n'):
        parts = line.split('\t')
        qid, _, docid, rel = parts
        qrels[qid][docid] = int(rel)
    
    # Convert to regular dict
    qrels = dict(qrels)
    
    # Save to JSON
    output_path = os.path.join(output_dir, f"exp001_qrels.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(qrels, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Loaded qrels for {len(qrels)} queries")
    print(f"✓ Saved to {output_path}")
    
    return qrels


def parse_trec_results(results_file="results/baseline_dense/exp_001_baseline_dense.txt"):
    """
    Parse TREC format results file
    
    Format: query_id Q0 doc_id rank score run_name
    
    Args:
        results_file: Path to TREC results file
        
    Returns:
        Dict mapping query_id -> [(doc_id, score, rank), ...]
    """
    print(f"Parsing results from {results_file}...")
    
    results = defaultdict(list)
    
    with open(results_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            qid = parts[0]
            docid = parts[2]
            rank = int(parts[3])
            score = float(parts[4])
            
            results[qid].append({
                'doc_id': docid,
                'score': score,
                'rank': rank
            })
    
    # Convert to regular dict and sort by rank
    results = {
        qid: sorted(docs, key=lambda x: x['rank'])
        for qid, docs in results.items()
    }
    
    # Save to JSON
    output_dir = os.path.dirname(results_file)
    output_path = os.path.join(output_dir, "exp_001_results_parsed.json")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Parsed results for {len(results)} queries")
    print(f"✓ Saved to {output_path}")
    
    return results


def load_experiment_data(
    force_download=False,
    language="ar",
    split="dev"
) -> Tuple[Dict, Dict, Dict]:
    """
    Load all data needed for error analysis
    
    Args:
        force_download: If True, re-download even if files exist
        language: Language code
        split: Dataset split
        
    Returns:
        Tuple of (topics, qrels, results)
    """
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    
    topics_file = os.path.join(output_dir, "exp001_topics.json")
    qrels_file = os.path.join(output_dir, "exp001_qrels.json")
    results_file = "results/baseline_dense/exp_001_results_parsed.json"
    
    # Load or download topics
    if force_download or not os.path.exists(topics_file):
        topics = download_miracl_topics(language, split, output_dir)
    else:
        print(f"Loading topics from {topics_file}...")
        with open(topics_file, 'r', encoding='utf-8') as f:
            topics = json.load(f)
        print(f"✓ Loaded {len(topics)} queries")
    
    # Load or download qrels
    if force_download or not os.path.exists(qrels_file):
        qrels = download_miracl_qrels(language, split, output_dir)
    else:
        print(f"Loading qrels from {qrels_file}...")
        with open(qrels_file, 'r', encoding='utf-8') as f:
            qrels = json.load(f)
        print(f"✓ Loaded qrels for {len(qrels)} queries")
    
    # Parse results
    if force_download or not os.path.exists(results_file):
        results = parse_trec_results()
    else:
        print(f"Loading results from {results_file}...")
        with open(results_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        print(f"✓ Loaded results for {len(results)} queries")
    
    print("\n" + "="*60)
    print("Data Loading Complete")
    print("="*60)
    print(f"Topics:  {len(topics)} queries")
    print(f"Qrels:   {len(qrels)} queries with relevance judgments")
    print(f"Results: {len(results)} queries with retrieval results")
    print("="*60 + "\n")
    
    return topics, qrels, results


# Example usage
if __name__ == "__main__":
    topics, qrels, results = load_experiment_data()
    
    # Show sample
    sample_qid = list(topics.keys())[0]
    print(f"\nSample Query:")
    print(f"  ID: {sample_qid}")
    print(f"  Text: {topics[sample_qid]}")
    print(f"  Relevant docs: {len(qrels.get(sample_qid, {}))}")
    print(f"  Retrieved docs: {len(results.get(sample_qid, []))}")
    
    if sample_qid in results:
        print(f"  Top-3 results:")
        for i, doc in enumerate(results[sample_qid][:3], 1):
            is_relevant = doc['doc_id'] in qrels.get(sample_qid, {})
            print(f"    {i}. {doc['doc_id']} (score: {doc['score']:.4f}) {'✓ RELEVANT' if is_relevant else ''}")
