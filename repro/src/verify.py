"""Frozen reconstruction of the three checks accepted by the live judge.

This baseline intentionally leaves Claims 4--6 BLOCKED. Children must retain
these regression checks and replace the blocked entries only with direct,
claim-specific evidence.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

import core as M
import claim4_flatness
import claim6_local_error


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "outputs"
GAME = M.make_game(a=1.0, b=1.0, c=3.0)
EPS = 0.05


def cpu_allocation() -> dict[str, object]:
    affinity = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None
    cgroup_cpu_max = None
    cpu_max = Path("/sys/fs/cgroup/cpu.max")
    if cpu_max.exists():
        cgroup_cpu_max = cpu_max.read_text().strip()
    return {
        "estimated_required_cores": 2,
        "selected_backend": "hf",
        "selected_flavor": "cpu-upgrade",
        "os_cpu_count": os.cpu_count(),
        "affinity_cpu_count": affinity,
        "cgroup_cpu_max": cgroup_cpu_max,
        "runtime_scope": "uv environment materialization plus serial NumPy regressions",
    }


def max_stable_h(beta: float, rho: float = 0.9, steps: int = 1500) -> float:
    lo, hi = 1e-4, 2.0
    for _ in range(14):
        mid = (lo + hi) / 2.0
        if M.converges(GAME, beta, rho, EPS, mid, T=steps):
            lo = mid
        else:
            hi = mid
    return lo


def accepted_regressions() -> list[dict[str, object]]:
    betas = [-0.3, 0.0, 0.3, 0.6, 0.9]
    stable = [max_stable_h(beta) for beta in betas]
    c1 = all(stable[i] > stable[i + 1] for i in range(len(stable) - 1))

    monotone_betas = np.linspace(-0.49, 0.9, 8)
    continuous = [M.bound_continuous(GAME, float(beta), 1.0) for beta in monotone_betas]
    discrete = [M.bound_discrete(GAME, float(beta), 1.0) for beta in monotone_betas]
    c2 = all(continuous[i] > continuous[i + 1] for i in range(7)) and all(
        discrete[i] > discrete[i + 1] for i in range(7)
    )

    bilinear = M.make_game(a=0.0, b=0.0, c=1.0)
    any_converged = any(
        M.converges(bilinear, beta, rho, EPS, h, T=1000)
        for beta in (-0.5, 0.0, 0.5, 0.9)
        for rho in (0.5, 0.9, 0.99)
        for h in (0.001, 0.01, 0.1)
    )
    c3 = M.bound_discrete(bilinear, 0.0, EPS) == 0.0 and not any_converged

    return [
        {
            "claim": 1,
            "status": "VERIFIED" if c1 else "FAILED",
            "beta": betas,
            "max_stable_h": stable,
            "strictly_decreasing": c1,
        },
        {
            "claim": 2,
            "status": "VERIFIED" if c2 else "FAILED",
            "beta": monotone_betas.tolist(),
            "continuous_bound": continuous,
            "discrete_bound": discrete,
            "strictly_decreasing": c2,
            "source_scope_note": "Discrete monotonicity is checked inside Corollary 4.5's beta domain.",
        },
        {
            "claim": 3,
            "status": "VERIFIED" if c3 else "FAILED",
            "eigenvalues_real": np.asarray(bilinear["lam"]).real.tolist(),
            "bound_discrete": M.bound_discrete(bilinear, 0.0, EPS),
            "any_converged": any_converged,
        },
    ]


def main() -> int:
    started = time.perf_counter()
    claims = accepted_regressions()
    claim4 = claim4_flatness.run(OUTPUT)
    claim4_checker_path = OUTPUT / "claim4_checker.json"
    claim4_checker = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("check_claim4.py")),
            str(OUTPUT / "claim4_flatness.csv"),
            str(claim4_checker_path),
        ],
        check=False,
    )
    claim4_checker_payload = (
        json.loads(claim4_checker_path.read_text())
        if claim4_checker_path.exists()
        else {"passed": False}
    )
    claim4_status = (
        "VERIFIED"
        if claim4_checker.returncode == 0 and claim4_checker_payload["passed"]
        else "FAILED"
    )
    claim4["verdict"] = claim4_status
    claims.append(
        {
            "claim": 4,
            "status": claim4_status,
            "metric": claim4["metric"],
            "interaction_dominated_contract_passed": claim4_checker_payload.get(
                "interaction_dominated_contract_passed", False
            ),
            "interaction_free_negative_control_failed_reversed_contract": (
                claim4_checker_payload.get(
                    "interaction_free_negative_control_failed_reversed_contract", False
                )
            ),
        }
    )
    claims.append(
        {"claim": 5, "status": "BLOCKED", "reason": "No faithful GAN training evidence yet."}
    )
    claim6 = claim6_local_error.run(OUTPUT)
    checker_path = OUTPUT / "claim6_checker.json"
    checker = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("check_claim6.py")),
            str(OUTPUT / "claim6_local_error.csv"),
            str(checker_path),
        ],
        check=False,
    )
    checker_payload = json.loads(checker_path.read_text()) if checker_path.exists() else {"passed": False}
    claim6_status = "VERIFIED" if checker.returncode == 0 and checker_payload["passed"] else "FAILED"
    claim6["verdict"] = claim6_status
    claims.append(
        {
            "claim": 6,
            "status": claim6_status,
            "direct_local_error": claim6["summary"],
            "negative_control_failed_h3_contract": checker_payload.get(
                "negative_control_failed_h3_contract", False
            ),
        }
    )
    accepted_pass = all(item["status"] == "VERIFIED" for item in claims[:3])
    payload = {
        "paper": "2605.19392",
        "openreview": "4MVVscCjYu",
        "baseline_judge_score": "6/12",
        "historical_space_revision": "2e0e908df273cf1cbba8a5455926f06d5f411808",
        "claims": claims,
        "accepted_regressions_pass": accepted_pass,
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "numpy": np.__version__,
        },
        "cpu": cpu_allocation(),
        "runtime_seconds": time.perf_counter() - started,
    }
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "baseline_verdict.json").write_text(json.dumps(payload, indent=2) + "\n")
    print("=== FROZEN BASELINE EVIDENCE ===")
    print(json.dumps(payload, indent=2))
    print("=== CLAIM 6 RAW LOCAL-ERROR EVIDENCE ===")
    print(json.dumps(claim6, indent=2))
    print("=== CLAIM 4 RAW FLATNESS EVIDENCE ===")
    print(json.dumps(claim4, indent=2))
    if not accepted_pass or claim4_status != "VERIFIED" or claim6_status != "VERIFIED":
        print("ERROR: cumulative claim verification failed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
