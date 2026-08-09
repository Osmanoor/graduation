# AI-generated figures

**One figure in this thesis was produced with an image-generation model rather than TikZ.**
This directory holds everything needed to reproduce or re-audit it.

## Fig 2.1 — RAG pipeline

| | |
|---|---|
| Output | `../output/png/fig_2_1_rag_pipeline.png` (2752×1536 PNG, ≈437 dpi at text width) |
| Tool | [PaperBanana](https://github.com/llmsresearch/paperbanana) v0.1.2 |
| VLM (planner/critic) | `gemini-flash-latest` |
| Image model | `gemini-3-pro-image-preview` |
| Current version | **v2**, generated 2026-08-09, accepted at iteration 1 of 3 |
| Prompt | `fig_2_1_rag_pipeline_prompt.txt` |
| Spec | `research_decisions/CH2_FIGURES_SPEC.md`, Fig 2.1 |

Reproduce with:

```bash
GOOGLE_API_KEY=... paperbanana generate \
  -i fig_2_1_rag_pipeline_prompt.txt \
  -c "The three stages of a Retrieval-Augmented Generation system, showing a retrieved chunk being injected into the prompt sent to the language model." \
  --vlm-model gemini-flash-latest --image-model gemini-3-pro-image-preview -n 3
```

## Version history

**v1** (`fig_2_1_v1_typo_rejected.png`) — three stages with a plain three-line worked-example
strip at the bottom. Superseded on Elhaj's review: *"illustrate that there is a chunk injected
in the worked example … I just want to illustrate the worked example and the chunk a bit
better."* Kept because it also documents the text-error failure mode: **its first iteration
printed "What was the University of Khartoum founded?"** PaperBanana's own critic caught it.

**v2** (current) — the chunk is now traceable end to end. `Split into chunks` visibly emits
chunk cards; the retriever returns a stack of `Chunk 1/2/3` with Chunk 2 highlighted and tagged
`most relevant`; and Stage 3 is dominated by a `Prompt sent to the LLM` box built from three
labelled slots — `instruction`, `INJECTED CHUNK` (same green as Chunk 2, holding the actual
chunk text), and `question`. Accepted at iteration 1; the critic reported no issues.

## Why this one and not TikZ

Requested by Elhaj. Every other figure in the thesis is TikZ vector; this is the single
exception. It passed a five-point accept gate defined in the spec: all English labels spelled
correctly, ≥300 dpi at printed width, the three stages visually distinguishable, no Arabic
involved (deliberately — the figure is a general RAG explanation), and a palette close enough
to `system_diagrams/_style.tex` to sit beside Figures 2.2–2.5.

Legibility was verified by cropping the rendered thesis page at 300 dpi, not by eyeballing a
screen preview: the quoted chunk text sets at roughly 8–9 pt in print, which is normal for
figure text.

## ⚠️ Three things to know

1. **It is raster, not vector.** It cannot be edited — only regenerated, and a regeneration will
   not reproduce the same image. Every other thesis figure is an editable `.tex`.

2. **Never ship a generated figure without reading every word in it.** See the v1 typo above.
   Image models fail on text specifically, and a raster typo cannot be patched.

3. **Generation time is wildly variable.** The v1 run took ~30 s per image; the v2 run took
   **46 minutes** for a single image on the same account, presumably queueing or throttling. Do
   not assume a regeneration is quick, and do not schedule one close to a deadline.

## Facts asserted in the figure

The worked example states the University of Khartoum was founded in 1902 as Gordon Memorial
College and became the University of Khartoum in 1956. Verified 2026-08-09: Gordon Memorial
College was founded in 1902; it merged with the Kitchener School of Medicine in 1951 as
University College Khartoum and officially became the University of Khartoum on 24 July 1956.

## Deliberate correctness constraint

The index is drawn generically as **"Index (sparse, dense, or hybrid)"**, not as a vector
database, and retrieval is not described as semantic similarity only. The canonical RAG figure
in the literature hardwires dense retrieval; RAG does not require it, and §2.1.3 of this thesis
gives BM25 equal billing. **Preserve this if the figure is ever regenerated** — it is stated
explicitly in the prompt file as a critical requirement.
