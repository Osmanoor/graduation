"""
PaperBanana generation script for CSQE figure variants.
Run: python thesis_figures/gen_csqe_variants.py
Outputs go to: thesis_figures/output/png/fig_3_8_csqe_aigen_v*.png
"""

import asyncio
import os
import shutil
from pathlib import Path

# Must be set before importing Settings so BaseSettings picks it up via alias
# Set GOOGLE_API_KEY in your environment before running, e.g.:
#   export GOOGLE_API_KEY=<your-key>   (Linux/macOS)
#   $env:GOOGLE_API_KEY="<your-key>"   (PowerShell)
if not os.environ.get("GOOGLE_API_KEY"):
    raise EnvironmentError("GOOGLE_API_KEY env var not set")

from paperbanana import PaperBananaPipeline, GenerationInput, DiagramType
from paperbanana.core.config import Settings

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
OUT_DIR = Path("thesis_figures/output/png")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── shared context ────────────────────────────────────────────────────────────
SHARED_CONTEXT = """\
CSQE (Corpus-Steered Query Expansion) is the central contribution of this
Arabic information-retrieval thesis.  The system improves BM25 search over the
MIRACL Arabic Wikipedia corpus through a three-stage pipeline:

STAGE 1 — First-pass retrieval
The original user query q is sent to BM25 against the MIRACL Arabic corpus
(8.7 million Wikipedia passages).  BM25 returns the top-k₁ = 5 candidate
passages D₁…D₅.  These passages serve as corpus context for Stage 2; they
are not the final answer.

STAGE 2 — LLM expansion (four independent samples from Aya Expanse 8B)
The Aya Expanse 8B multilingual LLM is called four times:

  • Corpus-grounded samples c₁, c₂ (two calls):  Prompt = q + D₁…D₅.
    The LLM is told to write a short Arabic passage that answers the query
    using the retrieved documents.  These samples borrow real corpus
    vocabulary and resist hallucination.

  • Blind samples b₁, b₂ (two calls):  Prompt = q only (no retrieved
    context).  The LLM draws on parametric knowledge.  These samples add
    diverse vocabulary not constrained by the first-pass results.

Ablation result: the 2+2 combination outperforms either corpus-only (4c+0b)
or blind-only (0c+4b) variants, confirming the two sample types are
complementary.

STAGE 3 — Re-retrieval with the expanded query
The final expanded query is assembled as:
  q_CSQE = (q repeated α=4 times) ⊕ c₁ ⊕ c₂ ⊕ b₁ ⊕ b₂

The α=4 query repetitions are critical: without them, BM25 term dilution
caused by the long appended pseudo-documents would suppress the original
query signal.  α=4 was found to be the optimal value in Exp 011.

This expanded query is fed to BM25 a second time, producing the final
top-100 ranked passages used for evaluation.

RESULTS:
• CSQE on BM25 alone:  nDCG@10 = 0.616  (+33% over BM25 baseline 0.462)
• Best system (CSQE on BM25 + Dense on original q, fused via RRF k=20):
  nDCG@10 = 0.714  (thesis headline result; the Dense+RRF fusion is a
  separate architectural step shown in a different figure)

KEY INSIGHT:
Corpus-grounded samples anchor the expansion in real Wikipedia text (actual
Arabic vocabulary, correct entity names).  Blind samples broaden vocabulary.
Together they prevent the hallucination failure modes seen in plain Query2Doc.

WORKED EXAMPLE — query "ما هي الأسماء الخمسة في اللغة العربية؟"
(What are the Five Nouns in Arabic grammar?)
• Blind Query2Doc mistakes the grammar term for a list of common names
  (Muhammad, Adam, Ibrahim …), retrieving the wrong Wikipedia articles
  → nDCG@10 = 0.000.
• CSQE retrieves the Wikipedia article on الأسماء الخمسة in Stage 1,
  grounds c₁/c₂ in the correct grammar content (أب أخ حم فو ذو),
  and recovers the relevant passage in Stage 3 → nDCG@10 = 1.000.
"""


# ── variant definitions ───────────────────────────────────────────────────────
VARIANTS = [
    {
        "id": "v1",
        "intent": (
            "A clear, stage-labelled flowchart of the CSQE three-stage pipeline. "
            "Show the user query entering Stage 1 (BM25 first-pass), the top-5 "
            "retrieved passages flowing into Stage 2 where Aya 8B produces four "
            "samples (two corpus-grounded c₁,c₂ and two blind b₁,b₂), then all "
            "four samples plus α=4 query repetitions concatenated into one expanded "
            "query in Stage 3 (BM25 second-pass) producing the final ranked list. "
            "Differentiate the corpus-grounded samples visually from the blind samples. "
            "Include the result nDCG@10 = 0.616."
        ),
        "iterations": 3,
    },
    {
        "id": "v2",
        "intent": (
            "A side-by-side comparison layout contrasting Blind Query2Doc (left column) "
            "with CSQE (right column), using the الأسماء الخمسة worked example. "
            "Left column: query → LLM (no context) → hallucinates a list of names → "
            "wrong retrieval → nDCG@10 = 0.000. "
            "Right column: query → BM25 first-pass → top-5 passages → LLM produces "
            "corpus-grounded expansion about أب أخ حم فو ذو → correct retrieval → "
            "nDCG@10 = 1.000. "
            "The visual contrast between the two paths is the main point."
        ),
        "iterations": 3,
    },
    {
        "id": "v3",
        "intent": (
            "A compact overview that fits in a thesis single-column figure. "
            "Show the pipeline as three horizontal bands labelled Stage 1, Stage 2, "
            "Stage 3. Inside Stage 2 show four distinct LLM call boxes: c₁ and c₂ "
            "shaded one colour (corpus-grounded), b₁ and b₂ shaded a different colour "
            "(blind). Show the query repetition factor α=4 in the Stage 3 concatenation "
            "formula. Keep labels concise so nothing is crowded."
        ),
        "iterations": 3,
    },
    {
        "id": "v4",
        "intent": (
            "A narrative-driven figure that foregrounds the corpus-grounding mechanism. "
            "Show the two-path divergence clearly: one path from the query goes straight "
            "to Aya 8B (blind), the other first hits BM25, retrieves real Wikipedia "
            "passages, then goes to Aya 8B (grounded). Both paths produce pseudo-documents "
            "that are concatenated with four repetitions of the original query before the "
            "final BM25 retrieval. Show the query repetition formula q⊕q⊕q⊕q⊕c₁⊕c₂⊕b₁⊕b₂ "
            "as a visual element rather than just a text label."
        ),
        "iterations": 3,
    },
]


async def generate_variant(pipeline, variant, idx):
    vid = variant["id"]
    print(f"\n[{idx+1}/{len(VARIANTS)}] Generating {vid}…")

    gen_input = GenerationInput(
        source_context=SHARED_CONTEXT,
        communicative_intent=variant["intent"],
        diagram_type=DiagramType.METHODOLOGY,
    )

    result = await pipeline.generate(gen_input)

    src = Path(result.image_path)
    dst = OUT_DIR / f"fig_3_8_csqe_aigen_{vid}.png"
    shutil.copy2(src, dst)
    n_iter = len(result.iterations) if result.iterations else 1
    print(f"  [OK] saved -> {dst.name}  (iterations: {n_iter})")
    return dst


async def main():
    settings = Settings(
        vlm_model="gemini-2.5-flash",
        refinement_iterations=3,
    )
    pipeline = PaperBananaPipeline(settings=settings)

    results = []
    for idx, variant in enumerate(VARIANTS):
        dst = await generate_variant(pipeline, variant, idx)
        results.append(dst)

    print("\n\nAll variants generated:")
    for p in results:
        print(f"  {p}")


if __name__ == "__main__":
    asyncio.run(main())
