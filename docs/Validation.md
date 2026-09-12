# Validation and Verification — Milestones 0 and 1

Read `Prerequisites.md` first. Validation is deliberately layered so it is clear whether the machine passed only the dependency-free kernel checks or the complete M0-M1 acceptance suite.

## 1. Preflight

```bash
cd portable-agentic-ai-governance
./scripts/preflight_node1.sh
```

This checks OS context, commands, Python >=3.11, venv support, pytest availability, repository completeness, write permission, disk space, and—when `PAG_SECURITY_PROFILE=production`—the mandatory fail-closed secret contract.

## 2. One-shot Node1 deployment and validation

```bash
./deploy/deploy_node1.sh
```

The script:

1. runs preflight;
2. recreates `.venv` using `--system-site-packages` so an approved system pytest can be reused offline;
3. exports `PYTHONPATH=$REPO/src`;
4. writes a `.pth` entry inside the venv as an additional src-layout safeguard;
5. creates protected runtime directories;
6. verifies package import;
7. executes the complete validation driver.

## 3. Validation layers

### Layer A — syntax/import

```bash
source .venv/bin/activate
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python -m compileall -q src
python -c 'import portable_ai_governance; print(portable_ai_governance.__version__)'
```

### Layer B — standard-library sovereign self-tests

```bash
python scripts/run_self_tests.py
```

Expected M0-M1 checks:

```text
PASS illegal-transition
PASS budget-fail-closed
PASS request-signing-tamper
PASS persistent-replay
PASS risk-acceptance-prohibited
PASS evidence-tamper
PASS golden-onboarding
PASS unauthorized-onboarding
PASS mapping-complete
SELF-TESTS PASS: 9/9
```

### Layer C — extended pytest acceptance suite

```bash
python -m pytest -q
```

The validation driver first tries `python -m pytest` inside the active venv. If pytest is provided by the approved base Python but is not visible inside the venv, it falls back to that recorded base interpreter. In both cases `PYTHONPATH` is set to `src/`, so test collection imports the repository package deterministically.

If pytest is absent, the script reports that the extended suite was skipped. That is sufficient for a developer smoke test but **not** a claim that the complete M0-M1 acceptance gate ran.

### Layer D — control/framework completeness

```bash
python scripts/check_control_mapping.py
```

Every control in the M0-M1 catalog must have mapping data. Unknown mandatory controls fail closed.

### Layer E — golden AI-system onboarding

```bash
rm -f var/evidence/governance.jsonl
python -m portable_ai_governance.cli onboard \
  --input examples/golden_onboarding/system.json \
  --run-id validation-golden-001
```

Expected state path:

```text
START
VALIDATE_REQUEST
AUTHORIZE
LOAD_TRUSTED_CONTEXT
PLAN
POLICY_VALIDATE_PLAN
EXECUTE_BOUNDED_TOOLS
VERIFY_OUTPUT
RECORD_EVIDENCE
COMPLETE
```

### Layer F — signed evidence verification

```bash
python -m portable_ai_governance.cli verify-evidence
```

Expected result is `ok: true` / `verified`. Tampering with a recorded payload must cause verification failure.

### Layer G — security-profile contract

Lab:

```bash
export PAG_SECURITY_PROFILE=lab
python -m portable_ai_governance.cli validate-security
```

Production-profile contract test:

```bash
export PAG_SECURITY_PROFILE=production
export PAG_FAIL_CLOSED=1
export PAG_EVIDENCE_SIGNING_KEY="$(openssl rand -hex 32)"
export PAG_REQUEST_SIGNING_KEY="$(openssl rand -hex 32)"
export PAG_APPROVAL_SIGNING_KEY="$(openssl rand -hex 32)"
python -m portable_ai_governance.cli validate-security
```

The keys must be independent. These environment variables are bootstrap validation only; later milestones move keys into managed secret/KMS/HSM providers.

## 4. Mandatory negative coverage

M0-M1 must demonstrate at least:

- illegal graph transition is rejected;
- monotonic budget terminates when exceeded;
- modified HMAC-signed body is rejected;
- nonce replay remains rejected after reopening the persistent cache;
- an AI Risk Agent cannot accept risk;
- unauthorized onboarding is denied;
- evidence modification breaks chain/signature verification;
- an unmapped mandatory control fails acceptance.

## 5. Troubleshooting

### `ModuleNotFoundError: portable_ai_governance`

Cause: this repository uses a `src/` layout and Python was launched without the local package installed or `PYTHONPATH` configured.

Fix:

```bash
source .venv/bin/activate
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python -c 'import portable_ai_governance; print(portable_ai_governance.__version__)'
python -m pytest -q
```

The revised `deploy_node1.sh` and `validate_node1.sh` do this automatically.

### `No module named pytest`

Install `python3-pytest` through the approved Ubuntu repository or an approved Python package source, then recreate/re-run deployment.

### `python3 -m venv` fails

```bash
sudo apt install python3-venv
```

### production profile fails

Check `PAG_FAIL_CLOSED=1`, ensure all three secrets are present and independent, and do not include whitespace introduced by a malformed environment file.

## 6. Node2

Node2 is not required for M0-M1. No camera, media transport, GPU, or edge-service test belongs in the M0-M1 acceptance gate. Milestone 2 introduces generic edge workload/service identity controls; application repositories then supply their own device/media tests.
