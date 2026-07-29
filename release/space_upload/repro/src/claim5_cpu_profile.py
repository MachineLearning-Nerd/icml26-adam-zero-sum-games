"""Route 3: CPU calibration for the unresolved full GAN campaign.

Synthetic tensors are intentional here: this script measures the cost of the
reported image shapes, batch size, architectures, WGAN-GP backward pass, and
parameter-gradient L1 statistic. It does not claim to reproduce GAN quality.
"""

from __future__ import annotations

import gc
import json
import math
import os
import time
from pathlib import Path

import torch
from torch import nn
from torch.nn import functional as F


BATCH_SIZE = 64
LATENT_DIM = 128
BASE_CHANNELS = 16
LEARNING_RATE = 2e-4
GRADIENT_PENALTY = 10.0
HORIZON_FROM_PUBLISHED_PLOTS = 16000
CONFIGURATIONS = 44  # 7 beta + 4 rho settings, across four architecture/dataset pairs.
SEED = 20260729


class CNNGenerator(nn.Module):
    def __init__(self, size: int):
        super().__init__()
        blocks = int(math.log2(size)) - 2
        channels = BASE_CHANNELS * 4
        self.fc = nn.Linear(LATENT_DIM, channels * 4 * 4)
        layers: list[nn.Module] = []
        for _ in range(blocks):
            next_channels = max(BASE_CHANNELS, channels // 2)
            layers.extend(
                [
                    nn.ConvTranspose2d(channels, next_channels, 4, 2, 1),
                    nn.BatchNorm2d(next_channels),
                    nn.ReLU(),
                ]
            )
            channels = next_channels
        layers.extend([nn.Conv2d(channels, 3, 3, 1, 1), nn.Tanh()])
        self.net = nn.Sequential(*layers)

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        return self.net(self.fc(z).reshape(z.shape[0], BASE_CHANNELS * 4, 4, 4))


class CNNDiscriminator(nn.Module):
    def __init__(self, size: int):
        super().__init__()
        blocks = int(math.log2(size)) - 2
        channels = BASE_CHANNELS
        layers: list[nn.Module] = [nn.Conv2d(3, channels, 3, 1, 1), nn.LeakyReLU(0.2)]
        for _ in range(blocks):
            next_channels = min(BASE_CHANNELS * 4, channels * 2)
            layers.extend(
                [
                    nn.Conv2d(channels, next_channels, 4, 2, 1),
                    nn.LeakyReLU(0.2),
                ]
            )
            channels = next_channels
        self.net = nn.Sequential(*layers)
        self.head = nn.Linear(channels * 4 * 4, 1)

    def forward(self, image: torch.Tensor) -> torch.Tensor:
        features = self.net(image)
        return self.head(features.flatten(1)).flatten()


class ResUp(nn.Module):
    def __init__(self, input_channels: int, output_channels: int):
        super().__init__()
        self.conv1 = nn.Conv2d(input_channels, output_channels, 3, 1, 1)
        self.conv2 = nn.Conv2d(output_channels, output_channels, 3, 1, 1)
        self.skip = nn.Conv2d(input_channels, output_channels, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = self.skip(F.interpolate(x, scale_factor=2, mode="nearest"))
        x = F.interpolate(x, scale_factor=2, mode="nearest")
        x = self.conv1(F.relu(x))
        return residual + self.conv2(F.relu(x))


class ResDown(nn.Module):
    def __init__(self, input_channels: int, output_channels: int):
        super().__init__()
        self.conv1 = nn.Conv2d(input_channels, output_channels, 3, 1, 1)
        self.conv2 = nn.Conv2d(output_channels, output_channels, 3, 1, 1)
        self.skip = nn.Conv2d(input_channels, output_channels, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = F.avg_pool2d(self.skip(x), 2)
        x = self.conv1(F.leaky_relu(x, 0.2))
        x = self.conv2(F.leaky_relu(x, 0.2))
        return residual + F.avg_pool2d(x, 2)


class ResGenerator(nn.Module):
    def __init__(self, size: int):
        super().__init__()
        blocks = int(math.log2(size)) - 2
        channels = BASE_CHANNELS * 4
        self.fc = nn.Linear(LATENT_DIM, channels * 4 * 4)
        layers: list[nn.Module] = []
        for _ in range(blocks):
            next_channels = max(BASE_CHANNELS, channels // 2)
            layers.append(ResUp(channels, next_channels))
            channels = next_channels
        self.blocks = nn.Sequential(*layers)
        self.final = nn.Conv2d(channels, 3, 3, 1, 1)

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        x = self.fc(z).reshape(z.shape[0], BASE_CHANNELS * 4, 4, 4)
        return torch.tanh(self.final(F.relu(self.blocks(x))))


class ResDiscriminator(nn.Module):
    def __init__(self, size: int):
        super().__init__()
        blocks = int(math.log2(size)) - 2
        channels = BASE_CHANNELS
        self.initial = nn.Conv2d(3, channels, 3, 1, 1)
        layers: list[nn.Module] = []
        for _ in range(blocks):
            next_channels = min(BASE_CHANNELS * 4, channels * 2)
            layers.append(ResDown(channels, next_channels))
            channels = next_channels
        self.blocks = nn.Sequential(*layers)
        self.head = nn.Linear(channels * 4 * 4, 1)

    def forward(self, image: torch.Tensor) -> torch.Tensor:
        features = F.leaky_relu(self.blocks(self.initial(image)), 0.2)
        return self.head(features.flatten(1)).flatten()


def parameter_gradient_l1(module: nn.Module) -> float:
    return float(
        sum(
            parameter.grad.detach().abs().sum()
            for parameter in module.parameters()
            if parameter.grad is not None
        )
    )


def make_models(architecture: str, size: int) -> tuple[nn.Module, nn.Module]:
    if architecture == "CNN":
        return CNNGenerator(size), CNNDiscriminator(size)
    return ResGenerator(size), ResDiscriminator(size)


def joint_training_step(
    generator: nn.Module,
    discriminator: nn.Module,
    generator_optimizer: torch.optim.Optimizer,
    discriminator_optimizer: torch.optim.Optimizer,
    size: int,
) -> float:
    real = torch.rand(BATCH_SIZE, 3, size, size) * 2.0 - 1.0
    z = torch.randn(BATCH_SIZE, LATENT_DIM)
    with torch.no_grad():
        fake = generator(z)
    discriminator_optimizer.zero_grad(set_to_none=True)
    real_score = discriminator(real)
    fake_score = discriminator(fake)
    alpha = torch.rand(BATCH_SIZE, 1, 1, 1)
    interpolated = (alpha * real + (1.0 - alpha) * fake).requires_grad_(True)
    interpolated_score = discriminator(interpolated)
    input_gradient = torch.autograd.grad(
        interpolated_score.sum(), interpolated, create_graph=True
    )[0]
    penalty = (
        input_gradient.flatten(1).norm(2, dim=1).sub(1.0).square().mean()
        * GRADIENT_PENALTY
    )
    discriminator_loss = fake_score.mean() - real_score.mean() + penalty
    discriminator_loss.backward()
    discriminator_gradient = parameter_gradient_l1(discriminator)
    discriminator_optimizer.step()

    generator_optimizer.zero_grad(set_to_none=True)
    generated = generator(torch.randn(BATCH_SIZE, LATENT_DIM))
    generator_loss = -discriminator(generated).mean()
    generator_loss.backward()
    generator_gradient = parameter_gradient_l1(generator)
    generator_optimizer.step()
    return discriminator_gradient + generator_gradient


def cgroup_quota() -> tuple[str | None, int]:
    path = Path("/sys/fs/cgroup/cpu.max")
    raw = path.read_text().strip() if path.exists() else None
    if raw and not raw.startswith("max"):
        quota, period = map(int, raw.split())
        return raw, max(1, quota // period)
    return raw, min(8, os.cpu_count() or 1)


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_quota, allocated_cores = cgroup_quota()
    torch.set_num_threads(allocated_cores)
    torch.set_num_interop_threads(1)
    torch.manual_seed(SEED)
    profiles: list[dict[str, object]] = []
    for architecture, dataset, size in (
        ("CNN", "CIFAR-10", 32),
        ("CNN", "STL-10", 64),
        ("ResNet", "CIFAR-10", 32),
        ("ResNet", "STL-10", 64),
    ):
        generator, discriminator = make_models(architecture, size)
        generator_optimizer = torch.optim.Adam(
            generator.parameters(), lr=LEARNING_RATE, betas=(0.0, 0.9)
        )
        discriminator_optimizer = torch.optim.Adam(
            discriminator.parameters(), lr=LEARNING_RATE, betas=(0.0, 0.9)
        )

        with torch.inference_mode():
            started = time.perf_counter()
            for _ in range(3):
                discriminator(generator(torch.randn(BATCH_SIZE, LATENT_DIM)))
            forward_seconds = (time.perf_counter() - started) / 3.0

        joint_training_step(
            generator, discriminator, generator_optimizer, discriminator_optimizer, size
        )
        measured_seconds: list[float] = []
        gradient_l1: list[float] = []
        for _ in range(2):
            started = time.perf_counter()
            gradient_l1.append(
                joint_training_step(
                    generator,
                    discriminator,
                    generator_optimizer,
                    discriminator_optimizer,
                    size,
                )
            )
            measured_seconds.append(time.perf_counter() - started)
        seconds_per_step = sum(measured_seconds) / len(measured_seconds)
        profiles.append(
            {
                "architecture": architecture,
                "dataset_shape": dataset,
                "resolution": size,
                "batch_size": BATCH_SIZE,
                "base_channels": BASE_CHANNELS,
                "forward_only_seconds": forward_seconds,
                "joint_wgan_gp_seconds": seconds_per_step,
                "measured_step_seconds": measured_seconds,
                "parameter_gradient_l1": gradient_l1,
                "single_configuration_16000_step_hours": (
                    seconds_per_step * HORIZON_FROM_PUBLISHED_PLOTS / 3600.0
                ),
            }
        )
        del generator, discriminator, generator_optimizer, discriminator_optimizer
        gc.collect()

    total_hours_one_seed = sum(
        profile["single_configuration_16000_step_hours"] * 11 for profile in profiles
    )
    payload = {
        "claim": 5,
        "route": 3,
        "route_name": "full-shape CPU feasibility calibration",
        "profile_scope": (
            "Synthetic images; full reported resolutions and batch size; CNN and "
            "ResNet; WGAN-GP backward; parameter-gradient L1 measurement."
        ),
        "not_claim_evidence": True,
        "assumed_training_design": {
            "joint_critic_generator_ratio": "1:1 lower-cost calibration",
            "gradient_penalty": GRADIENT_PENALTY,
            "latent_dim": LATENT_DIM,
            "base_channels": BASE_CHANNELS,
            "optimizer_betas": [0.0, 0.9],
            "learning_rate": LEARNING_RATE,
            "published_plot_horizon": HORIZON_FROM_PUBLISHED_PLOTS,
            "configuration_count": CONFIGURATIONS,
        },
        "cpu": {
            "estimated_required_cores": 8,
            "selected_backend": "hf",
            "selected_flavor": "cpu-upgrade",
            "cgroup_cpu_max": raw_quota,
            "actual_quota_cores": allocated_cores,
            "torch_threads": torch.get_num_threads(),
        },
        "profiles": profiles,
        "projected_hours_one_seed_44_configs": total_hours_one_seed,
        "projected_hours_three_seeds_44_configs": total_hours_one_seed * 3.0,
        "projection_excludes": [
            "dataset input pipeline",
            "Inception Score generation and evaluation",
            "additional critic updates",
            "uncertainty from the undisclosed architecture",
        ],
        "verdict": "BLOCKED",
    }
    (output_dir / "claim5_route3_cpu_profile.json").write_text(
        json.dumps(payload, indent=2) + "\n"
    )
    return payload
