# M13 Prerequisites

- M11 requirement matrix present and unchanged.
- M12 control mapping present and validated.
- Python 3.10+.
- OpenSSL/Ed25519 support used by existing repository signing primitives.
- `bash`, `tar`, `gzip`, `sha256sum`, `find`, `install`, `pytest`.
- Node1 retains signing authority; Node2 receives verifier-only material.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.
