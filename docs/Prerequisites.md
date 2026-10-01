# Common Prerequisites

This document covers repository-wide prerequisites. Milestone-specific additions live in `Prerequisites-M*.md` files.

## Supported baseline

The code requires Python 3.10 or newer and is designed for Linux-oriented validation/deployment workflows. Individual milestones may have additional host/platform assumptions.

## Core commands

Common workflows expect:

- `python3`;
- Python `venv` / `pip` for development environments;
- `git`;
- `bash`;
- `openssl`;
- `sha256sum`;
- `tar` / `gzip`;
- standard GNU user/file utilities.

Install only what is appropriate for the host and selected milestone. Do not mutate a production or evidence host merely to make an optional capability appear available.

## Python development environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

Direct source execution may use:

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
```

## Git and release prerequisites

Operators should be able to:

- fetch and verify tags;
- inspect exact commit identity;
- keep the working tree clean for release evidence generation;
- create release archives with `git archive`;
- keep runtime evidence and secrets outside tracked source.

## Runtime storage

Generated evidence is runtime state, not source. Keep it in protected local directories such as `var/` or milestone-specific installation paths under the user's configuration directory.

Private signing material must use restrictive permissions and must never be copied into verifier-only bundles.

## Node roles

The repository uses two logical roles:

- **Node1 / release authority** — may generate and sign evidence;
- **Node2 / independent verifier** — verifies signed evidence without the private release signing key.

A milestone may be exercised locally with fixtures, but LIVE cross-node acceptance should preserve this authority split.

## Current M21 additions

See [`Prerequisites-M21.md`](Prerequisites-M21.md) for platform-audit tools such as `mokutil`, `fwupdmgr`, `systemd-analyze`, MAC utilities, and `tpm2-tools`.
