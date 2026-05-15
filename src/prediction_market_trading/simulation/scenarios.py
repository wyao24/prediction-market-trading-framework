from __future__ import annotations

import pandas as pd

from prediction_market_trading.state.models import EventPhase, MarketCategory


def _build_scenario(
    scenario: str,
    market_id: str,
    prices: list[float],
    spreads: list[float],
    depths: list[float],
    buy_volumes: list[float],
    sell_volumes: list[float],
    aggressive_volumes: list[float],
    wallet_trade_sizes: list[float],
    wallet_concentrations: list[float],
    timing_scores: list[float],
    specialization_scores: list[float],
    persistence_scores: list[float],
    market_category: MarketCategory,
    event_phase: EventPhase = EventPhase.PRE_EVENT,
) -> pd.DataFrame:
    timestamps = pd.date_range("2026-01-01 09:00:00", periods=len(prices), freq="min")
    rows: list[dict[str, object]] = []
    previous_price = prices[0]

    for index, price in enumerate(prices):
        recent_volume = buy_volumes[index] + sell_volumes[index]
        rows.append(
            {
                "scenario": scenario,
                "market_id": market_id,
                "timestamp": timestamps[index],
                "mid_price": price,
                "yes_price": price,
                "no_price": 1.0 - price,
                "spread": spreads[index],
                "depth": depths[index],
                "recent_volume": recent_volume,
                "buy_volume": buy_volumes[index],
                "sell_volume": sell_volumes[index],
                "aggressive_volume": aggressive_volumes[index],
                "wallet_trade_size": wallet_trade_sizes[index],
                "wallet_concentration": wallet_concentrations[index],
                "timing_score": timing_scores[index],
                "specialization_score": specialization_scores[index],
                "persistence_score": persistence_scores[index],
                "consistency_score": persistence_scores[index],
                "price_change": price - previous_price if index else 0.0,
                "event_phase": event_phase.value,
                "market_category": market_category.value,
            }
        )
        previous_price = price

    return pd.DataFrame(rows)


def generate_crowd_overreaction_scenario() -> pd.DataFrame:
    return _build_scenario(
        scenario="crowd_overreaction",
        market_id="crowd-001",
        prices=[0.44, 0.48, 0.56, 0.65, 0.61, 0.55],
        spreads=[0.03, 0.03, 0.035, 0.04, 0.03, 0.025],
        depths=[140, 120, 90, 80, 110, 130],
        buy_volumes=[40, 55, 90, 95, 35, 25],
        sell_volumes=[20, 18, 25, 20, 40, 45],
        aggressive_volumes=[42, 60, 88, 92, 30, 24],
        wallet_trade_sizes=[10, 12, 14, 15, 10, 9],
        wallet_concentrations=[0.20, 0.18, 0.22, 0.24, 0.22, 0.20],
        timing_scores=[0.20, 0.22, 0.18, 0.15, 0.20, 0.25],
        specialization_scores=[0.18, 0.20, 0.22, 0.20, 0.18, 0.18],
        persistence_scores=[0.25, 0.30, 0.28, 0.20, 0.18, 0.15],
        market_category=MarketCategory.RETAIL_HEAVY,
    )


def generate_agent_conviction_shock_scenario() -> pd.DataFrame:
    return _build_scenario(
        scenario="agent_conviction_shock",
        market_id="agent-001",
        prices=[0.52, 0.54, 0.60, 0.67, 0.72, 0.76],
        spreads=[0.015, 0.015, 0.018, 0.018, 0.02, 0.02],
        depths=[260, 280, 300, 320, 300, 290],
        buy_volumes=[35, 42, 110, 90, 75, 60],
        sell_volumes=[18, 16, 28, 22, 18, 15],
        aggressive_volumes=[30, 35, 100, 82, 68, 55],
        wallet_trade_sizes=[30, 40, 120, 115, 95, 80],
        wallet_concentrations=[0.55, 0.60, 0.78, 0.80, 0.76, 0.72],
        timing_scores=[0.65, 0.72, 0.88, 0.90, 0.86, 0.82],
        specialization_scores=[0.70, 0.72, 0.80, 0.82, 0.80, 0.78],
        persistence_scores=[0.60, 0.68, 0.82, 0.88, 0.90, 0.86],
        market_category=MarketCategory.INFO_HEAVY,
    )


def generate_stealth_accumulation_scenario() -> pd.DataFrame:
    return _build_scenario(
        scenario="stealth_accumulation",
        market_id="stealth-001",
        prices=[0.40, 0.41, 0.43, 0.46, 0.49, 0.52],
        spreads=[0.018, 0.018, 0.02, 0.02, 0.022, 0.022],
        depths=[220, 225, 230, 240, 245, 250],
        buy_volumes=[22, 24, 28, 32, 34, 36],
        sell_volumes=[18, 16, 15, 16, 18, 20],
        aggressive_volumes=[15, 16, 18, 20, 22, 23],
        wallet_trade_sizes=[24, 26, 28, 30, 30, 32],
        wallet_concentrations=[0.62, 0.64, 0.66, 0.68, 0.70, 0.72],
        timing_scores=[0.58, 0.62, 0.68, 0.72, 0.74, 0.76],
        specialization_scores=[0.60, 0.62, 0.64, 0.66, 0.68, 0.70],
        persistence_scores=[0.62, 0.66, 0.70, 0.76, 0.80, 0.82],
        market_category=MarketCategory.MIXED,
    )


def generate_boundary_longshot_bias_scenario() -> pd.DataFrame:
    return _build_scenario(
        scenario="boundary_longshot_bias",
        market_id="boundary-001",
        prices=[0.04, 0.05, 0.07, 0.09, 0.08, 0.06],
        spreads=[0.04, 0.04, 0.045, 0.05, 0.045, 0.04],
        depths=[90, 85, 80, 75, 80, 95],
        buy_volumes=[14, 18, 24, 26, 16, 12],
        sell_volumes=[9, 10, 11, 12, 15, 18],
        aggressive_volumes=[12, 16, 22, 24, 12, 10],
        wallet_trade_sizes=[5, 5, 6, 6, 5, 4],
        wallet_concentrations=[0.18, 0.16, 0.18, 0.20, 0.18, 0.16],
        timing_scores=[0.20, 0.18, 0.16, 0.14, 0.18, 0.20],
        specialization_scores=[0.15, 0.15, 0.18, 0.18, 0.15, 0.15],
        persistence_scores=[0.20, 0.24, 0.26, 0.18, 0.16, 0.14],
        market_category=MarketCategory.RETAIL_HEAVY,
    )


def generate_all_scenarios() -> dict[str, pd.DataFrame]:
    return {
        "crowd_overreaction": generate_crowd_overreaction_scenario(),
        "agent_conviction_shock": generate_agent_conviction_shock_scenario(),
        "stealth_accumulation": generate_stealth_accumulation_scenario(),
        "boundary_longshot_bias": generate_boundary_longshot_bias_scenario(),
    }

