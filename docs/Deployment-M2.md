# Milestone 2 Deployment

## 1. Node1 prerequisites

Run the existing Ubuntu 24.04 prerequisite installer and base deployment first:

```bash
./deploy/install_prerequisites_ubuntu2404.sh
PAG_SECURITY_PROFILE=lab ./deploy/deploy_node1.sh
```

M2 additionally requires OpenSSL with TLS 1.3 support and network reachability between the selected nodes.

## 2. Generate deployment material on the trusted administration host

Set the identities that must appear in certificate SANs:

```bash
export PAG_TRUST_DOMAIN=pag.local
export PAG_NODE1_DNS=<node1-dns-name>
export PAG_NODE1_IP=<node1-ip>
export PAG_NODE2_DNS=<node2-dns-name>
export PAG_NODE2_IP=<node2-ip>

./deploy/m2/bootstrap_m2_material.sh "$PWD/var/m2-bootstrap"
```

This generates:

```text
var/m2-bootstrap/
  ca-private/              # CA custody only; never deploy
  node1/
    pki/
    secrets/
    identities.json
    workloads.json
  node2/
    pki/
    secrets/
    identities.json
    workloads.json
```

Transfer `node2/` only through an authenticated encrypted administrative channel. Never transfer `ca-private/`.

## 3. One-shot Node1 deployment

```bash
./deploy/m2/one_shot_node1.sh "$PWD/var/m2-bootstrap"
```

Default configuration location:

```text
~/.config/portable-ai-governance/m2
```

Or choose an explicit path:

```bash
./deploy/m2/one_shot_node1.sh \
  "$PWD/var/m2-bootstrap" \
  /opt/pag/m2-config
```

## 4. Node2 prerequisites and one-shot deployment

The M2 runtime supports Python 3.10+ so the Ubuntu 22.04 / Python 3.10 edge node can participate. On an Ubuntu 22.04 Node2:

```bash
./deploy/m2/install_prerequisites_ubuntu2204_node2.sh
```

Copy the repository/release to Node2, copy only the approved M2 node material, then run:

```bash
./deploy/m2/one_shot_node2.sh <material-root-containing-node2>
```

Node2 does not need the CA private key.

## 5. Start Node1 security probe manually

```bash
set -a
source ~/.config/portable-ai-governance/m2/production.env
set +a
source .venv/bin/activate
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"

python -m portable_ai_governance.services.security_probe \
  --host 0.0.0.0 \
  --port 9443
```

## 6. Optional hardened systemd installation on Node1

```bash
export PAG_SERVICE_USER="$USER"
export PAG_BIND_PORT=9443
./deploy/m2/install_node1_systemd.sh \
  "$HOME/.config/portable-ai-governance/m2"
```

The generated unit uses `UMask=0077`, `NoNewPrivileges`, `PrivateTmp`, `ProtectSystem=strict`, and explicit writable paths.

## 7. Firewall

Allow TCP/9443 only from the expected Node2 management/application network. Do not expose the validation probe to the Internet.

Example with UFW, after substituting the real Node2 IP:

```bash
sudo ufw allow from <NODE2-IP> to any port 9443 proto tcp
```

## 8. Remote verification from Node2

```bash
./scripts/m2/validate_remote_node1.sh <NODE1-DNS-OR-IP> 9443 \
  "$HOME/.config/portable-ai-governance/m2/production.env"
```

Expected: HTTP 200 and `PASS: remote Node1 M2 secure ping`.

## M12 integration

Existing deployment semantics remain intact. M12 uses separate `deploy/m12/` one-shot and verifier packaging scripts; Node1 retains M12 private signing material and Node2 receives verifier-only material.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.

## M16 integration — CRA Secure Update & Product Lifecycle
M16 consumes the existing milestone evidence without rewriting its historical responsibility. It adds support-period/lifecycle evidence, signed secure-update metadata and payload verification, anti-rollback decisions, update-retention/free-update policy checks, and end-of-support notification preparation. M16 keeps host OS/firmware modification and network rollout out of acceptance; see `docs/M16-CRA-Secure-Update-Product-Lifecycle.md`, `docs/Deployment-M16.md`, and `docs/Validation-M16.md`.
