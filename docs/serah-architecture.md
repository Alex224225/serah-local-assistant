# Serah — Local-First Assistant Architecture

> **Status of this document:** Describes the private production system. Components marked "Implemented in private system" are not runnable from this public repository. The `serah_demo` package (under `src/`) is the only code demonstrated here.

---

## Purpose

Serah is a personal AI assistant designed around one core principle: the human stays in control of every consequential action. She is not a chatbot and not an autonomous agent. She is a local research, memory, and accountability system that amplifies human decision-making without replacing it.

---

## Design Principles

### 1. Local-First Memory — *Implemented in private system*

Serah's memory lives in an Obsidian vault — a folder of plain Markdown files on a dedicated local machine. She does not depend on cloud memory, chat history, or any external service for her knowledge of ongoing projects, goals, and decisions.

This means memory persists across AI model changes and provider switches, memory is human-readable and auditable at any time, no conversation context limits apply to persistent knowledge, and the vault can be backed up, versioned, and exported like any codebase.

### 2. Outside Consultant Model — *Implemented in private system*

Claude and other LLMs are treated as outside consultants — called in for complex analysis, auditing, and synthesis. They are not Serah's brain. They do not hold her memory. When a Claude session ends, Serah's vault retains everything important.

This prevents a common failure mode: treating a stateless LLM session as a persistent agent and losing context on every reset.

### 3. Ask-Me-First Gates — *Implemented in private system*

Serah operates freely for low-risk local work (research, organisation, drafting, analysis). She must ask before any action in sensitive categories:

- Spending money or using paid APIs
- Trading financial instruments
- Deleting important files
- Installing major software
- Changing system or security settings
- Exposing local services online
- Sending emails or messages
- Connecting to bank or broker accounts
- Rewriting major project files

**Important:** These gates are behavioral controls enforced through prompt design and session structure. They are not complete technical security boundaries. Prompt instructions can be overridden if the system is misused or misconfigured. In the private system, additional code-level restrictions, process isolation, and tool permission settings provide further layers of protection. The gate system is one layer, not the whole defence.

### 4. Cheap-First Inference — *Implemented in private system*

Serah uses a local Ollama model for everyday cheap tasks: inbox processing, briefing generation, idea classification, health checks. Claude is called only when the task requires it — analysis, audit, complex synthesis.

This keeps operating costs near zero for routine operations and reserves the expensive model for high-value work.

---

## Memory Structure — *Implemented in private system*

Serah's vault uses a numbered folder convention that maps to her functional areas. The structure below is an example from the private system — these folders are not present in this public repository.

```
vault/                           # Private system — not in this repository
├── 00_Inbox/                    # Items waiting for human review
├── 01_Research/                 # Research queue, session notes, briefs
├── 02_Daily_Briefings/          # Auto-generated daily status briefings
├── 03_Idea_Proposals/           # Ideas surfaced for human approval
├── 04_Current_Goals/            # Active goals with status tracking
├── 05_Project_Masterpiece/      # Long-horizon creative/build project
├── 06_Trading_Journal/          # Research journal (private)
├── 07_Business_And_Opportunities/
├── 08_Mistakes_And_Lessons/     # Error log and lesson capture
├── 09_Self_Improvement/
├── 10_System_Rules/             # ASK_ME_FIRST.md, MISSION.md, operational rules
├── 11_Context_Packs/            # Handoff packs, status snapshots, task tickets
└── 99_Archive/
```

Each folder has a defined purpose and defined content lifetime. Nothing is stored in the vault without intention.

---

## Operational Loop — *Implemented in private system*

Serah's daily cycle follows a structured loop:

**1. Briefing Generation.** Serah (or Claude) generates a daily briefing from vault state: current goals, pending inbox items, recent decisions, suggested focus.

**2. Inbox Review.** Human reviews flagged items. Each item gets a decision: continue / save for later / archive / forget.

**3. Research.** Serah runs approved research tasks, writes structured briefs to the research folder. Sources are captured. Findings are proposals, not actions.

**4. Idea Proposals.** Serah surfaces ideas for human review. No idea becomes a project without explicit human approval.

**5. Goal Tracking.** Goals are updated based on session outcomes. Goals have a defined status: active / paused / complete / dropped.

**6. Lesson Capture.** Mistakes or unexpected outcomes are logged immediately.

---

## How Claude Fits In — *Implemented in private system*

Claude is called as an outside analyst in specific scenarios:

| Scenario | What Claude does |
|---|---|
| Research brief synthesis | Reads approved sources, writes structured brief |
| Trading candidate audit | Runs 18-item checklist, returns a verdict |
| System design review | Reviews policies, flags gaps, proposes improvements |
| Context handoff | Rebuilds status snapshot when vault state changes significantly |

Claude's outputs always go into the vault as proposals. The human reads them, decides what to keep, and updates the vault accordingly. Claude cannot write to the vault directly or trigger any action outside the conversation.

---

## What Serah Is Not

**Not autonomous.** She does not take consequential actions without human approval.

**Not always-on.** She runs on demand and on schedule, not continuously.

**Not a trading bot.** The Opportunity Engine (a separate research-only case study) does not place orders autonomously. See [trading-safety-harness-case-study.md](trading-safety-harness-case-study.md).

**Not a replacement for judgment.** She amplifies research capacity and reduces friction, but human judgment is the final gate for every decision.

---

## Private System Build Phase

The following components are operational in the private system (not demonstrated in this repository):

- Obsidian vault structure and naming conventions
- Ask-Me-First gate enforcement in Claude prompt design
- Local Ollama model for cheap inference tasks
- Briefing generation, inbox review loop, idea proposal cycle
- Research queue and structured research brief format
- Context pack / handoff system for Claude session continuity
- Opportunity Engine (see case study)

What is demonstrated in this repository: the `serah_demo` package, which shows the evidence-packet pipeline (packet building, validation, report generation) using synthetic local data. See `src/serah_demo/` and `examples/`.

---

## Planned — Not Yet Implemented

- Voice interface integration
- Browser-controlled research automation with per-source approval
- Local dashboard
