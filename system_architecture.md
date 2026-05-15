# System Architecture

## Objective

Define the full software architecture for implementing the prediction-market trading strategy on Polymarket.

This architecture connects:

- research logic
- signal generation
- decision-making
- portfolio management
- execution
- monitoring
- evaluation

The system is designed to support a progression from:
- historical replay
- paper trading
- shadow deployment
- live trading

---

## SECTION 1: DESIGN PRINCIPLES

### 1. Separation of Concerns
Each major function should live in its own module:
- data ingestion
- feature computation
- signal generation
- decision logic
- sizing / portfolio logic
- execution
- monitoring / logging

This prevents strategy logic from becoming entangled with exchange-specific implementation.

---

### 2. Research / Production Consistency
The same core signal and decision logic should be reusable across:
- historical backtests
- paper trading
- live deployment

Implementation should avoid rewriting logic separately for research and production.

---

### 3. Safety First
The system must fail safely.

If:
- data becomes stale
- account state is uncertain
- order status is unclear
- risk constraints are violated

the system should stop trading or reduce risk automatically.

---

### 4. Event-Driven + State-Based Design
The system should react to:
- new trades
- order book updates
- wallet activity
- event phase changes
- fills / cancellations

while maintaining an internal state representation of:
- market state
- wallet state
- portfolio state
- risk state

---

## SECTION 2: HIGH-LEVEL LAYERS

The full system consists of the following layers:

1. Market Universe Layer
2. Data Ingestion Layer
3. State Store Layer
4. Feature / Signal Layer
5. Process Inference Layer
6. Decision Layer
7. Portfolio / Sizing Layer
8. Execution Layer
9. Risk Control Layer
10. Monitoring / Logging Layer
11. Evaluation / Replay Layer

---

## SECTION 3: MARKET UNIVERSE LAYER

### Purpose
Determine which markets are eligible for monitoring and trading.

### Inputs
- market metadata
- event metadata
- category
- liquidity statistics
- time to resolution

### Responsibilities
- discover new markets
- exclude structurally bad markets
- build and refresh watchlists
- group related markets by event / category

### Example Filters
- minimum liquidity
- minimum recent trading activity
- acceptable spread
- strategy-supported category
- compatible event phase

### Notes
This layer should primarily rely on market discovery endpoints and market metadata.

---

## SECTION 4: DATA INGESTION LAYER

### Purpose
Collect all raw exchange and market data required by the system.

### Subsystems

#### 4.1 Public Market Data
- order book snapshots
- order book updates
- recent trades
- prices
- market metadata

#### 4.2 Wallet / Activity Data
- trade history
- wallet participation
- holder / activity information
- recent wallet flows

#### 4.3 Private Account Data
- balances
- open orders
- fills
- positions

### Modes
- historical ingestion
- live streaming
- periodic polling fallback

### Notes
The architecture should support both REST-style pull and WebSocket-style streaming where available.

---

## SECTION 5: STATE STORE LAYER

### Purpose
Maintain the current internal state of the system.

### State Objects

#### 5.1 Market State
- current YES / NO prices
- current depth
- spread
- imbalance
- event phase
- price region

#### 5.2 Wallet State
- filtered candidate wallets
- ACS-related metrics
- new-wallet metrics
- historical timing / specialization data

#### 5.3 Portfolio State
- open positions
- pending orders
- realized / unrealized PnL
- event cluster exposure

#### 5.4 Risk State
- daily loss
- exposure caps
- stale-data flags
- system health flags

### Design Requirement
State should be queryable by all downstream modules without repeated recomputation.

---

## SECTION 6: FEATURE / SIGNAL LAYER

### Purpose
Transform raw data into structured features and signals.

### Submodules

#### 6.1 Crowd Feature Engine
Computes:
- imbalance
- aggression
- liquidity thinness
- dispersion
- overreaction indicators

#### 6.2 Agent Feature Engine
Computes:
- wallet timing
- wallet sizing quality
- wallet specialization
- wallet consistency
- local credibility

#### 6.3 New Wallet Engine
Computes:
- new-wallet attention filter
- linkage likelihood
- new-wallet behavior score
- cluster patterns

#### 6.4 Boundary / Context Engine
Computes:
- boundary proximity
- event phase
- category modifiers
- time-to-resolution modifiers
- YES / NO asymmetry

### Output
A unified signal state for each monitored market.

---

## SECTION 7: PROCESS INFERENCE LAYER

### Purpose
Infer which underlying process is currently dominant.

### Outputs

#### 7.1 Crowd Process State
- crowd pressure score
- overreaction likelihood

#### 7.2 Agent Process State
- active credible wallet involvement
- strength of agent-driven signal

#### 7.3 New Wallet Process State
- hidden-identity likelihood
- fresh-agent credibility

#### 7.4 Boundary Process State
- whether boundary logic is active
- whether extreme prices should be faded, followed, or avoided

### Notes
This layer does not place trades.
It only interprets current conditions.

---

## SECTION 8: DECISION LAYER

### Purpose
Turn inferred process states into trade intents.

### Decision Types
- no trade
- fade
- follow
- boundary fade
- boundary follow
- watch only
- reduce / exit

### Inputs
- signal state
- process inference
- horizon selection
- context state

### Outputs
- decision type
- confidence level
- strategy bucket
- reason codes
- intended horizon

### Design Principle
Decision logic should be fully deterministic and explainable.

---

## SECTION 9: PORTFOLIO / SIZING LAYER

### Purpose
Convert trade intent into target position size and exposure.

### Inputs
- decision type
- edge strength
- strategy quality score (SQS)
- current exposure
- event cluster correlation
- risk state

### Responsibilities
- determine initial size
- determine scaling rules
- enforce portfolio caps
- cap correlated exposure
- adjust size for strategy quality

### Outputs
- target size
- max allowed size
- whether trade is blocked
- whether scaling is permitted

### Notes
This layer should implement the probability-weighted but heuristic sizing framework.

---

## SECTION 10: EXECUTION LAYER

### Purpose
Translate target positions into actual exchange orders.

### Responsibilities
- choose passive vs aggressive execution
- submit orders
- cancel / replace stale orders
- track fill status
- reconcile open orders and positions

### Order Logic
- follow trades may allow more aggressive execution
- fade trades should be more price-sensitive
- boundary trades require strict price discipline

### Execution Safety
- never trade without synchronized state
- reject orders if market data is stale
- reject orders if account state is uncertain

### Notes
Polymarket trading occurs through the CLOB using signed orders and authenticated requests.

---

## SECTION 11: RISK CONTROL LAYER

### Purpose
Override the rest of the system when risk conditions are violated.

### Hard Stops
- max daily loss
- max position per market
- max position per event cluster
- max category exposure
- stale-data detection
- desynchronized account state
- excessive open-order count

### Soft Controls
- reduce size after drawdown
- reduce size in uncertain contexts
- tighten thresholds near resolution

### Rule
This layer can block any trade regardless of upstream signal quality.

---

## SECTION 12: MONITORING / LOGGING LAYER

### Purpose
Record all system behavior and support debugging, evaluation, and auditing.

### Must Log
- market snapshot
- wallet state
- signals
- process inference
- decision
- target size
- order actions
- fill results
- exit reason

### Monitoring Views
- system health
- active positions
- pending orders
- high-ACS wallet activity
- boundary opportunities
- error / alert stream

### Notes
This layer is essential for both debugging and strategy evaluation.

---

## SECTION 13: EVALUATION / REPLAY LAYER

### Purpose
Support offline evaluation and post-trade analysis.

### Uses
- historical replay
- paper trading
- shadow evaluation
- strategy scoring
- wallet-score validation
- context breakdown analysis

### Requirement
The replay engine should reuse the same feature, signal, and decision logic as production.

---

## SECTION 14: DATA FLOW

### Step 1
Market universe layer selects markets to monitor.

### Step 2
Data ingestion layer pulls and streams raw data.

### Step 3
State store updates internal market, wallet, portfolio, and risk states.

### Step 4
Feature / signal layer computes structured signals.

### Step 5
Process inference layer identifies dominant crowd / agent / boundary conditions.

### Step 6
Decision layer generates trade intent.

### Step 7
Portfolio / sizing layer determines allowed position size.

### Step 8
Risk layer approves or blocks the trade.

### Step 9
Execution layer submits / manages orders.

### Step 10
Monitoring / logging layer records everything.

### Step 11
Evaluation layer later replays outcomes and updates strategy quality.

---

## SECTION 15: DEPLOYMENT STAGES

### Stage 1: Historical Replay
- no live orders
- validate signal and decision logic

### Stage 2: Paper Trading
- live public data
- simulated fills
- no capital at risk

### Stage 3: Shadow Mode
- live system
- full decision and execution logic
- order transmission blocked

### Stage 4: Small Live Deployment
- tight risk caps
- limited market universe
- minimal sizing

### Stage 5: Controlled Expansion
- only after stable performance and system reliability

---

## SECTION 16: RECOMMENDED CODE MODULES

### Core Directories
- `market_universe/`
- `ingestion/`
- `state/`
- `signals/`
- `process_inference/`
- `decision/`
- `portfolio/`
- `execution/`
- `risk/`
- `monitoring/`
- `evaluation/`
- `config/`

### Key Principle
The architecture should be modular enough that:
- signals can be improved independently
- exchange logic can be swapped or upgraded
- research and production remain aligned

---

## SECTION 17: CORE INSIGHT

The trading strategy is not a single model.

It is a pipeline:

raw data → structured state → signals → process inference → trade decision → sizing → execution → evaluation

The system should preserve this separation so that:
- reasoning stays interpretable
- failures are diagnosable
- strategy improvements are modular