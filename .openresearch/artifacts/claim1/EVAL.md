# Claim 1 evaluator contract

Run `uv run --locked python repro/src/verify.py`. Success requires a strictly
decreasing stable boundary and an independent checker exit code of zero. The
reversed-order control must be rejected.
