# Chapter 2 Compilation Guide

## Generated Chapter 2: Theoretical Background and Literature Review

### File Location
`University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter2_generated.tex`

### Integration with Main Thesis

#### Option 1: Replace Existing Chapter 2
```bash
# Backup original
cp chapter2.tex chapter2_original_backup.tex

# Replace with generated version
cp chapter2_generated.tex chapter2.tex
```

#### Option 2: Keep Both (Recommended for Review)
Keep `chapter2_generated.tex` separate and review before replacing `chapter2.tex`

### Compilation Instructions

#### Full Thesis Compilation
```bash
# Navigate to thesis template root
cd University_of_Khartoum__EEE_bachelor_s_thesis_template/

# Compile main thesis
pdflatex 1-main.tex
bibtex 1-main
pdflatex 1-main.tex
pdflatex 1-main.tex

# Output: 1-main.pdf
```

#### Using latexmk (Recommended)
```bash
latexmk -pdf 1-main.tex
```

### Chapter 2 Structure

**Section 2.1: Theoretical Background - RAG Fundamentals**
- 2.1.1: The Hallucination Problem in LLMs
- 2.1.2: The Standard RAG Architecture

**Section 2.2: The Retrieval Bottleneck and Query Mismatch**
- 2.2.1: The Semantic Gap in Retrieval
- 2.2.2: Query Sensitivity and Noise

**Section 2.3: Taxonomy of Advanced RAG Paradigms**
- 2.3.1: Index-Centric Approaches (Structural Enhancements)
- 2.3.2: Process-Centric Approaches (Agentic RAG)

**Section 2.4: Query Enhancement Techniques - State-of-the-Art**
- 2.4.1: Generative Query Expansion
- 2.4.2: Query Rewriting and Refinement
- 2.4.3: Iterative and Active Retrieval

**Section 2.5: RAG in Morphologically Rich and Low-Resource Languages**
- 2.5.1: The Arabic Linguistic Challenge
- 2.5.2: Current Arabic RAG Baselines
- 2.5.3: The Research Gap

**Section 2.6: Summary and Research Positioning**

### Required Citations (Add to References.bib)

The chapter references the following papers. Ensure they are in your `References.bib` file:

```bibtex
@article{yao2024survey,
  title={A Survey on Retrieval-Augmented Generation},
  author={Yao, Yunfan and others},
  year={2024}
}

@article{lewis2020retrieval,
  title={Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks},
  author={Lewis, Patrick and others},
  journal={NeurIPS},
  year={2020}
}

@article{karpukhin2020dense,
  title={Dense Passage Retrieval for Open-Domain Question Answering},
  author={Karpukhin, Vladimir and others},
  journal={EMNLP},
  year={2020}
}

% Add other citations as needed:
% - robustness_rag
% - qe_rag
% - raptor
% - lightrag
% - densex
% - selfrag
% - hyde
% - query2doc
% - rewrite_retrieve_read
% - query_optimization_survey
% - rqrag
% - levelrag
% - miracl
% - alsubhi2025
```

### Customization Needed

1. **Add Specific Citations:**
   - Replace placeholder citations (e.g., `\cite{robustness_rag}`) with actual BibTeX keys
   - Ensure all referenced papers are in `References.bib`

2. **Add Figures (Optional):**
   - Consider adding diagrams for RAG architecture (Section 2.1.2)
   - Add taxonomy diagram (Section 2.3)
   - Add query enhancement workflow (Section 2.4)

3. **Expand Sections (If Needed):**
   - Section 2.5.2 can be expanded with more Arabic baseline details
   - Section 2.4 can include more technique examples

4. **Adjust Depth:**
   - Current version is comprehensive but can be condensed if page limit is a concern
   - Each subsection can be expanded with more examples if needed

### Review Checklist

Before finalizing:
- [ ] All citations are in References.bib
- [ ] Citations compile without errors
- [ ] Section numbering is correct
- [ ] Figures (if added) are referenced correctly
- [ ] Grammar and spelling checked
- [ ] Consistent terminology throughout
- [ ] Transitions between sections are smooth
- [ ] Summary (2.6) accurately reflects chapter content

### Integration with Chapter 3

Chapter 2 ends with a clear research gap, which should lead naturally into Chapter 3 (Methodology). Ensure Chapter 3 begins with:

> "Building on the research gap identified in Chapter 2, this chapter presents our methodology for investigating query enhancement techniques in Arabic RAG systems..."

### Estimated Length

- **Current:** ~12-15 pages (depending on formatting)
- **Can be adjusted:** Each section can be expanded or condensed as needed

### Notes

- **Modular Design:** Each section is self-contained and can be edited independently
- **Funnel Approach:** Starts broad (RAG fundamentals) → narrows to specific (Arabic query enhancement)
- **Gap Positioning:** Section 2.5.3 clearly establishes the research gap your thesis addresses
- **Future-Proof:** Structure allows easy addition of new papers/findings

### Troubleshooting

**Issue:** Citation not found
- **Solution:** Add missing entry to `References.bib`

**Issue:** Section numbering off
- **Solution:** Ensure `\setcounter{secnumdepth}{3}` in main.tex

**Issue:** Chapter too long
- **Solution:** Condense Section 2.3 (Taxonomy) or move some content to appendix

**Issue:** Need more Arabic content
- **Solution:** Expand Section 2.5 with additional Arabic NLP papers

---

**Generated:** January 2, 2026  
**Based on:** Meeting outcomes (2.1.2026) and literature review  
**Status:** Ready for review and integration  
**Next Step:** Add specific citations and compile with main thesis
