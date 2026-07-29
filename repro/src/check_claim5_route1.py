"""Independent checker for Claim 5's honest route-1 BLOCKED result."""

from __future__ import annotations

import json
import sys
from pathlib import Path


CRITICAL = {
    "executable_author_code",
    "exact_resnet_definition",
    "exact_cnn_definition",
    "training_seeds",
    "main_experiment_training_horizon",
    "inception_implementation_and_sample_count",
    "raw_gradient_norm_timeseries",
}


def main(input_path: Path, output_path: Path) -> int:
    payload = json.loads(input_path.read_text())
    fields = payload["required_reproduction_fields"]
    critical_missing = sorted(name for name in CRITICAL if fields.get(name) is not True)
    settings_present = (
        payload["disclosed"]["datasets"] == ["CIFAR-10 32x32", "STL-10 64x64"]
        and payload["disclosed"]["architectures"] == ["ResNet", "CNN"]
        and payload["disclosed"]["learning_rate"] == 0.0002
        and payload["disclosed"]["batch_size"] == 64
    )
    honest_blocked = (
        payload["verdict"] == "BLOCKED"
        and not payload["author_source_uniquely_executable"]
        and bool(critical_missing)
    )
    passed = settings_present and honest_blocked
    result = {
        "checker": "result-only source-completeness checker",
        "reported_settings_recovered": settings_present,
        "critical_missing_fields": critical_missing,
        "blocked_instead_of_false_pass": honest_blocked,
        "passed": passed,
    }
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print("=== CLAIM 5 ROUTE 1 CHECKER ===")
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: check_claim5_route1.py INPUT.json OUTPUT.json")
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
