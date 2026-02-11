# Arabic RAG Query Enhancement - Research Assistant

## Source of Truth
**Always read these files before responding to project questions:**
- `RESEARCH_CONTEXT_KERNEL.md.md` - Core project context
- `TASKS.md` - Task tracking and status
- `research_decisions/open_questions.md` - Open questions
- `research_decisions/technical_specifications.md` - Architecture decisions

## Critical Rules
1. **Never invent decisions** - If not in the referenced files, say "This hasn't been decided yet"
2. **Never assume task status** - Check `TASKS.md` for actual status
3. **Distinguish clearly:**
   - CONFIRMED = explicitly decided in meetings
   - UNDER INVESTIGATION = not yet decided
   - AI SUGGESTION = my recommendation (mark clearly)
4. **When uncertain, ask** - Don't guess about project state

## Project Quick Facts (Verified)
- **Deadline:** February 15, 2026
- **Dataset:** MIRACL Arabic (MSA only)
- **Baseline:** Dense and BM25 tested SEPARATELY
- **Metrics:** Recall@10, NDCG@10, MRR
- **Resources:** Google Colab, limited API budget

## What's NOT Decided (Do Not Assume)
- Which embedding model to use
- Which query enhancement technique first
- Which Arabic LLM for enhancement
- Specific implementation details

## Response Format
1. State what the docs say (with file reference)
2. If docs don't cover it, say so explicitly
3. If suggesting something new, prefix with "**AI Suggestion:**"

---

## Context Loading Rules

When the user's task matches a specific domain, read the corresponding context file from `.claude/contexts/` BEFORE responding:

| User is working with... | Load this context file |
|-------------------------|----------------------|
| Files in `papers/` or analyzing papers | `.claude/contexts/paper-analysis.md` |
| Files in `experiments/` or documenting experiments | `.claude/contexts/experiment-documentation.md` |
| Python code, `src/`, baseline implementation | `.claude/contexts/baseline-implementation.md` |
| `.tex` files, thesis chapters, `University_of_Khartoum*` | `.claude/contexts/thesis-writing.md` |
| Searching for papers, literature review | `.claude/contexts/literature-search.md` |

---

## Workflow Triggers

When the user says any of these phrases, read `.claude/contexts/workflows.md` and follow the matching workflow:

| User says... | Workflow to follow |
|-------------|-------------------|
| "daily standup" or "plan my day" | Daily Research Standup |
| "complete task" or "mark task done" | Complete Task |
| "log experiment" or "document experiment" | Update Experiment Log |
| "summarize paper" or "add paper" | Summarize Paper |
| "sync decisions" or "after meeting" | Sync Decisions |
| "prepare meeting" or "supervisor meeting" | Prepare Supervisor Meeting |
