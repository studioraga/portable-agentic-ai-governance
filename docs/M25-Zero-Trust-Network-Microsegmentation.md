# M25 — Zero-Trust Network & Micro-segmentation

## Purpose

M25 extends the immutable M24 release with machine-readable network zones, default-deny flow policy, workload-identity-bound mTLS requirements, egress allowlisting, detection rules, deterministic firewall rendering, signed evidence, and independent Node2 verification.

M25 closes the M22 `CISSP-D4-002` engineering gap. It does not claim that every physical switch, VLAN, router, IDS appliance, DNS resolver, VPN, or cloud security group in a production environment is configured merely because the repository policy validates.

## Invariants

1. Default east-west decision is deny.
2. Default egress decision is deny.
3. Management, control-plane, verifier, monitoring, and external trust zones are explicit.
4. Protected machine-to-machine flows require encrypted transport and approved workload identity.
5. An unlisted port, zone pair, workload identity, or egress destination is denied.
6. Denied flows, identity mismatch, unauthorized egress, and scan indicators are detection events.
7. Firewall material is generated deterministically from policy.
8. Validation never changes the host firewall automatically.
9. Node1 owns policy-generation authority and the M25 signing private key.
10. Node2 receives verifier-only material and no private key.

## Controls

| Control | Purpose |
|---|---|
| `ENT-NET-001` | authoritative network zones and trust boundaries |
| `ENT-NET-002` | default-deny east-west micro-segmentation |
| `ENT-NET-003` | mTLS workload identity binding |
| `ENT-NET-004` | default-deny egress allowlisting |
| `ENT-NET-005` | management/verifier-zone isolation |
| `ENT-NET-006` | network anomaly/detection policy |
| `ENT-NET-007` | deterministic firewall rendering and negative-path evidence |

## Architecture

```text
Management zone
      |
      | encrypted admin path
      v
+-------------------+
| Node1 control     |
| plane / authority |
+-------------------+
      ^       |
      |       | telemetry only
mTLS  |       v
      |  Monitoring zone
+-------------------+
| Node2 verifier    |
+-------------------+

Everything not represented by an approved flow is denied by policy.
External egress is separately default-deny.
```

## Deployment boundary

`generated-nftables.conf` is evidence/reference material. M25 validation does not run `nft -f` and does not modify physical VLANs, switches, routers, cloud ACLs or host routing. A production deployment may apply equivalent rules only after an operator reviews the generated policy against the actual environment.

## Claim boundary

M25 is an engineering evidence/control milestone. It does not assert CISSP certification, ISO/IEC 27001 certification, ISO/IEC 42001 certification or CRA conformity.
