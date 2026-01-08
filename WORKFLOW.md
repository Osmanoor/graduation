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
   - Kiro will read TASKS.md and show available tasks
   - For each task, you'll see its Context Files
   - Choose a task to work on
   - Kiro will summarize the task's Why, Deliverables, and what files to reference
3. **Read the Context Files** listed for your chosen task
4. **Start working**

### During Work

**Use Kiro for:**
- Coding help: Type `#baseline-implementation` for code patterns
- Paper research: Use arXiv MCP - "Search arXiv for [topic]"
- Questions: Ask about the project (Kiro has context from steering)

**Work outside Kiro if preferred:**
- Google Colab experiments
- Reading papers
- Team discussions

### After Completing Work

**For experiments:**
1. Trigger **"Update Experiment Log"** hook
2. Provide your actual metric values
3. Kiro creates experiment doc + updates TASKS.md outcomes

**For any task:**
1. Trigger **"Complete Task"** hook
2. Confirm deliverables and outcomes
3. Kiro updates:
   - Task status in TASKS.md
   - Outcomes section
   - Related context files
   - Notes which tasks are now unblocked

### After a Meeting/Discussion

1. Trigger **"Sync Decision Status"** hook
2. Tell Kiro what was decided
3. Kiro updates relevant files

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

| Hook | Use When | What It Does |
|------|----------|--------------|
| **Daily Research Standup** | Start of work session | Shows available tasks with their context files, helps you pick one |
| **Complete Task** | Finished a task | Updates TASKS.md status & outcomes, updates related context files |
| **Update Experiment Log** | After running experiment | Creates experiment doc, updates task outcomes |
| **Summarize Paper** | Found relevant paper | Creates paper summary, links to relevant tasks |
| **Sync Decision Status** | After meeting/discussion | Updates decision docs based on what you tell it |
| **Prepare Supervisor Meeting** | Before supervisor meeting | Generates progress summary from actual file contents |

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
