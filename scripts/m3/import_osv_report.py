#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def severity(v: dict) -> str:
    values: list[str] = []
    raw = v.get("severity", [])
    if isinstance(raw, list):
        for item in raw:
            if not isinstance(item, dict):
                continue
            score = str(item.get("score", "")).upper()
            if "CRITICAL" in score:
                values.append("critical")
            elif "HIGH" in score:
                values.append("high")
            elif "MEDIUM" in score or "MODERATE" in score:
                values.append("medium")
            elif "LOW" in score:
                values.append("low")

    for db in (v.get("database_specific", {}), v.get("ecosystem_specific", {})):
        if not isinstance(db, dict):
            continue
        value = str(db.get("severity", "")).lower()
        if value in {"critical", "high", "medium", "moderate", "low"}:
            values.append("medium" if value == "moderate" else value)

    order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    return max(values, key=lambda x: order[x]) if values else "unknown"


def _collect_vulnerabilities(raw: dict) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    results = raw.get("results", [])
    if isinstance(results, list):
        for result in results:
            if not isinstance(result, dict):
                continue
            packages = result.get("packages", [])
            if not isinstance(packages, list):
                continue
            for package in packages:
                if not isinstance(package, dict):
                    continue
                vulnerabilities = package.get("vulnerabilities", [])
                if not isinstance(vulnerabilities, list):
                    continue
                for vuln in vulnerabilities:
                    if isinstance(vuln, dict):
                        findings.append({
                            "id": str(vuln.get("id", "unknown")),
                            "severity": severity(vuln),
                        })

    direct = raw.get("vulnerabilities", [])
    if isinstance(direct, list):
        for vuln in direct:
            if isinstance(vuln, dict):
                findings.append({
                    "id": str(vuln.get("id", "unknown")),
                    "severity": severity(vuln),
                })

    unique = {(x["id"], x["severity"]): x for x in findings}
    return [unique[k] for k in sorted(unique)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize OSV-Scanner JSON into PAG M3 vulnerability evidence."
    )
    parser.add_argument("input", help="OSV-Scanner JSON output")
    parser.add_argument("output", help="Normalized PAG vulnerability report")
    args = parser.parse_args()

    source = Path(args.input)
    destination = Path(args.output)

    if not source.is_file():
        print(f"FAIL: OSV input file does not exist: {source}", file=sys.stderr)
        print(
            "Generate it first with: scripts/m3/run_osv_scan.sh <repo> <raw-json>",
            file=sys.stderr,
        )
        return 2

    try:
        raw = json.loads(source.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: invalid OSV JSON {source}: {exc}", file=sys.stderr)
        return 2

    if not isinstance(raw, dict):
        print("FAIL: OSV JSON root must be an object", file=sys.stderr)
        return 2

    findings = _collect_vulnerabilities(raw)
    metadata = raw.get("pag_scan_metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}

    status = str(metadata.get("status", "completed"))
    scope = str(metadata.get("scope", "application-runtime-dependencies"))
    dependency_inventory = metadata.get("dependency_inventory")

    if status == "no-package-sources":
        if not isinstance(dependency_inventory, dict):
            print(
                "FAIL: no-package-sources evidence lacks dependency inventory",
                file=sys.stderr,
            )
            return 2
        if int(dependency_inventory.get("runtime_dependency_count", -1)) != 0:
            print(
                "FAIL: no-package-sources evidence conflicts with declared runtime dependencies",
                file=sys.stderr,
            )
            return 2
        if int(dependency_inventory.get("dependency_manifest_count", -1)) != 0:
            print(
                "FAIL: no-package-sources evidence conflicts with dependency manifests",
                file=sys.stderr,
            )
            return 2

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scanner": "osv-scanner",
        "scan_status": status,
        "scan_scope": scope,
        "vulnerabilities": findings,
    }
    if isinstance(dependency_inventory, dict):
        output["dependency_inventory"] = dependency_inventory

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    destination.chmod(0o600)
    print(
        f"PASS: normalized {len(findings)} OSV findings into {destination} "
        f"(status={status})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
