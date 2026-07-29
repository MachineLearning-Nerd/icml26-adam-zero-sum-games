"""Independent checker for the mandatory Claim 5 falsification route."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(input_path: Path, output_path: Path) -> int:
    payload = json.loads(input_path.read_text())
    valid = [
        candidate["name"]
        for candidate in payload["candidates"]
        if candidate["gan_domain_satisfied"]
        and candidate["all_required_joint_gradient_and_is_evidence_present"]
        and candidate["contradicts_exact_tendency_quantifier"]
    ]
    universal_control = payload["universalized_negative_control"]
    control_detects_stronger_counterexample = (
        universal_control["counterexample_detected"]
        and not universal_control["is_the_paper_exact_quantifier"]
    )
    quadratic_rejected_for_domain = any(
        candidate["name"] == "quadratic_rho_point95_point99_reversal"
        and not candidate["gan_domain_satisfied"]
        for candidate in payload["candidates"]
    )
    exact_falsification_absent = (
        not valid
        and not payload["falsification_established"]
        and payload["valid_assumption_satisfying_counterexamples"] == []
    )
    honest_final_status = payload["verdict"] == "BLOCKED" and len(payload["unblockers"]) >= 3
    passed = (
        control_detects_stronger_counterexample
        and quadratic_rejected_for_domain
        and exact_falsification_absent
        and honest_final_status
    )
    result = {
        "checker": "independent assumptions-and-quantifier falsification checker",
        "stronger_universal_claim_control_is_falsified": (
            control_detects_stronger_counterexample
        ),
        "assumption_violating_quadratic_candidate_rejected": quadratic_rejected_for_domain,
        "exact_claim_has_no_valid_counterexample": exact_falsification_absent,
        "final_status_blocked_with_unblockers": honest_final_status,
        "passed": passed,
    }
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print("=== CLAIM 5 ROUTE 4 CHECKER ===")
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: check_claim5_route4.py INPUT.json OUTPUT.json")
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
