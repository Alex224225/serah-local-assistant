# Trading Safety Harness / Opportunity Engine

*Portfolio Case Study*

---

## Purpose

The Trading Safety Harness is a research and safety-engineering sub-project built
on top of the Serah local assistant infrastructure.

Its goal is to demonstrate that an LLM-assisted financial research pipeline can be
made safe by design — not just by instruction — by enforcing hard gates at every
layer between a market observation and a human trade decision.

**This is not a trading bot.** It is a research amplifier with a built-in referee
system. The human is the only entity in the system that can place an order, and only
after the system has produced and audited a structured evidence packet.

**Orders placed to date: 0.**

---

## The Core Problem It Solves

LLM-assisted trading research creates a specific failure mode: the model sounds
confident, the analysis looks plausible, and the human accepts the output without
verifying the underlying data. If the model hallucinated a price, a catalyst, or
a volume figure, the human may never catch it.

The Trading Safety Harness solves this by:

1. Never trusting a single data source
2. Never letting the model produce a "buy" recommendation from unvalidated inputs
3. Requiring structured evidence before Claude even sees a candidate
4. Having Claude audit that evidence against a fixed 18-item checklist, not free-form
5. Blocking order placement behind an explicit typed confirmation phrase in every session

---

## Architecture

```
Yahoo Finance (yfinance, free tier, ~15-min delayed)
        |
        v
[Fast Mover Scanner]
   Python script
   Runs on schedule (market hours)
   No Robinhood connection. No order logic.
   Output: Research Lead Only
        |
        v
[Alert Files] (.jsonl flat files)
   One file per trading day
   Each alert: ticker, price, move%, volume, spread, scoring
   Status stamped: "Research Lead Only — No trade action taken"
        |
        v
[Opportunity Engine]
   Python module suite
   Validates alert against packet schema (required fields, types, ranges)
   Builds structured JSON evidence packet
   Computes tier (Tier 1–4 based on data quality and volume confirmation)
        |
        v
[Claude Audit] (human-initiated)
   Claude receives a candidate packet
   Runs 18-item audit checklist:
     - Data sanity check (math verification)
     - Market data freshness gate (timestamp validation)
     - Web search date lock (catalyst must be dated, source named)
     - Volume confirmation (numeric RVOL required)
     - Extension check (parabolic risk flag)
     - Spread check (execution feasibility)
     - Catalyst quality check
     - Halt risk assessment
     - Float / dilution flags
     - Regime check (market context)
     - ... and more
   Returns: PAPER TRADE ONLY / WATCH / REJECT
        |
        v
[Human Decision Point]
   Human reads the Claude audit verdict and evidence packet
   Human decides whether to act
   If acting: must type exact confirmation phrase in that session
   No abbreviation or paraphrase accepted
        |
        v
[Zero orders placed]
   System is in DRY RUN ONLY mode.
   Live trading requires 10 valid PAPER TRADE ONLY signals per engine.
   Current count: 0/10 (both engines).
```

---

## Safety Design

### Layer 1 — Scanner Isolation
The scanner Python script has no connection to any brokerage API. It contains no
order logic, no account references, and no trade execution code. It reads from Yahoo
Finance and writes to flat files. This is verifiable by reading the source.

### Layer 2 — Research Lead Stamp
Every scanner alert is stamped with two mandatory fields:

```json
"status": "Research Lead Only",
"no_trade_statement": "No trade action taken"
```

These fields are required by schema. An alert without them fails validation and
cannot enter the opportunity engine.

### Layer 3 — Schema Validation
The opportunity engine validates every packet against a strict schema before Claude
sees it. Required fields include:
- Numeric price, volume, and spread (not null, not zero)
- Named data source with explicit freshness label
- Ticker exchange and quote type
- Risk flags array (populated even if empty)
- Missing fields array (explicitly listed)

A packet with missing required fields is flagged with a `missing_fields` list and
tiered down. Claude sees the missing fields and factors them into the audit.

### Layer 4 — Data Sanity Auditor Agent
A dedicated Claude sub-agent (`data-sanity-auditor`) verifies math before the main
audit runs. It checks:
- Is the claimed price move mathematically consistent with the bid/ask?
- Does the volume figure make sense given the time of day?
- Are there contradictions between fields?

The auditor returns PASS, WATCH — DATA MISMATCH, or REJECT — DATA INVALID.
A REJECT here ends the audit. No further analysis is produced.

### Layer 5 — 18-Item Claude Audit Checklist
The main audit is structured as a numbered checklist, not free-form analysis. Claude
must address each item explicitly. The verdict options are:

| Verdict | Meaning |
|---|---|
| PAPER TRADE ONLY | All 18 items pass. Logs toward the 10-signal counter. |
| WATCH | Some items pass but one or more gates are conditional. No signal credit. |
| REJECT | One or more hard gates fail. Candidate is discarded. |

Claude cannot produce a PAPER TRADE ONLY verdict on a candidate with:
- Missing numeric volume or RVOL
- Unverified or undated catalyst
- Stale data beyond the freshness threshold
- Math errors flagged by the data sanity auditor
- Extension above 25% intraday without additional justification

### Layer 6 — Kill Switch (Typed Confirmation Phrase)
No order can be placed without the human typing an exact confirmation phrase in the
active session. The phrase is case-sensitive and phrase-exact. No abbreviations,
synonyms, or prior approvals carry over between sessions.

### Layer 7 — Live Eligibility Counter
Live trading is blocked until each engine (Normal/Core and Fast Runner) accumulates
10 valid PAPER TRADE ONLY signals. Signal counts are per-engine and not shared.
Scanner alerts do not count. Claude audits on test data do not count. Only real-
session, policy-cleared verdicts logged to the dry-run log count.

**Current status: 0/10 on both engines. Live trading is BLOCKED.**

### Layer 8 — Risk Officer Agent
A second agent (`risk-officer`) reviews any candidate that reaches PAPER TRADE ONLY
and applies a final risk-framing review. It can downgrade to WATCH or REJECT if it
identifies risk factors the data sanity auditor and main audit did not surface.

---

## Evidence Packet Flow

The opportunity engine produces structured JSON packets that capture the full
state of a candidate at audit time. A packet contains:

```
schema_version         — document version for forward compatibility
status                 — always "Research Lead Only" at creation
timestamp_utc / _et    — when the data was captured
ticker / exchange      — what was scanned
price / prev_close     — price data with source and freshness label
move_pct               — calculated move
volume{}               — current session volume, ADV (20d/30d), RVOL current/projected,
                         dollar volume, source, timestamp
spread{}               — bid, ask, spread_pct, validity flag
catalyst{}             — present?, type, source, source_date, event_date, freshness
setup{}                — setup type, quality, suggested invalidation
regime{}               — SPY/QQQ/IWM context, VIX, with-market flag
trade_skeleton_idea{}  — entry idea, invalidation, exit logic (Claude-populated)
risk_flags[]           — array of risk flag strings
missing_fields[]       — explicit list of fields the packet could not populate
modules_fired[]        — which engine modules ran on this packet
tier                   — 1 (weakest) to 4 (strongest)
tier_reason            — plain-English explanation of tier assignment
data_source            — named source string
data_freshness         — explicit freshness label
```

Missing fields are never silently dropped — they are listed explicitly so Claude
knows exactly what data was unavailable during the audit.

---

## Dry-Run Status

| Metric | Value |
|---|---|
| System mode | DRY RUN ONLY |
| Dry-run scans completed | 6 |
| Candidates audited by Claude | Multiple across 6 scans |
| Valid PAPER TRADE ONLY signals — Normal/Core engine | 0 / 10 |
| Valid PAPER TRADE ONLY signals — Fast Runner engine | 0 / 10 |
| Live trading eligibility | BLOCKED (both engines) |
| Real orders placed | 0 |
| Policy violations | 0 |
| Data sanity auditor tests | Passed (WATCH — DATA MISMATCH correctly returned on injected bad data) |
| Risk officer tests | Passed (REJECT correctly returned on injected dangerous candidate) |

The agents were tested with injected bad data to verify they catch specific failure
modes: math inconsistency, missing required fields, dangerous setup characteristics.
Both agents returned the correct verdict. See `docs/proof-log.md` for detail.

---

## What This Proves as a Portfolio Project

1. **Safety-first pipeline design.** Seven independent safety layers, each catchable
   independently. A failure at layer 2 does not require layer 6 to save you.

2. **Structured evidence over vibes.** The system forces every candidate into a
   machine-readable schema before a human reads it. The human sees structured facts,
   not a model's narrative.

3. **LLM as auditor, not actor.** Claude is given a packet and a checklist. It cannot
   place orders. It cannot fetch live data autonomously. It is a reviewer.

4. **Separation of concerns.** Scanner, opportunity engine, audit layer, and order
   execution are distinct systems. None of them have access to the next layer's
   authority. The scanner cannot trigger an audit. The auditor cannot trigger an order.

5. **Verifiable dry-run history.** The system has produced real scanner runs on real
   market data (Yahoo Finance, delayed), generated real opportunity packets, and logged
   real Claude audit verdicts — all in dry-run mode with zero real orders.

6. **Agent testing.** Both sub-agents were tested with adversarial inputs. Failure
   modes were verified, not assumed.

---

## What Is Intentionally Excluded from Public Release

The following exist in the private repository but are not included here:

| Excluded Item | Reason |
|---|---|
| Account numbers and broker configuration | Personal financial account identifiers |
| Real account balance | Private financial information |
| Brokerage MCP connection settings | Live broker API integration details |
| Claude order-placement prompt templates | Operational prompts tied to live account |
| Pre-order checklist with account confirmation steps | Live account operational protocol |
| Specific asset positions held outside this system | Private portfolio detail |
| Private Obsidian vault notes | Personal daily journal, goals, session logs |
| Local machine paths | System-specific file paths |
| `.claude/settings.local.json` | Contains local permission allowlists |

The exclusions do not reduce the demonstrable engineering value of the public artifacts.
The safety architecture, the scanner, the opportunity engine, the schema, and the
agent definitions are the portfolio artifacts. The operational account plumbing is not.
