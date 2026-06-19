# Trading Safety Harness — Case Study

> **Status:** This case study describes components implemented in the private system. The public `serah_demo` package demonstrates the evidence-packet pipeline with synthetic data. No brokerage connections, live market data, or order-execution capability are present in this public repository.

---

## Purpose

The Trading Safety Harness is a research and safety-engineering sub-project built on top of the Serah local assistant infrastructure.

Its goal is to demonstrate that an LLM-assisted financial research pipeline can be made safe by design — not just by instruction — by enforcing hard gates at every layer between a market observation and a human trade decision.

**This is not a trading bot.** It is a research amplifier with a structured auditing system. The human is the only entity in the system that can act on any finding, and only after the system has produced and audited a structured evidence packet.

**Orders placed to date: 0.**

---

## The Core Problem It Solves

LLM-assisted trading research creates a specific failure mode: the model sounds confident, the analysis looks plausible, and the human accepts the output without verifying the underlying data. If the model hallucinated a price, a catalyst, or a volume figure, the human may never catch it.

The Trading Safety Harness addresses this by never trusting a single data source, never letting the model produce a recommendation from unvalidated inputs, requiring structured evidence before Claude sees a candidate, having Claude audit that evidence against a fixed 18-item checklist (not free-form analysis), and blocking any action behind an explicit human-confirmation gate in every session.

---

## Architecture — *Implemented in private system*

```
Yahoo Finance (yfinance, free tier, ~15-min delayed)
    |
        v
        [Fast Mover Scanner]
            Python script, runs on schedule (market hours)
                No brokerage connection. No order logic.
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
                                                    Validates alert against packet schema
                                                        Builds structured JSON evidence packet
                                                            Computes tier (1–4 based on data quality and volume confirmation)
                                                                |
                                                                    v
                                                                    [Claude Audit] (human-initiated)
                                                                        Claude receives a candidate packet
                                                                            Runs 18-item audit checklist
                                                                                Returns: PAPER TRADE ONLY / WATCH / REJECT
                                                                                    |
                                                                                        v
                                                                                        [Human Decision Point]
                                                                                            Human reads the Claude audit verdict and evidence packet
                                                                                                Human decides whether to act
                                                                                                    If acting: must provide explicit confirmation in that session
                                                                                                        |
                                                                                                            v
                                                                                                            [Zero orders placed]
                                                                                                                System is in DRY RUN ONLY mode
                                                                                                                    Live eligibility requires 10 valid PAPER TRADE ONLY signals per engine
                                                                                                                        Current count: 0/10 (both engines)
                                                                                                                        ```
                                                                                                                        
                                                                                                                        ---
                                                                                                                        
                                                                                                                        ## Safety Layers
                                                                                                                        
                                                                                                                        ### Layer 1 — Scanner Isolation *(Implemented in private system)*
                                                                                                                        
                                                                                                                        The scanner Python script has no connection to any brokerage API. It contains no order logic, no account references, and no trade execution code. It reads from Yahoo Finance and writes to flat files.
                                                                                                                        
                                                                                                                        ### Layer 2 — Research Lead Stamp *(Implemented in private system)*
                                                                                                                        
                                                                                                                        Every scanner alert is stamped with two mandatory fields:
                                                                                                                        
                                                                                                                        ```json
                                                                                                                        "status": "Research Lead Only",
                                                                                                                        "no_trade_statement": "No trade action taken"
                                                                                                                        ```
                                                                                                                        
                                                                                                                        These fields are required by schema. An alert without them fails validation and cannot enter the opportunity engine.
                                                                                                                        
                                                                                                                        ### Layer 3 — Schema Validation *(Implemented in private system; demonstrated in serah_demo)*
                                                                                                                        
                                                                                                                        The opportunity engine validates every packet against a strict schema before Claude sees it. A packet with missing required fields is flagged with a `missing_fields` list and tiered down. Claude sees the missing fields and factors them into the audit.
                                                                                                                        
                                                                                                                        The public `serah_demo` package demonstrates this validation logic using synthetic data. See `src/serah_demo/validator.py`.
                                                                                                                        
                                                                                                                        ### Layer 4 — Data Sanity Auditor Agent *(Implemented in private system)*
                                                                                                                        
                                                                                                                        A dedicated Claude sub-agent verifies math before the main audit runs: whether the claimed price move is mathematically consistent with bid/ask, whether volume figures make sense given the time of day, and whether there are contradictions between fields. A REJECT here ends the audit.
                                                                                                                        
                                                                                                                        ### Layer 5 — 18-Item Claude Audit Checklist *(Implemented in private system)*
                                                                                                                        
                                                                                                                        The main audit is structured as a numbered checklist, not free-form analysis. Claude must address each item explicitly. The verdict options are PAPER TRADE ONLY, WATCH, and REJECT.
                                                                                                                        
                                                                                                                        Claude cannot produce a PAPER TRADE ONLY verdict on a candidate with missing numeric volume or RVOL, unverified or undated catalyst, stale data beyond the freshness threshold, math errors flagged by the data sanity auditor, or extension above 25% intraday without additional justification.
                                                                                                                        
                                                                                                                        ### Layer 6 — Explicit Human-Confirmation Gate *(Implemented in private system)*
                                                                                                                        
                                                                                                                        No action can be taken without the human providing explicit confirmation in the active session. This is a session-level behavioral control — it ensures the human has actively reviewed and chosen to proceed in that specific context.
                                                                                                                        
                                                                                                                        **Important:** A typed confirmation phrase is a behavioral approval mechanism, not a cryptographic lock or process-isolated enforcement boundary. It works as intended when the system is used honestly and correctly. It does not substitute for code-level restrictions, which are enforced separately in the private system.
                                                                                                                        
                                                                                                                        ### Layer 7 — Live Eligibility Counter *(Implemented in private system)*
                                                                                                                        
                                                                                                                        Live trading is blocked until each engine accumulates 10 valid PAPER TRADE ONLY signals. Signal counts are per-engine and are not shared. Scanner alerts do not count. Claude audits on test data do not count. Only real-session, policy-cleared verdicts logged to the dry-run log count.
                                                                                                                        
                                                                                                                        **Current status: 0/10 on both engines. Live trading is BLOCKED.**
                                                                                                                        
                                                                                                                        ---
                                                                                                                        
                                                                                                                        ## Evidence Packet Flow
                                                                                                                        
                                                                                                                        The opportunity engine produces structured JSON packets that capture the full state of a candidate at audit time. Key fields include schema version, status, timestamps, ticker and exchange, price data with named source and explicit freshness label, volume in multiple forms (session, ADV, RVOL), spread, catalyst details, market regime context, risk flags, and an explicit list of missing fields.
                                                                                                                        
                                                                                                                        Missing fields are never silently dropped — they are listed explicitly so Claude knows exactly what data was unavailable during the audit.
                                                                                                                        
                                                                                                                        A synthetic example of a complete evidence packet is available at `examples/valid_packet.json`.
                                                                                                                        
                                                                                                                        ---
                                                                                                                        
                                                                                                                        ## Dry-Run Status
                                                                                                                        
                                                                                                                        | Metric | Value |
                                                                                                                        |---|---|
                                                                                                                        | System mode | DRY RUN ONLY |
                                                                                                                        | Dry-run scans completed | 6 (private system) |
                                                                                                                        | Normal/Core engine — valid PAPER TRADE ONLY signals | 0 / 10 |
                                                                                                                        | Fast Runner engine — valid PAPER TRADE ONLY signals | 0 / 10 |
                                                                                                                        | Live trading eligibility | BLOCKED (both engines) |
                                                                                                                        | Real orders placed | 0 |
                                                                                                                        | Policy violations | 0 |
                                                                                                                        
                                                                                                                        ---
                                                                                                                        
                                                                                                                        ## What This Demonstrates as a Portfolio Project
                                                                                                                        
                                                                                                                        Safety-first pipeline design with seven independent safety layers, each catchable independently. A failure at layer 2 does not require layer 6 to catch it.
                                                                                                                        
                                                                                                                        Structured evidence over narrative. The system forces every candidate into a machine-readable schema before a human reads it. The human sees structured facts, not a model's story.
                                                                                                                        
                                                                                                                        LLM as auditor, not actor. Claude is given a packet and a checklist. It cannot place orders. It cannot fetch live data autonomously. It is a reviewer.
                                                                                                                        
                                                                                                                        Separation of concerns. Scanner, opportunity engine, audit layer, and any downstream action are distinct systems. The scanner cannot trigger an audit. The auditor cannot trigger an action.
                                                                                                                        
                                                                                                                        Verifiable dry-run history. The system has produced real scanner runs on real market data (Yahoo Finance, delayed), generated real opportunity packets, and logged real Claude audit verdicts — all in dry-run mode with zero real orders.
                                                                                                                        
                                                                                                                        ---
                                                                                                                        
                                                                                                                        ## What Is Intentionally Excluded from Public Release
                                                                                                                        
                                                                                                                        | Excluded Item | Reason |
                                                                                                                        |---|---|
                                                                                                                        | Account numbers and broker configuration | Personal financial account identifiers |
                                                                                                                        | Real account balance | Private financial information |
                                                                                                                        | Brokerage API connection settings | Live broker integration details |
                                                                                                                        | Claude order-placement prompt templates | Operational prompts tied to live account |
                                                                                                                        | Specific asset positions | Private portfolio detail |
                                                                                                                        | Private Obsidian vault notes | Personal daily journal, goals, session logs |
                                                                                                                        | Local machine paths | System-specific file paths |
                                                                                                                        | Private configuration files | Contains local permission allowlists |
                                                                                                                        
                                                                                                                        The exclusions do not reduce the demonstrable engineering value of the public artifacts. The safety architecture, schema design, and agent definitions are the portfolio artifacts. Operational account plumbing is not included.
