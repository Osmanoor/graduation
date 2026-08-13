# F2 · Two-day defence prep plan

**Written:** 2026-08-12 · **Defence:** 2026-08-14 · **Format:** 10 min total, 5 min each
**Status:** coaching plan, not a deliverable. Tick things off and throw it away after the defence.

---

## 0. SUPERSEDED — read [F3_presentation_plan.md](F3_presentation_plan.md) instead

> This section told you to cut `F1_slides_draft.html` down to 10 slides. That was wrong.
> F1 was a narrative experiment for explaining QE/CSQE intuitively — never a finished deck —
> and it does not follow the structure Dr. Tahani mandated in her voice notes (agenda slide,
> theory capped at 1–2 slides, methodology and results prioritised). The deck starts clean;
> F1 is kept as a source of sentences and the mufti analogy.
>
> **Sections 1 and 3 below (the reading blocks and defence-day rules) are still valid.**
> Section 4's skeleton is replaced by §3 of F3.

Your five steps are the right steps. But step order 2→3→4 assumes you are **building content**.
You are not. You already have `F1_defence_script.md` (3,300 words) and `F1_slides_draft.html`
(22 slides). Both are built for a **25–30 minute** talk.

You have **10 minutes**.

So the job for the next two days is **cutting, not creating.** That changes everything:

| Your plan said | Change it to |
|---|---|
| Brainstorm the main points | Open the 22 slides and **delete 12 of them** |
| Build our content | Cut the script from 3,300 words → **1,200 words** |
| Build slides in Canva/Gamma | Cut the deck you already have. Do not restart in a new tool. |
| Decide which figures to make | **Make zero.** You have 60 rendered PNGs already. Pick 3. |

Creating from scratch in a new tool with 2 days left is the single most common way
final-year teams lose marks. You have assets. Cut them.

### The 10-minute budget, in hard numbers

- **10 min of speech ≈ 1,200 words.** Not negotiable. Read aloud and time it.
- **~600 words each.** That is about two A4 pages of double-spaced text, total, for both of you.
- **10 content slides + 1 title = 11.** Five slides each. ~55 seconds per slide.
- Every slide you add steals ~50 seconds from another slide. There is no free slide.

---

## 1. Today (Aug 12) — reading. 3 hours, timeboxed.

Do this **alone**, before you talk to Osman. Reading together is slower and you will
drift into discussing the deck instead of reading.

### Block A · Chapter 1 — 30 minutes, hard stop

`Chapters/chapter1.tex` — 1,661 words. Four sections: Preamble, Problem Definition,
Objectives, Thesis Layout.

You are not reading to learn it. You wrote it. You are reading to extract **four things.**
Write them by hand on one sheet of paper:

1. **The objectives, copied out verbatim and numbered.** Exactly as they appear. Do not
   paraphrase. This is the contract you signed with the jury and they will check it.
2. Next to each objective, one line: **"met / partly met / not met"** — and the *number*
   that proves it.
3. The problem statement, **compressed to one sentence in your own words.** If you cannot
   do it in one sentence, you do not own it yet. Try again.
4. Anything in Ch1 that is **no longer true** of the finished work. Objectives written in
   November sometimes do not match what got built. If there is a mismatch, you must know
   about it before the jury finds it — not to hide it, to have a sentence ready.

> This is the highest-value 30 minutes of the whole two days. The objectives list is going
> to become slide 2 of your deck (see §4).

### Block B · Chapter 5 — 45 minutes, hard stop

`Chapters/chapter5.tex` — 2,813 words. Three sections: Conclusions (l.8),
Challenges (l.33), Recommendations for Future Work (l.58).

Extract **three things**, again by hand:

1. From **Conclusions** — the sentences that state a *claim*. Mark each one C1, C2, C3…
   You will probably find 4–6. Then circle the **two** you would keep if you could only
   keep two. Those two are your results slide.
2. From **Challenges** — the honest list. For each item, ask: *"if a jury member raises
   this, do I have a 20-second answer?"* Write the answer if you don't. This section is
   your Q&A armour and it is the reason to read Ch5 properly rather than skim it.
3. From **Recommendations** — pick **one** future-work item you can say with conviction.
   Only one. "What next?" is a near-certain question and a vague answer there undoes a
   good talk.

### Block C · Skim Ch 2, 3, 4 — 90 minutes total, hard stop

**Skim means: figures, tables, and the first paragraph of each section. Nothing else.**
Do not read body prose. Set a timer per chapter.

- **Ch2 (6,065 words) — 20 min.** You need §Related Work → §Research Gap only. Everything
  else in Ch2 is background you already know. The gap paragraph is what justifies your
  existence to the jury.
- **Ch3 (5,268 words) — 25 min.** Look at the *figures only*: pipeline, mDPR, BM25S,
  Query2Doc, hybrid, CSQE. Six diagrams. You are choosing which one goes on your
  methodology slide. Read §CSQE (l.394) properly — it is the one method you must be able
  to explain cold.
- **Ch4 (9,491 words) — 45 min.** This is your Q&A ammunition, not slide material. Read
  **the tables and figure captions only.** Eleven figures. Your goal is to know *where*
  each number lives so that if challenged you can say "that's Table 4.x" with confidence.
  Pay special attention to §Per-Query Error Analysis (l.720) — win/loss, first-pass split,
  regressions. That is where a sharp examiner will push.

**Do not** try to memorise Ch4's numbers. Memorise **six**: 0.4621, 0.4993, 0.6267, 0.7137,
+54.5%, 56.8%. Everything else you may look up or say "I'd have to check the table."

### End of today, before you sleep

Write **one paragraph**, five sentences, answering: *what did we do and why does it matter?*
No numbers. No jargon. If you can write that paragraph, the deck almost writes itself.
If you can't, that is the thing to fix with Osman tomorrow — not the slide design.

---

## 2. Tomorrow (Aug 13) — the cutting session with Osman

### Session 1 · 60 min — cut, don't brainstorm

Open `F1_slides_draft.html` in a browser. Twenty-two slides. Go through them once and
sort each into **KEEP / KILL / MERGE**. Rules:

- You may keep **10**.
- Anything that is background the jury already knows → KILL. They know what ChatGPT is.
- Anything that is a *second* example of a point already made → KILL.
- Two slides making one point → MERGE.

Then decide the **speaking split**. My recommendation, and it follows the natural seam in
the existing narrative:

- **Mohammed (5 min):** problem → why Arabic is harder → the diagnosis (fault is in the query)
- **Osman (5 min):** the method (Query2Doc → CSQE → placement) → results → limits

Whoever speaks second must *not* re-explain anything. Practise the handover sentence out
loud. It should be one sentence and it should be the same every time.

### Session 2 · 90 min — write the 1,200 words

Cut the script, don't rewrite it. `F1_defence_script.md` already has the good sentences in
it; most of what you delete is the connective prose between them. Keep every sentence that
is bolded in that file — those are the load-bearing ones — and delete around them.

**Protect these three things through the cut.** They are the highest value-per-second
material you have:

1. **"Retrieval sets the ceiling."** One sentence. It pre-empts *"where is the generation?"*,
   which is the most likely hostile question. Delivering it unprompted is worth 30 seconds.
2. **The «الأسماء الخمسة» example.** 90 seconds, and the best 90 seconds in the deck. The
   jury are Arabic speakers; they will get it instantly and with no explanation from you.
   No diagram in the world teaches the problem that fast.
3. **The placement table** (0.6267 / 0.6474 / 0.6936 / **0.7137**). Four rows. This is your
   actual contribution and it fits on one slide.

Everything else is negotiable. If the cut gets painful, cut Query2Doc background and cut
the model comparison entirely — ten models is a chapter, not a slide.

### Session 3 · 60 min — figures. Decision already made.

**Reuse thesis figures. Build nothing new. No animation.**

You have 60 rendered PNGs in [thesis_figures/output/png/](thesis_figures/output/png/).
Building new figures costs hours and earns zero marks; Canva animation costs an evening and
earns less than zero if it stutters on the projector. Pick **three**, maximum:

| Slot | Candidate | Why |
|---|---|---|
| Problem | `fig_2_5_arabic_challenges.png` or `fig_4_3_length_box_v1.png` | shows the failure, no explanation needed |
| Method | `fig_3_8_csqe_aigen_v5a.png` | the one diagram that carries CSQE |
| Results | `fig_4_11_progression_v2_annot.png` | one image, whole story, already annotated |

Check each at full screen for readability before committing. A thesis figure sized for A4
often has 8pt labels that vanish on a projector. If the labels are too small, that is the
*only* legitimate reason to touch a figure — and the fix is re-render at larger font, not redraw.

### Session 4 · evening, 60 min — rehearse with a stopwatch

Full run, both of you, standing, out loud, timed. Then again. Then again.

**The deck freezes tonight.** No edits after this session.

Expect the first run to be 15 minutes. That is normal. Cut, don't speed up — a rushed
10-minute delivery of a 15-minute talk is the worst possible outcome and the jury can hear it.

---

## 3. Defence day (Aug 14) — no building

- One full rehearsal, out loud, timed.
- Read your Ch5 Challenges sheet once. That's the Q&A prep.
- **Do not open the slides to improve them.** Nothing you change in the last hours will be
  rehearsed, and unrehearsed slides are where people freeze.

---

## 4. Recommended 11-slide skeleton

Fill this in during Session 1. Blank on purpose — the content decisions are yours.

| # | Slot | Who | Target | Source slide in F1 |
|---|---|---|---|---|
| 1 | Title | — | 10s | 01 |
| 2 | **Objectives** (from your Ch1 sheet) | M | 30s | *new — costs 30s, buys the jury's checklist* |
| 3 | The problem: retrieval sets the ceiling | M | 60s | 04 + 05 merged |
| 4 | Why Arabic is harder | M | 60s | 09 |
| 5 | The diagnosis: the fault is in the query | M | 60s | 08 |
| 6 | Handover + the fix: expand the query | O | 60s | 11 |
| 7 | **الأسماء الخمسة** — it hallucinated | O | 90s | 14 + 15 merged |
| 8 | CSQE: look before you speak | O | 60s | 16 + 17 merged |
| 9 | **Placement** — the contribution | O | 60s | 18 |
| 10 | Results + did we meet the objectives | O | 60s | 19 + 20 merged |
| 11 | Limits, then thank you | O | 30s | 21 + 22 merged |

Slide 2 and slide 10 are a matched pair: state the contract, then show you kept it. That
loop is what makes a short defence feel complete rather than truncated.

**Killed:** 02, 03, 06, 07, 10, 12, 13 — background, dataset detail, the circle, model
comparison. All of it is legitimate Q&A material. None of it survives a 10-minute cut.

---

## 5. Things not to do

- Do not restart the deck in Canva or Gamma. You have a deck.
- Do not build new figures.
- Do not animate anything.
- Do not read Ch2 or Ch3 in full.
- Do not memorise numbers beyond the six in §1 Block C.
- Do not add a slide after tomorrow night.
