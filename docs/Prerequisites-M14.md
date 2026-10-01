# Prerequisites — M14

- M11, M12 and M13 baselines must be present and unchanged.
- Python >= 3.10, OpenSSL, `sha256sum`, `tar`, `install`, `find`, and pytest.
- Node1 is the reporting-evidence authority; Node2 is verifier-only.
- M13 cases must contain manufacturer-awareness and deadline anchors.
- Manufacturer/product/Assigned Representative reporting metadata must be available.
- No live SRP API dependency is permitted for M14 acceptance.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.
