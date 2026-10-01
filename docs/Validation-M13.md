# M13 Validation

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
./scripts/m13/validate_m13_local.sh
./scripts/m13/validate_m13_regression.sh
```

Required positive coverage includes Article 14(5)(a), Article 14(5)(b), NOT_SEVERE, INCOMPLETE, AEV and severe-incident clock families, awareness-journal integrity and M11/M12 digest bindings. Required negative validation includes tampered material rejection, private-key rejection on Node2, awareness-journal chain rejection and private-key-free verifier packaging.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.
