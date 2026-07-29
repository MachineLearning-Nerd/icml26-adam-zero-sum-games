# Claim 6 method

The test uses the exact simultaneous, bias-corrected Adam-DA update and the
paper's Continuous Adam-DA vector field. The loss

`f(x,y) = 0.2(1-cos x) - 0.2(1-cos y) + sin(x)sin(y)`

has globally bounded derivatives of every order. For each of four initial
points and seven independently fixed step sizes, Adam-DA is warmed for 50
steps. This exceeds the paper's burn-in threshold for every tested step size.
The next Adam-DA iterate is compared with a 128-substep RK4 integration of the
continuous vector field over one interval of length `h`.

The primary measurement is the log-log slope of one-step error against `h`.
An independent script sees only the generated CSV and recomputes each slope.
The negative control removes the O(h) modified-equation correction, leaving
the paper's SignGDA-flow; it must scale as O(h^2) and fail the O(h^3) contract.

Exact fixed command:

`uv run --locked python repro/src/verify.py`

Determinism: no random sampling is used.
