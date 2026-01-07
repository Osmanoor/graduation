# Kiro Research Assistant Configuration

## 1. Context Analysis Summary

### Current Project Phase
**Phase 1: Baseline Implementation (Weeks 1-3 of 6)**
- Setting up MIRACL dataset
- Implementing Dense and BM25 retrievers separately
- Establishing evaluation pipeline

### Immediate Priorities
1. Download and configure MIRACL Arabic dataset
2. Implement BM25 baseline (simpler, no GPU needed)
3. Research embedding model costs for Dense baseline
4. Set up evaluation pipeline (Recall@10, NDCG@10, MRR)

### Key Blockers / Open Questions
| Question | Status | Impact |
|----------|--------|--------|
| Embedding model selection | Under Investigation | Blocks Dense baseline |
| First QE technique | Decide after baseline | Blocks Phase 2 |
| Arabic LLM for QE | Under Investigation | Blocks enhancement layer |
| MIRACL storage/compute | Planning | 2.1M passages = ~50GB |

### Task Types I'll Help With
- Literature search and paper summarization
- Experiment design and documentation
- Code review and debugging (Python, retrieval systems)
- Thesis chapter drafting
- Decision documentation
- Meeting preparation

---

## 2. Steering Files Created

### Always-Included
| File | Purpose |
|------|---------|
| `research-assistant.md` | Core project context, decisions, behavior rules |

### File-Match Conditional
| File | Trigger Pattern | Purpose |
|------|-----------------|---------|
| `paper-analysis.md` | `papers/**/*.md` | Paper summary template |
| `experiment-documentation.md` | `**/exp_*.md`, `**/experiment*.md` | Experiment doc standards |
| `thesis-writing.md` | `**/*.tex`, `**/chapter*.md` | Thesis writing guidelines |

### Manual-Inclusion (use #steering-name in chat)
| File | Purpose |
|------|---------|
| `baseline-implementation.md` | Code patterns for baseline setup |
| `literature-search.md` | Paper search workflow |

---

## 3. Hooks Configured

### Manual Hooks (click to trigger)
| Hook | Description |
|------|-------------|
| **Update Experiment Log** | Document a completed experiment |
| **Summarize Paper** | Create structured paper summary |
| **Daily Research Standup** | Plan the day's work |
| **Sync Decision Status** | Update docs after meeting |
| **Prepare Supervisor Meeting** | Generate meeting materials |

### Automatic Hooks (on file save)
| Hook | Trigger | Action |
|------|---------|--------|
| **Validate Experiment Doc** | Save `exp_*.md` | Check completeness |
| **Check Paper Format** | Save `papers/*.md` | Validate template |

---

## 4. MCP Servers Configured

### `.kiro/settings/mcp.json`
```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-mcp-server"],
      "autoApprove": ["search_papers", "list_papers", "read_paper"]
    },
    "semantic-scholar": {
      "command": "uvx", 
      "args": ["semanticscholar-mcp-server"],
      "autoApprove": ["search_papers", "get_paper", "get_citations"]
    },
    "huggingface": {
      "command": "npx",
      "args": ["-y", "@huggingface/mcp-server"],
      "autoApprove": ["search_datasets", "search_models"]
    }
  }
}
```

### Prerequisites
```bash
# Install uv (Python package manager with uvx)
pip install uv
# or on Windows: winget install astral-sh.uv

# Node.js required for HuggingFace MCP
# Already have npm? You're set.
```

### What Each Server Provides
- **arXiv:** Search papers, download PDFs, read content
- **Semantic Scholar:** Citation networks, paper metadata, author info
- **HuggingFace:** Search models, datasets, papers on HF Hub

---

## 5. Multi-IDE Strategy: Kiro vs Anti-Gravity (Gemini 2.5 Pro)

### Task Allocation

| Task | Best Tool | Rationale |
|------|-----------|-----------|
| **Code implementation** | Kiro | File system access, debugging |
| **Quick iterations** | Kiro | Fast responses, tool integration |
| **Paper deep-dives** | Anti-Gravity | 1M context for full papers |
| **Literature synthesis** | Anti-Gravity | Compare 10+ papers at once |
| **Thesis chapter drafts** | Anti-Gravity | Long-form generation |
| **Experiment debugging** | Kiro | Code execution, file access |
| **Meeting prep** | Kiro | Access to project files |
| **Arabic text analysis** | Anti-Gravity | Better multilingual handling |

### Context Handoff Protocol

**Kiro → Anti-Gravity:**
1. Export relevant context to a markdown file
2. Include: Current decisions, specific question, relevant paper summaries
3. Paste into Anti-Gravity with clear task description

**Anti-Gravity → Kiro:**
1. Copy output (paper summary, chapter draft, analysis)
2. Save to appropriate location in project
3. Use Kiro hooks to validate/integrate

### Shared Artifacts
- All documents live in this repo (single source of truth)
- Anti-Gravity outputs saved to `/gemini_opinions/` or appropriate folder
- Kiro validates and integrates into project structure

---

## 6. Spec Templates Created

Location: `.kiro/specs/templates/`

| Template | Use Case |
|----------|----------|
| `thesis-chapter-spec.md` | Planning a thesis chapter |
| `paper-analysis-spec.md` | Deep-diving into a paper |
| `experiment-spec.md` | Designing an experiment |

### How to Use Specs
1. Copy template to `.kiro/specs/[name].md`
2. Fill in requirements section
3. Work through design with Kiro
4. Execute tasks with checkboxes

---

## 7. Implementation Checklist

### Immediate (Do Now)
- [x] Create `.kiro/steering/research-assistant.md`
- [x] Create `.kiro/steering/paper-analysis.md`
- [x] Create `.kiro/steering/experiment-documentation.md`
- [x] Create `.kiro/steering/thesis-writing.md`
- [x] Create `.kiro/steering/baseline-implementation.md`
- [x] Create `.kiro/steering/literature-search.md`
- [x] Create `.kiro/settings/mcp.json`
- [x] Create `.kiro/hooks/hooks.json`
- [x] Create spec templates

### Setup Required (Manual Steps)
- [ ] Install `uv` for MCP servers: `pip install uv`
- [ ] Restart Kiro to load MCP servers
- [ ] Test MCP servers: Ask "Search arXiv for Arabic RAG papers"
- [ ] Create `experiments/` folder for experiment docs
- [ ] Verify hooks appear in Kiro's Agent Hooks panel

### First Use
- [ ] Trigger "Daily Research Standup" hook
- [ ] Test paper summarization with a new paper
- [ ] Run baseline implementation with `#baseline-implementation` steering

---

## Quick Reference

### Chat Commands
- `#baseline-implementation` - Load baseline coding guide
- `#literature-search` - Load paper search workflow
- `#File:RESEARCH_CONTEXT_KERNEL.md.md` - Load project overview
- `#Folder:papers` - Load all paper summaries

### Hook Triggers
- Open Agent Hooks panel in Kiro sidebar
- Click hook name to trigger
- Automatic hooks fire on file save

### Key Project Files
```
RESEARCH_CONTEXT_KERNEL.md.md     # Start here
meetings/6.1.2026_meeting_outcomes.md  # Latest decisions
research_decisions/open_questions.md   # What needs research
research_decisions/technical_specifications.md  # Architecture
```
