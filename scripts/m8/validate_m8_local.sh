#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}";python3 -m pytest -q "$ROOT/tests/action_agent/test_m8_action_agent.py";echo 'PASS: Milestone 8 approval-controlled actions validation complete'
