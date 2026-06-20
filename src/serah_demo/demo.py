# demo.py - Synthetic demonstration. SYNT-X fictional. No orders.
import json, pathlib, sys
from .validator import validate_alert
from .packet_builder import build_packet, ValidationError
from .report_builder import build_review_packet_text, build_operator_report

EXAMPLES_DIR = pathlib.Path(__file__).parent.parent.parent / 'examples'


def run_demo():
    print('serah_demo v1.0 - Synthetic Demo. SYNT-X DOES NOT EXIST.')
    valid_data = json.loads((EXAMPLES_DIR / 'synthetic_alert.json').read_text())
    is_valid, errors = validate_alert(valid_data)
    assert is_valid, f'Valid alert failed: {errors}'
    packet = build_packet(valid_data)
    packet2 = build_packet(valid_data)
    assert packet.content_hash == packet2.content_hash, 'Idempotency FAIL'
    invalid_data = json.loads((EXAMPLES_DIR / 'invalid_alert.json').read_text())
    is_bad, bad_errors = validate_alert(invalid_data)
    assert not is_bad, 'Invalid alert should have failed validation'
    try:
        build_packet(invalid_data)
        sys.exit(1)
    except ValidationError:
        pass
    report = build_review_packet_text(packet)
    op = build_operator_report([packet], invalid_count=1, invalid_errors=bad_errors[:3])
    print(f'Packet: {packet.packet_id} Tier:{packet.tier} Ready:{packet.is_ready_for_audit}')
    print(f'Hash: {packet.content_hash[:32]}')
    print(f'Validation errors on invalid: {len(bad_errors)}')
    print(op)
    print('Done. No network. No orders.')
