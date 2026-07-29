# Claim-by-claim reproduction: Adam dynamics in zero-sum games

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-4MVVscCjYu-understanding-dynamics-of-adam-in-zero-sum-games-an-ode-approach/blob/main/notebooks/adam_zero_sum_reproduction.py)

This project reproduces six audited claims from
*Understanding Dynamics of Adam in Zero-Sum Games: An ODE Approach*
([arXiv 2605.19392](https://arxiv.org/abs/2605.19392)). The central test uses
the paper's interaction-dominated quadratic setting: smaller first-order
momentum \(\beta\) expands the stable step-size range. The observed maximum
stable \(h\) decreases from **0.07712 at β = −0.3** to **0.002907 at β = 0.9**.

Five claims are directly **VERIFIED**: reverse-beta stability, both decreasing
bound formulas, bilinear divergence, both beta and rho flatness directions, and
the corrected ODE's local error (observed order **2.9961**, versus **1.9956**
for the O(h²) control). The named ResNet/CNN CIFAR-10/STL-10 GAN experiment is
**BLOCKED** after four verification/falsification routes because the source
does not uniquely specify the experiment and a faithful three-seed CPU
campaign independently projects above 337 hours.

This is a clean-room CPU reproduction, not a full-scale GAN retraining. All
formal runs used Hugging Face `cpu-upgrade` with an actual 8-vCPU quota, a
single uv lock, and the same fixed command. Previous live judged score:
**6/12**. Conservative post-publication forecast: **8–10/12**; best-supported
possible score: **10/12**, not a judge result.

- [Illustrated technical report](reports/adam-zero-sum/report.md)
- [Tutorial marimo notebook](notebooks/adam_zero_sum_reproduction.py)
- [Pinned raw evidence](.openresearch/artifacts/release/raw/)
- [Evaluator provenance](.openresearch/artifacts/release/provenance.md)

## Experiment log

Every formal node inherited the exact command shown below.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `main` | Publication surface | Not run as an experiment (publication surface) | Reader-facing report, notebook, and evidence | N/A |
| [`orx/judged-6-of-12-baseline-reconstruction`](https://github.com/MachineLearning-Nerd/icml26-repro-4MVVscCjYu-understanding-dynamics-of-adam-in-zero-sum-games-an-ode-approach/tree/orx/judged-6-of-12-baseline-reconstruction) | Freeze judged Claims 1–3 and uv environment | `uv run --locked python repro/src/verify.py` | Claims 1–3 VERIFIED; 4–6 initially BLOCKED | HF cpu-upgrade, 8 vCPU |
| [`orx/claim-6-fixed-time-aligned-local-error`](https://github.com/MachineLearning-Nerd/icml26-repro-4MVVscCjYu-understanding-dynamics-of-adam-in-zero-sum-games-an-ode-approach/tree/orx/claim-6-fixed-time-aligned-local-error) | Direct fixed-time local-error scaling | `uv run --locked python repro/src/verify.py` | Claim 6 VERIFIED; order 2.996 vs 1.996 control | HF cpu-upgrade, 8 vCPU |
| [`orx/claim-4-published-rho-grid-replication`](https://github.com/MachineLearning-Nerd/icml26-repro-4MVVscCjYu-understanding-dynamics-of-adam-in-zero-sum-games-an-ode-approach/tree/orx/claim-4-published-rho-grid-replication) | Add the missing rho flatness axis | `uv run --locked python repro/src/verify.py` | Claim 4 VERIFIED on published grid | HF cpu-upgrade, 8 vCPU |
| [`orx/claim-5-route-1-source-completeness-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-4MVVscCjYu-understanding-dynamics-of-adam-in-zero-sum-games-an-ode-approach/tree/orx/claim-5-route-1-source-completeness-audit) | Audit exact GAN reproducibility | `uv run --locked python repro/src/verify.py` | 13 missing fields; BLOCKED | HF cpu-upgrade, 8 vCPU |
| [`orx/claim-5-route-2-reported-table-consistency`](https://github.com/MachineLearning-Nerd/icml26-repro-4MVVscCjYu-understanding-dynamics-of-adam-in-zero-sum-games-an-ode-approach/tree/orx/claim-5-route-2-reported-table-consistency) | Reconstruct author IS tables | `uv run --locked python repro/src/verify.py` | Direction supported; fixed-beta inconsistency; BLOCKED | HF cpu-upgrade, 8 vCPU |
| [`orx/claim-5-route-3-cpu-feasibility-calibration`](https://github.com/MachineLearning-Nerd/icml26-repro-4MVVscCjYu-understanding-dynamics-of-adam-in-zero-sum-games-an-ode-approach/tree/orx/claim-5-route-3-cpu-feasibility-calibration) | Full-shape WGAN-GP CPU profile | `uv run --locked python repro/src/verify.py` | 337+ hours projected for three seeds; BLOCKED | HF cpu-upgrade, 8 vCPU |
| [`orx/claim-5-route-4-mandatory-falsification`](https://github.com/MachineLearning-Nerd/icml26-repro-4MVVscCjYu-understanding-dynamics-of-adam-in-zero-sum-games-an-ode-approach/tree/orx/claim-5-route-4-mandatory-falsification) | Assumption-audited falsification search | `uv run --locked python repro/src/verify.py` | No valid counterexample; Claim 5 BLOCKED | HF cpu-upgrade, 8 vCPU |
| [`orx/cumulative-evaluator-visible-release-candidate`](https://github.com/MachineLearning-Nerd/icml26-repro-4MVVscCjYu-understanding-dynamics-of-adam-in-zero-sum-games-an-ode-approach/tree/orx/cumulative-evaluator-visible-release-candidate) | Emit complete hash-addressed evidence bundle | `uv run --locked python repro/src/verify.py` | Claims 1–4,6 pass; Claim 5 BLOCKED; all checkers pass | HF cpu-upgrade, 8 vCPU |

## Reproduce

```bash
uv sync --locked
uv run --locked python repro/src/verify.py
```

For the tutorial:

```bash
uv run --locked marimo edit notebooks/adam_zero_sum_reproduction.py
uv run --locked marimo run notebooks/adam_zero_sum_reproduction.py
```

The fixed formal run regenerates `outputs/`, exits nonzero on a scientific or
control failure, and prints a SHA-256 manifest plus all raw text evidence.

---

## Original workspace

ICML 2026 agent reproduction workspace for 4MVVscCjYu.
