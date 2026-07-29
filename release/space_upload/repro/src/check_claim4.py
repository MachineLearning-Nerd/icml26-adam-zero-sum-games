"""Result-only checker for the Section 5 beta/rho flatness contract."""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


def strict(values: list[float], direction: str) -> bool:
    pairs = zip(values, values[1:])
    return all(left < right for left, right in pairs) if direction == "increasing" else all(
        left > right for left, right in pairs
    )


def main(csv_path: Path, output_path: Path) -> int:
    records: list[dict[str, object]] = []
    with csv_path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            records.append(
                {
                    "game": row["game"],
                    "axis": row["axis"],
                    "parameter": float(row["parameter"]),
                    "start_id": int(row["start_id"]),
                    "horizon": int(row["horizon"]),
                    "metric": float(row["cumulative_avg_gradient_l1"]),
                }
            )

    grouped: dict[tuple[str, str, int, float], list[float]] = defaultdict(list)
    paired: dict[tuple[str, str, int, float], dict[int, float]] = defaultdict(dict)
    for row in records:
        key = (str(row["game"]), str(row["axis"]), int(row["horizon"]), float(row["parameter"]))
        grouped[key].append(float(row["metric"]))
        paired[key][int(row["start_id"])] = float(row["metric"])

    summaries: list[dict[str, object]] = []
    rng = np.random.default_rng(20260729)
    accepted_horizons = (3000, 10000)
    for game in ("interaction_dominated", "interaction_free_control"):
        for axis, expected_direction in (("beta", "increasing"), ("rho", "decreasing")):
            for horizon in accepted_horizons:
                parameters = sorted(
                    key[3]
                    for key in grouped
                    if key[:3] == (game, axis, horizon)
                )
                means = [float(np.mean(grouped[(game, axis, horizon, value)])) for value in parameters]
                low = paired[(game, axis, horizon, parameters[0])]
                high = paired[(game, axis, horizon, parameters[-1])]
                start_ids = sorted(set(low) & set(high))
                differences = np.array(
                    [
                        (high[start_id] - low[start_id])
                        if axis == "beta"
                        else (low[start_id] - high[start_id])
                        for start_id in start_ids
                    ]
                )
                bootstrap = np.array(
                    [
                        np.mean(rng.choice(differences, size=len(differences), replace=True))
                        for _ in range(10000)
                    ]
                )
                summaries.append(
                    {
                        "game": game,
                        "axis": axis,
                        "horizon": horizon,
                        "parameters": parameters,
                        "means": means,
                        "expected_direction": expected_direction,
                        "strict_expected_order": strict(means, expected_direction),
                        "paired_extreme_difference_mean": float(differences.mean()),
                        "paired_extreme_difference_99pct_ci": [
                            float(np.quantile(bootstrap, 0.005)),
                            float(np.quantile(bootstrap, 0.995)),
                        ],
                        "all_paired_extreme_differences_positive": bool(np.all(differences > 0.0)),
                    }
                )

    primary = [row for row in summaries if row["game"] == "interaction_dominated"]
    control = [row for row in summaries if row["game"] == "interaction_free_control"]
    primary_pass = all(
        row["strict_expected_order"]
        and row["all_paired_extreme_differences_positive"]
        and row["paired_extreme_difference_99pct_ci"][0] > 0.0
        for row in primary
    )
    control_failed = any(not row["strict_expected_order"] for row in control)
    passed = primary_pass and control_failed
    result = {
        "checker": "result-only means, paired contrasts, and fixed-seed bootstrap",
        "accepted_horizons": list(accepted_horizons),
        "summaries": summaries,
        "interaction_dominated_contract_passed": primary_pass,
        "interaction_free_negative_control_failed_reversed_contract": control_failed,
        "passed": passed,
    }
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print("=== CLAIM 4 INDEPENDENT CHECKER ===")
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: check_claim4.py INPUT.csv OUTPUT.json")
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
