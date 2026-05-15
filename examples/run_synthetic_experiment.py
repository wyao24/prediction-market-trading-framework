from __future__ import annotations

from pathlib import Path

import pandas as pd

from prediction_market_trading.replay.engine import run_replay
from prediction_market_trading.simulation.scenarios import (
    generate_agent_conviction_shock_scenario,
    generate_boundary_longshot_bias_scenario,
    generate_crowd_overreaction_scenario,
)


def _save_outputs(project_root: Path, scenario_name: str, decision_log: pd.DataFrame, trades: pd.DataFrame) -> None:
    output_dir = project_root / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    decision_log.to_csv(output_dir / f"{scenario_name}_decision_log.csv", index=False)
    if not trades.empty:
        trades.to_csv(output_dir / f"{scenario_name}_trades.csv", index=False)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    scenarios = {
        "crowd_overreaction": generate_crowd_overreaction_scenario(),
        "agent_conviction_shock": generate_agent_conviction_shock_scenario(),
        "boundary_longshot_bias": generate_boundary_longshot_bias_scenario(),
    }

    for name, frame in scenarios.items():
        result = run_replay(frame, simulate_trades=True)
        print(f"\n=== {name} ===")
        print(result.decision_log[["timestamp", "mid_price", "cps", "acs", "oi", "decision_type", "reason_codes"]].to_string(index=False))
        if result.trades.empty:
            print("No trades were simulated.")
        else:
            print("\nTrades:")
            print(result.trades[["trade_id", "strategy_type", "entry_price", "exit_price", "return_pct", "pnl"]].to_string(index=False))
            print("\nEvaluation:")
            print(result.evaluation_summary.to_string(index=False))
        _save_outputs(project_root, name, result.decision_log, result.trades)


if __name__ == "__main__":
    main()

