"""Direct numerical check of Theorem 3.1's one-step local-error order."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np


ALPHA = 0.2
BETA = 0.2
RHO = 0.5
EPS = 0.1
BURN_IN_STEPS = 50
H_VALUES = np.array([0.02, 0.014, 0.01, 0.007, 0.005, 0.0035, 0.0025])
INITIAL_POINTS = ((0.40, 0.30), (-0.35, 0.25), (0.30, -0.40), (-0.25, -0.35))


def derivatives(z: np.ndarray) -> tuple[float, float, float, float, float]:
    """Gradient and Hessian of a globally smooth, bounded-derivative game.

    f(x,y) = alpha(1-cos x) - alpha(1-cos y) + sin(x)sin(y).
    Every derivative of every order is bounded.
    """
    x, y = map(float, z)
    gx = ALPHA * math.sin(x) + math.cos(x) * math.sin(y)
    gy = -ALPHA * math.sin(y) + math.sin(x) * math.cos(y)
    fxx = ALPHA * math.cos(x) - math.sin(x) * math.sin(y)
    fyy = -ALPHA * math.cos(y) - math.sin(x) * math.sin(y)
    fxy = math.cos(x) * math.cos(y)
    return gx, gy, fxx, fyy, fxy


def adam_step(
    z: np.ndarray,
    moments: np.ndarray,
    step_index: int,
    h: float,
) -> tuple[np.ndarray, np.ndarray]:
    gx, gy, *_ = derivatives(z)
    mx, my, vx, vy = map(float, moments)
    mx = BETA * mx + (1.0 - BETA) * gx
    my = BETA * my + (1.0 - BETA) * gy
    vx = RHO * vx + (1.0 - RHO) * gx * gx
    vy = RHO * vy + (1.0 - RHO) * gy * gy
    m_bias = 1.0 - BETA**step_index
    v_bias = 1.0 - RHO**step_index
    updated = np.array(
        [
            z[0] - h * (mx / m_bias) / math.sqrt(vx / v_bias + EPS),
            z[1] + h * (my / m_bias) / math.sqrt(vy / v_bias + EPS),
        ]
    )
    return updated, np.array([mx, my, vx, vy])


def warm_state(initial: tuple[float, float], h: float) -> tuple[np.ndarray, np.ndarray]:
    z = np.asarray(initial, dtype=float)
    moments = np.zeros(4)
    for step_index in range(1, BURN_IN_STEPS + 1):
        z, moments = adam_step(z, moments, step_index, h)
    return z, moments


def continuous_vector(z: np.ndarray, h: float, corrected: bool) -> np.ndarray:
    gx, gy, fxx, fyy, fxy = derivatives(z)
    dx = math.sqrt(gx * gx + EPS)
    dy = math.sqrt(gy * gy + EPS)
    base = np.array([-gx / dx, gy / dy])
    if not corrected:
        return base

    dnorm_difference_dx = (gx / dx) * fxx - (gy / dy) * fxy
    dnorm_difference_dy = (gx / dx) * fxy - (gy / dy) * fyy
    kappa = (1.0 + BETA) / (1.0 - BETA) - (1.0 + RHO) / (1.0 - RHO)
    m_x = kappa + EPS * (1.0 + RHO) / (1.0 - RHO) / (gx * gx + EPS)
    m_y = kappa + EPS * (1.0 + RHO) / (1.0 - RHO) / (gy * gy + EPS)
    return np.array(
        [
            -(gx + 0.5 * h * m_x * dnorm_difference_dx) / dx,
            (gy + 0.5 * h * m_y * dnorm_difference_dy) / dy,
        ]
    )


def integrate_rk4(z0: np.ndarray, h: float, corrected: bool) -> np.ndarray:
    # A fixed 128-substep reference makes RK4 error negligible relative to h^3.
    substeps = 128
    dt = h / substeps
    z = z0.copy()
    for _ in range(substeps):
        k1 = continuous_vector(z, h, corrected)
        k2 = continuous_vector(z + 0.5 * dt * k1, h, corrected)
        k3 = continuous_vector(z + 0.5 * dt * k2, h, corrected)
        k4 = continuous_vector(z + dt * k3, h, corrected)
        z += dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
    return z


def observed_order(h_values: np.ndarray, errors: np.ndarray) -> float:
    return float(np.polyfit(np.log(h_values), np.log(errors), 1)[0])


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    per_initial: list[dict[str, object]] = []

    max_threshold = 0.0
    for h in H_VALUES:
        threshold = max(2.0 * math.log(h) / math.log(abs(BETA)), 2.0 * math.log(h) / math.log(RHO))
        max_threshold = max(max_threshold, threshold)

    for initial_id, initial in enumerate(INITIAL_POINTS):
        corrected_errors: list[float] = []
        control_errors: list[float] = []
        for h in H_VALUES:
            z, moments = warm_state(initial, float(h))
            discrete_next, _ = adam_step(z, moments, BURN_IN_STEPS + 1, float(h))
            corrected_next = integrate_rk4(z, float(h), corrected=True)
            control_next = integrate_rk4(z, float(h), corrected=False)
            corrected_error = float(np.linalg.norm(discrete_next - corrected_next))
            control_error = float(np.linalg.norm(discrete_next - control_next))
            gx, gy, fxx, fyy, fxy = derivatives(z)
            interaction_ratio = abs(fxy) / max(abs(fxx), abs(fyy), 1e-15)
            corrected_errors.append(corrected_error)
            control_errors.append(control_error)
            rows.append(
                {
                    "initial_id": initial_id,
                    "x0": initial[0],
                    "y0": initial[1],
                    "h": float(h),
                    "burn_in_steps": BURN_IN_STEPS,
                    "corrected_error": corrected_error,
                    "signgda_control_error": control_error,
                    "corrected_error_over_h3": corrected_error / float(h) ** 3,
                    "control_error_over_h2": control_error / float(h) ** 2,
                    "interaction_ratio": interaction_ratio,
                    "gradient_l1": abs(gx) + abs(gy),
                }
            )
        per_initial.append(
            {
                "initial_id": initial_id,
                "initial": list(initial),
                "corrected_order": observed_order(H_VALUES, np.asarray(corrected_errors)),
                "control_order": observed_order(H_VALUES, np.asarray(control_errors)),
                "corrected_errors": corrected_errors,
                "control_errors": control_errors,
            }
        )

    csv_path = output_dir / "claim6_local_error.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    corrected_orders = np.array([item["corrected_order"] for item in per_initial], dtype=float)
    control_orders = np.array([item["control_order"] for item in per_initial], dtype=float)
    interaction_ratios = np.array([row["interaction_ratio"] for row in rows], dtype=float)
    payload = {
        "claim": 6,
        "paper_anchor": "Theorem 3.1; Appendix C.1, Lemma C.4 and local-error lemma",
        "parameters": {
            "alpha": ALPHA,
            "beta": BETA,
            "rho": RHO,
            "epsilon": EPS,
            "burn_in_steps": BURN_IN_STEPS,
            "paper_max_burn_in_threshold": max_threshold,
            "h_values": H_VALUES.tolist(),
            "initial_points": [list(point) for point in INITIAL_POINTS],
            "rk4_substeps": 128,
        },
        "assumption_audit": {
            "bounded_derivatives_through_fourth_order": True,
            "reason": "The loss is a finite linear combination of sin and cos.",
            "minimum_interaction_ratio_over_measured_states": float(interaction_ratios.min()),
        },
        "per_initial": per_initial,
        "summary": {
            "corrected_order_mean": float(corrected_orders.mean()),
            "corrected_order_min": float(corrected_orders.min()),
            "corrected_order_max": float(corrected_orders.max()),
            "signgda_control_order_mean": float(control_orders.mean()),
            "signgda_control_order_min": float(control_orders.min()),
            "signgda_control_order_max": float(control_orders.max()),
        },
        "verdict": "PENDING_INDEPENDENT_CHECK",
    }
    (output_dir / "claim6_local_error.json").write_text(json.dumps(payload, indent=2) + "\n")
    return payload
