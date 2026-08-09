"""
PaperBanana regeneration of Figure 3.6 (CSQE pipeline) -- v5, corrected.

Provider: OpenAI (gpt-4o for planning/styling/critic, gpt-image-1 for image
generation). Google Gemini keys were tried first but every one had zero
image-gen quota (free tier); this run uses an OpenAI key with confirmed,
working billing instead.

Replaces fig_3_8_csqe_aigen_v4_boosted.png, which contained four structural
errors (diagnosed 2026-08-09):
  1. Top-5 passages were shown feeding the BLIND LLM (blind sees q only).
  2. A fabricated "Query Re-Ranker" block -- CSQE does no re-ranking.
  3. Query repetition (alpha=4 copies of q) was missing from the diagram.
  4. Final output labelled "D1-D5" -- it is a full second-pass corpus search
     returning the top-100.

Usage:
    PowerShell:  $env:OPENAI_API_KEY='<key>'; python thesis_figures/gen_csqe_fig36_v5.py
    bash:        OPENAI_API_KEY=<key> python thesis_figures/gen_csqe_fig36_v5.py

    Optional: pass one or more variant ids to generate only those, e.g.
        python thesis_figures/gen_csqe_fig36_v5.py v5a

Outputs: thesis_figures/output/png/fig_3_8_csqe_aigen_v5{a,b,c}.png

Facts verified against:
  arabic-rag-query-enhancement/experiments/exp_013_csqe_aya_8b.ipynb (CONFIG cell)
  University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter3.tex (Sec 3.8)
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
This diagram documents CSQE (Corpus-Steered Query Expansion) exactly as
implemented in an Arabic information-retrieval thesis (MIRACL Arabic dev set,
2,896 queries, Arabic Wikipedia, 2,061,414 passages; LLM = Aya Expanse 8B).

The diagram must show FOUR steps, in this exact order, with these exact
data-flow connections. Do not add, merge, rename or reorder any step.

=== STEP 1 -- FIRST-PASS RETRIEVAL ===
  INPUT : the user query q (short, one line of text)
  BLOCK : BM25 (first pass), searching the MIRACL Arabic corpus index
  OUTPUT: the top k1 = 5 candidate passages, labelled D1 D2 D3 D4 D5
  These 5 passages are CONTEXT for step 2 only. They are NOT the final answer.

=== STEP 2 -- PARALLEL LLM GENERATION (two independent branches) ===
  Both branches call the SAME model, Aya Expanse 8B, temperature 1.0,
  max 128 new tokens, and both run at the same time (in parallel).

  BRANCH A -- BLIND (generative):
    INPUT : the user query q ONLY.
            *** The blind branch NEVER receives D1-D5. There must be NO arrow
            of any kind from the top-5 passages into the blind branch. ***
    TASK  : "write a passage that answers the query" -- the model writes from
            its own parametric knowledge, HyDE style.
    OUTPUT: 2 blind pseudo-documents, labelled b1 and b2.

  BRANCH B -- CORPUS-GROUNDED (extractive):
    INPUT : the underlying LLM prompt contains both q and the five passages
            D1-D5, but in the DIAGRAM draw only ONE incoming arrow into this
            box -- from "Top-5 Passages D1-D5" -- since q's involvement is
            already implied by q having produced D1-D5 upstream in Stage 1.
            Do not draw a second arrow from "User Query q" into this box.
            *** This is the ONLY branch that consumes D1-D5. ***
    TASK  : "examine the retrieved documents and extract the key sentences
            relevant to the query" -- the model EXTRACTS existing sentences,
            it does not invent new content.
    OUTPUT: 2 corpus-grounded pseudo-documents, labelled c1 and c2.

=== STEP 3 -- QUERY ASSEMBLY (plain string concatenation) ===
  This step is a simple CONCATENATION of text strings. Nothing is scored,
  sorted, filtered, weighted, selected or re-ranked here.
  INPUTS: (i) the original query q repeated alpha = 4 times, and
          (ii) the four pseudo-documents c1, c2, b1, b2 (each used once).
  OUTPUT: the expanded query
            q_CSQE = q q q q + c1 + c2 + b1 + b2
  WHY alpha = 4: repeating q counteracts BM25 term dilution, because the four
  appended pseudo-documents are far longer than the original query.

=== STEP 4 -- SECOND-PASS RE-RETRIEVAL ===
  INPUT : the expanded query q_CSQE
  BLOCK : BM25 (second pass) -- a COMPLETE, FRESH search over the entire
          2.06M-passage corpus index, not a re-scoring of D1-D5.
  OUTPUT: the final ranked list, top-100 passages.
  RESULT: NDCG@10 = 0.616, up from 0.462 for BM25 with the raw query q.

=== FACTUAL CONSTRAINTS -- THESE ERRORS MUST NOT APPEAR ===
  1. There is NO re-ranker, NO "query re-ranker", NO re-ranking block, and no
     box, arrow or label containing the words "rank", "re-rank" or "re-ranked"
     anywhere in the figure. CSQE concatenates strings; it never re-ranks.
  2. The blind LLM branch is fed by q alone. No line may run from the top-5
     passages box to the blind LLM box.
  3. The alpha = 4 repetition of q must be visible in step 3 as an explicit
     element (for example a row of four small "q" chips, or the literal text
     "q x 4"). It is not optional decoration -- it is a core mechanism.
  4. The final output is the top-100 passages from a full corpus search. It
     must NOT be drawn or labelled as D1-D5, and must not look like the same
     five passages coming back.
  5. alpha = 4 is the number of times q is REPEATED in step 3. It is not the
     number of LLM calls. Never write "alpha" next to the LLM boxes.
  6. Exactly 2 blind samples (b1, b2) and exactly 2 grounded samples (c1, c2).
     Not 4 of each, not 5, not 1.
  7. Both LLM boxes are the same model, Aya Expanse 8B. Do not name any other
     model, and do not show a second, different model.
  8. The blind LLM box and the corpus-grounded LLM box are PARALLEL siblings,
     not a chain. There must be NO arrow directly connecting the blind LLM box
     to the corpus-grounded LLM box (in either direction). Each receives its
     own input independently and produces its own output independently.
  9. Every one of the four stage titles -- "Stage 1", "Stage 2", "Stage 3",
     "Stage 4" -- must appear as a visible heading somewhere in the image.
     Do not silently drop a stage's title.
  10. The assembly formula/chips in Stage 3 must display all EIGHT symbols,
      once each, in this order: q, q, q, q, c1, c2, b1, b2. Do not omit c1,
      c2 or b2. Do not draw a redundant second "qqqq" block in addition to
      four separate q chips -- draw the four q's exactly once.
  11. Spell "concatenation" correctly in every occurrence.
  12. The arrow feeding the blind LLM box must visibly originate at the
      "User Query q" box itself (touch its border directly), not at the BM25
      box or anywhere along the BM25-to-passages chain. Route it with a
      clearly visible gap above/around the BM25 box so no reader could trace
      it back to BM25 -- it must read unambiguously as "q, and only q, goes
      to the blind LLM."
  13. Do not repeat any label text twice inside the same box. In particular,
      the corpus-grounded LLM box must say "Corpus-Grounded" exactly ONCE.
      Proofread every box for accidental duplicated words/lines before
      finalizing.
  14. Exactly ONE arrow may leave the "Top-5 Passages D1-D5" box, and it must
      point to the corpus-grounded LLM box. Do NOT draw two separate arrows
      (or one arrow split into two parallel line segments/elbows) between
      "Top-5 Passages D1-D5" and the corpus-grounded LLM box -- a single
      line, single arrowhead, one clean connection.
  15. The four stage panels (the large rounded background rectangles behind
      Stage 1, Stage 2, Stage 3, Stage 4) must NOT all be the same flat grey.
      Give each of the four panels its own distinct light pastel tint (for
      example: pale blue for Stage 1, pale green for Stage 2, pale purple/
      lavender for Stage 3, pale amber/yellow for Stage 4), so the four
      stages are visually distinguishable from each other at a glance while
      staying light enough that the black text and the inner colored boxes
      remain fully legible on top of them.
"""

# ── Shared rendering constraints appended to every variant intent ─────────────
STYLE_RULES = """\
STRICT RENDERING RULES:
- All text must be English and plain ASCII. No Arabic script, no Greek letters
  drawn as glyphs -- write the word "alpha" instead. Spell out "NDCG@10".
- Every word must be spelled correctly and be fully legible at thesis print
  size. Prefer few, short labels over many long ones. No filler lorem text,
  no fake sub-labels, no decorative unreadable micro-text.
- Every arrow must start and end on a box. No dangling, crossing or ambiguous
  arrows. If two arrows must cross, route them around instead.
- Flat, clean, modern academic vector style on a white background: rounded
  rectangles, 1-2 pt outlines, a restrained palette (one hue for retrieval
  blocks, one for LLM blocks, one for the assembly block, grey for data).
  No 3-D, no drop shadows, no gradients, no photographic texture, no clip-art
  robots, no glow effects.
- Use a colour key that separates the two branches: the blind branch and the
  corpus-grounded branch must be visibly different colours, and the legend or
  labels must say which is which.
"""


VARIANTS = [
    {
        "id": "v5a",
        "aspect": "16:9",
        "intent": (
            "A horizontal, four-stage pipeline flowchart for a thesis methodology "
            "section, read left to right, with each stage inside its own labelled, "
            "lightly tinted panel. "
            "The four panel backgrounds must use four DIFFERENT light pastel tints "
            "(e.g. pale blue / pale green / pale lavender / pale amber), not a "
            "single repeated grey -- this is required, not optional. "
            "PANEL 1 (pale blue background) titled 'Stage 1: First-Pass "
            "Retrieval': box 'User Query q' -> "
            "box 'BM25 (first pass)' with a small database cylinder underneath "
            "labelled 'MIRACL Arabic Corpus' -> data box 'Top-5 Passages D1-D5'. "
            "Exactly ONE arrow leaves the 'Top-5 Passages D1-D5' box (it targets "
            "the corpus-grounded LLM box in Panel 2) -- never draw two arrows or "
            "a doubled/split line between these two boxes. "
            "PANEL 2, HEADED with the visible title 'Stage 2: Parallel LLM "
            "Generation' at its top (do not omit this heading): two SIDE-BY-SIDE "
            "columns, drawn at the same height, with a visible gap between them "
            "and NO arrow of any kind connecting one column to the other. "
            "LEFT column is the blind branch: an arrow carrying only the query q "
            "starts by visibly touching the border of the 'User Query q' box "
            "(not the BM25 box), then routes above panel 1 with a clear visible "
            "gap over the BM25 box, so it clearly bypasses BM25 and the passages "
            "box entirely and cannot be mistaken for originating at BM25 -- "
            "enters box 'Aya Expanse 8B - Blind (generate), 2 samples' -> data "
            "box 'b1, b2'. "
            "RIGHT column is the corpus-grounded branch: exactly ONE arrow enters "
            "it, from 'Top-5 Passages D1-D5' directly to box 'Aya Expanse 8B - "
            "Corpus-Grounded (extract key sentences), 2 samples' -> data box "
            "'c1, c2'. Do not draw a second arrow into this box from anywhere else "
            "-- one single line, one arrowhead. The left and right columns are "
            "independent siblings that both start from panel 1 -- neither one "
            "feeds into the other. "
            "Add the small caption 'temperature 1.0, 128 tokens' once under the "
            "panel title. "
            "PANEL 3 titled 'Stage 3: Query Assembly (concatenation, spelled "
            "correctly)': a single wide box labelled 'Concatenate'. Into it flow "
            "a single horizontal row of exactly eight small chips, left to right, "
            "reading: q, q, q, q, c1, c2, b1, b2 -- each symbol drawn exactly "
            "once, no duplicates, no extra 'qqqq' block. Annotate the first four "
            "chips together as 'alpha = 4 repeats of the original query'. The row "
            "is fed by an arrow carrying b1,b2 from the left column and an arrow "
            "carrying c1,c2 from the right column. Below the chip row, show the "
            "assembled string as text: 'q_CSQE = q q q q + c1 + c2 + b1 + b2'. "
            "PANEL 4 titled 'Stage 4: Re-Retrieval': box 'BM25 (second pass, full "
            "corpus)' with the same database cylinder underneath -> final box "
            "'Final Ranked List: Top-100 Passages' annotated 'NDCG@10 = 0.616 "
            "(BM25 alone: 0.462)'. "
            + STYLE_RULES
        ),
    },
    {
        "id": "v5b",
        "aspect": "4:3",
        "intent": (
            "A vertical, four-stage pipeline flowchart for a thesis methodology "
            "section, read top to bottom, laid out as four horizontal bands "
            "separated by thin rules, each band titled on its left edge. "
            "BAND 1 'Stage 1: First-Pass Retrieval': 'User Query q' -> 'BM25 (first "
            "pass)' -> 'Top-5 Passages D1-D5'. A database cylinder labelled 'MIRACL "
            "Arabic Corpus, 2.06M passages' sits beside BM25 and feeds it. "
            "BAND 2 'Stage 2: Parallel LLM Generation': the flow forks into a LEFT "
            "column and a RIGHT column. "
            "LEFT column, blind branch: only the query q feeds it -- draw a long "
            "vertical arrow labelled 'q only' coming down the far left from the "
            "'User Query q' box, skipping past BM25 and past the passages box, into "
            "'Aya Expanse 8B - Blind: generate from parametric knowledge' -> "
            "'b1, b2 (blind pseudo-documents)'. "
            "RIGHT column, corpus-grounded branch: fed by BOTH 'q' and the 'Top-5 "
            "Passages D1-D5' box, into 'Aya Expanse 8B - Corpus-Grounded: extract "
            "key sentences from D1-D5' -> 'c1, c2 (grounded pseudo-documents)'. "
            "Mark the fork point with a small label 'same model, both branches run "
            "in parallel, temperature 1.0'. "
            "BAND 3 'Stage 3: Query Assembly': the two columns merge into one "
            "'Concatenate (string join)' box that also receives four small chips "
            "'q q q q' labelled 'alpha = 4 repeats, counters BM25 term dilution'. "
            "Output: 'q_CSQE = q q q q + c1 + c2 + b1 + b2'. "
            "BAND 4 'Stage 4: Re-Retrieval': 'BM25 (second pass over the full "
            "corpus)' -> 'Final Top-100 Ranked Passages, NDCG@10 = 0.616'. "
            + STYLE_RULES
        ),
    },
    {
        "id": "v5c",
        "aspect": "16:9",
        "intent": (
            "A fork-and-merge pipeline figure that makes the two expansion sources "
            "the visual centrepiece, read left to right in four labelled stages. "
            "On the far left a single node 'User Query q'. From it, TWO clearly "
            "separated paths leave. "
            "LOWER PATH (corpus-grounded, drawn in the retrieval colour): "
            "q -> 'BM25 first pass (k1 = 5)' -> '5 Wikipedia passages D1-D5' -> "
            "'Aya Expanse 8B: extract key sentences' -> 'c1, c2'. Annotate this "
            "path 'vocabulary attested in the corpus'. "
            "UPPER PATH (blind, drawn in a different colour): q goes DIRECTLY to "
            "'Aya Expanse 8B: generate a passage' -> 'b1, b2'. This path must "
            "visibly touch nothing else -- it must not pass through, or receive any "
            "arrow from, BM25 or the passages box. Annotate it 'parametric "
            "knowledge, no corpus context'. "
            "The two paths then MERGE into a central assembly node drawn as a wide "
            "banner: 'Concatenate: q_CSQE = q q q q + c1 + c2 + b1 + b2', with the "
            "four leading 'q' copies drawn as four small identical chips and "
            "labelled 'alpha = 4'. Make clear by the label 'string concatenation, "
            "no scoring' that this node only joins text. "
            "From the banner, one arrow goes to 'BM25 second pass over the full "
            "2.06M-passage corpus' and then to the final node 'Top-100 ranked "
            "passages -- NDCG@10 = 0.616'. "
            "Place small stage tags 'Stage 1', 'Stage 2', 'Stage 3', 'Stage 4' "
            "above the corresponding regions. "
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

    dst = OUT_DIR / f"fig_3_8_csqe_aigen_{vid}.png"
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
