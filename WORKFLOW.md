# Research Workflow Guide
**For:** Mohammed Elhaj & Osman Bashir  
**Project:** Arabic RAG Query Enhancement

---

## Files to Read First (In Order)

1. **`RESEARCH_CONTEXT_KERNEL.md.md`** - Project overview, what's decided vs under investigation
2. **`meetings/6.1.2026_meeting_outcomes.md`** - Latest decisions from our review meeting
3. **`TASKS.md`** - Current task list with assignments and status
4. **`research_decisions/technical_specifications.md`** - Architecture and implementation details
5. **This file (`WORKFLOW.md`)** - How we work

---

## Daily Workflow

### Starting Your Work Session

1. **Open Kiro** in this project folder
2. **Trigger "Daily Research Standup" hook** (in Agent Hooks panel)
   - This will ask Kiro to check your tasks and suggest focus areas
3. **Check `TASKS.md`** for your assigned tasks
4. **Update task status** as you work

### During Coding/Implementation

**Option A: Use Kiro (Preferred)**
- For baseline implementation: Type `#baseline-implementation` in chat to load coding patterns
- For debugging: Just describe the issue, Kiro has project context
- For paper research: Use arXiv MCP - ask "Search arXiv for [topic]"

**Option B: Work Outside Kiro**
- That's fine! Just document your work
- When done, use "Update Experiment Log" hook to document results

### After Completing an Experiment

1. **Trigger "Update Experiment Log" hook**
2. Answer the prompts about what you tested and results
3. Kiro will create a doc in `experiments/exp_XXX.md`
4. **Update `TASKS.md`** - mark task as done

### After a Meeting/Discussion

1. **Trigger "Sync Decision Status" hook**
2. Tell Kiro what was discussed
3. Kiro will update the relevant context files
4. Review the changes

---

## Kiro Setup Summary

### Steering Files (Auto-loaded Context)

| File | When It Loads | What It Does |
|------|---------------|--------------|
| `research-assistant.md` | Always | Project context, rules, references main docs |
| `paper-analysis.md` | When in `/papers/` | Paper summary template |
| `experiment-documentation.md` | When editing `exp_*.md` | Experiment doc standards |
| `thesis-writing.md` | When editing `.tex` files | Thesis guidelines |

### Manual Steering (Type in Chat)

| Command | Use When |
|---------|----------|
| `#baseline-implementation` | Coding the baseline system |
| `#literature-search` | Hunting for papers |

### Hooks (In Agent Hooks Panel)

| Hook | Use When |
|------|----------|
| Daily Research Standup | Start of work session |
| Update Experiment Log | After running an experiment |
| Summarize Paper | Found a relevant paper to add |
| Sync Decision Status | After meeting or decision change |
| Prepare Supervisor Meeting | Before meeting with supervisor |

### MCP Tools

| Tool | Use For |
|------|---------|
| arXiv | Search and download papers |

---

## File Organization

```
project/
├── RESEARCH_CONTEXT_KERNEL.md.md  # Source of truth for project state
├── TASKS.md                        # Task list (update daily)
├── WORKFLOW.md                     # This file
├── QUICK_REFERENCE.md              # One-page summary
├── README.md                       # Project overview
│
├── meetings/                       # Meeting transcripts and outcomes
│   ├── 6.1.2026_meeting_outcomes.md  # Latest decisions
│   └── ...
│
├── research_decisions/             # Technical docs
│   ├── technical_specifications.md
│   └── open_questions.md
│
├── experiments/                    # Experiment documentation
│   ├── exp_001_baseline_bm25.md
│   └── ...
│
├── papers/                         # Paper summaries
│   └── ...
│
└── .kiro/                          # Kiro configuration (don't edit manually)
    ├── steering/
    ├── hooks/
    └── settings/
```

---

## Communication Protocol

### When to Update Docs

| Event | Update These Files |
|-------|-------------------|
| Completed a task | `TASKS.md` |
| Ran an experiment | `experiments/exp_XXX.md`, `TASKS.md` |
| Made a decision | `RESEARCH_CONTEXT_KERNEL.md.md`, `open_questions.md` |
| Had a meeting | `meetings/[date]_outcomes.md` |
| Found relevant paper | `papers/[year]_[title].md` |

### Handoff Between Team Members

When handing off work:
1. Update `TASKS.md` with current status
2. Add notes to relevant experiment doc
3. Commit changes to git
4. Message teammate with summary

---

## When to NOT Use Kiro

It's okay to work outside Kiro for:
- Quick Google Colab experiments
- Reading papers in browser
- Team discussions

Just remember to:
- Document results using the hooks when done
- Update `TASKS.md` manually if needed

---

## Troubleshooting

**Kiro doesn't have context:**
- Check if steering files are in `.kiro/steering/`
- Restart Kiro to reload config

**MCP not working:**
- Run `pip install uv` first
- Restart Kiro after installing

**Lost track of project state:**
- Read `RESEARCH_CONTEXT_KERNEL.md.md` - it's the source of truth
- Check `TASKS.md` for current status

---

## Quick Start Checklist

- [ ] Read `RESEARCH_CONTEXT_KERNEL.md.md`
- [ ] Read `meetings/6.1.2026_meeting_outcomes.md`
- [ ] Read `TASKS.md` and assign owners to Week 1 tasks
- [ ] Test Kiro setup: Trigger "Daily Research Standup" hook
- [ ] Start on Task 1.1 or 1.2
