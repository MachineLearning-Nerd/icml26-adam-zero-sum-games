"""Numerical primitives for the frozen judged-baseline reconstruction.

The game is

    min_x max_y  (a/2) x^2 + c x y - (b/2) y^2,

so its GDA Jacobian is [[-a, -c], [c, -b]].
"""

from __future__ import annotations

import numpy as np


def make_game(a: float, b: float, c: float) -> dict[str, object]:
    jacobian = np.array([[-a, -c], [c, -b]], dtype=float)
    return {
        "a": float(a),
        "b": float(b),
        "c": float(c),
        "jacobian": jacobian,
        "lam": np.linalg.eigvals(jacobian),
    }


def gradf(state: tuple[float, float], game: dict[str, object]) -> tuple[float, float]:
    x, y = state
    a = float(game["a"])
    b = float(game["b"])
    c = float(game["c"])
    return a * x + c * y, c * x - b * y


def simulate(
    game: dict[str, object],
    x0: float,
    y0: float,
    beta: float,
    rho: float,
    eps: float,
    h: float,
    steps: int,
) -> np.ndarray:
    """Run the simultaneous, bias-corrected Adam-DA update from the paper."""
    x, y = float(x0), float(y0)
    mx = my = vx = vy = 0.0
    trajectory = np.empty((steps + 1, 2), dtype=float)
    trajectory[0] = (x, y)
    for n in range(1, steps + 1):
        gx, gy = gradf((x, y), game)
        mx = beta * mx + (1.0 - beta) * gx
        my = beta * my + (1.0 - beta) * gy
        vx = rho * vx + (1.0 - rho) * gx * gx
        vy = rho * vy + (1.0 - rho) * gy * gy
        m_bias = 1.0 - beta**n
        v_bias = 1.0 - rho**n
        x -= h * (mx / m_bias) / np.sqrt(vx / v_bias + eps)
        y += h * (my / m_bias) / np.sqrt(vy / v_bias + eps)
        trajectory[n] = (x, y)
        if not np.isfinite(x + y) or max(abs(x), abs(y)) > 1e8:
            trajectory[n:] = np.nan
            break
    return trajectory


def converges(
    game: dict[str, object],
    beta: float,
    rho: float,
    eps: float,
    h: float,
    T: int = 1500,
) -> bool:
    trajectory = simulate(game, 0.5, 0.5, beta, rho, eps, h, T)
    if not np.isfinite(trajectory).all():
        return False
    radius = np.linalg.norm(trajectory, axis=1)
    tail = radius[-max(100, T // 10) :]
    return bool(tail.mean() < 0.08 * radius[0] and tail[-1] < 0.1 * radius[0])


def bound_continuous(game: dict[str, object], beta: float, eps: float) -> float:
    """Theorem 4.3, minimized over interaction-dominated eigenvalues."""
    bounds: list[float] = []
    for lam in np.asarray(game["lam"]):
        re, im = abs(float(lam.real)), abs(float(lam.imag))
        if im > re and re > 0.0:
            bounds.append(2.0 * np.sqrt(eps) * (1.0 - beta) * re / ((1.0 + beta) * (im**2 - re**2)))
    return float(min(bounds)) if bounds else 0.0


def bound_discrete(game: dict[str, object], beta: float, eps: float) -> float:
    """Theorem 4.4, minimized over the full Jacobian spectrum."""
    bounds: list[float] = []
    for lam in np.asarray(game["lam"]):
        re, im = abs(float(lam.real)), abs(float(lam.imag))
        if re == 0.0:
            return 0.0
        denominator = (1.0 + beta**2) * abs(lam) ** 2 + 2.0 * beta * (im**2 - re**2)
        if denominator > 0.0:
            bounds.append(2.0 * np.sqrt(eps) * (1.0 - beta**2) * re / denominator)
    return float(min(bounds)) if bounds else 0.0
