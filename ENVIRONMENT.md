# Environment and reproduction boundary

## Locked command

```bash
uv sync --locked
uv run --locked python repro/src/verify.py
```

The release uses Python `3.12.13`, NumPy `2.5.1`, the committed `uv.lock`, and
Hugging Face `cpu-upgrade`. The accepted run used an 8-vCPU cgroup quota, 26.288
seconds of verifier time, and no GPU.

## Accepted evidence

- C1–C3: the result-only checker recomputes the strict order, zero-bound
  certificate, and all expected negative controls.
- C4: 432 raw rows cover the published beta/rho grid, two accepted horizons,
  eight paired starts, bootstrap contrasts, and the interaction-free control.
- C6: 32 raw local-error rows compare corrected ODE and SignGDA at fixed
  physical time, with burn-in threshold checks.
- C5: four audit routes pass their own controls but intentionally finish
  `BLOCKED`; the CPU profile is resource evidence only.

## Runtime boundary

The fixed command regenerates the scientific evidence and is heavier than a
documentation check. `verify_final.py` validates the committed release
contract without launching it. No current judge rerun is claimed here.
