# Audit status

**State:** Claims 1–4 and 6 have scoped numerical evidence with independent
controls. Claim 5 remains blocked as a paper-level GAN reproduction.

- Paper: [Understanding Dynamics of Adam in Zero-Sum Games: An ODE Approach](https://arxiv.org/abs/2605.19392)
- Authors: Yi Feng, Weiming Ou, and Xiao Wang
- ICML submission: `4MVVscCjYu`
- Repository: [MachineLearning-Nerd/icml26-adam-zero-sum-games](https://github.com/MachineLearning-Nerd/icml26-adam-zero-sum-games)
- Overall status: `PARTIAL_C1_C2_C3_C4_C6_VERIFIED_C5_BLOCKED_HISTORICAL_SCORE_6_OF_12_NO_CURRENT_SCORE`
- C1–C3: `VERIFIED_SCOPED` under the interaction-dominated and bilinear game contracts
- C4: `VERIFIED_SCOPED` on the published `rho <= 0.9` grid, paired initial states, two accepted horizons, and an interaction-free negative control
- C5: `BLOCKED_PROTOCOL` because 13 source fields are missing, Table 2 has a fixed-beta inconsistency, and the faithful three-seed CPU campaign is projected above 337 hours
- C6: `VERIFIED_SCOPED` by direct fixed-time corrected-ODE order measurement with an O(h²) SignGDA control
- Historical external score: `6/12`
- Current score claim: `false`
- Forecast: `8–10/12` only; not a judge result
- Publication allowed: `false`
- Official author endorsement: `false` / not claimed
- Commit identity: all reachable history uses `MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`
- Recovery bundle SHA-256: `3affb8220c1f9cbc1065c0f85639559c93136adfb466e3c9180ccd0f30f070b9`

The accepted results are finite or assumption-scoped numerical checks. They do
not replace the paper’s analytical proofs, and Claim 5’s source/table/resource
audit is not presented as GAN training evidence or falsification.
