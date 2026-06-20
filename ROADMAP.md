# Roadmap

This roadmap covers the public repository and the public demo package (`serah_demo`).
Items specific to the private production system are noted as such and are not tracked here.

---

## Status Legend

| Label | Meaning |
|-------|---------|
| **Implemented in private system** | Exists and runs in the private system; not available in this repository |
| **Demonstrated in this repository** | Working code in this public repo |
| **Planned** | Intended for future implementation |
| **Experimental** | Under active exploration; design not finalised |

---

## Near-term (Current Focus)

- [x] Rewrite root README with accurate status labels and architecture overview
- [x] Create runnable public demo package (`src/serah_demo/`)
- [x] Add synthetic fixture examples under `examples/`
- [x] Add CI workflow (install, pytest, no secrets, no network)
- [x] Publish MIT license, SECURITY.md, CONTRIBUTING.md, CHANGELOG.md
- [x] Fix `pyproject.toml` build-backend to `setuptools.build_meta`
- [ ] Add architecture diagrams to `assets/` (SVG or PNG)
- [ ] Expand synthetic fixture coverage (edge cases, boundary values)
- [ ] Document the context-handoff and daily-briefing systems in more detail

## Medium-term

- [ ] Add more example validator test cases covering all documented validation rules
- [ ] Publish a rendered demo output (HTML or PDF) so readers can see what the pipeline produces
  without running it locally
- [ ] Add a `DEMO.md` showing a complete annotated run of `python -m serah_demo`
- [ ] Improve `docs/serah-architecture.md` with a worked example of the ask-me-first gate flow
- [ ] Add a decision log documenting key design trade-offs

## Long-term / Experimental

These items are speculative and may change significantly or be dropped.

- [ ] Voice interface integration *(Planned — private system)*
- [ ] Browser-controlled research automation *(Planned — private system)*
- [ ] Local dashboard for session review *(Planned — private system)*
- [ ] Additional safety-engineering case studies published as documentation

## Out of Scope for This Repository

The following are part of the private system and will not be published here:

- Full Obsidian vault structure and active notes
- Brokerage configuration, authentication, or order-execution code
- Scanner implementation and real market data retrieval
- Agent prompt templates used in the private system
- Personal operational logs and vault contents
- Machine-specific configuration or local Windows paths

---

*Last updated: 2026-06*
