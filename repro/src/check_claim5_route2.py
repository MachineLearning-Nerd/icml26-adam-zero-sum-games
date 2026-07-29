"""Independent result-only checker for Claim 5 route 2."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(input_path: Path, output_path: Path) -> int:
    payload = json.loads(input_path.read_text())
    beta_direction = all(
        row["spearman_beta_vs_is"] < 0.0 for row in payload["beta_summaries"]
    )
    beta_not_strict = any(
        not row["strict_is_decrease_as_beta_increases"]
        for row in payload["beta_summaries"]
    )
    rho_strict = all(
        row["strict_is_increase_as_rho_increases"]
        and row["spearman_rho_vs_is"] == 1.0
        for row in payload["rho_summaries"]
    )
    fixed_beta_inconsistency = all(
        row["distance_to_beta_minus_point_three"] < row["distance_to_beta_zero"]
        for row in payload["fixed_beta_consistency"]
    )
    honest_blocked = payload["verdict"] == "BLOCKED"
    passed = (
        beta_direction
        and beta_not_strict
        and rho_strict
        and fixed_beta_inconsistency
        and honest_blocked
    )
    result = {
        "checker": "result-only reported-table audit",
        "all_beta_rank_associations_have_paper_direction": beta_direction,
        "beta_association_is_not_strictly_monotone": beta_not_strict,
        "all_rho_tables_are_strictly_monotone": rho_strict,
        "table2_rho_point9_is_closer_to_beta_minus_point3_than_beta0": (
            fixed_beta_inconsistency
        ),
        "blocked_instead_of_reproduction_pass": honest_blocked,
        "passed": passed,
    }
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print("=== CLAIM 5 ROUTE 2 CHECKER ===")
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: check_claim5_route2.py INPUT.json OUTPUT.json")
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
