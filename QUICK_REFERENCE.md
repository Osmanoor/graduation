# Quick Reference Card
**Project:** Arabic RAG Query Enhancement  
**Last Updated:** January 2, 2026

---

## 🎯 Core Decision Summary

| Decision | Choice | Status |
|----------|--------|--------|
| **Approach** | Technology-oriented | ⏳ Pending supervisor confirmation |
| **Dataset** | MIRACL (Arabic) | ✅ Finalized |
| **Architecture** | Simple baseline + query enhancement | ✅ Finalized |
| **Retriever** | Hybrid (Dense + BM25) | ✅ Finalized |
| **Embedding Model** | BGE-m3 / Jina AI / Qwen | ⏳ Selection in progress |
| **First Technique** | HyDE or Query Rewriting | ⏳ After baseline |
| **Evaluation** | Recall@10, NDCG@10 | ✅ Finalized |

---

## 📁 Essential Documents (Read These First)

1. **`RESEARCH_CONTEXT_KERNEL.md.md`** - Project overview & current status
2. **`meetings/2.1.2026_meeting_outcomes.md`** - All decisions from planning meeting
3. **`research_decisions/technical_specifications.md`** - Implementation details
4. **`research_decisions/open_questions.md`** - What needs to be decided

---

## 🏗️ System Architecture (One-Liner)

```
Query → [Enhancement Layer] → [Dense + BM25] → Top-10 Chunks → Evaluate
```

**Our Focus:** The Enhancement Layer

---

## 📊 Project Checkpoints

| Checkpoint | Goal | Timeline | Status |
|------------|------|----------|--------|
| **CP1** | Proof of Concept | 2-3 weeks | 🔄 Current |
| **CP2** | Technique Iteration | 2-3 weeks | ⏳ Next |
| **CP3** | Model Generalization | 2-3 weeks | ⏳ Future |
| **CP4** | Benchmarking | Optional | ⏳ Future |

---

## 🎓 Query Enhancement Techniques

1. **HyDE** - Generate hypothetical document, use for retrieval
2. **Query Rewriting** - Transform dialect → MSA
3. **Query Expansion** - Add synonyms, handle morphology
4. **Query Decomposition** - Break complex queries into sub-queries

**First to implement:** HyDE or Query Rewriting (TBD)

---

## 📅 This Week's Tasks

- [ ] Finalize embedding model (BGE-m3 / Jina AI / Qwen)
- [ ] Download & preprocess MIRACL dataset
- [ ] Implement baseline RAG (Dense + BM25)
- [ ] Set up evaluation pipeline
- [ ] Document baseline performance

---

## ❓ Questions for Supervisor (Today)

1. Technology-oriented vs. Problem-oriented approach?
2. Retrieval-only scope acceptable?
3. Dialectical support: now or later?
4. Expected contribution level?
5. Key deadlines and milestones?
6. Resource recommendations?

---

## 📝 Today's Deliverables

- [x] Meeting outcomes documented
- [x] Technical specifications written
- [x] Open questions cataloged
- [x] Chapter 2 generated (LaTeX)
- [x] Presentation slides created (LaTeX)
- [ ] Supervisor meeting completed
- [ ] Feedback integrated

---

## 🔗 Quick Links

- **Full Meeting Transcription:** `meetings/2.1.2026.md`
- **Expert Consultation:** `meetings/Consultation with Mohammed Rashad.md`
- **Chapter 2:** `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter2_generated.tex`
- **Presentation:** `presentations/supervisor_meeting_2jan2026.tex`
- **Generation Summary:** `meetings/GENERATION_SUMMARY.md`

---

## 🚀 Compilation Quick Commands

### Presentation
```bash
cd presentations
pdflatex supervisor_meeting_2jan2026.tex
```

### Chapter 2 (Full Thesis)
```bash
cd University_of_Khartoum__EEE_bachelor_s_thesis_template
pdflatex 1-main.tex
bibtex 1-main
pdflatex 1-main.tex
pdflatex 1-main.tex
```

---

## 💡 Key Insights

1. **Simplicity wins:** Simple baseline + one layer beats complex architectures
2. **Scale through experiments:** More experiments = more contribution
3. **MIRACL is gold standard:** Best retrieval-focused Arabic dataset
4. **Checkpoints provide flexibility:** Can stop at any checkpoint with valid contribution
5. **Documentation is critical:** Everything is documented for reproducibility

---

## ⚠️ Known Challenges

1. **Dialectical gap:** MIRACL is MSA-only
2. **Evaluation granularity:** Need to understand *what* improved
3. **Resource constraints:** Limited GPU, API costs, time
4. **Contribution clarity:** Will clarify after CP1 results

---

## 📞 For AI Agents

**Before making suggestions:**
1. Check `RESEARCH_CONTEXT_KERNEL.md.md` for current status
2. Check `meetings/2.1.2026_meeting_outcomes.md` for decisions
3. Check `research_decisions/open_questions.md` for pending items
4. Don't assume - we've documented everything!

---

**Status:** ✅ Ready for supervisor meeting  
**Next Milestone:** Checkpoint 1 completion (2-3 weeks)  
**Last Updated:** January 2, 2026
