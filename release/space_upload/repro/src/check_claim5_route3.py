"""Independent result-only checker for the Claim 5 CPU calibration."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(input_path: Path, output_path: Path) -> int:
    payload = json.loads(input_path.read_text())
    profiles = payload["profiles"]
    settings = {
        (row["architecture"], row["dataset_shape"], row["resolution"])
        for row in profiles
    }
    settings_complete = settings == {
        ("CNN", "CIFAR-10", 32),
        ("CNN", "STL-10", 64),
        ("ResNet", "CIFAR-10", 32),
        ("ResNet", "STL-10", 64),
    }
    full_batch = all(row["batch_size"] == 64 for row in profiles)
    control_faster = all(
        row["forward_only_seconds"] < row["joint_wgan_gp_seconds"] for row in profiles
    )
    timings_positive = all(
        row["joint_wgan_gp_seconds"] > 0.0
        and all(value > 0.0 for value in row["parameter_gradient_l1"])
        for row in profiles
    )
    allocation_audited = (
        payload["cpu"]["selected_flavor"] == "cpu-upgrade"
        and payload["cpu"]["actual_quota_cores"] > 1
    )
    honest_blocked = payload["not_claim_evidence"] and payload["verdict"] == "BLOCKED"
    passed = (
        settings_complete
        and full_batch
        and control_faster
        and timings_positive
        and allocation_audited
        and honest_blocked
    )
    result = {
        "checker": "result-only CPU feasibility checker",
        "four_reported_shape_architecture_pairs_profiled": settings_complete,
        "batch_size_64": full_batch,
        "forward_only_control_is_faster": control_faster,
        "training_and_gradient_measurements_positive": timings_positive,
        "cpu_upgrade_allocation_audited": allocation_audited,
        "profile_not_promoted_to_claim_evidence": honest_blocked,
        "passed": passed,
    }
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print("=== CLAIM 5 ROUTE 3 CHECKER ===")
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: check_claim5_route3.py INPUT.json OUTPUT.json")
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
