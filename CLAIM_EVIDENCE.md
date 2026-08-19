# Claim-to-evidence ledger

The six claim rows below separate the paper statement, the production path,
the controls, and the boundary of the accepted result.

| Claim | Paper anchor | How the result is produced | Evidence and controls | Status |
| --- | --- | --- | --- | --- |
| C1 — reverse-beta stability | Theorems 4.3–4.4 | Simulate the quadratic interaction-dominated game with eigenvalues `−1±3i`, locate the maximum stable step size over five beta values, and reject a reversed-order observation. | `repro/src/core.py`, `repro/src/check_claims123.py`, `reports/adam-zero-sum/raw/baseline_verdict.json`, and `claims123_checker.json`. | **VERIFIED_SCOPED** |
| C2 — decreasing continuous/discrete bounds | Corollary 4.5 | Evaluate both closed-form bound arrays on eight interior beta values and require every adjacent difference to be strictly negative. | `repro/src/verify.py`, `repro/src/check_claims123.py`, and the constant-array negative control. | **VERIFIED_SCOPED** |
| C3 — bilinear non-convergence | Corollary 4.6 | Check the exact zero positive-step bound for `f(x,y)=xy`, corroborate 36 beta/rho/step configurations, and reject a perturbed-spectrum control. | `repro/src/check_claims123.py`, `reports/adam-zero-sum/raw/baseline_verdict.json`, and `claims123_checker.json`. | **VERIFIED_SCOPED** |
| C4 — beta/rho flatness thesis | Section 5, “Implicit Gradient Regularization” | Run the published beta and rho grids at horizons 3,000 and 10,000 over eight paired initial states, calculate paired 99% bootstrap intervals, and require an interaction-free control to reverse the ordering. | `repro/src/claim4_flatness.py`, `repro/src/check_claim4.py`, `reports/adam-zero-sum/raw/claim4_flatness.csv`, and `claim4_checker.json`. | **VERIFIED_SCOPED** |
| C5 — GAN AvgS/Inception tendency | Section 5, ResNet/CNN improved-WGAN experiments | Audit source completeness, reported table directions/consistency, full-shape CPU feasibility, and an assumption-audited falsification route; do not substitute synthetic tensors for GAN evidence. | `repro/src/claim5_source_audit.py`, `claim5_table_audit.py`, `claim5_cpu_profile.py`, `claim5_falsification.py`, four route checkers, and `reports/adam-zero-sum/raw/`. | **BLOCKED_PROTOCOL** |
| C6 — corrected O(h³) local error | Theorem 3.1 and Appendix C.1 | Compare corrected-ODE trajectories with an RK4 reference at fixed physical time for four initial states and eight step sizes; compare against the uncorrected SignGDA flow. | `repro/src/claim6_local_error.py`, `repro/src/check_claim6.py`, `claim6_local_error.csv`, and `claim6_checker.json`. | **VERIFIED_SCOPED** |

## Claim 5 blocker record

The four completed routes answer different questions: what the source omits,
whether the reported tables are internally consistent, whether a faithful run
fits the available CPU budget, and whether an assumption-satisfying
counterexample exists. They do not produce the missing joint per-run AvgS and
Inception Score traces. The paper’s qualitative “tend” wording is therefore
blocked, not falsified.

## Evidence boundaries

1. The arXiv HTML source and TeX archive are pinned in [`SOURCE_AUDIT.md`](SOURCE_AUDIT.md).
2. Claims 1–4 and 6 are finite numerical corroborations under explicit
   contracts; they do not replace universal proofs.
3. The 6/12 value is the historical live judge result. The 8–10 value is a
   forecast in the inherited report and is not a current score.

The full path inventory is [`EVIDENCE_MANIFEST.json`](EVIDENCE_MANIFEST.json).
