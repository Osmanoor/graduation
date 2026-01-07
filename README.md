# Arabic RAG Query Enhancement - Graduation Project

**Project Title:** Improving Retrieval Recall in Arabic RAG Systems via Query Enhancement  
**Institution:** University of Khartoum, Faculty of Engineering  
**Team:** Mohammed Elhaj, Osman Bashir  
**Status:** Phase 1 - Active Investigation & Baseline Setup  
**Last Updated:** January 6, 2026

---

## 🎯 Project Overview

This graduation project focuses on improving the retrieval recall of Retrieval-Augmented Generation (RAG) systems for Arabic language through query enhancement techniques.

**Core Approach:** Apply query enhancement techniques to a simple RAG baseline and measure improvements in retrieval metrics.

**Important Note:** Our datasets (MIRACL, ARABICA) are MSA-only, so dialectical mismatch is not our primary focus. Our techniques may still help with dialects, but we cannot directly measure this.

---

## 📋 Quick Start Guide

### Essential Documents (Read in Order)
1. **`meetings/6.1.2026_meeting_outcomes.md`** - Latest decision clarifications (READ FIRST)
2. **`RESEARCH_CONTEXT_KERNEL.md.md`** - Project overview and current status
3. **`research_decisions/technical_specifications.md`** - System architecture and implementation
4. **`research_decisions/open_questions.md`** - What's still under investigation

### For Specific Information
- **What was decided vs. still open:** `meetings/6.1.2026_meeting_outcomes.md`
- **Dataset details:** `research_decisions/technical_specifications.md`
- **Expert consultation:** `meetings/Consultation with Mohammed Rashad.md`
- **Full meeting transcriptions:** `meetings/6.1.2026.md`, `meetings/2.1.2026.md`

---

## 🏗️ System Architecture

```
User Query (Arabic)
    ↓
[Query Enhancement Layer] ← Our Focus
    ↓
[Retriever: Dense OR BM25 (tested separately)]
    ↓
Retrieved Chunks (Top-10)
    ↓
[Evaluation: Recall@10, NDCG@10, MRR]
```

**Key Change (6/1/2026):** Test Dense and BM25 separately, not just Hybrid. This gives more insight into where improvements come from.

---

## 📊 Decision Status Summary

| Decision | Status | Notes |
|----------|--------|-------|
| **Approach** | ✅ Confirmed | Technology-oriented |
| **Dataset** | ✅ Confirmed | MIRACL (~95% confidence) |
| **Baseline** | ✅ Confirmed | Test Dense, BM25 separately |
| **Metrics** | ✅ Confirmed | Recall@10, NDCG@10, MRR |
| **Timeline** | ✅ Confirmed | ~6 weeks (optimistic) |
| **Embedding Model** | ⏳ Under Investigation | Open Source vs Closed Source tradeoff |
| **First Technique** | ⏳ Under Investigation | Decide after baseline |
| **Secondary Dataset** | ⏳ Potential | ARABICA for long-term only |

---

## 📅 Timeline

**Total:** ~6 weeks (January 6 - February 15, 2026)  
**Note:** Acknowledged as "optimistic"

| Phase | Goal | Timeline |
|-------|------|----------|
| **Baseline** | Dense + BM25 setup | Weeks 1-3 |
| **Enhancement** | First technique | Weeks 4-5 |
| **Analysis** | Documentation | Week 6 |

---

## ⚠️ Key Challenges

1. **Scale:** MIRACL = 2.1M passages (~50GB storage)
2. **Dialectical:** Both datasets are MSA-only
3. **Iteration Speed:** Open Source embedding = slow; Closed Source = costs
4. **Timeline:** 6 weeks is optimistic

---

## 📁 Repository Structure

```
arabic-rag-query-enhancement/
├── RESEARCH_CONTEXT_KERNEL.md.md    # Project overview and status
├── QUICK_REFERENCE.md               # One-page quick reference
├── README.md                         # This file
├── meetings/
│   ├── 6.1.2026.md                  # Decision review meeting (3 parts)
│   ├── 6.1.2026_meeting_outcomes.md # Latest decision clarifications
│   ├── 2.1.2026.md                  # Planning meeting (4 parts)
│   ├── 2.1.2026_meeting_outcomes.md # Original outcomes
│   └── Consultation with Mohammed Rashad.md
├── research_decisions/
│   ├── technical_specifications.md  # Architecture & implementation
│   ├── open_questions.md            # What's still under investigation
│   └── AI_ASSUMED_DECISIONS_REVIEW.md # What AI got wrong (reviewed)
├── papers/
│   └── [paper summaries]
├── gemini_opinions/
│   └── [strategic discussions]
└── University_of_Khartoum__EEE_bachelor_s_thesis_template/
    └── [thesis template files]
```

---

## 📞 For AI Agents

**Before making suggestions:**
1. Read `meetings/6.1.2026_meeting_outcomes.md` FIRST
2. Check what's "Under Investigation" vs "Confirmed"
3. Don't assume - we've documented our uncertainty!
4. Mark AI suggestions clearly as suggestions, not decisions

**Key Principle:** We are in "active investigation" mode, not "blind implementation" mode.

---

## 👥 Team

- **Mohammed Elhaj** - Project lead, implementation
- **Osman Bashir** - Research, dataset analysis, implementation

---

**Last Updated:** January 6, 2026  
**Next Update:** After baseline implementation
