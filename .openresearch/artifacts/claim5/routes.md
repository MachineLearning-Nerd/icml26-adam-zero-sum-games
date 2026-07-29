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

## Route 3 — full-shape CPU feasibility calibration

Interpretation: a faithful verification requires the reported batch size,
image resolutions, architecture families, WGAN-GP backward pass, parameter
gradient statistic, 16,000-step horizon visible in the published plots, and 44
momentum/setting combinations.

Method: profile batch-64 CNN and ResNet WGAN-GP joint updates at 32×32 and
64×64 on HF cpu-upgrade, including the parameter-gradient L1 statistic.
Forward-only evaluation is the negative control. Independently project the
lower-bound one- and three-seed campaign time.

Synthetic batches are used only for resource calibration. They are not CIFAR
or STL evidence, and this route cannot verify the scientific claim.

Status before execution: `PENDING`.

## Route 4 — mandatory falsification

Exact interpretation: this is a qualitative empirical tendency across the four
named GAN settings, not a universal strict ordering for every adjacent
momentum pair or every seed.

Method: test four candidate counterexamples against every domain assumption and
the exact tendency quantifier: the beta=-0.5 versus -0.3 IS reversal; the Table
2 fixed-beta mismatch; the quadratic rho>0.9 reversal; and the synthetic CPU
profile. An independent checker rejects metadata ambiguity, missing joint
AvgS/IS evidence, and non-GAN examples as invalid falsifications.

Negative control: the reported beta pair does falsify a deliberately stronger
universal strict-monotonic claim. This proves the route can recognize a genuine
contradiction while refusing to substitute that stronger quantifier for the
paper's wording.

Status before execution: `PENDING`.
