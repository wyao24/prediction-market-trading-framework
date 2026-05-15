from prediction_market_trading.scoring.rules import (
    compute_agent_credibility_score,
    compute_crowd_pressure_score,
    compute_overreaction_indicator,
)


def test_crowd_pressure_rises_with_imbalance_aggression_and_thin_liquidity() -> None:
    low_score = compute_crowd_pressure_score(
        order_flow_imbalance=0.10,
        trade_aggression=0.20,
        liquidity_thinness=0.20,
        price_acceleration=0.10,
    )
    high_score = compute_crowd_pressure_score(
        order_flow_imbalance=0.85,
        trade_aggression=0.90,
        liquidity_thinness=0.80,
        price_acceleration=0.70,
    )
    assert high_score > low_score


def test_agent_credibility_rises_with_timing_and_persistence() -> None:
    low_score = compute_agent_credibility_score(
        wallet_timing=0.20,
        wallet_trade_size=10.0,
        market_depth=200.0,
        wallet_concentration=0.20,
        specialization_score=0.20,
        persistence_score=0.20,
    )
    high_score = compute_agent_credibility_score(
        wallet_timing=0.85,
        wallet_trade_size=90.0,
        market_depth=200.0,
        wallet_concentration=0.80,
        specialization_score=0.75,
        persistence_score=0.88,
    )
    assert high_score > low_score


def test_overreaction_rises_with_large_move_low_acs_and_thin_liquidity() -> None:
    low_score = compute_overreaction_indicator(
        price_change=0.02,
        liquidity_thinness=0.20,
        agent_credibility_score=0.80,
        persistence_score=0.80,
    )
    high_score = compute_overreaction_indicator(
        price_change=0.18,
        liquidity_thinness=0.85,
        agent_credibility_score=0.20,
        persistence_score=0.15,
    )
    assert high_score > low_score

