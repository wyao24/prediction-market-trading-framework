from __future__ import annotations

from dataclasses import replace

from prediction_market_trading.state.models import (
    DecisionState,
    DecisionType,
    LifecyclePhase,
    MarketState,
    PriceRegion,
    TradeState,
)


def _mark_to_market(trade_state: TradeState, latest_price: float) -> TradeState:
    if trade_state.entry_price is None:
        return replace(trade_state, current_price=latest_price)
    raw_return = trade_state.direction * (latest_price - trade_state.entry_price)
    pnl = trade_state.size * raw_return
    return replace(
        trade_state,
        current_price=latest_price,
        pnl=pnl,
        return_pct=raw_return,
    )


def _infer_direction(decision_type: DecisionType, market_state: MarketState) -> int:
    if decision_type == DecisionType.BOUNDARY_FADE:
        if market_state.price_region in {PriceRegion.NEAR_LOW, PriceRegion.EXTREME_LOW}:
            return 1
        return -1
    if decision_type == DecisionType.BOUNDARY_FOLLOW:
        if market_state.price_region in {PriceRegion.NEAR_HIGH, PriceRegion.EXTREME_HIGH}:
            return 1
        return 1 if market_state.price_change >= 0 else -1
    if decision_type == DecisionType.FOLLOW:
        return 1 if market_state.price_change >= 0 else -1
    return -1 if market_state.price_change >= 0 else 1


def setup_trade(
    trade_id: str,
    decision_state: DecisionState,
    market_state: MarketState,
    size: float,
) -> TradeState:
    return TradeState(
        trade_id=trade_id,
        market_id=market_state.market_id,
        timestamp=market_state.timestamp,
        decision_type=decision_state.decision_type,
        strategy_type=decision_state.decision_type.value,
        lifecycle_phase=LifecyclePhase.SETUP,
        direction=_infer_direction(decision_state.decision_type, market_state),
        size=size,
        intended_horizon=decision_state.intended_horizon,
        event_phase=market_state.event_phase,
        price_region=market_state.price_region,
        reason_codes=list(decision_state.reason_codes),
    )


def enter_trade(trade_state: TradeState, market_state: MarketState) -> TradeState:
    return replace(
        trade_state,
        timestamp=market_state.timestamp,
        entry_price=market_state.mid_price,
        current_price=market_state.mid_price,
        lifecycle_phase=LifecyclePhase.ENTRY,
    )


def validate_trade(trade_state: TradeState, market_state: MarketState) -> TradeState:
    updated = _mark_to_market(trade_state, market_state.mid_price)
    favorable_move = (market_state.mid_price - (trade_state.entry_price or market_state.mid_price)) * trade_state.direction > 0
    phase = LifecyclePhase.VALIDATION if favorable_move else LifecyclePhase.INVALIDATION
    status = "open" if favorable_move else "closed"
    return replace(
        updated,
        timestamp=market_state.timestamp,
        lifecycle_phase=phase,
        bars_held=trade_state.bars_held + 1,
        status=status,
        exit_price=market_state.mid_price if not favorable_move else trade_state.exit_price,
    )


def scale_trade(trade_state: TradeState, size_increment: float, market_state: MarketState) -> TradeState:
    updated = _mark_to_market(trade_state, market_state.mid_price)
    return replace(
        updated,
        timestamp=market_state.timestamp,
        lifecycle_phase=LifecyclePhase.SCALE,
        size=trade_state.size + size_increment,
        bars_held=trade_state.bars_held + 1,
    )


def exit_trade(trade_state: TradeState, market_state: MarketState) -> TradeState:
    updated = _mark_to_market(trade_state, market_state.mid_price)
    return replace(
        updated,
        timestamp=market_state.timestamp,
        lifecycle_phase=LifecyclePhase.EXIT,
        exit_price=market_state.mid_price,
        bars_held=trade_state.bars_held + 1,
        status="closed",
    )


def invalidate_trade(trade_state: TradeState, market_state: MarketState) -> TradeState:
    updated = _mark_to_market(trade_state, market_state.mid_price)
    return replace(
        updated,
        timestamp=market_state.timestamp,
        lifecycle_phase=LifecyclePhase.INVALIDATION,
        exit_price=market_state.mid_price,
        bars_held=trade_state.bars_held + 1,
        status="closed",
    )


def transition_trade_state(
    trade_state: TradeState,
    market_state: MarketState,
    latest_decision: DecisionState,
) -> TradeState:
    if latest_decision.decision_type == DecisionType.EXIT:
        return exit_trade(trade_state, market_state)

    if trade_state.lifecycle_phase == LifecyclePhase.ENTRY:
        return validate_trade(trade_state, market_state)

    if latest_decision.decision_type in {DecisionType.FOLLOW, DecisionType.BOUNDARY_FOLLOW, DecisionType.FADE, DecisionType.BOUNDARY_FADE}:
        favorable = (market_state.mid_price - (trade_state.entry_price or market_state.mid_price)) * trade_state.direction > 0
        if favorable and trade_state.lifecycle_phase == LifecyclePhase.VALIDATION:
            return scale_trade(trade_state, size_increment=trade_state.size * 0.25, market_state=market_state)
        if not favorable:
            return invalidate_trade(trade_state, market_state)

    return _mark_to_market(
        replace(trade_state, timestamp=market_state.timestamp, bars_held=trade_state.bars_held + 1),
        market_state.mid_price,
    )

