# Workflow Templates

These are step-by-step workflows triggered by keyword phrases.
Follow the matching workflow exactly. Do NOT skip steps.

---

## Daily Research Standup
**Trigger:** "daily standup", "plan my day"

1. Read `TASKS.md`
2. List tasks that are "In Progress" or can be started (dependencies met)
3. For each available task, show its "Context Files" section so the user knows what to reference
4. Ask which task the user wants to work on
5. When they choose, summarize the task's Why, Deliverables, and Context Files
6. Do NOT invent task status - only report what's in TASKS.md

---

## Complete Task
**Trigger:** "complete task", "mark task done"

Ask the user:
1. Which task number? (e.g., 1.4)
2. What were the deliverables completed?
3. What are the outcomes to record?

Then:
- A) Update the task status to "Done" in TASKS.md
- B) Fill in the Outcomes section for that task
- C) Check if any context files listed in that task need updates (e.g., RESEARCH_CONTEXT_KERNEL.md.md, open_questions.md)
- D) Check if this unblocks other tasks and note them
- Do NOT mark anything done that the user doesn't confirm

---

## Update Experiment Log
**Trigger:** "log experiment", "document experiment"

Ask the user:
1. Which task was this for? (e.g., Task 2.3)
2. What were the exact metric values? (Recall@10, NDCG@10, MRR)
3. What dataset subset did you use?
4. What did you learn?

Then:
- A) Create experiment doc in `experiments/exp_XXX.md` following `.claude/contexts/experiment-documentation.md` template
- B) Update the task's Outcomes section in TASKS.md
- C) Tell the user which other context files should be updated (e.g., RESEARCH_CONTEXT_KERNEL.md.md)
- Do NOT invent any metric values - only use what the user provides

---

## Summarize Paper
**Trigger:** "summarize paper", "add paper"

1. The user will provide paper details
2. Create a summary in `papers/[YEAR]_[Title].md` following the exact template in `.claude/contexts/paper-analysis.md`
3. After creating, tell the user which tasks this paper might be relevant to (check TASKS.md context files)
4. Only include information the user provides - do NOT invent details

---

## Sync Decisions
**Trigger:** "sync decisions", "after meeting"

1. The user will describe what was decided in a meeting or discussion
2. Based ONLY on what they tell you, suggest updates to:
   - `TASKS.md` if task status changed
   - `RESEARCH_CONTEXT_KERNEL.md.md` if decisions changed
   - `research_decisions/open_questions.md` if questions were resolved
3. Do NOT assume any decisions the user doesn't explicitly state

---

## Prepare Supervisor Meeting
**Trigger:** "prepare meeting", "supervisor meeting"

1. Read `TASKS.md` and `RESEARCH_CONTEXT_KERNEL.md.md`
2. Generate:
   - Tasks completed since last update (only those marked Done)
   - Current blockers (from `research_decisions/open_questions.md`)
   - Questions we need supervisor input on
3. Base everything on the actual file contents - do NOT invent progress
