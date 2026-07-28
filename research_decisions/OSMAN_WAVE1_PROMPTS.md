# Osman — Wave 1 Agent Prompts

**Created:** 2026-07-28. Prompts for Osman's Wave-1 tasks from `research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md`.
**Covered:** C1 + C8 (Prompt 1), C2 + C3 (Prompt 2), C6 (Prompt 3), C7 (Prompt 4).
**Skipped by decision (2026-07-28):** C9 dedication (write last), C10 chapter summaries (depends on other content edits — would need re-updating).

## How to use

- Run **one prompt per fresh agent/chat**, from the repo root.
- All four are **independent** — any order works. Suggested: 1 → 4 → 3 → 2 (Prompt 2 is the heaviest; Prompt 1 is a 10-minute win).
- **Run one at a time and review + commit between prompts** — each agent leaves its changes uncommitted in the working tree, so overlapping runs would mix diffs.
- ⚠️ If the Overleaf copy is ahead of this repo for any file an agent touches (especially `1-main.tex` — see the title-page note in Prompt 1), sync first.

---

## Prompt 1 — Front matter order + page-numbering check (C1 + C8)

```
You are working in the Arabic RAG thesis repo. The LaTeX source is in
`University_of_Khartoum__EEE_bachelor_s_thesis_template/` — main file `1-main.tex`,
compiled with XeLaTeX (fontspec + polyglossia, Arabic support), bibliography via
BibTeX with IEEEtran style. Keep every edit minimal and surgical: do not reformat,
rewrap, or "improve" anything outside the task. Do not commit — leave changes in
the working tree and end with a report.

TASK 1 — Front matter reorder (supervisor directive).
Dr. Tahani requires this exact front-matter order:
  1. Cover/Title Page  2. Declaration of Authorship  3. Dedication
  4. Acknowledgments  5. Abstract (English)  6. Arabic Abstract (المستخلص)
  7. Table of Contents  8. List of Figures  9. List of Tables
  10. List of Abbreviations
Current state in `1-main.tex` (lines ~114–126): items 1–6 are already correct, but
then it goes \listoftables → \listoffigures → \tableofcontents → abbreviations.
Reorder that block to: \tableofcontents → \listoffigures → \listoftables →
\include{7-ListofAbbreviations}, keeping sensible \newpage separation (each \include
already starts a new page; keep \newpage between the three lists) and keeping the
block before \pagenumbering{arabic}. Note `tocbibind` is loaded, so the lists
self-register in the ToC — don't add manual \addcontentsline for them.


TASK 2 — Page-number placement audit (verify, don't blindly change).
Observed in the PDF: page numbers appear top-right on normal pages but bottom-center
on chapter-start pages, and the front matter uses roman numerals. This is standard
LaTeX `report`-class behavior (fancyhdr for normal pages; `plain` style on \chapter
pages). Read `University_of_Khartoum__EEE_bachelor_s_thesis_template/thesis Guidelines .pdf`
and check whether the faculty specifies page-number placement. 
- If the guidelines specify a placement: make the document comply (e.g., redefine
  the `plain` page style via fancyhdr's \fancypagestyle{plain}{...} so chapter pages
  match), and say what rule you applied.
- If the guidelines are silent: change NOTHING and report that the current behavior
  is standard and acceptable.

VERIFICATION: if `xelatex` is available locally, compile from inside the template
folder (xelatex 1-main.tex; bibtex 1-main; xelatex 1-main.tex twice) and confirm no
new errors and that the front matter renders in the required order. If xelatex is
not installed, do a static check of the include order and say compilation must be
verified on Overleaf.

REPORT: list every change (file:line), every TODO left, and the guidelines verdict
on page numbering.
```

---

## Prompt 2 — Abbreviations: first-mention sweep + build the list (C2 + C3)

```
You are working in the Arabic RAG thesis repo. The LaTeX source is in
`University_of_Khartoum__EEE_bachelor_s_thesis_template/` — main file `1-main.tex`,
chapters in `Chapters/chapter1.tex` … `chapter5.tex`, English abstract
`5-Abstract.tex`, Arabic abstract `6-ARAbstract.tex`, abbreviations file
`7-ListofAbbreviations.tex`. Compiled with XeLaTeX. Keep edits minimal and
surgical. Do not commit — leave changes in the working tree and end with a report.

CONTEXT: Supervisor directive (Dr. Tahani):
- The List of Abbreviations must be filled (it is currently the template
  placeholder — "Test Example"/"Another Example") and sorted alphabetically A→Z.
- First-mention rule: the FIRST time any abbreviation appears in the main thesis
  text, write the full phrase followed by the abbreviation in parentheses —
  e.g. "Retrieval-Augmented Generation (RAG) systems…" — and every later mention
  uses the abbreviation alone.

TASK 1 — Inventory.
Sweep `5-Abstract.tex` + `Chapters/chapter1..5.tex` and build a complete inventory
of abbreviations/acronyms actually used (expect things like: RAG, IR, QE, LLM,
MSA, NLP, BM25, mDPR, DPR, CSQE, HyDE, Q2D/Query2Doc, nDCG, MRR, RRF, CC, MoE,
API, GPU, VRAM, FP16/BF16/NF4, TF-IDF, OALL, KV, OOM, SOTA, TREC, EN/AR — plus any
others you find). Rules:
- Model NAMES are not abbreviations (Qwen, Jais, Aya, SILMA, Gemma, Falcon, ALLaM,
  MIRACL is a dataset acronym — include it; judgement call: include dataset/metric
  acronyms, exclude pure product names).
- For each entry record: expansion, first-occurrence location in the main text.

TASK 2 — First-mention fixes (main text = Chapters 1–5).
For each abbreviation: at its first occurrence in Chapter 1–5 prose, ensure the
full-phrase + (ABBR) form; convert any LATER spelled-out occurrences to the bare
abbreviation ONLY where that clearly improves compliance (do not mass-rewrite
prose; leave stylistically deliberate repetitions of the full term if removing
them would harm readability — flag borderline cases in the report instead).
The English abstract is read standalone: ensure any acronym used in
`5-Abstract.tex` is also expanded there at first use, independently of the
chapters.
STRICT EXCLUSIONS — never edit: `6-ARAbstract.tex` (being rewritten separately
with its own Arabization convention); verbatim/quoted LLM prompt blocks in Ch.3
(e.g. the CSQE system prompt); table/figure content and captions (abbreviation-only
is fine there); any generated files (`Chapters/chapter2_generated.tex`, anything
under `thesis_figures/`) — if a first mention lands inside one of these, define
the term in the nearest preceding prose instead and note it.

TASK 3 — Build the List of Abbreviations.
Rewrite `7-ListofAbbreviations.tex`: remove the two placeholder entries, add every
inventoried abbreviation sorted A→Z using the template's \acro format. Follow the
template's bold-initials style (\acro{RAG}{\textbf{R}etrieval-\textbf{A}ugmented
\textbf{G}eneration}) where the letters map cleanly; use plain text where bolding
is awkward (e.g. BM25, nDCG@10, FP16). Update the [LONGEST] option to the actual
longest acronym label so the column aligns.

VERIFICATION: compile with xelatex if available (from the template folder:
xelatex 1-main.tex; bibtex 1-main; xelatex twice) — no new errors, list renders
sorted. Otherwise static-check and note Overleaf verification is needed.

REPORT: the full inventory table (abbr → expansion → first-mention location →
action taken), every edit made (file:line), and all borderline cases you chose
NOT to change.
```

---

## Prompt 3 — Citations: order-of-appearance + web access dates (C6)

```
You are working in the Arabic RAG thesis repo. The LaTeX source is in
`University_of_Khartoum__EEE_bachelor_s_thesis_template/` — main file `1-main.tex`,
chapters in `Chapters/`, bibliography `References.bib`, style
\bibliographystyle{IEEEtran} with plain BibTeX (compiled 1-main.bbl exists).
Keep edits minimal and surgical. Do not commit — leave changes in the working
tree and end with a report.

CONTEXT: Supervisor directives (Dr. Tahani):
(a) Citations must strictly follow IEEE order-of-appearance numbering
    ([1], [2], [3]… in the order they first appear in the text).
(b) Every web reference must include the full URL and an explicit access date,
    IEEE style: "[Online]. Available: https://… [Accessed: Mon. DD, YYYY]".

TASK 1 — Verify order-of-appearance (this is a VERIFICATION; expect a pass).
IEEEtran.bst is an unsorted style that lists references in citation order, so
this should already hold — prove it rather than assume it. Method: extract the
\citation entries in order from `1-main.aux` (or scan chapter files for the first
\cite of each key in document order) and compare against the entry order in
`1-main.bbl`. If the .aux/.bbl are stale relative to the .tex sources, recompile
first if xelatex+bibtex are available; otherwise say the check needs a fresh
Overleaf compile and do the best static approximation. Report PASS or the exact
mismatches. Do not "fix" ordering by editing References.bib entry order — entry
order in the .bib file is irrelevant to IEEEtran output.

TASK 2 — Web-reference audit in References.bib.
Identify every entry that is fundamentally an online resource (model cards,
HuggingFace pages, blog posts, documentation, @misc/@online entries with url or
howpublished fields). Journal/conference papers with DOIs or arXiv IDs do NOT
need access dates — leave them alone. For each web entry:
  1. Check the URL is present and complete.
  2. Verify the URL still resolves (fetch it). If it resolves, stamp today's date
     as the access date. If it is DEAD, do NOT stamp a date — flag it prominently
     in the report for a replacement decision.
  3. Add the access date so it actually renders in IEEE format. First inspect how
     existing entries render in `1-main.bbl` to pick the mechanism that works with
     IEEEtran (typically the `note` field: note = {[Online]. Available:
     \url{...}. [Accessed: Jul. 28, 2026]} — but confirm against the .bbl and
     avoid duplicating the URL if the style already prints the url field).
  4. Keep formatting consistent across ALL web entries.
Standing decision — do NOT delete unused/orphaned .bib entries (a previous team
decision keeps them); just note any you notice.
Also do NOT change author/title/venue fields: they were verified and corrected in
June 2026 sweeps; if something looks wrong, flag it in the report instead of
editing.

VERIFICATION: recompile (xelatex 1-main.tex; bibtex 1-main; xelatex twice) if
available and confirm the bibliography renders with URLs + access dates and no
new warnings about undefined citations. Otherwise static-check and note Overleaf
verification is needed.

REPORT: Task 1 verdict (PASS/mismatch list); table of all web entries
(key → URL → alive/dead → change made); any dead links or suspicious entries
flagged for Osman.
```

---

## Prompt 4 — Caption placement sweep: tables above, figures below (C7)

```
You are working in the Arabic RAG thesis repo. The LaTeX source is in
`University_of_Khartoum__EEE_bachelor_s_thesis_template/` — main file `1-main.tex`,
chapters in `Chapters/chapter1.tex` … `chapter5.tex` (plus
`Chapters/chapter2_generated.tex` and any files pulled in via \input — trace
them). Compiled with XeLaTeX. Keep edits minimal and surgical. Do not commit —
leave changes in the working tree and end with a report.

CONTEXT: Supervisor directive (Dr. Tahani): table captions must be ABOVE the
table; figure captions must be BELOW the figure. Tables and figures are distinct
entity types with separate numbering (already per-chapter — verify, don't
change). We believe placement is already correct — the job is to verify every
single instance and fix any violations.

TASK:
1. Enumerate EVERY table environment (table, table*, tabularx wrapped in table,
   longtable if any) across the chapter files and all \input'ed .tex files.
   For each: confirm \caption appears BEFORE the tabular content. 
2. Enumerate EVERY figure environment (figure, figure*, subfig usage). For each:
   confirm \caption appears AFTER the \includegraphics / tikz / subfloat content.
3. Fix violations by MOVING the \caption line. Critical LaTeX rule: \label must
   stay immediately AFTER its \caption (a \label before \caption binds to the
   wrong counter and silently breaks cross-references) — when you move a caption,
   move its label with it, and while you're at each site, verify the
   caption+label adjacency even where placement was already correct.
4. Algorithm/listing environments are OUT of scope (different convention) — just
   list them in the report without editing.
5. Generated files note: if a violation sits in `chapter2_generated.tex` or any
   file under `thesis_figures/`, fix it there too BUT flag it in the report — it
   may be overwritten if the generator is re-run, so the fix may need to go into
   the generating notebook as well.

VERIFICATION: compile with xelatex if available (xelatex 1-main.tex; bibtex
1-main; xelatex twice) and confirm no new errors and that cross-references
(\ref) still resolve (no "??" in the log/PDF). Otherwise static-check and note
Overleaf verification is needed.

REPORT: full inventory (Table X.Y / Figure X.Y → file:line → OK or FIXED),
every caption/label move, and any generated-file fixes that need upstreaming.
```
