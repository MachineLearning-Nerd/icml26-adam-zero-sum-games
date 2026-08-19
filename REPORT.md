# Audit report

## Executive result

Claims 1–4 and 6 have scoped numerical evidence with independent controls.
Claim 5 remains blocked as a paper-level GAN reproduction because the source
does not uniquely determine the experiment, one reported table is internally
inconsistent, and a faithful three-seed campaign is outside the calibrated CPU
window.

Overall status:

`PARTIAL_C1_C2_C3_C4_C6_VERIFIED_C5_BLOCKED_HISTORICAL_SCORE_6_OF_12_NO_CURRENT_SCORE`

## Claim matrix

| Claim | Result | Main boundary |
| --- | --- | --- |
| C1 | `VERIFIED_SCOPED` | Finite quadratic stability boundary under the interaction-dominated contract. |
| C2 | `VERIFIED_SCOPED` | Eight-point evaluation of source closed forms; calculus proof remains in the paper. |
| C3 | `VERIFIED_SCOPED` | Bilinear zero-bound specialization plus finite corroborating sweep. |
| C4 | `VERIFIED_SCOPED` | Published rho grid only; wider exploratory rho values are nonmonotone. |
| C5 | `BLOCKED_PROTOCOL` | Missing fields, fixed-beta table mismatch, no raw joint AvgS/IS, and 337+ CPU-hour projection. |
| C6 | `VERIFIED_SCOPED` | Four smooth initial states, fixed physical time, corrected O(h³) versus O(h²) control. |

## Quantitative evidence

- C1 maximum stable step sizes decrease from `0.0771225` at beta `−0.3` to `0.00290748` at beta `0.9`.
- C2 continuous and discrete bound arrays are strictly decreasing across all eight tested interior beta values.
- C3 the bilinear discrete bound is exactly `0.0`; none of 36 corroborating configurations converged.
- C4 at horizon 10,000, beta means rise `0.559897→0.599793`, rho means fall `0.0288615→0.0223741`, and both paired 99% intervals exclude zero.
- C6 corrected order mean is `2.99608` (range `2.98305–3.00910`); SignGDA control mean is `1.99559`.
- C5 reports 13 missing critical fields and a projected 337.303 hours for three seeds before data loading or Inception Score evaluation.

## Score and publication boundary

- Historical live score: `6/12`
- Current score claim: `false`
- Forecast: `8–10/12`, forecast only
- Publication allowed: `false`
- Official author endorsement: `false` / not claimed

Use [`CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md) for production paths and
[`SOURCE_AUDIT.md`](SOURCE_AUDIT.md) for source/version scope.
