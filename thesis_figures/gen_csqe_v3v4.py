"""Generate CSQE variants v3 and v4 only."""
import asyncio
import os
import shutil
import sys
from pathlib import Path

os.environ.setdefault("GOOGLE_API_KEY", "AIzaSyBEleYdOfIkr6aJ_Pjlxaxkz1GOkzY2NJE")

from paperbanana import PaperBananaPipeline, GenerationInput, DiagramType
from paperbanana.core.config import Settings

OUT_DIR = Path("thesis_figures/output/png")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SHARED_CONTEXT = """\
CSQE (Corpus-Steered Query Expansion) is the central contribution of this
Arabic information-retrieval thesis. The system improves BM25 search over the
MIRACL Arabic Wikipedia corpus through a three-stage pipeline:

STAGE 1 - First-pass retrieval
The original user query q is sent to BM25 against the MIRACL Arabic corpus
(8.7 million Wikipedia passages). BM25 returns the top-k1 = 5 candidate
passages D1 to D5. These passages serve as corpus context for Stage 2; they
are not the final answer.

STAGE 2 - LLM expansion (four independent samples from Aya Expanse 8B)
The Aya Expanse 8B multilingual LLM is called four times:

  - Corpus-grounded samples c1, c2 (two calls): Prompt = q + D1 to D5.
    The LLM is told to write a short Arabic passage that answers the query
    using the retrieved documents. These samples borrow real corpus vocabulary
    and resist hallucination.

  - Blind samples b1, b2 (two calls): Prompt = q only (no retrieved context).
    The LLM draws on parametric knowledge. These samples add diverse
    vocabulary not constrained by the first-pass results.

Ablation: the 2+2 combination outperforms corpus-only (4c+0b) or blind-only
(0c+4b) variants, confirming the two sample types are complementary.

STAGE 3 - Re-retrieval with the expanded query
Final expanded query assembled as:
  q_CSQE = (q repeated alpha=4 times) + c1 + c2 + b1 + b2

The alpha=4 query repetitions counter BM25 term dilution caused by the long
appended pseudo-documents. alpha=4 was the optimal value in Exp 011.

This expanded query is fed to BM25 a second time, producing the final
top-100 ranked passages for evaluation.

RESULTS:
- CSQE on BM25 alone: nDCG@10 = 0.616 (+33% over BM25 baseline 0.462)
- Best system (CSQE on BM25 + Dense on original q, fused via RRF k=20):
  nDCG@10 = 0.714 (thesis headline result)

KEY INSIGHT: Corpus-grounded samples anchor the expansion in real Wikipedia
text. Blind samples broaden vocabulary. Together they prevent the
hallucination failure modes seen in plain blind Query2Doc.

WORKED EXAMPLE - query about the Five Nouns in Arabic grammar:
- Blind Query2Doc mistakes the grammar term for a list of common names
  (Muhammad, Adam, Ibrahim...), retrieving wrong Wikipedia articles: nDCG=0.0
- CSQE retrieves the Wikipedia article on the Five Nouns in Stage 1,
  grounds c1/c2 in correct grammar content (father, brother, etc.),
  and recovers the relevant passage in Stage 3: nDCG=1.0
"""

VARIANTS = [
    {
        "id": "v3",
        "intent": (
            "A compact overview that fits in a thesis single-column figure. "
            "Show the pipeline as three horizontal bands labelled Stage 1, Stage 2, "
            "Stage 3. Inside Stage 2 show four distinct LLM call boxes: c1 and c2 "
            "shaded one colour (corpus-grounded), b1 and b2 shaded a different colour "
            "(blind). Show the query repetition factor alpha=4 in the Stage 3 "
            "concatenation formula. Keep labels concise so nothing is crowded."
        ),
    },
    {
        "id": "v4",
        "intent": (
            "A narrative-driven figure that foregrounds the corpus-grounding mechanism. "
            "Show the two-path divergence clearly: one path from the query goes straight "
            "to Aya 8B (blind), the other first hits BM25, retrieves real Wikipedia "
            "passages, then goes to Aya 8B (grounded). Both paths produce pseudo-documents "
            "that are concatenated with four repetitions of the original query before the "
            "final BM25 retrieval. Show the query repetition formula "
            "q+q+q+q+c1+c2+b1+b2 as a visual element rather than just a text label."
        ),
    },
]


async def main():
    settings = Settings(vlm_model="gemini-2.5-flash", refinement_iterations=3)
    pipeline = PaperBananaPipeline(settings=settings)

    for variant in VARIANTS:
        vid = variant["id"]
        sys.stdout.write(f"Generating {vid}...\n")
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
        sys.stdout.write(f"[OK] {vid} saved, {n_iter} iterations\n")
        sys.stdout.flush()

    sys.stdout.write("ALL DONE\n")
    sys.stdout.flush()


if __name__ == "__main__":
    asyncio.run(main())
