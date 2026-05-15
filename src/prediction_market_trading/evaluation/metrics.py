from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd


def _as_array(values: Sequence[float] | pd.Series) -> np.ndarray:
    return np.asarray(list(values), dtype=float)


def hit_rate(returns: Sequence[float] | pd.Series) -> float:
    array = _as_array(returns)
    if array.size == 0:
        return 0.0
    return float((array > 0).mean())


def average_return(returns: Sequence[float] | pd.Series) -> float:
    array = _as_array(returns)
    if array.size == 0:
        return 0.0
    return float(array.mean())


def expected_value(returns: Sequence[float] | pd.Series) -> float:
    array = _as_array(returns)
    if array.size == 0:
        return 0.0
    wins = array[array > 0]
    losses = array[array <= 0]
    win_component = wins.mean() * (wins.size / array.size) if wins.size else 0.0
    loss_component = losses.mean() * (losses.size / array.size) if losses.size else 0.0
    return float(win_component + loss_component)


def max_drawdown(returns: Sequence[float] | pd.Series) -> float:
    array = _as_array(returns)
    if array.size == 0:
        return 0.0
    cumulative = np.cumsum(array)
    running_peak = np.maximum.accumulate(cumulative)
    drawdowns = running_peak - cumulative
    return float(drawdowns.max(initial=0.0))


def volatility(returns: Sequence[float] | pd.Series) -> float:
    array = _as_array(returns)
    if array.size == 0:
        return 0.0
    return float(array.std(ddof=0))


def win_loss_asymmetry(returns: Sequence[float] | pd.Series) -> float:
    array = _as_array(returns)
    wins = array[array > 0]
    losses = array[array < 0]
    if wins.size == 0 or losses.size == 0:
        return 0.0
    return float(wins.mean() / abs(losses.mean()))


def sample_size(returns: Sequence[float] | pd.Series) -> int:
    return int(_as_array(returns).size)


def strategy_context_grouping(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame(
            columns=[
                "strategy_type",
                "market_category",
                "event_phase",
                "price_region",
                "horizon",
                "sample_size",
                "hit_rate",
                "average_return",
                "expected_value",
                "max_drawdown",
                "volatility",
                "win_loss_asymmetry",
            ]
        )

    group_columns = [
        "strategy_type",
        "market_category",
        "event_phase",
        "price_region",
        "horizon",
    ]

    rows: list[dict[str, object]] = []
    for keys, group in trades.groupby(group_columns):
        returns = group["return_pct"]
        rows.append(
            {
                "strategy_type": keys[0],
                "market_category": keys[1],
                "event_phase": keys[2],
                "price_region": keys[3],
                "horizon": keys[4],
                "sample_size": sample_size(returns),
                "hit_rate": hit_rate(returns),
                "average_return": average_return(returns),
                "expected_value": expected_value(returns),
                "max_drawdown": max_drawdown(returns),
                "volatility": volatility(returns),
                "win_loss_asymmetry": win_loss_asymmetry(returns),
            }
        )
    return pd.DataFrame(rows).sort_values(group_columns).reset_index(drop=True)

