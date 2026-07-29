# Claim 5 verification routes

## Route 1 — source completeness audit

Interpretation: the claim refers to the exact author experiment, not any nearby
GAN benchmark.

Method: reconstruct every disclosed setting from Section 5, Appendix D, and
Tables 1–2; independently check whether the source uniquely specifies an
executable experiment.

Status before execution: `PENDING`.

Success for this route means an honest, machine-checked `BLOCKED` result when
critical fields are absent. It does not count as scientific verification of the
GAN claim.

## Route 2 — reported-table consistency and association

Interpretation: before attempting a new training implementation, test whether
the paper's own numeric IS tables consistently support the claimed association.

Method: reconstruct every Table 1 and Table 2 mean, compute per-setting rank
association and strict monotonicity, and cross-check the shared rho=0.9
configuration against the text's claimed fixed beta.

Status before execution: `PENDING`.

Author-reported values remain author evidence. Even a consistent table cannot
be promoted to reproduction evidence.
