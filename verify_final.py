#!/usr/bin/env python3
"""Verify the committed publication contract for this repository."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_STATUS = "PARTIAL_C1_C2_C3_C4_C6_VERIFIED_C5_BLOCKED_HISTORICAL_SCORE_6_OF_12_NO_CURRENT_SCORE"
EXPECTED_BRANCHES = {
    "audit/c4-beta-rho-flatness",
    "audit/c4-published-rho-grid",
    "audit/c5-cpu-feasibility",
    "audit/c5-mandatory-falsification",
    "audit/c5-source-completeness",
    "audit/c5-table-consistency",
    "audit/c6-direct-local-error",
    "audit/c6-fixed-time-local-error",
    "historical/judged-baseline",
    "main",
    "release/cumulative-evidence",
    "release/final-publication-gates",
    "release/warning-free-notebook",
}
EXPECTED_COMMITS = 29
CANONICAL_IDENTITY = "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"


def load(name: str):
    return json.loads((ROOT / name).read_text())


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"verification failed: {message}")


def published_branches() -> set[str]:
    remote = {
        name.removeprefix("origin/")
        for name in git(
            "for-each-ref", "refs/remotes/origin", "--format=%(refname:short)"
        ).splitlines()
        if name.startswith("origin/") and name != "origin/HEAD"
    }
    if remote:
        return remote
    return set(git("for-each-ref", "refs/heads", "--format=%(refname:short)").splitlines())


def main() -> None:
    claims = load("claims.json")
    verdicts = load("reproduction_verdicts.json")
    manifest = load("EVIDENCE_MANIFEST.json")
    state = load("AUTONOMOUS_STATE.json")
    baseline = load("reports/adam-zero-sum/raw/baseline_verdict.json")
    claims123_checker = load("reports/adam-zero-sum/raw/claims123_checker.json")
    claim4_checker = load("reports/adam-zero-sum/raw/claim4_checker.json")
    claim5_route1 = load("reports/adam-zero-sum/raw/claim5_route1_checker.json")
    claim5_route2 = load("reports/adam-zero-sum/raw/claim5_route2_checker.json")
    claim5_route3 = load("reports/adam-zero-sum/raw/claim5_route3_checker.json")
    claim5_route4 = load("reports/adam-zero-sum/raw/claim5_route4_checker.json")
    claim5_falsification = load("reports/adam-zero-sum/raw/claim5_route4_falsification.json")
    claim6_checker = load("reports/adam-zero-sum/raw/claim6_checker.json")
    red_team = load("release/space_upload/evidence/red_team_prepublication_final.json")

    expected_statuses = {
        "C1": "VERIFIED_SCOPED",
        "C2": "VERIFIED_SCOPED",
        "C3": "VERIFIED_SCOPED",
        "C4": "VERIFIED_SCOPED",
        "C5": "BLOCKED_PROTOCOL",
        "C6": "VERIFIED_SCOPED",
    }
    require(claims["overall_status"] == EXPECTED_STATUS, "claims overall status")
    require(state["overall_status"] == EXPECTED_STATUS, "state overall status")
    require(verdicts["claim_statuses"] == expected_statuses, "verdict statuses")
    require({claim["id"]: claim["status"] for claim in claims["claims"]} == expected_statuses, "claim statuses")
    require(all((ROOT / path).exists() for path in manifest["required_paths"]), "manifest paths")
    require(claims["paper"]["html_sha256"] == manifest["source"]["html_sha256"], "source hash")
    statuses = {str(item["claim"]): item["status"] for item in baseline["claims"]}
    require(statuses == {"1": "VERIFIED", "2": "VERIFIED", "3": "VERIFIED", "4": "VERIFIED", "5": "BLOCKED", "6": "VERIFIED"}, "baseline claim statuses")
    require(baseline["baseline_judge_score"] == "6/12", "historical score")
    require(baseline["accepted_regressions_pass"] is True, "accepted regressions")
    require(claims123_checker["passed"] is True, "Claims 1-3 checker")
    require(claim4_checker["passed"] is True, "Claim 4 checker")
    require(all(route["passed"] is True for route in [claim5_route1, claim5_route2, claim5_route3, claim5_route4]), "Claim 5 route checkers")
    require(claim5_falsification["verdict"] == "BLOCKED" and claim5_falsification["falsification_established"] is False, "Claim 5 blocked boundary")
    require(claim6_checker["passed"] is True, "Claim 6 checker")
    require(red_team["passed"] is True and red_team["conclusions"]["honest_status_vector"] is True, "red-team release review")
    require(verdicts["historical_external_result"]["current_score_claim"] is False, "current score claim")
    require(verdicts["publication"]["publication_allowed"] is False, "publication state")
    require(verdicts["publication"]["author_endorsement_claimed"] is False, "author endorsement state")
    require("DineshAI/4MVVscCjYu" in (ROOT / "release/space_upload/logbook.json").read_text(), "Space identity")

    branches = published_branches()
    require(branches == EXPECTED_BRANCHES, "published branches")
    require(not any(branch.startswith("orx/") for branch in branches), "legacy orx branch")
    require(int(git("rev-list", "--all", "--count")) == EXPECTED_COMMITS, "reachable commit count")
    identities = git("log", "--all", "--format=%an <%ae>\n%cn <%ce>").splitlines()
    require(identities and all(identity == CANONICAL_IDENTITY for identity in identities), "canonical commit identity")

    print(
        "FINAL_AUDIT=VERIFIED "
        f"branches={len(branches)} commits={EXPECTED_COMMITS} "
        "claims=C1:C4_C6_verified_scoped,C5_blocked_protocol historical_score=6/12 "
        "current_score_claim=false publication_allowed=false"
    )


if __name__ == "__main__":
    main()
