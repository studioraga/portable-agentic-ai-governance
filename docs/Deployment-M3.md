# Milestone 3 Deployment

## 1. Install/verify release-authority vulnerability scanner on Node1

M3 production vulnerability evidence requires a real scanner. The generated
`m3-offline-fixture` report is test-only.

```bash
./deploy/m3/install_osv_scanner.sh
export PATH="$HOME/.local/bin:$PATH"
./scripts/m3/preflight_release_authority.sh
```

The installer defaults to pinned OSV-Scanner `v2.4.0` and verifies the downloaded
binary against the checksum file published with the same official release.
Override only through an explicit reviewed change:

```bash
export PAG_OSV_SCANNER_VERSION=v2.4.0
```

## 2. Build release-authority material on Node1

```bash
source .venv/bin/activate
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python scripts/m3/build_m3_material.py --root "$PWD" --out "$PWD/var/m3-material"
```

This creates software/AI BOMs, digest locks, provenance, vulnerability policy,
a test-only fixture report, and an Ed25519 release keypair. `signing-private.pem`
remains on trusted release-authority Node1.

## 3. Generate real OSV vulnerability evidence

Do not type `/path/to/raw-osv-output.json` literally. Generate it:

```bash
./scripts/m3/run_osv_scan.sh \
  "$PWD" \
  "$PWD/var/m3-scans/raw-osv-output.json"

python scripts/m3/import_osv_report.py \
  "$PWD/var/m3-scans/raw-osv-output.json" \
  "$PWD/var/m3-material/vulnerability-report.json"
```

Or use the combined helper:

```bash
./scripts/m3/scan_and_import_osv.sh \
  "$PWD" \
  "$PWD/var/m3-material/vulnerability-report.json"
```

OSV-Scanner exit code `1` means vulnerabilities were found; it is still valid
scanner evidence. M3 vulnerability policy makes the allow/block decision.

Verify the normalized report:

```bash
python -m json.tool var/m3-material/vulnerability-report.json
```

The scanner must be `osv-scanner`, not `m3-offline-fixture`.

## 4. Node1 M3 one-shot deployment

Production default: acquire a real OSV scan automatically.

```bash
export PATH="$HOME/.local/bin:$PATH"
./deploy/m3/one_shot_node1.sh "$PWD/var/m3-material"
```

Alternatively use externally produced normalized evidence:

```bash
export PAG_M3_VULN_REPORT_SOURCE=/secure/path/vulnerability-report.json
./deploy/m3/one_shot_node1.sh "$PWD/var/m3-material"
```

Fixture evidence is allowed only for explicit local/test validation:

```bash
PAG_M3_ALLOW_FIXTURE_SCAN=1 ./deploy/m3/one_shot_node1.sh "$PWD/var/m3-material"
```

Never use that mode for production acceptance.

## 5. Package verifier-only material for Node2

```bash
./deploy/m3/package_verifier_material.sh \
  "$PWD/var/m3-material" \
  "$PWD/../m3-verifier-material.tar.gz"
sha256sum -c "$PWD/../m3-verifier-material.tar.gz.sha256"
```

The verifier bundle must exclude `signing-private.pem`.

## 6. Node2 M3-only deployment

After securely transferring and extracting the verifier-only bundle:

```bash
./deploy/m3/one_shot_node2.sh /path/to/m3-material
```

Node2 does not need OSV-Scanner to verify an already signed release. The scanner
belongs on the trusted release-authority/CI side unless Node2 is itself a build
or release authority.

## 7. Full M0-M3 one-shot deployment

Node1:

```bash
export PATH="$HOME/.local/bin:$PATH"
./deploy/m3/one_shot_node1_full.sh /path/to/m2-bootstrap "$PWD/var/m3-material"
```

Node2:

```bash
./deploy/m3/one_shot_node2_full.sh /path/to/node2-m2-material /path/to/m3-verifier-material
```

Both finish by executing combined M2+M3 production validation.

## OSV no-package-sources handling

OSV-Scanner V2 can return exit code `128` with `No package sources found` when a source tree contains no supported dependency manifests. M3 never treats exit `128` as a clean scan by itself.

`run_osv_scan.sh` first runs the real OSV source scan. If OSV reports `No package sources found`, the script invokes `check_dependency_inventory.py` and only emits zero-dependency evidence when both of the following are true:

- `project.dependencies` in `pyproject.toml` is empty; and
- no supported dependency manifest/lock file exists outside excluded generated/development directories.

If either condition is false, release validation fails closed. The normalized report records `scan_status=no-package-sources`, the scan scope, and the dependency inventory used to justify that result.

The current framework declares no third-party runtime Python dependencies, so a verified `no-package-sources` result is valid for the application dependency scope. It is not a machine-wide OS vulnerability scan and does not replace host/container vulnerability management.

## Generated M3 material permissions

Release-authority material is private by default. `build_m3_material.py` uses
`umask 077`, creates generated directories as mode `0700`, and finalizes all
generated M3 files as mode `0600`, including BOMs, provenance, locks, prompts,
tool registry, signatures and public verification material. Deployment keeps
the verifier-side copy owner-only as well.

Validation commands:

```bash
find var/m3-scans var/m3-material -type f -perm -0020 -print
find var/m3-scans var/m3-material -type f -perm -0002 -print
```

Both commands must produce no output before verifier packaging or production
promotion.

## M12 integration

Existing deployment semantics remain intact. M12 uses separate `deploy/m12/` one-shot and verifier packaging scripts; Node1 retains M12 private signing material and Node2 receives verifier-only material.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.
