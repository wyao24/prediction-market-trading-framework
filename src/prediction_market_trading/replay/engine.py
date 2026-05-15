from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import count

import pandas as pd

from prediction_market_trading.config.settings import ExperimentConfig, default_experiment_config
from prediction_market_trading.decision.engine import generate_decision
from prediction_market_trading.evaluation.metrics import strategy_context_grouping
from prediction_market_trading.inference.engine import infer_dominant_process
from prediction_market_trading.lifecycle.machine import (
    enter_trade,
    exit_trade,
    setup_trade,
    transition_trade_state,
)
from prediction_market_trading.portfolio.sizing import (
    determine_edge_level,
    determine_position_size,
    enforce_risk_caps,
)
from prediction_market_trading.scoring.rules import (
    compute_agent_credibility_score,
    compute_crowd_pressure_score,
    compute_overreaction_indicator,
)
from prediction_market_trading.signals.features import (
    classify_price_region,
    compute_liquidity_thinness,
    compute_order_flow_imbalance,
    compute_persistence,
    compute_price_acceleration,
    compute_trade_aggression,
    compute_wallet_concentration,
)
from prediction_market_trading.state.models import (
    DecisionState,
    DecisionType,
    EventPhase,
    MarketCategory,
    MarketState,
    PortfolioState,
    PriceRegion,
    SignalState,
)


@dataclass(slots=True)
class ReplayResult:
    decision_log: pd.DataFrame
    trades: pd.DataFrame
    evaluation_summary: pd.DataFrame


def _coerce_event_phase(value: object) -> EventPhase:
    if isinstance(value, EventPhase):
        return value
    return EventPhase(str(value))


def _coerce_market_category(value: object) -> MarketCategory:
    if isinstance(value, MarketCategory):
        return value
    return MarketCategory(str(value))


def _trade_to_row(trade_state: object, market_category: str) -> dict[str, object]:
    return {
        "trade_id": trade_state.trade_id,
        "market_id": trade_state.market_id,
        "strategy_type": trade_state.strategy_type,
        "decision_type": trade_state.decision_type.value,
        "event_phase": trade_state.event_phase.value,
        "market_category": market_category,
        "price_region": trade_state.price_region.value,
        "horizon": trade_state.intended_horizon,
        "entry_price": trade_state.entry_price,
        "exit_price": trade_state.exit_price,
        "size": trade_state.size,
        "pnl": trade_state.pnl,
        "return_pct": trade_state.return_pct,
        "bars_held": trade_state.bars_held,
        "status": trade_state.status,
    }


def run_replay(
    market_data: pd.DataFrame,
    config: ExperimentConfig | None = None,
    *,
    simulate_trades: bool = True,
) -> ReplayResult:
    cfg = config or default_experiment_config()
    data = market_data.copy().sort_values("timestamp").reset_index(drop=True)
    decision_rows: list[dict[str, object]] = []
    trade_rows: list[dict[str, object]] = []

    portfolio_state = PortfolioState(
        capital=cfg.starting_capital,
        available_capital=cfg.starting_capital,
        max_trade_fraction=cfg.thresholds.max_trade_fraction,
        max_total_exposure=cfg.thresholds.max_total_exposure,
        max_event_exposure=cfg.thresholds.max_event_exposure,
        strategy_quality_score=cfg.default_strategy_quality,
    )

    price_window: list[float] = []
    active_trade = None
    trade_counter = count(1)

    for row in data.itertuples(index=False):
        price_window.append(float(row.mid_price))
        recent_prices = price_window[-5:]
        price_change = float(getattr(row, "price_change", 0.0))
        if price_change == 0.0 and len(recent_prices) >= 2:
            price_change = recent_prices[-1] - recent_prices[-2]

        price_region = classify_price_region(
            float(row.mid_price),
            boundary_low=cfg.thresholds.boundary_low,
            extreme_low=cfg.thresholds.extreme_low,
            boundary_high=cfg.thresholds.boundary_high,
            extreme_high=cfg.thresholds.extreme_high,
        )
        order_flow_imbalance = compute_order_flow_imbalance(float(row.buy_volume), float(row.sell_volume))
        trade_aggression = compute_trade_aggression(float(row.aggressive_volume), float(row.recent_volume))
        liquidity_thinness = compute_liquidity_thinness(float(row.spread), float(row.depth))
        price_acceleration = compute_price_acceleration(recent_prices)

        if hasattr(row, "wallet_concentration") and row.wallet_concentration is not None:
            wallet_concentration = float(row.wallet_concentration)
        else:
            residual_volume = max(float(row.recent_volume) - float(row.wallet_trade_size), 0.0)
            wallet_concentration = compute_wallet_concentration([float(row.wallet_trade_size), residual_volume])

        if hasattr(row, "persistence_score") and row.persistence_score is not None:
            persistence = float(row.persistence_score)
        else:
            persistence = compute_persistence(recent_prices)

        market_state = MarketState(
            market_id=str(row.market_id),
            timestamp=pd.Timestamp(row.timestamp).to_pydatetime(),
            mid_price=float(row.mid_price),
            yes_price=float(getattr(row, "yes_price", row.mid_price)),
            no_price=float(getattr(row, "no_price", 1.0 - row.mid_price)),
            spread=float(row.spread),
            depth=float(row.depth),
            recent_volume=float(row.recent_volume),
            order_flow_imbalance=order_flow_imbalance,
            trade_aggression=trade_aggression,
            price_change=price_change,
            event_phase=_coerce_event_phase(getattr(row, "event_phase", EventPhase.PRE_EVENT.value)),
            market_category=_coerce_market_category(getattr(row, "market_category", MarketCategory.MIXED.value)),
            price_region=price_region,
        )

        cps = compute_crowd_pressure_score(
            order_flow_imbalance=order_flow_imbalance,
            trade_aggression=trade_aggression,
            liquidity_thinness=liquidity_thinness,
            price_acceleration=price_acceleration,
            weights=cfg.score_weights,
        )
        acs = compute_agent_credibility_score(
            wallet_timing=float(getattr(row, "timing_score", 0.0)),
            wallet_trade_size=float(getattr(row, "wallet_trade_size", 0.0)),
            market_depth=market_state.depth,
            wallet_concentration=wallet_concentration,
            specialization_score=float(getattr(row, "specialization_score", 0.0)),
            persistence_score=persistence,
            consistency_score=float(getattr(row, "consistency_score", persistence)),
            weights=cfg.score_weights,
        )
        oi = compute_overreaction_indicator(
            price_change=price_change,
            liquidity_thinness=liquidity_thinness,
            agent_credibility_score=acs,
            persistence_score=persistence,
            weights=cfg.score_weights,
        )

        signal_state = SignalState(
            order_flow_imbalance=order_flow_imbalance,
            trade_aggression=trade_aggression,
            liquidity_thinness=liquidity_thinness,
            price_acceleration=price_acceleration,
            wallet_concentration=wallet_concentration,
            persistence=persistence,
            crowd_pressure_score=cps,
            agent_credibility_score=acs,
            overreaction_indicator=oi,
        )

        process_state = infer_dominant_process(market_state, signal_state)
        decision_state = generate_decision(market_state, signal_state, process_state, cfg)
        edge_level = determine_edge_level(
            decision_state.decision_type,
            crowd_pressure_score=cps,
            agent_credibility_score=acs,
            overreaction_indicator=oi,
            persistence=persistence,
        )
        decision_state = replace(decision_state, edge_level=edge_level)
        proposed_size = determine_position_size(
            edge_level=edge_level,
            strategy_quality_score=portfolio_state.strategy_quality_score,
            capital=portfolio_state.available_capital,
            max_trade_fraction=portfolio_state.max_trade_fraction,
        )
        allowed_size = enforce_risk_caps(
            proposed_size=proposed_size,
            current_exposure=portfolio_state.current_exposure,
            capital=portfolio_state.capital,
            max_trade_fraction=portfolio_state.max_trade_fraction,
            max_total_exposure=portfolio_state.max_total_exposure,
            event_exposure=portfolio_state.event_exposure,
            max_event_exposure=portfolio_state.max_event_exposure,
        )

        decision_rows.append(
            {
                "timestamp": row.timestamp,
                "market_id": row.market_id,
                "scenario": getattr(row, "scenario", "unknown"),
                "mid_price": row.mid_price,
                "price_region": price_region.value,
                "event_phase": market_state.event_phase.value,
                "market_category": market_state.market_category.value,
                "cps": cps,
                "acs": acs,
                "oi": oi,
                "persistence": persistence,
                "dominant_process": process_state.dominant_process.value,
                "decision_type": decision_state.decision_type.value,
                "reason_codes": ",".join(decision_state.reason_codes),
                "edge_level": edge_level,
                "proposed_size": allowed_size,
            }
        )

        if not simulate_trades:
            continue

        if active_trade is None and decision_state.decision_type in {
            DecisionType.FADE,
            DecisionType.FOLLOW,
            DecisionType.BOUNDARY_FADE,
            DecisionType.BOUNDARY_FOLLOW,
        } and allowed_size > 0.0:
            active_trade = setup_trade(
                trade_id=f"trade-{next(trade_counter)}",
                decision_state=decision_state,
                market_state=market_state,
                size=allowed_size,
            )
            active_trade = enter_trade(active_trade, market_state)
            portfolio_state.current_exposure = allowed_size
            portfolio_state.event_exposure = allowed_size
            continue

        if active_trade is None:
            continue

        active_trade = transition_trade_state(active_trade, market_state, decision_state)

        if active_trade.bars_held >= cfg.thresholds.replay_horizon_steps and active_trade.status == "open":
            active_trade = exit_trade(active_trade, market_state)

        if active_trade.status == "closed":
            trade_rows.append(
                _trade_to_row(
                    active_trade,
                    market_category=market_state.market_category.value,
                )
            )
            portfolio_state.current_exposure = 0.0
            portfolio_state.event_exposure = 0.0
            active_trade = None

    if simulate_trades and active_trade is not None:
        final_row = data.iloc[-1]
        final_market_state = MarketState(
            market_id=str(final_row["market_id"]),
            timestamp=pd.Timestamp(final_row["timestamp"]).to_pydatetime(),
            mid_price=float(final_row["mid_price"]),
            yes_price=float(final_row.get("yes_price", final_row["mid_price"])),
            no_price=float(final_row.get("no_price", 1.0 - final_row["mid_price"])),
            spread=float(final_row["spread"]),
            depth=float(final_row["depth"]),
            recent_volume=float(final_row["recent_volume"]),
            order_flow_imbalance=0.0,
            trade_aggression=0.0,
            price_change=float(final_row.get("price_change", 0.0)),
            event_phase=_coerce_event_phase(final_row.get("event_phase", EventPhase.PRE_EVENT.value)),
            market_category=_coerce_market_category(final_row.get("market_category", MarketCategory.MIXED.value)),
            price_region=classify_price_region(
                float(final_row["mid_price"]),
                boundary_low=cfg.thresholds.boundary_low,
                extreme_low=cfg.thresholds.extreme_low,
                boundary_high=cfg.thresholds.boundary_high,
                extreme_high=cfg.thresholds.extreme_high,
            ),
        )
        active_trade = exit_trade(active_trade, final_market_state)
        trade_rows.append(_trade_to_row(active_trade, market_category=final_market_state.market_category.value))

    trades = pd.DataFrame(trade_rows)
    evaluation_summary = strategy_context_grouping(trades) if not trades.empty else strategy_context_grouping(pd.DataFrame())
    return ReplayResult(
        decision_log=pd.DataFrame(decision_rows),
        trades=trades,
        evaluation_summary=evaluation_summary,
    )

