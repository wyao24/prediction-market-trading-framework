# Probability-Weighted Sizing Framework

## Objective

Define a structured approach to position sizing that combines:

- signal-based edge estimation
- empirically evaluated strategy performance
- risk controls

Sizing is determined by:

> Edge × Strategy Quality × Risk Constraints

---

## SECTION 1: EDGE ESTIMATION

Edge is derived from signals, not exact probabilities.

---

### Inputs

- Agent Credibility Score (ACS)
- Crowd Pressure Score (CPS)
- Overreaction Indicator (OI)
- Boundary context
- Persistence
- YES/NO structure

---

### Edge Levels

| Level | Description |
|------|------------|
| Weak | slight mispricing |
| Medium | moderate confidence |
| Strong | clear signal |
| Very Strong | rare, high-alignment |

---

## SECTION 2: STRATEGY BUCKETS

Trades are grouped into:

1. Fade (crowd overreaction)
2. Follow (agent-driven)
3. Boundary Fade (low price longshot)
4. Boundary Follow (high price, high ACS)
5. New Wallet

Each bucket is evaluated separately.

---

## SECTION 3: STRATEGY EVALUATION

For each strategy, track:

### Metrics

- Hit Rate
- Average Return
- Expected Value (EV)
- Drawdown
- Volatility

---

### Context Breakdown

Evaluate performance by:

- market category
- event phase
- price region

---

## SECTION 4: STRATEGY QUALITY SCORE (SQS)

Assign each strategy a quality score:

| Level | Meaning |
|------|--------|
| Low | unreliable |
| Medium | partially reliable |
| High | strong historical performance |

---

## SECTION 5: SIZING RULES

---

### Step 1: Determine Edge

From signal strength.

---

### Step 2: Determine SQS

From historical evaluation.

---

### Step 3: Assign Size

| Edge | SQS | Size |
|------|-----|------|
| Very Strong | High | large |
| Strong | High | medium-large |
| Medium | High | medium |
| Strong | Medium | medium |
| Medium | Medium | small |
| Any | Low | very small or none |

---

## SECTION 6: FRACTIONAL KELLY CONCEPT

Sizing should be:

- proportional to edge
- scaled down (10–30% of theoretical Kelly)

---

## SECTION 7: RISK CONTROLS

---

### Position Caps

- max size per trade
- max exposure per event

---

### Boundary Risk

- only large size if strong signal + high SQS

---

### New Strategy Risk

- reduce size for untested strategies

---

## SECTION 8: SCALING

- enter small
- scale after validation
- never full size at entry

---

## SECTION 9: FEEDBACK LOOP

After each trade:

- update performance metrics
- update SQS
- adjust future sizing

---

## SECTION 10: CORE PRINCIPLE

Sizing is not based on confidence alone.

It is based on:

> confidence × proven effectiveness

This ensures:
- strong strategies scale up
- weak strategies are naturally suppressed