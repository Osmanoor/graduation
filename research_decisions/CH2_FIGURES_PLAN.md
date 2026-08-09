# Chapter 2 Figures — Plan

> **⚠️ SUPERSEDED IN PART, 2026-08-09.** Elhaj reviewed this plan and made two changes:
> the **Transformer figure (§3, proposed Fig 2.1) is dropped** — §2.1.1 stays text-only — and
> the **RAG figure is to be rebuilt using PaperBanana**. The approved set and the full
> per-figure design are in **`CH2_FIGURES_SPEC.md`**, which is the document to build from.
> This file remains the record of *why* (the approach decision in §2 and the risks in §6 still
> stand).

**Created:** 2026-08-09
**Trigger:** Dr. Tahani's August voice notes, recording 5:
> "chapter 2 ده مفترض يكون فيه الـ theoretical background والـ literature review وكده، يكون فيه صور
> يعني. ما شايفة ولا صورة ولا أي حاجة! ... دايماً الـ figures بتشرح الجزء الصعب فهمه أكتر ... ممكن من الـ
> literature طبعاً ما بترسموها من أول وجديد. فحاولوا إذا ممكن في chapter 2 تعملوا insertion لبعض
> الصور وتضيفوها هناك في الـ list of figures فوق."

Three instructions in that: (1) add figures to Chapter 2, (2) they must explain the *hard*
parts, (3) taking the idea from published literature is expected — we are not required to
invent every diagram.

---

## 1. Current state — she is right

| Chapter | Pages | Figures |
|---|---|---|
| 1 | 1–5 | 0 |
| **2** | **6–30** | **1** (Fig 2.1, RAG architecture) |
| 3 | 31–56 | 7 |
| 4 | 57–87 | 11 |
| 5 | 88–97 | 0 |

Chapter 2 is 25 pages with one diagram. Chapters 3 and 4 — the two she called "perfect" —
average one figure every 3 pages.

**Two Chapter 2 figures already exist and were deleted by us.** On 2026-06-01 (commit
`7c11c7a`) four system diagrams were archived to `thesis_figures/archive/system_diagrams_dropped/`
on Osman's review note: *"the diagrams are actually a lot and clear concepts should not have
diagrams."* Two of the four were Chapter 2 figures:

- `fig_2_2_qe_taxonomy` — archived because it "overlaps with Table 2.1"
- `fig_2_3_dense_vs_sparse` — archived as a "standard IR primer"

Dr. Tahani has now overruled that principle for Chapter 2. Both sources and PDFs are intact
and restorable.

---

## 2. Approach decision — build them in TikZ

Three options were considered.

| Option | Verdict |
|---|---|
| **TikZ, in-house** | **Chosen.** |
| Web images / screenshots from papers | Supporting role only |
| AI image generation (Gemini / "nano banana") | Rejected |

**Why TikZ.** The thesis already carries seven TikZ system diagrams built on a shared palette
(`thesis_figures/system_diagrams/_style.tex`): defined stroke/fill pairs per role, FontAwesome
icons, `Stealth` arrowheads, 2 pt rounded corners, grayscale-safe. Anything sourced elsewhere
will read as foreign next to Figures 3.1–3.9 and an examiner leafing through will see it
immediately. TikZ also gives vector PDF at any zoom, picks up the body font automatically, and
costs nothing in licensing. The toolchain is verified working on this machine (MiKTeX xelatex).

**Why not raster/AI images.** Image models cannot render legible technical labels and produce
garbled text in Latin script and worse in Arabic — unusable for a labelled diagram, and Figure
2.6 below is built entirely around Arabic word forms. Not a viable path for any figure here.

**Where web search does help.** For the Transformer figure and the NDCG figure, look at how
two or three published papers present the same idea, then draw our own version and caption it
`Adapted from [ref]`. That is the normal academic route and is exactly what she sanctioned.
Reproducing a copyrighted figure bitmap-for-bitmap is the thing to avoid — a redrawn,
attributed version has no such problem.

**Feasibility already proven (2026-08-09):** Arabic text inside a standalone TikZ diagram
compiles and renders correctly RTL, with diacritics, using
`polyglossia` + `\newfontfamily\arabicfont[Script=Arabic,Scale=1.2]{Arial}` and `\textarabic{}`
inside nodes. This was the only real technical risk in the set and it is closed. Probe kept at
`scratchpad/artest/`.

---

## 3. Proposed figure set

Six new figures, taking Chapter 2 from 1 to 7. Existing Fig 2.1 shifts to 2.2 — no `\ref`
breaks, because every figure reference in the thesis already goes through `\ref{}` (verified:
zero hardcoded "Figure 2.x" strings anywhere in `Chapters/`).

| New # | § | Figure | Origin | Tier |
|---|---|---|---|---|
| 2.1 | 2.1.1 | Encoder-only vs decoder-only Transformer | new, adapted from Vaswani | 1 |
| 2.2 | 2.1.2 | RAG architecture | **exists** | — |
| 2.3 | 2.1.3 | Sparse vs dense retrieval | **restore** from archive + fix | 2 |
| 2.4 | 2.1.4 | Where the QE layer sits in a RAG pipeline | new | 2 |
| 2.5 | 2.1.4 | QE taxonomy — four families | **redesign** of archived | 2 |
| 2.6 | 2.1.5 | Arabic retrieval challenges | new | **1** |
| 2.7 | 2.2.4 | NDCG@10 worked example | new | 1 |

Optional eighth, if Chapter 2 can afford the page: a QE research timeline for §2.5 (see §5).

Page cost estimate: each diagram is roughly a third of a page plus caption, so ≈ 2.5 pages
added to Chapter 2. Nothing in Chapters 3–5 moves except pagination.

---

### Fig 2.1 — Encoder-only vs decoder-only Transformer (§2.1.1)

**The hard part it explains.** §2.1.1 currently states the attention equation, then names
encoder-only and decoder-only paradigms in two sentences, then moves on. An examiner outside
NLP has no picture of either, and — more importantly — no picture of *why the thesis needs
both*.

**Content.** Two columns. Left: encoder-only, bidirectional attention over the whole sequence,
output = one contextual vector → labelled **used by mDPR in this thesis**. Right: decoder-only,
causal masked attention, autoregressive next-token generation → labelled **used by the ten QE
generators in this thesis**. A shared block beneath both showing scaled dot-product attention,
carrying Equation 2.1 so the figure and the maths are visibly the same object.

**Why this and not a full Transformer block diagram.** Redrawing Vaswani's figure would be a
textbook copy that teaches nothing specific to this work. Tying the two families to the two
model roles the thesis actually uses makes it *our* figure.

**Caption:** `Adapted from Vaswani et al. \cite{vaswani_2017_attention}.`

---

### Fig 2.3 — Sparse vs dense retrieval (§2.1.3) — restore

Archived source: `archive/system_diagrams_dropped/fig_2_3_dense_vs_sparse.tex`. Two parallel
lanes, BM25 (tokenise → stem → TF scoring → inverted index) against mDPR (encode → 768-d
vector → inner product → FAISS), both ending at top-*k*.

**Two defects to fix before it goes back in:**
1. The italic annotation *"complementary strengths: BM25 high recall, mDPR high precision"*
   is placed between the lanes and **collides with the box borders**. Move it to the caption.
2. Verify "768-d" against `chapter3.tex` §3.4 before restoring.

Cheapest figure in the set — the layout is already done.

---

### Fig 2.4 — Where the QE layer sits (§2.1.4)

Requested independently by Osman (`thesis_figures/FIGURE_NOTES_MOHAMMED.md` §1): Fig 2.2 shows
the generic query → retriever → LLM → answer flow, and we need one that marks the QE layer's
position explicitly.

**Content.** The same pipeline as Fig 2.2, with a highlighted QE block inserted between the
user query and the retriever (`thHi` style — the palette's "our contribution" colour), showing
`q → q'` and a callout that nothing downstream changes: same index, same retriever, same
generator. That last point *is* the modularity argument §2.1.4 makes in prose and is worth
seeing.

---

### Fig 2.5 — QE taxonomy (§2.1.4) — redesign

**Not a straight restore.** The archived version splits QE into *lexical/statistical* vs
*LLM-based generative*, but §2.1.4 was since rewritten around Song and Zheng's four atomic
operations — expansion, decomposition, disambiguation, abstraction. The old figure no longer
matches the text it would sit beside.

**New structure.** Root *Query Enhancement* → four family branches matching the four
`\subsubsection`s. Expansion alone expands further into lexical (PRF, RM3) and LLM-based
(HyDE, Query2Doc, GRF, CSQE). Query2Doc and CSQE highlighted as the two the thesis builds on.

**Osman's edit, carried forward:** delete the in-image *"built on in this thesis"* annotation
and put it in the caption instead.

**Relationship to Table 2.1.** The original archiving reason was overlap with Table 2.1. It
does not hold: Table 2.1 is a flat list of reviewed papers with datasets and headline results;
the figure shows the *structure* of the field and where our two techniques sit inside it.
Different jobs.

---

### Fig 2.6 — Arabic retrieval challenges (§2.1.5) — **highest value in the set**

This is the figure to get right. It is the one that is genuinely ours, it explains the hardest
and most thesis-specific material in the chapter, and it is the visual form of the problem
statement.

**Content — four panels, real examples, then one shared consequence.**

| Panel | Example | Already in the thesis? |
|---|---|---|
| Morphological richness | root ك-ت-ب → كِتاب / كاتب / مكتبة / مكتوب | §2.1.5 prose |
| Orthographic variation | إبن الهيثم vs ابن الهيثم | **chapter4.tex §4.2.4** |
| Diacritic sensitivity | المَثَانة vs المثانة | **chapter4.tex §4.2.4** |
| Diglossia | dialectal query vs MSA passage | §2.1.5 prose |

All four converge on one bar: *one concept, many surface forms → BM25 scores them as different
terms → relevant passage missed* → and an arrow out to QE as the query-side remedy.

**Deliberate design choice:** use the *same* Arabic examples that Chapter 4's error analysis
found empirically. Chapter 2 then predicts exactly what Chapter 4 measures, and the examiner
sees the thesis close its own loop. Those examples are already cited at `chapter4.tex:144`.

**Technical note:** needs `polyglossia` + `\arabicfont` in the standalone preamble. Verified
working — see §2.

---

### Fig 2.7 — NDCG@10 worked example (§2.2.4)

**The hard part it explains.** NDCG@10 is the headline number of the entire thesis — every
table, every figure, the abstract, the title's justification. §2.2.4 defines it with two
equations and no intuition. An examiner is more likely to ask about this than about anything
else in Chapter 2.

**Content.** A ten-slot ranked list with relevance grades marked; the `1/log₂(i+1)` discount
plotted or printed alongside each rank so the positional penalty is visible; the same documents
re-sorted into the ideal ranking (IDCG); and the division producing a concrete NDCG@10 value.
One made-up query, small integers, arithmetic that a reader can follow by eye.

**Cross-check before drawing:** the worked value must be internally consistent with
Equations 2.7 and 2.8 as printed. Compute it in a script, not by hand.

---

## 4. Build order

1. **Fig 2.3** — restore from archive, fix the overlapping label, recompile. Fastest win,
   re-validates the whole build path end to end.
2. **Fig 2.6** — Arabic challenges. Highest value, highest effort, and the Arabic-in-TikZ
   pattern it establishes is reused nowhere else, so any surprises surface early.
3. **Fig 2.5** — QE taxonomy redesign, then **Fig 2.4** — QE layer placement. Same section,
   build together so they read as a pair and do not repeat each other.
4. **Fig 2.1** — Transformer. Gather two or three published reference renderings first.
5. **Fig 2.7** — NDCG worked example. Compute the numbers in a script before drawing.
6. Insert all six into `chapter2.tex` with captions and labels, rebuild, check the List of
   Figures, check no float lands badly.

Per-figure loop: write `thesis_figures/system_diagrams/fig_2_N_*.tex` → `xelatex` →
copy PDF to `output/pdf/` → render PNG and inspect → insert into `chapter2.tex`.

---

## 5. Open — one call needed

**The research-timeline figure for §2.5 (Related Work).** A horizontal timeline
2022 → 2025 (HyDE '22 · Query2Doc '23, GRF '23 · CSQE '24, RQ-RAG '24 · MuGI, Exp4Fuse '25)
against a near-empty *Arabic IR* lane, with this thesis placed at the intersection.

For: it renders the §2.5.4 research-gap argument as a picture, which is the single argument
Chapter 2 exists to make, and literature-review chapters conventionally carry one.

Against: it is the only proposed figure that does not explain a *difficult concept* — her
stated criterion — and §2.5.4 already makes the argument in prose. It is also the figure most
exposed to the open literature-verification item in Phase A review flag 5 (the "no monolingual
Arabic LLM-QE evaluation" claim was only ever searched at sub-7B scope). Drawing an empty
Arabic lane commits us visually to a gap claim that is still pending re-verification.

**Recommendation: defer.** Build the six first. Revisit only if Chapter 2 still looks thin,
and only after the Phase A flag-5 literature re-check clears.

---

## 6. Risks

- **Float placement.** Chapter 2 is dense with equations and two wide tables. Six new floats
  can push text apart badly. Existing figures use `[H]` (hard placement, `float` package) —
  keep that, and check the rendered pages rather than trusting the log.
- **Page count.** ≈ +2.5 pages on a 135-page document. No constraint is known to be near a
  limit, but the ¾-page abstract rule (voice note 8) is unaffected either way.
- **Arial dependency.** `\arabicfont` resolves to Arial, which this machine has and Overleaf
  does not. Already a known thesis-wide issue (task J3b): Overleaf substitutes a wider font and
  the Arabic abstract reflows to two pages. Figure 2.6 makes one more page depend on which
  machine builds the deliverable. **Decide the build machine before submission.**
- **Naming.** `thesis_figures/system_diagrams/README.md` still lists `fig_2_2_qe_taxonomy` and
  `fig_2_3_dense_vs_sparse` at their *old* numbers. Under this plan the taxonomy becomes 2.5
  and dense-vs-sparse stays 2.3. Rename files to match the printed numbers, or the same
  legacy-filename confusion that hit Figures 4.5/4.6 (task H1b) repeats here.
