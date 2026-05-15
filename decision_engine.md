# Combined Decision Engine (Final)

## Objective

Integrate:

- Agent Credibility Score (ACS)
- Crowd Pressure Score (CPS)
- Shock Detection
- Overreaction Detection
- YES/NO Flow Structure
- Time Horizon
- Event Phase
- Price Location
- Market Category

into a unified trading decision framework.

---

## SECTION 1: CORE PRINCIPLES

1. Do not trade raw direction — trade overreaction and credibility
2. Crowd explains movement — agents explain truth
3. Boundaries are asymmetric opportunities
4. Signals must be interpreted through context

---

## SECTION 2: INPUTS

### Market Signals
- order flow imbalance
- trade aggressiveness
- price movement
- liquidity conditions

---

### Wallet Signals
- filtered wallet set (size-based)
- Agent Credibility Score (ACS)
- wallet participation in move

---

### Context Variables
- time horizon (fast / mid / slow)
- event phase (pre / live / post)
- price location (interior / near-boundary / extreme)
- market category (retail-heavy / info-heavy / mixed)

---

## SECTION 3: CORE SCORES

### Crowd Pressure Score (CPS)
Measures:
- urgency
- imbalance
- dispersion
- structural instability

---

### Agent Credibility Score (ACS)
Measures:
- timing (historical + local)
- size / conviction
- specialization
- consistency
- PnL (low weight)

---

### Shock Indicator (SI)

Detects:
- large price jumps
- large trades relative to depth
- sudden structural change

---

### Overreaction Indicator (OI)

Detects when a move is excessive relative to:

- liquidity
- follow-through
- agent confirmation

---

## SECTION 4: HORIZON SELECTION

Choose trade horizon:

- Fast (seconds–minutes)
- Mid (minutes–hours)
- Slow (hours–expiration)

---

## SECTION 5: DECISION PIPELINE

### Step 1: Detect Event

If SI is low:
→ No trade (unless strong agent accumulation)

If SI is high:
→ Proceed

---

### Step 2: Evaluate Flow Source

Compare:
- CPS
- ACS of active wallets

---

### Step 3: Check Overreaction

Overreaction exists if:
- large move in thin liquidity
- no strong agent confirmation
- weak persistence

---

### Step 4: Evaluate YES/NO Structure

- Which side has high-ACS wallets?
- Is opposing side weak or strong?
- Is flow one-sided or conflicted?

---

### Step 5: Apply Horizon Logic

#### FAST HORIZON

- High CPS + OI + Low ACS → Fade
- High CPS + No OI → No trade
- High ACS (early) → Monitor only

---

#### MID HORIZON

- High ACS + persistence → Follow
- High CPS + reversal → Fade confirmation
- Rising ACS → Build conviction

---

#### SLOW HORIZON

- High ACS + repeated behavior → Follow
- Low structure → No trade

---

### Step 6: Apply Context Modifiers

#### Event Phase

- Pre-event:
  - Increase CPS weight
  - Decrease ACS reliability

- Live:
  - Increase ACS importance
  - Decrease CPS reliability

- Post-event:
  - Reduce all signal confidence

---

#### Market Category

- Retail-heavy:
  - Increase CPS baseline
  - Require stronger ACS

- Info-heavy:
  - Increase ACS weight

- Mixed:
  - Require confirmation

---

## SECTION 6: BOUNDARY LOGIC (ASYMMETRIC)

### Extreme Low Prices (~0–5%)

If:
- CPS high
- ACS low

→ Aggressive Fade (buy YES)

If:
- ACS high

→ Avoid

---

### Extreme High Prices (~95–100%)

If:
- ACS high
- persistence confirmed

→ Aggressive Follow (buy YES)

If:
- CPS high and ACS low

→ Do NOT blindly follow (possible overextension)

---

### Key Principle

Boundary trades are asymmetric:

- Longshot bias → fade low probabilities
- Credible conviction → follow high probabilities

---

## SECTION 7: FINAL DECISION RULES

### Fade (Crowd Overreaction)

- CPS high
- OI present
- ACS low

---

### Follow (Agent Signal)

- ACS high
- persistence confirmed
- flow coherent

---

### Boundary Fade

- extreme low price
- low ACS
- crowd-driven

---

### Boundary Follow

- extreme high price
- high ACS
- persistence

---

### Avoid

- conflicting ACS vs CPS
- unclear flow dominance
- extreme boundary without confirmation

---

## SECTION 8: RISK CONTROLS

- Never act on a single signal
- Require persistence for agent-based trades
- Reduce exposure near boundaries unless strong signal
- Adjust thresholds by category and phase
- Avoid overfitting wallet behavior

---

## SECTION 9: CORE INSIGHT

- CPS tells you what the crowd is doing
- ACS tells you whether to trust it
- OI tells you if it went too far

Edge comes from combining all three.