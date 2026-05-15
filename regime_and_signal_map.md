# Regime and Signal Map

## Objective

Define the mapping from:

raw market observations → signals → underlying processes → strategy types

This file establishes the conceptual foundation for interpreting market behavior.

---

## SECTION 1: CORE PROCESSES

All market behavior is interpreted as a combination of:

### 1. Crowd Process
- many participants
- high dispersion
- urgency-driven (FOMO, panic)
- prone to overreaction

---

### 2. Agent Process
- few participants
- high concentration
- informed or structured behavior
- capable of moving price with persistence

---

### 3. Boundary Process
- price near 0 or 1
- longshot bias or convergence dynamics
- asymmetric behavior

---

## SECTION 2: TIME HORIZONS

Signals behave differently across horizons:

### Fast (seconds–minutes)
- detects events
- crowd bursts
- initial agent shocks

---

### Mid (minutes–hours)
- persistence vs reversal
- validation of moves
- agent confirmation

---

### Slow (hours–expiration)
- repeated correctness
- convergence to outcome
- long-term agent behavior

---

## SECTION 3: CONTEXT DIMENSIONS

Each market state must be interpreted through:

### Event Phase
- Pre-event
- Live
- Post-event / near resolution

---

### Market Category
- Retail-heavy (sports, entertainment)
- Info-heavy (macro, finance)
- Mixed (politics)

---

### Price Location
- Interior
- Near boundary
- Extreme boundary

---

## SECTION 4: SIGNAL → PROCESS MAPPING

### Crowd Signals
- imbalance
- aggression
- dispersion
- price acceleration

→ maps to Crowd Process

---

### Agent Signals
- wallet timing
- size relative to depth
- concentration
- persistence
- specialization

→ maps to Agent Process

---

### Boundary Signals
- extreme price
- asymmetric behavior
- lack of liquidity depth
- context sensitivity

→ maps to Boundary Process

---

## SECTION 5: PROCESS → STRATEGY MAPPING

### Crowd Process
→ Fade strategy (only if overreaction present)

---

### Agent Process
→ Follow strategy (only if persistence confirmed)

---

### Boundary Process
→ Asymmetric:
- near 1% → fade (longshot bias)
- near 99% → follow if ACS high

---

## SECTION 6: CORE PRINCIPLE

Markets are not in a single regime.

At any moment:
- multiple processes may be active
- dominance must be inferred from signals

The goal is to identify:
> which process dominates at the chosen trading horizon