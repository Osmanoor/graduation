"""
PaperBanana generation script for CSQE figure variants.

Usage:
    set GOOGLE_API_KEY=<your-key>     # PowerShell: $env:GOOGLE_API_KEY='<key>'
    python thesis_figures/gen_csqe_variants.py

Outputs: thesis_figures/output/png/fig_3_8_csqe_aigen_v{1..4}.png

All pipeline facts verified against:
  arabic-rag-query-enhancement/docs/experiments/exp_013_csqe_aya_8b.md
  research_decisions/csqe_parameter_verification.md
"""

import asyncio
import os
import shutil
import sys
from pathlib import Path

# Set GOOGLE_API_KEY in your environment before running. Never hardcode here.
#   PowerShell:  $env:GOOGLE_API_KEY='<key>'
#   bash:        export GOOGLE_API_KEY=<key>
if not os.environ.get("GOOGLE_API_KEY"):
    raise EnvironmentError("GOOGLE_API_KEY env var not set")

from paperbanana import PaperBananaPipeline, GenerationInput, DiagramType
from paperbanana.core.config import Settings

OUT_DIR = Path("thesis_figures/output/png")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Verified source context ───────────────────────────────────────────────────
# Facts cross-checked against exp_013 doc and parameter verification doc.
# Key deviations from the original CSQE paper (Lei et al. arXiv:2402.18031):
#   - k1 = 5 (paper uses k=10; our MIRACL Arabic implementation uses k=5)
#   - LLM = Aya Expanse 8B BF16 (paper uses GPT-3.5-turbo)
#   - corpus-grounded prompt asks for EXTRACTION not free-form answer writing
SHARED_CONTEXT = """\
CSQE (Corpus-Steered Query Expansion) is the central methodological
contribution of this Arabic information-retrieval thesis.
Dataset: MIRACL Arabic dev set, 2,896 queries, Wikipedia corpus (8.7M passages, MSA).
LLM: Aya Expanse 8B (CohereForAI/aya-expanse-8b), BF16, A100 40 GB.

━━ STAGE 1: First-pass BM25 retrieval ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The user query q is submitted to a BM25s index over all 8.7 M passages.
BM25 returns the top k1 = 5 candidate passages (our implementation; the
original paper uses k=10). Each passage is truncated to 128 tokens.
These 5 passages are the CORPUS CONTEXT for Stage 2. They are NOT the
final retrieval result.

━━ STAGE 2: Four LLM calls (temp = 1.0, max_new_tokens = 128) ━━━━━━━━━━━━━
Aya Expanse 8B is called four times independently:

  CORPUS-GROUNDED samples c1, c2  [batch size 8; prompt ~800-1000 tokens]
    Prompt includes: query q + the 5 retrieved passages.
    Instruction (translated): "Examine the retrieved documents. Identify the
    relevant ones, even partially. Extract the key sentences from each document
    that contribute to their relevance."
    The LLM EXTRACTS text from the retrieved passages -- it does NOT generate
    free-form answers. This grounds the expansion in real corpus vocabulary
    and prevents hallucination.

  BLIND samples b1, b2  [batch size 32; prompt ~60-80 tokens]
    Prompt includes: query q only (no retrieved documents).
    Instruction: "Write a short passage to answer the question."
    The LLM generates from parametric knowledge (HyDE-style).
    These add vocabulary diversity not constrained by the first-pass results.

Ablation (exp 013c vs 013d vs 013):
  corpus-only (4c + 0b): nDCG@10 = 0.538
  blind-only  (0c + 4b): nDCG@10 = 0.575
  2+2 combined:          nDCG@10 = 0.616  <- best; types are complementary

━━ STAGE 3: Re-retrieval with the alpha-weighted expanded query ━━━━━━━━━━━━━
Final query assembled as:
  q_CSQE = q + q + q + q + c1 + c2 + b1 + b2
  (i.e., alpha = 4 copies of q concatenated before the four pseudo-documents)

The alpha = 4 repetition factor is REQUIRED to prevent term dilution: without
it, BM25 down-weights the original short query against the much longer appended
pseudo-documents. alpha = 4 = N_total (one repeat per expansion) was found
optimal in Exp 011 on BM25+blind QE.

q_CSQE is submitted to BM25 for a second retrieval pass. Final output: top-100
ranked passages used for evaluation.

━━ RESULTS (MIRACL Arabic dev, 2,896 queries) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BM25 alone:                  nDCG@10 = 0.4621  (baseline)
  Best blind QE (Aya, beta=2): nDCG@10 = 0.5855  (Exp 011)
  BM25 + CSQE (2+2, alpha=4):  nDCG@10 = 0.6157  (+33.2% over baseline)
  Hybrid RRF k=20 (no QE):     nDCG@10 = 0.6267  (dense + BM25 fusion, no QE)
  BEST: BM25+CSQE fused with Dense (original q) via RRF k=20:
                                nDCG@10 = 0.7137  <- thesis headline

CSQE error analysis: improves 56.8% of queries, regresses 16.6%.
Short queries (< 5 words) gain the most: delta nDCG = +0.199.

━━ WORKED EXAMPLE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Query: "ma hiya al-asma' al-khamsa fi al-lugha al-'arabiyya?"
Arabic: "ما هي الأسماء الخمسة في اللغة العربية؟"
English: "What are the Five Nouns in Arabic grammar?"

BLIND QE failure: LLM without corpus context confuses the Arabic grammar
term "Five Nouns" (a technical grammar category) with a list of personal
names -- it generates names like Muhammad, Adam, Ibrahim. BM25 retrieves
biography articles about people. Relevant grammar article is never found.
nDCG@10 = 0.000.

CSQE success: Stage 1 BM25 retrieves the correct Wikipedia article on
al-asma' al-khamsa (the Five Nouns: ab, akh, ham, faw, dhaw -- father,
brother, father-in-law, mouth, possessor-of). Stage 2 corpus-grounded
extraction locks onto this correct content. Stage 3 re-retrieval finds
the relevant grammar article. nDCG@10 = 1.000.

This query (qid 3034) is the clearest demonstration: blind QE makes a
category error that any Arabic speaker recognises instantly; CSQE fixes it
because the first-pass corpus prevents the hallucination.
"""

# ── Variant definitions ───────────────────────────────────────────────────────
VARIANTS = [
    {
        "id": "v1",
        "intent": (
            "A clear, stage-labelled flow diagram of the three-stage CSQE pipeline "
            "for Arabic BM25 retrieval. "
            "Stage 1 box: query q enters BM25, which returns the top-5 passages "
            "(each truncated to 128 tokens). "
            "Stage 2 box: Aya Expanse 8B is invoked 4 times (temp=1.0): "
            "two corpus-grounded calls (c1, c2) each receive query + 5 passages and "
            "EXTRACT key sentences; "
            "two blind calls (b1, b2) receive query only and generate from parametric "
            "knowledge. Use distinct visual styles (colour or shading) to distinguish "
            "corpus-grounded from blind boxes. "
            "Stage 3 box: the four pseudo-documents plus 4 repetitions of q are "
            "concatenated (show formula q x4 + c1+c2+b1+b2 or alpha=4 label), then "
            "fed to BM25 for the second retrieval. "
            "Annotate the final output: nDCG@10 = 0.616."
        ),
    },
    {
        "id": "v2",
        "intent": (
            "A side-by-side contrast figure showing WHY corpus grounding matters. "
            "Title: 'Blind Query2Doc vs. CSQE -- Arabic grammar query example'. "
            "LEFT column (Blind QE): "
            "  query (Five Nouns / al-asma' al-khamsa) -> Aya 8B (no context) "
            "  -> generates list of personal names: Muhammad, Adam, Ibrahim ... "
            "  -> BM25 retrieves biography articles "
            "  -> relevant grammar article not found -> nDCG@10 = 0.000. "
            "RIGHT column (CSQE): "
            "  query -> BM25 first-pass retrieves grammar article on Five Nouns "
            "  -> Aya 8B extracts: father/ab, brother/akh, father-in-law/ham, "
            "     mouth/faw, possessor/dhaw from the retrieved article "
            "  -> BM25 re-retrieval finds the correct grammar article "
            "  -> nDCG@10 = 1.000. "
            "The category-error hallucination on the left vs. corpus-anchored "
            "extraction on the right is the single visual point. "
            "Show the Arabic terms where possible."
        ),
    },
    {
        "id": "v3",
        "intent": (
            "A compact pipeline overview designed for single-column thesis width (~8 cm). "
            "Three horizontal bands: "
            "  Band 1 (Stage 1): query q -> BM25 -> top-5 passages. "
            "  Band 2 (Stage 2): four LLM call boxes arranged in two pairs -- "
            "    c1+c2 (corpus-grounded, one colour) and b1+b2 (blind, different colour). "
            "    Label: Aya Expanse 8B, temp=1.0. "
            "  Band 3 (Stage 3): concatenation node showing 'q*4 + c1+c2+b1+b2' "
            "    (alpha=4 repetitions) -> BM25 second pass -> final ranked list. "
            "Keep all text labels short. Show nDCG improvement: 0.462 -> 0.616."
        ),
    },
    {
        "id": "v4",
        "intent": (
            "A narrative figure foregrounding the corpus-grounding mechanism "
            "as a fork-and-merge topology. "
            "From a central query node, two branches diverge: "
            "  CORPUS BRANCH: query -> BM25 (k1=5) -> 5 Wikipedia passages -> "
            "    Aya 8B (extract key sentences) -> c1, c2. "
            "  BLIND BRANCH: query -> Aya 8B (generate from knowledge) -> b1, b2. "
            "Both branches converge at a MERGE node that assembles the final expanded "
            "query. Display the assembly formula as a banner or framed node: "
            "  q_CSQE = [q][q][q][q][c1][c2][b1][b2] "
            "  (four copies of q, then four pseudo-documents). "
            "The merged query feeds into BM25 for the final retrieval step. "
            "Label the corpus branch with 'vocabulary anchored in Wikipedia text' "
            "and the blind branch with 'parametric diversity'. "
            "Show the headline metric: nDCG@10 = 0.616 for BM25+CSQE."
        ),
    },
]


async def generate_variant(pipeline, variant, idx):
    vid = variant["id"]
    sys.stdout.write(f"\n[{idx+1}/{len(VARIANTS)}] Generating {vid} ...\n")
    sys.stdout.flush()

    result = await pipeline.generate(GenerationInput(
        source_context=SHARED_CONTEXT,
        communicative_intent=variant["intent"],
        diagram_type=DiagramType.METHODOLOGY,
    ))

    src = Path(result.image_path)
    dst = OUT_DIR / f"fig_3_8_csqe_aigen_{vid}.png"
    shutil.copy2(src, dst)

    n_iter = len(result.iterations) if result.iterations else 1
    sys.stdout.write(f"[OK] {vid} saved ({n_iter} iteration(s)): {dst.name}\n")
    sys.stdout.flush()
    return dst


async def main():
    settings = Settings(
        vlm_model="gemini-3.1-pro-preview",
        image_model="gemini-3-pro-image",
        refinement_iterations=3,
    )
    pipeline = PaperBananaPipeline(settings=settings)

    for idx, variant in enumerate(VARIANTS):
        await generate_variant(pipeline, variant, idx)

    sys.stdout.write("\nAll 4 variants complete.\n")
    sys.stdout.flush()


if __name__ == "__main__":
    asyncio.run(main())
