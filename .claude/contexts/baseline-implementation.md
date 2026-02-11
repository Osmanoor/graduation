# Baseline Implementation Guide

**Reference:** `research_decisions/technical_specifications.md`

## Architecture (Confirmed)

```
User Query -> [Retriever: Dense OR BM25] -> Top-10 Chunks -> Evaluate
```

**Key Point:** We test Dense and BM25 SEPARATELY, not as hybrid.

## MIRACL Dataset Structure

```python
# Corpus format (from MIRACL docs)
{
    "docid": str,      # Document ID
    "title": str,      # Article title (Arabic)
    "text": str        # Passage text (Arabic)
}

# Query format
{
    "query_id": str,
    "query": str       # Query text (Arabic)
}

# Relevance judgments (qrels)
# query_id, docid, relevance (0-3 scale)
```

## Evaluation Metrics (Confirmed)

```python
# All three metrics required for every experiment
metrics = ["Recall@10", "NDCG@10", "MRR"]
```

## Implementation Notes

**BM25:**
- Use Pyserini or rank-bm25
- Arabic tokenization needed
- No GPU required

**Dense:**
- Embedding model: UNDER INVESTIGATION (check TASKS.md)
- Vector store: FAISS (local)
- GPU recommended

## Do NOT
- Implement hybrid until both baselines are done
- Assume embedding model is decided (check current status)
- Skip documentation of results
