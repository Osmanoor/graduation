---
inclusion: manual
---

# Gemini CLI Delegation Guide

You have access to a Gemini CLI MCP server with these tools:

## When to Use Gemini

Use `gemini-cli` tools when:
- Task requires very large context (multiple papers, long documents)
- Multi-document synthesis or comparison
- Academic or technical deep research
- Complex reasoning that benefits from Gemini's context window

## Available Tools

1. **deep_research** - For research questions, synthesis, analysis
2. **summarize** - For condensing long content
3. **compare** - For structured comparisons

## Usage Pattern

1. Delegate the task fully to Gemini
2. Receive Gemini's detailed response
3. Summarize, contextualize, and adapt for the user's specific project
4. Apply project-specific knowledge (from RESEARCH_CONTEXT_KERNEL.md, TASKS.md)

## Example Delegation

For "Research Arabic RAG benchmarks":
```
Tool: gemini-cli.deep_research
Arguments:
  system: "You are a research assistant specializing in NLP. Be exhaustive and cite sources."
  prompt: "Research Arabic RAG benchmarks, datasets, and evaluation methods. Focus on MIRACL, ArabicMTEB, and recent 2024-2025 papers."
  model: "gemini-2.0-flash"
```

Then contextualize the result for the user's specific project constraints.
