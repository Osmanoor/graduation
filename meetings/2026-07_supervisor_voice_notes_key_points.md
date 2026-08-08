# Supervisor Voice Notes (July 2026) — Key Information & Impact

**Source:** `meetings/2026-07_supervisor_voice_notes_transcripts.md` (16 voice notes, ~38 min, `recordings/*.ogg`).
**Raw engine output:** `meetings/voice_notes_raw/{gemini,speechmatics}/`.
**Extracted:** 2026-07-28. **Re-verified against a second engine:** 2026-08-05.
**Speaker:** the supervisor, Dr. Tahani — *inferred from content*, not stated in the audio.

**Scope note:** unlike `Thesis Review Report.md`, which answered *our* 10 specific questions, these notes are **general guidance broadcast to all four project groups**. That distinction matters for the page-count conflict in §1.1.

> **Provenance.** Every file was transcribed twice — Speechmatics Batch v2 and `gemini-3.1-pro-preview` — and the outputs diffed. Gemini is the primary text. The full difference table is in the transcripts file under *"Where the two engines disagree"*. Three claims in the first version of this file were marked *inferred* and are now **confirmed** by the second engine; one new conflict opened (panel size). Corrections are listed in §5.

---

## TL;DR — what actually changes

| # | Finding | Effect on the task list |
|---|---|---|
| 1 | **She expects 50–70 pages, max ~80** — we are calibrated to ≤100 and measure 100–105 | **D5 severity is unresolved until she answers.** Could mean cutting ~20 pages, not ~5 |
| 2 | **"ما تكون ترجمة Google ولا ترجمة AI"** for the Arabic abstract | **B2 is tagged `[AI]`.** Direct conflict — see §3.1 |
| 3 | **She must see Ch.1, Ch.5 and BOTH abstracts before submission**; unavailable from ~1/8 | **B2 is now gating a supervisor review**, not just a formatting task |
| 4 | Full **cover-page spec** recovered from the audio | **Unblocks the audit J2 defers** |
| 5 | Defense is **live on Google Meet**; theory capped at **1–2 slides** | **F1** gets a concrete brief |

---

## 1. Load-bearing findings

### 1.1 Page count — CONFLICT, still unresolved ⚠️

> **Note 8:** *"ما في عدد محدد ولكن متوقع يعني من 50، 70 أقصى حاجة ممكن 80 صفحة. It's quite enough يعني للمشروع."*

She says this immediately **after** explaining that appendices are lettered and numbered separately, so 50–80 reads as the **numbered body ending at the references page**.

| Source | Figure |
|---|---|
| `Thesis Review Report.md` §10 — her answer to *our* question | core Ch.1–5 **≤ 100** |
| Voice note 8 — general guidance to all four groups | **50–70 expected, ~80 max** |
| `THESIS_FINAL_SUBMISSION_TASKS.md` D2 (measured from the compiled PDF, 2026-08-02) | **105** |
| Same file, J1 (measured after the Times New Roman fix, 2026-08-01) | **exactly 100** |

Two separate conflicts sit on top of each other here:

- **Which ceiling binds** — 80 or 100. The specific answer she gave us normally beats general guidance, but the gap is large enough to change the plan.
- **What our count actually is** — J1's 100 postdates the font fix; D2's 105 was measured from a PDF built *before* it (this is exactly the stale-PDF hazard J4 documents). J1 is the later measurement of the two in real terms.

**Why it matters:** under a 100 ceiling we are at the line and D5 trims for margin. Under an 80 ceiling we are ~20 pages over and D2's appendix moves plus an aggressive D5 would still not be enough. **This one question sizes D5.** Bundle it with the question D2 already has queued for her (`D2 DECISION 3`).

### 1.2 No AI translation for the Arabic abstract 🔒

> **Note 13:** *"الترجمة حاولوا بقدر الإمكان ما تكون ترجمة **Google** ولا ترجمة **AI**، حاولوا استخدموا الـ terminologies المستخدمة عندنا في اللغة العربية الصحيحة، ده في ترجمة المستخلص."*

Speechmatics rendered this as *"ولا ترجمة أي"* and the AI clause was lost. Gemini recovers it. **B2 is currently tagged `[AI]`** in the task list. See §3.1.

### 1.3 She must review Ch.1, Ch.5 and both abstracts before submission 🔒

> **Note 13:** *"بكون ممكن محتاجة أشوف Chapter 1 و Chapter 5 اللي هو comments, conclusion and recommendations for future work، ده بكون مهم أشوفه. **أهم من ديل كلهم الـ abstract بالعربي والإنجليزي لازم أشوفهم، لازم أشوفهم قبل التسليم.**"*

She has already seen Ch.2 in full and Ch.3/Ch.4 partially. What she has not seen and explicitly requires: **Ch.1, Ch.5, and both abstracts** — the abstracts rated above the chapters, with "لازم أشوفهم" repeated.

B1 is done. **B2 is the open item on this gate**, and it is Osman's.

### 1.4 Dates and availability ⚠️ verify

> **Note 13:** *"عندي زواج بتي يوم **1/8**، فهكون في حالة بتاعت عدم استقرار في الفترة الجاية."*
> **Note 14:** *"ممكن من **يوم خمسة** اللي هو **بعد التسليم** نحدد يوم… أنا بكون إن شاء الله فضيت."*

Gemini transcribes the wedding date directly as **1/8 (1 August)**, confirming what was previously an inference from spoken numerals. `يوم خمسة` = the 5th; Gemini flags that the month is not spoken, but 5 August is the only reading consistent with the wedding and with *"after the submission"*.

**Implication: submission falls in the first days of August, and she is effectively unavailable in the run-up to 1 August.** Anything needing her review (§1.3) has to reach her before then.

### 1.5 Defense format and panel

- **Live on Google Meet** (note 12) — the last two years were pre-recorded.
- Slides officially English; **mixed Arabic/English delivery explicitly fine**: *"عادي احنا الطلاب بيشتغلوا mix"*.
- Questions are **not** meant to be hard — they verify you did the work: *"أسئلة بغرض التأكد… عشان التقييم يكون fair"*.
- Both students in **one panel**, splitting the talk, with **seamless handoffs**. Questions go to a *named* student; not knowing your partner's section is a negative mark.
- Expect *"open page X, explain this table"* → **keep a copy of the thesis open**.
- Soft vs. hard copy is the **coordinator's** call, not hers.
- ⚠️ **Panel size unresolved.** Speechmatics heard *supervisor + 3 engineers*; Gemini heard *supervisor + 2 examiners*. The engines disagree and the readings are not acoustically close. Do not cite a number.

### 1.6 Presentation structure (note 9)

Concrete, and more specific than we had:

1. Title slide — project name large, student names, supervisor
2. **Agenda slide — mandatory**
3. Introduction / Problem Definition — *"أهم حاجة"*
4. Objectives
5. Methodology — strictly what was actually done
6. Results and Discussion
7. Conclusion

> **Theory is capped at 1–2 slides maximum.** Her reasoning: examiners already know the theory, and if you overrun they cut you off — *"يقولوا ليك لا خلاص كفاية امشي خلاص للنتائج"* — so you lose the chance to present your own work. Minimal text, heavy on graphics and bullets, explanation delivered verbally.

She also refers twice to a **recorded presentation-skills lecture she previously sent**. Worth finding.

### 1.7 Marks arithmetic (notes 1, 8)

- Examiners allocate **10 of 60 marks** to the thesis document itself.
- Poor presentation of the document can cost **5–6 of those 10**, and *"بتطلعك من الـ A plus"* — it takes A+ off the table regardless of content quality.
- She names the exact failure mode: an **abstract** over ¾ page (*"صفحتين، صفحة ونص"*), or one too short (*"two paragraphs ما واصلة نص صفحة"*), or unjustified margins, or the wrong font.

### 1.8 Cite a submitted paper as a contribution (note 13)

> *"إذا في مجموعة قدمت paper للنشر حتى ولو ما نشرت يستحسن كمان تشيروا ليها كـ **contribution**… بيزيد من أسهم الطلاب."*

Frame it as a **contribution**, and it counts even if only submitted or accepted-not-published.

---

## 2. Formatting and content rules, consolidated

### 2.1 Document formatting (note 1)

| Element | Rule |
|---|---|
| Body | **12 pt Times New Roman, unbold, 1.5 line spacing, justified** |
| Chapter title | **18 pt bold, centred** |
| Side headings (1.1) | **16 pt TNR bold** |
| Heading range she quotes | 14 / 16 / up to 18 |
| Cover title | **20 pt TNR bold** |

**Cover page, full spec** — project title 20 pt TNR bold · the submission phrase in *italic* · student names **and index numbers** · supervisor name · *"submitted to Department of Electrical and Electronic Engineering, Faculty of Engineering, University of Khartoum"* · date · university logo (recent practice). **Do not design one yourself** (*"ما بتعمل صفحة غلاف من راسك"*) — use the department template, and if the coordinator circulates one, that overrides.

**Page numbering** — cover is page `i` roman but **shows no number**; all front matter is roman in a **separate section**; arabic numerals start at Chapter 1 and run to the references page.

### 2.2 Chapters

- **Ch.1** — general introduction, problem definition, objectives. **Not** methodology or results. Related work belongs in Ch.2. **Always short.** Ends with the thesis layout paragraph.
- **Objectives** — may be revised right up to thesis writing; must be *"very specific"* (she says it twice), point at the methodology actually performed, and show the stated problem was solved.
- **Thesis layout** — she allows *"one long paragraph … or different paragraphs"*, preferring continuous prose. ⚠️ Softer than the Review Report's "must be ONE paragraph". C4's one-paragraph target is still the safe choice.
- **Ch.2** — all theory, definitions and equations live here. Ch.3 **cross-references the section** instead of restating it.
- **Ch.3** — may be named after the project. Every step, *"من الـ A to Z"*. Written **zig-zag** with Ch.4: 3.1 → its results in 4.1, 3.2 → 4.2.
- **Ch.4** — flexible title (*results discussion / results and discussion / results analysis and discussion*). Results need not be perfect; the **engineering explanation of why** is what earns marks. **Graphics preferred over prose and tables** — tables that must stay have to be clear and meaningful.
- **Ch.5** — *"comments, conclusion and recommendations for future work"*. Recommendations are emphasised: they must guide future students, **and you must be able to explain why you did not implement them yourself**.

### 2.3 Floats, citations, appendices

- **Figures** — centred; number and caption **below**, also centred; bold. Numbered per chapter (2.1, 2.2).
- **Tables** — caption **above**. Numbered per chapter.
- **Captions must be self-explanatory** — not one word, not vague; an examiner should never have to ask what a figure shows.
- **Equations** — numbered per chapter. *(Checked: 15 `\begin{equation}` environments, 0 unnumbered display blocks. Already compliant.)*
- **Citations** — `[n]` at the **end of the paragraph**, numbered **by order of first appearance**, IEEE style. Web references need full URL + access date.
- **Abbreviations** — first mention written in full, the abbreviated letters capitalised, abbreviation in **round brackets, explicitly not square**. List of Abbreviations in front matter after ToC / List of Figures / List of Tables, sorted **alphabetically**.
- **Appendices** — lettered, with their own numbering: A1, A2, A3 / B1, B2, B3. Code goes here.

---

## 3. Impact on `THESIS_FINAL_SUBMISSION_TASKS.md`

Assessed against the task list **as it stands on 2026-08-05** (Phase A complete, J1/B1/C1/C2/C3/C6/C7/C8/D1/D2/E1 done).

### 3.1 B2 — the `[AI]` tag now conflicts with an explicit instruction ⚠️

B2 is tagged `[AI]` and scoped as "re-derive from the new English abstract". She said: **no Google translation, no AI translation** (§1.2).

This is not fatal, but it needs a deliberate call. Reading her intent charitably, the target is *machine-translated Arabic that reads like machine-translated Arabic* — not a ban on tooling. The defensible route: **Osman writes the Arabic himself**, using AI only to check terminology against standard Arabic equivalents, and the result is reviewed by both of you for fluency. What must not happen is pasting the English abstract into a model and shipping the output.

Worth deciding explicitly and recording in the task, because she **will read this abstract personally** (§1.3) and machine-translated Arabic is recognisable on sight.

### 3.2 B2 is now on the critical path

B1 is done; B2 is the last piece of the artefact she rated most important and said twice she must see before submission — and she goes quiet around 1 August (§1.4). B2's position in Phase B understates its urgency.

### 3.3 J2 — the cover-page audit is unblocked

J2 currently reads *"Cover page not yet audited against [01:47]"*. The spec is now fully recovered (§2.1) and the audit can be done. J2 also gains: chapter titles must be **centred**, and the body-weight question is settled (**unbold** — Speechmatics's "bold" was a transcription error). Subsection (1.1.1) has no explicit rule from her; 14 pt is the natural reading of her "14, 16, up to 18" range.

*Applied to the task file in this pass.*

### 3.4 D5 cannot be sized until the page question is answered

E1 concluded *"D5 does not need to be aggressive"* from a 97-page measurement; D2 reversed that with 105. The 80-page reading would reverse it much further. **D5's scope is blocked on §1.1**, and that is a one-line question to her.

### 3.5 Smaller confirmations

| Task | Effect |
|---|---|
| **C3** (done) | Verify abbreviations use **round** brackets, not square — new detail, quick grep |
| **C4** (open) | Still correct as written; she is softer than the Report, so no need to force one paragraph if it reads badly |
| **C5** (open) | Unchanged |
| **E2 / E3** (open) | Add: figures must be **centred**; captions self-explanatory. Her graphics-over-tables preference supports E1's verdicts |
| **J3** (open) | Strengthened — she requires tables be *"clear, understandable and meaningful"*; `tab:full_summary` printing "Baselin" fails that outright |
| **A6** (done) | Ch.5 must carry **recommendations for future work**, and you must be able to justify not implementing them. Worth a read-through against her framing |
| **D3** (open) | Appendix numbering confirmed: A1/A2/A3 per appendix letter |
| **F1** (open) | Now has a concrete brief — §1.6 |

### 3.6 New task candidates — **AI Suggestion**

| ID | Task | Owner | Effort |
|---|---|---|---|
| **D6** | Send Ch.1 + Ch.5 + EN/AR abstracts to Dr. Tahani for pre-submission review, before ~1 Aug; allow a round-trip | Elhaj | S |
| **D7** | One message, four questions: binding page ceiling (§1.1); the D2 DECISION 3 appendix question; confirm the dates; soft vs. hard copy | Elhaj | S |
| **J10** | Audit the cover page against the full spec in §2.1 — *(or fold into J2)* | Elhaj | S |
| **D8** | If any paper has been submitted, cite it as a **contribution** (§1.8) | JOINT | S |
| **F2** | Split the talk with seamless handoffs; both able to answer on **any** section; build the deck to §1.6's structure with theory capped at 1–2 slides | JOINT | M |
| **F3** | Rehearsal ladder: mirror → teammate → group session with her (~5 Aug). Find her presentation-skills lecture | JOINT | M |
| **F4** | Navigable copy of the thesis open during the live defense (§1.5) | JOINT | S |

---

## 4. Open questions for her ⚠️

1. **Is our binding ceiling 80 or 100 pages?** Highest-value question on this list — it sizes D5. *(§1.1)*
2. **Do the per-model description sections in Ch.2 count as appendix material?** *(already queued as D2 DECISION 3 — send together)*
3. **Confirm the dates:** wedding 1 August, rehearsal the 5th, and the actual submission deadline. *(§1.4)*
4. **Soft copy, hard copy, or both** at the defense — has the coordinator ruled? *(§1.5)*
5. Has the coordinator circulated a **cover-page template** this year? *(§2.1)*

---

## 5. Corrections applied after the second-engine cross-check (2026-08-05)

What changed in this file versus its first version:

- **The ¾-page rule → confirmed as the abstract.** Previously flagged *"⚠️ inference — the word abstract does not appear"*. Gemini's transcript contains *"فتح الـ abstract ولقى الـ abstract أكتر من تلاتة أرباع صفحة"*. **Caveat withdrawn.**
- **Wedding date → confirmed 1/8.** Previously inferred from spoken numerals.
- **The review gate → confirmed as the abstracts.** Previously inferred from *"بالعربي والإنجليزي"*; Gemini has *"الـ abstract بالعربي والإنجليزي"* explicitly.
- **Added:** the AI-translation ban (§1.2), round-vs-square brackets (§2.3), the A+ consequence (§1.7), the full cover-page spec (§2.1), the presentation structure and 1–2 slide theory cap (§1.6), equation numbering (§2.3), figure centring (§2.3), Ch.5's real name (§2.2), "contribution" framing (§1.8).
- **Corrected:** body text is **unbold** 12 pt (the first version, following Speechmatics, implied bold).
- **New unresolved conflict:** panel size, supervisor + 2 or + 3 (§1.5).
- **Impact section rewritten.** The first version was written against a stale copy of the task list and recommended changes to tasks that were already complete.

Full engine-by-engine difference table: `2026-07_supervisor_voice_notes_transcripts.md` → *"Where the two engines disagree"*.

---

## 6. No action needed

- **Note 15** is pure reassurance — all four groups did strong work; confidence is 90% of the defense.
- **Note 11** — eye contact, body language, hands out of pockets. One substantive point: **if you don't understand a question, ask for it to be repeated**; an off-point answer scores worse than asking.
- **Note 10**'s history of the defense format (solo defenses → paired panels) is background.
- **Note 6** praises the analysis itself — *"طريقة تحليلكم professional"*. Her concern is the **presentation** of it, not the quality.
