# Security Policy

## Scope

This repository contains the **public documentation and demo package** for the Serah project.

The `src/serah_demo` package is a read-only demonstration tool. It:

- Uses no network connections.
- Reads no external files beyond what is explicitly passed to its functions.
- Has no capability to place, draft, modify, cancel, or submit financial orders.
- Contains no secrets, credentials, or authentication tokens.
- Operates entirely on synthetic local fixtures.

The private production system (scanner, Obsidian vault, brokerage configuration, prompt templates,
and operational logs) is **not included** in this repository.

## Reporting a Vulnerability

If you discover a security issue in this public repository, please open a GitHub Issue with the
label **security** describing the problem. Do not include exploit code or sensitive details in a
public issue — if the issue is sensitive, reach out through GitHub's private vulnerability
reporting feature (Security → Report a vulnerability).

## What Is Not in Scope

- The private production system is not accessible from this repository. Vulnerabilities in the
  private system cannot be verified or reproduced using the public code.
- Claims about the private system's security posture cannot be confirmed from public sources.

## Dependencies

The `serah-demo` package has no runtime dependencies beyond the Python standard library
(Python 3.11+). Development dependencies are `pytest` and `pytest-cov`, both well-maintained
open-source projects.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | Yes       |

## Contact

For non-sensitive questions, open a GitHub Issue. For sensitive reports, use GitHub's private
vulnerability reporting feature.
