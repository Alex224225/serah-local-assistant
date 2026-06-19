"""models.py - Data models for the serah_demo package.

All models operate on synthetic data only. No real market data, brokerage
connections, or order-placement capability is present.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class VolumeData:
      current_session_volume: int
      dollar_volume: float
      source: str
      timestamp: str
      adv_20d: Optional[float] = None
      adv_30d: Optional[float] = None
      rvol_current: Optional[float] = None
      rvol_projected: Optional[float] = None


@dataclass
class SpreadData:
      bid: float
      ask: float
      spread_pct: float
      valid: bool


@dataclass
class CatalystData:
      present: bool
      freshness: str
      type: Optional[str] = None
      source: Optional[str] = None
      source_date: Optional[str] = None
      event_date: Optional[str] = None


@dataclass
class Alert:
      """Raw scanner alert (input to the packet builder).

          Attributes are intentionally typed loosely so the validator can
              catch type errors explicitly rather than via constructor failures.
                  """
      schema_version: str
      status: str
      no_trade_statement: str
      timestamp_utc: str
      ticker: str
      exchange: str
      quote_type: str
      price: Any  # validated as float > 0 by validator
    prev_close: float
    move_pct: float
    data_source: str
    data_freshness: str
    volume: Dict[str, Any]
    spread: Dict[str, Any]
    catalyst: Dict[str, Any]
    risk_flags: List[str]
    missing_fields: List[str]
    timestamp_et: Optional[str] = None
    trading_date: Optional[str] = None
    company_name: Optional[str] = None


@dataclass
class EvidencePacket:
      """Structured evidence packet produced by the packet builder.

          Contains provenance, content hash, and all validated fields.
              This packet is what would be presented for human review.
                  No order-placement capability is associated with this object.
                      """
      packet_id: str
      schema_version: str
      status: str
      no_trade_statement: str
      timestamp_utc: str
      ticker: str
      price: float
      prev_close: float
      move_pct: float
      data_source: str
      data_freshness: str
      volume: VolumeData
      spread: SpreadData
      catalyst: CatalystData
      risk_flags: List[str]
      missing_fields: List[str]
      tier: int
      tier_reason: str
      content_hash: str
      provenance: Dict[str, Any]
      is_ready_for_audit: bool

    def to_dict(self) -> Dict[str, Any]:
              return asdict(self)


def _compute_packet_id(ticker: str, timestamp_utc: str, index: int = 0) -> str:
      """Generate a stable packet identifier from ticker, timestamp, and index."""
      date_part = timestamp_utc[:10].replace("-", "")
      return f"PKT-{date_part}-{ticker}-{index:03d}"


def _compute_content_hash(data: Dict[str, Any]) -> str:
      """Compute a SHA-256 content hash over the canonical JSON representation."""
      canonical = json.dumps(data, sort_keys=True, ensure_ascii=True)
      return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def now_utc_iso() -> str:
      """Return the current UTC time as an ISO 8601 string."""
      return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
  
