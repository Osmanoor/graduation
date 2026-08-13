# F3 · Presentation plan — 10 min defence

**Written:** 2026-08-12 · **Defence:** 2026-08-14 · **Format:** 10 min talk + 10 min Q&A, live on Google Meet
**Supersedes:** the "cut F1 down" advice in [F2_two_day_prep_plan.md](F2_two_day_prep_plan.md) §0.
F1 stays as a **narrative source** — good sentences and one good analogy — not as a deck to trim.

---

## 1. The rules this plan obeys

From Dr. Tahani's voice notes, [Part II](../../meetings/2026-07_supervisor_voice_notes_transcripts.md#note-9)
(notes 9–12, 16). These are not suggestions — she is on the panel.

| Rule | Source | Consequence for us |
|---|---|---|
| Cover → **Agenda** → problem → objectives → methodology → results & discussion → conclusion | Note 9 | Agenda slide is **mandatory**. We did not have one. |
| Problem definition is **أهم حاجة** | Note 9 | Gets the largest single block: 90 seconds. |
| **1–2 slides of theory, maximum** | Note 9 | One theory slide. RAG + the two retrievers. That's all. |
| "ما تسهب في النظريات… بتضيع الزمن" | Note 9 | Everything in Ch2 is off the slides. It lives in Q&A. |
| Light text, lean on **drawings and bullets**; explanation is verbal | Note 9 | No paragraphs on slides. A figure + ≤6 words per line. |
| Split roles; **smooth handover**; both must know everything | Note 10 | One rehearsed handover sentence. Both learn both halves. |
| They may ask: *"open page X"*, *"explain this figure"*, *"what does this table mean"* | Note 10 | Thesis PDF open in a second window. Know all 11 Ch4 figures. |
| Live on Google Meet; **mixed Arabic/English is fine** | Note 12 | Screen share, not a projector. Arabic examples land natively. |
| Rehearse three times: mirror → teammate → group | Note 16 | Built into the schedule. |

**Two consequences worth naming.** Google Meet screen share means animation is a liability
(it stutters and drops frames over a shared connection) and small figure labels get worse,
not better, after video compression. And 10 minutes of Q&A against 10 minutes of talk means
**the Q&A is where the marks are** — plan for it as seriously as the slides.

---

## 2. The spine: 9 objectives → 3 groups

Chapter 1 lists **nine** objectives (i–ix). Nine will not fit on a slide and cannot be
tracked by a listener. They cluster naturally into three, and Chapter 5's conclusions fall
into the same three groups. Use these as the agenda, the objectives slide, and the
conclusion slide — the same three labels all three times.

| Group | Objectives | Conclusions | One-line claim |
|---|---|---|---|
| **A · Diagnose** | i, ii | i | Built both baselines, measured where and why Arabic retrieval fails |
| **B · Adapt** | iii, iv, v, vi | ii–vi | Made Query2Doc work in Arabic with small open models; found sparse ≠ dense |
| **C · Ground & place** | vii, viii, ix | vii–xi | Corpus-grounded the expansion, and found *where* to apply it |

Saying the same three words at minute 2, minute 3, and minute 9 is what makes a 10-minute
talk feel complete instead of rushed. Repetition is the structure.

---

## 3. The agenda

Five sections, in Dr. Tahani's mandated order. This is what goes on slide 2, and it is the
order the examiners will expect to see.

| # | Agenda item | Time | Slides |
|---|---|---|---|
| 1 | **Problem Definition** | 105s | 3–4 |
| 2 | **Objectives** | 45s | 5 |
| 3 | **Methodology** | 240s | 6–9 |
| 4 | **Results & Discussion** | 100s | 10–11 |
| 5 | **Conclusion & Future Work** | 75s | 12–13 |

**Theory is not an agenda item.** It is one slide (6) that opens the methodology, placed there
because Dr. Tahani's rule is that theory is only needed once the problem and objectives are
already set: *"النظريات دي كلها معروفة للناس بعد ما شرحت الـ problem بتاعتي وحددت الـ objectives"*.
Putting a "Background" heading on the agenda invites the panel to expect a background section,
which is exactly the section she wants capped.

### What falls under each item

**1 · Problem Definition — 105s, 2 slides.** The most important block in the talk.
- RAG is how LLMs are grounded, and its answer is bounded by what retrieval returns — *retrieval
  sets the ceiling*. Shown with the RAG loop, not taught.
- Arabic retrieval fails at scale, and we measured it ourselves rather than citing it:
  34% of queries fail, ~1 in 10 has no relevant passage even in the top 100.
- Three linguistic causes: morphology, orthography, diglossia.
- The fault is in the **query**, not the retriever or the index — shortest queries score 0.345.
  That is what selects a pre-retrieval intervention.

> The failure numbers are technically Chapter 4 results. They belong here anyway: a measured
> problem is far stronger than an asserted one, and it delivers objective ii early. Label the
> slide "our baseline error analysis" so the provenance is visible and nobody thinks you are
> quoting a paper.

**2 · Objectives — 45s, 1 slide.** The nine objectives, grouped into the three of §2 above.
Do not put nine lines on a slide.

**3 · Methodology — 240s, 4 slides.** The block Dr. Tahani says to prioritise.
- **Setup + the only theory slide.** Sparse (BM25S) vs dense (mDPR) — the distinction the whole
  contribution rests on. MIRACL Arabic: 2,896 queries, 2.06M passages, human judgements. NDCG@10.
- **Query2Doc adapted to Arabic.** Expand the query with a generated pseudo-document. It helped
  dense universally, degraded sparse for 6 of 9 models through term dilution; query repetition
  fixed all nine. One line here covers the ten-model comparison.
- **CSQE.** Ground the expansion in first-pass retrieved documents instead of generating blind.
  Carried by the «الأسماء الخمسة» example.
- **Hybrid fusion and the placement question.** Both retrievers merged (RRF), then the three
  placements tested: sparse only, dense only, both.

**4 · Results & Discussion — 100s, 2 slides.**
- The progression: 0.4621 → **0.7137**, +54.5% over BM25 and +13.9% over the strongest no-QE
  hybrid. The placement table is the discussion: 0.6474 / 0.6936 / **0.7137**.
- Per-query analysis: 56.8% of queries improved, mean +0.189; gains concentrate on short queries
  and on queries whose first pass was already good (0.8877 vs 0.5814).

**5 · Conclusion & Future Work — 75s, 2 slides.**
- The same three objective groups, each ticked with the number that proves it.
- The transferable finding: retriever-specific query representation.
- Three challenges, one future direction.

---

## 3b. Slide-by-slide · 13 slides, 600 seconds

Times are speaking time. Add them up before writing a word of script: **600s hard.**

### Mohammed — 290s · problem, objectives, setup, first method

| # | Slide | s | On the slide | Figure |
|---|---|---|---|---|
| 1 | Cover | 15 | Title large, both names, Dr. Tahani, UofK EEE, 2026 | — |
| 2 | **Agenda** | 20 | The five items above | — |
| 3 | Problem — retrieval sets the ceiling | 45 | RAG loop, step 2 highlighted | `fig_2_1_rag_arch.png` |
| 4 | Problem — measured, and why Arabic | 60 | 34% · 10% · 0.345 + the three causes | `fig_2_5_arabic_challenges.png` |
| 5 | **Objectives** | 45 | Three groups, one line each | — |
| 6 | Setup + the one theory slide | 50 | BM25 vs mDPR · MIRACL · NDCG@10 | `fig_2_2_sparse_vs_dense.png` |
| 7 | Query2Doc + repetition | 55 | Expansion helps dense, dilutes sparse; repetition recovers all 9 | `fig_3_5_query2doc.png` |

### Handover — one rehearsed sentence

> "That gets us a working expansion. Osman will show you what went wrong with it, and what we did about it."

Say it identically every rehearsal. Note 10 makes the handover a graded moment.

### Osman — 310s · the two contributions, results, conclusion

| # | Slide | s | On the slide | Figure |
|---|---|---|---|---|
| 8 | **CSQE** | 80 | «الأسماء الخمسة» before/after · ground it in real documents | **new — see §4** |
| 9 | **Placement** | 55 | Hybrid, then the three assignments | `fig_3_9_best_system_aigen_v2a.png` |
| 10 | Results — progression | 60 | 0.4621 → 0.7137, +54.5% | `fig_4_11_progression_v2_annot.png` |
| 11 | Results — where the gains are | 40 | 56.8% improved · first-pass split | `fig_4_13_firstpass_v2_annot.png` |
| 12 | Conclusion | 45 | The three groups, ticked with numbers | — |
| 13 | Challenges & future work | 30 | 3 limits, 1 next step | — |

**Slide 8 is the one to protect.** «ما هي الأسماء الخمسة في اللغة العربية؟» → the model answered
with a list of boys' names, and a question the system had already solved at rank 1 dropped to
zero. The panel are Arabic speakers on a video call — they will get it in three seconds with no
explanation from you. It teaches blind-generation failure *and* motivates corpus grounding in
one move. Mixed Arabic/English is explicitly allowed (Note 12), so say this part in Arabic.

**Slide 9 is the actual contribution.** Same technique, same fusion, only the placement changes,
and the spread is 0.0663. It is what makes this a thesis rather than an application of someone
else's method.

**Where the time will go wrong.** Methodology is 240 of the 600 seconds — exactly the block where
teams over-explain, get cut off, and never reach their results. **If a rehearsal runs long, cut
slide 7 to 40s** — Query2Doc is prior work, not ours. Never cut slide 9 or slide 10.

---

## 3c. What is excluded from the thesis, and why

Nothing here is deleted — it is **relocated to Q&A**, where there are ten minutes waiting.

| Excluded | Why | Where it goes |
|---|---|---|
| **Ch2 theory in full** — transformers, RAG internals, BM25 formula, cosine similarity, RRF/CC equations, NDCG/MRR derivations | Dr. Tahani's explicit 1–2 slide cap; the panel are EEE faculty who know it; it is the single biggest time sink | Q&A |
| **The 10-model comparison** (obj. iv) — leaderboards, Falcon-H1, Jais-2, Qwen3, SILMA | A whole chapter section that does not advance the story toward 0.7137. Costs ~2 min to present honestly | **One line on slide 7 + one on slide 12** — see warning below |
| **Cross-cutting model findings** — size correlation, generational improvement, OALL not predictive | Genuinely interesting, entirely secondary to the contribution | Q&A |
| **Dropped models** — ALLaM-7B tokeniser bug, GPT-OSS-20B | A negative result about someone else's model, not our contribution | Q&A (Challenges iii) |
| **Alpha sweep** (α=1–4) | An ablation of an ablation, and nearly flat (0.7123→0.7137). Zero narrative value | Q&A |
| **CC vs RRF fusion** | Two methods, near-identical (0.7088 vs 0.7137). Showing both invites "why RRF?" and costs time | Q&A — present RRF only, consistently |
| **CSQE component ablation** — corpus-only 0.5381 / blind-only 0.5752 / mixed 0.6157 | A *defensive* result: it answers "why not corpus-only?" It is wasted unless asked | **Backup slide** — high chance of being asked |
| **Engineering detail** — batching, left-padding, 4-bit NF4, T4/A100, 40 min/run, two-notebook workflow | Implementation, not finding. Compresses to "on free Colab GPUs" | Q&A (obj. iii) |
| **Recall@10, Recall@100, MRR** | One metric on slides keeps every number on the same scale and comparable | Q&A — say the others exist |
| **Dataset selection rationale** | A justification, not a finding | Q&A — covered by the "why only MSA?" answer |
| **Related-work lineage** — HyDE, GRF, Exp4Fuse | Compresses to one line: "built on English with 175B proprietary models" | Q&A — Exp4Fuse is the novelty answer |
| **5 of 8 challenges, 8 of 9 future-work items** | 75 seconds cannot carry seventeen bullets | Q&A |

> ⚠️ **The one exclusion that carries risk: the model comparison.** It is a *stated objective* (iv)
> and a large piece of your work. If it is invisible in the talk, an examiner checking the
> objectives against the presentation will ask where it went — and that is an avoidable bad
> moment. It must appear twice, briefly: on slide 7 ("we compared ten open models between 2 and
> 8 billion parameters; Aya Expanse 8B was best overall") and as a ticked line on slide 12.
> Two sentences, and the objective is visibly met.

---

## 4. Figures — decision

**Reuse from [thesis_figures/output/png/](../../thesis_figures/output/png/). Build exactly one new visual.**

There are 60 rendered PNGs and they cover 5 of the 6 slots above. The one genuine gap is the
«الأسماء الخمسة» before/after — the strongest content in the talk has no thesis figure, because
in the thesis it is prose. Build that one. It is a two-panel comparison:

```
  الاستعلام: ما هي الأسماء الخمسة في اللغة العربية؟

  ┌─ blind expansion ──────────┐   ┌─ corpus-steered ───────────┐
  │ ١. محمد ٢. آدم ٣. إبراهيم  │   │ أب، أخ، حم، فو، ذو          │
  │ (most popular boys' names) │   │ (copied from the corpus)   │
  │            0.000           │   │           1.000            │
  └────────────────────────────┘   └────────────────────────────┘
```

Content is already written up in [F1_csqe_example.md](F1_csqe_example.md) — take the text from
there rather than re-deriving it.

**Check every reused figure at full screen before committing.** Thesis figures are sized for A4
at 8–9pt labels; on a shared Meet window at 1080p those become unreadable. If a label is too
small, **re-render it larger from the plotting script** — do not redraw it and do not screenshot
and stretch it. That is the only figure work worth doing in two days.

**No animation.** On a shared Google Meet stream it drops frames, and it earns nothing.

---

## 5. Tooling — one thing to flag

**Canva MCP is not connected in this session.** The only MCP servers available here are Gamma,
Gmail, Google Calendar and Hugging Face, and all four are unauthenticated — this session cannot
run the OAuth flow, so you would need to authorize them from your claude.ai connector settings
first. Canva is not in the list at all.

So the practical options are:
- **Canva in the browser, by hand** — you keep full design control, which is what you actually
  want since design is your objection to F1. Slowest, but 12 slides is not many.
- **Gamma via MCP** — needs authorizing first, and it generates a whole deck from a prompt.
  Fast, but you get its aesthetic, not yours.
- **Plain PowerPoint** — Dr. Tahani said "الغالب الأعم الناس بتشتغل على الـ PowerPoint" and no
  tool is required. Zero risk on a screen share.

**My call: build it by hand in Canva.** Twelve slides with one figure each is a two-hour job,
you get the design you want, and this plan already fixes the content so the tool only has to
render it. Export to PDF and present the PDF — a live Canva link on a shared Meet is one more
thing that can fail.

---

## 6. Q&A — 10 minutes, and it is half the exam

More Q&A than talk. Prepare it properly.

**Drill 1 · every Chapter 4 figure, one sentence each.** Note 10 says they will ask *"شرح لينا
الـ figure الفلاني"* and *"الـ table ده بيعني شنو؟"*. There are 11 figures in Ch4. Split them:
each of you takes all 11, not five each — questions get aimed at one person by name, and "my
partner did that part" is explicitly a scoring penalty.

**Drill 2 · the Challenges list is the question list.** Chapter 5 §5.2 has eight items and they
are precisely what an examiner would probe: resource limits, term dilution, the dropped model
(ALLaM), MSA-only scope, single technique, mDPR not fine-tuned, first-pass dependence, the
CC-BY-NC licence. You wrote them. Own them out loud in 20 seconds each.

**Drill 3 · the six numbers.** 0.4621 · 0.4993 · 0.6267 · 0.7137 · +54.5% · 56.8%. Anything else,
say "that's in Table 4.x, let me open it" — and have the PDF open to do it. Note 10 says having
the thesis to hand is expected, not a weakness.

**The three questions most likely to come:**
1. *"Where is the generation? This is only half a RAG system."* → retrieval sets the ceiling.
   Better still, say it in slide 3 so it never gets asked.
2. *"Why only MSA?"* → MIRACL is the only Arabic benchmark with human relevance judgements at
   this scale. It is in Challenges iv, and dialect evaluation is Recommendation iii.
3. *"Is this actually new?"* → the narrow claim only: corpus-steered expansion applied
   asymmetrically to the sparse retriever in an Arabic MSA dense–sparse hybrid.

---

## 7. Order of work from here

1. **Finish your read of Ch1 + Ch5** (you're mid-way). Confirm the 3-group mapping in §2 above
   matches how you read the objectives — you and Osman own that call, not me.
2. **Agree the split and the 12 slots** with Osman. One session, 45 min. Not a brainstorm from
   zero — react to the table in §3, move things, delete things.
3. **Write the words.** 600 words each, out loud, timed as you write. Pull sentences from
   `F1_defence_script.md` where they fit — it has good lines even if the deck is wrong.
4. **Build in Canva.** 12 slides, one figure each, minimal text.
5. **Rehearse ×3** per Note 16: alone at a mirror, then together, then with the group.
6. **Freeze the deck the night before.** Export to PDF.
