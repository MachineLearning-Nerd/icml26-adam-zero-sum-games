# Claim 4 method

The primary game is the same interaction-dominated quadratic used for the
accepted stability evidence:

`f(x,y) = x^2/2 + 3xy - y^2/2`.

Its cross/self Hessian ratio is 3 and its Adam-DA/GDA Jacobian eigenvalues are
`-1 ± 3i`. The code implements simultaneous bias-corrected Adam-DA and
computes the paper's exact cumulative `AvgS` metric.

The beta and rho axes use the fixed values named in the source. Eight paired
starts and two predeclared late horizons prevent a single trajectory or
selected checkpoint from deciding the result. A result-only checker recomputes
strict orderings, paired extreme contrasts, and fixed-seed 99% bootstrap
intervals from CSV alone.

The interaction-free game `f(x,y)=x^2/2-y^2/2` is the negative control. It
retains the zero-sum form and self-curvature but violates the thesis's
interaction-dominance assumption; at least one reversed-momentum ordering must
disappear.

Exact fixed command:

`uv run --locked python repro/src/verify.py`
