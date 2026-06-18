# Serah — Local-First Personal AI Assistant + Trading Safety Harness

A personal AI system built to research, plan, and stay accountable — with a separate
research-only trading harness that enforces safety gates before any analysis reaches
a human decision point.

> **Status:** Active development. All trading components are dry-run only.
> Zero real orders have been placed.

---

## What This Is

**Serah** is a local-first personal AI assistant. She lives on a dedicated machine,
uses a local Obsidian vault as persistent memory, and treats Claude and other LLMs as
outside consultants rather than her own brain. She is built to:

- Maintain a daily briefing and accountability loop
- Manage a structured research queue and decision inbox
- Propose ideas and wait for explicit human approval before acting on anything risky
- Run local AI (Ollama) for cheap everyday tasks, escalate to Claude for complex analysis
- Learn from approved internet research without autonomous browsing

**The Trading Safety Harness** is a separate sub-project built on top of Serah's
infrastructure. It demonstrates how to wire an LLM-based research pipeline with
hard safety gates so that analysis never becomes action without explicit human
confirmation. It is a research and safety-engineering portfolio project — not a
live trading system.

---

## Repository Layout

```
serah-local-assistant/
├── README.md                          # This file
├── docs/
│   ├── serah-architecture.md          # How Serah works as a local assistant
│   ├── trading-safety-harness-case-study.md  # The safety harness in detail
│   ├── opportunity-engine-overview.md # Evidence packet pipeline
│   └── proof-log.md                   # Dry-run run history and test evidence
└── assets/
    └── README.md                      # Diagrams and screenshots (see note)
```

> The full source code (scanner, opportunity engine, agent definitions, policy docs)
> lives in a private repository. This export contains documentation and architecture
> artifacts only. Source code is available on request with context.

---

## Project Highlights

### Serah Local Assistant
- Local-first architecture: Obsidian vault as memory, Ollama for cheap inference
- Ask-Me-First gate system covering ~15 action categories
- Structured inbox, research queue, daily briefing, and idea proposal loop
- Claude used as an outside reviewer, not as autonomous agent
- No cloud dependency for core memory or daily operations

### Trading Safety Harness
- **Scanner:** Python + Yahoo Finance (free tier, ~15-min delayed data). Writes research
  leads to flat files. Has no connection to any broker. No order logic exists in the
  scanner code.
- **Opportunity Engine:** Structured JSON evidence packets with strict schema validation.
  A candidate cannot reach Claude for audit without passing schema gates first.
- **Claude Audit:** 18-item checklist required for every candidate. Claude acts as
  analyst/auditor, not as order-placer.
- **Kill Switch:** No order can be placed unless the human types an exact confirmation
  phrase in that session. Paraphrases do not count.
- **Dry-Run Requirement:** 10 valid audit-cleared signals per engine are required before
  live eligibility could even be considered. The system is currently at 0/10.
- **Orders placed to date: 0**

---

## Tech Stack

| Component | Technology |
|---|---|
| Memory / vault | Obsidian (local markdown) |
| Local inference | Ollama (llama3.2:3b) |
| LLM analyst | Claude (via Claude Code) |
| Scanner data | Yahoo Finance via `yfinance` (free tier) |
| Scanner language | Python 3.9+ |
| Agent definitions | Claude Code `.claude/agents/` |
| Scheduling | Windows Task Scheduler (bat scripts) |
| Data format | Flat files: `.jsonl`, `.json`, `.md` |
| Version control | Git |

---

## Safety Philosophy

This project treats LLM-based automation as a **research amplifier**, not a
decision-maker. Every layer of the system is designed so that:

1. The LLM (Claude) can read, analyze, and report — but cannot act unilaterally
2. Human approval is required at every gate that touches real resources
3. Automation produces structured evidence, not conclusions
4. The human reads the evidence and decides

The trading harness applies this philosophy to financial research specifically, because
financial mistakes are expensive and irreversible. The goal is to demonstrate that
AI-assisted research pipelines can be made safe by design, not just by instruction.

---

## What Is Intentionally Excluded from This Export

- Account numbers, account types, or broker identifiers
- Account balances or position details
- Live brokerage connection settings or MCP tool configurations
- Private Obsidian vault notes (daily journals, session logs, personal goals)
- Local machine paths
- Any file that contains live order protocols or Claude order-placement prompts
- Screenshots of brokerage interfaces

See `docs/trading-safety-harness-case-study.md` for a full list of exclusions.

---

## Status

| Component | Status |
|---|---|
| Serah local assistant | Active — foundation phase complete |
| Scanner (Python) | Active — running daily on schedule |
| Opportunity engine | Active — test packets generating |
| Claude audit pipeline | Active — dry-run tested |
| Agent definitions (data-sanity-auditor, risk-officer) | Active — validated |
| Live trading eligibility | BLOCKED — 0/10 signals per engine |
| Real orders placed | 0 |

### Futures Learning Track

The current public export is focused mainly on equity-style scanner research, but the broader learning track also includes futures market structure.

Futures are treated as an education and research topic only. The system does not trade futures, does not place futures orders, and does not connect to any futures broker. Futures-related work is limited to learning concepts such as contract specifications, leverage, margin requirements, tick size, session structure, liquidity, risk controls, and why futures require stricter safety rules than basic stock research.

Any future futures-related module would remain dry-run only and would require a separate packet schema, risk checks, position-sizing rules, and safety gates before any live use could even be considered.

Current futures status: education and research only. No futures orders, no futures broker connection, and no live futures trading.

| Futures learning track | Education/research only — no broker connection, no live trading |
