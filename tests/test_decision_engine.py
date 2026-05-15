from datetime import datetime

from prediction_market_trading.decision.engine import generate_decision
from prediction_market_trading.state.models import (
    DecisionType,
    DominantProcess,
    EventPhase,
    MarketCategory,
    MarketState,
    PriceRegion,
    ProcessState,
    SignalState,
)


def _market_state(price_region: PriceRegion = PriceRegion.INTERIOR) -> MarketState:
    return MarketState(
        market_id="market-1",
        timestamp=datetime(2026, 1, 1, 9, 0, 0),
        mid_price=0.50,
        spread=0.02,
        depth=200.0,
        recent_volume=100.0,
        event_phase=EventPhase.PRE_EVENT,
        market_category=MarketCategory.MIXED,
        price_region=price_region,
    )


def _process_state(dominant: DominantProcess) -> ProcessState:
    return ProcessState(
        dominant_process=dominant,
        crowd_score=0.0,
        agent_score=0.0,
        boundary_score=0.0,
        boundary_active=dominant == DominantProcess.BOUNDARY,
        explanation=[],
    )


def test_high_cps_high_oi_low_acs_produces_fade() -> None:
    decision = generate_decision(
        _market_state(),
        SignalState(
            order_flow_imbalance=0.8,
            trade_aggression=0.9,
            liquidity_thinness=0.8,
            price_acceleration=0.8,
            wallet_concentration=0.2,
            persistence=0.2,
            crowd_pressure_score=0.85,
            agent_credibility_score=0.20,
            overreaction_indicator=0.90,
        ),
        _process_state(DominantProcess.CROWD),
    )
    assert decision.decision_type == DecisionType.FADE


def test_high_acs_and_persistence_produces_follow() -> None:
    decision = generate_decision(
        _market_state(),
        SignalState(
            order_flow_imbalance=0.2,
            trade_aggression=0.3,
            liquidity_thinness=0.2,
            price_acceleration=0.3,
            wallet_concentration=0.8,
            persistence=0.9,
            crowd_pressure_score=0.25,
            agent_credibility_score=0.88,
            overreaction_indicator=0.20,
        ),
        _process_state(DominantProcess.AGENT),
    )
    assert decision.decision_type == DecisionType.FOLLOW


def test_extreme_low_price_with_low_acs_produces_boundary_fade() -> None:
    market_state = _market_state(price_region=PriceRegion.EXTREME_LOW)
    market_state.mid_price = 0.04
    decision = generate_decision(
        market_state,
        SignalState(
            order_flow_imbalance=0.7,
            trade_aggression=0.8,
            liquidity_thinness=0.9,
            price_acceleration=0.7,
            wallet_concentration=0.2,
            persistence=0.2,
            crowd_pressure_score=0.75,
            agent_credibility_score=0.18,
            overreaction_indicator=0.78,
        ),
        _process_state(DominantProcess.BOUNDARY),
    )
    assert decision.decision_type == DecisionType.BOUNDARY_FADE


def test_conflicting_signals_produce_watch() -> None:
    decision = generate_decision(
        _market_state(),
        SignalState(
            order_flow_imbalance=0.7,
            trade_aggression=0.8,
            liquidity_thinness=0.4,
            price_acceleration=0.6,
            wallet_concentration=0.8,
            persistence=0.8,
            crowd_pressure_score=0.75,
            agent_credibility_score=0.80,
            overreaction_indicator=0.25,
        ),
        _process_state(DominantProcess.MIXED),
    )
    assert decision.decision_type in {DecisionType.WATCH, DecisionType.NO_TRADE}

