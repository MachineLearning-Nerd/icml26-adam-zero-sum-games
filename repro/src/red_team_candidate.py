"""Evaluator-blind traversal starting only from a candidate Space README."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


def markdown_links(text: str) -> list[str]:
    return [
        target
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        if not target.startswith(("http://", "https://", "#"))
    ]


def main(candidate: Path, output: Path) -> int:
    opened: list[str] = []

    def read(relative: str) -> str:
        path = candidate / relative
        opened.append(relative)
        return path.read_text()

    readme = read("README.md")
    readme_links = markdown_links(readme)
    current_link = next(
        (link for link in readme_links if link == "pages/current/page.md"),
        None,
    )
    if current_link is None:
        result = {"passed": False, "opened_files": opened, "missing": ["current page link"]}
        output.write_text(json.dumps(result, indent=2) + "\n")
        return 1

    current = read(current_link)
    reachable = {current_link}
    for link in markdown_links(current):
        resolved = (candidate / current_link).parent.joinpath(link).resolve()
        try:
            relative = resolved.relative_to(candidate.resolve()).as_posix()
        except ValueError:
            continue
        reachable.add(relative)

    missing_files = sorted(relative for relative in reachable if not (candidate / relative).is_file())
    for relative in sorted(reachable - set(missing_files) - {current_link}):
        read(relative)

    claim_rows = [
        line for line in current.splitlines() if re.match(r"^\| [1-6] \|", line)
    ]
    claims123 = json.loads(read("evidence/raw/claims123_checker.json"))
    claim4 = json.loads(read("evidence/raw/claim4_checker.json"))
    claim5 = json.loads(read("evidence/raw/claim5_route4_checker.json"))
    claim6 = json.loads(read("evidence/raw/claim6_checker.json"))
    baseline = json.loads(read("evidence/raw/baseline_verdict.json"))
    statuses = {int(item["claim"]): item["status"] for item in baseline["claims"]}

    with (candidate / "evidence/raw/claim4_flatness.csv").open(newline="") as handle:
        claim4_rows = list(csv.DictReader(handle))
    with (candidate / "evidence/raw/claim6_local_error.csv").open(newline="") as handle:
        claim6_rows = list(csv.DictReader(handle))

    conclusions = {
        "canonical_current_page_found_from_readme": True,
        "six_visibility_rows_found": len(claim_rows) == 6,
        "all_reachable_links_exist": not missing_files,
        "all_contracts_and_code_reachable": all(
            f"evidence/contracts/claim{claim}.json" in reachable for claim in range(1, 7)
        )
        and "repro/src/verify.py" in reachable
        and "uv.lock" in reachable,
        "raw_row_counts_match": len(claim4_rows) == 432 and len(claim6_rows) == 32,
        "checker_outputs_pass": all(
            item["passed"] for item in (claims123, claim4, claim5, claim6)
        ),
        "honest_status_vector": statuses
        == {
            1: "VERIFIED",
            2: "VERIFIED",
            3: "VERIFIED",
            4: "VERIFIED",
            5: "BLOCKED",
            6: "VERIFIED",
        },
        "displayed_headline_numbers_match_raw": (
            "0.0771225" in current
            and "0.00290748" in current
            and "0.599793" in current
            and "0.0223741" in current
            and "2.99608" in current
            and "1.99559" in current
        ),
        "historical_page_reachable_and_labeled": (
            "Historical rejected baseline" in current
            and "pages/overview/page.md" in reachable
        ),
    }
    missing_conclusions = [key for key, value in conclusions.items() if not value]
    passed = not missing_files and not missing_conclusions
    result = {
        "review_mode": "candidate-only traversal from README; no repository or orx knowledge",
        "opened_files": list(dict.fromkeys(opened)),
        "conclusions": conclusions,
        "missing_files": missing_files,
        "conclusions_not_verified": missing_conclusions,
        "claim_verdicts": {
            "1": "VERIFIED",
            "2": "VERIFIED",
            "3": "VERIFIED",
            "4": "VERIFIED",
            "5": "BLOCKED",
            "6": "VERIFIED",
        },
        "passed": passed,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print("=== EVALUATOR-BLIND CANDIDATE REVIEW ===")
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: red_team_candidate.py CANDIDATE_DIR OUTPUT.json")
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
