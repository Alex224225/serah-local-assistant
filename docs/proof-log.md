# Proof Log — Build and Test Evidence

> **Scope**: This document describes activity in the **private system** (not included in this
> public repository). All file paths, scanner configurations, agent logs, and brokerage read
> references shown here are **examples from the private system**. They are documented here for
> transparency and auditability, not as runnable public code.

This document records what was actually built, tested, and run. It is a factual log of system
activity, not a claims document. All entries are from dry-run mode. Zero real orders were
placed at any point.

---

## Status Legend

| Label | Meaning |
|-------|---------|
| **Implemented in private system** | Exists and runs in the private system; not available in this repository |
| **Demonstrated in this repository** | Working code in this public repo |
| **Planned** | Intended for future implementation |
| **Experimental** | Under active exploration |

---

## System Initialization

*Implemented in private system. File paths below are examples from the private system and are
not included in this public repository.*

| Date | Component | What Happened |
|------|-----------|---------------|
| 2026-06-14 | TradingSystem vault | Folder structure created, policy documents written, safety rules finalized |
| 2026-06-14 | Fast Mover Scanner v1 | First scanner run completed in test mode (market closed) |
| 2026-06-14 | Config/ScannerConfig.json *(private)* | Scanner configuration written and validated |
| 2026-06-14 | Data/ScannerUniverse *(private)* | Initial ticker universe defined |
| 2026-06-14 | Safety policy | All hard rules finalized and documented |
| 2026-06-14 | Read-only connection test | Brokerage account status confirmed via read-only calls only |
| 2026-06-15 | Scanner scheduling *(private)* | Scheduling tasks installed |
| 2026-06-15 | Scanner preflight | First preflight check passed |

---

## Scanner Run History

*Implemented in private system. All runs use delayed public market data. All output is stamped
"Research Lead Only — No trade action taken."*

Alert files are stored in the private system at a path of the form:
`Data/ScannerAlerts/YYYY-MM-DD_alerts.jsonl` *(private system — not included in this repository)*.

Multiple scheduled scan sessions were completed across several days in June 2026. Each session
produced alert files covering various tickers. No session resulted in any order being placed.

---

## Dry-Run Audit Sessions

*Implemented in private system.*

Six dry-run scans have been completed. In each session:

- Scanner alert data was reviewed.
- Candidates were evaluated against an audit checklist.
- No trade verdicts have been issued (0/10 per engine).
- No orders were placed.

Representative candidates were reviewed and rejected across sessions for reasons including:
high extension (parabolic risk), delayed data (volume not confirmed), missing stock-specific
catalyst, weak relative volume, and insufficient spread data.

A data sanity check detected a hallucinated price during one session: a web search returned
a price that differed significantly from the brokerage read-only feed. The discrepancy was
flagged, the web result was discarded, and the brokerage quote was used as ground truth.
This is an example of the data sanity check functioning correctly.

---

## Opportunity Engine Development

*Implemented in private system.*

| Date | Milestone |
|------|-----------|
| 2026-06-15 | Packet schema (v1.0) defined |
| 2026-06-15 | Packet validator written and tested |
| 2026-06-15 | v1 alert adapter written |
| 2026-06-16 | Capital allocation policy written — two engines defined |
| 2026-06-16 | Shadow live dry-run module written |
| 2026-06-17 | Full test suite written |
| 2026-06-17 | Replay module written |
| 2026-06-17 | Operator status report module written |
| 2026-06-18 | Handoff module written |
| 2026-06-18 | Shadow dry-run run on real June 18 alert data — 3 sessions |

Shadow dry-run session files are stored in the private system. Each produced a candidate list
with tier assignments and missing fields. No packets were automatically sent to the AI auditor.
Human initiation is required for the audit step.

---

## Agent Test Results

*Implemented in private system. The public repository demonstrates equivalent validation logic
in `src/serah_demo/validator.py` (Demonstrated in this repository).*

Two AI sub-agents were defined and tested in the private system:

**Data Sanity Auditor**
- Test type: Injected candidate with deliberate errors
- Expected verdict: WATCH — DATA MISMATCH
- Actual verdict: WATCH — DATA MISMATCH
- Result: **PASS** — agent correctly identified all injected errors
- Safety confirmation: No scanner executed; no brokerage call made; no web search run;
  no files edited by agent; no order placed, cancelled, modified, drafted, or reviewed.

**Risk Officer**
- Test type: Injected dangerous candidate (extreme extension, no stop loss, missing catalyst)
- Expected verdict: REJECT
- Actual verdict: REJECT
- Result: **PASS** — agent correctly blocked the candidate
- Safety confirmation: Same as above — no brokerage calls, no orders, no file edits.

Note: These prompt-based controls are behavioral guardrails. They are not complete technical
security boundaries. Code-level isolation, process permissions, and the explicit
human-confirmation gate provide additional enforcement layers.

---

## Live Eligibility Status

*Implemented in private system.*

| Field | Value |
|-------|-------|
| System mode | DRY RUN ONLY |
| Dry-run scans completed (system-wide) | 6 |
| Normal/Core engine — valid PAPER TRADE ONLY signals | 0 / 10 |
| Normal/Core engine — live eligibility | BLOCKED |
| Fast Runner engine — valid PAPER TRADE ONLY signals | 0 / 10 |
| Fast Runner engine — live eligibility | BLOCKED |
| System-wide live trading | BLOCKED |
| Orders placed | 0 |
| Policy violations | 0 |

Live trading will remain BLOCKED until:

1. The relevant engine accumulates 10 valid PAPER TRADE ONLY signals (not scanner alerts,
   not test data — real-session AI-audited verdicts).
2. **AND** the account holder activates the **explicit human-confirmation gate** (types the
   designated confirmation phrase in that session).

Neither condition is currently met. No eligibility review is active.

---

## What Has Never Happened

For the avoidance of any ambiguity:

- No real order has been placed, reviewed, drafted, or cancelled by this system.
- No brokerage account has been modified.
- The scanner has never called any brokerage API to place or review orders.
- No AI session has ever had access to place orders (the explicit human-confirmation gate
  has never been activated).
- No live trading eligibility has been reached (0/10 signals on both engines).
- No real capital has been deployed.
- No simulated profit or loss figures exist.
- No backtests have been marked as live-eligible.
