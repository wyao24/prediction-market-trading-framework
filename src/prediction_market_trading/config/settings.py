from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScoreWeights:
    """Initial experimental weights derived from the research docs.

    These weights are intentionally simple heuristics. They are not validated and
    should be treated as transparent defaults for early replay experiments.
    """

    crowd_pressure: dict[str, float] = field(
        default_factory=lambda: {
            "order_flow_imbalance": 0.35,
            "trade_aggression": 0.25,
            "liquidity_thinness": 0.20,
            "price_acceleration": 0.20,
        }
    )
    agent_credibility: dict[str, float] = field(
        default_factory=lambda: {
            "timing": 0.25,
            "size_relative_to_depth": 0.20,
            "wallet_concentration": 0.20,
            "specialization": 0.15,
            "persistence": 0.15,
            "consistency": 0.05,
        }
    )
    overreaction: dict[str, float] = field(
        default_factory=lambda: {
            "price_change": 0.35,
            "liquidity_thinness": 0.25,
            "weak_agent_confirmation": 0.20,
            "lack_of_persistence": 0.20,
        }
    )


@dataclass(frozen=True)
class ThresholdConfig:
    boundary_low: float = 0.10
    extreme_low: float = 0.05
    boundary_high: float = 0.90
    extreme_high: float = 0.95

    cps_medium: float = 0.50
    cps_high: float = 0.65
    acs_medium: float = 0.50
    acs_low: float = 0.35
    acs_high: float = 0.65
    oi_high: float = 0.60
    persistence_confirmed: float = 0.60
    thin_liquidity: float = 0.60

    max_trade_fraction: float = 0.10
    max_total_exposure: float = 0.35
    max_event_exposure: float = 0.20

    replay_horizon_steps: int = 3


@dataclass(frozen=True)
class ExperimentConfig:
    score_weights: ScoreWeights = field(default_factory=ScoreWeights)
    thresholds: ThresholdConfig = field(default_factory=ThresholdConfig)
    starting_capital: float = 10_000.0
    default_strategy_quality: float = 0.50
    save_outputs: bool = True


def default_experiment_config() -> ExperimentConfig:
    return ExperimentConfig()

