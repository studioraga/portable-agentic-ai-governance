# M17 Validation

Run focused tests and local acceptance:

```bash
python3 -m pytest -q tests/cra_annex_evidence
./scripts/m17/validate_m17_local.sh
```

Release gate:

```bash
./scripts/m17/validate_m17_regression.sh
```

Acceptance requires all 22 Annex I rows, 14 Part I + 8 Part II, digest-valid evidence references, explicit gaps, no CRA conformity claim, and M11–M16 baseline bindings.

## M18 integration

M18 assembles the CRA Article 31 / Annex VII technical-documentation evidence file from the evidence produced by M3-M17. This document remains an input/reference to that assembly; M18 does not retroactively change this milestone's scope. The M18 technical file is explicitly a draft evidence package: it makes no CRA conformity claim, does not perform a conformity assessment, does not authorize CE marking, and does not fabricate the EU Declaration of Conformity. Product-specific production/security test evidence that remains incomplete is carried forward to M19 as an explicit readiness gap.
