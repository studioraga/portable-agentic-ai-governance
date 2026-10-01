# M16 Deployment

Node1 builds signed M16 lifecycle/update material with `deploy/m16/one_shot_node1.sh`, validates it, and creates a private-key-free verifier archive using `deploy/m16/package_verifier_material.sh`.

Node2 verifies the archive checksum, confirms that no private key is present, then runs `deploy/m16/one_shot_node2.sh <m16-material>` and `scripts/m16/verify_node2.sh`.

M16 deployment does not update the operating system or flash device firmware; its update payload is a synthetic acceptance artifact used to prove signing, digest, policy and anti-rollback controls.

## M17 — CRA Annex-I Compliance Evidence integration

M17 consumes the existing M3–M16 security, vulnerability, incident, reporting, PSIRT/CVD and secure-update evidence and binds it to all Annex I Part I/II requirement rows from the frozen M11 CRA matrix. M17 records `EVIDENCED`, `PARTIAL` and `GAP` states with SHA-256 evidence references; it does not mutate M11 requirement status, perform conformity assessment, generate the Annex VII technical file, or claim CRA conformity. See `docs/M17-CRA-Annex-I-Compliance-Evidence.md` and `docs/Validation-M17.md`.
