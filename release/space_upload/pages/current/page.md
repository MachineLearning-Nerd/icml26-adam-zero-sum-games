# Current claim-by-claim verification

This page is the canonical evaluator entrypoint for arXiv 2605.19392,
*Understanding Dynamics of Adam in Zero-Sum Games: An ODE Approach*. It
supersedes the old inline verifier at judged Space revision
`2e0e908df273cf1cbba8a5455926f06d5f411808`. That old page remains reachable,
unchanged, and is labeled **[Historical rejected baseline](../overview/page.md)**.
The historical [index page](../index.md) is also preserved.

> **Audit status:** Claims 1–4 and 6 are `VERIFIED_SCOPED`; Claim 5 is
> `BLOCKED_PROTOCOL`. The historical judge score is `6/12`; the current
> candidate has no judge score claim, no publication claim, and no author
> endorsement claim.

**Fixed command**

```bash
uv run --locked python repro/src/verify.py
```

**Pinned execution:** evidence Git SHA
`43327acebf41a3f13e73f2a57337e383eb87376c`; uv lock; Python 3.12.13;
NumPy 2.5.1; HF `cpu-upgrade`; estimated 8 cores; actual cgroup quota 8 vCPU;
1m30s job wall time; 26.288s verifier time. Claim 4's bootstrap seed is
`20260729`; other scientific checks use fixed initial states and no RNG.

[Main verifier](../../repro/src/verify.py) ·
[uv project](../../pyproject.toml) ·
[complete uv lock](../../uv.lock) ·
[tutorial notebook](../../notebooks/adam_zero_sum_reproduction.py) ·
[raw manifest](../../evidence/raw/output_manifest.json) ·
[provenance](../../evidence/provenance.md) ·
[release forecast report](release-report.md) ·
[first evaluator-blind review](../../evidence/red_team_prepublication_round1.json) ·
[final evaluator-blind review](../../evidence/red_team_prepublication_final.json)

Claim contracts:
[1](../../evidence/contracts/claim1.json) ·
[2](../../evidence/contracts/claim2.json) ·
[3](../../evidence/contracts/claim3.json) ·
[4](../../evidence/contracts/claim4.json) ·
[5](../../evidence/contracts/claim5.json) ·
[6](../../evidence/contracts/claim6.json).

## Claim 1 — VERIFIED

**Exact source contract.** Under Theorems 4.3–4.4's
interaction-dominated zero-sum setting, smaller first-order momentum beta
permits a broader stable Adam-DA step-size range. The tested quadratic has
game-Jacobian eigenvalues \(-1\pm3i\), so
\(|\operatorname{Im}\lambda|>|\operatorname{Re}\lambda|>0\).

The fixed-criterion boundary is strictly decreasing:

| beta | −0.3 | 0.0 | 0.3 | 0.6 | 0.9 |
|---:|---:|---:|---:|---:|---:|
| max stable h | 0.0771225 | 0.0520994 | 0.0306161 | 0.0148698 | 0.00290748 |

The [independent result-only checker](../../repro/src/check_claims123.py) recomputes
strict order from [raw JSON](../../evidence/raw/baseline_verdict.json). Its
reversed-observation control fails the contract as intended; checker exit is
zero only when both primary and control outcomes are correct.
[Checker output](../../evidence/raw/claims123_checker.json).

**Limitation:** numerical boundary evidence is scoped to the audited quadratic;
it is not presented as a universal proof over every loss.

## Claim 2 — VERIFIED

**Exact source contract.** Corollary 4.5 says the stable-step upper bound is
strictly decreasing in beta in \((-1,1)\), for both the continuous and discrete
forms, under the preceding assumptions.

Across beta
`[-0.49,-0.29143,-0.09286,0.10571,0.30429,0.50286,0.70143,0.9]`,
the continuous bound decreases
`[0.73039,0.45565,0.30118,0.20220,0.13335,0.08270,0.04387,0.01316]`;
the discrete bound decreases
`[0.33322,0.29583,0.23054,0.16755,0.11490,0.07263,0.03886,0.01169]`.

The same [result-only checker](../../repro/src/check_claims123.py) independently
tests every adjacent pair. A constant-array control is rejected for failing
strictness. Full arrays and checker inputs are in
[baseline_verdict.json](../../evidence/raw/baseline_verdict.json).

**Limitation:** the finite grid evaluates the closed forms; the source
corollary—not the grid alone—carries the universal calculus statement.

## Claim 3 — VERIFIED

**Exact source contract.** Corollary 4.6 states that Adam-DA fails to converge
on bilinear zero-sum games for every momentum and positive step-size choice.
For \(f(x,y)=xy\), both real eigenvalue parts are exactly zero, making the
paper's discrete stability upper bound exactly `0.0`. None of the 36
beta/rho/h corroborating configurations converged.

The independent checker validates the zero-bound certificate and rejects a
perturbed non-bilinear spectrum with real parts `−0.1` as its negative control.
[Raw result](../../evidence/raw/baseline_verdict.json) ·
[checker source](../../repro/src/check_claims123.py).

**Limitation:** the finite sweep is corroboration. The universal part is the
machine-checked zero-bound specialization of the source formula.

## Claim 4 — VERIFIED

**Exact source contract.** Section 5 claims that smaller beta and larger
second-order momentum rho move Adam-DA trajectories toward flatter regions,
measured by cumulative average
\(\|\nabla_x f\|_1+\|\nabla_y f\|_1\). The interaction-dominated quadratic
has cross/self Hessian ratio `3.0`. Tests use eight paired initial states,
horizons 3,000 and 10,000, beta
`[-0.3,0,0.3,0.6,0.9]`, and the paper's rho grid `[0.3,0.5,0.7,0.9]`.

At horizon 10,000, beta means strictly increase:
`[0.559897,0.560788,0.562454,0.566696,0.599793]`; rho means strictly
decrease: `[0.0288615,0.0276554,0.0255154,0.0223741]`. The paired extreme
contrasts have 99% bootstrap intervals `[0.03653,0.04315]` for beta and
`[0.005906,0.007340]` for rho. Every paired extreme difference has the expected
sign.

The interaction-free control (cross/self ratio `0`) reverses both expected
orders, so this is not a generic decay detector. The independent checker uses
seed `20260729` and sees only the
[432-row raw CSV](../../evidence/raw/claim4_flatness.csv).

[Verifier](../../repro/src/claim4_flatness.py) ·
[independent checker](../../repro/src/check_claim4.py) ·
[checker output](../../evidence/raw/claim4_checker.json).

**Limitation:** a wider exploratory sweep was nonmonotone above rho `0.9`; the
VERIFIED verdict is explicitly limited to the paper's published rho grid.

## Claim 5 — BLOCKED

**Exact source contract.** In the paper's ResNet and CNN improved-WGAN
experiments on CIFAR-10 and STL-10, smaller beta and larger rho empirically
tend to lower cumulative parameter-gradient AvgS, and lower AvgS tends to
coincide with higher Inception Score. This is a qualitative tendency across
the four named settings, not universal strict ordering of every adjacent pair.

Four materially different routes were required because confidence stayed LOW:

1. **Source completeness:** 13 critical fields are absent—exact architectures,
   code, data pipeline, latent design, update ratio, penalty, epsilon, seeds,
   horizon, IS protocol, raw traces, and per-seed scores.
2. **Reported-table audit:** beta/IS Spearman associations have the paper's
   direction in all four settings (`−0.75` to `−0.893`); every rho/IS table is
   strictly increasing. But Table 2's rho `0.9` values match beta `−0.3` in
   three settings (within `0.006` in the fourth), not the text's fixed beta `0`.
3. **CPU feasibility:** a full reported batch/resolution WGAN-GP shape profile
   projects `112.434` hours for 44 configurations at one seed and `337.303`
   hours at three seeds, excluding data input, IS, extra critic steps, and
   undisclosed-architecture uncertainty. Synthetic tensors were resource-only,
   never claim evidence.
4. **Mandatory falsification:** no candidate both satisfies the exact GAN
   domain and provides joint AvgS/IS evidence contradicting the qualitative
   tendency. The reported beta `−0.5` versus `−0.3` IS pair does falsify a
   deliberately stronger universal monotonic control in all four settings,
   proving the checker is non-vacuous. It does not falsify the paper's actual
   wording.

[Route 1 raw/checker](../../evidence/raw/claim5_route1_source_audit.json) ·
[Route 2 raw/checker](../../evidence/raw/claim5_route2_table_audit.json) ·
[Route 3 raw/checker](../../evidence/raw/claim5_route3_cpu_profile.json) ·
[Route 4 raw](../../evidence/raw/claim5_route4_falsification.json) ·
[Route 4 checker](../../evidence/raw/claim5_route4_checker.json) ·
[all route source](../../repro/src/claim5_falsification.py).

**Unblockers:** author executable code and exact configurations; raw paired
AvgS/IS; resolved fixed beta for Table 2; and sufficient CPU budget for the
calibrated campaign. Missing data, ambiguity, and a non-GAN reversal are not
misreported as falsification.

## Claim 6 — VERIFIED

**Exact source contract.** Theorem 3.1 and Appendix C.1 claim one-step local
truncation error \(O(h^3)\) for the corrected modified ODE after a momentum
transient, on a fixed finite horizon with smooth derivatives through fourth
order, beta in \((-1,1)\), and rho in \((0,1)\).

The test loss is a finite sin/cos combination, so all derivatives are globally
bounded. Parameters are beta `0.2`, rho `0.5`, epsilon `0.1`; four initial
states and eight h values are aligned at physical time `0.2`. Every burn-in
count exceeds the paper threshold; minimum measured interaction ratio is
`3.1683`.

The corrected observed orders are `2.98305` and `3.00910` across the four
states (mean `2.99608`). The SignGDA flow without the O(h) modified-equation
correction has orders `1.99038` and `2.00080` (mean `1.99559`): it is accepted
as O(h²) and rejected as O(h³).

[32-row error CSV](../../evidence/raw/claim6_local_error.csv) ·
[verifier](../../repro/src/claim6_local_error.py) ·
[result-only checker](../../repro/src/check_claim6.py) ·
[checker output](../../evidence/raw/claim6_checker.json).

**Limitation:** this is direct numerical verification under an
assumption-satisfying smooth game, not a proof for every admissible loss.

## Evaluator visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | this page §1 | yes | yes | [JSON](../../evidence/raw/baseline_verdict.json) | [output](../../evidence/raw/claims123_checker.json) | reversed observations | Theorems 4.3–4.4 scoped boundary | VERIFIED |
| 2 | this page §2 | yes | yes | [JSON](../../evidence/raw/baseline_verdict.json) | [output](../../evidence/raw/claims123_checker.json) | constant array | Corollary 4.5 both bounds | VERIFIED |
| 3 | this page §3 | yes | yes | [JSON](../../evidence/raw/baseline_verdict.json) | [output](../../evidence/raw/claims123_checker.json) | perturbed spectrum | Corollary 4.6 zero-bound certificate | VERIFIED |
| 4 | this page §4 | yes | yes | [CSV](../../evidence/raw/claim4_flatness.csv) | [output](../../evidence/raw/claim4_checker.json) | interaction-free game | Section 5 beta and rho AvgS | VERIFIED |
| 5 | this page §5 | yes | yes | [route 4](../../evidence/raw/claim5_route4_falsification.json) | [output](../../evidence/raw/claim5_route4_checker.json) | stronger universal claim | named GAN tendency | BLOCKED |
| 6 | this page §6 | yes | yes | [CSV](../../evidence/raw/claim6_local_error.csv) | [output](../../evidence/raw/claim6_checker.json) | O(h²) SignGDA flow | Theorem 3.1 O(h³) local error | VERIFIED |

Every raw file is covered by
[output_manifest.json](../../evidence/raw/output_manifest.json). The current
verifier exits nonzero if an accepted claim, independent checker, or expected
negative control fails.

## Forecast, not a judge result

Previous live judged score: **6/12**. Conservative projected range:
**8–10/12**. Best-supported possible score: **10/12**. Claims 4 and 6 changed
from INCONCLUSIVE to VERIFIED in this candidate; Claim 5 remains BLOCKED. Only
the live evaluator can change the score.
