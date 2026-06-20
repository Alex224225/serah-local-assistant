"""packet_builder.py - Evidence packet construction for the serah_demo package.

Transforms a validated alert dict into a structured EvidencePacket with
provenance, timestamps, a stable identifier, and a content hash.

No network access, no brokerage connection, no order-placement capability.
All data must be synthetic local data.
"""

from __future__ import annotations

from typing import Any, Dict

from .models import (
    Alert,
    CatalystData,
    EvidencePacket,
    SpreadData,
    VolumeData,
    _compute_content_hash,
    _compute_packet_id,
    now_utc_iso,
)
from .validator import validate_alert


class ValidationError(Exception):
    """Raised when an alert fails validation and cannot be built into a packet."""


def build_packet(alert_data: Dict[str, Any], packet_index: int = 0) -> EvidencePacket:
    """Build a validated EvidencePacket from a raw alert dict.

    Args:
        alert_data: Raw alert dict (typically loaded from JSON).
        packet_index: Sequential index for packet ID generation.

    Returns:
        EvidencePacket with all fields populated, content hash, and provenance.

    Raises:
        ValidationError: If the alert fails any validation check.
    """
    is_valid, errors = validate_alert(alert_data)
    if not is_valid:
        raise ValidationError(
            f"Alert failed validation with {len(errors)} error(s):\n"
            + "\n".join(f"  - {e}" for e in errors)
        )

    ticker = alert_data["ticker"]
    timestamp_utc = alert_data["timestamp_utc"]
    price = float(alert_data["price"])
    prev_close = float(alert_data["prev_close"])
    move_pct = float(alert_data["move_pct"])

    vol_raw = alert_data["volume"]
    volume = VolumeData(
        current_session_volume=int(vol_raw["current_session_volume"]),
        dollar_volume=float(vol_raw.get("dollar_volume", 0.0)),
        source=vol_raw["source"],
        timestamp=vol_raw["timestamp"],
        adv_20d=_float_or_none(vol_raw.get("adv_20d")),
        adv_30d=_float_or_none(vol_raw.get("adv_30d")),
        rvol_current=_float_or_none(vol_raw.get("rvol_current")),
        rvol_projected=_float_or_none(vol_raw.get("rvol_projected")),
    )

    spread_raw = alert_data["spread"]
    spread = SpreadData(
        bid=float(spread_raw["bid"]),
        ask=float(spread_raw["ask"]),
        spread_pct=float(spread_raw["spread_pct"]),
        valid=bool(spread_raw.get("valid", True)),
    )

    cat_raw = alert_data["catalyst"]
    catalyst = CatalystData(
        present=bool(cat_raw.get("present", False)),
        freshness=str(cat_raw.get("freshness", "unknown")),
        type=cat_raw.get("type"),
        source=cat_raw.get("source"),
        source_date=cat_raw.get("source_date"),
        event_date=cat_raw.get("event_date"),
    )

    tier, tier_reason = _compute_tier(volume, catalyst)
    missing_fields = list(alert_data.get("missing_fields", []))
    is_ready = len(missing_fields) == 0 and tier >= 2

    packet_id = _compute_packet_id(ticker, timestamp_utc, packet_index)
    built_at = now_utc_iso()

    # Content hash covers all core data fields (not provenance itself)
    hashable = {
        "ticker": ticker,
        "timestamp_utc": timestamp_utc,
        "price": price,
        "prev_close": prev_close,
        "move_pct": move_pct,
        "status": alert_data["status"],
        "tier": tier,
    }
    content_hash = _compute_content_hash(hashable)

    provenance = {
        "created_by": "serah_demo v1.0",
        "created_at": built_at,
        "source_alert_fields": list(alert_data.keys()),
        "is_synthetic": True,
        "no_network_access": True,
        "no_brokerage_connection": True,
        "no_order_capability": True,
    }

    return EvidencePacket(
        packet_id=packet_id,
        schema_version=alert_data["schema_version"],
        status=alert_data["status"],
        no_trade_statement=alert_data["no_trade_statement"],
        timestamp_utc=timestamp_utc,
        ticker=ticker,
        price=price,
        prev_close=prev_close,
        move_pct=move_pct,
        data_source=alert_data["data_source"],
        data_freshness=alert_data["data_freshness"],
        volume=volume,
        spread=spread,
        catalyst=catalyst,
        risk_flags=list(alert_data.get("risk_flags", [])),
        missing_fields=missing_fields,
        tier=tier,
        tier_reason=tier_reason,
        content_hash=content_hash,
        provenance=provenance,
        is_ready_for_audit=is_ready,
    )


def _float_or_none(val: Any):
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _compute_tier(volume: VolumeData, catalyst: CatalystData):
    """Assign a tier (1-4) based on volume quality and catalyst confirmation."""
    rvol = volume.rvol_current

    if rvol is None:
        return 1, "RVOL not available; delayed data with no volume confirmation"

    if rvol >= 2.0 and catalyst.present and catalyst.freshness == "fresh":
        return 4, f"RVOL {rvol:.2f}x >= 2.0x; catalyst confirmed and fresh; spread valid"

    if rvol >= 1.5 and volume.adv_20d is not None:
        return 3, f"RVOL {rvol:.2f}x >= 1.5x; all volume fields populated; catalyst {catalyst.freshness}"

    if rvol >= 1.0:
        return 2, f"RVOL {rvol:.2f}x in 1.0x-1.49x range; standard checklist applies"

    return 1, f"RVOL {rvol:.2f}x < 1.0x; additional scepticism required"
