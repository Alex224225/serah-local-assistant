# Proof Log — Build and Test Evidence

This document records what was actually built, tested, and run. It is a factual
log of system activity, not a claims document. All entries are from dry-run mode.
Zero real orders were placed at any point.

---

## System Initialization

| Date | Component | What Happened |
|---|---|---|
| 2026-06-14 | TradingSystem vault | Folder structure created, policy documents written, safety rules finalized |
| 2026-06-14 | Fast Mover Scanner v1 | First scanner run completed in test mode (market closed) |
| 2026-06-14 | Config/ScannerConfig.json | Scanner configuration written and validated |
| 2026-06-14 | Data/ScannerUniverse | Initial ticker universe (28 tickers) defined |
| 2026-06-14 | Safety policy | All 8 hard rules finalized and documented |
| 2026-06-14 | Read-only connection test | Brokerage account status confirmed via read-only calls only |
| 2026-06-15 | Scanner scheduling | Windows Task Scheduler tasks installed (preflight, market loop, EOD summary) |
| 2026-06-15 | Scanner preflight | First preflight check passed: Python version, config validity, universe file, output directories |

---

## Scanner Run History

All runs use Yahoo Finance (yfinance, free tier, approximately 15-minute delayed data).
All output is stamped "Research Lead Only — No trade action taken."

| Date | Run Type | Tickers Scanned | Alerts Generated |
|---|---|---|---|
| 2026-06-14 | Test (market closed) | 28 | 2 (INTC +5.11%, ARM +8.68%) |
| 2026-06-15 | Live market hours | Multiple batches | Multiple alerts per run |
| 2026-06-15 | Preflight | — | PASS |
| 2026-06-16 | Live market hours | Scheduled batches | Daily alert files generated |
| 2026-06-16 | Preflight | — | PASS |
| 2026-06-17 | Live market hours | Scheduled batches | Daily alert files generated |
| 2026-06-17 | Preflight | — | PASS |
| 2026-06-18 | Live market hours | Scheduled batches | INTC, RBLX, NSC, MRVL, KLAC, ENTG, SMCI, MPWR flagged |
| 2026-06-18 | Preflight | — | PASS |

Scanner alert files: `Data/ScannerAlerts/YYYY-MM-DD_alerts.jsonl` (one per day).
Each line is a complete JSON alert object for a single ticker at a single scan time.

---

## Dry-Run Audit Sessions

Six dry-run scans have been completed. In each session:
- Scanner alert data was reviewed
- Candidates were evaluated against the 18-item Claude audit checklist
- No PAPER TRADE ONLY verdicts have been issued (0/10 per engine)
- No orders were placed

Representative candidates reviewed and rejected:

| Session | Ticker | Move | Verdict | Primary Rejection Reason |
|---|---|---|---|---|
| Scan 1 | AXTI | +14.50% | WATCH (DRY RUN) | High extension — parabolic risk |
| Scan 1 | LRCX | +6.25% | WATCH (DRY RUN) | Delayed data, RVOL not confirmed |
| Scan 2 | NVDA | +3.49% | WATCH | No stock-specific catalyst — macro only |
| Scan 3 | Multiple | Various | WATCH / REJECT | Weak RVOL across all candidates |
| Scan 4–6 | Various | Various | WATCH / REJECT | Delayed data, volume confirmation missing |

A hallucinated price was detected during Scan 2: a web search returned a price of
$225.005 for a ticker that was simultaneously quoted at $212.35 by the brokerage
read-only feed. The discrepancy was flagged by the data sanity auditor, the web
search result was discarded, and the brokerage live quote was used as ground truth.
This is an example of the data sanity check functioning correctly.

---

## Opportunity Engine Development

| Date | Milestone |
|---|---|
| 2026-06-15 | Packet schema (v1.0) defined |
| 2026-06-15 | Packet validator written and tested |
| 2026-06-15 | v1 alert adapter written — converts scanner alerts to opportunity packets |
| 2026-06-16 | Capital allocation policy written — two engines defined (Normal/Core, Fast Runner) |
| 2026-06-16 | Shadow live dry-run module written |
| 2026-06-17 | Full test suite written (12 test files, one per module) |
| 2026-06-17 | Replay module written — replays historical alert files through engine |
| 2026-06-17 | Operator status report module written |
| 2026-06-18 | Handoff module written |
| 2026-06-18 | Shadow dry-run run on real June 18 alert data — 3 sessions |

Shadow dry-run sessions on 2026-06-18 data:
- `shadow_live_20260618T151241Z.md`
- `shadow_live_20260618T151406Z.md`
- `shadow_live_20260618T151645Z.md`

Each produced a candidate list with tier assignments and missing fields. No packets
were automatically sent to Claude. Human initiation is required for the audit step.

---

## Agent Test Results

Two Claude sub-agents were defined and tested:

### data-sanity-auditor

**Test type:** Injected fake candidate with deliberate errors

**Injected errors:**
- Claimed move of +40% but underlying math showed +25%
- Missing current session volume
- Missing RVOL
- Missing spread
- Unknown catalyst date and source
- No live brokerage quote
- ADV source unnamed
- Entry, invalidation, and exit absent

**Expected verdict:** WATCH — DATA MISMATCH
**Actual verdict:** WATCH — DATA MISMATCH
**Result:** PASS — agent correctly identified all injected errors

**Safety confirmation:**
- No scanner executed
- No brokerage MCP call made
- No web search run
- No files edited by agent
- No order placed, cancelled, modified, drafted, or reviewed

---

### risk-officer

**Test type:** Injected fake dangerous candidate

**Injected characteristics:**
- Extreme intraday extension (parabolic move, late session)
- No defined stop loss
- Missing catalyst source
- High spread
- Recent trading halt history
- All-in position sizing implied

**Expected verdict:** REJECT
**Actual verdict:** REJECT
**Result:** PASS — agent correctly blocked the candidate

**Safety confirmation:**
- Same as above — no brokerage calls, no orders, no file edits

---

## Live Eligibility Status

| Field | Value |
|---|---|
| System mode | DRY RUN ONLY |
| Dry-run scans completed (system-wide) | 6 |
| Normal/Core engine — valid PAPER TRADE ONLY signals | 0 / 10 |
| Normal/Core engine — live eligibility | BLOCKED |
| Fast Runner engine — valid PAPER TRADE ONLY signals | 0 / 10 |
| Fast Runner engine — live eligibility | BLOCKED |
| System-wide live trading | BLOCKED |
| Orders placed | 0 |
| Policy violations | 0 |

**Live trading will remain BLOCKED until:**
1. The relevant engine accumulates 10 valid PAPER TRADE ONLY signals (not scanner alerts,
   not test data — real-session Claude-audited verdicts)
2. AND the account holder types the exact approval phrase in that session

Neither condition is currently met. No eligibility review is active.

---

## What Has Never Happened

For the avoidance of any ambiguity:

- No real order has been placed, reviewed, drafted, or cancelled by this system
- No brokerage account has been modified
- The scanner has never called any brokerage API
- No Claude session has ever had access to place orders (the approval phrase has
  never been typed)
- No live trading eligibility has been reached (0/10 signals on both engines)
- No real capital has been deployed
- No simulated profit or loss figures exist
- No backtests have been marked as live-eligible
