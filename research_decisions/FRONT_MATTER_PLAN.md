# Front Matter — Plan for the Empty Pages (J10)

**Date:** 2026-08-04 · **Status:** PLAN. Nothing applied.
**Why it matters:** these are the **first four pages an examiner sees**. Dr. Tahani puts the
write-up at **10 marks of 60**, and `2026-07_supervisor_voice_notes_key_points.md:97` records
that presentation faults alone *"can cost 5–6 of those 10"*.

---

## 1. Current state — all four are empty or placeholder

| Page | File | State |
|---|---|---|
| Title | `1-main.tex:100-119` | **Every field is a template placeholder** |
| Declaration of Authorship | `2-DeclarationofAuthorship.tex` | **One template instruction sentence.** No declaration text at all |
| Dedication | `3-Dedication.tex` | **`\chapter*{Dedication}` and nothing else** |
| Acknowledgments | `4-Acknowledgements.tex` | **`\chapter*{Acknowledgments}` and nothing else** |

Verbatim, the title page currently prints:

```
This is the Thesis Title
Student Name (Index)
Student Name (Index)
Supervisor name
September 2024
```

---

## 2. What only Elhaj/Osman can supply

Nothing in the repo contains any of these. I searched: names appear in experiment docs
(*Mohammed Elhaj Sami*, *Osman Bashir*), but there is **no title, no index number, and no
supervisor surname** anywhere.

| # | Needed | Notes |
|---|---|---|
| Q1 | **The exact thesis title** | ⚠️ **Is a title already registered with the department?** If the project was registered under a fixed title, that one must be used and §4's options are irrelevant. Check first. |
| Q2 | **Both index numbers** | Format per department convention |
| Q3 | **Dr. Tahani's full name and academic title** | Only "Dr. Tahani" appears anywhere in the repo |
| Q4 | **Submission month and year** | Currently says September 2024 |
| Q5 | **Has the coordinator circulated a template?** | Voice note 1 [02:22]: *"إذا حصل تغيير والمنسقة رسلت … تمبلت محددة الناس تمشي على التمبليت بتاع المنسقة"* — if she sent one, follow it and ignore §3 |

---

## 3. Formatting rules that are already specified

From `meetings/2026-07_supervisor_voice_notes_transcripts.md`, Note 1:

| Element | Rule | Source | Current |
|---|---|---|---|
| Project name | **Times New Roman 20 bold** | [01:47] | `\Large` ≈ **17.3 pt** ❌ |
| Cover page | Has a **department standard** — do not invent one | [01:47] | template default |
| University logo | Recent years place it at the top | [02:22] | ✅ present |
| Title page numbering | Is page i, but **the number is not printed** | [02:55] | ✅ correct |
| Body | Times New Roman 12, 1.5 spacing, justified | [00:40], [01:16] | ✅ fixed in J1/J2 |

⚠️ **One open conflict, from task C8 and unresolved since 2026-07-28.** The faculty guidelines
say *"The Title page is considered to be page one… Roman numerals begin with the title"*, but
`1-main.tex:122` places `\pagenumbering{roman}` **after** the titlepage, so the Declaration
becomes **i** instead of **ii**. One-line fix, but it shifts every front-matter numeral.
**Fold this into J10 rather than leaving it open separately.**

---

## 4. Title — options to choose from

Derived from the thesis's own research question. **Only relevant if no title is registered (Q1).**

| # | Title | Character |
|---|---|---|
| A | *LLM-Based Query Enhancement for Arabic Information Retrieval* | Short, safe, but does not name the contribution |
| B | **Corpus-Steered Query Expansion for Arabic Information Retrieval in Hybrid Sparse–Dense Pipelines** | Names the actual contribution and the final system. **Recommended.** |
| C | *Query Enhancement for Arabic Retrieval-Augmented Generation: Blind and Corpus-Steered Expansion Across Sparse, Dense and Hybrid Retrievers* | Complete but long; will wrap to three lines at 20 pt |

**Why B:** it matches what Phase A rewrote the thesis to be about. A title that says only
"query enhancement" would repeat the pre-A1 framing the whole of Phase A removed, and C is
too long for a 20 pt cover line.

---

## 5. Declaration of Authorship — draft

No template exists in the faculty guidelines (their preliminary-pages list does not even
include this page — it is **Dr. Tahani's** requirement, from the C1 ordering). Standard form:

> I declare that this thesis, submitted in partial fulfilment of the requirements for the
> degree of Bachelor of Science in Electrical and Electronic Engineering, is my own work
> except where acknowledged. It contains no material previously published or written by
> another person, nor material which to a substantial extent has been accepted for the award
> of any other degree at the University of Khartoum or any other institution, except where
> due acknowledgement is made in the text. Any contribution made to this research by others
> is explicitly acknowledged.
>
> \vspace{1.5cm}
> Name: ………………………………  Signature: ………………………  Date: ………………
> Name: ………………………………  Signature: ………………………  Date: ………………

⚠️ **Two authors, so it needs two signature blocks.** ⚠️ **Confirm the department does not
have its own required wording** — this is generic, and a declaration is a formal statement.

---

## 6. Acknowledgments — skeleton

Optional per the faculty guidelines, but the page already exists in the ordering, so leaving
it blank is worse than removing it. **This must be written by Elhaj and Osman personally** —
a generated acknowledgement is the one page where that would be obvious. Suggested beats,
roughly half a page:

1. Dr. Tahani — supervision, and specifically the review that reshaped the thesis
2. The Department of Electrical and Electronic Engineering
3. Anyone who gave technical help or compute access
4. Family

---

## 7. Dedication — Osman (task C9)

Already assigned and deliberately deferred to the end. Personal; nothing to plan here.

---

## 8. Recommended order

1. **Answer Q1–Q5** (§2). Q1 and Q5 gate everything — a registered title or a coordinator
   template would override §3 and §4.
2. Fill the title page + fix the 20 pt title size + resolve the C8 roman-numeral conflict, in
   one edit.
3. Declaration — confirm wording, then apply.
4. Acknowledgments — Elhaj and Osman write it.
5. Dedication — Osman, last (C9).
6. Rebuild and confirm the front-matter numbering still runs i … xv without a gap.

**Page impact: zero.** Front matter does not count toward the 100-page core.
