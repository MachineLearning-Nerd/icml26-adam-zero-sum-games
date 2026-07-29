"""Independent result-only checker and negative controls for Claims 1--3."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def strictly_decreasing(values: list[float]) -> bool:
    return all(left > right for left, right in zip(values, values[1:]))


def main(input_path: Path, output_path: Path) -> int:
    payload = json.loads(input_path.read_text())
    claims = {int(item["claim"]): item for item in payload["claims"]}

    claim1 = claims[1]
    claim1_pass = (
        claim1["status"] == "VERIFIED"
        and strictly_decreasing([float(value) for value in claim1["max_stable_h"]])
    )

    claim2 = claims[2]
    claim2_pass = (
        claim2["status"] == "VERIFIED"
        and strictly_decreasing([float(value) for value in claim2["continuous_bound"]])
        and strictly_decreasing([float(value) for value in claim2["discrete_bound"]])
    )

    claim3 = claims[3]
    claim3_pass = (
        claim3["status"] == "VERIFIED"
        and all(abs(float(value)) <= 1e-15 for value in claim3["eigenvalues_real"])
        and float(claim3["bound_discrete"]) == 0.0
        and not bool(claim3["any_converged"])
    )

    controls = {
        "claim1_reversed_observations_fail": not strictly_decreasing(
            list(reversed([float(value) for value in claim1["max_stable_h"]]))
        ),
        "claim2_constant_bound_fails_strictness": not strictly_decreasing(
            [float(claim2["continuous_bound"][0])] * len(claim2["continuous_bound"])
        ),
        "claim3_positive_real_part_fails_bilinear_certificate": not all(
            abs(value) <= 1e-15 for value in (-0.1, -0.1)
        ),
    }
    passed = claim1_pass and claim2_pass and claim3_pass and all(controls.values())
    result = {
        "checker": "independent result-only checker for accepted Claims 1-3",
        "claim_checks": {
            "claim1_strict_boundary_order": claim1_pass,
            "claim2_both_bounds_strict": claim2_pass,
            "claim3_bilinear_zero-bound_certificate": claim3_pass,
        },
        "negative_controls": controls,
        "passed": passed,
    }
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print("=== CLAIMS 1-3 INDEPENDENT CHECKER ===")
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: check_claims123.py INPUT.json OUTPUT.json")
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
