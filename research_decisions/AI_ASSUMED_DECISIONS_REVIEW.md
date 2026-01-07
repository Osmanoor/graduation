# AI-Assumed Decisions - Review Complete
**Created:** January 2, 2026  
**Reviewed:** January 6, 2026 (3-part meeting)  
**Purpose:** Document decisions the AI made that were reviewed/revised  
**Status:** ✅ REVIEW COMPLETE - See `meetings/6.1.2026_meeting_outcomes.md`

---

## ✅ Review Summary

This document was reviewed in a 3-part meeting on January 6, 2026. The full meeting transcription is in `meetings/6.1.2026.md` and structured outcomes are in `meetings/6.1.2026_meeting_outcomes.md`.

**Key Outcomes:**
- Most architectural decisions were confirmed with nuances
- Baseline strategy changed: Test Dense and BM25 separately (not just Hybrid)
- Several items remain "Under Investigation"
- Documentation updated to reflect "active investigation" state

---

## Category 1: Architecture Decisions

### 1.1 Hybrid Retrieval (Dense + BM25)
**What I Documented:** "Decision: Implement hybrid retrieval as baseline" (marked as ✅ Finalized)
**Review Result:** 🔄 **REVISED** - Test all three separately

**Reality from Meeting:** You discussed hybrid as an option, but didn't explicitly finalize it

**Meeting Evidence:**
- Part 2, ~06:00: Osman suggests "ممكن تكون حاجة resource احسن برضو انو ممكن نشتغل بيهو" (BM25 as option)
- Part 2, ~12:31: Osman says "نجرب في ده ونجرب في ده" (test both)
- You discussed testing both separately AND together

**My Justification (Why I Assumed):**
- Multiple papers you reviewed use hybrid approaches
- Mohamed Rashad didn't object to hybrid
- It's a common baseline in RAG research
- Allows testing both sparse and dense independently

**Actual Status:** Should be "Under Investigation - Leaning toward Hybrid"

**Questions for You:**
1. Do you want to commit to hybrid now, or test Dense-only first?
2. Should baseline be: (a) Dense only, (b) BM25 only, (c) Hybrid, or (d) Test all three?

---

### 1.2 Embedding Model Selection
**What I Documented:** "BGE-m3, Jina AI, or Qwen - selection in progress" (marked as ⏳)

**Reality from Meeting:** You mentioned these as candidates but didn't commit to testing all three

**Meeting Evidence:**
- Part 2, ~01:08: Mohammed mentions BGE, Jina AI, Qwen as options
- Part 2, ~21:49: Osman asks "الـ Embedding Model مش حنستخدم أحسن واحد؟"
- No explicit decision on which to test or how many

**My Justification (Why I Listed These):**
- These are the most commonly mentioned in your discussions
- They appear in your technical notes
- They're multilingual and support Arabic

**Actual Status:** Should be "Candidates Identified - Selection Method Not Decided"

**Questions for You:**
1. Will you test all three, or pick one based on benchmarks?
2. Do you want to add/remove any candidates?
3. What's the selection criteria priority: (a) Performance, (b) Cost, (c) Open-source, (d) All equally?

---

### 1.3 Evaluation Metrics
**What I Documented:** "Recall@10, NDCG@10, MRR" (marked as ✅ Finalized)

**Reality from Meeting:** You discussed Recall@10 and NDCG@10, but MRR wasn't explicitly mentioned

**Meeting Evidence:**
- Part 2, ~22:28: Mohammed mentions "Recall@10" and "NDCG@10"
- MRR was not discussed in the meeting transcription

**My Justification (Why I Added MRR):**
- It's a standard retrieval metric
- MIRACL benchmark uses it
- Complements Recall and NDCG

**Actual Status:** Should be "Recall@10 and NDCG@10 confirmed, MRR is AI suggestion"

**Questions for You:**
1. Do you want to include MRR, or stick to Recall@10 and NDCG@10 only?
2. Any other metrics you want to track?

---

## Category 2: Methodology Decisions

### 2.1 Technology-Oriented Approach
**What I Documented:** "Decision: Technology-oriented (apply techniques, discover problems)" with "⏳ Pending supervisor confirmation"

**Reality from Meeting:** This was discussed extensively but NOT finalized - you explicitly wanted supervisor input

**Meeting Evidence:**
- Part 2, ~25:46: Long discussion about Problem-oriented vs Tech-oriented
- Part 2, ~30:52: Osman says "كلامك منطقي والله" but no final decision
- Part 4, ~02:40: You explicitly ask "Question for Supervisor: Do you agree with this approach?"

**My Justification (Why I Leaned This Way):**
- You spent more time discussing tech-oriented benefits
- Mohamed Rashad's advice aligns with tech-oriented
- Safer with existing datasets

**Actual Status:** Should be "Under Active Discussion - Supervisor Input Required"

**Questions for You:**
1. Do you have a personal preference before the meeting?
2. What would make you choose problem-oriented instead?

---

### 2.2 First Query Enhancement Technique
**What I Documented:** "HyDE or Query Rewriting (to be decided after baseline)"

**Reality from Meeting:** You discussed multiple techniques but didn't narrow to these two

**Meeting Evidence:**
- Part 2, ~20:51: Mohammed discusses HyDE
- Part 2, ~05:02: Discussion of Query Rewriting for dialectical
- Part 2, ~06:43: Discussion of Query Expansion
- No explicit narrowing to just two options

**My Justification (Why I Narrowed):**
- HyDE is well-established and language-agnostic
- Query Rewriting directly addresses Arabic dialectical challenge
- Both were discussed more than others

**Actual Status:** Should be "Multiple Candidates - No Prioritization Yet"

**Questions for You:**
1. Do you want to narrow to HyDE and Query Rewriting, or keep all options open?
2. What criteria will you use to select the first technique?

---

## Category 3: Dataset Decisions

### 3.1 MIRACL as Primary Dataset
**What I Documented:** "Decision: MIRACL as primary dataset" (marked as ✅ Finalized)

**Reality from Meeting:** Strong consensus but you wanted to validate with supervisor

**Meeting Evidence:**
- Part 3, ~21:00: Strong discussion favoring MIRACL
- Part 4, ~02:03: Mohammed says "موافق على MIRACL"
- But Part 4, ~10:05: You still wanted supervisor input on dataset choice

**My Justification (Why I Marked Finalized):**
- Strongest consensus in the meeting
- Dataset analysis report strongly recommends it
- Mohamed Rashad's advice aligns with MIRACL's simplicity

**Actual Status:** Should be "Strong Consensus - Pending Supervisor Confirmation"

**Questions for You:**
1. Are you 95%+ confident in MIRACL, or still open to alternatives?
2. What would make you reconsider?

---

### 3.2 Arabic QA as Secondary Dataset
**What I Documented:** "Secondary Dataset: Arabic QA (90K questions with difficulty labels)"

**Reality from Meeting:** Mentioned as option but not committed

**Meeting Evidence:**
- Part 3, ~21:00: Discussed as having "Hard" labels
- Not explicitly chosen as "secondary dataset"

**My Justification (Why I Designated It):**
- It was discussed positively
- Complements MIRACL (MSA + difficulty labels)
- Useful for generalization testing

**Actual Status:** Should be "Candidate for Future Testing - Not Committed"

**Questions for You:**
1. Do you want to commit to Arabic QA as secondary now?
2. Or leave it as "potential future dataset"?

---

## Category 4: Scope Decisions

### 4.1 Deferring Generation Evaluation
**What I Documented:** "Decision to isolate retrieval (not full generation pipeline initially)"

**Reality from Meeting:** Discussed but not explicitly decided as a hard rule

**Meeting Evidence:**
- Part 2, ~22:28: Mohammed discusses focusing on retrieval metrics
- Part 2, ~23:03: Discussion about when to evaluate generation
- No explicit "we will NOT do generation in CP1" decision

**My Justification (Why I Assumed):**
- Retrieval-first is simpler and more focused
- Aligns with MIRACL's retrieval-focused nature
- Can add generation later

**Actual Status:** Should be "Likely Approach - Not Explicitly Decided"

**Questions for You:**
1. Do you want to explicitly defer generation to later checkpoints?
2. Or keep it as "we'll see after retrieval results"?

---

### 4.2 Dialectical Support Deferred
**What I Documented:** "Limitation: MSA-only (dialectical support deferred to later checkpoint)"

**Reality from Meeting:** Discussed as a challenge but no explicit deferral decision

**Meeting Evidence:**
- Part 2, ~20:51: Discussion of dialectical as challenge
- Part 2, ~28:13: Discussion of dialectical mismatch as problem
- Part 4, ~02:40: You ask supervisor about dialectical priority
- No explicit "we defer this" decision

**My Justification (Why I Assumed Deferral):**
- MIRACL is MSA-only
- Dialectical datasets are smaller/less standard
- Can be addressed in CP2 with Query Rewriting

**Actual Status:** Should be "Open Question - Supervisor Input Needed"

**Questions for You:**
1. Do you want to explicitly defer dialectical to CP2+?
2. Or try to address it in CP1 somehow?

---

## Category 5: Implementation Details

### 5.1 Checkpoint Timeline (2-3 weeks each)
**What I Documented:** "Checkpoint 1: 2-3 weeks"

**Reality from Meeting:** No explicit timeline discussed

**Meeting Evidence:**
- No specific timeline mentioned in meeting transcription

**My Justification (Why I Assumed):**
- Standard sprint length
- Allows for setup, experimentation, analysis
- Fits typical graduation project timeline

**Actual Status:** Should be "AI Estimate - Not Discussed"

**Questions for You:**
1. What's your actual timeline/deadline?
2. How much time do you have for CP1?

---

### 5.2 Versioning Strategy (v0.1, v0.2, etc.)
**What I Documented:** "Versioning: Arabic HyDE v0.1, v0.2, v0.3..."

**Reality from Meeting:** Mentioned once but not adopted as strategy

**Meeting Evidence:**
- Part 2, ~02:50: Mohammed mentions "version 0.1, 0.2" as example
- Not discussed as formal versioning strategy

**My Justification (Why I Formalized It):**
- Good practice for tracking experiments
- Helps with reproducibility
- Common in ML research

**Actual Status:** Should be "AI Suggestion - Not Discussed"

**Questions for You:**
1. Do you want to adopt this versioning scheme?
2. Or use a different experiment tracking method?

---

### 5.3 Code Structure Proposal
**What I Documented:** Detailed folder structure in technical_specifications.md

**Reality from Meeting:** Not discussed at all

**My Justification (Why I Created It):**
- Standard ML project structure
- Helps with organization
- Common best practice

**Actual Status:** Should be "AI Suggestion - Not Discussed"

**Questions for You:**
1. Do you want to use this structure?
2. Do you have your own preferred structure?

---

## Category 6: Chapter 2 Content Decisions

### 6.1 Section Structure
**What I Documented:** 6 main sections with specific subsections

**Reality from Meeting:** You had an initial draft outline but didn't finalize structure

**Meeting Evidence:**
- `chapter2_initial_draft.md` has a proposed structure
- Meeting discussed "refinements" but didn't specify what

**My Justification (Why I Used This Structure):**
- Based on your initial draft
- Follows standard literature review format
- Funnel approach (broad → narrow → gap)

**Actual Status:** Should be "Based on Draft - Needs Review"

**Questions for You:**
1. Is this structure what you wanted?
2. What "refinements" did you discuss in the meeting?

---

### 6.2 Depth of Coverage
**What I Documented:** Comprehensive coverage of each technique

**Reality from Meeting:** Not discussed

**My Justification (Why I Made It Comprehensive):**
- Standard thesis chapter length
- Shows breadth of literature review
- Establishes expertise

**Actual Status:** Should be "AI Judgment - May Need Adjustment"

**Questions for You:**
1. Is this too detailed or too brief?
2. Any sections you want expanded/condensed?

---

## Summary of AI Overreach

### Decisions I Should NOT Have Finalized:
1. ❌ Hybrid retrieval as definite baseline
2. ❌ Specific embedding model candidates
3. ❌ MRR as evaluation metric
4. ❌ Technology-oriented approach (pending supervisor)
5. ❌ HyDE/Query Rewriting as only first technique options
6. ❌ Arabic QA as committed secondary dataset
7. ❌ Explicit deferral of generation evaluation
8. ❌ Explicit deferral of dialectical support
9. ❌ 2-3 week checkpoint timelines
10. ❌ Versioning strategy
11. ❌ Code structure
12. ❌ Chapter 2 structure without your review

### What I Should Have Done Instead:
- Mark everything as "Under Investigation" unless you explicitly said "we decided"
- Use language like "Leaning toward" or "Considering" instead of "Decision"
- Clearly separate "Discussed Options" from "Finalized Decisions"
- Ask clarifying questions before assuming

---

## Recommended Actions

### For You:
1. Review each item above
2. Mark as: ✅ Approve / ⏳ Keep Pending / ❌ Reject / 🔄 Revise
3. I'll update all documents based on your feedback

### For Me (Future):
1. Be more conservative with "finalized" status
2. Distinguish between "strong consensus" and "decided"
3. Mark AI suggestions clearly as such
4. Ask before assuming

---

## Questions for Immediate Clarification

**High Priority (Affects Today's Meeting):**
1. MIRACL as primary dataset - Finalize or keep pending?
2. Technology-oriented approach - Your preference before supervisor input?
3. Dialectical support - Address in CP1 or defer?

**Medium Priority (Affects This Week):**
4. Hybrid vs. Dense-only vs. BM25-only baseline?
5. Which embedding models to test?
6. First query enhancement technique selection criteria?

**Low Priority (Can Decide Later):**
7. Versioning strategy?
8. Code structure?
9. Chapter 2 refinements?

---

**Status:** ⚠️ REQUIRES HUMAN REVIEW  
**Next Step:** Your approval/revision of each item  
**Then:** I'll update all generated documents to reflect actual status
