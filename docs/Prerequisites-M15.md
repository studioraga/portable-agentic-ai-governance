# M15 Prerequisites

- Frozen M14 release and unchanged M11/M12/M13/M14 control baselines.
- Python 3.10+, OpenSSL and SHA-256 utilities.
- M14 reporting evidence available for synthetic AEV/severe-incident user-notification generation.
- External network dispatch is not required for acceptance.

## M16 integration — CRA Secure Update & Product Lifecycle
M16 consumes the existing milestone evidence without rewriting its historical responsibility. It adds support-period/lifecycle evidence, signed secure-update metadata and payload verification, anti-rollback decisions, update-retention/free-update policy checks, and end-of-support notification preparation. M16 keeps host OS/firmware modification and network rollout out of acceptance; see `docs/M16-CRA-Secure-Update-Product-Lifecycle.md`, `docs/Deployment-M16.md`, and `docs/Validation-M16.md`.
