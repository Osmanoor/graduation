# CSQE Implementation Plan: Corpus-Steered Query Expansion for Arabic RAG
## Task 6.3b-implement

**Date:** 2026-04-04  
**Status:** Ready to implement — research complete (Task 6.3b-research done)  
**Experiment ID:** exp_013  
**Estimated time:** 2-3 days  
**Colab GPU:** A100 preferred, T4 acceptable  

---

## Quick Reference

| Item | Value |
|------|-------|
| Base model | `CohereForAI/aya-expanse-8b` |
| BM25 first-pass k | 10 |
| Doc truncation | 128 tokens |
| Temperature | 1.0 |
| Corpus samples (N1) | 2 |
| Blind samples (N2) | 2 |
| Query repetition (α) | 1 (no repetition in CSQE — differs from Query2Doc) |
| Target nDCG@10 | ≥ 0.74 (min success: beat hybrid = 0.6267) |
| Output pkl | `results/enhanced_queries/exp_013_csqe_aya_8b.pkl` |
| Output TREC | `results/exp_013_csqe_bm25.txt` |

---

## What CSQE Does (vs. Our Current Query2Doc)

**Current Query2Doc pipeline:**
```
query → LLM → pseudo_doc → (query * n) + " " + pseudo_doc → BM25
```
The LLM generates blindly from its parametric knowledge (may hallucinate, may not match corpus vocabulary).

**CSQE pipeline:**
```
query → BM25 first-pass (k=10) → extract pivotal sentences → LLM generates grounded expansion
     → N=2 corpus-originated expansions + N=2 blind expansions → concatenate → BM25 final
```
The key difference: the LLM SEES actual corpus documents before generating. This grounds its output in real MIRACL vocabulary, fixing the corpus mismatch that Query2Doc suffers.

---

## Notebook Structure: `experiments/exp_013_csqe_aya_8b.ipynb`

Create this as a **new notebook** (don't modify existing Aya notebook). Structure:

### Cell 0 — Title markdown
```
# Experiment 013: CSQE — Corpus-Steered Query Expansion
# Model: Aya Expanse 8B | BM25 k=10 | 2+2 expansions
```

### Cell 1 — Setup (copy from Query_generator_aya_8b.ipynb cells 3-7)
```python
# Clone repo, install deps, mount Drive, HuggingFace login
# IDENTICAL to existing Aya notebook setup
```

### Cell 2 — Imports
```python
import os, sys, json, pickle, time, re
from tqdm.notebook import tqdm
import numpy as np
import torch

# BM25 for first-pass retrieval
from pyserini.search.lucene import LuceneSearcher

# Aya model
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# Data + evaluation
from src.utils.data_loader import MIRACLDataLoader
```

### Cell 3 — Configuration (single config dict — all hyperparameters here)
```python
CONFIG = {
    # BM25 first-pass
    "bm25_index_path": "/content/drive/MyDrive/bm25s_index",  # adjust if needed
    "top_k_docs": 10,           # K in CSQE paper
    "doc_truncation_tokens": 128,  # truncate each retrieved doc to 128 tokens

    # LLM generation
    "model_name": "CohereForAI/aya-expanse-8b",
    "temperature": 1.0,          # IMPORTANT: 1.0 not 0.1 (need diversity for sampling)
    "max_new_tokens": 256,
    "top_p": 0.9,
    "num_corpus_samples": 2,     # N1 corpus-originated expansions
    "num_blind_samples": 2,      # N2 blind expansions (HyDE-style)

    # Query construction
    "query_repetition": 1,       # α=1 (CSQE does NOT use query repetition)

    # Output
    "exp_id": "exp_013",
    "output_pkl": "results/enhanced_queries/exp_013_csqe_aya_8b.pkl",
    "output_trec_bm25": "results/exp_013_csqe_bm25.txt",
    "run_name": "exp_013_csqe_aya",
    "checkpoint_every": 500,     # save partial results every 500 queries
    "checkpoint_path": "/content/drive/MyDrive/exp_013_checkpoint.pkl",
}
```

### Cell 4 — Load MIRACL data
```python
# Load queries and qrels (identical to all other notebooks)
data_loader = MIRACLDataLoader(language="ar", split="dev")
topics, qrels = data_loader.load_all()

query_ids = list(topics.keys())
query_texts = [topics[qid]['title'] for qid in query_ids]

print(f"Queries: {len(query_ids)}")
print(f"Sample: {query_texts[0]}")
```

### Cell 5 — Load BM25 index for first-pass retrieval
```python
# NOTE: This uses Pyserini LuceneSearcher (the same BM25 used in baseline)
# BM25S index path is on Google Drive — use the same path as in evaluate_enhanced_queries.ipynb

searcher = LuceneSearcher(CONFIG["bm25_index_path"])
searcher.set_language("ar")  # Arabic analyzer

# Test
hits = searcher.search("الذكاء الاصطناعي", k=CONFIG["top_k_docs"])
print(f"Test retrieval: {len(hits)} hits")
print(f"Top doc: {hits[0].docid} score={hits[0].score:.4f}")
```

**IMPORTANT:** The BM25 index path may be Pyserini Lucene format, not BM25S format. Check:
- `evaluate_enhanced_queries.ipynb` uses `BM25SRetriever` from `src/retrievers/bm25s_retriever.py`
- If BM25S is not compatible with `LuceneSearcher`, use `BM25SRetriever` directly for first-pass

Alternative using BM25SRetriever:
```python
from src.retrievers.bm25s_retriever import BM25SRetriever
bm25_retriever = BM25SRetriever(index_path=CONFIG["bm25_index_path"])

# Returns: list of (docid, score) tuples
def bm25_first_pass(query_text, k=10):
    results = bm25_retriever.search(query_text, k=k)
    return results  # [(docid, score), ...]
```

### Cell 6 — Helper: extract docid metadata
```python
def parse_docid(docid):
    """Parse X#Y format to get article_id and passage_position."""
    parts = docid.split('#')
    return {
        "article_id": int(parts[0]),
        "passage_pos": int(parts[1]) if len(parts) > 1 else 0
    }

def truncate_to_tokens(text, max_tokens=128, tokenizer=None):
    """
    Truncate text to roughly max_tokens.
    Fast approximation: 128 tokens ≈ 100-110 Arabic words (Arabic tokens ~1.2 chars/token).
    Use tokenizer if available, else char-based fallback.
    """
    if tokenizer is not None:
        tokens = tokenizer.encode(text, add_special_tokens=False)
        if len(tokens) > max_tokens:
            tokens = tokens[:max_tokens]
            return tokenizer.decode(tokens, skip_special_tokens=True)
        return text
    else:
        # Rough fallback: 128 tokens ≈ 512 chars for Arabic
        return text[:512]
```

### Cell 7 — CSQE Prompt Template
```python
# The CSQE one-shot prompt (Arabic)
# DO NOT change the structure — this mirrors the CSQE paper exactly

CSQE_SYSTEM = "أنت مساعد بحثي متخصص في استرجاع المعلومات باللغة العربية."

CSQE_ONE_SHOT_EXAMPLE = """
الاستعلام: "كيف تكون بعض أسماك القرش ذات دم دافئ"
المستندات المسترجعة:
1. معظم أسماك القرش ذات دم بارد. البعض، مثل الماكو والقرش الأبيض الكبير، ذات دم دافئ جزئياً (هي كائنات ماصة للحرارة).
2. هل أسماك القرش ذات دم بارد أم دافئ؟ لدى أسماك القرش سمعة بأنها ذات دم بارد.
3. أسماك القرش البيضاء الكبيرة هي من بين أسماك القرش القليلة ذات الدم الدافئ.

ستبدأ بفحص المستندات المسترجعة وتحديد المستندات ذات الصلة، حتى لو كانت جزئياً، بالاستعلام. بمجرد تحديد المستندات ذات الصلة، ستستخرج الجمل الرئيسية من كل مستند التي تساهم في صلتها.

بناءً على الاستعلام "كيف تكون بعض أسماك القرش ذات دم دافئ"، قمت بفحص المستندات المسترجعة أولاً. فيما يلي المستندات ذات الصلة والجمل الرئيسية المستخرجة من كل منها:

المستند 1:
"معظم أسماك القرش ذات دم بارد. البعض، مثل الماكو والقرش الأبيض الكبير، ذات دم دافئ جزئياً (هي كائنات ماصة للحرارة)."

المستند 3:
"أسماك القرش البيضاء الكبيرة هي من بين أسماك القرش القليلة ذات الدم الدافئ."
"""

def build_csqe_prompt(query, retrieved_docs_truncated):
    """
    Build the CSQE corpus-grounded prompt.
    retrieved_docs_truncated: list of truncated doc texts (up to 10)
    """
    docs_str = "\n".join(
        f"{i+1}. {doc}" for i, doc in enumerate(retrieved_docs_truncated)
    )
    
    instruction = (
        "ستبدأ بفحص المستندات المسترجعة وتحديد المستندات ذات الصلة، "
        "حتى لو كانت جزئياً، بالاستعلام. بمجرد تحديد المستندات ذات الصلة، "
        "ستستخرج الجمل الرئيسية من كل مستند التي تساهم في صلتها."
    )
    
    prompt = f"{CSQE_ONE_SHOT_EXAMPLE}\n\nالاستعلام: \"{query}\"\nالمستندات المسترجعة:\n{docs_str}\n\n{instruction}"
    return prompt

def build_blind_prompt(query):
    """
    Build the blind (HyDE-style) expansion prompt.
    Standard Query2Doc prompt — generates without corpus context.
    """
    return (
        f"اكتب فقرة قصيرة تجيب على السؤال التالي باللغة العربية:\n\n{query}\n\nالإجابة:"
    )
```

### Cell 8 — Load Aya Expanse 8B
```python
# Identical to Query_generator_aya_8b.ipynb cells 12-13
# Copy the model loading code directly from that notebook
# Key settings: 4-bit NF4, BF16 compute dtype

# CHANGE FROM ORIGINAL: temperature must be 1.0 (not 0.1)
# because CSQE needs diversity across N=2 samples
```

### Cell 9 — CSQE Enhancer class
```python
class CSQEEnhancer:
    def __init__(self, model, tokenizer, bm25_retriever, config):
        self.model = model
        self.tokenizer = tokenizer
        self.bm25 = bm25_retriever
        self.config = config
    
    def get_retrieved_docs(self, query):
        """BM25 first-pass: retrieve top-k documents."""
        results = self.bm25.search(query, k=self.config["top_k_docs"])
        docs = []
        for docid, score in results:
            # Fetch document text from BM25 index
            doc_text = self.bm25.get_doc_text(docid)  # adjust method name if needed
            truncated = truncate_to_tokens(
                doc_text,
                max_tokens=self.config["doc_truncation_tokens"],
                tokenizer=self.tokenizer
            )
            docs.append({
                "docid": docid,
                "score": score,
                "text": truncated,
                "meta": parse_docid(docid)
            })
        return docs
    
    def generate_sample(self, prompt, temperature=None):
        """Generate a single sample from the model."""
        if temperature is None:
            temperature = self.config["temperature"]
        
        inputs = self.tokenizer.apply_chat_template(
            [
                {"role": "system", "content": CSQE_SYSTEM},
                {"role": "user", "content": prompt}
            ],
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_new_tokens=self.config["max_new_tokens"],
                temperature=temperature,
                top_p=self.config["top_p"],
                do_sample=True,
            )
        
        generated = outputs[0][inputs.shape[1]:]
        return self.tokenizer.decode(generated, skip_special_tokens=True).strip()
    
    def enhance(self, query):
        """
        Full CSQE pipeline for a single query.
        Returns dict with all intermediate results + final enhanced query.
        """
        # Step 1: BM25 first-pass
        retrieved_docs = self.get_retrieved_docs(query)
        doc_texts = [d["text"] for d in retrieved_docs]
        
        # Step 2: Generate N1=2 corpus-originated expansions
        corpus_prompt = build_csqe_prompt(query, doc_texts)
        corpus_expansions = []
        for _ in range(self.config["num_corpus_samples"]):
            exp = self.generate_sample(corpus_prompt, temperature=1.0)
            corpus_expansions.append(exp)
        
        # Step 3: Generate N2=2 blind expansions (no corpus context)
        blind_prompt = build_blind_prompt(query)
        blind_expansions = []
        for _ in range(self.config["num_blind_samples"]):
            exp = self.generate_sample(blind_prompt, temperature=1.0)
            blind_expansions.append(exp)
        
        # Step 4: Concatenate all expansions
        # Format: original_query + corpus_expansions + blind_expansions
        α = self.config["query_repetition"]
        all_expansions = corpus_expansions + blind_expansions
        
        final_query = (query + " ") * α + " ".join(all_expansions)
        
        return {
            "original": query,
            "retrieved_docids": [d["docid"] for d in retrieved_docs],
            "corpus_expansions": corpus_expansions,
            "blind_expansions": blind_expansions,
            "enhanced": final_query,
        }
```

**NOTE on `get_doc_text`:** Check whether BM25SRetriever has a method to fetch raw doc text by docid. If not, you may need to preload the MIRACL corpus as a dict `{docid: text}` using the HuggingFace dataset:
```python
from datasets import load_dataset
corpus_ds = load_dataset("miracl/miracl-corpus", "ar", split="train")
corpus = {row["docid"]: row["text"] for row in corpus_ds}
```
This uses ~4-5GB RAM. Load once and reuse.

### Cell 10 — Sanity check (5 queries)
```python
# ALWAYS run this before the full run
# Check:
# 1. Retrieved docs look reasonable (Arabic text, correct length)
# 2. Corpus expansion is grounded (cites/quotes from docs)
# 3. Blind expansion looks like normal Query2Doc output
# 4. Final concatenated query is not empty / not garbled

sample_qids = query_ids[:5]
for qid in sample_qids:
    q = topics[qid]['title']
    result = enhancer.enhance(q)
    print(f"\n{'='*60}")
    print(f"QID: {qid}")
    print(f"Query: {q}")
    print(f"Retrieved {len(result['retrieved_docids'])} docs")
    print(f"Corpus exp 1 ({len(result['corpus_expansions'][0])} chars):")
    print(f"  {result['corpus_expansions'][0][:200]}")
    print(f"Blind exp 1 ({len(result['blind_expansions'][0])} chars):")
    print(f"  {result['blind_expansions'][0][:200]}")
    print(f"Final query ({len(result['enhanced'])} chars):")
    print(f"  {result['enhanced'][:300]}")

# STOP HERE if any of the above looks wrong
# Common issues:
# - corpus expansion is empty → prompt translation issue
# - corpus expansion ignores docs → prompt instruction not clear
# - Arabic output has Latin chars → Aya generating in English
```

### Cell 11 — Full run with checkpointing
```python
import pickle, os
from tqdm.notebook import tqdm

# Resume from checkpoint if exists
start_idx = 0
results = []
if os.path.exists(CONFIG["checkpoint_path"]):
    with open(CONFIG["checkpoint_path"], "rb") as f:
        checkpoint = pickle.load(f)
    results = checkpoint["results"]
    start_idx = len(results)
    print(f"Resuming from checkpoint at query {start_idx}")

# Main loop
start_time = time.time()
for i, (qid, query) in enumerate(tqdm(
    zip(query_ids[start_idx:], query_texts[start_idx:]),
    initial=start_idx, total=len(query_ids)
)):
    result = enhancer.enhance(query)
    result["qid"] = qid
    results.append(result)
    
    # Checkpoint every N queries
    if (start_idx + i + 1) % CONFIG["checkpoint_every"] == 0:
        with open(CONFIG["checkpoint_path"], "wb") as f:
            pickle.dump({"results": results, "config": CONFIG}, f)
        elapsed = time.time() - start_time
        print(f"  Checkpoint saved at {start_idx + i + 1} queries ({elapsed/60:.1f} min)")

elapsed = time.time() - start_time
print(f"\nDone: {len(results)} queries in {elapsed/60:.1f} minutes")
```

### Cell 12 — Save results in standard pkl format
```python
# Save in SAME format as all other enhanced_queries pkl files
# Structure must match what evaluate_enhanced_queries.ipynb expects

enhanced_queries_flat = [r["enhanced"] for r in results]

output = {
    "query_ids": [r["qid"] for r in results],
    "original": [topics[r["qid"]]['title'] for r in results],
    "enhanced": enhanced_queries_flat,
    "model": CONFIG["model_name"],
    "config": CONFIG,
    "stats": {
        "total_queries": len(results),
        "avg_original_len": np.mean([len(r["original"]) for r in results]),
        "avg_enhanced_len": np.mean([len(r["enhanced"]) for r in results]),
        "avg_expansion_ratio": np.mean([
            len(r["enhanced"])/len(r["original"]) for r in results if len(r["original"]) > 0
        ]),
    },
    # Store full results (intermediate steps) separately for analysis
    "full_results": results,
}

# Save to Drive
output_path = f"/content/drive/MyDrive/{CONFIG['output_pkl'].split('/')[-1]}"
with open(output_path, "wb") as f:
    pickle.dump(output, f)

# Copy to local results dir
os.makedirs("results/enhanced_queries", exist_ok=True)
import shutil
shutil.copy(output_path, CONFIG["output_pkl"])

print(f"Saved to {output_path}")
print(f"Stats: {output['stats']}")
```

### Cell 13 — BM25 Evaluation
```python
# Reuse BM25SRetriever and pytrec_eval from evaluate_enhanced_queries.ipynb
# DO NOT rewrite evaluation from scratch — copy the evaluation section

# The evaluator should:
# 1. Load the pkl we just saved
# 2. Run BM25 retrieval on enhanced queries
# 3. Compute nDCG@10, Recall@10, Recall@100, MRR
# 4. Save TREC run file to results/exp_013_csqe_bm25.txt

# Copy relevant cells from evaluate_enhanced_queries.ipynb:
# - BM25SRetriever initialization
# - search loop
# - pytrec_eval computation
# - results printing
```

### Cell 14 — Results table + comparison
```python
# Print comparison against all baselines
baselines = {
    "BM25 baseline": 0.4621,
    "mDPR baseline": 0.4993,
    "Aya blind Query2Doc (BM25)": 0.5855,   # best from exp_011 (β=2)
    "Hybrid RRF baseline": 0.6267,           # STRONGEST baseline to beat
    "CSQE Aya 8B (this exp)": ndcg_result,  # fill in after evaluation
}

print("\n=== RESULTS: nDCG@10 ===")
for name, score in sorted(baselines.items(), key=lambda x: x[1]):
    marker = " ← THIS EXP" if "CSQE" in name else ""
    print(f"  {score:.4f}  {name}{marker}")

print(f"\nVs. hybrid baseline: {ndcg_result - 0.6267:+.4f}")
print(f"Vs. blind Query2Doc: {ndcg_result - 0.5855:+.4f}")
```

### Cell 15 — Ablation analysis (qualitative)
```python
# For 20 random queries, print:
# - Original query
# - Retrieved doc titles (article names from docid)
# - Corpus expansion (is it grounded?)
# - Blind expansion (is it hallucinating?)
# - Was this query improved vs. blind baseline?
#
# Purpose: understand whether corpus grounding is actually helping
# This feeds the thesis qualitative analysis section

import random
random.seed(42)
sample_indices = random.sample(range(len(results)), 20)

for idx in sample_indices[:5]:  # print 5 in notebook, save all 20 to file
    r = results[idx]
    qid = r["qid"]
    print(f"\nQID: {qid}")
    print(f"Query: {r['original']}")
    # Print article titles of retrieved docs
    for docid in r["retrieved_docids"][:3]:
        article_id = docid.split("#")[0]
        # title lookup — if corpus dict is available
        print(f"  Retrieved: {docid}")
    print(f"Corpus exp: {r['corpus_expansions'][0][:150]}")
    print(f"Blind exp:  {r['blind_expansions'][0][:150]}")
```

---

## Hyperparameter Variants to Try (After Baseline CSQE)

Run these only if baseline CSQE does not beat the hybrid (0.6267):

| Exp | Change | Expected Effect |
|-----|--------|----------------|
| 013b | k=15 (more docs) | More context for LLM |
| 013c | N=4+0 (all corpus, no blind) | Ablation: corpus-only |
| 013d | N=0+4 (all blind, no corpus) | Ablation: blind-only |
| 013e | α=2 (query repetition) | Combine with repetition fix |
| 013f | Jais-2-8B instead of Aya | Arabic-specialized model |

**Run ablations in this order of priority.** If 013 beats hybrid, run 013c and 013d for the thesis ablation study (they're cheap, add analytical value).

---

## Critical File Paths (for Colab)

| Resource | Path |
|----------|------|
| BM25 index | `/content/drive/MyDrive/bm25s_index` (verify against evaluate_enhanced_queries.ipynb) |
| MIRACL qrels | Loaded via `MIRACLDataLoader` |
| Previous pkl files | `/content/drive/MyDrive/enhanced_queries_aya_expanse_8b_final.pkl` |
| Checkpoint | `/content/drive/MyDrive/exp_013_checkpoint.pkl` |
| Output pkl | `/content/drive/MyDrive/exp_013_csqe_aya_8b.pkl` |

---

## Things to Read Before Starting

1. `research_decisions/mufti_approach_deep_research.md` — Section 8 (prompt templates) and Section 9 (risks)
2. `experiments/Query_generator_aya_8b.ipynb` — Copy setup cells (1-9) and model loading (12-13)
3. `experiments/evaluate_enhanced_queries.ipynb` — Copy evaluation cells for BM25 scoring

---

## Success Criteria

| Outcome | nDCG@10 | Interpretation |
|---------|---------|----------------|
| Failure | < 0.5855 | Worse than blind Query2Doc — debug prompts |
| Partial success | 0.5855 – 0.6267 | Better than blind but not hybrid — tune hyperparams |
| **Minimum success** | **> 0.6267** | **Beats hybrid baseline — main thesis result** |
| Target success | > 0.74 | Expected from CSQE paper projection |
| Stretch goal | > 0.80 | Exceptional — would match state-of-art |

---

## After the Experiment: What to Update

1. **CLAUDE.md** — Add exp_013 result to "Reference Baselines" tables
2. **TASKS.md** — Mark 6.3b-implement done, update outcomes
3. **Thesis Chapter 4** — Add CSQE method description, results table, ablation discussion
4. **RESEARCH_CONTEXT_KERNEL.md.md** — Update best result achieved
5. **Create** `docs/experiments/exp_013_csqe_aya_8b.md` — Experiment log

---

## Prompt for New Session to Implement This

Use this prompt when opening a new Claude Code session to start the implementation:

```
I'm continuing my Arabic RAG thesis project. I need to implement Experiment 013 (CSQE).

Read these files in this order:
1. research_decisions/csqe_implementation_plan.md  ← THIS FILE (full plan)
2. research_decisions/mufti_approach_deep_research.md  ← Sections 7-9 (algorithm, prompts, risks)
3. experiments/Query_generator_aya_8b.ipynb  ← Copy setup/model-loading cells
4. experiments/evaluate_enhanced_queries.ipynb  ← Copy evaluation cells

Task: Create experiments/exp_013_csqe_aya_8b.ipynb following csqe_implementation_plan.md exactly.

Key decisions (already made, do not reconsider):
- Algorithm: CSQE (BM25 first-pass k=10, 2 corpus + 2 blind expansions, temperature=1.0)
- Model: CohereForAI/aya-expanse-8b
- Target: beat hybrid baseline (0.6267 nDCG@10)
- Output format: same pkl structure as existing enhanced_queries notebooks

Start by reading the 4 files above, then create the notebook.
```
