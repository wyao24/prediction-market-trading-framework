from prediction_market_trading.replay.engine import run_replay
from prediction_market_trading.simulation.scenarios import (
    generate_agent_conviction_shock_scenario,
    generate_crowd_overreaction_scenario,
)


def test_crowd_scenario_produces_fade_or_watch() -> None:
    result = run_replay(generate_crowd_overreaction_scenario())
    assert result.decision_log["decision_type"].isin(["FADE", "WATCH", "BOUNDARY_FADE"]).any()


def test_agent_scenario_produces_follow_or_watch() -> None:
    result = run_replay(generate_agent_conviction_shock_scenario())
    assert result.decision_log["decision_type"].isin(["FOLLOW", "WATCH", "BOUNDARY_FOLLOW"]).any()
