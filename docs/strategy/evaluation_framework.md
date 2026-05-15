# Strategy Evaluation Framework

## Objective

Provide a rigorous method to:

- evaluate performance of each strategy
- determine where each strategy works
- quantify reliability of signals
- update Strategy Quality Scores (SQS)
- inform position sizing decisions

---

## SECTION 1: EVALUATION UNIT

Evaluation is performed at the level of:

> Strategy × Context

---

### Strategy Buckets

1. Fade (crowd overreaction)
2. Follow (agent-driven)
3. Boundary Fade (low price)
4. Boundary Follow (high price, high ACS)
5. New Wallet

---

### Context Dimensions

Each trade is tagged by:

- Market Category (sports, macro, politics, etc.)
- Event Phase (pre, live, post)
- Price Region (interior, near-boundary, extreme)
- Horizon (fast, mid, slow)

---

### Example Unit

"Fade trades in sports, pre-event, interior price region"

---

## SECTION 2: CORE METRICS

---

### 2.1 Hit Rate

Definition:
- percentage of profitable trades

---

### 2.2 Average Return

Definition:
- mean return per trade

---

### 2.3 Expected Value (EV)

Definition:
- average return accounting for wins and losses

Most important metric.

---

### 2.4 Drawdown

Definition:
- largest cumulative loss

---

### 2.5 Volatility

Definition:
- variability of returns

---

### 2.6 Win/Loss Asymmetry

Definition:
- average win vs average loss

---

## SECTION 3: DATA COLLECTION

Each trade must record:

- strategy type
- context variables
- entry price
- exit price
- size
- PnL
- time held
- reason for exit (profit / invalidation / time)

---

## SECTION 4: MINIMUM SAMPLE SIZE

Avoid overfitting small samples.

---

### Guidelines

- < 20 trades → ignore conclusions
- 20–50 trades → weak signal
- 50–100 trades → moderate confidence
- 100+ trades → strong confidence

---

## SECTION 5: STRATEGY QUALITY SCORE (SQS)

---

### Definition

SQS represents:

> how reliable a strategy is in a given context

---

### Inputs

- EV (primary)
- drawdown
- stability
- sample size

---

### SQS Levels

| Level | Description |
|------|------------|
| Low | unreliable or negative EV |
| Medium | inconsistent or weak EV |
| High | consistent positive EV |

---

## SECTION 6: CONTEXT-SPECIFIC EVALUATION

---

### Key Principle

Strategies are not global.

They must be evaluated per context.

---

### Example

- Fade (sports, pre-event) → high SQS
- Fade (macro, live) → low SQS

---

## SECTION 7: PERFORMANCE STABILITY

---

### Evaluate:

- rolling EV over time
- consistency across subperiods
- sensitivity to regime changes

---

### Red Flags

- performance concentrated in small period
- highly unstable returns
- large drawdowns relative to EV

---

## SECTION 8: UPDATE RULES

---

### After Each Trade

- update metrics for relevant strategy-context unit
- update rolling statistics

---

### Periodic Updates

- recompute SQS
- adjust sizing rules

---

## SECTION 9: FEEDBACK INTO SIZING

---

### Integration

- High SQS → allow larger sizing
- Medium SQS → moderate sizing
- Low SQS → minimal or no sizing

---

### New Strategies

- start with low SQS
- increase only after sufficient data

---

## SECTION 10: FAILURE ANALYSIS

---

### For Losing Trades

Identify:

- was signal wrong?
- was context misclassified?
- was execution poor?
- was exit incorrect?

---

### For Winning Trades

Identify:

- was it repeatable?
- or random / lucky?

---

## SECTION 11: AVOIDING BIASES

---

### Survivorship Bias
- track all trades, not just winners

---

### Selection Bias
- include all signals that were traded

---

### Overfitting
- do not overreact to small samples

---

### Confirmation Bias
- do not reinterpret losing trades as “correct ideas”

---

## SECTION 12: CORE PRINCIPLE

You are not trying to prove that a strategy works.

You are trying to determine:

> where it works, how well it works, and whether it is reliable

Only then should it influence sizing.