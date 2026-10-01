# M10 deployment

## Node1 / release authority

Build M10 only on Node1:

```bash
python3 scripts/m10/build_m10_material.py \
  --m9-material "$PWD/var/m9-material" \
  --out "$PWD/var/m10-material"

./deploy/m10/one_shot_node1.sh \
  "$PWD/var/m9-material" \
  "$PWD/var/m10-material"
```

Node1 retains:

- `signing-private.pem`
- `workflow-decision-private.pem`

## Node2 / verifier

Node2 receives verifier material only:

```bash
./deploy/m10/one_shot_node2.sh \
  /path/to/m10-material \
  /path/to/m9-material/security-ops-manifest.json
```

Node2 must not contain either M10 private key.

## Full release generation

```bash
./deploy/m10/one_shot_node1_full.sh \
  var/m2-bootstrap var/m3-material var/m4-material var/m5-material \
  var/m6-material var/m7-material var/m8-material var/m9-material var/m10-material
```

After the final Node1 generation passes, do not regenerate it while validating Node2. Package and transfer one coherent M4-M10 verifier chain.

## M12 integration

Existing deployment semantics remain intact. M12 uses separate `deploy/m12/` one-shot and verifier packaging scripts; Node1 retains M12 private signing material and Node2 receives verifier-only material.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.
