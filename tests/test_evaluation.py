import pandas as pd

from prediction_market_trading.evaluation.metrics import (
    expected_value,
    hit_rate,
    max_drawdown,
    strategy_context_grouping,
)


def test_hit_rate_calculation() -> None:
    assert hit_rate([0.10, -0.05, 0.02, 0.00]) == 0.5


def test_expected_value_calculation() -> None:
    assert round(expected_value([0.10, -0.05, 0.02]), 6) == round((0.10 - 0.05 + 0.02) / 3.0, 6)


def test_drawdown_calculation() -> None:
    assert max_drawdown([0.10, -0.05, -0.10, 0.03]) >= 0.10


def test_grouping_by_strategy_context() -> None:
    trades = pd.DataFrame(
        [
            {
                "strategy_type": "FADE",
                "market_category": "retail_heavy",
                "event_phase": "pre_event",
                "price_region": "interior",
                "horizon": "fast",
                "return_pct": 0.05,
            },
            {
                "strategy_type": "FADE",
                "market_category": "retail_heavy",
                "event_phase": "pre_event",
                "price_region": "interior",
                "horizon": "fast",
                "return_pct": -0.02,
            },
        ]
    )
    grouped = strategy_context_grouping(trades)
    assert len(grouped) == 1
    assert grouped.loc[0, "sample_size"] == 2

