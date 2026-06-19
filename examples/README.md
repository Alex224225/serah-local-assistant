# Examples — Synthetic Fixtures

> **All data in this directory is entirely synthetic and fictional.**
>
> The ticker symbol `SYNT-X` and the entity "SynthEx Corp" do not exist. All prices, volumes, spreads, and other figures are invented for demonstration purposes only. Nothing in this directory constitutes, resembles, or should be treated as a real financial recommendation or market observation.

---

## Contents

| File | Description |
|---|---|
| `synthetic_alert.json` | A valid synthetic scanner alert for `SYNT-X`. Passes all required field checks. |
| `invalid_alert.json` | A malformed synthetic alert. Contains type errors, a negative bid, and missing required fields. Used to demonstrate rejection behaviour. |
| `valid_packet.json` | A fully built evidence packet built from `synthetic_alert.json`. All required fields populated. Tier 3. |
| `review_packet.md` | Human-readable audit presentation generated from `valid_packet.json`. |
| `operator_report.txt` | Example operator session summary showing packet status, tier distribution, and readiness gate output. |

---

## How to Regenerate

These files represent the kind of output the `serah_demo` package produces. You can regenerate similar output by running:

```bash
pip install -e ".[dev]"
python -m serah_demo
```

The demo loads `examples/synthetic_alert.json`, validates it, builds a packet, and generates a report — printing output to the terminal.

---

## Safety Notes

- No file in this directory connects to any real market data source.
- No file in this directory constitutes a trade recommendation.
- No file in this directory contains real account information, brokerage identifiers, or credentials.
- The `SYNT-X` symbol is deliberately fictional and does not correspond to any listed security.
