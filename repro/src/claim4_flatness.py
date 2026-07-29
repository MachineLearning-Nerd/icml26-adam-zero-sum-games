"""Direct beta/rho test of the Section 5 cumulative L1-gradient thesis."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

import core as M


BETA_VALUES = (-0.3, 0.0, 0.3, 0.6, 0.9)
RHO_VALUES = (0.3, 0.5, 0.7, 0.9)
HORIZONS = (1000, 3000, 10000)
STARTS = (
    (0.5, 0.5),
    (-0.5, 0.5),
    (0.5, -0.5),
    (-0.5, -0.5),
    (0.8, 0.2),
    (-0.8, 0.2),
    (0.2, -0.8),
    (-0.2, -0.8),
)
EPS = 0.05


def cumulative_gradient_l1(
    game: dict[str, object],
    start: tuple[float, float],
    beta: float,
    rho: float,
    h: float,
) -> tuple[np.ndarray, np.ndarray]:
    trajectory = M.simulate(game, *start, beta, rho, EPS, h, max(HORIZONS))
    gradient_l1 = np.array(
        [sum(abs(value) for value in M.gradf(tuple(state), game)) for state in trajectory[1:]]
    )
    cumulative = np.cumsum(gradient_l1) / np.arange(1, len(gradient_l1) + 1)
    return gradient_l1, cumulative


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    games = {
        "interaction_dominated": M.make_game(a=1.0, b=1.0, c=3.0),
        "interaction_free_control": M.make_game(a=1.0, b=1.0, c=0.0),
    }
    rows: list[dict[str, object]] = []
    specifications = (
        ("beta", BETA_VALUES, 0.9, 0.0005),
        ("rho", RHO_VALUES, 0.0, 0.01),
    )
    for game_name, game in games.items():
        for axis, values, fixed_value, h in specifications:
            for parameter in values:
                beta = float(parameter) if axis == "beta" else float(fixed_value)
                rho = float(fixed_value) if axis == "beta" else float(parameter)
                for start_id, start in enumerate(STARTS):
                    gradient_l1, cumulative = cumulative_gradient_l1(
                        game, start, beta, rho, h
                    )
                    for horizon in HORIZONS:
                        rows.append(
                            {
                                "game": game_name,
                                "axis": axis,
                                "parameter": float(parameter),
                                "beta": beta,
                                "rho": rho,
                                "h": h,
                                "epsilon": EPS,
                                "start_id": start_id,
                                "x0": start[0],
                                "y0": start[1],
                                "horizon": horizon,
                                "cumulative_avg_gradient_l1": float(cumulative[horizon - 1]),
                                "instantaneous_gradient_l1": float(gradient_l1[horizon - 1]),
                                "interaction_ratio": (
                                    abs(float(game["c"]))
                                    / max(abs(float(game["a"])), abs(float(game["b"])))
                                ),
                            }
                        )

    csv_path = output_dir / "claim4_flatness.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    payload = {
        "claim": 4,
        "paper_anchor": "Section 5 thesis and AvgS definition",
        "metric": "cumulative average of ||grad_x f||_1 + ||grad_y f||_1",
        "parameters": {
            "beta_values": list(BETA_VALUES),
            "rho_values": list(RHO_VALUES),
            "horizons": list(HORIZONS),
            "starts": [list(start) for start in STARTS],
            "beta_sweep": {"fixed_rho": 0.9, "h": 0.0005},
            "rho_sweep": {"fixed_beta": 0.0, "h": 0.01},
            "epsilon": EPS,
        },
        "assumption_audit": {
            "interaction_game_cross_to_self_hessian_ratio": 3.0,
            "interaction_game_jacobian_eigenvalues": [
                [float(value.real), float(value.imag)]
                for value in np.asarray(games["interaction_dominated"]["lam"])
            ],
            "negative_control_cross_to_self_hessian_ratio": 0.0,
        },
        "row_count": len(rows),
        "verdict": "PENDING_INDEPENDENT_CHECK",
    }
    (output_dir / "claim4_flatness.json").write_text(json.dumps(payload, indent=2) + "\n")
    return payload
