# M27 Prerequisites

## Immutable parent

M27 must start from commit `82b9331edbe1d12f30b6283b15584ac506038018`, tag `m26-soc-incident-backup-dr-v0.26.0`.

## Minimum software

- Git
- Python 3.10+
- `venv`
- `pytest` via the project development extra
- OpenSSL/cryptography support already required by previous milestones

## Optional production AppSec tooling

The deterministic validation adapters do not install external scanners. For production evidence, integrate approved tools such as:

- SAST: Semgrep, Bandit, CodeQL
- Secret scanning: Gitleaks, TruffleHog
- SCA: OSV-Scanner, Grype, Trivy
- IaC/container: Checkov, Trivy, Hadolint
- DAST/API: OWASP ZAP, Schemathesis
- Fuzzing: Atheris, Hypothesis, libFuzzer, AFL++
- Penetration test: authorized independent internal or external assessor

Do not place scanner API tokens, private keys, proprietary reports, or raw sensitive payloads in Git. Generated M27 material belongs under ignored `var/m27-*` paths.
