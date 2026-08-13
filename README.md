# Understanding Dynamics of Adam in Zero-Sum Games

Independent reproduction audit for [“Understanding Dynamics of Adam in Zero-Sum Games: An ODE Approach”](https://arxiv.org/abs/2605.19392).

The repository is published as [`icml26-adam-zero-sum-games`](https://github.com/MachineLearning-Nerd/icml26-adam-zero-sum-games).

## What the paper does

The paper derives ordinary differential equations that approximate the discrete Adam descent-ascent (Adam-DA) method used in zero-sum games. It uses the ODE view to study two questions:

1. how first- and second-order momentum affect local stability and convergence; and
2. whether Adam-DA implicitly favors flatter regions in interaction-dominated games.

The paper’s central qualitative conclusion reverses the familiar minimization intuition: in the studied competitive setting, smaller first-order momentum β improves the stable step-size range, while smaller β and larger second-order momentum ρ are associated with lower cumulative gradient norms. The paper also reports GAN experiments across architectures and datasets.

This repository is a clean-room CPU reproduction and evidence audit. It does not contain an official author implementation, and it does not treat an under-specified or infeasible GAN experiment as reproduced evidence.

## Current claim ledger

Each status below records the evidence actually produced by this repository. A numerical **VERIFIED** result is scoped to the stated assumptions, finite grids, and controls; it is not a replacement for the paper’s analytical theorem.

| Claim | Paper statement | How the claim is produced | Evidence | Status |
| --- | --- | --- | --- | --- |
| 1 | Theorems 4.3–4.4: in an interaction-dominated game, smaller β permits a larger stable Adam-DA step size | Simulate the quadratic game with Jacobian eigenvalues −1±3i, locate the maximum stable step size across β = −0.3, 0, 0.3, 0.6, 0.9, and reject a reversed-order control | [`core.py`](repro/src/core.py), [`check_claims123.py`](repro/src/check_claims123.py), [`baseline_verdict.json`](reports/adam-zero-sum/raw/baseline_verdict.json) | **VERIFIED** |
| 2 | Corollary 4.5: both continuous and discrete stability bounds strictly decrease with β | Evaluate both closed-form bound arrays on an interior β grid and require every adjacent difference to be strictly negative; reject a constant-array control | [`verify.py`](repro/src/verify.py), [`claim1–3 EVAL contracts`](.openresearch/artifacts/claim2/EVAL.md) | **VERIFIED** |
| 3 | Corollary 4.6: bilinear zero-sum games have zero positive-step stability bound and fail to converge | Check the exact zero-bound certificate for f(x, y) = xy, corroborate it on 36 β/ρ/h configurations, and reject a perturbed-spectrum control | [`check_claims123.py`](repro/src/check_claims123.py), [`claim3 source audit`](.openresearch/artifacts/claim3/source_audit.md) | **VERIFIED** |
| 4 | Section 5 thesis: smaller β and larger ρ move Adam-DA toward lower cumulative gradient norms in interaction-dominated games | Run the published β and ρ grids at horizons 3,000 and 10,000 over eight paired initial states, compute paired 99% bootstrap intervals, and require an interaction-free control to reject the ordering | [`claim4_flatness.py`](repro/src/claim4_flatness.py), [`claim4_flatness.csv`](reports/adam-zero-sum/raw/claim4_flatness.csv), [`claim4 EVAL`](.openresearch/artifacts/claim4/EVAL.md) | **VERIFIED on the published grid** |
| 5 | GAN experiments: lower cumulative parameter-gradient AvgS tends to coincide with higher Inception Score across four named settings | Audit source completeness, check the paper’s reported tables, profile the reported WGAN-GP shapes, and run an assumption-audited falsification route; do not substitute toy tensors for GAN evidence | [`claim5 routes`](.openresearch/artifacts/claim5/routes.md), [`claim5 source audit`](.openresearch/artifacts/claim5/source_audit.md), [`claim5 route evidence`](reports/adam-zero-sum/raw/) | **BLOCKED** |
| 6 | Theorem 3.1 / Appendix C.1: the corrected modified ODE has O(h³) local error after the momentum transient | Compare fixed-time trajectories for four smooth initial states and eight step sizes against an RK4 reference; require corrected-ODE slopes near 3, reject the O(h²) SignGDA control, and check the burn-in threshold | [`claim6_local_error.py`](repro/src/claim6_local_error.py), [`claim6_local_error.csv`](reports/adam-zero-sum/raw/claim6_local_error.csv), [`claim6 EVAL`](.openresearch/artifacts/claim6/EVAL.md) | **VERIFIED, scoped numerical check** |

The paper-level GAN claim remains unresolved for concrete reasons: 13 critical experimental fields are missing from the source, one reported fixed-β table is inconsistent with the text, and a faithful three-seed CPU campaign was projected above 337 hours before data loading or Inception Score evaluation. Those are reproducibility blockers, not a falsification of the paper.

## Reproduce the audit

The project uses Python 3.12 with a locked [uv](https://docs.astral.sh/uv/) environment.

```bash
uv sync --locked
uv run --locked python repro/src/verify.py
```

The fixed command regenerates the claim outputs, raw CSV/JSON evidence, SHA-256 manifest, and independent checker results. It exits nonzero when a claim contract, expected negative control, or release check fails. Formal runs used Hugging Face `cpu-upgrade` with an 8-vCPU quota.

For the interactive tutorial:

```bash
uv run --locked marimo edit notebooks/adam_zero_sum_reproduction.py
uv run --locked marimo run notebooks/adam_zero_sum_reproduction.py
```

## Repository contents

| Path | Purpose |
| --- | --- |
| [`repro/src/`](repro/src/) | The quadratic Adam-DA core, claim verifiers, independent checkers, source audits, and release checks |
| [`reports/adam-zero-sum/`](reports/adam-zero-sum/) | Reader-facing technical report, figures, raw results, and release forecast |
| [`.openresearch/artifacts/`](.openresearch/artifacts/) | Claim contracts, exact source anchors, limitations, evaluation notes, and route definitions |
| [`release/space_upload/`](release/space_upload/) | Hash-addressed evaluator-facing package and current claim-by-claim page |
| [`notebooks/`](notebooks/) | Reproducible marimo tutorial |
| [`pyproject.toml`](pyproject.toml) / [`uv.lock`](uv.lock) | Pinned runtime and dependency definition |

## Branch organization

The original branches were generated under `orx/*`. They are being renamed to make each evidence route self-describing. The complete old-to-new mapping and provenance policy are in [`branch-audit.md`](branch-audit.md).

| Branch | Role |
| --- | --- |
| `main` | Canonical implementation, current evidence bundle, report, notebook, and documentation |
| `historical/judged-baseline` | Frozen reconstruction of the previous 6/12 judged baseline |
| `audit/c4-beta-rho-flatness` | Initial beta/rho flatness exploration and control analysis |
| `audit/c4-published-rho-grid` | Replication on the paper’s published rho grid |
| `audit/c5-source-completeness` | Audit of missing fields in the exact GAN experiment |
| `audit/c5-table-consistency` | Consistency and rank-direction checks for reported Inception Score tables |
| `audit/c5-cpu-feasibility` | Full-shape WGAN-GP CPU timing and campaign-cost calibration |
| `audit/c5-mandatory-falsification` | Assumption-audited falsification search for the GAN claim |
| `audit/c6-direct-local-error` | Direct corrected-ODE local-error measurement |
| `audit/c6-fixed-time-local-error` | Fixed-physical-time alignment and O(h³) versus O(h²) control |
| `release/cumulative-evidence` | Hash-addressed cumulative evaluator bundle |
| `release/final-publication-gates` | Final release packaging and gate checks |
| `release/warning-free-notebook` | Warning-free reader-facing notebook release |

Branch names describe the experiment or release surface; they do not imply that every branch contains a completed paper-level claim.

## Paper metadata

- **Title:** Understanding Dynamics of Adam in Zero-Sum Games: An ODE Approach
- **Authors:** Yi Feng, Weiming Ou, and Xiao Wang
- **Paper:** [arXiv:2605.19392](https://arxiv.org/abs/2605.19392)
- **Source version audited here:** arXiv v1, retrieved and hashed in the claim source-audit files
- **Current collection:** ICML 2026 reproduction audit

### Citation

```bibtex
@misc{feng2026understanding,
  title         = {Understanding Dynamics of Adam in Zero-Sum Games: An ODE Approach},
  author        = {Feng, Yi and Ou, Weiming and Wang, Xiao},
  year          = {2026},
  eprint        = {2605.19392},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG}
}
```

## Thank you to the authors

Thank you to Yi Feng, Weiming Ou, and Xiao Wang for developing the ODE analysis of Adam-DA, making the paper’s assumptions and predictions available for independent study, and sharing a result that can be examined claim by claim. This repository is a documentation and reproduction companion, with respect for the authors’ original work and attribution.

## Maintenance attribution

Repository documentation, branch naming, audit notes, and maintenance commits in this collection are attributed to **MachineLearning-Nerd**. Scientific authorship and ownership of the paper’s ideas remain with the paper authors.
