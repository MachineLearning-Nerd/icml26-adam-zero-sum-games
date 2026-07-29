- Previous live judged score: `6/12`
- Conservative projected score range after the proposed change: `8–10/12`
- Best-supported possible new score: `10/12` — forecast only, not a judge result

# Release forecast and claim summary

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| 1 | 2 | 2 | HIGH | VERIFIED | Strict boundary order reruns; independent checker and reversed-order control pass. |
| 2 | 2 | 2 | HIGH | VERIFIED | Both source bound forms are strictly decreasing; constant-array control is rejected. |
| 3 | 2 | 2 | HIGH | VERIFIED | Purely imaginary spectrum yields an exact zero-bound certificate; sweep corroborates it. |
| 4 | 0 | 2 | HIGH | VERIFIED | Both beta and published rho directions pass at two horizons with paired 99% CIs; interaction-free control reverses them. Risk: verdict is scoped to rho ≤ 0.9. |
| 5 | 0 | 2 | LOW | BLOCKED | Four distinct routes completed. Exact author GAN experiment is under-specified and independently projected beyond 337 CPU hours for three seeds. No valid falsification was found. |
| 6 | 0 | 2 | HIGH | VERIFIED | Direct corrected local-error order is 2.996; SignGDA control is 1.996 and rejected as O(h³). |

Current total score: **6/12**. This candidate does not claim earned points
before the live judge. The conservative projected total is **8–10/12** and the
best-supported possible total is **10/12**.

Claims changed since the previous verdict: Claim 4 now directly covers the
missing rho component; Claim 6 now directly measures O(h³) local truncation
error against an O(h²) control. Claim 5 remains BLOCKED because the exact
ResNet/CNN CIFAR-10/STL-10 experiment is not uniquely specified, raw paired
AvgS/IS data are absent, Table 2's fixed beta is inconsistent, and the
calibrated faithful CPU campaign is outside the available practical window.

## Experiment tree

The frozen judged reconstruction is the root. Research descended through the
successful fixed-time Claim 6 node, the published-grid Claim 4 node, four
stacked Claim 5 routes, a cumulative evidence-emission node, and the final
release-gate child. Failed scientific boundary nodes remain frozen and are not
the current verifier.

Winning evidence branch:
`orx/cumulative-evaluator-visible-release-candidate`, evidence Git SHA
`43327acebf41a3f13e73f2a57337e383eb87376c`.

## Compute and command

Every formal node used exactly:

```bash
uv run --locked python repro/src/verify.py
```

The candidate evidence run used Hugging Face `cpu-upgrade`; estimate 8 cores,
actual cgroup quota 8 vCPU; wall time 1m30s; verifier time 26.288s. No GPU was
used. Earlier scientific runs used the same flavor and fixed command. The
pinned image was
`ghcr.io/astral-sh/uv:0.11.29-python3.12-trixie-slim`.

## Release action

After all gates pass, upload only the prepared text allowlist to the existing
Space `DineshAI/4MVVscCjYu` through the Hugging Face API. Do not create another
Space and do not delete historical files. Then download the exact published
revision, verify all hashes and canonical traversal, mark it awaiting judge,
and fast-forward the exact reader-facing text to GitHub `main`.
