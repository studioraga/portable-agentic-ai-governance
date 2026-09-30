# M11 — CRA Product Security Foundation

M11 creates the authoritative engineering specification for future CRA work. It does **not** claim CRA conformity and does not implement ENISA reporting side effects.

## Authority split

- **Node1 — CRA release authority:** owns the authoritative requirement matrix, produces deterministic coverage reports, and signs the M11 manifest. The M11 private signing key remains on Node1.
- **Node2 — CRA independent verifier:** receives only verifier material, verifies signature/digests and runs read-only M11 checks. Node2 must not receive M11 private signing material.

## Authoritative inputs

`governance/cra/cra-requirements.json` maps manufacturer/product-security obligations to current M0-M10 implementation, current coverage (`met`, `partial`, `gap`), a future `CRA-*` control, and the target milestone M11-M20.

The matrix covers the M11 engineering baseline for Article 13, Article 14, Article 31, Annex I Parts I-II, Annex II, and Annex VII. Obligation text is paraphrased for engineering use; the exact `legal_reference` controls and must be checked against the current EUR-Lex text.

## M11 non-goals

M11 does not implement active-exploitation intelligence, statutory deadline clocks, SRP submission, PSIRT/CVD intake, user notification, secure update distribution, technical-file generation, conformity assessment, or CE/DoC issuance. Those are explicitly assigned to M12-M20.

## Local validation

```bash
./scripts/m11/validate_m11_local.sh
```

## Node1

```bash
./deploy/m11/one_shot_node1.sh ./var/m11-material
./deploy/m11/package_verifier_material.sh ./var/m11-material ./var/m11-verifier.tar.gz
```

Transfer only the verifier package/material to Node2. Never transfer `signing-private.pem`.

## Node2

After extracting the verifier package:

```bash
./deploy/m11/one_shot_node2.sh /path/to/m11-material
```

A passing M11 validation proves integrity and traceability of the CRA engineering baseline; it does not prove CRA legal conformity.
