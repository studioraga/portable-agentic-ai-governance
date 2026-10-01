# M16 Prerequisites

- M15 release checked out as the Git baseline.
- Python 3.10+ and pytest.
- OpenSSL with Ed25519 support.
- M11-M15 baseline/control files present and unchanged.
- Node1 retains private signing material; Node2 must receive verifier-only M16 material.

## M17 — CRA Annex-I Compliance Evidence integration

M17 consumes the existing M3–M16 security, vulnerability, incident, reporting, PSIRT/CVD and secure-update evidence and binds it to all Annex I Part I/II requirement rows from the frozen M11 CRA matrix. M17 records `EVIDENCED`, `PARTIAL` and `GAP` states with SHA-256 evidence references; it does not mutate M11 requirement status, perform conformity assessment, generate the Annex VII technical file, or claim CRA conformity. See `docs/M17-CRA-Annex-I-Compliance-Evidence.md` and `docs/Validation-M17.md`.
