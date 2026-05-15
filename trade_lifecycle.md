# Trade Lifecycle Framework

## Objective

Define the full lifecycle of a trade from setup to exit, including:

- entry conditions
- position sizing
- validation logic
- management rules
- exit conditions
- re-entry logic

Each trade is tied to a specific hypothesis:
- crowd overreaction (fade)
- agent-driven move (follow)
- boundary behavior (asymmetric)

---

## SECTION 1: TRADE TYPES

### 1. Fade Trades
Hypothesis:
- price moved too far relative to underlying conditions

---

### 2. Follow Trades
Hypothesis:
- credible agent is driving a real repricing

---

### 3. Boundary Trades
Hypothesis:
- longshot bias or convergence dynamics dominate near extremes

---

## SECTION 2: TRADE PHASES

---

### Phase 1: Setup

Conditions:
- signals align with a trade hypothesis
- CPS / ACS / OI evaluated
- context (phase, category, boundary) supports trade

Action:
- no position yet
- monitor for entry trigger

---

### Phase 2: Entry

#### Entry Conditions

##### Fade:
- CPS high
- OI present
- ACS low

##### Follow:
- ACS high
- early persistence observed

##### Boundary:
- price at extreme
- ACS/CPS interpreted asymmetrically

---

#### Entry Size

Initial position should be:
- small to medium (not full size)

Depends on:
- signal strength
- context confidence
- boundary proximity

---

## SECTION 3: VALIDATION PHASE

This is the most important phase.

Occurs shortly after entry.

---

### Validation Signals

#### For Fade:
- price stops moving upward
- begins to stall or reverse
- no high-ACS wallet continues buying

---

#### For Follow:
- price continues in direction
- same wallet or similar wallets add
- opposing side weakens

---

#### For Boundary:
- price fails to move further in extreme direction
- OR credible continuation occurs

---

### Actions

#### Positive Validation:
- increase position (scale in)

#### Negative Validation:
- reduce or exit quickly

---

## SECTION 4: POSITION MANAGEMENT

---

### Scaling Rules

#### Fade:
- scale as price stabilizes or reverses
- avoid scaling into strong continuation

---

#### Follow:
- scale as persistence strengthens
- scale with additional agent confirmation

---

#### Boundary:
- scale only if signal remains consistent
- be cautious near extreme levels

---

### Monitoring Signals

- price persistence vs reversal
- new wallet participation
- change in ACS of participants
- change in CPS (crowd returning or fading)
- YES/NO structural changes

---

## SECTION 5: EXIT LOGIC

---

### Exit Types

#### 1. Profit Exit

##### Fade:
- price reverts toward equilibrium

##### Follow:
- move slows or reaches target region

##### Boundary:
- move exits extreme region or converges

---

#### 2. Invalidation Exit (MOST IMPORTANT)

##### Fade invalidation:
- high-ACS wallet enters and pushes price further
- price continues without resistance

---

##### Follow invalidation:
- price fails to persist
- reversal occurs
- wallet stops participating

---

##### Boundary invalidation:
- strong ACS contradicts initial interpretation
- rapid move against position with persistence

---

#### 3. Time-Based Exit

- trade exceeds intended horizon
- event phase changes (e.g. pre → live)
- resolution approaches

---

## SECTION 6: POSITION SIZING

---

### Initial Size

Depends on:
- signal clarity
- ACS vs CPS differential
- context (phase, category)
- boundary risk

---

### Scaling

- increase only after validation
- never full size at entry
- reduce in uncertain conditions

---

### Risk Control

- limit exposure per trade
- reduce size in boundary zones unless high conviction
- reduce size in conflicting signals

---

## SECTION 7: RE-ENTRY LOGIC

---

### Conditions for Re-Entry

- original hypothesis reappears
- new signal confirms earlier thesis
- new wallets or flow support same direction

---

### Avoid Re-Entry When

- hypothesis clearly invalidated
- market structure has changed
- agent behavior contradicts prior signal

---

## SECTION 8: FAILURE MODES

---

### Fade Failures
- real information misclassified as crowd
- persistence underestimated

---

### Follow Failures
- false agent signals
- overconfidence in ACS

---

### Boundary Failures
- fading true outcomes
- following overextended moves

---

## SECTION 9: CORE PRINCIPLE

A trade is not just an entry.

It is a sequence:

1. Hypothesis
2. Entry
3. Validation
4. Management
5. Exit

The edge comes from managing the sequence correctly, not just identifying signals.