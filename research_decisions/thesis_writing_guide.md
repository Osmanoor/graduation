# Thesis Writing Guide — Dr. Tahani's Supervisory Guidelines
**Source:** Supervisor meeting on 17 March 2026 (full transcription in `meetings/17.3.2026.md`)
**Purpose:** Comprehensive reference for writing the thesis. This file captures ALL advice Dr. Tahani gave so that no one needs to re-read the meeting transcription.

---

## 1. Overall Thesis Structure

The thesis has a **core body** (Chapters 1–5), preceded by **front matter** and followed by **references** and **appendices**.

### Writing Order (CRITICAL)
Do NOT write chapters in numerical order. The recommended sequence is:

1. **Chapter 2** (Literature Review & Background) — write first
2. **Chapter 3** (Methodology) — write in parallel with Chapter 4
3. **Chapter 4** (Results & Discussion) — write in zigzag with Chapter 3
4. **Chapter 1** (Introduction) — write AFTER 2, 3, 4
5. **Chapter 5** (Conclusion) — write AFTER 2, 3, 4
6. **Abstract & المستخلص** — write last (summarizes everything)
7. **Front matter** — Table of Contents, Lists, etc. (generated last)

---

## 2. Chapter-by-Chapter Guidelines

### Chapter 1: Introduction
- **Write this AFTER Chapters 2, 3, and 4** — it should read like the Proposal but written by people who now deeply understand the work.
- **Structure:**
  - 1.1 General Introduction / Preamble — a general entry into the topic area, explain the problem in broad terms
  - 1.2 Problem Definition — clear statement of the research problem
  - 1.3 Objectives — **MUST match what was actually implemented in the Methodology**. It's OK to diverge from the original Proposal, but the final thesis objectives must align with what you actually did.
  - 1.4 Thesis Layout / Organization of the Thesis — brief summary of each chapter ("Chapter 1 contains..., Chapter 2 covers..., Chapter 3 describes..., etc.")
- **Do NOT include:** Methodology details, results, or expected results — those belong in later chapters
- **References:** Chapter 1 typically has NO references (it's your own framing and problem statement)
- **Key principle from Dr. Tahani:** "You cannot write objectives and then have done something different in the methodology"

### Chapter 2: Literature Review & Theoretical Background
- **This is the thickest chapter.** It is NOT just a list of published papers.
- **Content includes:**
  1. **Theoretical background & definitions:** LLMs, RAG systems, Query Enhancement, BM25 algorithm, Dense Retrieval, vector similarity, embedding models — any concept the reader needs to understand your work
  2. **Mathematical models:** BM25 scoring formula, cosine similarity, NDCG/MRR/Recall equations, any relevant mathematical formulations
  3. **Description of ALL models used in experiments:** Falcon-H1, Jais-2, Qwen (all versions), ALLaM, Aya, Gemma, SILMA, GPT-OSS — each model must be described HERE in Chapter 2
  4. **Related Work / Literature Review subtitle:** Published papers you reviewed (the 20+ papers). This is a *subtitle* within Chapter 2, not the entire chapter
- **Key rule from Dr. Tahani:** "When you come to Chapter 3 (Methodology), you do NOT re-explain models or concepts. You just reference them by their Chapter 2 subtitle number." For example: "As described in Section 2.3.4, Jais-2 is an Arabic-specialized model..." — you never re-describe what Jais-2 is in Chapter 3.
- **This includes even models that failed** — ALLaM and GPT-OSS must be described in Chapter 2 even though they were dropped

### Chapter 3: Methodology (MOST IMPORTANT CHAPTER)
- **Dr. Tahani emphasized:** "This is your real research — everything you actually did belongs here"
- **Content includes:**
  - Dataset description (MIRACL Arabic)
  - Baseline implementation approach (BM25S, mDPR)
  - Error analysis methodology
  - Query2Doc technique and your modifications (zero-shot vs few-shot, temperature tuning, etc.)
  - Model comparison experimental setup and configuration
  - Expanded experiment methodology (chunking-aware QE, etc.)
  - **ALL experiment setup details:** hardware (Colab, GPU type), hyperparameters, quantization settings, prompts used
  - Even minor work or work that led to negative results — "even if it's something very minor, as long as it's YOUR work and you got a result, even a negative one, you write it"
- **Use flowcharts and processing diagrams** — these are critical for explaining the process regardless of programming language
- **NO code in the thesis body** — code goes in the Appendix only
- **Zigzag writing with Chapter 4:** Section 3.1 (methodology step) → results of that step go in 4.1. Section 3.2 (next step) → results in 4.2. And so on. The reader alternates between what you did and what happened.

### Chapter 4: Results and Discussion
- **Content includes:**
  - ALL results: tables, figures, comparison charts, leaderboards
  - Engineering analysis of each result — not just "here are the numbers" but WHY, what it means
  - Discussion: "This is the best model because...", "We dropped this model because...", "When compared against baseline X, model Y showed..."
  - Conclusions within each section (not just at the end)
  - Comparison with original paper results (e.g., our zero-shot Arabic results vs. Query2Doc paper's few-shot English results)
- **Written in zigzag with Chapter 3** — each methodology section maps to a results section
- **Dr. Tahani's advice:** "The same explanation you gave in the presentation — translate it into scientific engineering language with proper analysis for every result you reached"
- **Experiment setup/configuration goes in Chapter 3, NOT here** — Chapter 4 is purely results, analysis, and discussion

### Chapter 5: Conclusion and Recommendations
- **Write this AFTER Chapters 2, 3, and 4**
- **Content includes:**
  - Comments and overall conclusions — summary of what you achieved
  - Challenges you faced (models you couldn't test, resource limitations, time constraints)
  - **Recommendations for future work** — this is very important because you are the domain experts. Future students may continue from your suggestions
- **Dr. Tahani's emphasis:** "Your recommendations are very important because you are the people who went deepest into this topic and worked on it in the most detailed way"

---

## 3. Front Matter (Before Chapter 1)

These pages appear before Chapter 1 and are numbered in **Roman numerals** (I, II, III, IV...). The cover page does NOT show page numbering.

### Required Pages (in order):
1. **Cover page** — project name, student names, student IDs, supervisor name, year. Must follow university guidelines exactly. Dr. Tahani: "If basic information is missing or incomplete, the examiner immediately gets the impression of carelessness"
2. **Declaration of Authorship** (if required by template)
3. **Dedication** (optional)
4. **Acknowledgements** (optional)
5. **Abstract** (English) — see Section 4 below
6. **المستخلص** (Arabic abstract) — direct translation of the English abstract
7. **Table of Contents** — with page numbers
8. **List of Figures** — with page numbers
9. **List of Tables** — with page numbers
10. **List of Abbreviations** — sorted alphabetically

Total: approximately 10 pages of front matter.

---

## 4. Abstract Writing

The Abstract is the **first thing the examiner reads** after the cover page.

### Structure (all can be continuous paragraphs, no headings needed):
1. **Introductory sentence** (1–2 lines) — a gateway sentence that tells the reader what area you're working in (e.g., "Retrieval-Augmented Generation systems for Arabic...")
2. **Problem statement** — brief description of the problem
3. **Objectives** — what you set out to achieve
4. **Methodology** — what approach you used
5. **Results** — key findings
6. **Conclusion** — main takeaway

### Formatting:
- **~300–350 words** (should fill approximately 3/4 of a page)
- 12pt Times New Roman, 1.5 line spacing
- Dr. Tahani: "With one glance I can tell if the abstract is comprehensive or not — it should be about 3/4 of a page, not more than a page, not less than half"
- The Arabic المستخلص is a faithful translation of the English Abstract

---

## 5. Formatting Standards

### Body Text
- **Font:** 12pt Times New Roman
- **Line spacing:** 1.5
- **Alignment:** Justified (both margins)
- **Writing voice:** Passive voice throughout ("The experiment was conducted..." not "We conducted...")

### Headings and Subtitles
- Every subtitle MUST have a number: 1.1, 1.2, 2.1, 2.2, 2.2.1, 2.2.2, etc.
- Numbering is hierarchical by chapter

### References (IEEE Format)
- **Numbering:** By order of appearance in the thesis, NOT by importance
- **In-text citation:** Square brackets — [1], [2], etc. — placed BEFORE the full stop of the sentence
- **Format:** "As shown in [1]." (bracket, then full stop)
- **Reference list:** Appears after Chapter 5, formatted according to IEEE standards:
  - Journal papers, conference papers, textbooks, websites — each has a specific IEEE format
  - Websites must include "Accessed on [date]"
- **Consistency:** Reference [1] in the text must be reference [1] in the reference list — the examiner WILL cross-check

### Figures
- **Numbering:** By chapter — Figure 2.1 (first figure in Chapter 2), Figure 4.3 (third figure in Chapter 4)
- **Caption:** Below the figure, with a descriptive name (not just "Flowchart" — must be self-explanatory)
- **In-text reference:** "As shown in Figure 2.1" — capital "F" for Figure
- **All figures** must be referenced in the text AND listed in the List of Figures

### Tables
- **Numbering:** By chapter — Table 2.1, Table 4.2, etc. (separate numbering from figures)
- **Caption:** ABOVE the table (unlike figures which are below)
- **In-text reference:** Same style as figures
- **All tables** must be referenced in the text AND listed in the List of Tables

### Abbreviations
- **First occurrence:** Write the full name followed by the abbreviation in parentheses — "Retrieval-Augmented Generation (RAG)"
- **Subsequent occurrences:** Just use the abbreviation — "RAG"
- **Capital letters:** The letters that form the abbreviation should be capitalized in the full form
- **List of Abbreviations:** In front matter, sorted alphabetically

### Appendices
- **Numbering:** Separate from thesis body — A1, A2, A3 for Appendix A; B1, B2, B3 for Appendix B
- **Appendix A:** Code listings (ALL code goes here, never in the thesis body)
- **Appendix B:** Additional derivations, equations, supplementary material that's useful but not core
- Use appendices for anything the reader might need but that would break the flow of the main chapters

---

## 6. Documentation Quality

### Dr. Tahani's Warning (verbatim sentiment):
> "Students sometimes do excellent work in experiments and coding but fail in documentation. This is very dangerous because documentation is worth approximately **15% of the grade**. The examiner's first impression upon seeing the thesis — if the documentation is careless, the immediate thought is 'these students don't follow standards,' and that creates a negative impression even if the practical work was excellent."

### Key Points:
- **Sequence and flow** are critical — the thesis should read logically from start to finish
- **Consistency** in formatting, numbering, and referencing throughout
- First impressions matter enormously — cover page, abstract, and table of contents set the tone
- An examiner reads: Abstract → Chapter 1 → sometimes jumps to Conclusion → then reads everything

---

## 7. Presentation Guidelines

### Format (subject to change based on university decision):
- **10-minute recorded video** — may change to in-person defense depending on circumstances
- PowerPoint or Prezi presentation
- Uploaded along with the thesis document

### Structure:
- **Split:** 5 minutes per student — one student does the first half, the other does the second half
- **DO NOT** alternate frequently between presenters (Dr. Tahani: "Constant switching is very annoying for the examiner")
- Keep the flow smooth and uninterrupted

### Demo:
- Can include a demo of the best model/result
- Options:
  1. Embed as a video clip within the presentation (preferred — keeps it smooth)
  2. Hyperlink at the end (less preferred — can break flow)
- **Do NOT** break the presentation flow to open external links mid-presentation
- If recorded, make the demo a seamless part of the recording

### Rehearsal:
- Dr. Tahani will conduct a rehearsal/practice run before the final recording
- Record the presentation AFTER exams (not before)

---

## 8. Publication

### Dr. Tahani's Encouragement:
- "If you feel there's a real contribution, you can publish a paper — this significantly strengthens your position"
- "Having a published paper, even at the faculty journal level, is a very strong point"

### Publishing Options (easiest to hardest):
1. **Pre-print** (e.g., arXiv) — ~3 pages, fastest, published online immediately if contribution is real
2. **Faculty of Engineering journal** (University of Khartoum) — familiar standards, easier review process
3. **Engineering Society journal** — regional, still accessible
4. **Regional/International conferences or journals** — highest impact but longer review

### Urgency:
- "LLM research is moving very fast — publish your results as soon as possible before others working on the same area overtake you"
- "This is a hot topic and everyone is working on it"

---

## 9. Timeline (from 17 March 2026 meeting)

| Milestone | Target Date | Notes |
|-----------|------------|-------|
| Thesis first draft ready | Mid-April 2026 | Chapters 2, 3, 4 complete; Ch 1 & 5 drafted |
| Presentation ready | Mid-April 2026 | PowerPoint/Prezi prepared (not yet recorded) |
| Expanded experiments done | Mid-April 2026 | All practical work finished |
| Exams period | May 2026 | No project work — focus on coursework |
| Record presentation | After last exam | ~1 week window |
| Project submission | 1 week after last exam | Thesis + video + presentation files |

### Dr. Tahani's Advice:
- "I don't want you to rush during that final week — the thesis should already be ready, the presentation written and reviewed. Only the recording should be left for after exams."
- "I want good grades in ALL courses, not just the project — dedicate May entirely to exam preparation"

---

## 10. Examiner's Perspective (What Dr. Tahani Looks For)

Dr. Tahani shared her personal evaluation process as an examiner:

1. **First:** Reads the Abstract — checks if it comprehensively summarizes the entire project
2. **Second:** Checks Chapter 1 — problem clearly stated? Objectives clear? Thesis layout present?
3. **Sometimes:** Jumps to Chapter 5 (Conclusion) to get the full picture
4. **Then:** Reads the full thesis from beginning to end
5. **Cross-checks:** Reference numbers in text match reference list; figures/tables are properly numbered and captioned
6. **Impression factors:**
   - Is the cover page complete and accurate?
   - Is the abstract the right length (~3/4 page)?
   - Are all sections properly numbered?
   - Is the formatting consistent throughout?
   - Do references follow IEEE format?

---

## 11. Defense Format (Uncertain — Depends on University)

- Previous years: recorded video submission (due to war/displacement)
- This year: university announced in-person exams — defense format TBD
- Possibility: in-person defense (would require different preparation)
- Possibility: teacher strike after Eid (would delay everything)
- Dr. Tahani: "We prepare for all scenarios and be ready early so we're not rushed at the end"

---

## 12. Checklist Before Submission

### Front Matter
- [ ] Cover page with all required information (per university guidelines)
- [ ] Abstract (~300-350 words, ~3/4 page)
- [ ] المستخلص (Arabic translation of abstract)
- [ ] Table of Contents with page numbers
- [ ] List of Figures with page numbers
- [ ] List of Tables with page numbers
- [ ] List of Abbreviations (alphabetically sorted)
- [ ] Roman numeral page numbering (I, II, III...)

### Chapter 1
- [ ] General introduction / preamble
- [ ] Problem definition
- [ ] Objectives (matching actual methodology)
- [ ] Thesis layout / organization summary
- [ ] No references needed (typically)

### Chapter 2
- [ ] Theoretical background and definitions (LLM, RAG, QE, BM25, Dense, etc.)
- [ ] Mathematical models and equations
- [ ] Description of ALL models used (including dropped ones)
- [ ] Related work / literature review of published papers
- [ ] Proper IEEE references throughout

### Chapter 3
- [ ] Complete methodology with all steps
- [ ] Experiment setup and configuration details
- [ ] Flowcharts and processing diagrams (NO code)
- [ ] Every piece of work documented (even negative results)
- [ ] Zigzag structure mapping to Chapter 4 sections

### Chapter 4
- [ ] Results for every methodology section (zigzag with Ch. 3)
- [ ] Figures and tables properly numbered and captioned
- [ ] Engineering analysis and discussion for each result
- [ ] Model comparisons with clear conclusions
- [ ] Best/worst model identified with justification

### Chapter 5
- [ ] Overall conclusions
- [ ] Challenges encountered
- [ ] Recommendations for future work
- [ ] Clear and useful for future researchers

### References
- [ ] IEEE format
- [ ] Numbered by order of appearance
- [ ] Every in-text citation has a corresponding entry
- [ ] Websites include "Accessed on [date]"

### Appendices
- [ ] Code listings (Appendix A)
- [ ] Additional derivations/supplementary material (Appendix B if needed)
- [ ] Separate numbering (A1, A2, B1, B2)

### Presentation
- [ ] PowerPoint/Prezi prepared
- [ ] ~10 minutes total (5 min per student)
- [ ] Demo included (as video clip, smooth integration)
- [ ] Rehearsal done with Dr. Tahani
- [ ] Final recording (after exams)
