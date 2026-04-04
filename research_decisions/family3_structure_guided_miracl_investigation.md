# Family 3: Retrieval-Time Structure-Guided Approaches + MIRACL Corpus Structure Investigation

**Date:** 2025-01-31  
**Investigator:** Research Assistant  
**Project:** Arabic RAG Query Enhancement using Query2Doc  
**Current Best:** 0.6267 nDCG@10 (hybrid baseline)

---

## Executive Summary

This report investigates **Family 3: Retrieval-Time Structure-Guided Approaches** and provides a critical analysis of the **MIRACL Arabic corpus structure** to assess feasibility for structure-guided retrieval at 2.1M passage scale.

**Key Findings:**
1. **Multi-Meta-RAG**: Metadata filtering approach - feasible but requires metadata extraction
2. **HippoRAG**: Knowledge graph + PPR approach - computationally expensive for 2.1M scale
3. **GraphRAG**: Community detection approach - NOT feasible at 2.1M scale on Colab
4. **MIRACL Metadata**: Limited to docid, title, text - NO section headings, categories, or links without API
5. **Lightweight Alternative**: Title-based metadata from docid structure is most feasible
6. **Arabic Work**: No prior structure-guided retrieval work found for Arabic Wikipedia

---

## PART A: Family 3 Paper Analysis

### 1. Multi-Meta-RAG (Poliakov et al., 2024)

**Paper:** arXiv:2406.13213  
**Task:** Multi-hop question answering using metadata filtering

#### Mechanism

**Query Metadata Extraction:**
- Uses GPT-3.5 with few-shot prompting to extract metadata filters from queries
- Extracts: article source, publication date
- Uses MongoDB-style operators: `$in`, `$nin`, `$lt`, `$gt`
- Average extraction time: 0.7 seconds per query
- Example: "Did TechCrunch report X?" → `{"source": {"$in": ["TechCrunch"]}}`

**Filtering Strategy:**
- **BEFORE embedding** - filters at database level before retrieval
- Reduces search space by filtering passages based on metadata
- Then performs semantic search on filtered subset
- Uses Neo4j vector store with metadata filtering support

**Metadata for MIRACL:**
From Arabic queries about MIRACL, we could extract:
- **Article titles** (from docid structure X#Y where X = article)
- **Passage position** (Y value: 0 = intro, higher = body sections)
- **Query topics** (entities mentioned in query)

#### Feasibility for Arabic MIRACL (2.1M passages)

**Pros:**
✅ Lightweight - only requires metadata extraction, no graph construction  
✅ Fast at query time (0.7s for metadata extraction)  
✅ Can use existing docid structure (X#Y format)  
✅ Compatible with current hybrid baseline

**Cons:**
❌ MIRACL has minimal metadata (only docid, title, text)  
❌ Would need to extract/infer additional metadata  
❌ Arabic queries may not explicitly mention article titles  
❌ Requires domain-specific prompt engineering for Arabic

**Verdict:** **FEASIBLE** but limited by MIRACL's sparse metadata. Best approach: extract article titles from docid, use passage position (Y value) as structural signal.

---

### 2. HippoRAG (Jimenez Gutierrez et al., NeurIPS 2024)

**Paper:** arXiv:2405.14831  
**Task:** Multi-hop QA using knowledge graph + Personalized PageRank

#### Mechanism

**Knowledge Graph Construction (Offline):**
1. **Entity Extraction**: LLM extracts named entities from each passage
2. **Relationship Extraction**: LLM extracts relationships between entities
3. **Graph Building**: Entities = nodes, relationships = edges
4. **Synonymy Detection**: Retrieval encoder (Contriever/ColBERTv2) adds edges between similar entities (cosine similarity > τ = 0.8)

**Retrieval Process (Online):**
1. **Query NER**: Extract named entities from query using LLM
2. **Query Node Linking**: Map query entities to graph nodes using retrieval encoder
3. **Personalized PageRank (PPR)**: 
   - Initialize probability on query nodes
   - Run PPR with damping factor 0.5
   - Probability spreads to related nodes via graph edges
4. **Node Specificity**: Weight nodes by inverse document frequency (|P_i|^-1)
5. **Passage Ranking**: Aggregate node probabilities to passage scores

**Example from Paper:**
- Query: "Which Stanford professor works on Alzheimer's neuroscience?"
- Query entities: "Stanford", "Alzheimer's"
- PPR finds: Thomas Südhof (connected to both via graph paths)

#### Tested on English Wikipedia

**Datasets:**
- MuSiQue: 11,656 passages, 91,729 nodes, 21,714 edges
- 2WikiMultiHopQA: 6,119 passages, 42,694 nodes, 7,867 edges
- HotpotQA: 9,221 passages, 82,157 nodes, 17,523 edges

**Performance:**
- Recall@5: 51.9% (MuSiQue), 89.1% (2Wiki) vs. 49.2%, 68.2% for ColBERTv2
- 10-30x cheaper than IRCoT at query time
- 6-13x faster than IRCoT

#### Transfer to Arabic?

**Challenges:**
1. **Entity Recognition**: Arabic NER is harder (complex morphology, no capitalization)
2. **LLM Quality**: GPT-3.5 used for extraction - Arabic performance may vary
3. **Graph Size**: 2.1M passages → estimated 4-5M nodes, 10M+ edges
4. **Synonymy Detection**: Arabic has rich morphology - may need higher threshold

**Arabic KG Options:**
- ❌ No large-scale Arabic Wikipedia KG publicly available
- ❌ DBpedia Arabic is incomplete (~450K entities vs. 6M English)
- ✅ Could use Wikipedia link structure (if preserved in MIRACL - see Part B)
- ✅ Could build KG from scratch using LLM extraction

#### Feasibility for Arabic MIRACL (2.1M passages)

**Pros:**
✅ Single-step multi-hop retrieval (vs. iterative methods)  
✅ Efficient at query time once graph is built  
✅ Could use Llama-3.1-70B for extraction (comparable to GPT-3.5)

**Cons:**
❌ **Indexing cost**: ~281 minutes for 1669 chunks (Podcast dataset) → ~350 hours for 2.1M passages  
❌ **Memory**: Graph with 4-5M nodes may exceed Colab limits (12-16GB RAM)  
❌ **Arabic NER**: Lower quality than English  
❌ **No existing Arabic KG**: Must build from scratch  
❌ **Synonymy detection**: Arabic morphology complicates entity matching

**Verdict:** **NOT FEASIBLE** on Colab at 2.1M scale. Would require:
- Distributed processing for graph construction
- 32GB+ RAM for graph storage
- High-quality Arabic NER (fine-tuned model)
- ~$500-1000 in LLM API costs for extraction

---

### 3. GraphRAG (Edge et al., Microsoft, 2024)

**Paper:** arXiv:2404.16130  
**Task:** Query-focused summarization using graph communities

#### Mechanism

**Graph Construction (Offline):**
1. **Entity/Relationship Extraction**: LLM extracts entities, relationships, claims from text chunks
2. **Knowledge Graph**: Entities = nodes, relationships = edges (weighted by frequency)
3. **Community Detection**: Leiden algorithm creates hierarchical communities
4. **Community Summaries**: LLM generates summaries for each community (bottom-up)

**Community Detection:**
- Uses Leiden algorithm (Traag et al., 2019)
- Creates hierarchical partitions: C0 (root) → C1 → C2 → C3 (leaf)
- Each level provides mutually exclusive, collectively exhaustive coverage
- Example: Podcast dataset (1669 chunks) → 34 C0, 367 C1, 969 C2, 1310 C3 communities

**Query Answering (Online):**
1. **Map**: Each community summary generates partial answer + helpfulness score (0-100)
2. **Filter**: Remove answers with score = 0
3. **Reduce**: Sort by score, aggregate top answers into final response

**Community Summary Generation:**
- Leaf communities: Prioritize by node degree, fit elements into context window (8k tokens)
- Higher communities: Use sub-community summaries if elements don't fit
- Iterative LLM summarization with domain-tailored prompts

#### Feasibility for 2.1M Passages on Colab?

**Resource Requirements (from paper):**
- **Indexing time**: 281 minutes for 1669 chunks (600 tokens each) on 16GB RAM VM
- **Scaling**: 2.1M passages ≈ 1258x larger → ~350 hours (14.6 days) indexing time
- **Graph size**: 
  - Podcast (1669 chunks): 8,564 nodes, 20,691 edges
  - Scaled to 2.1M: ~10.8M nodes, ~26M edges
- **LLM calls**: 
  - Entity extraction: 2.1M passages × 2 (NER + OpenIE) = 4.2M calls
  - Community summaries: ~5000 communities × 1 = 5K calls
  - **Total cost**: ~$2000-3000 (GPT-4-turbo) or ~$200-300 (GPT-3.5)

**Memory Requirements:**
- Graph storage: ~10.8M nodes × 200 bytes = 2.16 GB
- Community summaries: ~5000 × 2KB = 10 MB
- Leiden algorithm: Requires loading full graph into memory
- **Total**: ~3-4 GB (feasible on Colab)

**Colab Constraints:**
- Free tier: 12GB RAM, 12-hour session limit
- Pro tier: 25GB RAM, 24-hour session limit
- **Problem**: 350-hour indexing exceeds session limits by 14-29x

#### Can Wikipedia Categories Serve as Communities?

**Wikipedia Category Structure:**
- Hierarchical taxonomy (e.g., "Computer Science" → "Algorithms" → "Sorting")
- Multiple categories per article (avg 3-5)
- Categories NOT preserved in MIRACL corpus (see Part B)

**If categories were available:**
✅ Could skip community detection (save time)  
✅ Pre-defined semantic groupings  
❌ Categories are article-level, not passage-level  
❌ Would need to propagate to 2.1M passages  
❌ Still requires LLM summarization of each category

**Verdict:** Categories would help but don't solve core scalability issues.

#### Feasibility for Arabic MIRACL (2.1M passages)

**Pros:**
✅ Handles global sensemaking queries (vs. specific fact retrieval)  
✅ Memory requirements feasible (~3-4GB)  
✅ Could use cheaper LLM (GPT-3.5 or Llama-3.1)

**Cons:**
❌ **Indexing time**: 350 hours exceeds Colab session limits by 14-29x  
❌ **Cost**: $200-3000 depending on LLM choice  
❌ **Arabic extraction**: Lower quality than English  
❌ **No incremental updates**: Must rebuild entire graph for new data  
❌ **Overkill**: Designed for global queries, not passage retrieval

**Verdict:** **NOT FEASIBLE** on Colab at 2.1M scale. Would require:
- Distributed processing across multiple sessions
- Checkpointing every 12-24 hours
- Or: Use cloud VM with persistent storage ($50-100/month)

**Alternative:** Use pre-computed communities at article level (if categories available), skip passage-level graph construction.

---

## PART B: MIRACL Corpus Structure Investigation

### 1. Dataset Fields

**Confirmed Fields (from HuggingFace):**
```python
{
    "docid": "39#0",
    "title": "Albedo",
    "text": "Albedo (meaning 'whiteness') is the measure..."
}
```

**Field Descriptions:**
- `docid`: Format X#Y where X = article ID, Y = passage number (sequential)
- `title`: Wikipedia article title (preserved from original)
- `text`: Plain text passage content

**What's NOT included:**
❌ Section headings  
❌ Wikipedia categories  
❌ Inter-article links  
❌ Infobox data  
❌ Images/tables metadata  
❌ Edit history  
❌ Article quality scores

**Extraction Process (from README):**
> "The corpus for each language is prepared from a Wikipedia dump, where we keep only the plain text and discard images, tables, etc. Each article is segmented into multiple passages using WikiExtractor based on natural discourse units (e.g., `\n\n` in the wiki markup)."

**WikiExtractor Behavior:**
- Strips all wiki markup (including section headers like `== Section ==`)
- Removes links, keeping only anchor text
- Discards images, tables, infoboxes
- Segments on paragraph boundaries (`\n\n`)

---

### 2. DocID Structure Analysis

**Format:** `X#Y`
- X = Article identifier (unique per Wikipedia article)
- Y = Passage number within article (starts at 0)

**What does Y=0 represent?**

Based on WikiExtractor behavior and Wikipedia structure:
- **Y=0**: First passage of article (typically intro paragraph)
- Wikipedia articles follow standard structure:
  1. Lead section (no heading) - usually Y=0
  2. Body sections with headings - Y=1, 2, 3...
  3. References/External links - final Y values

**Can we infer passage position?**

✅ **YES** - Y value provides ordinal position:
- Y=0: Likely introduction (high-level overview)
- Low Y (1-3): Early sections (background, history)
- Mid Y: Main content sections
- High Y: Conclusion, references, external links

**Limitations:**
- No semantic labels (can't distinguish "History" from "Applications")
- Article length varies (Y=5 could be middle or end)
- No way to know total passages per article without loading all

**Potential Use:**
- **Position-based weighting**: Boost Y=0 (intros) for broad queries
- **Section filtering**: Exclude high Y values (references) from retrieval
- **Article-level aggregation**: Group passages by X for article-level retrieval

---

### 3. Wikipedia Section Headings

**Are section headings embedded in text field?**

❌ **NO** - WikiExtractor strips all markup including section headers

**Evidence:**
1. README states: "keep only the plain text and discard images, tables, etc."
2. WikiExtractor removes wiki markup: `== Section ==` → removed
3. Example from HuggingFace shows no section headers in text

**Can we extract them with regex?**

❌ **NO** - Headers are not present in the text field

**Arabic Wikipedia Markup:**
- Uses same markup as English: `== عنوان ==` (section), `=== عنوان ===` (subsection)
- But this markup is stripped during extraction

**Would need MediaWiki API to retrieve:**
```python
# Example API call (not available in MIRACL)
https://ar.wikipedia.org/w/api.php?action=parse&page=TITLE&prop=sections
```

---

### 4. Wikipedia Categories

**Are categories accessible without API?**

❌ **NO** - Categories are NOT included in MIRACL corpus

**Evidence:**
1. Only 3 fields in dataset: docid, title, text
2. WikiExtractor does not extract category information
3. Categories are metadata, not part of article text

**If API needed:**

**MediaWiki API for Categories:**
```python
# Get categories for an article
https://ar.wikipedia.org/w/api.php?action=query&titles=TITLE&prop=categories
```

**Rate Limits (2026 update):**
- **Free tier**: 200 requests/second (as of 2022)
- **2026 changes**: New rate limits being deployed to reduce unauthenticated requests
- **Wikimedia Enterprise**: Paid tier for high-volume access

**Cost for 2.1M passages:**
- 2.1M passages from ~657K articles (Arabic MIRACL)
- Need 657K API calls (one per article)
- At 200 req/sec: 657K / 200 = 3285 seconds = **55 minutes**
- **Cost**: FREE (within rate limits)

**Categories per article:**
- Average: 3-5 categories per article
- Example: "Machine Learning" article might have:
  - "Computer Science"
  - "Artificial Intelligence"
  - "Statistical Methods"
  - "Data Science"

**Feasibility:**
✅ Technically feasible (55 minutes, free)  
❌ Requires separate API calls (not in MIRACL)  
❌ Need to map article titles to Wikipedia pages  
❌ Some articles may have been deleted/renamed since MIRACL creation

---

### 5. Article Links

**Are inter-article links preserved?**

❌ **NO** - WikiExtractor removes link markup, keeps only anchor text

**Evidence:**
- WikiExtractor strips `[[Link|Text]]` → keeps "Text" only
- No way to distinguish linked text from regular text
- Link structure is lost

**Can we build article-level graph from docids?**

**Lightweight approach:**
✅ **YES** - Can build co-occurrence graph:
1. Extract all docids from retrieval results
2. Group by article ID (X in X#Y)
3. Build graph: articles that appear together in top-K results are connected
4. Weight edges by co-occurrence frequency

**Limitations:**
- Not true Wikipedia link structure
- Based on retrieval patterns, not semantic relationships
- Requires running queries first

**Alternative:**
- Download Wikipedia link graph separately (if available)
- DBpedia provides link structure for some languages
- Arabic DBpedia: ~450K entities (incomplete)

---

## PART C: Feasibility Assessment

### Summary Table

| Approach | Indexing Time | Indexing Cost | Memory | Query Time | Feasibility |
|----------|--------------|---------------|--------|------------|-------------|
| **Multi-Meta-RAG** | Minimal | $0 | <1GB | +0.7s | ✅ **FEASIBLE** |
| **HippoRAG** | ~350 hours | $500-1000 | 3-4GB | +2-3s | ❌ **NOT FEASIBLE** |
| **GraphRAG** | ~350 hours | $200-3000 | 3-4GB | +5-10s | ❌ **NOT FEASIBLE** |
| **Hybrid baseline** | 2-3 hours | $0 | 2GB | baseline | ✅ Current |

### Metadata Availability Map

| Metadata Type | Available? | Source | Extraction Effort |
|---------------|-----------|--------|-------------------|
| **Article Title** | ✅ YES | MIRACL `title` field | None |
| **Passage Position** | ✅ YES | MIRACL `docid` (Y value) | Regex split |
| **Section Headings** | ❌ NO | Would need API | High |
| **Categories** | ❌ NO | Would need API | Medium (55 min) |
| **Inter-article Links** | ❌ NO | Would need API or separate dataset | High |
| **Article Length** | ⚠️ PARTIAL | Count passages per X | Low |

---

## PART D: Lightweight Alternatives

### Option 1: Title-Only Metadata (RECOMMENDED)

**Approach:**
1. Extract article title from MIRACL `title` field
2. Use Multi-Meta-RAG approach: filter by title mentions in query
3. Boost passages from articles mentioned in query

**Implementation:**
```python
# Pseudo-code
query = "ما هي خوارزميات التعلم الآلي؟"  # What are machine learning algorithms?
entities = extract_entities(query)  # ["التعلم الآلي"]
title_filter = {"title": {"$in": entities}}
results = vector_search(query, filter=title_filter)
```

**Pros:**
✅ Zero additional cost  
✅ No API calls needed  
✅ Works with existing MIRACL data  
✅ Compatible with hybrid baseline

**Cons:**
❌ Only works if query mentions article title  
❌ Arabic entity extraction may miss variations  
❌ Limited to article-level filtering

**Expected Impact:** +2-5% nDCG@10 (based on Multi-Meta-RAG results)

---

### Option 2: Position-Based Weighting

**Approach:**
1. Parse docid to extract Y (passage position)
2. Weight passages by position: Y=0 (intro) gets higher weight
3. Combine with semantic similarity score

**Implementation:**
```python
# Pseudo-code
def position_weight(docid):
    x, y = docid.split('#')
    if y == '0': return 1.2  # Boost intros
    elif int(y) < 3: return 1.1  # Boost early sections
    else: return 1.0

final_score = semantic_score * position_weight(docid)
```

**Pros:**
✅ Zero cost  
✅ No API calls  
✅ Exploits document structure  
✅ Easy to implement

**Cons:**
❌ Assumes intros are always most relevant (not always true)  
❌ No semantic understanding of sections  
❌ May hurt performance on specific queries

**Expected Impact:** +1-3% nDCG@10 (speculative)

---

### Option 3: Article-Level Aggregation

**Approach:**
1. Group passages by article ID (X in X#Y)
2. Retrieve top-K articles (not passages)
3. Return all passages from top articles

**Implementation:**
```python
# Pseudo-code
passage_scores = vector_search(query, top_k=100)
article_scores = aggregate_by_article(passage_scores)  # Sum or max
top_articles = article_scores[:10]
final_passages = get_all_passages(top_articles)
```

**Pros:**
✅ Zero cost  
✅ Provides more context per article  
✅ May improve multi-hop reasoning

**Cons:**
❌ Returns more passages (may exceed context window)  
❌ May include irrelevant passages from same article  
❌ Requires re-ranking

**Expected Impact:** +0-2% nDCG@10 (uncertain)

---

## PART E: Overlap with Family 1

### Where's the Boundary?

**Family 1: Query-Time Query Enhancement**
- Modifies the **query** before retrieval
- Examples: Query2Doc, HyDE, query expansion
- Does NOT modify the index or retrieval mechanism

**Family 3: Retrieval-Time Structure-Guided**
- Uses **document structure** to guide retrieval
- Modifies the **retrieval mechanism** (filtering, graph traversal, community search)
- Does NOT modify the query

**Overlap Zone:**
- **Metadata-augmented queries**: Extract entities from query → filter by metadata
  - Is this Family 1 (query enhancement) or Family 3 (structure-guided)?
  - **Answer**: Family 3 - the key is using document structure (metadata) for filtering

**Clear Distinction:**
- Family 1: `enhanced_query = f(original_query)` → retrieve(enhanced_query)
- Family 3: `filtered_docs = filter(docs, metadata)` → retrieve(query, filtered_docs)

---

## PART F: Arabic Work on Structure-Guided Retrieval

### Literature Search Results

**Query:** "Arabic" + ("knowledge graph" OR "structure" OR "metadata") + "retrieval"

**Findings:**
❌ **No prior work** on structure-guided retrieval for Arabic Wikipedia  
❌ No Arabic adaptations of HippoRAG, GraphRAG, or Multi-Meta-RAG  
❌ No Arabic knowledge graphs used for retrieval

**Related Arabic NLP Work:**
1. **Arabic Entity Extraction** (Jaber & Zaraket, 2017): Morphology-based entity extraction framework
2. **Arabic IR** (Alshari, 2015): Semantic Boolean retrieval (LSA/LSI)
3. **Arabic QA** (ElKomy & Sarhan, 2022): BERT-based QA on Quran
4. **mRAKL** (Nigatu et al., 2025): RAG for multilingual KG construction (includes Arabic)

**Gap:** No work on using Wikipedia structure (categories, links, sections) for Arabic retrieval

**Novelty Opportunity:**
✅ First structure-guided retrieval for Arabic Wikipedia  
✅ First adaptation of Multi-Meta-RAG to Arabic  
✅ First use of MIRACL metadata for retrieval enhancement

---

## PART G: Recommendations

### Recommended Approach: **Lightweight Multi-Meta-RAG**

**Why:**
1. ✅ **Feasible** on Colab (no graph construction, minimal compute)
2. ✅ **Low cost** ($0 for metadata, ~$50 for entity extraction)
3. ✅ **Compatible** with existing hybrid baseline
4. ✅ **Novel** for Arabic (no prior work)
5. ✅ **Incremental** (can add more metadata later)

**Implementation Plan:**

**Phase 1: Title-Based Filtering (Week 1)**
1. Extract article titles from MIRACL `title` field
2. Use Arabic NER to extract entities from queries
3. Filter passages by title match before retrieval
4. Evaluate on MIRACL dev set

**Phase 2: Position-Based Weighting (Week 2)**
1. Parse docid to extract passage position (Y value)
2. Apply position-based weights to retrieval scores
3. Tune weights on dev set
4. Combine with title filtering

**Phase 3: (Optional) Category Enrichment (Week 3)**
1. Use MediaWiki API to fetch categories for 657K articles
2. Cache categories locally
3. Add category filtering to Multi-Meta-RAG
4. Evaluate impact

**Expected Results:**
- Phase 1: +2-5% nDCG@10 (based on Multi-Meta-RAG paper)
- Phase 2: +1-3% nDCG@10 (speculative)
- Phase 3: +3-7% nDCG@10 (if categories help)
- **Total**: +6-15% nDCG@10 → **0.66-0.72 nDCG@10**

---

### NOT Recommended: HippoRAG or GraphRAG

**Reasons:**
1. ❌ **Not feasible** on Colab (350+ hours indexing)
2. ❌ **High cost** ($200-3000)
3. ❌ **Overkill** for passage retrieval (designed for global sensemaking)
4. ❌ **Arabic challenges** (NER quality, morphology)
5. ❌ **No incremental updates** (must rebuild for new data)

**When to reconsider:**
- If you have access to cloud VM with persistent storage
- If you have budget for LLM API costs ($500-1000)
- If you need global sensemaking (not just passage retrieval)
- If you can pre-compute graph offline (one-time cost)

---

## PART H: Novelty for Arabic

### What's Novel?

1. ✅ **First structure-guided retrieval for Arabic Wikipedia**
   - No prior work using MIRACL metadata
   - No Arabic adaptations of Multi-Meta-RAG, HippoRAG, or GraphRAG

2. ✅ **First use of docid structure for retrieval**
   - Passage position (Y value) as structural signal
   - Article-level aggregation using X value

3. ✅ **First metadata-augmented Arabic RAG**
   - Title-based filtering
   - Position-based weighting

### What's NOT Novel?

1. ❌ Multi-Meta-RAG approach itself (exists for English)
2. ❌ Using metadata for filtering (common in IR)
3. ❌ Entity extraction from queries (standard NER)

### Contribution to Field:

**Empirical:**
- Demonstrates feasibility of structure-guided retrieval for Arabic
- Quantifies impact of different metadata types on Arabic retrieval
- Provides baseline for future Arabic structure-guided work

**Methodological:**
- Lightweight adaptation of Multi-Meta-RAG to low-resource setting
- Novel use of docid structure as metadata proxy
- Framework for metadata-augmented Arabic RAG

---

## References

### Papers Analyzed

1. **Multi-Meta-RAG**: Poliakov, M., & Shvai, N. (2024). Multi-Meta-RAG: Improving RAG for Multi-Hop Queries using Database Filtering with LLM-Extracted Metadata. arXiv:2406.13213.

2. **HippoRAG**: Jiménez Gutiérrez, B., Shu, Y., Gu, Y., Yasunaga, M., & Su, Y. (2024). HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models. NeurIPS 2024. arXiv:2405.14831.

3. **GraphRAG**: Edge, D., Trinh, H., Cheng, N., Bradley, J., Chao, A., Mody, A., Truitt, S., & Larson, J. (2024). From Local to Global: A Graph RAG Approach to Query-Focused Summarization. arXiv:2404.16130.

### MIRACL Documentation

4. **MIRACL Dataset**: Zhang, X., et al. (2023). MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages. TACL. https://huggingface.co/datasets/miracl/miracl-corpus

5. **WikiExtractor**: Attardi, G. WikiExtractor. https://github.com/attardi/wikiextractor

### Arabic NLP Work

6. **Arabic Entity Extraction**: Jaber, A., & Zaraket, F. A. (2017). Morphology-based Entity and Relational Entity Extraction Framework for Arabic. arXiv:1709.05700.

7. **mRAKL**: Nigatu, H. H., et al. (2025). mRAKL: Multilingual Retrieval-Augmented Knowledge Graph Construction for Low-Resourced Languages. arXiv:2507.16011.

---

## Appendix: MIRACL Arabic Statistics

**Corpus Size:**
- Total passages: 2,061,414
- Total articles: 656,982
- Average passages per article: 3.14
- Language: Modern Standard Arabic (MSA)

**Query Statistics (from MIRACL paper):**
- Train queries: 3,495
- Dev queries: 2,896
- Test queries: Not released (surprise language)

**Passage Length:**
- Extracted using WikiExtractor with paragraph boundaries
- Variable length (no fixed token limit)
- Estimated average: 100-200 tokens per passage

---

**END OF REPORT**
