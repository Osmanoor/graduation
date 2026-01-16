# Google Colab Quick Start Guide

**Experiment 001: Dense Baseline (mDPR)**

---

## Prerequisites

1. Google account (for Colab)
2. Enable T4 GPU in Colab (recommended)
   - Runtime → Change runtime type → T4 GPU

---

## Steps to Run

### 1. Open Colab

Go to: https://colab.research.google.com/

### 2. Upload Notebook

**Option A: Direct Upload**
- File → Upload notebook
- Upload: `experiments/exp_001_baseline_dense.ipynb`

**Option B: From GitHub**
- File → Open notebook → GitHub tab
- Enter: `Osmanoor/graduation`
- Select: `arabic-rag-query-enhancement/experiments/exp_001_baseline_dense.ipynb`

### 3. Run Setup Cell

Run the first cell (Step 1):
```python
# Clone repository
!git clone https://github.com/Osmanoor/graduation.git
%cd graduation/arabic-rag-query-enhancement

# Install dependencies...
```

**Wait for installation to complete** (~2-3 minutes)

### 4. Restart Runtime

**IMPORTANT:** After installation completes:
1. Click **Runtime** → **Restart runtime**
2. Click **Yes** when prompted

### 5. Run Experiment

After restart:
1. Run **Step 2** cell (Configure Environment)
2. Run all remaining cells in order
3. Wait for results (~2-3 minutes with GPU)

---

## Expected Output

### During Execution

```
Loading MIRACL data...
✓ Loaded 2896 queries
✓ Loaded qrels for 2896 queries

Loading mDPR encoder on GPU...
✓ Encoder loaded on GPU

Loading FAISS index...
⚠️ First run: downloading ~6GB (5-10 minutes)
✓ Index loaded: 2,061,414 documents

Encoding 2896 queries on GPU...
[Progress bar]
✓ Encoded 2896 queries

Searching FAISS index...
✓ Search complete

Evaluating...
```

### Final Results

```
============================================================
EXPERIMENT 001: Dense Baseline Results
============================================================
Recall@10:      0.6156
Recall@100:     0.8407 (Expected: ~0.841)
NDCG@10:        0.4993 (Expected: ~0.499)
MRR:            0.5328
Queries:        2896
============================================================

Achievement:
  Recall@100: 99.96%
  NDCG@10:    100.06%

✓ Results saved to results/baseline_dense/
```

---

## Troubleshooting

### Issue: "No module named 'src'"

**Solution:** Make sure you ran Step 2 (Configure Environment) after restart.

### Issue: "JAVA_HOME not set"

**Solution:** 
1. Verify you restarted runtime after Step 1
2. Run Step 2 cell again

### Issue: "GPU not available"

**Solution:**
1. Runtime → Change runtime type
2. Select **T4 GPU**
3. Save
4. Restart from Step 1

### Issue: "Index download is slow"

**Normal!** First run downloads 6GB index. Takes 5-10 minutes.
Subsequent runs will use cached index (much faster).

### Issue: "Out of memory"

**Solution:**
1. Runtime → Disconnect and delete runtime
2. Runtime → Change runtime type → High-RAM
3. Restart from Step 1

---

## Runtime Estimates

| Phase | Time (T4 GPU) | Time (CPU) |
|-------|---------------|------------|
| Installation | 2-3 min | 2-3 min |
| Index download (first run) | 5-10 min | 5-10 min |
| Query encoding | 1-2 min | 10-15 min |
| FAISS search | <1 min | <1 min |
| **Total (first run)** | **8-15 min** | **17-30 min** |
| **Total (cached)** | **2-3 min** | **10-15 min** |

---

## Verification

Your experiment is successful if:

✅ No errors during execution  
✅ Recall@100 ≈ 0.841 (±0.01)  
✅ NDCG@10 ≈ 0.499 (±0.01)  
✅ Results saved to `results/baseline_dense/`  
✅ Two files created:
   - `exp_001_baseline_dense.txt` (TREC format)
   - `exp_001_metrics.json` (metrics)

---

## Next Steps After Baseline

1. **Download results** (optional):
   ```python
   from google.colab import files
   files.download('results/baseline_dense/exp_001_metrics.json')
   ```

2. **Implement query enhancement:**
   - Create new enhancer in `src/enhancers/`
   - Copy notebook to `exp_002_qe_dense.ipynb`
   - Replace `IdentityEnhancer` with your enhancer
   - Run and compare with baseline

3. **Analyze improvements:**
   - Which queries improved?
   - Which queries degraded?
   - Why?

---

## Common Questions

**Q: Do I need to clone the repo every time?**  
A: No! After first run, the repo is cached. Just reconnect to the same runtime.

**Q: Can I run without GPU?**  
A: Yes, but it will be slower (~10-15 min vs 2-3 min).

**Q: How much does this cost?**  
A: Free! Colab free tier is sufficient. No paid subscription needed.

**Q: Can I save results to Google Drive?**  
A: Yes! Add this cell:
```python
from google.colab import drive
drive.mount('/content/drive')

# Copy results to Drive
!cp -r results/ /content/drive/MyDrive/graduation_results/
```

**Q: The notebook disconnected. Do I lose progress?**  
A: The index is cached, so re-running is fast. But you'll need to re-run all cells.

---

## Support

If you encounter issues:

1. Check this troubleshooting guide
2. Verify all prerequisites
3. Try restarting runtime
4. Check GitHub issues: https://github.com/Osmanoor/graduation/issues

---

**Ready to run!** 🚀

Open the notebook in Colab and follow the steps above.
