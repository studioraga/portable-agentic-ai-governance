# M22 Validation

## Required gates

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/enterprise_security
./scripts/m22/validate_m22_local.sh
./scripts/m22/validate_m22_regression.sh
```

## Expected security properties

- exactly eight CISSP domains are represented;
- every M22 requirement has a unique ID and a mapping record;
- every referenced pre-M22 control exists in the control catalog;
- every `PARTIAL` or `GAP` requirement appears in the gap register;
- no M22 artifact asserts CISSP/ISO/CRA certification or conformity;
- M22 is bound to the immutable M21.1 parent commit;
- M22 source content is hash-bound even before the final commit;
- signed manifest tampering fails verification;
- Node2 verifier material contains no private signing key.

## Negative validation

Tamper test:

```bash
cp -a var/m22-material /tmp/m22-tamper
printf '\n' >> /tmp/m22-tamper/gap-register.json
python3 scripts/m22/validate_m22_node.py \
  --material /tmp/m22-tamper \
  --repo-root "$PWD"
# expected: non-zero
```

Private-key boundary test:

```bash
./deploy/m22/package_verifier_material.sh \
  var/m22-material \
  /tmp/m22-verifier.tar.gz
! tar -tzf /tmp/m22-verifier.tar.gz | grep -Eqi 'private.*pem'
```

## M23 relationship

M23 extends the frozen M22 enterprise-security foundation with enterprise human identity, OIDC federation evidence, strong MFA context, phishing-resistant privileged authentication, expiring entitlement review, signed single-use JIT privilege grants, dual-approved break-glass access, segregation of duties, and independent Node1/Node2 verification. The authoritative M23 documents are `docs/M23-Enterprise-Identity-MFA-PAM.md`, `docs/Prerequisites-M23.md`, `docs/Deployment-M23.md`, and `docs/Validation-M23.md`. Historical M0-M22 behavior and evidence remain immutable.
