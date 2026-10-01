# M17 — CRA Annex-I Compliance Evidence

M17 aggregates traceable evidence for all 22 Annex I Part I and Part II requirement rows in the authoritative M11 matrix. It does **not** change the M11 legal/status baseline, perform a CRA conformity assessment, generate the Annex VII technical file, or claim CRA conformity.

## Outputs

- `annex-i-evidence-index.json`: requirement-to-evidence traceability with SHA-256 digests.
- `annex-i-coverage-summary.json`: Part I/Part II coverage and `EVIDENCED`/`PARTIAL`/`GAP` counts.
- `annex-i-evidence-gaps.json`: explicit unresolved evidence gaps.
- `m17-annex-i-manifest.json` + signature: digest-bound M11–M16 baseline and M17 artifacts.

## Boundaries

M17 is evidence aggregation only. M18 builds the Annex VII technical file; M19 performs production Node1/Node2 validation; conformity assessment remains a separate manufacturer/notified-body process as applicable.

## Known gaps intentionally retained

- Annex I Part I(2)(b): product-specific secure-by-default/reset evidence.
- Annex I Part I(2)(i): product-specific evidence that negative impact on other devices/networks is minimised.
- Annex I Part I(2)(m): product-specific secure/permanent data-removal and transfer evidence.
- Annex I Part II(3): existing tests are evidence, but M19 production validation is still required for regular product-security test/review closure.
