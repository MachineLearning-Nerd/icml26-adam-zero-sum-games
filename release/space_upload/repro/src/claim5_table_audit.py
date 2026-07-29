"""Route 2: reconstruct and audit the paper-reported Inception Score tables."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


SETTINGS = ("ResNet CIFAR-10", "ResNet STL-10", "CNN CIFAR-10", "CNN STL-10")
BETA = np.array([-0.5, -0.3, -0.2, 0.0, 0.2, 0.3, 0.5])
BETA_IS = {
    "ResNet CIFAR-10": [7.002, 7.087, 7.020, 7.022, 5.217, 4.698, 4.160],
    "ResNet STL-10": [6.878, 7.181, 6.969, 6.445, 5.565, 4.858, 4.447],
    "CNN CIFAR-10": [6.761, 7.010, 7.062, 6.804, 6.519, 6.322, 4.942],
    "CNN STL-10": [7.520, 7.791, 7.383, 7.594, 7.302, 7.178, 6.775],
}
RHO = np.array([0.3, 0.5, 0.7, 0.9])
RHO_IS = {
    "ResNet CIFAR-10": [6.265, 6.308, 6.483, 7.087],
    "ResNet STL-10": [5.571, 6.335, 6.486, 7.187],
    "CNN CIFAR-10": [6.280, 6.685, 6.809, 7.010],
    "CNN STL-10": [6.541, 6.775, 7.332, 7.791],
}


def ranks(values: np.ndarray) -> np.ndarray:
    return np.argsort(np.argsort(values)).astype(float)


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    beta_summaries: list[dict[str, object]] = []
    rho_summaries: list[dict[str, object]] = []
    for setting in SETTINGS:
        beta_values = np.asarray(BETA_IS[setting])
        beta_summaries.append(
            {
                "setting": setting,
                "spearman_beta_vs_is": float(
                    np.corrcoef(ranks(BETA), ranks(beta_values))[0, 1]
                ),
                "strict_is_decrease_as_beta_increases": bool(
                    np.all(np.diff(beta_values) < 0.0)
                ),
                "best_beta": float(BETA[np.argmax(beta_values)]),
            }
        )
        rho_values = np.asarray(RHO_IS[setting])
        rho_summaries.append(
            {
                "setting": setting,
                "strict_is_increase_as_rho_increases": bool(
                    np.all(np.diff(rho_values) > 0.0)
                ),
                "spearman_rho_vs_is": float(
                    np.corrcoef(ranks(RHO), ranks(rho_values))[0, 1]
                ),
            }
        )

    beta_zero_index = int(np.where(BETA == 0.0)[0][0])
    beta_minus_point_three_index = int(np.where(BETA == -0.3)[0][0])
    fixed_beta_consistency = []
    for setting in SETTINGS:
        table2_rho_point9 = RHO_IS[setting][-1]
        fixed_beta_consistency.append(
            {
                "setting": setting,
                "table2_rho_point9": table2_rho_point9,
                "table1_beta_zero": BETA_IS[setting][beta_zero_index],
                "table1_beta_minus_point_three": BETA_IS[setting][
                    beta_minus_point_three_index
                ],
                "distance_to_beta_zero": abs(
                    table2_rho_point9 - BETA_IS[setting][beta_zero_index]
                ),
                "distance_to_beta_minus_point_three": abs(
                    table2_rho_point9
                    - BETA_IS[setting][beta_minus_point_three_index]
                ),
            }
        )

    payload = {
        "claim": 5,
        "route": 2,
        "route_name": "reported-table consistency and association audit",
        "source_hashes": {
            "Table_1.tex": "fa81759aa1061d92d58eae6c060b53595648567dbf2273857fbd589ca9dc361e",
            "Table_2.tex": "90fae30aa8711bd0033d3af97d9b3ec480536dae2aba4540851cbeea80f899bd",
        },
        "beta_values_ascending": BETA.tolist(),
        "beta_inception_scores": BETA_IS,
        "rho_values_ascending": RHO.tolist(),
        "rho_inception_scores": RHO_IS,
        "beta_summaries": beta_summaries,
        "rho_summaries": rho_summaries,
        "fixed_beta_consistency": fixed_beta_consistency,
        "paper_text_fixed_beta_for_rho_sweep": 0.0,
        "verdict": "BLOCKED",
        "reason": (
            "Reported aggregate IS values support directional association, but "
            "are not reproduction data and Table 2's rho=0.9 values align with "
            "the beta=-0.3 row rather than the text's fixed beta=0 setting."
        ),
    }
    (output_dir / "claim5_route2_table_audit.json").write_text(
        json.dumps(payload, indent=2) + "\n"
    )
    return payload
