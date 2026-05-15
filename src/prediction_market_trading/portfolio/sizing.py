from __future__ import annotations

import numpy as np

from prediction_market_trading.state.models import DecisionType


def _clip(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return float(np.clip(value, lower, upper))


def determine_edge_level(
    decision_type: DecisionType,
    crowd_pressure_score: float,
    agent_credibility_score: float,
    overreaction_indicator: float,
    persistence: float,
) -> str:
    if decision_type in {DecisionType.NO_TRADE, DecisionType.WATCH, DecisionType.EXIT, DecisionType.REDUCE}:
        return "none"

    if decision_type in {DecisionType.FADE, DecisionType.BOUNDARY_FADE}:
        conviction = (0.5 * crowd_pressure_score) + (0.5 * overreaction_indicator)
    else:
        conviction = (0.65 * agent_credibility_score) + (0.35 * persistence)

    if conviction >= 0.80:
        return "very_strong"
    if conviction >= 0.65:
        return "strong"
    if conviction >= 0.50:
        return "medium"
    return "weak"


def determine_position_size(
    edge_level: str,
    strategy_quality_score: float,
    capital: float,
    max_trade_fraction: float = 0.10,
) -> float:
    base_fraction_by_edge = {
        "none": 0.00,
        "weak": 0.01,
        "medium": 0.03,
        "strong": 0.06,
        "very_strong": 0.10,
    }
    base_fraction = base_fraction_by_edge.get(edge_level, 0.00)
    scaled_fraction = base_fraction * _clip(strategy_quality_score)
    return min(capital * scaled_fraction, capital * max_trade_fraction)


def enforce_risk_caps(
    proposed_size: float,
    current_exposure: float,
    capital: float,
    max_trade_fraction: float,
    max_total_exposure: float,
    event_exposure: float = 0.0,
    max_event_exposure: float = 0.20,
) -> float:
    trade_cap = capital * max_trade_fraction
    total_cap = max((capital * max_total_exposure) - current_exposure, 0.0)
    event_cap = max((capital * max_event_exposure) - event_exposure, 0.0)
    return max(0.0, min(proposed_size, trade_cap, total_cap, event_cap))


def fractional_kelly_position_size(*_args: object, **_kwargs: object) -> float:
    raise NotImplementedError("Fractional Kelly sizing is intentionally deferred in this scaffold.")

