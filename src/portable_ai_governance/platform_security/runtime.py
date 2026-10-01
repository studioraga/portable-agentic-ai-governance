from __future__ import annotations

import json
import subprocess
from pathlib import Path

from portable_ai_governance.supply_chain.signing import verify_blob

from .common import (
    M20_BASELINE_COMMIT,
    M20_BASELINE_TAG,
    sha256_file,
)
from .firmware import verify_descriptor


def evaluate_m21_material(
    root,
    repo_root=None,
):
    root = Path(root)

    required_artifacts = [
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
        "dice-demo.json",
        "m21-platform-manifest.json",
        "m21-platform-manifest.json.sig",
        "signing-public.pem",
    ]

    checks = [
        (
            f"present:{artifact}",
            (root / artifact).is_file(),
        )
        for artifact in required_artifacts
    ]

    if not all(
        result
        for _, result in checks
    ):
        return {
            "ok": False,
            "checks": checks,
            "errors": [
                "missing material"
            ],
        }

    manifest_path = (
        root
        / "m21-platform-manifest.json"
    )

    manifest_signature_path = (
        root
        / "m21-platform-manifest.json.sig"
    )

    public_key_path = (
        root
        / "signing-public.pem"
    )

    manifest = json.loads(
        manifest_path.read_text()
    )

    checks.append(
        (
            "manifest-signature",
            verify_blob(
                manifest_path,
                public_key_path,
                manifest_signature_path,
            ),
        )
    )

    for artifact_name, expected_digest in (
        manifest.get(
            "artifacts",
            {},
        ).items()
    ):
        artifact_path = (
            root
            / artifact_name
        )

        checks.append(
            (
                f"digest:{artifact_name}",
                artifact_path.is_file()
                and sha256_file(
                    artifact_path
                )
                == expected_digest,
            )
        )

    checks.append(
        (
            "firmware-signature-and-payload",
            verify_descriptor(
                root
                / "firmware-descriptor.json",
                root
                / "firmware.bin",
                public_key_path,
                root
                / "firmware-descriptor.json.sig",
            ),
        )
    )

    summary = json.loads(
        (
            root
            / "platform-validation-summary.json"
        ).read_text()
    )

    boundaries = manifest.get(
        "boundaries",
        {},
    )

    checks.extend(
        [
            (
                "no-fuse-burn",
                boundaries.get(
                    "no_fuse_burn"
                )
                is True,
            ),
            (
                "no-uefi-key-enrollment",
                boundaries.get(
                    "no_uefi_key_enrollment"
                )
                is True,
            ),
            (
                "no-firmware-flash",
                boundaries.get(
                    "no_firmware_flash"
                )
                is True,
            ),
            (
                "no-debug-fuse-change",
                boundaries.get(
                    "no_debug_fuse_change"
                )
                is True,
            ),
            (
                "no-host-reconfiguration",
                boundaries.get(
                    "no_host_reconfiguration"
                )
                is True,
            ),
            (
                "no-conformity-claim",
                boundaries.get(
                    "cra_conformity_claim"
                )
                is False,
            ),
            (
                "node2-verifier-only",
                boundaries.get(
                    "node2_verifier_only"
                )
                is True,
            ),
            (
                "summary-no-conformity",
                summary.get(
                    "cra_conformity_claim"
                )
                is False,
            ),
        ]
    )

    if repo_root:
        repo_root = Path(
            repo_root
        )

        current_head_result = subprocess.run(
            [
                "git",
                "-c",
                f"safe.directory={repo_root}",
                "-C",
                str(repo_root),
                "rev-parse",
                "HEAD",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        current_head = (
            current_head_result
            .stdout
            .strip()
        )

        checks.append(
            (
                "git-head-readable",
                current_head_result.returncode
                == 0
                and bool(
                    current_head
                ),
            )
        )

        manifest_m20 = (
            manifest.get(
                "m20_baseline_commit"
            )
            or manifest.get(
                "m20_commit"
            )
        )

        checks.append(
            (
                "m20-baseline-bound",
                manifest_m20
                == M20_BASELINE_COMMIT,
            )
        )

        baseline_exists = subprocess.run(
            [
                "git",
                "-c",
                f"safe.directory={repo_root}",
                "-C",
                str(repo_root),
                "cat-file",
                "-e",
                (
                    f"{M20_BASELINE_COMMIT}"
                    "^{commit}"
                ),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        checks.append(
            (
                "m20-baseline-exists",
                baseline_exists.returncode
                == 0,
            )
        )

        baseline_ancestry = subprocess.run(
            [
                "git",
                "-c",
                f"safe.directory={repo_root}",
                "-C",
                str(repo_root),
                "merge-base",
                "--is-ancestor",
                M20_BASELINE_COMMIT,
                current_head,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        checks.append(
            (
                "m20-baseline-ancestor",
                baseline_ancestry.returncode
                == 0,
            )
        )

        baseline_tag_result = subprocess.run(
            [
                "git",
                "-c",
                f"safe.directory={repo_root}",
                "-C",
                str(repo_root),
                "rev-list",
                "-n",
                "1",
                M20_BASELINE_TAG,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        resolved_baseline_tag = (
            baseline_tag_result
            .stdout
            .strip()
        )

        checks.append(
            (
                "m20-baseline-tag-bound",
                baseline_tag_result.returncode
                == 0
                and resolved_baseline_tag
                == M20_BASELINE_COMMIT,
            )
        )

        source_commit = (
            manifest.get(
                "m21_source_commit"
            )
        )

        if (
            source_commit
            and current_head
        ):
            source_exists = subprocess.run(
                [
                    "git",
                    "-c",
                    f"safe.directory={repo_root}",
                    "-C",
                    str(repo_root),
                    "cat-file",
                    "-e",
                    (
                        f"{source_commit}"
                        "^{commit}"
                    ),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            checks.append(
                (
                    "m21-source-exists",
                    source_exists.returncode
                    == 0,
                )
            )

            source_ancestry = subprocess.run(
                [
                    "git",
                    "-c",
                    f"safe.directory={repo_root}",
                    "-C",
                    str(repo_root),
                    "merge-base",
                    "--is-ancestor",
                    source_commit,
                    current_head,
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            checks.append(
                (
                    "m21-source-lineage",
                    source_ancestry.returncode
                    == 0,
                )
            )

        else:
            checks.append(
                (
                    "m21-source-exists",
                    False,
                )
            )

            checks.append(
                (
                    "m21-source-lineage",
                    False,
                )
            )

    ok = all(
        result
        for _, result in checks
    )

    return {
        "ok": ok,
        "checks": checks,
        "errors": (
            []
            if ok
            else [
                "one or more checks failed"
            ]
        ),
        "validation_mode": summary.get(
            "validation_mode"
        ),
        "production_ready": summary.get(
            "production_ready"
        ),
    }
