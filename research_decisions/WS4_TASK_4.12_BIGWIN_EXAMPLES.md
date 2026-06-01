# WS4 Task 4.12 — Big-Win Examples: Verification + Replacements + Golden Diagram Example

**Date:** 2026-05-31
**Owner:** Claude (mined from pkls), for Osman/Elhaj review
**Feeds:** §4.10 big-win table (**5.C.17**), the failure-mode discussion, and the figure plan (**7.1** — "illustrated graph" idea from the 4.12 team decision)
**Source artifacts:**
- `results/enhanced_queries/exp_013_csqe_aya_8b.pkl` — CSQE full results (`full_results`: per-qid first-pass docs, corpus-grounded expansions, blind samples, final enhanced string)
- `results/enhanced_queries/enhanced_queries_aya_expanse_8b.pkl` — Aya blind Query2Doc (System B) expansions

> **Verifiability caveat (read first).** The per-query nDCG runs (Config A RRF + Aya-blind BM25) lived in Colab and are **not in this repo**, so the exact `CSQE = 1.000 / blind = 0.000` scores cannot be recomputed *from the repo alone*. What **is** fully verifiable from the pkls — and is what every example below rests on — is the *qualitative big-win signature*: (a) the blind expansion confidently describes the **wrong entity**, and (b) the first-pass corpus docs + both CSQE corpus-grounded samples lock onto the **correct entity**. This is the same evidence basis the WS4 report used for 4.12. **UPDATE — these scores are now VERIFIED:** the per-query analysis was re-run on 2026-05-31 (`phase4_quick_wins_Ablation_erroranalysis.ipynb`) and sanity-checked against the published aggregates (blind **0.5046** / CSQE **0.6936** / BM25 **0.4621** — all matched exactly). The **three finalized examples in §2** each scored **blind nDCG@10 = 0.000 → CSQE nDCG@10 = 1.000**, read directly from the per-query run. See **§5** for the data map + the self-contained verification cell.
>
> **2026-05-31 update (Drive search).** The per-query scores are **not saved anywhere as a file** — they are computed inside `phase4_quick_wins_Ablation_erroranalysis.ipynb` (Drive id `1T9G85NmNODr6dpjx5ms6pNQ0CL_nXboV`) and only the *aggregate buckets* are written out (`results_phase4/exp_11_ablations/error_analysis_patterns.csv`). The saved TREC run files that **do** exist are listed in §5. ⚠️ One config caveat: the saved `hybrid_csqe_rrf_k20.txt` is **Config C / Both-expanded (0.6936)**, not Config A (0.7137) — this is the known WS4.17 / WS1.3 issue. It does **not** affect example selection (every big-win below is carried by the shared **BM25+CSQE** component, identical in Configs A and C), but the thesis caption should cite the Config-A per-query score once WS1.3 re-runs it.

---

## 1. Final selected examples (verified — feed 5.C.17 big-win table)

**Selected by Mohammed on 2026-05-31** from the 70 clean perfect-flip candidates produced by the verification cell (§5). All three are short definitional **"ما هو / ما هي" (what is X)** queries, all verified at **blind nDCG@10 = 0.000 → CSQE nDCG@10 = 1.000**.

> **Read the framing right (important).** For all three, **plain BM25 (raw query, no expansion) already scored 1.000** — the relevant article was retrievable from the bare query. So these examples specifically demonstrate that **the blind (hallucinated) pseudo-document *poisons* a query the retriever had already solved, while CSQE's corpus-grounded pseudo-document stays on target and preserves the hit.** This is the cleanest possible illustration of *why grounding matters*: it isolates the harm of ungrounded generation. (They are **not** "BM25 could not find it" cases — for that flavour, see the runner-up qid 14250 in the verification output, where plain BM25 also = 0.000.)

| # | Query (qid) | blind | CSQE | plain BM25 |
|---|---|---|---|---|
| 1 | ما هو الرباط المنصوري؟ (10061) | **0.000** | **1.000** | 1.000 |
| 2 | ما هي الأسماء الخمسة في اللغة العربية؟ (3034) | **0.000** | **1.000** | 1.000 |
| 3 | ما هو الفن الجزيري؟ (11753) | **0.000** | **1.000** | 1.000 |

*(Metric = nDCG@10 via `pytrec_eval` against MIRACL Arabic binary qrels. "blind" = Aya blind Query2Doc on BM25; "CSQE" = CSQE hybrid RRF; "plain BM25" = raw query, no QE. Same comparison the §4.10 error analysis uses.)*

### 1. الرباط المنصوري (al-Ribāṭ al-Manṣūrī) — qid 10061
- **Query:** «ما هو الرباط المنصوري؟» — *"What is al-Ribat al-Mansuri?"*
- **Blind QE hallucinates → a surgical device:** *"a type of **surgical ligature/suture** used in operations to fix bones or soft tissue; flexible and absorbable, made of polypropylene or polyethylene, in the form of a thin elastic strip."*
- **CSQE grounds to (correct):** *"al-Ribat al-Mansuri — a **ribat (a Sufi lodge / shelter for the poor)** endowed by the **Mamluk Sultan al-Mansur Qalawun al-Salihi** for the poor and pilgrims of Jerusalem in **681 AH / 1282–1283 CE**."*
- **Contrast:** a modern surgical suture ↔ a 13th-century Mamluk Sufi lodge in Jerusalem.

### 2. الأسماء الخمسة (the Five Nouns) — qid 3034 ⭐ *best Arabic-native; recommended golden example*
- **Query:** «ما هي الأسماء الخمسة في اللغة العربية؟» — *"What are the Five Nouns in Arabic?"*
- **Blind QE hallucinates → a list of common names:** *"a special category of the most common/widely-used **names**, with specific grammatical rules: 1. **Muhammad**, 2. **Adam**, 3. **Ibrahim**, 4. **Is[maʿil]** …"* — it mistakes the grammatical term for a list of popular male first names.
- **CSQE grounds to (correct):** *"the Five Nouns known in Arabic are **(أب، أخ، حم، فو، ذو)** [father, brother, father-in-law, mouth, possessor-of]; grammarians dispute a sixth, **(هن)**, because it is rarely used."*
- **Contrast:** a list of famous names ↔ the actual Arabic-grammar category. **The most telling example** — an Arabic-centric LLM failing on a core point of Arabic *grammar*, exactly the niche-Arabic knowledge the thesis argues corpus grounding restores. An Arabic examiner will immediately recognise the error.

### 3. الفن الجزيري (Insular art) — qid 11753
- **Query:** «ما هو الفن الجزيري؟» — *"What is Insular art?"*
- **Blind QE hallucinates → modern land art:** *"a form of **contemporary art** combining natural elements and modern techniques … also known as **'environmental art' or 'land art'**; artists use earth, stone, plants, water…"* — it reads الجزيري as "island/environmental."
- **CSQE grounds to (correct):** *"**Insular art** (also **Hiberno-Saxon art**) — an art style produced in the **post-Roman period in the British Isles**; the term derives from the Latin **insula = island**."*
- **Contrast:** modern environmental/land art ↔ a medieval art-history term for early-medieval British Isles art.

---

## 2. (Superseded) earlier candidates

The earlier pkl-mined candidates (Ruth Handler, al-Bakri, Holberg) and the original three (الرباط المنصوري **kept**, Boileau, John Dewey **dropped**) were proposals made *before* per-query scores were available. They are replaced by the three score-verified examples in §1. Boileau (11213) and the Ruth Handler / al-Bakri / Holberg set remain valid backups if a 4th/5th example is ever wanted — but the §1 trio is the final selection.

---

## 3. Golden example for the workflow diagram (the "illustrated graph")

**Recommendation: الأسماء الخمسة / the Five Nouns (qid 3034).** Best fit for a single self-explanatory figure aimed at this thesis's (Arabic) examiners:
- **Short query** that fits in a box.
- **Arabic-native and unambiguous:** the blind error (listing *Muhammad / Adam / Ibrahim* as "the five nouns") is instantly recognisable as wrong to any Arabic speaker, and the correct answer (أب أخ حم فو ذو) is a textbook grammar fact.
- **Verified true end-to-end path:** blind = 0.000, CSQE = 1.000 confirmed from the run.

*(Alternative if a non-grammar / more "encyclopedic" figure is preferred: الرباط المنصوري — surgical suture ↔ Mamluk Sufi lodge.)*

### Suggested diagram layout (hand to WS7.1 figure plan)

```
            ┌──────────────────────────────────────────────────────┐
  Query ───►│ «ما هي الأسماء الخمسة في اللغة العربية؟»              │
            │  (What are "the Five Nouns" in Arabic grammar?)      │
            └───────────────┬──────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        ▼                                        ▼
┌──────────────────┐                  ┌────────────────────────────┐
│  BLIND Query2Doc │                  │  First-pass BM25 retrieval │
│  (no corpus)     │                  │  top-k corpus docs         │
└────────┬─────────┘                  └──────────────┬─────────────┘
         ▼                                            ▼
  "the most common NAMES:               Doc «أسماء خمسة»: the Five
   Muhammad, Adam, Ibrahim,             Nouns are أب أخ حم فو ذو
   ..."        ✗ HALLUCINATION          (+ disputed 6th: هن)   ✓
         │                                            │
         │                                            ▼
         │                              ┌────────────────────────────┐
         │                              │  CSQE corpus-grounded       │
         │                              │  expansion (أب أخ حم فو ذو) │
         │                              └──────────────┬─────────────┘
         ▼                                             ▼
   Retrieves WRONG docs                    Retrieves the CORRECT
   (proper-name / biography articles)      «أسماء خمسة» grammar article
        nDCG@10 = 0.000                          nDCG@10 = 1.000
```

The single visual point: **blind expansion drifts to a plausible-but-wrong reading of the term; the corpus document anchors the expansion to the real meaning, and retrieval flips from miss to hit.** (Note: plain BM25 alone also scores 1.000 here — so the figure is really showing that CSQE *avoids the damage* that blind expansion inflicts, rather than recovering an otherwise-impossible query.)

---

## 4. Reproduction
All examples were pulled with `PYTHONIOENCODING=utf-8` from the two pkls above; per-qid records expose `original`, `retrieved_docids`, `retrieved_doc_texts`, `corpus_expansions` (×2), `blind_expansions` (×2), `enhanced`. Candidates were ranked across all **1,193 definitional queries** ("من هو/ما هو/…") by `overlap(blind, corpus_docs) − overlap(corpus_exp, corpus_docs)` (most-divergent first), then manually screened for genuine hallucination + grounding cleanliness.

---

## 5. Where the per-query scores live (Drive) + verification cell

**Searched `colab_data` (id `1XxzstTVUePz4kxadwgFa-G4gWMUkijkT`) and `Colab Notebooks` (id `1xCpPSVAyG0S6OMUwAAkiR9D-cURuXH1E`) on 2026-05-31.** Result: there is **no saved per-query nDCG file**. The 1061-big-win / 258-failure / +0.1890-mean numbers are produced live inside the error-analysis notebook. What is saved are the **ranked TREC run files** (top-100/query) and the **aggregate** CSVs. Everything needed to recompute exact per-query nDCG@10 is present:

| Artifact | Drive location | Drive id | What it is |
|---|---|---|---|
| Error-analysis notebook | `Colab Notebooks/` | `1T9G85NmNODr6dpjx5ms6pNQ0CL_nXboV` | computes per-query blind-vs-CSQE nDCG (Config **C**) |
| `bm25_csqe_run.txt` | `colab_data/results_phase4/exp_21_csqe_hybrid/` | `11BxX36yLS6Pw7zSoFxNmRdG0x-f6FqMp` | **BM25+CSQE** ranking → aggregate 0.6157 |
| `hybrid_csqe_rrf_k20.txt` | same folder | `1y1ceNTgvdespuduqwomLigHwsTe-ZI3d` | CSQE+Hybrid RRF (Config **C**, 0.6936) |
| `dense_csqe_run.txt` | same folder | `1GYP0Axie4quzmYVH7BSDm2na13xpIzFe` | Dense+CSQE ranking |
| `hybrid_rrf_k20.txt` (no-QE) | `…/exp_12_hybrid_baseline/` | `1aK37B93n5Ut4s1_vpZxTmI1gfKLp9h4T` | no-QE hybrid baseline (0.6267) |
| `error_analysis_patterns.csv` | `…/exp_11_ablations/` | `1hcxpfnAmJE_JypVbcqnrMTFg2MoHcQ3J` | aggregate buckets only (confirms baseline = **Aya-blind-BM25 0.5046**, system = Config C 0.6936) |
| `exp_013_csqe_aya_8b_results.pkl` | `colab_data/results/` | `1wkxPeVTEs5OQVJkQcKQ76_i1K6QzLgUK` | CSQE `full_results` (first-pass docs, corpus/blind samples) |

**The blind baseline run is *not* saved** — "Aya-blind-BM25 = 0.5046" is regenerated from `enhanced_queries_aya_expanse_8b.pkl` (in the repo) by BM25-retrieving its `enhanced` field at n=1. The cell below does exactly that.

### Verified-score miner (self-contained — run in the phase4 / error-analysis Colab, Drive mounted, repo `src` on path)

Reproduces the three known aggregates as a sanity gate (blind-BM25 **0.5046**, BM25+CSQE **0.6157**, CSQE-hybrid **0.6936**), then dumps every clean `blind≈0 / CSQE≈1` definitional big-win with its real scores.

```python
import os, pickle, numpy as np, pandas as pd
from collections import defaultdict
from src.utils.data_loader_hf import MIRACLDataLoader
from src.evaluation.metrics import RetrievalEvaluator
from src.retrievers.bm25 import BM25SRetriever

# --- paths (adjust DRIVE/COLAB_DATA to your mount) ---
COLAB_DATA = "/content/drive/MyDrive/colab_data"            # the shared colab_data folder
EXP21      = f"{COLAB_DATA}/results_phase4/exp_21_csqe_hybrid"
BLIND_PKL  = "results/enhanced_queries/enhanced_queries_aya_expanse_8b.pkl"
CSQE_PKL   = "results/enhanced_queries/exp_013_csqe_aya_8b.pkl"

# 1) qrels (binary) + metric
topics, qrels = MIRACLDataLoader('ar', 'dev').load_all()
ev = RetrievalEvaluator(qrels)
def pq(run):                                   # per-query nDCG@10
    r = ev.evaluate_per_query(run, ['ndcg_cut_10'])
    return {q: r[q]['ndcg_cut_10'] for q in r}
def agg(d):  return np.mean(list(d.values()))

# 2) read a saved TREC run -> {qid:{docid:score}}
def read_run(path):
    run = defaultdict(dict)
    for line in open(path):
        p = line.split()
        if len(p) >= 6: run[p[0]][p[2]] = float(p[4])
    return run
csqe_bm25   = read_run(f"{EXP21}/bm25_csqe_run.txt")          # expect agg 0.6157
csqe_hybrid = read_run(f"{EXP21}/hybrid_csqe_rrf_k20.txt")    # expect agg 0.6936 (Config C)

# 3) regenerate blind Aya-BM25 (System B, n=1) from the repo pkl
blind = pickle.load(open(BLIND_PKL, 'rb'))                   # column dict: query_ids[], enhanced[]
qids  = [str(q) for q in blind['query_ids']]
bm = BM25SRetriever(index_path=f"{COLAB_DATA}/bm25s_index",
                    corpus_ids_path=f"{COLAB_DATA}/corpus_ids.pkl")
hits = bm.search(blind['enhanced'], k=100)                  # enhanced = original + blind doc
blind_run = {qids[i]: {str(d): s for d, s in hits[i]} for i in range(len(qids))}

# 4) per-query scores + sanity gate
nd_b, nd_bc, nd_hc = pq(blind_run), pq(csqe_bm25), pq(csqe_hybrid)
print("SANITY  blind-BM25=%.4f (exp 0.5046) | BM25+CSQE=%.4f (0.6157) | CSQE-hyb=%.4f (0.6936)"
      % (agg(nd_b), agg(nd_bc), agg(nd_hc)))

# 5) build per-query table; flag clean definitional big-wins
DEF = ('من هو','من هي','ما هو','ما هي','ما هى','من هم')
csqe = pickle.load(open(CSQE_PKL, 'rb'))
corpus_exp = {str(q): fr for q, fr in zip(csqe['query_ids'], csqe['full_results'])}
rows = []
for q in qids:
    t = topics[q]['title']
    rows.append(dict(qid=q, query=t, words=len(t.split()),
                     definitional=any(t.strip().startswith(p) for p in DEF),
                     blind_bm25=nd_b.get(q,0), csqe_bm25=nd_bc.get(q,0),
                     csqe_hybrid=nd_hc.get(q,0), delta=nd_bc.get(q,0)-nd_b.get(q,0)))
df = pd.DataFrame(rows)
bigwins = df[(df.blind_bm25 <= 0.10) & (df.csqe_bm25 >= 0.90) & df.definitional]\
            .sort_values('csqe_hybrid', ascending=False)
bigwins.to_csv('ws4_412_bigwin_candidates.csv', index=False)
print(f"clean 1.0/0.0 definitional big-wins: {len(bigwins)}  -> ws4_412_bigwin_candidates.csv")

# 6) spotlight the candidate qids already short-listed in §1–§2
for q in ['5343','1244','12454','765','11563','10061','11213','10320']:
    if q in nd_b:
        print(q, topics[q]['title'][:40],
              "| blindBM25=%.3f csqeBM25=%.3f csqeHyb=%.3f" % (nd_b[q], nd_bc[q], nd_hc[q]))
```

**Two things to confirm when running:** (a) the `COLAB_DATA` mount path (the run files were shared from the `graduation.uofk@gmail.com` Drive; the CSQE pkl's own config used `/content/drive/MyDrive/graduation project/colab_data/…`); (b) that the sanity line prints ≈ 0.5046 / 0.6157 / 0.6936 — if it does, the per-query 1.000/0.000 numbers in the spotlight block are trustworthy for the thesis table and the golden-figure caption.

**END.**
