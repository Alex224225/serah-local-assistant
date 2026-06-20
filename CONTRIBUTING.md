# Contributing

Thank you for your interest in Serah. Contributions to the public documentation and demo package
are welcome.

---

## Scope of This Repository

This is a **public documentation and demo repository**. The private production system — including
the scanner, Obsidian vault, brokerage configuration, agent prompt templates, and operational
data — is not included and is not open for external contribution.

Contributions are welcomed in:

- `docs/` — Documentation improvements, corrections, and clarifications.
- `src/serah_demo/` — Bug fixes or improvements to the public demo package.
- `tests/` — Additional test cases for the demo package.
- `examples/` — Additional synthetic fixture files (must use fictional data only).
- Root files — README, ROADMAP, CHANGELOG, SECURITY, CONTRIBUTING improvements.

---

## Ground Rules

1. **No real data.** All fixture data must use obviously fictional symbols (e.g., `SYNT-X`,
   `SynthEx Corp`). Do not introduce any real ticker symbols, account numbers, names,
   email addresses, or machine paths.

2. **No brokerage capability.** Do not add any code that connects to a brokerage, retrieves
   live market data, places orders, or manages real accounts.

3. **No private system reconstruction.** Do not attempt to reconstruct or reverse-engineer
   the private production system from documentation hints.

4. **Minimal dependencies.** Prefer the Python standard library. Any new runtime dependency
   requires justification.

5. **Tests required.** Any change to `src/serah_demo/` should include or update tests
   in `tests/test_demo.py`.

6. **CI must pass.** All tests must pass in the CI workflow before a PR is merged.

---

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Alex224225/serah-local-assistant.git
cd serah-local-assistant

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run the demo
python -m serah_demo
```

Requirements: Python 3.11+

---

## Submitting a Pull Request

1. Fork the repository and create a branch from `main`.
2. Make your changes following the ground rules above.
3. Ensure `pytest` passes locally.
4. Open a pull request with a clear description of what you changed and why.
5. Wait for review. The maintainer will respond when available.

---

## Reporting Issues

Open a GitHub Issue with a clear description of the problem. For security issues, see
[SECURITY.md](SECURITY.md).

---

## Code Style

- Python code follows PEP 8 with a soft line length of 100 characters.
- Docstrings use the one-line or multi-line format (no specific framework required).
- No type: ignore comments unless strictly necessary; prefer proper typing.

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License
(see [LICENSE](LICENSE)).
