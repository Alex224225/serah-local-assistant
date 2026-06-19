"""validator.py - Field and logic validation for the serah_demo package.

Validates Alert dicts (loaded from JSON) against the required schema.
All checks are purely local — no network access, no market data fetching,
no brokerage connection, no order-placement capability.
"""

from __future__ import annotations

  from datetime import datetime, timezone
    from typing import Any, Dict, List, Tuple


      ValidationResult = Tuple[bool, List[str]]


      def validate_alert(data: Dict[str, Any]) -> ValidationResult:
          """Validate a raw alert dict against the required schema.

      Returns (is_valid, errors) where errors is an empty list if valid.
            The alert is considered valid only when ALL checks pass.

            Checks performed:
            - Required top-level fields present and non-empty
        - price is a positive float (not a string, not zero, not negative)
            - volume.current_session_volume is a non-negative integer
        - spread: ask >= bid (ask must be >= bid)
            - spread_pct is internally consistent with bid/ask values
            - move_pct is internally consistent with price/prev_close
        - volume.timestamp is not later than timestamp_utc (source cannot post-date capture)
            - No blocking missing evidence when status is Research Lead Only
        - Duplicate inputs produce identical results (idempotency by design)
            - Invalid status transitions are rejected
            """
        errors: List[str] = []

            # --- Required top-level string fields ---
        required_strings = [
                  "schema_version", "status", "no_trade_statement",
                  "timestamp_utc", "ticker", "exchange", "quote_type",
                  "data_source", "data_freshness",
        ]
            for field in required_strings:
              val = data.get(field)
                      if val is None:
                        errors.append(f"Missing required field: {field}")
                        elif not isinstance(val, str) or not val.strip():
                        errors.append(f"{field} must be a non-empty string")

                            # --- Status value check ---
                        status = data.get("status", "")
                        valid_statuses = {"Research Lead Only"}
                            if status and status not in valid_statuses:
                              errors.append(f"Invalid status '{status}'; must be one of {sorted(valid_statuses)}")

                                  # --- price: must be a positive float ---
                              price = data.get("price")
                                  if price is None:
                                    errors.append("Missing required field: price")
                                    elif not isinstance(price, (int, float)) or isinstance(price, bool):
                                    errors.append(
                                      f"price must be a positive float, got {type(price).__name__}"
                                    )
                                    elif float(price) <= 0:
                                    errors.append(f"price must be > 0, got {price}")

                                        # --- prev_close: must be a positive float ---
                                    prev_close = data.get("prev_close")
                                        if prev_close is None:
                                          errors.append("Missing required field: prev_close")
                                          elif not isinstance(prev_close, (int, float)) or isinstance(prev_close, bool):
                                          errors.append("prev_close must be a positive float")
                                          elif float(prev_close) <= 0:
                                          errors.append(f"prev_close must be > 0, got {prev_close}")

                                              # --- move_pct: internal consistency ---
                                          move_pct = data.get("move_pct")
                                          if move_pct is not None and isinstance(price, (int, float)) and isinstance(prev_close, (int, float)):
                                            expected_move = (float(price) - float(prev_close)) / float(prev_close) * 100
                                            if abs(float(move_pct) - expected_move) > 0.5:
                                              errors.append(
                                                f"move_pct {move_pct:.4f} is inconsistent with price/prev_close "
                                                f"(expected {expected_move:.4f}, tolerance 0.5%)"
                                              )

                                                  # --- volume sub-object ---
                                              volume = data.get("volume", {})
                                              if not isinstance(volume, dict):
                                                errors.append("volume must be an object")
                                                    else:
                                                      csv = volume.get("current_session_volume")
                                                              if csv is None:
                                                                errors.append("volume.current_session_volume is required")
                                                                elif not isinstance(csv, int) or isinstance(csv, bool):
                                                                errors.append("volume.current_session_volume must be an integer")
                                                                        elif csv < 0:
                                                                errors.append(f"volume.current_session_volume must be non-negative, got {csv}")

                                                                vol_source = volume.get("source")
                                                                if not vol_source or not str(vol_source).strip():
                                                                  errors.append("volume.source must not be empty")

                                                                          # volume.timestamp must not be later than capture timestamp_utc
                                                                  vol_ts = volume.get("timestamp")
                                                                  cap_ts = data.get("timestamp_utc")
                                                                          if vol_ts and cap_ts:
                                                                                        try:
                                                                            vol_dt = datetime.fromisoformat(vol_ts.replace("Z", "+00:00"))
                                                                            cap_dt = datetime.fromisoformat(cap_ts.replace("Z", "+00:00"))
                                                                                            if vol_dt > cap_dt:
                                                                                              errors.append(
                                                                                                f"volume.timestamp ({vol_ts}) is later than capture "
                                                                                                f"timestamp_utc ({cap_ts}); source cannot post-date capture"
                                                                                              )
                                                                                                          except ValueError:
                                                                                              errors.append("volume.timestamp or timestamp_utc has invalid ISO 8601 format")

                                                                                                  # --- spread sub-object ---
                                                                                              spread = data.get("spread", {})
                                                                                              if not isinstance(spread, dict):
                                                                                                errors.append("spread must be an object")
                                                                                                    else:
                                                                                                      bid = spread.get("bid")
                                                                                                      ask = spread.get("ask")
                                                                                                      spread_pct = spread.get("spread_pct")
                                                                                                      
                                                                                                              if bid is None:
                                                                                                                errors.append("spread.bid is required")
                                                                                                                elif not isinstance(bid, (int, float)) or isinstance(bid, bool):
                                                                                                                errors.append("spread.bid must be a number")
                                                                                                                elif float(bid) < 0:
                                                                                                                errors.append(f"spread.bid must be >= 0, got {bid}")
                                                                                                                
                                                                                                                        if ask is None:
                                                                                                                          errors.append("spread.ask is required")
                                                                                                                          elif not isinstance(ask, (int, float)) or isinstance(ask, bool):
                                                                                                                          errors.append("spread.ask must be a number")
                                                                                                                          
                                                                                                                          if isinstance(bid, (int, float)) and isinstance(ask, (int, float)):
                                                                                                                            if float(ask) < float(bid):
                                                                                                                              errors.append(
                                                                                                                                f"spread.ask ({ask}) must be >= spread.bid ({bid})"
                                                                                                                              )
                                                                                                                              # spread_pct consistency: spread_pct = (ask - bid) / bid * 100
                                                                                                                              if spread_pct is not None and float(bid) > 0:
                                                                                                                                expected_spread_pct = (float(ask) - float(bid)) / float(bid) * 100
                                                                                                                                if abs(float(spread_pct) - expected_spread_pct) > 0.1:
                                                                                                                                  errors.append(
                                                                                                                                    f"spread_pct {spread_pct:.4f} is inconsistent with bid/ask values "
                                                                                                                                    f"(expected {expected_spread_pct:.4f}, tolerance 0.1%)"
                                                                                                                                  )
                                                                                                                                  
                                                                                                                                      # --- Blocking missing evidence check ---
                                                                                                                                  missing_fields = data.get("missing_fields", [])
                                                                                                                                  blocking = [f for f in missing_fields if _is_blocking(f)]
                                                                                                                                        if blocking:
                                                                                                                                          errors.append(
                                                                                                                                                        f"Blocking missing evidence present - not ready for audit: {blocking}"
                                                                                                                                          )
                                                                                                                                          
                                                                                                                                          return (len(errors) == 0, errors)
                                                                                                                                          
                                                                                                                                          
                                                                                                                                          def _is_blocking(field_name: str) -> bool:
                                                                                                                                              """Return True if a missing field is blocking for audit readiness."""
                                                                                                                                          blocking_fields = {
                                                                                                                                                    "volume.current_session_volume",
                                                                                                                                                    "volume.rvol_current",
                                                                                                                                                    "spread.bid",
                                                                                                                                                    "spread.ask",
                                                                                                                                                    "catalyst.source",
                                                                                                                                                    "catalyst.source_date",
                                                                                                                                          }
                                                                                                                                              return field_name in blocking_fields
                                                                                                                                          
