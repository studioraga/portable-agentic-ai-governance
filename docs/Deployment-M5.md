# Milestone 5 deployment

## Node1

```bash
./deploy/m5/one_shot_node1.sh "$PWD/var/m4-material" "$PWD/var/m5-material"
```

Full stack:

```bash
./deploy/m5/one_shot_node1_full.sh \
  "$PWD/var/m2-bootstrap" \
  "$PWD/var/m3-material" \
  "$PWD/var/m4-material" \
  "$PWD/var/m5-material"
```

## Verifier bundle

```bash
./deploy/m5/package_verifier_material.sh \
  "$PWD/var/m5-material" \
  "$PWD/../m5-verifier-material.tar.gz"
```

The verifier bundle must not contain `signing-private.pem`.

## Node2

```bash
./deploy/m5/one_shot_node2.sh \
  /path/to/m5-material \
  /path/to/m4/ai-security-manifest.json
```

Full stack:

```bash
./deploy/m5/one_shot_node2_full.sh \
  /path/to/m2-material-root \
  /path/to/m3-verifier-material \
  /path/to/m4-verifier-material \
  /path/to/m5-verifier-material
```

## Continuous-control refresh on Node1

M5 continuous-control evidence has a 24-hour freshness limit. Refresh it on the release-authority node and redistribute verifier-only material:

```bash
python3 scripts/m5/refresh_continuous_controls.py \
  --m4-material "$PWD/var/m4-material" \
  --m5-material "$PWD/var/m5-material"
```

Optional six-hour systemd timer:

```bash
./deploy/m5/install_continuous_controls_timer.sh \
  "$PWD/var/m4-material" \
  "$PWD/var/m5-material"
```

The timer exists only on the signing/release-authority node. Verifier-only nodes never receive the private M5 signing key; refreshed verifier material must be redistributed through the approved deployment channel.

## Downstream-bound M5 material (M6/M7 and later)

When M6/M7 bind an M5 release, `var/m5-material/.pag-downstream-bound.json` marks that M5 directory immutable. The M5 builder, refresh command, and timer installer refuse to mutate it. To produce new continuous-control evidence after downstream agents exist, create a new release generation through the latest downstream full release workflow so M5, M6, M7 (and later milestones) are rebuilt/re-signed in dependency order and redistributed together.

## M12 integration

Existing deployment semantics remain intact. M12 uses separate `deploy/m12/` one-shot and verifier packaging scripts; Node1 retains M12 private signing material and Node2 receives verifier-only material.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.
