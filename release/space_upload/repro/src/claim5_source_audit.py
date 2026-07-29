"""Route 1: machine-readable completeness audit of the paper's GAN experiment."""

from __future__ import annotations

import json
from pathlib import Path


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    disclosed = {
        "datasets": ["CIFAR-10 32x32", "STL-10 64x64"],
        "architectures": ["ResNet", "CNN"],
        "framework": "generally follows improved Wasserstein GAN",
        "optimizer": "simultaneous Adam-DA for generator and discriminator",
        "learning_rate": 0.0002,
        "batch_size": 64,
        "beta_sweep_fixed_rho": 0.9,
        "rho_sweep_fixed_beta": 0.0,
        "rho_values_from_table_2": [0.3, 0.5, 0.7, 0.9],
        "metric": "cumulative average parameter-gradient L1 norm and Inception Score",
    }
    required_reproduction_fields = {
        "executable_author_code": False,
        "exact_resnet_definition": False,
        "exact_cnn_definition": False,
        "dataset_split_and_preprocessing": False,
        "latent_distribution_and_dimension": False,
        "critic_to_generator_update_ratio": False,
        "gradient_penalty_coefficient": False,
        "adam_epsilon": False,
        "training_seeds": False,
        "main_experiment_training_horizon": False,
        "inception_implementation_and_sample_count": False,
        "raw_gradient_norm_timeseries": False,
        "per_seed_inception_scores": False,
    }
    payload = {
        "claim": 5,
        "route": 1,
        "route_name": "source completeness audit",
        "source": {
            "ar5iv_url": "https://ar5iv.labs.arxiv.org/html/2605.19392",
            "retrieval_date_utc": "2026-07-29",
            "html_sha256": "c7ebf813dc871eba1c0c93542fcf0a7d599c7c4d44a543a0000270ce48ae7998",
            "source_tar_sha256": "9922a66ab5708f357aa8be09f207565791a6488f48b0d8d2cf27011964521265",
            "anchors": [
                "Section 5 Experimental Setting and Results",
                "Appendix D / Additional Materials for Section 5",
                "Table 1",
                "Table 2",
            ],
        },
        "disclosed": disclosed,
        "required_reproduction_fields": required_reproduction_fields,
        "missing_critical_field_count": sum(not value for value in required_reproduction_fields.values()),
        "author_source_uniquely_executable": all(required_reproduction_fields.values()),
        "verdict": "BLOCKED",
        "reason": (
            "The source fixes the headline setting but does not identify a unique "
            "architecture, training process, seed distribution, or IS evaluator."
        ),
    }
    (output_dir / "claim5_route1_source_audit.json").write_text(
        json.dumps(payload, indent=2) + "\n"
    )
    return payload
