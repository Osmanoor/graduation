# CSQE AI-Generated Figure Variants — README

Generated via **PaperBanana 0.1.2** on 2026-06-05.

## Setup (reproduced by anyone with the API key)

**Tool:** PaperBanana — multi-agent academic diagram generator  
**Repo:** https://github.com/llmsresearch/paperbanana  
**Install:** `python -m pip install "paperbanana[mcp]"`

**Generation scripts:**
- `thesis_figures/gen_csqe_variants.py` — full 4-variant script
- `thesis_figures/gen_csqe_v3v4.py` — v3/v4 only (used for final run)

**Environment variable required:**
```
GOOGLE_API_KEY=<your-key>
```
Set this before calling `paperbanana.core.config.Settings()` — the field uses the alias `GOOGLE_API_KEY` (Pydantic BaseSettings reads it from env, not from the keyword arg `google_api_key`).

**Models:**
- VLM (planning + styling + critic): `gemini-2.5-flash`  
  Note: the PaperBanana default `gemini-2.0-flash` is deprecated as of 2026-06 — use `gemini-2.5-flash`.
- Image generation: `gemini-3-pro-image-preview` (PaperBanana default, confirmed available)

**MCP server config** (for Claude Code, add to project `.mcp.json` and restart):
```json
{
  "mcpServers": {
    "paperbanana": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "paperbanana[mcp]", "paperbanana-mcp"],
      "env": { "GOOGLE_API_KEY": "YOUR_KEY_HERE" }
    }
  }
}
```

**Pipeline notes:**
- No reference index was found (`data/reference_sets/` not populated) — the Retriever agent returned no examples. This means PaperBanana generated without in-context reference images, relying purely on the planner+stylist prompt chain.
- Each run used `refinement_iterations=3` but all 4 variants were approved by the critic in 1 iteration ("No issues found. Image is publication-ready.").
- Seeds: PaperBanana does not expose a seed parameter; reproducibility is approximate (same model + same prompt → similar but not identical output on re-run).

---

## Shared source context (all variants)

All variants used the same `source_context` (from `gen_csqe_variants.py` → `SHARED_CONTEXT`):

> Three-stage CSQE pipeline over MIRACL Arabic corpus:
> Stage 1: BM25 first-pass retrieval (top-k₁=5 passages).
> Stage 2: Aya Expanse 8B called 4 times — 2 corpus-grounded samples (c₁,c₂) + 2 blind samples (b₁,b₂).
> Stage 3: BM25 re-retrieval with q⊕q⊕q⊕q⊕c₁⊕c₂⊕b₁⊕b₂ (α=4 repetitions to counter term dilution).
> Results: BM25+CSQE = 0.616 nDCG@10; best system (CSQE+Dense RRF) = 0.714.
> Worked example: الأسماء الخمسة query — blind QE hallucinates names (nDCG=0.0), CSQE grounds to correct grammar article (nDCG=1.0).

---

## Variants

### v1 — Three-stage flowchart with results label

**File:** `fig_3_8_csqe_aigen_v1.png` (2.0 MB)  
**Generated:** 2026-06-05 08:49 (second clean run; first generated at 08:46 from run `run_20260605_084126_9127ae`)  
**Run ID:** `run_20260605_084757_7e92b0`  
**Iterations:** 1 (critic approved immediately)

**Communicative intent prompt:**
> A clear, stage-labelled flowchart of the CSQE three-stage pipeline. Show the user query entering Stage 1 (BM25 first-pass), the top-5 retrieved passages flowing into Stage 2 where Aya 8B produces four samples (two corpus-grounded c₁,c₂ and two blind b₁,b₂), then all four samples plus α=4 query repetitions concatenated into one expanded query in Stage 3 (BM25 second-pass) producing the final ranked list. Differentiate the corpus-grounded samples visually from the blind samples. Include the result nDCG@10 = 0.616.

**What makes it different:** Canonical left-to-right flowchart. All three stages clearly labelled. Four sample boxes colour-differentiated. Numeric result included.

---

### v2 — Side-by-side Blind vs. CSQE comparison with worked example

**File:** `fig_3_8_csqe_aigen_v2.png` (2.3 MB)  
**Generated:** 2026-06-05 08:51  
**Run ID:** `run_20260605_084757_7e92b0`  
**Iterations:** 1 (critic approved immediately)

**Communicative intent prompt:**
> A side-by-side comparison layout contrasting Blind Query2Doc (left column) with CSQE (right column), using the الأسماء الخمسة worked example. Left column: query → LLM (no context) → hallucinates a list of names → wrong retrieval → nDCG@10 = 0.000. Right column: query → BM25 first-pass → top-5 passages → LLM produces corpus-grounded expansion about أب أخ حم فو ذو → correct retrieval → nDCG@10 = 1.000. The visual contrast between the two paths is the main point.

**What makes it different:** Shows the failure mode directly. Examiner sees in one glance why blind QE fails and why corpus-grounding fixes it. Uses the recommended الأسماء الخمسة golden example.

---

### v3 — Compact three-band horizontal layout

**File:** `fig_3_8_csqe_aigen_v3.png` (2.2 MB)  
**Generated:** 2026-06-05 09:00  
**Run ID:** `run_20260605_085830_1e16c6`  
**Iterations:** 1 (critic approved immediately)

**Communicative intent prompt:**
> A compact overview that fits in a thesis single-column figure. Show the pipeline as three horizontal bands labelled Stage 1, Stage 2, Stage 3. Inside Stage 2 show four distinct LLM call boxes: c1 and c2 shaded one colour (corpus-grounded), b1 and b2 shaded a different colour (blind). Show the query repetition factor alpha=4 in the Stage 3 concatenation formula. Keep labels concise so nothing is crowded.

**What makes it different:** Designed for single-column space constraints. Horizontal band layout vs. left-to-right arrow chain. Prioritises label density over explicit flow arrows.

---

### v4 — Narrative two-path divergence with formula as visual element

**File:** `fig_3_8_csqe_aigen_v4.png` (2.2 MB)  
**Generated:** 2026-06-05 09:02  
**Run ID:** `run_20260605_085830_1e16c6`  
**Iterations:** 1 (critic approved immediately)

**Communicative intent prompt:**
> A narrative-driven figure that foregrounds the corpus-grounding mechanism. Show the two-path divergence clearly: one path from the query goes straight to Aya 8B (blind), the other first hits BM25, retrieves real Wikipedia passages, then goes to Aya 8B (grounded). Both paths produce pseudo-documents that are concatenated with four repetitions of the original query before the final BM25 retrieval. Show the query repetition formula q+q+q+q+c1+c2+b1+b2 as a visual element rather than just a text label.

**What makes it different:** Treats the formula as a visual node, not a caption. The two-path fork is the central compositional element, showing the divergence from query → blind vs. query → BM25 → grounded before they merge into one expanded query.

---

## Recommendation

**v2** — the side-by-side comparison with the الأسماء الخمسة worked example.

**Why:** The thesis's central claim is not "here is a pipeline diagram" but "corpus grounding prevents the hallucinations that blind QE introduces." v2 shows this in a single figure: the examiner sees the wrong path (blind → names hallucination → nDCG=0.0) and the right path (CSQE → correct grammar article → nDCG=1.0) without needing to read the caption. This is the تفسير-by-example approach recommended in `WS4_TASK_4.12_BIGWIN_EXAMPLES.md` §3.

v1 is the safer backup: a clean canonical pipeline diagram that describes the system without the worked example. If the thesis layout already includes a separate big-win table (§4.10, Table 5.C.17), v1 avoids redundancy. If Fig 3.8 needs to stand alone as a figure that also teaches the reader *why* CSQE works, v2 wins.

v3 and v4 are valid alternatives if column-width or layout constraints change the framing.

---

## Post-processing

None — all four images are raw PaperBanana outputs with no manual editing.

The existing TikZ source at `thesis_figures/system_diagrams/fig_3_8_csqe.tex` is preserved as the reproducible fallback.
