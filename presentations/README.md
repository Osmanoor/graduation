# Presentation Compilation Guide

## Supervisor Meeting Presentation (January 2, 2026)

### File Location
`presentations/supervisor_meeting_2jan2026.tex`

### Compilation Instructions

#### Using Overleaf (Recommended)
1. Go to [Overleaf](https://www.overleaf.com)
2. Create a new project → Upload Project
3. Upload `supervisor_meeting_2jan2026.tex`
4. Compile (should work automatically)

#### Using Local LaTeX Installation
```bash
# Navigate to presentations folder
cd presentations

# Compile with pdflatex (run twice for proper references)
pdflatex supervisor_meeting_2jan2026.tex
pdflatex supervisor_meeting_2jan2026.tex

# Output: supervisor_meeting_2jan2026.pdf
```

#### Using latexmk (Recommended for local)
```bash
latexmk -pdf supervisor_meeting_2jan2026.tex
```

### Presentation Structure

1. **Project Overview** (3 slides)
   - Title & Objective
   - Project Evolution (The Pivot)

2. **Finalized Methodology** (4 slides)
   - System Architecture
   - Technology-Oriented Approach
   - Dataset Selection (MIRACL)
   - Query Enhancement Techniques

3. **Project Roadmap** (3 slides)
   - Checkpoint Strategy
   - Checkpoint 1 Details
   - Checkpoints 2-4 Overview

4. **Progress Update** (2 slides)
   - Accomplishments
   - Current Status & Documentation

5. **Challenges & Questions** (2 slides)
   - Key Challenges
   - Questions for Supervisor

6. **Timeline & Next Steps** (2 slides)
   - Project Timeline
   - Immediate Next Steps

7. **Summary** (1 slide)

**Total:** ~17 slides, estimated 20-25 minutes presentation

### Customization Tips

- **Add University Logo:** Replace the logo path in title slide if needed
- **Adjust Colors:** Modify `\usecolortheme{default}` to your preference
- **Add More Details:** Each slide has room for expansion if needed
- **Remove Sections:** Comment out sections if time is limited

### Required LaTeX Packages
All packages used are standard in most LaTeX distributions:
- beamer (presentation class)
- tikz (diagrams)
- booktabs (tables)
- graphicx (images)
- hyperref (links)

### Troubleshooting

**Issue:** TikZ diagrams not rendering
- **Solution:** Ensure `tikz` package is installed

**Issue:** Theme not found
- **Solution:** Use `\usetheme{default}` instead of `Madrid`

**Issue:** Compilation errors
- **Solution:** Check LaTeX log file for specific errors, ensure all packages are installed

### Notes for Presentation

- **Slide 4 (Technology-Oriented):** This is a key decision point - be ready to discuss
- **Slide 8 (Checkpoints):** Emphasize scalability and flexibility
- **Slide 12 (Questions):** These are genuine questions - encourage discussion
- **Slide 14 (Timeline):** Adjust dates based on supervisor feedback

### After the Meeting

Update the following based on supervisor feedback:
- `research_decisions/open_questions.md` - Mark resolved questions
- `RESEARCH_CONTEXT_KERNEL.md.md` - Update with any new decisions
- `meetings/` - Create new meeting notes file

---

**Created:** January 2, 2026  
**For:** Supervisor Meeting  
**Authors:** Mohammed Elhaj, Osman Bashir
