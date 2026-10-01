# M21 Validation

M21 validation combines focused source tests, deterministic fixture validation, CI/static contracts, LIVE two-node evidence, negative tests, and the full M0–M21 regression chain.

## Focused tests

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/platform_security
```

These tests cover firmware signing/rollback behavior, tamper rejection, DICE determinism, simulated profile evaluation, systemd/MAC reference contracts, safety boundaries, and v0.21.1 source/baseline binding.

## Local deterministic validation

```bash
./scripts/m21/validate_m21_local.sh
```

This builds signed M21 material from fixture profiles, verifies it with the private key present, removes the private key, and verifies the same material as verifier-only evidence.

Expected validation mode: `SIMULATED`.

## CI/static gate

```bash
./scripts/m21/ci_validate.sh
```

This runs focused tests, Python compilation, JSON parsing, systemd unit verification when available, and AppArmor syntax validation when the parser is available.

## Full regression

```bash
set -o pipefail
./scripts/m21/validate_m21_regression.sh 2>&1 | tee /tmp/m21-regression.log
```

Expected terminal result:

```text
PASS: full M0-M21 regression + M20/M21 acceptance complete
```

## LIVE Node1/Node2 acceptance

LIVE acceptance additionally requires:

1. Node2 LIVE profile capture;
2. Node1 LIVE profile capture;
3. Node1 signed M21 material generation;
4. Node1 authority verification;
5. verifier-only package generation;
6. Node2 independent verification;
7. tamper rejection;
8. private-key injection rejection;
9. source/tag parity checks.

## v0.21.1 source-binding correction

v0.21.1 separates milestone ancestry from evidence-generation source identity.

The signed manifest records:

```text
m20_baseline_commit = 8b800814e576bcb08e12dc47c1039c5251c79d46
m20_baseline_tag    = m20-cra-enterprise-final-freeze-v0.20.0
m21_source_commit   = e83ebf03c6d1ce2f4076ab8e3dae8282e4aeb880
```

The verifier checks:

- Git HEAD readability;
- M20 baseline equality;
- M20 baseline commit existence;
- M20 baseline ancestry;
- M20 tag resolution to the exact baseline commit;
- M21 source commit existence;
- M21 source ancestry/lineage.

This permits later descendant source revisions to verify historical M21 evidence without incorrectly requiring the current HEAD to equal the M20 baseline.

## Current preserved LIVE result

| Check | Result |
|---|---|
| Validation mode | `LIVE` |
| Required checks passed | 15 |
| Required checks open | 2 |
| Production ready | `false` |
| CRA conformity claim | `false` |

Open required checks:

- `secure-boot-enabled`;
- `mac-enforcing`.

The verifier may still return `ok=true` for evidence integrity while the platform validation summary truthfully reports `production_ready=false`.
