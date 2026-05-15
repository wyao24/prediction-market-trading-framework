from __future__ import annotations

from collections.abc import Mapping

import numpy as np

from prediction_market_trading.config.settings import ScoreWeights


def _clip(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return float(np.clip(value, lower, upper))


def _weighted_average(values: Mapping[str, float], weights: Mapping[str, float]) -> float:
    numerator = 0.0
    denominator = 0.0
    for key, weight in weights.items():
        numerator += values.get(key, 0.0) * weight
        denominator += weight
    if denominator == 0.0:
        return 0.0
    return _clip(numerator / denominator)


def compute_crowd_pressure_score(
    order_flow_imbalance: float,
    trade_aggression: float,
    liquidity_thinness: float,
    price_acceleration: float,
    weights: ScoreWeights | None = None,
) -> float:
    config = weights or ScoreWeights()
    values = {
        "order_flow_imbalance": abs(order_flow_imbalance),
        "trade_aggression": trade_aggression,
        "liquidity_thinness": liquidity_thinness,
        "price_acceleration": abs(price_acceleration),
    }
    return _weighted_average(values, config.crowd_pressure)


def compute_agent_credibility_score(
    wallet_timing: float,
    wallet_trade_size: float,
    market_depth: float,
    wallet_concentration: float,
    specialization_score: float,
    persistence_score: float,
    consistency_score: float = 0.50,
    weights: ScoreWeights | None = None,
) -> float:
    config = weights or ScoreWeights()
    size_relative_to_depth = _clip(wallet_trade_size / max(market_depth, 1e-9))
    values = {
        "timing": _clip(wallet_timing),
        "size_relative_to_depth": size_relative_to_depth,
        "wallet_concentration": _clip(wallet_concentration),
        "specialization": _clip(specialization_score),
        "persistence": _clip(persistence_score),
        "consistency": _clip(consistency_score),
    }
    return _weighted_average(values, config.agent_credibility)


def compute_overreaction_indicator(
    price_change: float,
    liquidity_thinness: float,
    agent_credibility_score: float,
    persistence_score: float,
    weights: ScoreWeights | None = None,
) -> float:
    config = weights or ScoreWeights()
    normalized_move = _clip(abs(price_change) / 0.15)
    values = {
        "price_change": normalized_move,
        "liquidity_thinness": _clip(liquidity_thinness),
        "weak_agent_confirmation": 1.0 - _clip(agent_credibility_score),
        "lack_of_persistence": 1.0 - _clip(persistence_score),
    }
    return _weighted_average(values, config.overreaction)


def compute_new_wallet_behavior_score(
    activity_burst: float,
    directional_commitment: float,
    timing_score: float,
) -> float:
    values = {
        "activity_burst": _clip(activity_burst),
        "directional_commitment": _clip(directional_commitment),
        "timing_score": _clip(timing_score),
    }
    weights = {
        "activity_burst": 0.4,
        "directional_commitment": 0.35,
        "timing_score": 0.25,
    }
    return _weighted_average(values, weights)


def compute_strategy_quality_score(
    expected_value: float,
    hit_rate: float,
    max_drawdown: float,
    sample_size: int,
) -> float:
    # Placeholder SQS logic for early experiments. This is intentionally simple
    # and should be replaced once replay results accumulate.
    ev_score = _clip((expected_value + 0.10) / 0.20)
    hit_rate_score = _clip(hit_rate)
    drawdown_penalty = _clip(1.0 - max_drawdown)
    sample_confidence = _clip(sample_size / 100.0)
    composite = (
        (0.40 * ev_score)
        + (0.20 * hit_rate_score)
        + (0.20 * drawdown_penalty)
        + (0.20 * sample_confidence)
    )
    return _clip(composite)

