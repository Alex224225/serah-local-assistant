# Serah — Local-First Assistant Architecture

## Purpose

Serah is a personal AI assistant designed around one core principle: **the human stays
in control of every consequential action**. She is not a chatbot and not an autonomous
agent. She is a local research, memory, and accountability system that amplifies human
decision-making without replacing it.

---

## Design Principles

### 1. Local-First Memory
Serah's memory lives in an Obsidian vault — a folder of plain markdown files on a
dedicated local machine. She does not depend on cloud memory, chat history, or any
external service for her knowledge of ongoing projects, goals, and decisions.

This means:
- Memory persists across AI model changes and provider switches
- Memory is human-readable and auditable at any time
- No conversation context limits apply to persistent knowledge
- The vault can be backed up, versioned, and exported like any codebase

### 2. Outside Consultant Model
Claude and other LLMs are treated as **outside consultants** — called in for complex
analysis, auditing, and synthesis. They are not Serah's brain. They do not hold her
memory. When a Claude session ends, Serah's vault retains everything important.

This prevents a common failure mode: treating a stateless LLM session as a persistent
agent and losing context on every reset.

### 3. Ask-Me-First Gates
Serah operates freely for low-risk local work (research, organization, drafting,
analysis). She must ask before any action in approximately 15 categories:

- Spending money or using paid APIs
- Trading financial instruments
- Deleting important files
- Installing major software
- Changing system or security settings
- Exposing local services online
- Sending emails or messages
- Connecting to bank or broker accounts
- Rewriting major project files

This is enforced at the system design level, not just by instruction. Claude prompts
are structured so that outputs are always proposals, never actions.

### 4. Cheap-First Inference
Serah uses a local Ollama model (llama3.2:3b) for everyday cheap tasks: inbox
processing, briefing generation, idea classification, health checks. Claude is called
only when the task requires it — analysis, audit, complex synthesis.

This keeps operating costs near zero for routine operations and reserves the expensive
model for high-value work.

---

## Memory Structure

Serah's vault uses a numbered folder convention that maps to her functional areas:

```
vault/
├── 00_Inbox/          # Items waiting for human review and decision
├── 01_Research/       # Research queue, session notes, approved research briefs
├── 02_Daily_Briefings/ # Auto-generated daily status briefings
├── 03_Idea_Proposals/ # Ideas Serah surfaces for human approval
├── 04_Current_Goals/  # Active goals with status tracking
├── 05_Project_Masterpiece/  # Long-horizon creative/build project
├── 06_Trading_Journal/      # Trading research journal (private)
├── 07_Business_And_Opportunities/  # Business and financial opportunity tracking
├── 08_Mistakes_And_Lessons/        # Error log and lesson capture
├── 09_Self_Improvement/            # Personal growth tracking
├── 10_System_Rules/   # ASK_ME_FIRST.md, MISSION.md, operational rules
├── 11_Context_Packs/  # Handoff packs, status snapshots, Claude task tickets
└── 99_Archive/        # Completed items
```

Each folder has a defined purpose and a defined lifetime for its contents. Nothing
is stored in the vault that is not intentional.

---

## Operational Loop

Serah's daily cycle follows a structured loop:

```
1. BRIEFING GENERATION
   Serah (or Claude) generates a daily briefing from vault state:
   current goals, pending inbox items, recent decisions, suggested focus.

2. INBOX REVIEW
   Human reviews flagged items in 00_Inbox/.
   Each item gets a decision: continue / save for later / archive / forget.

3. RESEARCH
   Serah runs approved research tasks, writes structured briefs to 01_Research/.
   Sources are captured. Findings are proposals, not actions.

4. IDEA PROPOSALS
   Serah surfaces ideas to 03_Idea_Proposals/ for human review.
   No idea becomes a project without explicit human approval.

5. GOAL TRACKING
   04_Current_Goals/ is updated based on session outcomes.
   Goals have status: active / paused / complete / dropped.

6. LESSON CAPTURE
   Mistakes or unexpected outcomes are logged immediately.
   No mistake is too small to record.
```

---

## How Claude Fits In

Claude is called as an outside analyst in specific scenarios:

| Scenario | What Claude does |
|---|---|
| Research brief synthesis | Reads approved sources, writes structured brief |
| Trading candidate audit | Runs 18-item checklist, returns a verdict (PASS/WATCH/REJECT) |
| System design review | Reviews policies, flags gaps, proposes improvements |
| Context handoff | Rebuilds status snapshot when vault state changes significantly |

Claude's outputs always go into the vault as proposals. The human reads them,
decides what to keep, and updates the vault accordingly. Claude cannot write to the
vault directly or trigger any action outside the conversation.

---

## What Serah Is Not

- **Not autonomous:** She does not take consequential actions without human approval.
- **Not always-on:** She runs on demand and on schedule, not continuously.
- **Not a trading bot:** The trading harness (separate sub-project) is a research
  and safety-gate system. It does not place orders autonomously. See the
  trading safety harness case study.
- **Not a replacement for judgment:** She amplifies research capacity and reduces
  friction, but human judgment is the final gate for every decision.

---

## Current Build Phase

Foundation phase is complete. The following components are operational:

- Obsidian vault structure and naming conventions
- Ask-Me-First gate enforcement in Claude prompt design
- Local Ollama model for cheap inference tasks
- Briefing generation, inbox review loop, idea proposal cycle
- Research queue and structured research brief format
- Context pack / handoff system for Claude session continuity
- Trading safety harness (see separate case study)

Next phases planned: voice interface integration, browser-controlled research
automation with per-source approval, and a local dashboard.
