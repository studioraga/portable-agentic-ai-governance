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
