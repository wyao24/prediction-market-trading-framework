from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd

from prediction_market_trading.state.models import EventPhase, PriceRegion


def _clip(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return float(np.clip(value, lower, upper))


def compute_order_flow_imbalance(buy_volume: float, sell_volume: float) -> float:
    total_volume = max(buy_volume + sell_volume, 1e-9)
    return float((buy_volume - sell_volume) / total_volume)


def compute_trade_aggression(aggressive_volume: float, recent_volume: float) -> float:
    return _clip(aggressive_volume / max(recent_volume, 1e-9))


def compute_liquidity_thinness(
    spread: float,
    depth: float,
    reference_spread: float = 0.05,
    reference_depth: float = 1_000.0,
) -> float:
    spread_score = _clip(spread / reference_spread)
    depth_score = 1.0 - _clip(depth / reference_depth)
    return _clip((0.6 * spread_score) + (0.4 * depth_score))


def compute_price_acceleration(prices: Sequence[float] | pd.Series) -> float:
    array = np.asarray(list(prices), dtype=float)
    if array.size < 3:
        if array.size < 2:
            return 0.0
        return _clip((array[-1] - array[-2]) * 10.0, -1.0, 1.0)
    raw_acceleration = array[-1] - (2.0 * array[-2]) + array[-3]
    return _clip(raw_acceleration * 10.0, -1.0, 1.0)


def classify_price_region(
    price: float,
    boundary_low: float = 0.10,
    extreme_low: float = 0.05,
    boundary_high: float = 0.90,
    extreme_high: float = 0.95,
) -> PriceRegion:
    if price <= extreme_low:
        return PriceRegion.EXTREME_LOW
    if price <= boundary_low:
        return PriceRegion.NEAR_LOW
    if price >= extreme_high:
        return PriceRegion.EXTREME_HIGH
    if price >= boundary_high:
        return PriceRegion.NEAR_HIGH
    return PriceRegion.INTERIOR


def classify_event_phase(
    hours_to_resolution: float | None = None,
    *,
    is_live: bool = False,
    is_resolved: bool = False,
) -> EventPhase:
    if is_resolved:
        return EventPhase.POST_EVENT
    if is_live:
        return EventPhase.LIVE
    if hours_to_resolution is not None and hours_to_resolution <= 1.0:
        return EventPhase.LIVE
    return EventPhase.PRE_EVENT


def compute_wallet_concentration(wallet_sizes: Sequence[float] | pd.Series) -> float:
    sizes = np.abs(np.asarray(list(wallet_sizes), dtype=float))
    total_size = sizes.sum()
    if total_size <= 0 or sizes.size == 0:
        return 0.0
    shares = sizes / total_size
    top_share = float(shares.max())
    hhi = float(np.square(shares).sum())
    return _clip((0.5 * top_share) + (0.5 * hhi))


def compute_persistence(prices: Sequence[float] | pd.Series) -> float:
    array = np.asarray(list(prices), dtype=float)
    if array.size < 2:
        return 0.0
    diffs = np.diff(array)
    overall_direction = np.sign(array[-1] - array[0])
    if overall_direction == 0:
        return 0.0
    aligned = np.sign(diffs) == overall_direction
    return _clip(float(aligned.mean()))

