# SILMA Temperature: "Accidental Bug" vs "Recommended-Temperature Policy" — Adjudication

**Date:** 2026-07-31
**Scope:** Read-only audit. No `.tex`, `.ipynb`, `.csv` or `.pkl` file was modified.
**Question:** Was SILMA's temperature-0.7 pickle in the Exp 1.1 repetition sweep an accidental
file-mapping error, or a deliberate per-model "developer-recommended temperature" choice?

---

## 1. Verdict (up front)

**(a) — an isolated accidental file-mapping error in the Exp 1.1 sweep. Confidence: HIGH (~95%).**

Mohammed's recollection is **half right, and the half that is right does not apply to SILMA**:

- ✅ **TRUE:** the project genuinely did use *per-model* temperatures, and in at least two cases
  the value came from the model developers' own recommendation (Falcon-H1 = 0.1; Qwen3 = 0.7 with
  `top_p=0.8`, `top_k=20`). The thesis **already describes this policy** in §3.5.3 — so the thesis
  text is *not* missing the recommended-temperature account.
- ❌ **FALSE for SILMA:** there is no SILMA developer recommendation anywhere in the repo. SILMA is
  the one model whose temperature was chosen **empirically, by Osman, and the value he chose was
  0.1** — stated in his own results document, and hard-coded in his committed notebook. The 0.7 run
  is the *losing arm of that very comparison*, kept on disk and later re-loaded by mistake.
- Additional nuance: the per-model temperatures were **not** a policy applied top-down. The shared
  team guide prescribed `temperature=0.7` for **every** model as the default
  (`model_comparison_guide.md` lines 52, 148, 464, 499, 597 — all 0.7). Deviations were made
  case-by-case afterwards. SILMA's 0.7 pickle is simply the *first, default-configuration* run,
  superseded by the 0.1 run.
- Decisive counter-example to the "always use the developer's recommendation" account:
  **ALLaM-7B's model card recommends 0.6, and the team deliberately used 0.7 anyway**
  ("We test both 0.6 (model optimal) and 0.7 (cross-model comparison)" → `TEMPERATURE = 0.7`).
  Comparability beat the recommendation there, which is the opposite of the recalled policy.

**Practical consequence: nothing changes.** The prior conclusion in `SILMA_CONFLICT_RESOLUTION.md`
and task H1 stands. Re-run SILMA at **temperature 0.1**.

---

## 2. Evidence table

| # | Claim | Source (file:line) | What it says |
|---|---|---|---|
| E1 | SILMA's committed generation config is **temp 0.1** | `arabic-rag-query-enhancement/experiments/Query_generator_silma_2B.ipynb:510` | `TEMPERATURE = 0.1` — the only temperature constant in the notebook |
| E2 | …and it writes the temp-0.1 pickle | `Query_generator_silma_2B.ipynb:1051` | `output_file = "silma_2b_temp01.pkl"` |
| E3 | Osman's own results doc titles SILMA's canonical run "Temperature 0.1" | `arabic-rag-query-enhancement/docs/OSMAN_MODEL_COMPARISON_RESULTS.md:37,49` | "### Experiment 1: SILMA Kashif-2B (Temperature 0.1)"; config block `'temperature': 0.1` |
| E4 | …and names temp01 as the artefact of record | `OSMAN_MODEL_COMPARISON_RESULTS.md:58` | "Enhanced Queries: `results/enhanced_queries/silma_2b_temp01.pkl`" |
| E5 | **The temperature decision was empirical, not developer-recommended** | `OSMAN_MODEL_COMPARISON_RESULTS.md:18–31` | Section "Temperature Selection (SILMA 2B)": "Before running all models, we tested different temperature values using SILMA Kashif-2B to determine optimal generation parameters." → "**Decision:** Use temperature 0.1 for all subsequent experiments" |
| E6 | The "+2.5%" claim is a **dense** delta, measured on SILMA only | `OSMAN_MODEL_COMPARISON_RESULTS.md:300–306` | "Temp 0.7: NDCG@10 = 0.5052 / Temp 0.1: NDCG@10 = 0.5177 (+2.5%)". (0.5177−0.5052)/0.5052 = +2.47% ✅ |
| E7 | Team-wide default was 0.7 for **all** models — no per-model temp table ever existed | `research_decisions/model_comparison_guide.md:52, 148, 464, 499, 597` | Every per-model loading snippet, incl. SILMA (line 464), says `temperature=0.7` |
| E8 | Falcon-H1 is a **genuine** recommended-temperature case | `research_decisions/falcon_h1_research.md:196`; `Query_generator_falcon_h1.ipynb:1624`; `docs/experiments/exp_005_falcon_h1_3b_dense.md:67` | Model card: "recommended model temperature is 0.1 — higher than that, model's performance may largely drop"; notebook prints "FULL RUN: temperature=0.1 (Falcon recommended setting)" |
| E9 | Qwen3 is a **genuine** recommended-parameter case | `Query_generator_qwen3_4b.ipynb` cell 9; `docs/experiments/exp_007_qwen3_4b_dense.md:76` | `# Qwen3 non-thinking mode recommended parameters` → `TEMPERATURE = 0.7`, `TOP_P = 0.8`, `TOP_K = 20` |
| E10 | **ALLaM refutes a blanket "use the recommendation" policy** | `Query_generator_allam_7b.ipynb:291–293` | `# ALLaM model card recommends temperature=0.6` / `# We test both 0.6 (model optimal) and 0.7 (cross-model comparison)` / `TEMPERATURE = 0.7` |
| E11 | The sweep hard-codes SILMA's temp-0.7 pickle, with no comment or rationale | `arabic-rag-query-enhancement/experiments/phase4_quick_wins (1).ipynb:215` (identical at `phase4_quick_wins_Ablation_erroranalysis.ipynb:225` and `docs/experiments/phase4_quick_wins_Ablation_erroranalysis.ipynb:8468`) | `'SILMA 2B': 'silma_2b_temp07.pkl',` — the only entry in `PKL_FILES` that points at a superseded artefact |
| E12 | The sweep's own experiment doc never mentions temperature or input files at all | `arabic-rag-query-enhancement/docs/experiments/exp_011_bm25_repetition.md` | No occurrence of "temperature", "temp0", or any `.pkl` filename. A deliberate deviation would have been documented; nothing was. |
| E13 | Only SILMA has two variants on disk | `arabic-rag-query-enhancement/results/enhanced_queries/` (directory listing) | `silma_2b_temp01.pkl` (804,707 B) **and** `silma_2b_temp07.pkl` (788,216 B), both mtime 2026-03-17. No other model has a temp-pair. |
| E14 | Meeting record confirms the SILMA temp sweep was an in-house 0.7-vs-0.1 test | `meetings/analysis/pt3_notes.md:103–109`; `meetings/23.1_2026.pt3.md:167–169` | Item 3.11: "Temperature: SILMA tested at 0.7 vs 0.1 with 0.1 yielding +2.5%"; Mohammed corrects an AI-written "0.0 and 0.1" to 0.7-vs-0.1. No mention of any developer recommendation for SILMA. |
| E15 | Independent earlier verification reached the same reading | `research_decisions/WS4_VERIFICATION_REPORT.md:52–56` | "SILMA was actually run at **both 0.1 and 0.7** … The notebook's committed config is 0.1." |
| E16 | Nothing in the repo attributes a temperature to SILMA's developers | Repo-wide grep for `recommend.*temperat` / `temperat.*recommend` (case-insensitive) | Hits exist **only** for Falcon-H1 (0.1), Qwen3 (0.7), ALLaM (0.6). **Zero hits for SILMA.** `model_comparison_guide.md:453–483` lists SILMA's model card + RAGQA benchmark links and prescribes 0.7 as the generic default, citing no recommendation. |

---

## 3. Per-model temperature audit

`n=1` columns of Table 4.7 and the dense Table 4.6 both derive from the **same pickle per model**,
so "temperature used for dense + BM25 n=1" is a single value per row.

| Model | Temp for dense + BM25 n=1 (Tab. 4.6 / 4.7) | Temp in Exp 1.1 sweep | Pickle loaded by the sweep | Both variants on disk? | Consistent? |
|---|---|---|---|---|---|
| Aya Expanse 8B | **0.1** (`Query_generator_aya_8b.ipynb:833`) | 0.1 | `enhanced_queries_aya_expanse_8b.pkl` | No | ✅ |
| Jais-2 8B | **0.7** (`Query_generator_jais_2_8b.ipynb:626`) | 0.7 | `enhanced_queries_jais_2_8b_chat.pkl` | No | ✅ numbers — ❌ **Ch.3 Table 3.2 prints 0.1** (see §5) |
| Qwen3-8B | **0.1** (`Query_generator_qwen3_8b.ipynb:359`) | 0.1 | `enhanced_queries_qwen3_8b.pkl` | No | ✅ |
| Qwen 2.5 7B | **0.1** (`Query_generator_qwen25_7b.ipynb:646`) | 0.1 | `enhanced_queries_qwen25_7b.pkl` | No | ✅ |
| Qwen3-4B | **0.7** (`Query_generator_qwen3_4b.ipynb` cell 9; Qwen3 non-thinking rec.) | 0.7 | `enhanced_queries_qwen3_4b.pkl` | No | ✅ (but see §5 note on `top_p`) |
| Gemma 3 4B | **0.1** (`Query_generator_gemma3_4b.ipynb:636`) | 0.1 | `enhanced_queries_gemma3_4b.pkl` | No | ✅ |
| Qwen 2.5 3B | **0.7** (original Query2Doc default, exp_003) | 0.7 | `qwen25_3b_temp07.pkl` | No | ✅ |
| Falcon-H1 3B | **0.1** (model-recommended, E8) | 0.1 | `enhanced_queries_falcon_h1_3b_temp01.pkl` | **No** — the notebook has a temp-0.7 branch (`:1853–1903`) but `..._temp07.pkl` is **not on disk** | ✅ |
| **SILMA 2B** | **0.1** (E1–E4) | **0.7** | `silma_2b_temp07.pkl` | **YES** (E13) | ❌ **the sole failure** |
| ALLaM 7B *(dropped)* | 0.7 (card recommends 0.6; 0.7 chosen for comparability, E10) | n/a — excluded from the sweep | — | No | n/a |

**Nine of nine sweep rows use the same pickle as the model-comparison run except SILMA.** This is
corroborated numerically in `SILMA_CONFLICT_RESOLUTION.md` §2.3: the four models present in both
runs agree to 4 d.p. on nDCG@10 *and* Recall@10; only SILMA diverges on all four metrics.

---

## 4. Recommendation for the re-run

1. **Re-run SILMA at temperature 0.1**, using `results/enhanced_queries/silma_2b_temp01.pkl`.
   Change exactly one line: `phase4_quick_wins (1).ipynb` cell 7 →
   `'SILMA 2B': 'silma_2b_temp01.pkl'`. Regenerate all eight repetition configs
   (n∈{1,3,5,7,10}, β∈{2,4,6}). BM25S is CPU-only; ~8 min. Sanity check: the new
   `n=1` must land on **0.4277** (it is the same computation that produced Table 4.7), which
   doubles as proof the re-run is wired correctly.
2. **No other model needs re-running.** All eight others already consume the identical pickle in
   both the model comparison and the sweep.
3. **After the re-run**, also regenerate `thesis_figures/data/raw/model_comparison_bm25.csv:3`
   and `thesis_figures/output/pdf/table_4_3.tex:6` (they currently pair the temp-0.1 `n=1` metrics
   with the temp-0.7 best config, giving Δ=0.0555, which matches neither Table 4.11 nor 4.12), and
   regenerate **Figs 4.7 and 4.8** from a single source — they presently plot SILMA `n=1` at 0.4194
   and 0.4277 respectively.
4. Confirm after the re-run that SILMA's best config still exceeds 0.4621, so the
   "all nine models beat the BM25 baseline" observation at `chapter4.tex:494` survives. Very likely:
   temp-0.1 `n=1` starts 0.0083 above temp-0.7 `n=1`, and repetition added +0.0639 at temp 0.7.

---

## 5. Does the thesis text need to change?

**Not for the "recommended temperature" account — §3.5.3 already states it correctly.**
`chapter3.tex:317–325` opens with "Temperature was not fixed at a single value across all models"
and gives both mechanisms: (1) model-recommended values (Falcon-H1 0.1, Qwen3 sampling), and
(2) empirical testing (SILMA 0.7 vs 0.1, +2.5%, adopted "as the default for subsequent experiments
where no model-specific recommendation existed"). That is an accurate description of what happened,
including the ALLaM-style comparability override being implicit in the "default" language.

Two genuine, **separate** defects surfaced by this audit — both in Ch.3 Table 3.2, neither caused by
the SILMA issue and neither affecting any Chapter 4 number:

| # | Location | Currently says | Should say | Evidence |
|---|---|---|---|---|
| T1 | `chapter3.tex:294` (Table 3.2, Jais-2 8B row) | `Jais-2 8B & 8B & BF16 & 0.1 & 8 & A100` | **0.7** | `Query_generator_jais_2_8b.ipynb:626` → `TEMPERATURE = 0.7`; `thesis_figures/data/raw/table_3_2_gen_hyperparams.csv:8` also says `Jais-2-8B,0.7`. **The `.tex` cell is the outlier** — the CSV that feeds `thesis_figures/output/pdf/table_3_2.tex` is already correct. |
| T2 | `chapter3.tex:281` (Table 3.2 caption) | "All models used `max_new_tokens`=128 and `top_p`=0.9 unless otherwise noted." | Qwen3-4B is an unflagged exception | `Query_generator_qwen3_4b.ipynb` cell 9 uses `TOP_P = 0.8` and `TOP_K = 20` (Qwen3 non-thinking recommendation); the CSV at `table_3_2_gen_hyperparams.csv:5` also records `0.9`, so both the CSV and the caption need the exception noted. |

**Sections/tables/figures affected by T1 + T2:** `chapter3.tex` Table 3.2 only (line 294 value; line
281 caption), plus `thesis_figures/data/raw/table_3_2_gen_hyperparams.csv` line 5 (`top_p`) and any
regeneration of `thesis_figures/output/pdf/table_3_2.tex`. **No Chapter 4 or 5 number moves** —
Jais's and Qwen3-4B's results always came from their single respective pickles, so every reported
metric for them is internally consistent; only the printed hyperparameter cell is wrong.

**If, contrary to this report, Mohammed still wants to present SILMA at 0.7**, §3.5.3 would have to
be rewritten to say the opposite of what Osman's document records ("Decision: Use temperature 0.1
for all subsequent experiments") and Chapter 4's finding #4 (`chapter4.tex:433`, "Temperature 0.1
was found to be optimal … +2.5% over temperature 0.7") would become self-contradictory, since the
+2.5% is measured **on SILMA itself**. That path is not recommended.

---

## 6. Could not be determined from the repo

1. **SILMA-Kashif-2B's model card contents.** No offline copy exists in the repo, and no team
   document quotes a generation-parameter recommendation from silma-ai. The absence of any such
   quote — where Falcon-H1, Qwen3 and ALLaM recommendations *were* all recorded (E8–E10) — is
   strong circumstantial evidence that none was consulted, but it is not a direct check of the card.
   *(If certainty is wanted, one web fetch of the HF card settles it; the link is at
   `model_comparison_guide.md:482`.)*
2. **Who authored the `PKL_FILES` dict** and in what order. The notebooks are committed without
   per-cell authorship, and both `phase4_quick_wins (1).ipynb` and the ablation notebooks carry the
   identical mapping, so the error propagated by copy-paste from one origin that cannot be dated.
3. **Which SILMA run came first.** Both pickles carry the same 2026-03-17 mtime (a bulk Drive sync).
   The order is inferred from the guide's 0.7 default (E7) plus Osman's "Before running all models,
   we tested…" phrasing (E5), not from filesystem timestamps.
4. **Whether the temp-0.7 `n>1` SILMA numbers were ever spot-checked against temp-0.1.** No
   partial temp-0.1 sweep artefact exists, so the post-re-run values genuinely are unknown until
   the re-run happens.
