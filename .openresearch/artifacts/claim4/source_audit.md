# Claim 4 source audit

Source: ar5iv HTML for arXiv 2605.19392, retrieved with an explicit browser
User-Agent on 2026-07-29. SHA-256:
`c7ebf813dc871eba1c0c93542fcf0a7d599c7c4d44a543a0000270ce48ae7998`.

Anchor: Section 5, “Implicit Gradient Regularization,” underlined Thesis and
the subsequent definition of `AvgS`.

The paper calls this statement a thesis rather than a theorem. Its stated
scope is an interaction-dominated zero-sum game, assessed by cross-player
Hessian terms dominating self-Hessian terms or equivalently Jacobian
eigenvalues with large imaginary parts. “Flatter” means lower
`||grad_x f||_1 + ||grad_y f||_1`; the experimental quantity is the cumulative
average of this sum. The beta comparison fixes rho at 0.9. The rho comparison
fixes beta at 0. The direction is smaller beta and larger rho.

This verifier therefore provides scoped, direct corroboration; it does not
turn the paper's empirical thesis into a universal theorem.
