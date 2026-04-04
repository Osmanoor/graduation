# CSQE Parameter Verification

**Date:** April 4, 2026  
**Paper:** arXiv:2402.18031 (Lei et al., EACL 2024)  
**Status:** ✅ VERIFIED

---

## Parameters Claimed in Deep Research

From `mufti_approach_deep_research.md`:
- K=10 (top-K retrieved documents)
- 2+2 scheme (2 KEQE + 2 corpus-originated expansions)
- 128 tokens (document truncation)
- temp=1.0 (sampling temperature)

---

## Verification from Full Paper

### 1. K=10 (Top-K Documents) ✅ CONFIRMED

**Quote from Section 3.1 (Implementation):**
> "CSQE utilizes the top-10 retrieved documents, with each truncated to at most 128 tokens, excluding the Arguana dataset where we keep the top-3 documents due to its lengthy passages."

**Verification:** K=10 is correct for all datasets except Arguana (K=3).

---

### 2. 2+2 Scheme (Sampling Strategy) ✅ CONFIRMED

**Quote from Section 2 (Method):**
> "To increase diversity, we sample N generations from the LLM for expansion. For KEQE, N=5. As CSQE involves both KEQE and corpus-originated expansions, we sample N=2 for both KEQE and corpus-originated expansions, in total only 4 generations for fair comparison."

**Quote from Section 3.1 (Implementation):**
> "For KEQE, N=5. As CSQE involves both KEQE and corpus-originated expansions, we sample N=2 for both KEQE and corpus-originated expansions, making only 4 generations total for fair comparison."

**Verification:** 2+2 scheme is correct (2 KEQE + 2 corpus-originated = 4 total).

---

### 3. 128 Tokens (Document Truncation) ✅ CONFIRMED

**Quote from Section 3.1 (Implementation):**
> "CSQE utilizes the top-10 retrieved documents, with each truncated to at most 128 tokens"

**Verification:** 128-token truncation is correct.

---

### 4. Temperature=1.0 ✅ CONFIRMED

**Quote from Section 3.1 (Implementation):**
> "We sample from the LLM with a temperature of 1.0."

**Verification:** Temperature=1.0 is correct.

---

## Additional Implementation Details Extracted

### LLM Used
- **Model:** GPT-3.5-Turbo-0301
- **Note:** Paper states "updating HyDE's LLM from Text-Davinci-003 to GPT-3.5-Turbo cannot improve results"

### BM25 Configuration
- **Tool:** Pyserini
- **Parameters:** Default hyper-parameters (k1=0.9, b=0.4 typically)

### Query Repetition
**Quote from Section 2:**
> "We repeat the initial query q a number of times equal to the number of expansions during concatenation."

**Meaning:** If you have 4 expansions (2+2), the final query is:
```
q + q + q + q + expansion1 + expansion2 + expansion3 + expansion4
```

### Prompt Template (CSQE)
**Full prompt from Appendix A.1:**

```
Query: "how are some sharks warm blooded"
Retrieved documents:
1. Most sharks are cold-blooded. Some, like the Mako and the Great white shark, are partially warmblooded (they are endotherms)...
2. Are sharks cold-blooded or warm-blooded? Sharks have a reputation as cold-blooded...
3. Great white sharks are some of the only warm blooded sharks...
4. Sharks' blood gives them turbo speed...

You will begin by examining the initially retrieved documents and identifying the ones that are relevant, even partially, to the query. Once the relevant documents are identified, you will extract the key sentences from each document that contribute to their relevance.

Based on the query "how are some sharks warm blooded", I have examined the initially retrieved documents. Here are the relevant documents and the key sentences extracted from each:

Document 1:
"Most sharks are cold-blooded. Some, like the Mako and the Great white shark, are partially warm-blooded (they are endotherms)."
"Actually, the Salmon Shark is a warm-blooded shark."

Document 3:
"Great white sharks are some of the only warm-blooded sharks."
"This allows them to swim in colder waters in addition to warm, tropical waters."

Document 4:
"Salmon sharks can elevate their body temperatures by up to 20 degrees compared to the surrounding water, for example."

Query: "{q}"
Retrieved documents:
1. {d1}
2. {d2}
...
k. {dk}

You will begin by examining the initially retrieved documents and identifying the ones that are relevant, even partially, to the query. Once the relevant documents are identified, you will extract the key sentences from each document that contribute to their relevance.
```

### Prompt Template (KEQE)
**From Table 1:**

```
Please write a passage to answer the question
Question: {q}
Passage:
```

---

## Performance Results (for Reference)

### TREC DL19 (MS-MARCO)
- BM25 baseline: 50.6 nDCG@10
- BM25+CSQE: 67.3 nDCG@10 (+33% improvement)
- Beats Contriever^FT (supervised): 62.1 nDCG@10

### BEIR Low-Resource (Average)
- BM25 baseline: 43.7 nDCG@10
- BM25+CSQE: 49.7 nDCG@10 (+14% improvement)
- Beats Contriever^FT: 48.2 nDCG@10

### NovelEval (Queries LLMs Don't Know)
- BM25 baseline: 68.4 nDCG@10
- BM25+KEQE: 62.0 nDCG@10 (-9% degradation due to hallucination)
- BM25+CSQE: 82.6 nDCG@10 (+21% improvement)

**Key insight:** CSQE prevents hallucination-induced degradation on queries where LLMs lack knowledge.

---

## Adaptation for Arabic MIRACL

### Confirmed Parameters
- K=10 (retrieve top-10 passages)
- 2+2 scheme (2 KEQE + 2 corpus-originated)
- 128 tokens (truncate each passage to 128 tokens)
- temp=1.0 (sampling temperature)

### Context Extraction Strategy (MIRACL-Specific)
Since MIRACL passages are already segmented (X#Y format), we need to:

1. **Retrieve top-10 passages** using baseline dense retrieval
2. **Group by article ID** (X from docid X#Y)
3. **For each article group:**
   - Extract article title
   - Extract passage position (Y)
   - Truncate each passage to 128 tokens
   - Format as: "Document {i}: {title}\n{text}"
4. **Feed to LLM** with CSQE prompt (translated to Arabic)
5. **Extract pivotal sentences** from LLM response
6. **Combine with KEQE expansions** (2+2 scheme)
7. **Re-retrieve** with expanded query

### Arabic Prompt Translation
The prompt should be translated to Arabic for better LLM performance with Arabic queries. Example:

```arabic
الاستعلام: "{q}"
المستندات المسترجعة:
1. {d1}
2. {d2}
...

ستبدأ بفحص المستندات المسترجعة أولاً وتحديد المستندات ذات الصلة، حتى لو كانت جزئياً، بالاستعلام. بمجرد تحديد المستندات ذات الصلة، ستستخرج الجمل الرئيسية من كل مستند التي تساهم في صلتها.
```

---

## Conclusion

**All 4 parameters from deep research are VERIFIED:**
- ✅ K=10
- ✅ 2+2 scheme
- ✅ 128 tokens
- ✅ temp=1.0

**Additional details extracted:**
- Full prompt templates (English)
- Query repetition strategy
- BM25 default parameters
- Performance benchmarks
- LLM model (GPT-3.5-Turbo-0301)

**Ready for implementation:** All parameters and prompts are confirmed and documented.
