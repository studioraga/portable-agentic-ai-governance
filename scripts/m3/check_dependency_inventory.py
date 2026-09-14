#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SUPPORTED_MANIFEST_NAMES = {
    "requirements.txt",
    "requirements-dev.txt",
    "requirements-prod.txt",
    "requirements.lock",
    "poetry.lock",
    "Pipfile.lock",
    "uv.lock",
    "pdm.lock",
    "pylock.toml",
    "package-lock.json",
    "npm-shrinkwrap.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "Cargo.lock",
    "go.mod",
    "go.sum",
    "Gemfile.lock",
    "composer.lock",
}

EXCLUDED_DIRS = {".git", ".venv", "__pycache__", "var", "node_modules", ".pytest_cache"}


def parse_pyproject_dependencies(path: Path) -> list[str]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    try:
        import tomllib  # Python >= 3.11; release-authority Node1 uses this path.

        data = tomllib.loads(text)
        deps = data.get("project", {}).get("dependencies", [])
        return [str(x) for x in deps] if isinstance(deps, list) else []
    except ModuleNotFoundError:
        # Conservative fallback for Python 3.10. This only accepts a literal
        # project.dependencies array and fails closed on an unparseable value.
        m = re.search(
            r"(?ms)^\[project\]\s*(.*?)(?=^\[|\Z)",
            text,
        )
        if not m:
            return []
        section = m.group(1)
        dm = re.search(r"(?ms)^dependencies\s*=\s*\[(.*?)\]", section)
        if not dm:
            return []
        body = dm.group(1).strip()
        if not body:
            return []
        values = re.findall(r"['\"]([^'\"]+)['\"]", body)
        if not values:
            raise ValueError("could not parse project.dependencies")
        return values


def find_dependency_manifests(root: Path) -> list[str]:
    found: list[str] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        try:
            rel = p.relative_to(root)
        except ValueError:
            continue
        if any(part in EXCLUDED_DIRS for part in rel.parts[:-1]):
            continue
        name = p.name
        if name in SUPPORTED_MANIFEST_NAMES:
            found.append(str(rel))
            continue
        if name.startswith("requirements-") and name.endswith(".txt"):
            found.append(str(rel))
    return sorted(set(found))


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Inventory dependency declarations before interpreting OSV no-package-sources output."
    )
    ap.add_argument("root", help="Repository root")
    ap.add_argument("--json-out", help="Optional inventory JSON output")
    ap.add_argument(
        "--require-empty-runtime",
        action="store_true",
        help="Fail unless there are no declared runtime dependencies and no supported dependency manifests.",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"FAIL: repository root does not exist: {root}", file=sys.stderr)
        return 2

    try:
        runtime_dependencies = parse_pyproject_dependencies(root / "pyproject.toml")
    except (OSError, ValueError) as exc:
        print(f"FAIL: unable to inspect pyproject dependencies: {exc}", file=sys.stderr)
        return 2

    manifests = find_dependency_manifests(root)
    inventory = {
        "schema": "pag-m3-dependency-inventory-v1",
        "root": str(root),
        "runtime_dependencies": runtime_dependencies,
        "runtime_dependency_count": len(runtime_dependencies),
        "dependency_manifests": manifests,
        "dependency_manifest_count": len(manifests),
    }

    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n")
        out.chmod(0o600)

    print(json.dumps(inventory, sort_keys=True))

    if args.require_empty_runtime and (runtime_dependencies or manifests):
        print(
            "FAIL: OSV reported no package sources, but dependency declarations/manifests exist",
            file=sys.stderr,
        )
        return 3

    if args.require_empty_runtime:
        print("PASS: repository declares zero third-party runtime dependencies and no supported dependency manifests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
