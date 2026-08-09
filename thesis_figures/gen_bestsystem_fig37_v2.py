"""
PaperBanana regeneration of Figure 3.7 (best-performing system architecture) -- v2.

Replaces fig_3_9_best_system.pdf (plain TikZ), whose visual design the user
found weak, and whose "Query + CSQE corpus-grounded pdoc" box label omits
both the alpha=4 query repetition AND the blind pseudo-documents (b1, b2) --
"CSQE-expanded query" is defined in chapter3.tex Sec. 3.8.3 / Eq. 3.5 as the
FULL assembled query q_CSQE = q x4 + c1 + c2 + b1 + b2, same object shown in
Figure 3.6's Stage 3.

Provider: Google Gemini (gemini-3.1-pro-preview VLM, gemini-3-pro-image /
"Nano Banana Pro" image gen) -- the same provider that produced a clean,
error-free Figure 3.6 after 2 refinement rounds.

Usage:
    PowerShell:  $env:GOOGLE_API_KEY='<key>'; python thesis_figures/gen_bestsystem_fig37_v2.py
    bash:        GOOGLE_API_KEY=<key> python thesis_figures/gen_bestsystem_fig37_v2.py

Outputs: thesis_figures/output/png/fig_3_9_best_system_aigen_v2{a,b}.png

Facts verified against:
  University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter3.tex
    Sec 3.8.1 (Eq. 3.5, q_CSQE definition), Sec 3.8.3 (retriever-specific
    application, Figure 3.7 / fig:best_system caption).
  CLAUDE.md reference table: "A: BM25-expanded (BM25+CSQE + Dense raw), RRF
    k=20" = NDCG@10 0.7137 (thesis caption rounds to 0.714).
"""

import asyncio
import os
import shutil
import sys
from pathlib import Path

if not os.environ.get("GOOGLE_API_KEY"):
    raise EnvironmentError("GOOGLE_API_KEY env var not set")

from paperbanana import PaperBananaPipeline, GenerationInput, DiagramType
from paperbanana.core.config import Settings

OUT_DIR = Path("thesis_figures/output/png")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SCRATCH = Path(os.environ.get("PB_OUT", "outputs"))

# ── Verified source context ───────────────────────────────────────────────────
SOURCE_CONTEXT = """\
This diagram documents the best-performing system of an Arabic
information-retrieval thesis (MIRACL Arabic dev set, 2,896 queries; corpus =
2,061,414 Arabic Wikipedia passages). It is a SYSTEM-LEVEL fusion diagram --
it shows where the CSQE-expanded query plugs into a two-retriever fusion
pipeline. It does NOT re-derive how CSQE builds that query (that is a
separate, already-existing figure); it only needs to correctly SUMMARISE the
expanded query's composition in one compact label.

=== WHAT q_CSQE IS (do not simplify or drop parts of this) ===
q_CSQE = q + q + q + q + c1 + c2 + b1 + b2
  - "q" is the original user query, repeated alpha = 4 times.
  - c1, c2 are two corpus-grounded pseudo-documents (extracted from
    first-pass retrieved passages by Aya Expanse 8B).
  - b1, b2 are two blind pseudo-documents (generated from parametric
    knowledge by Aya Expanse 8B, no retrieved context).
  - THIS IS THE FULL DEFINITION. A box that mentions only "corpus-grounded"
    content and omits the repetition and the blind samples is WRONG and must
    not be reproduced. Every part -- the x4 repetition AND all four pseudo-
    documents c1, c2, b1, b2 -- must be visible in the diagram's CSQE box.

=== THE FIVE-NODE PIPELINE (do not add, remove, merge or reorder nodes) ===
1. START: "User Query q" -- a single node.
2. It forks into exactly two parallel, independent paths:

   TOP PATH (BM25 gets the expanded query):
     "User Query q" -> "CSQE-Expanded Query" node, which must display BOTH
     of these facts compactly: (a) the query is repeated alpha = 4 times,
     and (b) it is concatenated with four pseudo-documents c1, c2, b1, b2.
     Render this as the formula "q_CSQE = q x4 + c1 + c2 + b1 + b2" inside
     or directly under the node -- small, legible, not decorative -- so a
     reader sees the full composition at a glance without needing another
     figure. Then -> "BM25 Retrieval" -> its ranked list.

   BOTTOM PATH (Dense gets the ORIGINAL, unexpanded query):
     "User Query q" -> "Original Query (unexpanded)" -> "mDPR Retrieval" ->
     its ranked list. This path never touches CSQE, c1/c2/b1/b2, or alpha.

3. MERGE: both ranked lists feed into "RRF Fusion, k = 20".
4. FINAL: "RRF Fusion" -> "Final Top-100 Ranked List" annotated with the
   headline result: NDCG@10 = 0.714.

=== FACTUAL CONSTRAINTS -- THESE ERRORS MUST NOT APPEAR ===
1. The CSQE box must show ALL of: the x4 repetition of q, AND c1, c2, b1,
   b2. Do not show only "corpus-grounded" content -- the blind samples b1,
   b2 are an equally required part of q_CSQE.
2. The bottom path (mDPR) must carry the ORIGINAL query, never an expanded
   one. No arrow from the CSQE box to the mDPR branch.
3. Both retrieval outputs must merge at RRF fusion -- do not show BM25 or
   mDPR feeding the final result directly, and do not add a re-ranking step
   that is not RRF fusion.
4. The final NDCG@10 value is 0.714. Do not invent or alter this number.
5. Do not introduce any model or retriever other than: Aya Expanse 8B
   (inside the CSQE label only, if at all), BM25, mDPR, RRF fusion.
"""

STYLE_RULES = """\
STRICT RENDERING RULES:
- All text must be English and plain ASCII. No Arabic script, no Greek
  letters drawn as glyphs -- write the word "alpha" or use "x4" for the
  repetition. Spell out "NDCG@10".
- Every word must be spelled correctly and fully legible at thesis print
  size. Proofread every box for accidental duplicated words before
  finalizing -- do not repeat any label twice inside the same box.
- Every arrow must start and end on a box. No dangling, crossing or
  ambiguous arrows. If two arrows must cross, route them around instead.
- Flat, clean, modern academic vector style on a white background: rounded
  rectangles, 1-2 pt outlines, a restrained palette (one hue for the
  CSQE/expansion node, one for retrieval blocks, one for the fusion block,
  one highlight color for the final output). No 3-D, no drop shadows, no
  gradients, no photographic texture, no clip-art, no glow effects, no
  washed-out or faded background -- background must stay crisp white.
- This is a compact, single-row system diagram (not a multi-stage panel
  layout like a pipeline explainer) -- keep it tight and horizontal, sized
  for a thesis figure at roughly 95% text width.
"""

VARIANTS = [
    {
        "id": "v2a",
        "aspect": "16:9",
        "intent": (
            "A compact, single-row, left-to-right system architecture diagram "
            "for a thesis methodology section, matching the five-node pipeline "
            "described above exactly. "
            "Start at the left with one node 'User Query q'. From it, two arrows "
            "fork: one goes UP-RIGHT, one goes DOWN-RIGHT, into two clearly "
            "separated horizontal lanes (top lane and bottom lane) that run in "
            "parallel to the right and never touch each other. "
            "TOP LANE: 'User Query q' -> a highlighted node titled "
            "'CSQE-Expanded Query' that shows underneath its title, in smaller "
            "text, the formula 'q_CSQE = q x4 + c1 + c2 + b1 + b2' -- make this "
            "node visually distinct (e.g. a star icon or accent border) since it "
            "is the thesis's key contribution -> arrow -> 'BM25 Retrieval' node. "
            "BOTTOM LANE: 'User Query q' -> 'Original Query (unexpanded)' node "
            "-> arrow -> 'mDPR Retrieval' node. "
            "Both lanes' outputs then converge with two arrows into a single "
            "node 'RRF Fusion, k = 20' positioned between and to the right of "
            "the two lanes. "
            "From the fusion node, one arrow continues right to the final node: "
            "a highlighted box 'Final Top-100 Ranked List' with the annotation "
            "'NDCG@10 = 0.714' shown clearly beneath or beside it. "
            + STYLE_RULES
        ),
    },
    {
        "id": "v2b",
        "aspect": "21:9",
        "intent": (
            "A wide, ultra-compact banner-style system diagram, left to right, "
            "for a thesis figure that must fit at small print size. Same five- "
            "node topology as described above: 'User Query q' forks into a top "
            "lane and a bottom lane. "
            "TOP LANE (highlighted / accent color, since this is the thesis's "
            "novel contribution): 'User Query q' -> node 'CSQE-Expanded Query' "
            "containing, in one or two compact lines, both the repetition and "
            "the pseudo-documents: 'q x4 + c1 + c2 + b1 + b2' -- draw this as a "
            "small formula banner INSIDE the node so it reads in one glance, "
            "not as a separate detached label -> 'BM25' node. "
            "BOTTOM LANE (neutral color): 'User Query q' -> 'Original Query' -> "
            "'mDPR' node. "
            "Both lanes converge into 'RRF Fusion (k=20)' -> final highlighted "
            "node 'Top-100 -- NDCG@10 = 0.714'. "
            "Keep every box small and every label short; this diagram must "
            "remain legible even when scaled down to roughly 8cm tall. "
            + STYLE_RULES
        ),
    },
]


async def generate_variant(pipeline, variant, idx, total):
    vid = variant["id"]
    sys.stdout.write(f"\n[{idx + 1}/{total}] Generating {vid} ...\n")
    sys.stdout.flush()

    result = await pipeline.generate(GenerationInput(
        source_context=SOURCE_CONTEXT,
        communicative_intent=variant["intent"],
        diagram_type=DiagramType.METHODOLOGY,
        aspect_ratio=variant["aspect"],
    ))

    dst = OUT_DIR / f"fig_3_9_best_system_aigen_{vid}.png"
    shutil.copy2(Path(result.image_path), dst)

    n_iter = len(result.iterations) if result.iterations else 1
    sys.stdout.write(f"[OK] {vid} saved ({n_iter} iteration(s)): {dst}\n")
    sys.stdout.flush()
    return dst


async def main():
    settings = Settings(
        vlm_provider="gemini",
        vlm_model="gemini-3.1-pro-preview",
        image_provider="google_imagen",
        image_model="gemini-3-pro-image",  # Nano Banana Pro
        google_api_key=os.environ["GOOGLE_API_KEY"],
        refinement_iterations=4,
        output_dir=str(SCRATCH),
    )
    pipeline = PaperBananaPipeline(settings=settings)

    only = sys.argv[1:] or None
    todo = [v for v in VARIANTS if not only or v["id"] in only]
    for idx, variant in enumerate(todo):
        await generate_variant(pipeline, variant, idx, len(todo))

    sys.stdout.write("\nDone.\n")
    sys.stdout.flush()


if __name__ == "__main__":
    asyncio.run(main())
