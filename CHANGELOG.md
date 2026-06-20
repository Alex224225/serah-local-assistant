# Changelog

All notable changes to this public repository are documented here.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions
and uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-06

### Added

**Documentation**
- Root `README.md` rewritten: added Mermaid architecture diagram, feature status table with
  accurate labels (Implemented in private system / Demonstrated in this repository / Planned /
  Experimental), corrected safety language throughout.
- `docs/serah-architecture.md`: full architecture overview with corrected status labels and
  private-system labelling for folder patterns.
- `docs/trading-safety-harness-case-study.md`: replaced "kill switch" language with
  "explicit human-confirmation gate"; clarified that prompts are behavioral controls, not
  complete technical security boundaries.
- `docs/opportunity-engine-overview.md`: labelled private folder patterns as private-system
  examples; corrected status labels.
- `docs/proof-log.md`: labelled private-system paths; corrected status labels.
- `assets/README.md`: placeholder for future diagrams.
- `SECURITY.md`, `ROADMAP.md`, `CHANGELOG.md`, `CONTRIBUTING.md`: new supporting documents.
- `LICENSE`: MIT License.

**Public Demo Package (`src/serah_demo/`)**
- `models.py`: `VolumeData`, `SpreadData`, `CatalystData`, `Alert`, `EvidencePacket` dataclasses;
  content hash; stable packet ID.
- `validator.py`: 10+ validation rules including spread consistency, move_pct math, timestamp
  ordering, status transition guards, duplicate/idempotency handling.
- `packet_builder.py`: builds `EvidencePacket` from a validated `Alert`; computes tier;
  records provenance.
- `report_builder.py`: generates human-readable review packet text and compact operator report.
- `demo.py`: end-to-end demonstration run (valid path + rejection path).
- `main.py`: CLI entry point.
- `__main__.py`: enables `python -m serah_demo`.
- `__init__.py`: package init with safety disclaimer.

**Examples (`examples/`)**
- `README.md`: explains synthetic nature of all fixtures.
- `synthetic_alert.json`: valid SYNT-X scanner alert fixture.
- `invalid_alert.json`: deliberately malformed SYNT-BAD fixture for rejection testing.
- `valid_packet.json`: full evidence packet output fixture.
- `review_packet.md`: human-readable audit presentation.
- `operator_report.txt`: operator session summary.

**Tests (`tests/`)**
- `test_demo.py`: 25+ tests across `TestValidateAlert`, `TestBuildPacket`, `TestIdempotency`,
  `TestReportBuilder`, `TestSafetyProperties`.

**CI (`.github/workflows/ci.yml`)**
- Installs `serah-demo[dev]`, runs `pytest`; uses synthetic local fixtures only; no secrets;
  no network access; no market, brokerage, or order activity.

**Configuration**
- `pyproject.toml`: functional package configuration with `[dev]` extras, pytest config,
  coverage config, `serah-demo` console script entry point.
  Build backend: `setuptools.build_meta`.

### Changed

- Removed redundant `PUBLIC_EXPORT/` directory (contents preserved at repository root).

### Fixed

- `pyproject.toml` build-backend corrected from `setuptools.backends.legacy:build` to
  `setuptools.build_meta`.

---

## [Unreleased]

See `ROADMAP.md` for planned work.
