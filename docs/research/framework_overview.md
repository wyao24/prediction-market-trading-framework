# Prediction Market Trading Strategy Framework

## Overview

This repository contains a structured research and development framework for building trading strategies in prediction markets (e.g. Polymarket).

The system is based on:

- identifying crowd vs agent-driven behavior
- exploiting overreaction and longshot bias
- tracking and evaluating wallet-level signals
- adapting to context (event phase, category, boundary)
- using probability-weighted, performance-adjusted sizing
- continuously evaluating and refining strategies

---

## Core Philosophy

This is not a single model.

It is a **modular decision system** built around:

1. Signal extraction
2. Process inference
3. Strategy selection
4. Trade lifecycle management
5. Portfolio construction
6. Continuous evaluation

---

## Repository Structure

The framework is organized into the following components:

---

### 1. Regime & Signal Mapping

📄 `regime_and_signal_map.md`

Defines:
- core processes (crowd vs agent)
- time horizons
- context dimensions (event phase, category, price location)
- mapping from raw information → signals → decisions

---

📄 `signal_matrix.md`

Defines:
- all signals available in the system
- mapping from signals → processes
- how signals behave across horizons and contexts

---

📄 `scoring_framework.md`

Defines:
- how signals are combined into:
  - Crowd Pressure Score (CPS)
  - Agent Credibility Score (ACS)
- how scoring differs across time horizons
- what signals are reliable vs noisy

---

### 2. Agent & Wallet Modeling

📄 `wallet_scoring_rubric.md`

Defines:
- how to evaluate wallets using:
  - timing (local + historical)
  - size / conviction
  - PnL (low weight)
  - specialization
  - consistency

---

📄 `new_wallet_classification.md`

Defines:
- how to handle cold-start wallets
- attention filtering
- linkage detection (hidden identity)
- local behavior scoring
- integration into agent framework

---

### 3. Decision Engine

📄 `decision_engine.md`

Defines:
- how CPS, ACS, and context combine into trade decisions
- overreaction vs reaction logic
- YES / NO dual-sided flow interpretation
- asymmetric boundary behavior
- final trade classification (fade, follow, boundary, avoid)

---

### 4. Trade Execution Logic

📄 `trade_lifecycle.md`

Defines:
- phases of a trade:
  - setup
  - entry
  - validation
  - management
  - exit
- different lifecycle rules for:
  - fade trades
  - follow trades
  - boundary trades

---

### 5. Portfolio & Sizing

📄 `probability_sizing_framework.md`

Defines:
- heuristic probability-weighted sizing
- edge estimation from signals
- Strategy Quality Score (SQS)
- mapping edge × SQS → position size
- scaling and risk constraints

---

### 6. Evaluation & Feedback

📄 `evaluation_framework.md`

Defines:
- how to evaluate strategies
- metrics:
  - expected value (EV)
  - hit rate
  - drawdown
  - volatility
- evaluation by:
  - strategy type
  - context (category, phase, price region)
- updating SQS based on performance

---

### 7. System Architecture (for future implementation)

📄 `system_architecture.md`

Defines:
- full system pipeline from data → execution
- modular components:
  - ingestion
  - signals
  - decision
  - portfolio
  - execution
  - monitoring
- deployment stages:
  - replay
  - paper trading
  - shadow mode
  - live trading

---

## How Everything Fits Together

The full pipeline is:


raw market data
↓
feature / signal extraction
↓
CPS / ACS / new wallet scoring
↓
process inference (crowd vs agent vs boundary)
↓
decision engine (fade / follow / avoid)
↓
trade lifecycle (entry → validation → management → exit)
↓
position sizing (edge × SQS)
↓
execution (future implementation)
↓
evaluation (update SQS and strategy beliefs)


---

## Research Workflow

This repository is designed to support the following workflow:

---

### Step 1: Strategy Definition

- identify a hypothesis (e.g. crowd overreaction)
- map to signals using `signal_matrix.md`
- define decision rules using `combined_decision_engine.md`

---

### Step 2: Trade Simulation

- simulate trades (historically or hypothetically)
- apply:
  - lifecycle rules
  - sizing framework

---

### Step 3: Data Logging

For each trade, record:
- strategy type
- context
- signals
- entry / exit
- PnL
- reasoning

---

### Step 4: Evaluation

- group trades by:
  - strategy
  - context
- compute:
  - EV
  - drawdown
  - stability
- update Strategy Quality Score (SQS)

---

### Step 5: Refinement

- adjust:
  - signal thresholds
  - context filters
  - sizing rules
- remove weak strategies
- scale strong strategies

---

## Strategy Types

The system currently supports:

1. **Fade**
   - exploit crowd overreaction

2. **Follow**
   - follow credible agent signals

3. **Boundary Fade**
   - exploit longshot bias near low prices

4. **Boundary Follow**
   - follow strong conviction near high prices

5. **New Wallet**
   - detect emerging or hidden agents

---

## Key Insights

- Not all signals are equal — context matters
- Overreaction ≠ wrong direction, only wrong magnitude
- Wallet behavior provides strong structural edge
- Boundary behavior is asymmetric
- Strategies must be evaluated in context, not globally
- Sizing must depend on both edge and proven performance

---

## Current Focus

The current focus is:

> Formalizing strategies → coding → evaluating

Not:
- premature optimization
- overcomplicating execution
- expanding strategy set too early

---

## Next Steps

Short-term priorities:

1. Implement signal and decision logic in code
2. Build data logging system
3. Simulate trades (historical or paper)
4. Evaluate strategies using `evaluation_framework.md`
5. Iterate on thresholds and filters

---

## Long-Term Direction

- integrate with Polymarket APIs
- build execution engine
- deploy paper trading system
- gradually move to live trading
- refine wallet clustering and agent detection

---

## Final Principle

This system is designed to be:

- modular
- interpretable
- testable
- adaptable

The goal is not to predict outcomes directly.

The goal is to:

> identify when the market is behaving incorrectly,  
> and exploit that behavior systematically.