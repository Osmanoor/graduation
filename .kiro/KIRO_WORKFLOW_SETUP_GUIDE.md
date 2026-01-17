# Kiro Workflow Setup Guide
**Purpose:** A reusable guide for setting up Kiro as an effective AI assistant for any project  
**Based on:** Arabic RAG Query Enhancement project setup (January 2026)  
**Author:** Mohammed Elhaj

---

## Overview

This guide documents the process of configuring Kiro to be maximally helpful for a project. It covers:
1. Understanding your project's needs
2. Creating steering files (always-on context)
3. Setting up hooks (automated workflows)
4. Configuring MCP servers (external tools)
5. Preventing AI hallucinations
6. Creating task tracking systems

---

## Phase 1: Project Analysis

Before configuring Kiro, answer these questions about your project:

### 1.1 Project Context Questions

```
□ What is the project? (one sentence)
□ What's the timeline/deadline?
□ Who's on the team?
□ What are the main deliverables?
□ What decisions are CONFIRMED vs UNDER INVESTIGATION?
□ What resources/constraints exist? (budget, tools, time)
```

### 1.2 Workflow Questions

```
□ What tasks will you do repeatedly?
□ What information do you need to reference often?
□ What file types will you work with?
□ What external tools/APIs do you need?
□ How will you track progress?
□ How will you document work?
```

### 1.3 AI Assistance Questions

```
□ What should the AI ALWAYS know about your project?
□ What should the AI NEVER assume or invent?
□ What format should AI responses follow?
□ What files are the "source of truth"?
```

---

## Phase 2: Steering Files

Steering files provide context to Kiro. They live in `.kiro/steering/`.

### 2.1 Types of Steering Files

| Type | Front-matter | When It Loads |
|------|--------------|---------------|
| Always-on | (none) | Every chat |
| File-match | `inclusion: fileMatch` | When matching files are open |
| Manual | `inclusion: manual` | When you type `#filename` |

### 2.2 Core Steering File (Required)

Create `.kiro/steering/project-assistant.md`:

```markdown
# [Project Name] - Assistant

## Source of Truth
**Always read these files before responding:**

#[[file:path/to/main-context.md]]
#[[file:path/to/tasks.md]]

## Critical Rules

1. **Never invent decisions** - If not in docs, say "not decided yet"
2. **Never assume status** - Check task file for actual status
3. **Distinguish clearly:**
   - ✅ CONFIRMED = explicitly decided
   - ⏳ UNDER INVESTIGATION = not yet decided
   - 💡 AI SUGGESTION = my recommendation (mark clearly)
4. **When uncertain, ask** - Don't guess

## Project Quick Facts
- **Deadline:** [date]
- **Team:** [names]
- **Key constraint:** [main limitation]

## What's NOT Decided (Do Not Assume)
- [List undecided items]

## Response Format
1. State what docs say (with file reference)
2. If docs don't cover it, say so
3. Prefix suggestions with "**AI Suggestion:**"
```

### 2.3 File-Match Steering (Optional)

For context that loads when working with specific file types:

```markdown
---
inclusion: fileMatch
fileMatchPattern: "src/**/*.py"
---

# Python Development Guidelines

[Context specific to Python files in your project]
```

Common patterns:
- `"tests/**/*.py"` - Test files
- `"docs/**/*.md"` - Documentation
- `"src/components/**/*"` - UI components
- `"**/*.sql"` - Database files

### 2.4 Manual Steering (Optional)

For context you load on-demand by typing `#steering-name`:

```markdown
---
inclusion: manual
---

# Deployment Guide

[Context for deployment tasks - only loaded when needed]
```

### 2.5 File References in Steering

Use `#[[file:path]]` to include other files:

```markdown
## Architecture
#[[file:docs/architecture.md]]

## API Spec
#[[file:api/openapi.yaml]]
```

This keeps steering DRY - update source files, steering stays current.

---

## Phase 3: Hooks

Hooks automate common workflows. They live in `.kiro/hooks/hooks.json`.

### 3.1 Hook Structure

```json
{
  "hooks": [
    {
      "id": "unique-id",
      "name": "Display Name",
      "description": "What this does",
      "trigger": {
        "type": "manual"  // or "onFileSave", "onSessionStart"
      },
      "action": {
        "type": "send-message",
        "message": "The prompt to send to Kiro"
      }
    }
  ]
}
```

### 3.2 Recommended Hooks

**Daily Standup:**
```json
{
  "id": "daily-standup",
  "name": "Daily Standup",
  "description": "Check tasks and plan the day",
  "trigger": { "type": "manual" },
  "action": {
    "type": "send-message",
    "message": "Read TASKS.md and tell me: 1) Which tasks are in progress? 2) Which can I start today? 3) Any blockers? Only report what's in the file."
  }
}
```

**Log Completed Work:**
```json
{
  "id": "log-work",
  "name": "Log Completed Work",
  "description": "Document what was done",
  "trigger": { "type": "manual" },
  "action": {
    "type": "send-message",
    "message": "I completed some work. Ask me: 1) What did I do? 2) What was the outcome? 3) Any issues? Then update the relevant docs. Do NOT invent details."
  }
}
```

**Sync After Meeting:**
```json
{
  "id": "sync-meeting",
  "name": "Sync After Meeting",
  "description": "Update docs after discussion",
  "trigger": { "type": "manual" },
  "action": {
    "type": "send-message",
    "message": "I had a meeting. I'll tell you what was decided. Update only the files I mention with only the decisions I state. Do NOT assume anything."
  }
}
```

### 3.3 Anti-Hallucination Patterns for Hooks

Always include phrases like:
- "Only report what's in the file"
- "Do NOT invent details"
- "Do NOT assume anything I don't state"
- "Ask me for specifics"

---

## Phase 4: MCP Servers

MCP servers give Kiro access to external tools. Config lives in `.kiro/settings/mcp.json`.

### 4.1 Finding MCP Servers

Resources:
- https://github.com/modelcontextprotocol/servers
- https://mcpservers.org
- Search GitHub for "[tool-name] mcp server"

### 4.2 MCP Config Structure

```json
{
  "mcpServers": {
    "server-name": {
      "command": "command-to-run",
      "args": ["arg1", "arg2"],
      "env": {
        "API_KEY": "${ENV_VAR_NAME}"
      },
      "disabled": false,
      "autoApprove": ["tool1", "tool2"]
    }
  }
}
```

### 4.3 Useful MCP Servers

| Server | Purpose | Install |
|--------|---------|---------|
| **Jina** | Web search, URL reading, query expansion | Remote (no install) |
| **arXiv** | Academic paper search/download | `uv tool install arxiv-mcp-server` |
| **GitHub** | Repo management | Built into Kiro |
| **Filesystem** | File operations | Built into Kiro |

### 4.4 Jina MCP (Recommended)

```json
{
  "mcpServers": {
    "jina": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.jina.ai/v1?exclude_tools=search_jina_blog,capture_screenshot_url"
      ],
      "env": {
        "JINA_API_KEY": "${JINA_API_KEY}"
      },
      "disabled": false,
      "autoApprove": ["read_url", "search_web"]
    }
  }
}
```

Get free API key at https://jina.ai

---

## Phase 5: Task Tracking

### 5.1 TASKS.md Template

```markdown
# Project Tasks
**Project:** [Name]
**Timeline:** [Start - End]

## Current Phase: [Phase Name]

### This Week

| # | Task | Owner | Status | Depends On |
|---|------|-------|--------|------------|
| 1.1 | [Task description] | [Name] | ⏳ Not Started | - |
| 1.2 | [Task description] | [Name] | 🔄 In Progress | 1.1 |

## Status Legend
- ⏳ Not Started
- 🔄 In Progress
- ✅ Done
- ❌ Blocked (add reason)
```

### 5.2 WORKFLOW.md Template

```markdown
# Workflow Guide

## Files to Read First
1. [Main context file]
2. [Task file]
3. [This workflow file]

## Daily Workflow

### Starting Work
1. Open Kiro
2. Trigger "Daily Standup" hook
3. Check TASKS.md

### During Work
- Use relevant steering: `#steering-name`
- Use MCP tools as needed

### After Completing Work
1. Trigger "Log Work" hook
2. Update TASKS.md

## Kiro Tools Summary

### Steering Files
| File | When | Purpose |
|------|------|---------|
| ... | ... | ... |

### Hooks
| Hook | When | Purpose |
|------|------|---------|
| ... | ... | ... |

### MCP Tools
| Tool | Purpose |
|------|---------|
| ... | ... |
```

---

## Phase 6: Anti-Hallucination Checklist

Before finalizing your setup, verify:

### Steering Files
- [ ] References actual source-of-truth files with `#[[file:]]`
- [ ] Lists what's NOT decided
- [ ] Has "never invent" rules
- [ ] Requires AI to cite sources

### Hooks
- [ ] Each hook says "do NOT invent/assume"
- [ ] Hooks ask for specifics rather than assuming
- [ ] Output goes to documented locations

### Overall
- [ ] Single source of truth exists (one main context file)
- [ ] Task status is tracked in one place
- [ ] AI suggestions are clearly labeled

---

## Quick Setup Checklist

```
□ Create .kiro/steering/project-assistant.md (core context)
□ Create TASKS.md (task tracking)
□ Create WORKFLOW.md (team guide)
□ Create .kiro/hooks/hooks.json (automation)
□ Create .kiro/settings/mcp.json (external tools)
□ Add file-match steering for common file types (optional)
□ Add manual steering for specific workflows (optional)
□ Test: Trigger daily standup hook
□ Test: Ask about project - verify it reads your files
```

---

## Example: Voice Agent SaaS Project

Here's how you might adapt this for an AI voice agent project:

### Steering Focus Areas
- API integrations (Twilio, OpenAI, etc.)
- Voice/audio processing patterns
- Real-time constraints
- Customer conversation flows

### Suggested Hooks
- "Log Customer Issue" - Document support cases
- "API Integration Check" - Verify external service status
- "Deploy Checklist" - Pre-deployment verification

### Useful MCPs
- Jina (web search, documentation reading)
- Database MCP (if available for your DB)
- Monitoring MCP (if available)

### File-Match Steering Ideas
- `"src/agents/**/*"` - Voice agent logic
- `"src/integrations/**/*"` - API integration patterns
- `"tests/**/*"` - Testing standards

---

## Maintenance

### Weekly
- Review TASKS.md accuracy
- Update steering if decisions changed

### When Adding Features
- Add relevant steering if new file patterns emerge
- Add hooks for new repeated workflows

### When Onboarding Team Members
- Have them read WORKFLOW.md first
- Walk through hook usage
- Verify they can trigger daily standup

---

## Troubleshooting

**Kiro doesn't have context:**
- Check steering files exist in `.kiro/steering/`
- Verify file references use correct paths
- Restart Kiro

**MCP not working:**
- Check command exists (`uv`, `npx`, etc.)
- Verify API keys are set
- Check `.kiro/settings/mcp.json` syntax

**AI inventing things:**
- Add stronger "do NOT" rules to steering
- Make hooks more explicit
- Ensure source-of-truth files are referenced

---

**Document Version:** 1.0  
**Last Updated:** January 2026  
**Based on:** Arabic RAG Query Enhancement project
