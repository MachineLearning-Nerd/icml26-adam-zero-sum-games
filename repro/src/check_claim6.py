"""Independent result-only checker for Claim 6.

This file deliberately does not import the Adam or ODE implementation. It sees
only the generated machine-readable errors and recomputes the observed orders.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


def main(csv_path: Path, output_path: Path) -> int:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    with csv_path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            groups[row["initial_id"]].append(row)

    checks: list[dict[str, object]] = []
    for initial_id, rows in sorted(groups.items()):
        rows.sort(key=lambda row: float(row["h"]))
        h = np.array([float(row["h"]) for row in rows])
        corrected = np.array([float(row["corrected_error"]) for row in rows])
        control = np.array([float(row["signgda_control_error"]) for row in rows])
        corrected_order = float(np.polyfit(np.log(h), np.log(corrected), 1)[0])
        control_order = float(np.polyfit(np.log(h), np.log(control), 1)[0])
        checks.append(
            {
                "initial_id": int(initial_id),
                "corrected_order": corrected_order,
                "control_order": control_order,
                "corrected_is_h3": 2.70 <= corrected_order <= 3.30,
                "control_rejected_as_h3": control_order < 2.40,
                "control_is_h2": 1.70 <= control_order <= 2.30,
            }
        )

    burn_in_valid = all(
        int(row["burn_in_steps"]) > 0
        for rows in groups.values()
        for row in rows
    )
    passed = burn_in_valid and all(
        item["corrected_is_h3"] and item["control_rejected_as_h3"] and item["control_is_h2"]
        for item in checks
    )
    result = {
        "checker": "result-only independent log-log regression",
        "checks": checks,
        "negative_control": "SignGDA-flow without the O(h) modified-equation correction",
        "negative_control_failed_h3_contract": all(item["control_rejected_as_h3"] for item in checks),
        "passed": passed,
    }
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print("=== CLAIM 6 INDEPENDENT CHECKER ===")
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: check_claim6.py INPUT.csv OUTPUT.json")
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
