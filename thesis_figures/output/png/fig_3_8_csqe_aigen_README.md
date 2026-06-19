# CSQE AI-Generated Figure Variants — README

Generated via **PaperBanana 0.1.2**.

Two generations exist:
- **v1–v4.png** — 2026-06-19 run, `gemini-3.1-pro-preview` VLM + `gemini-3-pro-image` image gen (current)
- **v1–v4_boosted.png** — 2026-06-05 original run, `gemini-2.5-flash` VLM + `gemini-3-pro-image-preview` image gen (preserved for comparison)

## Setup (reproduced by anyone with the API key)

**Tool:** PaperBanana — multi-agent academic diagram generator  
**Repo:** https://github.com/llmsresearch/paperbanana  
**Install:** `python -m pip install "paperbanana[mcp]"`

**Generation script:** `thesis_figures/gen_csqe_variants.py`

**Environment variable required (never hardcode):**
```
$env:GOOGLE_API_KEY='<your-key>'   # PowerShell
export GOOGLE_API_KEY=<your-key>   # bash
```

---

## 2026-06-19 Run (current — v1–v4.png)

**Run ID:** `run_20260619_121015_df4fa0`  
**VLM (planning + styling + critic):** `gemini-3.1-pro-preview`  
**Image generation:** `gemini-3-pro-image`  
**refinement_iterations:** 3

**Pipeline notes:**
- No reference index found (`data/reference_sets/` not populated) — Retriever returned no examples; planner+stylist ran from text only.
- `gemini-3-pro-image` produced washed-out/low-contrast images on first iterations; the critic detected this and requested stronger colours. All variants recovered within 3 iterations.
- Source context fully verified against `exp_013_csqe_aya_8b.md` and `csqe_parameter_verification.md` — no hallucinated parameters.
- **Key correction vs. 2026-06-05 run:** corpus-grounded prompt now accurately describes the LLM task as EXTRACTION of key sentences from retrieved documents (not free-form answer generation).

### v1 — Three-stage flowchart with results label

**File:** `fig_3_8_csqe_aigen_v1.png` (2.0 MB)  
**Iterations:** 3 (critic flagged contrast issues; accepted after iteration 3)

**Communicative intent:**
> A clear, stage-labelled flow diagram of the three-stage CSQE pipeline for Arabic BM25 retrieval. Stage 1 box: query q enters BM25, which returns the top-5 passages (each truncated to 128 tokens). Stage 2 box: Aya Expanse 8B is invoked 4 times (temp=1.0): two corpus-grounded calls (c1, c2) each receive query + 5 passages and EXTRACT key sentences; two blind calls (b1, b2) receive query only and generate from parametric knowledge. Use distinct visual styles (colour or shading) to distinguish corpus-grounded from blind boxes. Stage 3 box: the four pseudo-documents plus 4 repetitions of q are concatenated (show formula q x4 + c1+c2+b1+b2 or alpha=4 label), then fed to BM25 for the second retrieval. Annotate the final output: nDCG@10 = 0.616.

---

### v2 — Side-by-side Blind vs. CSQE comparison with worked example

**File:** `fig_3_8_csqe_aigen_v2.png` (2.0 MB)  
**Iterations:** 2 (critic JSON parse error on iter 2; defaulted to approved)

**Communicative intent:**
> A side-by-side contrast figure showing WHY corpus grounding matters. Title: 'Blind Query2Doc vs. CSQE -- Arabic grammar query example'. LEFT column (Blind QE): query (Five Nouns / al-asma' al-khamsa) -> Aya 8B (no context) -> generates list of personal names: Muhammad, Adam, Ibrahim ... -> BM25 retrieves biography articles -> relevant grammar article not found -> nDCG@10 = 0.000. RIGHT column (CSQE): query -> BM25 first-pass retrieves grammar article on Five Nouns -> Aya 8B extracts: father/ab, brother/akh, father-in-law/ham, mouth/faw, possessor/dhaw from the retrieved article -> BM25 re-retrieval finds the correct grammar article -> nDCG@10 = 1.000. The category-error hallucination on the left vs. corpus-anchored extraction on the right is the single visual point. Show the Arabic terms where possible.

---

### v3 — Compact three-band horizontal layout

**File:** `fig_3_8_csqe_aigen_v3.png` (1.9 MB)  
**Iterations:** 1 (critic JSON parse error; defaulted to approved)

**Communicative intent:**
> A compact pipeline overview designed for single-column thesis width (~8 cm). Three horizontal bands: Band 1 (Stage 1): query q -> BM25 -> top-5 passages. Band 2 (Stage 2): four LLM call boxes arranged in two pairs -- c1+c2 (corpus-grounded, one colour) and b1+b2 (blind, different colour). Label: Aya Expanse 8B, temp=1.0. Band 3 (Stage 3): concatenation node showing 'q*4 + c1+c2+b1+b2' (alpha=4 repetitions) -> BM25 second pass -> final ranked list. Keep all text labels short. Show nDCG improvement: 0.462 -> 0.616.

---

### v4 — Narrative fork-and-merge with formula as visual element

**File:** `fig_3_8_csqe_aigen_v4.png` (2.0 MB)  
**Iterations:** 2 (critic flagged contrast on iter 1; JSON parse error on iter 2; defaulted to approved)

**Communicative intent:**
> A narrative figure foregrounding the corpus-grounding mechanism as a fork-and-merge topology. From a central query node, two branches diverge: CORPUS BRANCH: query -> BM25 (k1=5) -> 5 Wikipedia passages -> Aya 8B (extract key sentences) -> c1, c2. BLIND BRANCH: query -> Aya 8B (generate from knowledge) -> b1, b2. Both branches converge at a MERGE node that assembles the final expanded query. Display the assembly formula as a banner or framed node: q_CSQE = [q][q][q][q][c1][c2][b1][b2] (four copies of q, then four pseudo-documents). The merged query feeds into BM25 for the final retrieval step. Label the corpus branch with 'vocabulary anchored in Wikipedia text' and the blind branch with 'parametric diversity'. Show the headline metric: nDCG@10 = 0.616 for BM25+CSQE.

---

## 2026-06-05 Run (preserved as _boosted — v1–v4_boosted.png)

**Run ID:** `run_20260605_084757_7e92b0` (v1, v2) / `run_20260605_085830_1e16c6` (v3, v4)  
**VLM:** `gemini-2.5-flash`  
**Image gen:** `gemini-3-pro-image-preview`

All four variants were approved by the critic in 1 iteration each. File sizes: v1=2.0 MB, v2=2.3 MB, v3=2.1 MB, v4=2.1 MB.

Variants shared the same communicative intent as the 2026-06-19 run in overall structure, but the source context described corpus-grounded samples as "writing a short passage using the retrieved documents" rather than extracting key sentences. The 2026-06-19 run corrects this.

---

## Shared source context (2026-06-19 run)

All variants used the same `source_context` (verified against exp_013 doc and parameter verification doc):

- k₁ = 5 first-pass passages (our MIRACL implementation; original CSQE paper uses k=10)
- LLM: Aya Expanse 8B, BF16, A100 40 GB, temp=1.0, max_new_tokens=128
- Corpus-grounded (c1, c2): LLM **extracts key sentences** from retrieved passages — EXTRACTIVE
- Blind (b1, b2): LLM **generates** a passage from parametric knowledge — GENERATIVE
- Final query: q×4 ⊕ c1 ⊕ c2 ⊕ b1 ⊕ b2 (α=4 repetitions, one per expansion, to counter BM25 term dilution)
- BM25+CSQE: nDCG@10 = 0.6157 (+33.2% over BM25 baseline 0.4621)
- Best system (BM25+CSQE + Dense RRF k=20): nDCG@10 = 0.7137

Worked example (qid 3034): query «ما هي الأسماء الخمسة في اللغة العربية؟»  
Blind QE: confuses grammar term with personal names → nDCG@10 = 0.000  
CSQE: first-pass retrieves correct grammar article → extraction locks on أب أخ حم فو ذو → nDCG@10 = 1.000

---

## Recommendation

**v2** — the side-by-side comparison with the الأسماء الخمسة worked example.

The thesis's central claim is that corpus grounding prevents the hallucinations that blind QE introduces. v2 shows this in one figure: the examiner sees the wrong path (blind → names hallucination → nDCG=0.0) and the right path (CSQE → correct grammar article → nDCG=1.0) without reading the caption.

**v1** is the safer backup: a clean canonical pipeline diagram that describes the system without depending on the worked example. If the thesis already has a big-win table in a nearby section, v1 avoids redundancy.

**v3** and **v4** suit column-width-constrained layouts or situations where the formula needs to be a visual centrepiece.

---

## Post-processing

None — all images are raw PaperBanana outputs with no manual editing.

The TikZ source at `thesis_figures/system_diagrams/fig_3_8_csqe.tex` is preserved as the reproducible vector fallback.
