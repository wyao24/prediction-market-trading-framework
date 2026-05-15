from __future__ import annotations

from prediction_market_trading.config.settings import ExperimentConfig, default_experiment_config
from prediction_market_trading.state.models import (
    DecisionState,
    DecisionType,
    EventPhase,
    MarketState,
    PriceRegion,
    ProcessState,
    SignalState,
)


def generate_decision(
    market_state: MarketState,
    signal_state: SignalState,
    process_state: ProcessState,
    config: ExperimentConfig | None = None,
) -> DecisionState:
    cfg = config or default_experiment_config()
    thresholds = cfg.thresholds

    reason_codes: list[str] = []
    cps = signal_state.crowd_pressure_score
    acs = signal_state.agent_credibility_score
    oi = signal_state.overreaction_indicator
    persistence = signal_state.persistence

    if cps >= thresholds.cps_high:
        reason_codes.append("HIGH_CPS")
    if acs <= thresholds.acs_low:
        reason_codes.append("LOW_ACS")
    if acs >= thresholds.acs_high:
        reason_codes.append("HIGH_ACS")
    if oi >= thresholds.oi_high:
        reason_codes.append("OVERREACTION_PRESENT")
    if persistence >= thresholds.persistence_confirmed:
        reason_codes.append("PERSISTENCE_CONFIRMED")
    if signal_state.liquidity_thinness >= thresholds.thin_liquidity:
        reason_codes.append("THIN_LIQUIDITY")
    if market_state.event_phase == EventPhase.LIVE:
        reason_codes.append("LIVE_EVENT_PHASE")
    if market_state.price_region in {PriceRegion.NEAR_LOW, PriceRegion.EXTREME_LOW}:
        reason_codes.append("EXTREME_LOW_PRICE")
    if market_state.price_region in {PriceRegion.NEAR_HIGH, PriceRegion.EXTREME_HIGH}:
        reason_codes.append("EXTREME_HIGH_PRICE")

    conflicting_signals = cps >= thresholds.cps_high and acs >= thresholds.acs_high and oi < thresholds.oi_high
    boundary_low = market_state.price_region in {PriceRegion.NEAR_LOW, PriceRegion.EXTREME_LOW}
    boundary_high = market_state.price_region in {PriceRegion.NEAR_HIGH, PriceRegion.EXTREME_HIGH}

    if conflicting_signals:
        reason_codes.append("CONFLICTING_SIGNALS")
        decision = DecisionType.WATCH
    elif boundary_low and acs <= thresholds.acs_low and (oi >= thresholds.oi_high or cps >= thresholds.cps_medium):
        decision = DecisionType.BOUNDARY_FADE
    elif boundary_high and acs >= thresholds.acs_high and persistence >= thresholds.persistence_confirmed:
        decision = DecisionType.BOUNDARY_FOLLOW
    elif cps >= thresholds.cps_high and oi >= thresholds.oi_high and acs <= thresholds.acs_low:
        decision = DecisionType.FADE
    elif acs >= thresholds.acs_high and persistence >= thresholds.persistence_confirmed:
        decision = DecisionType.FOLLOW
    elif market_state.event_phase == EventPhase.LIVE and acs < thresholds.acs_high:
        decision = DecisionType.WATCH
    elif process_state.dominant_process.value == "unclear":
        decision = DecisionType.NO_TRADE
    elif cps >= thresholds.cps_medium or acs >= thresholds.acs_medium:
        decision = DecisionType.WATCH
    else:
        decision = DecisionType.NO_TRADE

    return DecisionState(
        market_id=market_state.market_id,
        timestamp=market_state.timestamp,
        decision_type=decision,
        reason_codes=reason_codes,
        intended_horizon="fast" if decision in {DecisionType.FADE, DecisionType.BOUNDARY_FADE} else "mid",
        strategy_quality_score=cfg.default_strategy_quality,
    )

