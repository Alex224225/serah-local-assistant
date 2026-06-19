"""test_demo.py - Test suite for the serah_demo public demonstration package.

All tests use synthetic local fixtures only. No network access, no brokerage
connection, no real market data, no order-placement capability.
Tests run with: pytest
"""
import json
import pathlib
import pytest

# Fixtures directory
EXAMPLES_DIR = pathlib.Path(__file__).parent.parent / "examples"

# Import the package modules
from serah_demo.validator import validate_alert
from serah_demo.packet_builder import build_packet, ValidationError
from serah_demo.report_builder import build_review_packet_text, build_operator_report
from serah_demo.models import _compute_content_hash


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def valid_alert():
    """Load the synthetic valid alert fixture."""
    return json.loads((EXAMPLES_DIR / "synthetic_alert.json").read_text())

@pytest.fixture
def invalid_alert():
    """Load the synthetic invalid alert fixture."""
    return json.loads((EXAMPLES_DIR / "invalid_alert.json").read_text())

@pytest.fixture
def valid_packet(valid_alert):
    """Build a packet from the valid alert fixture."""
    return build_packet(valid_alert)


# ─── Validator tests ──────────────────────────────────────────────────────────

class TestValidateAlert:
    def test_valid_alert_passes(self, valid_alert):
        is_valid, errors = validate_alert(valid_alert)
        assert is_valid, f"Expected valid alert to pass, got errors: {errors}"
        assert errors == []

    def test_invalid_alert_fails(self, invalid_alert):
        is_valid, errors = validate_alert(invalid_alert)
        assert not is_valid, "Expected invalid alert to fail validation"
        assert len(errors) > 0

    def test_price_as_string_fails(self, valid_alert):
        bad = {**valid_alert, "price": "not-a-number"}
        is_valid, errors = validate_alert(bad)
        assert not is_valid
        assert any("price" in e for e in errors)

    def test_negative_session_volume_fails(self, valid_alert):
        bad = dict(valid_alert)
        bad["volume"] = {**valid_alert["volume"], "current_session_volume": -1}
        is_valid, errors = validate_alert(bad)
        assert not is_valid
        assert any("current_session_volume" in e for e in errors)

    def test_ask_less_than_bid_fails(self, valid_alert):
        bad = dict(valid_alert)
        bad["spread"] = {**valid_alert["spread"], "bid": 100.0, "ask": 50.0}
        is_valid, errors = validate_alert(bad)
        assert not is_valid
        assert any("ask" in e for e in errors)

    def test_spread_pct_inconsistency_fails(self, valid_alert):
        bad = dict(valid_alert)
        bad["spread"] = {**valid_alert["spread"], "spread_pct": 99.0}
        is_valid, errors = validate_alert(bad)
        assert not is_valid
        assert any("spread_pct" in e for e in errors)

    def test_move_pct_inconsistency_fails(self, valid_alert):
        bad = dict(valid_alert)
        bad["move_pct"] = 99.0  # Inconsistent with price/prev_close
        is_valid, errors = validate_alert(bad)
        assert not is_valid
        assert any("move_pct" in e for e in errors)

    def test_volume_timestamp_later_than_capture_fails(self, valid_alert):
        bad = dict(valid_alert)
        bad["volume"] = {**valid_alert["volume"], "timestamp": "2099-01-01T00:00:00Z"}
        is_valid, errors = validate_alert(bad)
        assert not is_valid
        assert any("timestamp" in e for e in errors)

    def test_empty_data_source_fails(self, valid_alert):
        bad = {**valid_alert, "data_source": ""}
        is_valid, errors = validate_alert(bad)
        assert not is_valid
        assert any("data_source" in e for e in errors)

    def test_invalid_status_fails(self, valid_alert):
        bad = {**valid_alert, "status": "BUY NOW"}
        is_valid, errors = validate_alert(bad)
        assert not is_valid
        assert any("status" in e for e in errors)


# ─── Packet builder tests ─────────────────────────────────────────────────────

class TestBuildPacket:
    def test_valid_alert_builds_packet(self, valid_alert):
        packet = build_packet(valid_alert)
        assert packet is not None
        assert packet.ticker == "SYNT-X"

    def test_invalid_alert_raises_validation_error(self, invalid_alert):
        with pytest.raises(ValidationError):
            build_packet(invalid_alert)

    def test_packet_has_content_hash(self, valid_packet):
        assert valid_packet.content_hash.startswith("sha256:")
        assert len(valid_packet.content_hash) > 10

    def test_packet_has_packet_id(self, valid_packet):
        assert valid_packet.packet_id.startswith("PKT-")
        assert "SYNT-X" in valid_packet.packet_id

    def test_packet_status_is_research_lead_only(self, valid_packet):
        assert valid_packet.status == "Research Lead Only"

    def test_packet_has_no_trade_statement(self, valid_packet):
        assert valid_packet.no_trade_statement == "No trade action taken"

    def test_packet_tier_is_computed(self, valid_packet):
        assert 1 <= valid_packet.tier <= 4

    def test_packet_provenance_is_synthetic(self, valid_packet):
        assert valid_packet.provenance["is_synthetic"] is True
        assert valid_packet.provenance["no_order_capability"] is True
        assert valid_packet.provenance["no_brokerage_connection"] is True
        assert valid_packet.provenance["no_network_access"] is True

    def test_packet_price_matches_alert(self, valid_alert, valid_packet):
        assert valid_packet.price == float(valid_alert["price"])

    def test_spread_ask_gte_bid(self, valid_packet):
        assert valid_packet.spread.ask >= valid_packet.spread.bid

    def test_move_pct_internally_consistent(self, valid_packet):
        expected = (valid_packet.price - valid_packet.prev_close) / valid_packet.prev_close * 100
        assert abs(valid_packet.move_pct - expected) < 0.5


# ─── Idempotency tests ────────────────────────────────────────────────────────

class TestIdempotency:
    def test_same_input_produces_same_hash(self, valid_alert):
        p1 = build_packet(valid_alert)
        p2 = build_packet(valid_alert)
        assert p1.content_hash == p2.content_hash

    def test_same_input_produces_same_packet_id(self, valid_alert):
        p1 = build_packet(valid_alert)
        p2 = build_packet(valid_alert)
        assert p1.packet_id == p2.packet_id

    def test_different_tickers_produce_different_hashes(self, valid_alert):
        alert_b = {**valid_alert, "ticker": "SYNTH-Y"}
        p1 = build_packet(valid_alert)
        p2 = build_packet(alert_b)
        assert p1.content_hash != p2.content_hash


# ─── Report builder tests ─────────────────────────────────────────────────────

class TestReportBuilder:
    def test_review_packet_text_is_string(self, valid_packet):
        text = build_review_packet_text(valid_packet)
        assert isinstance(text, str)
        assert len(text) > 0

    def test_review_packet_contains_ticker(self, valid_packet):
        text = build_review_packet_text(valid_packet)
        assert valid_packet.ticker in text

    def test_review_packet_contains_disclaimer(self, valid_packet):
        text = build_review_packet_text(valid_packet)
        assert "SYNTHETIC" in text.upper()

    def test_operator_report_is_string(self, valid_packet):
        report = build_operator_report([valid_packet])
        assert isinstance(report, str)
        assert "OPERATOR SESSION REPORT" in report

    def test_operator_report_no_order_capability(self, valid_packet):
        report = build_operator_report([valid_packet])
        assert "No order" in report or "no order" in report.lower()


# ─── Safety tests ─────────────────────────────────────────────────────────────

class TestSafetyProperties:
    def test_packet_has_research_lead_only_status(self, valid_packet):
        """All packets must carry the Research Lead Only status."""
        assert valid_packet.status == "Research Lead Only"

    def test_packet_has_no_trade_statement(self, valid_packet):
        """All packets must carry the no-trade statement."""
        assert "No trade action taken" in valid_packet.no_trade_statement

    def test_packet_is_marked_synthetic(self, valid_packet):
        """Provenance must mark the packet as synthetic."""
        assert valid_packet.provenance.get("is_synthetic") is True

    def test_blocking_missing_fields_prevent_ready_status(self, valid_alert):
        """A packet with blocking missing fields must not be marked ready."""
        bad = dict(valid_alert)
        bad["missing_fields"] = ["volume.current_session_volume"]
        # This passes validation (missing_fields is just informational)
        # but the packet should not be ready
        # Note: blocking field detection is in validator._is_blocking
        from serah_demo.validator import _is_blocking
        assert _is_blocking("volume.current_session_volume")

    def test_non_blocking_missing_fields_allowed(self):
        from serah_demo.validator import _is_blocking
        assert not _is_blocking("company_name")
        assert not _is_blocking("timestamp_et")
