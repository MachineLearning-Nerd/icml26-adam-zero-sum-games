# Branch audit

This file records the transition from generated `orx/*` branch names to descriptive names. The old names are provenance references only; the live repository should expose the clean names.

## Branch map

| Historical branch | Clean branch | What it does | Evidence boundary |
| --- | --- | --- | --- |
| `orx/judged-6-of-12-baseline-reconstruction` | `historical/judged-baseline` | Preserves the previous judged 6/12 reconstruction and locked environment | Historical baseline; not the current cumulative verdict |
| `orx/claim-4-beta-rho-flatness-sweep` | `audit/c4-beta-rho-flatness` | Tests both momentum axes and the interaction-free control | Exploratory and control evidence leading to Claim 4 |
| `orx/claim-4-published-rho-grid-replication` | `audit/c4-published-rho-grid` | Replicates Claim 4 on the paper’s published rho grid | Scoped VERIFIED result; wider rho values are not covered |
| `orx/claim-5-route-1-source-completeness-audit` | `audit/c5-source-completeness` | Enumerates missing fields needed for a unique GAN reproduction | Correctly produces a BLOCKED reproducibility result |
| `orx/claim-5-route-2-reported-table-consistency` | `audit/c5-table-consistency` | Checks rank directions, monotonicity, and the fixed-beta table mismatch | Author-reported table evidence; not independent GAN training evidence |
| `orx/claim-5-route-3-cpu-feasibility-calibration` | `audit/c5-cpu-feasibility` | Profiles reported WGAN-GP shapes and estimates campaign cost | Resource calibration only; synthetic tensors are not GAN claim evidence |
| `orx/claim-5-route-4-mandatory-falsification` | `audit/c5-mandatory-falsification` | Tests candidate counterexamples against the exact qualitative quantifier and GAN domain | No valid falsification; Claim 5 remains BLOCKED |
| `orx/claim-6-direct-o-h3-local-error` | `audit/c6-direct-local-error` | Adds a direct local-error verifier for the corrected ODE | Scoped numerical route for Theorem 3.1 |
| `orx/claim-6-fixed-time-aligned-local-error` | `audit/c6-fixed-time-local-error` | Aligns all comparisons at one physical time and checks burn-in | VERIFIED numerical route with an O(h²) control |
| `orx/cumulative-evaluator-visible-release-candidate` | `release/cumulative-evidence` | Emits the complete raw evidence bundle and independent checker outputs | Evaluator-facing release candidate |
| `orx/final-publication-and-release-gates` | `release/final-publication-gates` | Packages claim contracts, manifests, and publication gates | Release packaging; no new scientific claim |
| `orx/warning-free-notebook-release-candidate` | `release/warning-free-notebook` | Keeps the reader-facing marimo notebook warning-free | Documentation/release quality route |

## Claim-to-branch map

- Claims 1–3 are rooted in `historical/judged-baseline` and the shared `repro/src/` checkers.
- Claim 4 is produced by the two `audit/c4-*` branches and their paired-grid/bootstrap controls.
- Claim 5 is deliberately split across four `audit/c5-*` routes because source ambiguity, table consistency, resource feasibility, and falsification answer different questions.
- Claim 6 is produced by the two `audit/c6-*` branches; the final check compares the corrected ODE directly with an O(h²) SignGDA control.
- The `release/*` branches package or validate evidence; they are not additional paper claims.

## Provenance rules

- `main` is the canonical branch for the implementation, current evidence, report, notebook, and documentation.
- Every clean branch must contain the same `README.md` and `branch-audit.md` documentation once published.
- Historical `orx/*` names may appear here as old-name provenance, but should not remain as live GitHub branch names or links.
- Pending, historical, and blocked routes must not be rewritten as final `VERIFIED` or `FALSIFIED` claims.
- Maintenance commits are authored and committed as `MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>`.

