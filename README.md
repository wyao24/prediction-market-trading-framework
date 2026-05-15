# Prediction Market Trading Framework

This repository is the first research-to-code scaffold for a prediction-market trading experimentation framework focused on Polymarket-style markets. The project translates the existing Markdown research into a modular Python package for historical replay, synthetic scenario generation, paper-style simulation, and structured evaluation. It is intentionally designed for experimentation rather than live trading. No real exchange execution, API credentials, or production integrations are included in this phase.

The core research idea is to distinguish between crowd-driven flow, agent or wallet-driven flow, and boundary behavior near extreme prices, then map those regimes into deterministic decisions such as fade, follow, boundary fade, boundary follow, watch, or avoid. The initial code emphasizes interpretable rules, typed state, reproducible experiments, and explicit assumptions rather than statistical optimization.

## Current Status

- Research documents have been organized under `docs/` and `reports/`.
- A lightweight Python package now mirrors the conceptual pipeline from market state to evaluation.
- Synthetic scenarios and a replay engine are included for first-pass experiments.
- The implementation is deterministic and deliberately conservative. It does not claim profitability.

## Repository Structure

```text
README.md
INVENTORY.md
pyproject.toml
docs/
  architecture/
  research/
  strategy/
src/
  prediction_market_trading/
    config/
    data/
    decision/
    evaluation/
    inference/
    lifecycle/
    portfolio/
    replay/
    scoring/
    signals/
    simulation/
    state/
tests/
examples/
data/
  raw/
  processed/
reports/
figures/
notebooks/
archive/
```

## Conceptual Pipeline

```text
raw market data
-> structured state
-> feature extraction
-> signal scoring
-> process inference
-> decision engine
-> sizing
-> simulated trade lifecycle
-> evaluation
```

## Installation

Use any Python 3.11+ interpreter available on your machine.

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## Running Tests

```bash
python -m pytest
```

## Running the First Synthetic Experiment

```bash
python examples/run_synthetic_experiment.py
```

The example generates several synthetic market scenarios, runs them through the replay pipeline, prints a decision log, and writes optional CSV outputs under `data/processed/`.

## Roadmap

- Expand synthetic scenarios into richer replay datasets.
- Add better wallet-history abstractions and cold-start wallet handling.
- Add richer trade simulation and fill assumptions for paper trading.
- Add adapters for future real market data ingestion without connecting to live execution.
- Validate and refine thresholds using replay instead of hardcoded intuition alone.

