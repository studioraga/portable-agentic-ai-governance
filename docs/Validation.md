# Validation and Verification — Milestones 0 and 1

Read `Prerequisites.md` first. Validation is deliberately layered so it is clear whether the machine passed only the dependency-free kernel checks or the complete M0-M1 acceptance suite.

## 1. Preflight

```bash
cd portable-agentic-ai-governance
./scripts/preflight_node1.sh
```

This checks OS context, commands, Python >=3.11, venv support, pytest availability, repository completeness, write permission, disk space, and—when `PAG_SECURITY_PROFILE=production`—the mandatory fail-closed secret contract, minimum secret length, and signing-key separation.

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

### Layer H — production signing-key separation

```bash
PYTHONPATH="$PWD/src" python scripts/check_production_key_separation.py
```

Expected:

```text
PASS production-independent-signing-keys
PASS production-all-key-reuse-rejected
PASS production-evidence-request-reuse-rejected
PASS production-evidence-approval-reuse-rejected
PASS production-request-approval-reuse-rejected
KEY-SEPARATION TESTS PASS: 5/5
```

### Layer I — runtime filesystem privacy

```bash
PYTHONPATH="$PWD/src" python scripts/check_runtime_permissions.py
```

Expected:

```text
PASS evidence-ledger-mode-0600
RUNTIME-PERMISSION TESTS PASS
```

Operational checks:

```bash
stat -c '%a %U:%G %n' var var/evidence var/runs var/state
find var -type f -perm -0020 -print
find var -type f -perm -0002 -print
```

Directories must be `0700`; runtime files must be `0600`; the two `find` commands must produce no output.

## 4. Mandatory negative coverage

M0-M1 must demonstrate at least:

- illegal graph transition is rejected;
- monotonic budget terminates when exceeded;
- modified HMAC-signed body is rejected;
- nonce replay remains rejected after reopening the persistent cache;
- an AI Risk Agent cannot accept risk;
- unauthorized onboarding is denied;
- evidence modification breaks chain/signature verification;
- an unmapped mandatory control fails acceptance;
- production rejects reuse of all three signing keys;
- production rejects every partial two-key reuse combination;
- production accepts three valid independent signing keys;
- evidence ledger files are created mode `0600`;
- no runtime file is group-writable or world-writable.

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

Check `PAG_FAIL_CLOSED=1`, ensure all three secrets are present, at least 32 characters, and pairwise independent, and do not include whitespace introduced by a malformed environment file. Run `scripts/check_production_key_separation.py` to distinguish key-domain failures from other production-profile failures.

### runtime files are group-writable

Correct existing local runtime state with:

```bash
find var -type f -exec chmod 600 {} +
find var -type d -exec chmod 700 {} +
```

The hardened deploy/validation scripts use `umask 077`, and `EvidenceLedger` explicitly forces its ledger to `0600`, so newly created M0-M1 runtime artifacts must not regain group/world write permission.

## 6. Node2

Node2 is not required for M0-M1. No camera, media transport, GPU, or edge-service test belongs in the M0-M1 acceptance gate. Milestone 2 introduces generic edge workload/service identity controls; application repositories then supply their own device/media tests.


## Milestone 4 boundary
Milestone 4 adds deterministic AI-system-security controls for model governance, data provenance, pre-retrieval authorization, embedding policy, AI evaluation, and AI threat modeling. It introduces no autonomous LLM agent and no LLM-directed tool execution. See `docs/M4-AI-System-Security.md`.


## Milestone 5 validation

Run dependency preflight first, then `scripts/m5/validate_m5_local.sh`. Required negative gates reject expired/self-approved exceptions, required-but-unapproved DPIAs, stale continuous controls and automated certification claims. Production acceptance requires `scripts/m5/validate_combined_node.sh` to pass M2+M3+M4+M5 simultaneously.
