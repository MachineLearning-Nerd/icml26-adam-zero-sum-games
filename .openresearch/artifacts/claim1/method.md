# Claim 1 method

The fixed verifier runs simultaneous bias-corrected Adam-DA from the same
initial state and binary-searches the largest accepted step size for five beta
values. The convergence predicate and every other parameter are frozen.

Raw results are in `../release/raw/baseline_verdict.json`. The independent
result-only checker is `repro/src/check_claims123.py`; its output is generated
by the final cumulative run. Its negative control reverses the observations and
must fail the decreasing-order contract.
