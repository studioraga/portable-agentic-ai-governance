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
