"""Route 4: mandatory assumption-satisfying falsification attempt for Claim 5."""

from __future__ import annotations

import json
from pathlib import Path


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    exact_contract = {
        "statement": (
            "For the paper's ResNet and CNN improved-WGAN experiments on "
            "CIFAR-10 and STL-10, smaller beta and larger rho empirically tend "
            "to produce lower cumulative AvgS, and lower AvgS tends to coincide "
            "with higher Inception Score."
        ),
        "domain": [
            "actual GAN training",
            "ResNet and CNN architectures",
            "CIFAR-10 and STL-10",
            "paper-defined cumulative parameter-gradient L1 AvgS",
            "Inception Score from the corresponding trained models",
        ],
        "quantifier": (
            "qualitative empirical tendency across settings, not a universal "
            "strict ordering for every adjacent momentum pair or seed"
        ),
    }
    candidates = [
        {
            "name": "beta_minus_point5_vs_minus_point3_reported_IS",
            "evidence": {
                "beta_minus_point5": [7.002, 6.878, 6.761, 7.520],
                "beta_minus_point3": [7.087, 7.181, 7.010, 7.791],
            },
            "gan_domain_satisfied": True,
            "all_required_joint_gradient_and_is_evidence_present": False,
            "contradicts_exact_tendency_quantifier": False,
            "rejection_reason": (
                "Every smaller-beta IS is lower for this one adjacent pair, "
                "but the source claim says 'tend' and no per-run joint AvgS/IS "
                "data are available. This refutes only a stronger universal claim."
            ),
        },
        {
            "name": "table2_fixed_beta_metadata_mismatch",
            "gan_domain_satisfied": True,
            "all_required_joint_gradient_and_is_evidence_present": False,
            "contradicts_exact_tendency_quantifier": False,
            "rejection_reason": (
                "The mismatch makes the experiment ambiguous; it is not a "
                "performance counterexample."
            ),
        },
        {
            "name": "quadratic_rho_point95_point99_reversal",
            "gan_domain_satisfied": False,
            "all_required_joint_gradient_and_is_evidence_present": False,
            "contradicts_exact_tendency_quantifier": False,
            "rejection_reason": (
                "The analytic quadratic is interaction-dominated but is not a "
                "ResNet/CNN GAN on CIFAR-10 or STL-10."
            ),
        },
        {
            "name": "synthetic_full_shape_cpu_profile",
            "gan_domain_satisfied": False,
            "all_required_joint_gradient_and_is_evidence_present": False,
            "contradicts_exact_tendency_quantifier": False,
            "rejection_reason": (
                "Synthetic tensors measure runtime only and contain neither "
                "dataset training nor Inception Scores."
            ),
        },
    ]
    universalized_control = {
        "statement": "IS is strictly nondecreasing whenever beta becomes smaller.",
        "is_the_paper_exact_quantifier": False,
        "counterexample": "beta=-0.5 has lower reported IS than beta=-0.3 in all four settings",
        "counterexample_detected": all(
            smaller < larger
            for smaller, larger in zip(
                candidates[0]["evidence"]["beta_minus_point5"],
                candidates[0]["evidence"]["beta_minus_point3"],
            )
        ),
    }
    valid_candidates = [
        candidate["name"]
        for candidate in candidates
        if candidate["gan_domain_satisfied"]
        and candidate["all_required_joint_gradient_and_is_evidence_present"]
        and candidate["contradicts_exact_tendency_quantifier"]
    ]
    payload = {
        "claim": 5,
        "route": 4,
        "route_name": "mandatory falsification",
        "exact_contract": exact_contract,
        "primary_sources": [
            {
                "name": "paper HTML",
                "sha256": "c7ebf813dc871eba1c0c93542fcf0a7d599c7c4d44a543a0000270ce48ae7998",
                "anchors": ["Section 5", "Appendix D", "Tables 1-2"],
            },
            {
                "name": "Improved Training of Wasserstein GANs",
                "arxiv": "1704.00028",
                "role": "framework reference, not proof of the target implementation",
            },
        ],
        "candidates": candidates,
        "universalized_negative_control": universalized_control,
        "valid_assumption_satisfying_counterexamples": valid_candidates,
        "falsification_established": bool(valid_candidates),
        "verdict": "FALSIFIED" if valid_candidates else "BLOCKED",
        "unblockers": [
            "author executable code and exact configurations",
            "raw per-run cumulative gradient and Inception Score data",
            "resolved fixed-beta setting for the rho sweep",
            "sufficient CPU budget for the independently calibrated full campaign",
        ],
    }
    (output_dir / "claim5_route4_falsification.json").write_text(
        json.dumps(payload, indent=2) + "\n"
    )
    return payload
