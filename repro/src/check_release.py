"""Offline release gates for the evaluator-visible artifact."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PINNED_RAW = ROOT / ".openresearch" / "artifacts" / "release" / "raw"
UPLOAD = ROOT / "release" / "space_upload"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output_path: Path) -> int:
    checks: dict[str, object] = {}

    pinned_manifest = json.loads((PINNED_RAW / "output_manifest.json").read_text())
    mismatches = [
        item["path"]
        for item in pinned_manifest["files"]
        if sha256(PINNED_RAW / item["path"]) != item["sha256"]
    ]
    checks["pinned_raw_manifest_matches"] = not mismatches
    checks["pinned_raw_mismatches"] = mismatches

    baseline = json.loads((PINNED_RAW / "baseline_verdict.json").read_text())
    statuses = {int(item["claim"]): item["status"] for item in baseline["claims"]}
    checks["honest_claim_statuses"] = statuses == {
        1: "VERIFIED",
        2: "VERIFIED",
        3: "VERIFIED",
        4: "VERIFIED",
        5: "BLOCKED",
        6: "VERIFIED",
    }
    checker_names = [
        "claims123_checker.json",
        "claim4_checker.json",
        "claim5_route1_checker.json",
        "claim5_route2_checker.json",
        "claim5_route3_checker.json",
        "claim5_route4_checker.json",
        "claim6_checker.json",
    ]
    checks["all_checker_outputs_pass"] = all(
        json.loads((PINNED_RAW / name).read_text())["passed"] for name in checker_names
    )

    current_page = UPLOAD / "pages" / "current" / "page.md"
    page_text = current_page.read_text()
    visibility_rows = [
        line
        for line in page_text.splitlines()
        if re.match(r"^\| [1-6] \|", line)
    ]
    checks["six_complete_visibility_rows"] = (
        len(visibility_rows) == 6
        and all("yes" in row and "](../../" in row for row in visibility_rows)
    )
    checks["all_claim_sections_present"] = all(
        f"## Claim {claim} —" in page_text for claim in range(1, 7)
    )
    checks["current_verifier_precedes_history"] = (
        "Current claim-by-claim" in (UPLOAD / "README.md").read_text()
        and "Historical rejected baseline" in page_text
        and json.loads((UPLOAD / "logbook.json").read_text())["root"]["file"]
        == "pages/current/page.md"
    )

    required_relative_links = re.findall(r"\]\((\.\./\.\./[^)]+)\)", page_text)
    missing_links = [
        link
        for link in required_relative_links
        if not (current_page.parent / link).resolve().exists()
    ]
    checks["all_new_relative_links_resolve"] = not missing_links
    checks["missing_new_links"] = missing_links

    contract_files = sorted((UPLOAD / "evidence" / "contracts").glob("claim*.json"))
    checks["six_valid_claim_contracts"] = len(contract_files) == 6 and all(
        json.loads(path.read_text())["claim"] == index
        for index, path in enumerate(contract_files, start=1)
    )

    report = ROOT / "reports" / "adam-zero-sum" / "report.md"
    report_text = report.read_text()
    image_paths = re.findall(r"!\[[^\]]*\]\((images/[^)]+)\)", report_text)
    image_errors: list[str] = []
    for relative in image_paths:
        try:
            ET.parse(report.parent / relative)
        except (ET.ParseError, OSError):
            image_errors.append(relative)
    checks["four_renderable_evidence_figures"] = len(image_paths) == 4 and not image_errors
    checks["figure_errors"] = image_errors
    checks["headline_figure_immediately_after_title"] = report_text.splitlines()[2].startswith("![")

    release_report = (ROOT / "reports" / "adam-zero-sum" / "release-report.md").read_text()
    checks["release_report_required_opening"] = release_report.startswith(
        "- Previous live judged score: `6/12`\n"
        "- Conservative projected score range after the proposed change: `8–10/12`\n"
        "- Best-supported possible new score: `10/12`"
    )
    checks["readme_has_exact_fixed_command_and_main_accounting"] = (
        "`uv run --locked python repro/src/verify.py`" in (ROOT / "README.md").read_text()
        and "Not run as an experiment (publication surface)" in (ROOT / "README.md").read_text()
    )
    red_team = json.loads(
        (ROOT / ".openresearch" / "artifacts" / "release" / "red_team_prepublication_final.json").read_text()
    )
    checks["evaluator_blind_review_passed"] = (
        red_team["passed"]
        and not red_team["missing_files"]
        and not red_team["conclusions_not_verified"]
        and len(red_team["opened_files"]) >= 30
    )

    allowlist_path = ROOT / "release" / "upload_allowlist.txt"
    upload_manifest_path = ROOT / "release" / "upload_manifest.sha256"
    allowlist = allowlist_path.read_text().splitlines() if allowlist_path.exists() else []
    actual_paths = sorted(
        path.relative_to(UPLOAD).as_posix() for path in UPLOAD.rglob("*") if path.is_file()
    )
    checks["exact_upload_allowlist"] = allowlist == actual_paths
    expected_upload_hashes: dict[str, str] = {}
    if upload_manifest_path.exists():
        for line in upload_manifest_path.read_text().splitlines():
            digest, name = line.split("  ", 1)
            expected_upload_hashes[name] = digest
    checks["upload_manifest_complete_and_exact"] = (
        sorted(expected_upload_hashes) == actual_paths
        and all(sha256(UPLOAD / name) == digest for name, digest in expected_upload_hashes.items())
    )

    text_decode_errors: list[str] = []
    secret_hits: list[str] = []
    secret_patterns = [
        re.compile(r"hf_[A-Za-z0-9]{20,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ]
    for relative in actual_paths:
        data = (UPLOAD / relative).read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text_decode_errors.append(relative)
            continue
        if "\x00" in text:
            text_decode_errors.append(relative)
        if any(pattern.search(text) for pattern in secret_patterns):
            secret_hits.append(relative)
    checks["text_only_upload"] = not text_decode_errors
    checks["text_decode_errors"] = text_decode_errors
    checks["no_secret_patterns"] = not secret_hits
    checks["secret_hit_paths"] = secret_hits

    protected = (
        ROOT / ".openresearch" / "artifacts" / "release" / "protected_manifest.sha256"
    ).read_text().splitlines()
    protected_paths = [line.split("  ", 1)[1] for line in protected]
    checks["protected_manifest_has_13_files"] = len(protected_paths) == 13
    checks["only_navigation_overwrites_protected_paths"] = sorted(
        set(actual_paths) & set(protected_paths)
    ) == ["README.md", "logbook.json"]

    passed = all(
        value
        for key, value in checks.items()
        if key
        not in {
            "pinned_raw_mismatches",
            "missing_new_links",
            "figure_errors",
            "text_decode_errors",
            "secret_hit_paths",
        }
    )
    result = {"checker": "offline evaluator-visible release gates", "checks": checks, "passed": passed}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print("=== RELEASE GATE CHECKER ===")
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_release.py OUTPUT.json")
    raise SystemExit(main(Path(sys.argv[1])))
