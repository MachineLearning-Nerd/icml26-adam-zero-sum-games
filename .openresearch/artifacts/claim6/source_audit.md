# Claim 6 source audit

- Source URL: `https://ar5iv.labs.arxiv.org/html/2605.19392`
- Retrieved with an explicit `OpenResearch-Reproduction/1.0` User-Agent on
  `2026-07-29T07:46:54Z`.
- HTML SHA-256:
  `c7ebf813dc871eba1c0c93542fcf0a7d599c7c4d44a543a0000270ce48ae7998`.
- TeX source URL: `https://export.arxiv.org/e-print/2605.19392`
- TeX archive SHA-256:
  `9922a66ab5708f357aa8be09f207565791a6488f48b0d8d2cf27011964521265`.

## Exact anchors and quantifiers

- Theorem 3.1, HTML anchor `#S3.Thmthm1`.
- Appendix C.1 (`Tex/Ap3.tex`), the lemma labelled
  `lemma: ODE for Sim-Adam`, and the lemma labelled
  `lemma: local error between ODEs`.
- Assumption: the loss is smooth with derivatives bounded through fourth
  order.
- Domain: `beta in (-1,1)`, `rho in (0,1)`, `epsilon > 0`, `h > 0`.
- Quantifier: any fixed finite time horizon.
- Burn-in: after
  `max{2 log(h)/log|beta|, 2 log(h)/log(rho)}` steps.
- Conclusion: one-step/local trajectory discrepancy is `O(h^3)`.

The paper explicitly contrasts this with SignGDA-flow, which has `O(h^2)`
local error. Stability-bound agreement is not the claimed quantity.
