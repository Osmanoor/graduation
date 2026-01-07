# Quick Reference Card
**Project:** Arabic RAG Query Enhancement  
**Last Updated:** January 7, 2026

---

## 📚 Start Here (Read Order)

1. `RESEARCH_CONTEXT_KERNEL.md.md` - Project overview & decisions
2. `meetings/6.1.2026_meeting_outcomes.md` - Latest decision status
3. `TASKS.md` - **Current task list with assignments**
4. `WORKFLOW.md` - **How we work with Kiro**

---

## 🎯 Core Decisions (Confirmed)

| Decision | Choice | Status |
|----------|--------|--------|
| **Approach** | Technology-oriented | ✅ Confirmed |
| **Dataset** | MIRACL (Arabic) | ✅ Confirmed (~95% confidence) |
| **Secondary Dataset** | ARABICA | ⏳ Potential/Long-term only |
| **Baseline** | Test Dense, BM25, (Hybrid) separately | ✅ Confirmed |
| **Embedding Model** | BGE-m3/E5 vs Jina | ⏳ Under Investigation |
| **First Technique** | TBD after baseline | ⏳ Under Investigation |
| **Evaluation** | Recall@10, NDCG@10, MRR | ✅ Confirmed |
| **Timeline** | ~6 weeks (until Feb 15) | ✅ Confirmed (optimistic) |

---

## 📁 Essential Documents (Read Order)

1. **`meetings/6.1.2026_meeting_outcomes.md`** - Latest decision clarifications (READ FIRST)
2. **`RESEARCH_CONTEXT_KERNEL.md.md`** - Project overview & current status
3. **`research_decisions/technical_specifications.md`** - Implementation details
4. **`research_decisions/open_questions.md`** - What needs to be decided

---

## 🏗️ System Architecture (One-Liner)

```
Query → [Enhancement Layer] → [Dense OR BM25] → Top-10 Chunks → Evaluate
```

**Our Focus:** The Enhancement Layer  
**Baseline:** Test Dense and BM25 separately (not just Hybrid)

---

## 📊 Project Timeline

| Phase | Goal | Timeline | Status |
|-------|------|----------|--------|
| **Baseline** | Dense + BM25 setup | Weeks 1-3 | 🔄 Current |
| **Enhancement** | First technique | Weeks 4-5 | ⏳ Next |
| **Analysis** | Documentation | Week 6 | ⏳ Future |

**Deadline:** February 15, 2026 (before Ramadan)

---

## ⏳ What's Still Under Investigation

1. **Embedding Model** - Open Source (BGE-m3, E5) vs Closed Source (Jina)
   - Tradeoff: Free but slow vs Fast but costs
2. **First Technique** - Decide after baseline analysis
3. **Hierarchical Structures** - Needs feasibility study
4. **Arabic LLMs** - Current suggestions weak, need research

---

## 🎓 Query Enhancement Techniques (Candidates)

1. **HyDE** - Generate hypothetical document, use for retrieval
2. **Query Rewriting** - Normalize/improve query
3. **Query Expansion** - Add synonyms, handle morphology
4. **Query Decomposition** - Break complex queries into sub-queries

**Selection:** After baseline is established and errors analyzed

---

## 📅 This Week's Tasks

- [x] Update documentation to reflect actual decisions
- [ ] Research embedding model costs/performance
- [ ] Prepare task list for parallel work
- [ ] Download MIRACL dataset
- [ ] Set up development environment

---

## ⚠️ Key Challenges

1. **Scale:** MIRACL = 2.1M passages (~50GB storage)
2. **Dialectical:** Both datasets are MSA-only (can't test dialects directly)
3. **Iteration Speed:** Open Source embedding = slow; Closed Source = costs
4. **Timeline:** 6 weeks is optimistic

**Mitigations:**
- Google Drive Pro (2TB) for storage
- Google Colab Pro for GPU
- Smaller subsets for prototyping

---

## 📝 Key Insights from 6/1/2026 Meeting

1. Test Dense and BM25 **separately** (not just Hybrid)
2. Dialectical is NOT primary focus (datasets are MSA)
3. Documentation is **critical** - every experiment fully documented
4. Timeline is "optimistic" - be realistic
5. Embedding model decision is a side task, don't block main work

---

## 📞 For AI Agents

**Before making suggestions:**
1. Read `meetings/6.1.2026_meeting_outcomes.md` FIRST
2. Check what's "Under Investigation" vs "Confirmed"
3. Don't assume - we've documented our uncertainty!
4. Mark AI suggestions clearly as suggestions, not decisions

**Key Principle:** We are in "active investigation" mode, not "blind implementation" mode.

---

## 🔗 Quick Links

- **Latest Decisions:** `meetings/6.1.2026_meeting_outcomes.md`
- **Full Meeting (6/1):** `meetings/6.1.2026.md`
- **Technical Specs:** `research_decisions/technical_specifications.md`
- **Open Questions:** `research_decisions/open_questions.md`
- **AI Assumptions Review:** `research_decisions/AI_ASSUMED_DECISIONS_REVIEW.md`

---

**Status:** ✅ Updated after 6/1/2026 review meeting  
**Next Milestone:** Baseline implementation (Weeks 1-3)  
**Last Updated:** January 6, 2026
