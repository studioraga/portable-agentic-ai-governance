import ast
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))


from portable_ai_governance.platform_security.common import (
    M20_BASELINE_COMMIT,
    M20_BASELINE_TAG,
)
from portable_ai_governance.platform_security.dice import (
    derive_cdi_demo,
)
from portable_ai_governance.platform_security.evaluation import (
    evaluate_profiles,
)
from portable_ai_governance.platform_security.firmware import (
    evaluate_update,
    make_descriptor,
    sign_descriptor,
    verify_descriptor,
)
from portable_ai_governance.supply_chain.signing import (
    generate_ed25519_keypair,
)


def load(name):
    return json.loads(
        (
            ROOT
            / "tests"
            / "fixtures"
            / "m21"
            / name
        ).read_text()
    )


def test_firmware_positive_and_rollback(
    tmp_path,
):
    payload = (
        ROOT
        / "tests"
        / "fixtures"
        / "m21"
        / "firmware.bin"
    )

    private_key = (
        tmp_path
        / "private.pem"
    )

    public_key = (
        tmp_path
        / "public.pem"
    )

    generate_ed25519_keypair(
        private_key,
        public_key,
    )

    descriptor_path = (
        tmp_path
        / "descriptor.json"
    )

    descriptor = make_descriptor(
        payload,
        "fw",
        "3.0.0",
        3,
        descriptor_path,
    )

    signature_path = (
        tmp_path
        / "descriptor.sig"
    )

    sign_descriptor(
        descriptor_path,
        private_key,
        signature_path,
    )

    assert verify_descriptor(
        descriptor_path,
        payload,
        public_key,
        signature_path,
    )

    positive = evaluate_update(
        "2.0.0",
        2,
        descriptor,
    )

    rollback = evaluate_update(
        "3.0.0",
        3,
        descriptor,
    )

    assert (
        positive["decision"]
        == "ACCEPT"
    )

    assert (
        rollback["decision"]
        == "REJECT"
    )


def test_tamper_fails(
    tmp_path,
):
    payload = (
        tmp_path
        / "firmware.bin"
    )

    payload.write_bytes(
        b"a"
    )

    private_key = (
        tmp_path
        / "private.pem"
    )

    public_key = (
        tmp_path
        / "public.pem"
    )

    generate_ed25519_keypair(
        private_key,
        public_key,
    )

    descriptor_path = (
        tmp_path
        / "descriptor.json"
    )

    make_descriptor(
        payload,
        "fw",
        "2",
        2,
        descriptor_path,
    )

    signature_path = (
        tmp_path
        / "descriptor.sig"
    )

    sign_descriptor(
        descriptor_path,
        private_key,
        signature_path,
    )

    payload.write_bytes(
        b"b"
    )

    assert not verify_descriptor(
        descriptor_path,
        payload,
        public_key,
        signature_path,
    )


def test_dice_deterministic():
    firmware_hash = (
        "aa" * 32
    )

    first = derive_cdi_demo(
        "11" * 32,
        firmware_hash,
        "cfg",
    )

    second = derive_cdi_demo(
        "11" * 32,
        firmware_hash,
        "cfg",
    )

    assert first == second
    assert len(first) == 64


def test_profile_evaluation_simulated():
    node1 = load(
        "node1-profile.json"
    )

    node2 = load(
        "node2-profile.json"
    )

    policy = json.loads(
        (
            ROOT
            / "governance"
            / "platform"
            / "m21"
            / "platform-security-policy.json"
        ).read_text()
    )

    result = evaluate_profiles(
        node1,
        node2,
        policy,
    )

    assert (
        result["validation_mode"]
        == "SIMULATED"
    )

    assert result["failed"] == 0

    assert not result[
        "production_ready"
    ]


def test_systemd_hardening_contract():
    unit_text = (
        ROOT
        / "examples"
        / "m21"
        / "systemd"
        / "pag-platform-demo.service"
    ).read_text()

    policy = json.loads(
        (
            ROOT
            / "governance"
            / "platform"
            / "m21"
            / "platform-security-policy.json"
        ).read_text()
    )

    required = policy[
        "service_required_directives"
    ]

    assert all(
        directive in unit_text
        for directive in required
    )


def test_mac_templates_exist():
    apparmor = (
        ROOT
        / "examples"
        / "m21"
        / "apparmor"
        / "usr.bin.pag-platform-demo"
    ).read_text()

    selinux = (
        ROOT
        / "examples"
        / "m21"
        / "selinux"
        / "pag_platform_demo.te"
    ).read_text()

    assert (
        "deny /dev/mem"
        in apparmor
    )

    assert (
        "init_daemon_domain"
        in selinux
    )


def test_threat_model_has_platform_threats():
    threat_model = json.loads(
        (
            ROOT
            / "governance"
            / "platform"
            / "m21"
            / "threat-model.json"
        ).read_text()
    )

    threats = (
        threat_model[
            "threats"
        ]
    )

    assert (
        len(threats)
        >= 10
    )

    assert any(
        "BMC" in item[
            "threat"
        ]
        for item in threats
    )


def test_boundaries_non_destructive():
    policy = json.loads(
        (
            ROOT
            / "governance"
            / "platform"
            / "m21"
            / "platform-security-policy.json"
        ).read_text()
    )

    boundaries = (
        policy[
            "boundaries"
        ]
    )

    assert boundaries[
        "no_fuse_burn"
    ]

    assert boundaries[
        "no_firmware_flash"
    ]

    assert boundaries[
        "no_uefi_key_enrollment"
    ]

    assert not boundaries[
        "cra_conformity_claim"
    ]


# ---------------------------------------------------------------------------
# M21 v0.21.1 regression coverage.
# ---------------------------------------------------------------------------

def test_m20_baseline_constant():
    assert (
        M20_BASELINE_COMMIT
        == "8b800814e576bcb08e12dc47c1039c5251c79d46"
    )

    assert (
        M20_BASELINE_TAG
        == "m20-cra-enterprise-final-freeze-v0.20.0"
    )


def test_m21_manifest_uses_baseline_and_source_binding():
    builder_path = (
        ROOT
        / "scripts"
        / "m21"
        / "build_m21_material.py"
    )

    tree = ast.parse(
        builder_path.read_text()
    )

    string_literals = {
        node.value
        for node in ast.walk(
            tree
        )
        if isinstance(
            node,
            ast.Constant,
        )
        and isinstance(
            node.value,
            str,
        )
    }

    assert (
        "m20_baseline_commit"
        in string_literals
    )

    assert (
        "m20_baseline_tag"
        in string_literals
    )

    assert (
        "m21_source_commit"
        in string_literals
    )

    # The corrected builder must never emit the legacy ambiguous
    # v0.21.0 field.
    assert (
        "m20_commit"
        not in string_literals
    )


def test_m21_builder_finalizes_signed_manifest():
    builder_path = (
        ROOT
        / "scripts"
        / "m21"
        / "build_m21_material.py"
    )

    tree = ast.parse(
        builder_path.read_text()
    )

    called_functions = {
        node.func.id
        for node in ast.walk(
            tree
        )
        if isinstance(
            node,
            ast.Call,
        )
        and isinstance(
            node.func,
            ast.Name,
        )
    }

    string_literals = {
        node.value
        for node in ast.walk(
            tree
        )
        if isinstance(
            node,
            ast.Constant,
        )
        and isinstance(
            node.value,
            str,
        )
    }

    assert (
        "write_json"
        in called_functions
    )

    assert (
        "sign_blob"
        in called_functions
    )

    assert (
        "secure_tree"
        in called_functions
    )

    assert (
        "m21-platform-manifest.json"
        in string_literals
    )

    assert (
        "m21-platform-manifest.json.sig"
        in string_literals
    )
