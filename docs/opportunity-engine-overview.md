# Opportunity Engine — Overview

> **Status:** This document describes components implemented in the private system. The public `serah_demo` package demonstrates the packet schema, validation, and report-generation concepts using synthetic data. No live scanner, brokerage connection, or market data access is present in this public repository.

---

## What It Is

The Opportunity Engine is the middle layer of the Trading Safety Harness pipeline. It sits between the scanner (which identifies market candidates) and the Claude audit (which evaluates them). Its job is to take a raw scanner alert and transform it into a structured, validated, schema-compliant evidence packet that Claude can audit reliably.

---

## Why It Exists

A scanner produces alerts. An alert is a market observation: a ticker moved a certain percentage with a certain volume. That is not enough information for a disciplined audit.

To audit a candidate properly, you need exact price and move with a named data source and explicit freshness label, volume in multiple forms (session volume, average daily volume, relative volume), spread to assess execution feasibility, catalyst details (what drove the move, when, sourced from where), market context (is the broader market moving with or against this candidate?), risk flags, and an explicit list of what data is missing and why.

The opportunity engine builds that complete picture, or explicitly records what it could not fill in. Claude receives the complete packet — including the missing_fields list — and factors the gaps into the audit verdict.

---

## Module Architecture — *Implemented in private system*

The private system contains the following modules. The module descriptions are provided as documentation; none of this source code is included in this public repository.

```
opportunity_engine/              # Private system — not in this repository
├── packet_schema.py             # Canonical packet structure and field types
├── packet_validator.py          # Validates a packet against the schema
├── v1_alert_adapter.py          # Converts scanner alerts into opportunity packets
├── claude_candidate_queue.py    # Manages packets awaiting Claude audit
├── claude_review_packet_builder.py  # Formats a packet for Claude audit
├── runtime_writer.py            # Writes runtime events to the archive log
├── shadow_live_dry_run.py       # Simulates a live dry-run session
├── replay_v1_alerts.py          # Replays historical alert files through the engine
├── handoff.py                   # Produces operator status reports
├── operator_status_report.py    # Formats current engine state for human review
├── paper_exit_strategy.py       # Generates paper exit tracking
└── test_*.py                    # Test suite (12 test files, one per module)
```

The public `serah_demo` package (`src/serah_demo/`) provides a minimal, runnable demonstration of the core concepts: schema definition, validation, packet building, and report generation using synthetic data.

---

## Packet Schema

Every candidate in the system is represented as a JSON packet conforming to the opportunity engine schema. A synthetic example is available at `examples/valid_packet.json`.

### Required Top-Level Fields

| Field | Type | Notes |
|---|---|---|
| schema_version | string | Document version for forward compatibility |
| status | string | Must be "Research Lead Only" on creation |
| no_trade_statement | string | Must be "No trade action taken" |
| timestamp_utc | ISO 8601 string | When data was captured |
| timestamp_et | ISO 8601 string | Eastern Time equivalent |
| trading_date | date string | YYYY-MM-DD |
| ticker | string | Exchange ticker symbol |
| exchange | string | e.g., NMS, NYQ |
| quote_type | string | e.g., EQUITY |
| price | float | Last price at capture |
| prev_close | float | Prior session close |
| move_pct | float | Calculated percent move |
| data_source | string | Named source string |
| data_freshness | string | Explicit freshness label |
| tier | integer | 1–4, computed by engine |
| tier_reason | string | Plain-English tier justification |
| risk_flags | array | Risk flag strings (may be empty array, never null) |
| missing_fields | array | Fields the engine could not populate |
| modules_fired | array | Which engine modules ran on this packet |

### Required Sub-Object Fields

**volume{}** — current_session_volume (integer, required), adv_20d, adv_30d, rvol_current, rvol_projected (floats or null, null triggers missing_fields entry), dollar_volume, source (named string), timestamp.

**spread{}** — bid, ask, spread_pct (floats), valid (boolean).

**catalyst{}** — present (boolean), type (string or null), source (string or null, named not generic), source_date, event_date (dates or null), freshness (fresh / stale / unknown).

**setup{}**, **regime{}**, **trade_skeleton_idea{}** — structured objects with defined fields. Claude populates trade_skeleton_idea during audit.

---

## Tier System

Every packet is assigned a tier (1–4) based on data quality and volume evidence. Tier governs how Claude should weight the candidate and what additional checks apply.

| Tier | Criteria | Audit Weight |
|---|---|---|
| 1 | RVOL < 1.0x, or delayed data with no confirmation | Weakest — additional scepticism required |
| 2 | RVOL 1.0x–1.49x, or one volume metric missing | Moderate — standard checklist applies |
| 3 | RVOL >= 1.5x, all volume fields populated | Strong — qualifies for audit |
| 4 | RVOL >= 2.0x, catalyst confirmed, spread tight | Strongest — highest audit priority |

A Tier 1 candidate cannot receive a PAPER TRADE ONLY verdict without explicit justification. In practice, most Tier 1 candidates receive WATCH or REJECT.

---

## Shadow Live Dry-Run — *Implemented in private system*

The shadow_live_dry_run module in the private system simulates what would happen in a live session by replaying real alert files through the full engine pipeline and logging what packets would have been sent to Claude for audit. Shadow dry-run sessions run on real market data from the scanner but produce no trades and send nothing to Claude automatically. A human must initiate the Claude audit step.

Shadow dry-run output files referenced in `docs/proof-log.md` exist in the private system only, under a path structured as `Reports/OpportunityEngine/ShadowLiveDryRuns/` (private system path — not present in this repository).

---

## Test Coverage — *Implemented in private system*

The private system contains 12 test files, one per module. All tests run without a live brokerage connection, without internet access, and without Claude API calls. They use synthetic or historical data only.

The public `tests/test_demo.py` file tests the `serah_demo` package using synthetic fixtures.
