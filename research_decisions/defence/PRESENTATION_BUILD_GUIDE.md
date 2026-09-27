# Defence presentation — build guide and handover

**What this is.** A complete description of how the 22-slide defence deck, its speaker notes,
and the PowerPoint/PDF deliverables were produced, so a future session can edit, re-render or
extend any part of it without re-deriving the setup.

**Written:** 2026-09-27. **Deck status:** complete and delivered.

---

## 1. What exists

Everything lives under `research_decisions/defence/`.

### Deliverables — the files you actually present from

| File | What it is |
|---|---|
| `slides/Defence_Presentation.pdf` | 22 pages, 3840×2160 per page. **Present from this** — nothing can shift or fail to render. |
| `slides/Defence_Presentation.pptx` | Same 22 slides as full-bleed images, **with speaker notes attached to every slide**. Use Presenter View. |
| `slides/Defence_Speaker_Notes.pdf` / `.html` | The script as a standalone RTL document, one card per slide. |
| `F12_SCRIPT_TO_READ.md` | The clean script — just what you say, no build notes. Generated from F11. |

### The script (content)

| File | Role |
|---|---|
| **`F11_final_script.md`** | **Single source of truth for the spoken script.** All cuts applied. Mohammed 5:03, Osman 4:32, total 9:35. Everything downstream is generated from this file. |
| `F7_intro_content_final.md` | Design document for slides 1–14 (Mohammed). Rationale, visual specs, timing analysis. Superseded as *script* by F11; still the reference for *why* each slide is shaped as it is. |
| `F8_osman_content.md` | Same, for slides 15–22 (Osman). |
| `F12_SCRIPT_TO_READ.md` | Generated output. Do not hand-edit — regenerate from F11. |

### Slide images

| Folder | Contents |
|---|---|
| `slides/final_v3/` | **The current deck.** 22 PNGs at 5504×3072, with logo, watermark and page numbers composited. Gitignored (≈334 MB). |
| `slides/raw_v3/` | The same 22 slides straight from the image model, before compositing. Gitignored. |
| `slides/deck_images/` | 1920×1080 JPEGs, ~4.6 MB total. **Tracked in git** as the portable preview set. |
| `slides/backup_v2/`, `slides/raw/`, `slides/final/`, `slides/v2/` | Earlier iterations. Kept for reference, gitignored. |

> **Why the big folders are gitignored.** The composited PNGs are ~15 MB each. Committing them
> was attempted and the push failed with HTTP 408. Only `deck_images/` plus the PPTX and PDF are
> tracked. Everything else is regenerable from the prompts and scripts, which *are* tracked.

---

## 2. How a slide is made

Three stages. Each is a separate script, so you can redo one without redoing the others.

```
prompts_CURRENT.txt  ──gen_all_v3.ps1──▶  raw_v3/*.png
                            (Gemini)
raw_v3/*.png ──composite_v3.ps1──▶ final_v3/*.png
             (logo · watermark · page numbers · thesis figures)
final_v3/*.png + F11_final_script.md ──build_deck.py──▶ PPTX + PDF
```

### Stage 1 — generate the artwork

**Model: `gemini-3-pro-image`** via the Gemini REST API. Output is 5504×3072 (16:9).

- `slides/gen_all_v3.ps1` — batch driver. Reads `style.txt` + one block of `prompts_CURRENT.txt`,
  calls the API, writes to `raw_v3/`.
- `slides/gen_gemini.ps1` — single-image version, takes `-StylePath -PromptPath -OutPath -Aspect -Resolution`.
- `slides/gen_slide.ps1` — the OpenAI equivalent (`gpt-image-2`), kept because it was used for the
  first pass. Max edge 3840; both dimensions must be divisible by 16, so true 16:9 is `3840x2160`.

Every prompt is prefixed with **`slides/style.txt`** (also copied as `STYLE_PREAMBLE.txt`) — the
shared design system that makes 22 separately generated images read as one deck: near-white ground,
emerald→teal→blue gradients, corner blobs, dot grids, white cards, gradient number badges, ochre
reserved for things that are wrong.

**Run it:**
```powershell
$env:GEMINI_API_KEY="..."      # never commit this
.\gen_all_v3.ps1 -Only "slide_07_arabic,slide_12_query2doc"
# omit -Only to regenerate all 22
```

### Stage 2 — composite

`slides/composite_v3.ps1` reads `raw_v3/`, writes `final_v3/`. It never modifies the raw files.

It does four things:
1. **UofK crest** onto slide 1, into the blank square the prompt reserves for it.
2. **Faint watermark** (22% opacity) top-right on every slide *except* slide 1, which already has
   the full-strength crest.
3. **Page number pill** bottom-right, `n / 22`, white pill with teal text so it reads on both the
   pale ground and the gradient wave. Skipped on slide 22.
4. **Real thesis figures** dropped into panels the prompts leave deliberately blank.

The figure map is a hashtable at the top of the script — coordinates are fractions of the slide:

| Slide | Figure | Panel (L, T, R, B) |
|---|---|---|
| 06 literature | `fig_2_3_qe_taxonomy` | 0.055, 0.375, 0.580, 0.865 |
| 12 query2doc | `fig_3_5_query2doc` | 0.055, 0.280, 0.460, 0.890 |
| 13 dense vs bm25 | `fig_4_5_models_bar_v1` | 0.055, 0.360, 0.480, 0.925 |
| 13 dense vs bm25 | `fig_4_5b_models_bar_bm25_v1` | 0.525, 0.360, 0.950, 0.925 |
| 14 repetition | `fig_4_7_repetition_v1` | 0.375, 0.360, 0.950, 0.925 |
| 16 csqe | `fig_3_8_csqe_aigen_v5a` | 0.060, 0.270, 0.940, 0.885 |
| 17 placement | `fig_3_9_best_system_aigen_v2a` | 0.545, 0.275, 0.950, 0.815 |
| 18 journey | `fig_4_11_progression_v2_annot` | 0.345, 0.330, 0.950, 0.925 |

Sources are `thesis_figures/output/png/`.

> **`fig_4_5b_models_bar_bm25_v1` was created for this deck.** Chapter 4 reports the BM25 model
> sweep as Table 4.6 only — there was no figure. `thesis_figures/gen_fig_bm25_bar.py` builds it from
> `model_comparison_bm25.csv` (column `n1_ndcg10`, i.e. *before* the repetition fix) in the same
> style as the dense chart, so the two sit side by side on slide 13. Asserts 3 above / 6 below the
> baseline, matching Table 4.6.

### Stage 3 — assemble

`slides/build_deck.py` (Python; needs `python-pptx` and `pillow`).

- Resizes `final_v3/` masters to **3840×2160, JPEG q95, no chroma subsampling**. At a 13.333-inch
  slide that is ~288 DPI, so PowerPoint renders 1:1 on a 4K display. An earlier 2560px build looked
  soft because PowerPoint was upscaling it.
- Also writes the 1920×1080 `deck_images/` preview set.
- Parses `F11_final_script.md` and attaches speaker notes per slide.
- Writes the PPTX and the PDF.

`build_pptx_notes.py` (scratchpad only, logic now folded into `build_deck.py`) was the PPTX-only
variant used to fix the notes.

---

## 3. Speaker notes — how they are parsed

`F11_final_script.md` uses a strict shape that the parsers depend on:

```markdown
## Slide 7 · But Arabic is not English — 10s

> والعربي عندو تحدياتو الخاصة: الاشتقاق، والإملاء، والتشكيل، والازدواجية اللغوية.

> Name the four and stop. Do not read the examples aloud.
```

- `## Slide N · Title — Xs` starts a slide. **Keep this format** or the parsers skip it.
- A run of consecutive `>` lines is **one paragraph**. A blank line ends it.
- A paragraph **containing any Arabic** is treated as **script**; a pure-Latin paragraph is
  **delivery guidance** and goes under a `— DELIVERY —` heading in the notes pane.
- `*[...]*` lines are stage directions.

> **Two parser bugs were fixed; do not reintroduce them.**
> 1. Markdown must be stripped **after** joining a paragraph's wrapped lines, not before —
>    `**bold**` spans in F11 routinely straddle a line break, and per-line stripping left orphaned
>    `**` in the output.
> 2. Script detection uses *"contains any Arabic"*, not *"Arabic-dominant"*. Slide 21's script is so
>    heavy with English terms (dialectal Arabic / first-pass quality gate / embedding models) that a
>    dominance test filed it as English guidance.

### Right-to-left in PowerPoint

Notes were initially written as one string with newlines. PowerPoint applies **one direction per
paragraph**, so Arabic sentences containing English terms came out with the runs visually reordered.

The fix, in `build_deck.py`: every line is its own paragraph, and each carries an explicit
`a:pPr rtl="1"` + `algn="r"` (Arabic) or `rtl="0"` + `algn="l"` (Latin). The complex-script
typeface (`a:cs`) is set alongside the Latin one so Arabic shapes in the same family.

**If you touch the notes code, verify with:**
```python
# every paragraph's rtl attribute must match whether it contains Arabic
```
The check script used during the build is reproduced in §6.

---

## 4. Known traps

These all bit during the build. They are prompt-level, not code-level, so they will come back if a
prompt is rewritten carelessly.

**The style file leaks into the slides as text.** Seven slides once rendered headers reading
"HEAVYBOLD UPPERCASE" or "UNIVERSITY THESIS DEFENCE" — phrases from the design brief. `style.txt`
now ends with an explicit *INSTRUCTION LEAK — ABSOLUTELY FORBIDDEN* block naming the words that must
never appear. Keep it.

**The model renders Q as O.** Slides 5 and 17 came out as "RETRIEVAL OUALITY" and "EXPANDED OUERY".
Both prompts now carry a `SPELLING GUARD` line. Any slide whose headline contains a capital Q needs
one.

**The model adds its own page number.** Slide 7 drew an "07" that collided with the composited pill.
Prompts for 06, 12, 14, 17, and the restored 03, 04, 07 carry a `PAGE NUMBER RULE` line. Add it to
any slide you regenerate.

**Never let the model draw a chart.** It invents plausible bar heights. Prompts reserve a
*completely empty blank white* panel and `composite_v3.ps1` drops the real figure in.

**Arabic renders correctly** — this was tested and it works, on both `gemini-3-pro-image` and
`gpt-image-2`. Earlier caution in `F9_theme.md` about overlaying Arabic afterwards is obsolete.

**Check headers after any batch.** The fastest way to catch leaks is a contact sheet of the top 20%
of all 22 slides in one image — see §6.

---

## 5. Editing recipes

### Change what is said on a slide
Edit `F11_final_script.md`, then:
```powershell
python slides\build_deck.py          # rebuilds PPTX + PDF + notes
```
Then regenerate `F12_SCRIPT_TO_READ.md` and `Defence_Speaker_Notes.*` (§6).

### Change what a slide looks like
Edit the matching block in `slides/prompts_CURRENT.txt`, then:
```powershell
$env:GEMINI_API_KEY="..."
.\slides\gen_all_v3.ps1 -Only "slide_12_query2doc"
.\slides\composite_v3.ps1
python slides\build_deck.py
```

### Swap or move a thesis figure
Edit the `$figs` hashtable in `composite_v3.ps1`, rerun it, rebuild. No regeneration needed.
Panel coordinates are fractions; match the figure's aspect ratio or it will letterbox.

### Add a slide
1. Add a block to `prompts_CURRENT.txt`.
2. Add the stem to the `$order` array in `composite_v3.ps1` **and** the `ORDER` list in
   `build_deck.py` — both must match, in the same order.
3. Add a `## Slide N · ...` section to `F11_final_script.md`.
4. Page numbers renumber automatically from the array length.

---

## 6. Regenerating the auxiliary documents

**`F12_SCRIPT_TO_READ.md`** — clean script, Arabic headings, cues italicised, Q&A points at the end.
Generated by a script that parses F11 the same way `build_deck.py` does. If it is lost, the
generator is short enough to rewrite: split on `## Slide N ·`, take `>` blocks, classify by presence
of Arabic, emit per-slide sections.

**`Defence_Speaker_Notes.html` / `.pdf`** — RTL standalone document. Built by
`build_script_doc.py` (scratchpad), then printed:
```powershell
chrome --headless --disable-gpu --no-pdf-header-footer `
  --print-to-pdf="Defence_Speaker_Notes.pdf" "file:///.../Defence_Speaker_Notes.html"
```

**Header contact sheet** — crop the top 20% of each of the 22 finals, tile 2-up with filename
labels, view as one image. This caught the style-leak on seven slides and the Q→O typo on two.
A bottom-strip version catches model-drawn page numbers.

---

## 7. Content constraints that shaped the deck

Set by the supervisor's voice notes (`meetings/2026-07_supervisor_voice_notes_transcripts.md`,
Part II, notes 9–12 and 16) and by the review in `F6_deck_review.md`:

- **Agenda slide is mandatory** as slide 2.
- **Theory capped at one slide.** Over-explaining theory is how teams run out of time before the
  results. All of Chapter 2 lives in Q&A.
- **Problem definition gets the largest block** — she named it explicitly.
- **Defence is live on Google Meet; mixed Arabic/English is accepted.**
- Panel may ask *"open slide 15"* or *"explain this figure"* — hence page numbers on every slide.

### Claims that were corrected and must not regress

| Claim | Correct form |
|---|---|
| The number **143** | Queries where **blind scored 0.000 and CSQE recovered to 1.000** (ch4:787). It is a CSQE win count, **not** a count of queries blind expansion broke. |
| First single-model experiment | Qwen 2.5 3B was dense **+8.9%** but BM25 **−11.5%** (Tables 4.3, 4.4). It did **not** improve both. |
| Novelty | Narrow claim only — asymmetric assignment across retriever *types* in a dense–sparse hybrid, for Arabic. `chapter2.tex:410` cites **Exp4Fuse** as closest prior art. |
| Why dense degrades | Complementarity collapse (Ch5 conclusion ix). The "mDPR is out-of-distribution on long queries" explanation was never tested — do not use it. |
| Short-query gain | **+43.6% proportional.** In absolute terms 4–8 word queries gained more (+0.197 vs +0.161). Say *proportional*. |
| 0.7137 vs 0.6936 | 0.7137 is corpus-level pooled; 0.6936 is the per-query mean of the same system. Never mix them. |

---

## 8. File inventory

```
research_decisions/defence/
├── PRESENTATION_BUILD_GUIDE.md      ← this file
├── F11_final_script.md              ← SOURCE OF TRUTH for the script
├── F12_SCRIPT_TO_READ.md            ← generated clean script
├── F7_intro_content_final.md        ← design doc, slides 1–14
├── F8_osman_content.md              ← design doc, slides 15–22
├── F6_deck_review.md                ← factual review; the corrections in §7 came from here
├── F9_theme.md                      ← palette rationale (Arabic-overlay advice is obsolete)
├── F10_time_cuts.md                 ← the cut analysis; all approved cuts are already in F11
├── F1–F5, speaker_notes*.html       ← superseded drafts, kept for history
└── slides/
    ├── prompts_CURRENT.txt          ← ONE BLOCK PER SLIDE, latest revision. Start here.
    ├── prompts_all.txt / _v3 / _v4 / _v4b_restored   ← revision history, superseded
    ├── style.txt  (= STYLE_PREAMBLE.txt)             ← shared design system
    ├── gen_all_v3.ps1 · gen_gemini.ps1 · gen_slide.ps1
    ├── composite_v3.ps1 · composite.ps1
    ├── build_deck.py
    ├── final_v3/ · raw_v3/          ← 22 each, gitignored
    ├── deck_images/                 ← 22 JPEGs, tracked
    └── Defence_Presentation.pptx / .pdf · Defence_Speaker_Notes.html / .pdf
```

> **`prompts_CURRENT.txt` is new and matters.** The prompts had drifted across three files by
> revision, and the final prompts for slides **03, 04 and 07** existed only in a temp directory that
> is now gone — regenerating from the old files would have silently reverted the unblurred
> hallucination on slide 3, the large RAG badge on slide 4, and the page-number guard on slide 7.
> Those three were reconstructed into `prompts_v4b_restored.txt` and merged. **Use
> `prompts_CURRENT.txt`; treat the numbered prompt files as history.**

---

## 9. Credentials

The OpenAI and Gemini API keys were pasted into chat during the build and **should be treated as
compromised**. Rotate them, then keep them in a gitignored `.env` or an environment variable.
No key is stored in any tracked file; every script reads from the environment.
