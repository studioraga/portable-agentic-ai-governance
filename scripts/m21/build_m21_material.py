#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))


from portable_ai_governance.action_agent.common import secure_tree
from portable_ai_governance.platform_security.common import (
    M20_BASELINE_COMMIT,
    M20_BASELINE_TAG,
    sha256_file,
    write_json,
)
from portable_ai_governance.platform_security.dice import derive_cdi_demo
from portable_ai_governance.platform_security.evaluation import evaluate_profiles
from portable_ai_governance.platform_security.firmware import (
    evaluate_update,
    make_descriptor,
    sign_descriptor,
)
from portable_ai_governance.supply_chain.signing import (
    generate_ed25519_keypair,
    sign_blob,
)


# ---------------------------------------------------------------------------
# Command-line arguments.
# ---------------------------------------------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument(
    "--node1-profile",
    required=True,
)

parser.add_argument(
    "--node2-profile",
    required=True,
)

parser.add_argument(
    "--out",
    required=True,
)

args = parser.parse_args()


# ---------------------------------------------------------------------------
# Restrictive default permissions for generated evidence.
# ---------------------------------------------------------------------------

os.umask(0o077)

out = Path(args.out).resolve()

out.mkdir(
    parents=True,
    exist_ok=True,
    mode=0o700,
)


# ---------------------------------------------------------------------------
# Copy M21 governance and policy material.
# ---------------------------------------------------------------------------

for rel, name in [
    (
        "governance/platform/m21/platform-security-policy.json",
        "platform-security-policy.json",
    ),
    (
        "governance/platform/m21/m21-control-mapping.json",
        "m21-control-mapping.json",
    ),
    (
        "governance/platform/m21/threat-model.json",
        "threat-model.json",
    ),
    (
        "governance/platform/m21/key-management-policy.json",
        "key-management-policy.json",
    ),
    (
        "governance/platform/m21/measured-boot-policy.json",
        "measured-boot-policy.json",
    ),
]:
    shutil.copy2(
        ROOT / rel,
        out / name,
    )

    os.chmod(
        out / name,
        0o600,
    )


# ---------------------------------------------------------------------------
# Copy Node1 and Node2 platform profiles.
# ---------------------------------------------------------------------------

for src, name in [
    (
        args.node1_profile,
        "node1-platform-profile.json",
    ),
    (
        args.node2_profile,
        "node2-platform-profile.json",
    ),
]:
    shutil.copy2(
        src,
        out / name,
    )

    os.chmod(
        out / name,
        0o600,
    )


# ---------------------------------------------------------------------------
# Evaluate LIVE/SIMULATED platform profiles.
# ---------------------------------------------------------------------------

node1_profile = json.loads(
    (
        out
        / "node1-platform-profile.json"
    ).read_text()
)

node2_profile = json.loads(
    (
        out
        / "node2-platform-profile.json"
    ).read_text()
)

policy = json.loads(
    (
        out
        / "platform-security-policy.json"
    ).read_text()
)

write_json(
    out / "platform-validation-summary.json",
    evaluate_profiles(
        node1_profile,
        node2_profile,
        policy,
    ),
)


# ---------------------------------------------------------------------------
# Build and sign the synthetic M21 firmware evidence.
# ---------------------------------------------------------------------------

firmware_path = out / "firmware.bin"

shutil.copy2(
    ROOT / "tests/fixtures/m21/firmware.bin",
    firmware_path,
)

os.chmod(
    firmware_path,
    0o600,
)


private_key_path = out / "signing-private.pem"
public_key_path = out / "signing-public.pem"

generate_ed25519_keypair(
    private_key_path,
    public_key_path,
)


descriptor_path = out / "firmware-descriptor.json"
descriptor_signature_path = out / "firmware-descriptor.json.sig"

descriptor = make_descriptor(
    firmware_path,
    "PAG-M21-DEMO-FW",
    "3.0.0",
    3,
    descriptor_path,
)

sign_descriptor(
    descriptor_path,
    private_key_path,
    descriptor_signature_path,
)


# ---------------------------------------------------------------------------
# Generate anti-rollback evidence.
# ---------------------------------------------------------------------------

write_json(
    out / "rollback-positive.json",
    evaluate_update(
        "2.0.0",
        2,
        descriptor,
    ),
)

write_json(
    out / "rollback-negative.json",
    evaluate_update(
        "4.0.0",
        4,
        descriptor,
    ),
)


# ---------------------------------------------------------------------------
# Generate DICE semantics demonstration.
# ---------------------------------------------------------------------------

firmware_sha256 = sha256_file(
    firmware_path
)

dice = {
    "mode": "DEMONSTRATION_ONLY",
    "hardware_dice_claim": False,
    "first_mutable_code_sha256": firmware_sha256,
    "cdi_sha256": derive_cdi_demo(
        "11" * 32,
        firmware_sha256,
        "PAG-M21",
    ),
    "note": (
        "Software derivation demonstrates DICE semantics only; "
        "hardware DICE must be evidenced by the platform."
    ),
}

write_json(
    out / "dice-demo.json",
    dice,
)


# ---------------------------------------------------------------------------
# Copy service-isolation and MAC reference-policy examples.
# ---------------------------------------------------------------------------

for rel, name in [
    (
        "examples/m21/systemd/pag-platform-demo.service",
        "pag-platform-demo.service",
    ),
    (
        "examples/m21/apparmor/usr.bin.pag-platform-demo",
        "apparmor-profile",
    ),
    (
        "examples/m21/selinux/pag_platform_demo.te",
        "selinux-policy.te",
    ),
]:
    shutil.copy2(
        ROOT / rel,
        out / name,
    )

    os.chmod(
        out / name,
        0o600,
    )


# ---------------------------------------------------------------------------
# Artifacts protected by the signed M21 manifest.
# ---------------------------------------------------------------------------

artifact_names = [
    "platform-security-policy.json",
    "m21-control-mapping.json",
    "threat-model.json",
    "key-management-policy.json",
    "measured-boot-policy.json",
    "pag-platform-demo.service",
    "apparmor-profile",
    "selinux-policy.te",
    "node1-platform-profile.json",
    "node2-platform-profile.json",
    "platform-validation-summary.json",
    "firmware.bin",
    "firmware-descriptor.json",
    "firmware-descriptor.json.sig",
    "rollback-positive.json",
    "rollback-negative.json",
    "dice-demo.json",
    "signing-public.pem",
]


# ---------------------------------------------------------------------------
# Bind generated evidence to the exact M21 source revision.
# ---------------------------------------------------------------------------

source_commit_result = subprocess.run(
    [
        "git",
        "-c",
        f"safe.directory={ROOT}",
        "-C",
        str(ROOT),
        "rev-parse",
        "HEAD",
    ],
    capture_output=True,
    text=True,
    check=False,
)

source_commit = source_commit_result.stdout.strip()

if (
    source_commit_result.returncode != 0
    or not source_commit
):
    raise RuntimeError(
        "Unable to resolve current Git HEAD for "
        "M21 source binding: "
        f"{source_commit_result.stderr.strip()}"
    )


# ---------------------------------------------------------------------------
# M21 signed-manifest content.
# ---------------------------------------------------------------------------

manifest = {
    "version": "0.21.1",
    "milestone": "M21",
    "purpose": (
        "Embedded Linux & Platform Security Validation"
    ),

    # Immutable M20 ancestry.
    "m20_baseline_commit": M20_BASELINE_COMMIT,

    # Immutable M20 release identity.
    "m20_baseline_tag": M20_BASELINE_TAG,

    # Exact M21 source revision used to generate this evidence.
    "m21_source_commit": source_commit,

    "artifacts": {
        name: sha256_file(out / name)
        for name in artifact_names
    },

    "boundaries": policy["boundaries"],
}


# ---------------------------------------------------------------------------
# Write and sign the M21 evidence manifest.
# ---------------------------------------------------------------------------

manifest_path = (
    out
    / "m21-platform-manifest.json"
)

manifest_signature_path = (
    out
    / "m21-platform-manifest.json.sig"
)

write_json(
    manifest_path,
    manifest,
)

sign_blob(
    manifest_path,
    private_key_path,
    manifest_signature_path,
)


# ---------------------------------------------------------------------------
# Apply restrictive permissions to the generated evidence tree.
# ---------------------------------------------------------------------------

secure_tree(out)


# ---------------------------------------------------------------------------
# Final generation status.
# ---------------------------------------------------------------------------

summary = json.loads(
    (
        out
        / "platform-validation-summary.json"
    ).read_text()
)

print(
    "PASS: M21 platform-security material "
    f"generated at {out}"
)

print(
    "PASS: validation_mode="
    f"{summary['validation_mode']}"
)
