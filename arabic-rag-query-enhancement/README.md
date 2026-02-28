# Arabic RAG Query Enhancement

Query enhancement techniques for improving Arabic retrieval-augmented generation systems.

## Project Structure

```
arabic-rag-query-enhancement/
├── data/                    # Dataset storage
│   ├── miracl/             # MIRACL dataset (accessed via HuggingFace)
│   └── processed/          # Processed data
├── src/                    # Source code
│   ├── retrievers/         # Retrieval implementations
│   │   ├── dense.py        # mDPR dense retriever
│   │   └── bm25.py         # BM25S sparse retriever
│   ├── enhancers/          # Query enhancement techniques
│   │   ├── base.py         # Base classes (Identity, QueryEnhancer)
│   │   └── query2doc.py    # Query2Doc LLM-based expansion
│   ├── evaluation/         # Evaluation metrics
│   │   └── metrics.py      # Recall, NDCG, MRR
│   └── utils/              # Utilities
│       └── data_loader_hf.py  # MIRACL data loader (HuggingFace)
├── experiments/            # Experiment notebooks
│   └── exp_001_baseline_dense.ipynb  # First baseline experiment
├── results/                # Experiment results
│   ├── baseline_dense/     # Dense baseline results
│   ├── baseline_bm25/      # BM25 baseline results (future)
│   └── enhanced/           # Enhanced results (future)
├── configs/                # Configuration files
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup (Google Colab)

### 1. Clone Repository

```bash
!git clone https://github.com/Osmanoor/graduation.git
%cd graduation/arabic-rag-query-enhancement
```

### 2. Install Dependencies

```bash
# Install Java 21 (required for Pyserini)
!apt-get install -qq openjdk-21-jdk-headless

# Install Python packages
!pip install -q -r requirements.txt
```

### 3. Restart Runtime

**IMPORTANT:** After installation, restart the Colab runtime:
- Runtime → Restart runtime

### 4. Configure Environment

```python
import os
import sys

# Set Java home
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-21-openjdk-amd64'

# Add project to path
sys.path.insert(0, '/content/graduation/arabic-rag-query-enhancement')
```

## Quick Start

### Run Baseline Experiment

```python
# Open and run: experiments/exp_001_baseline_dense.ipynb
```

### Use Components Programmatically

```python
from src.utils.data_loader import MIRACLDataLoader
from src.retrievers.dense import mDPRRetriever
from src.enhancers.base import IdentityEnhancer
from src.evaluation.metrics import RetrievalEvaluator

# Load data
loader = MIRACLDataLoader(language="ar", split="dev")
topics, qrels = loader.load_all()

# Initialize components
enhancer = IdentityEnhancer()  # No enhancement (baseline)
retriever = mDPRRetriever()
evaluator = RetrievalEvaluator(qrels)

# Run experiment
query_ids = list(topics.keys())
queries = [topics[qid]['title'] for qid in query_ids]
enhanced = enhancer.enhance_batch(queries)
results = retriever.search(enhanced, k=100)

# Evaluate
metrics = evaluator.evaluate(results)
print(f"NDCG@10: {metrics['ndcg_cut_10']:.4f}")
```

## Experiments

### Experiment 001: Dense Baseline

- **Notebook:** `experiments/exp_001_baseline_dense.ipynb`
- **Enhancement:** Identity (no enhancement)
- **Expected Results:**
  - Recall@100: ~0.841
  - NDCG@10: ~0.499
- **Status:** Complete

### Experiment 002: BM25 Baseline

- **Notebook:** `experiments/exp_002_baseline_bm25.ipynb`
- **Enhancement:** Identity (no enhancement)
- **Expected Results:**
  - Recall@100: ~0.860
  - NDCG@10: ~0.461
- **Status:** Ready to run

### Experiment 003: Query2Doc + Dense

- **Notebook:** `experiments/exp_003_query2doc_dense.ipynb`
- **Documentation:** `experiments/exp_003_query2doc_dense.md`
- **Enhancement:** Query2Doc (LLM-based pseudo-document generation)
- **LLM:** Qwen 2.5 3B Instruct
- **Baseline:** Exp 001
- **Results:**
  - Recall@100: 0.8594 (+2.19% vs baseline)
  - NDCG@10: 0.5435 (+8.93% vs baseline)
  - MRR: 0.5742
- **Status:** ✅ Complete (Feb 11, 2026)

### Experiment 004: Query2Doc + BM25

- **Notebooks:** 
  - Generator: `experiments/Query_generator_query2doc.ipynb`
  - Evaluator: `experiments/evaluate_enhanced_queries.ipynb`
- **Documentation:** `docs/experiments/exp_004_query2doc_bm25.md`
- **Enhancement:** Query2Doc (same as Exp 003)
- **LLM:** Qwen 2.5 3B Instruct
- **Baseline:** Exp 002
- **Results:**
  - Recall@100: 0.8155 (-4.92% vs baseline) ❌
  - NDCG@10: 0.4090 (-11.5% vs baseline) ❌
  - MRR: 0.4342 (-10.2% vs baseline) ❌
- **Key Finding:** Query2Doc DECREASED BM25 performance (opposite to Dense +8.93%)
- **Likely Cause:** Missing query repetition (paper recommends 5x for BM25)
- **Status:** ✅ Complete (Feb 12, 2026)

## Adding New Query Enhancement Techniques

1. Create a new class in `src/enhancers/`:

```python
from src.enhancers.base import QueryEnhancer

class MyEnhancer(QueryEnhancer):
    def enhance(self, query: str, query_id: str = None) -> str:
        # Your enhancement logic here
        enhanced = query + " additional context"
        return enhanced
```

2. Use it in experiments:

```python
from src.enhancers.my_enhancer import MyEnhancer

enhancer = MyEnhancer()
enhanced_queries = enhancer.enhance_batch(queries)
```

### Available Enhancers

- **IdentityEnhancer** (`base.py`): No enhancement, returns query unchanged (baseline)
- **Query2DocEnhancer** (`query2doc.py`): LLM-based pseudo-document generation using Qwen 2.5 3B

## Dataset

**MIRACL Arabic:**
- Corpus: 2,061,414 passages
- Queries: 2,896 (dev set)
- Language: Modern Standard Arabic (MSA)
- Access: Via Pyserini (no manual download needed)

## Hardware Requirements

- **GPU:** Recommended (T4 or better)
- **RAM:** 12GB+ (Google Colab free tier sufficient)
- **Storage:** ~6GB for mDPR index (downloaded on first run)

## Performance

- **Baseline retrieval:** ~2-3 minutes (T4 GPU)
- **CPU fallback:** ~10-15 minutes

## Citation

```bibtex
@misc{arabic-rag-qe-2026,
  title={Query Enhancement for Arabic Retrieval-Augmented Generation},
  author={Mohammed Elhaj and Osman Bashir},
  year={2026},
  institution={University of Khartoum}
}
```

## License

[Add your license here]

## Contact

- Mohammed Elhaj: [email]
- Osman Bashir: [email]
