from __future__ import annotations

import numpy as np

from prediction_market_trading.state.models import (
    DominantProcess,
    MarketState,
    PriceRegion,
    ProcessState,
    SignalState,
)


def _clip(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return float(np.clip(value, lower, upper))


def infer_crowd_process(
    crowd_pressure_score: float,
    overreaction_indicator: float,
    agent_credibility_score: float,
) -> float:
    return _clip(
        (0.55 * crowd_pressure_score)
        + (0.30 * overreaction_indicator)
        + (0.15 * (1.0 - agent_credibility_score))
    )


def infer_agent_process(
    agent_credibility_score: float,
    persistence: float,
    wallet_concentration: float,
    overreaction_indicator: float,
) -> float:
    return _clip(
        (0.50 * agent_credibility_score)
        + (0.25 * persistence)
        + (0.20 * wallet_concentration)
        + (0.05 * (1.0 - overreaction_indicator))
    )


def infer_boundary_process(
    price_region: PriceRegion,
    crowd_pressure_score: float,
    agent_credibility_score: float,
) -> float:
    if price_region == PriceRegion.INTERIOR:
        return 0.0
    if price_region in {PriceRegion.EXTREME_LOW, PriceRegion.EXTREME_HIGH}:
        base = 0.80
    else:
        base = 0.60
    signal_alignment = max(crowd_pressure_score, agent_credibility_score)
    return _clip((0.70 * base) + (0.30 * signal_alignment))


def infer_dominant_process(
    market_state: MarketState,
    signal_state: SignalState,
) -> ProcessState:
    crowd_score = infer_crowd_process(
        crowd_pressure_score=signal_state.crowd_pressure_score,
        overreaction_indicator=signal_state.overreaction_indicator,
        agent_credibility_score=signal_state.agent_credibility_score,
    )
    agent_score = infer_agent_process(
        agent_credibility_score=signal_state.agent_credibility_score,
        persistence=signal_state.persistence,
        wallet_concentration=signal_state.wallet_concentration,
        overreaction_indicator=signal_state.overreaction_indicator,
    )
    boundary_score = infer_boundary_process(
        price_region=market_state.price_region,
        crowd_pressure_score=signal_state.crowd_pressure_score,
        agent_credibility_score=signal_state.agent_credibility_score,
    )

    scores = {
        DominantProcess.CROWD: crowd_score,
        DominantProcess.AGENT: agent_score,
        DominantProcess.BOUNDARY: boundary_score,
    }
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_process, top_score = sorted_scores[0]
    second_process, second_score = sorted_scores[1]

    if top_score < 0.45:
        dominant = DominantProcess.UNCLEAR
    elif abs(top_score - second_score) <= 0.10 and second_score >= 0.50:
        dominant = DominantProcess.MIXED
    else:
        dominant = top_process

    explanation = [
        f"crowd_score={crowd_score:.2f}",
        f"agent_score={agent_score:.2f}",
        f"boundary_score={boundary_score:.2f}",
    ]
    if dominant == DominantProcess.MIXED:
        explanation.append(
            f"mixed_between={top_process.value}_{second_process.value}"
        )

    return ProcessState(
        dominant_process=dominant,
        crowd_score=crowd_score,
        agent_score=agent_score,
        boundary_score=boundary_score,
        boundary_active=market_state.price_region != PriceRegion.INTERIOR,
        explanation=explanation,
    )

