# Signal Matrix

## Objective

Define all signals used in the system and how they map to:

- Crowd Pressure Score (CPS)
- Agent Credibility Score (ACS)
- Overreaction Indicator (OI)

---

## SECTION 1: CROWD SIGNALS

### S1: Order Flow Imbalance
- large directional buying/selling
- high aggressiveness

Supports:
- CPS ↑

---

### S2: Trade Aggression
- marketable orders
- crossing spread

Supports:
- CPS ↑

---

### S3: Participation Dispersion
- many wallets involved
- low concentration

Supports:
- CPS ↑
- ACS ↓

---

### S4: Price Acceleration
- rapid price movement

Supports:
- CPS ↑
- OI candidate

---

### S5: Liquidity Thinness
- shallow book
- wide spread

Supports:
- CPS amplification
- OI ↑

---

## SECTION 2: AGENT SIGNALS

### S6: Trade Size Relative to Depth
- large trade vs book

Supports:
- ACS ↑

---

### S7: Wallet Concentration
- few wallets dominate flow

Supports:
- ACS ↑

---

### S8: Local Timing
- wallet enters before move

Supports:
- ACS ↑

---

### S9: Historical Timing
- wallet consistently early

Supports:
- ACS ↑ (strong)

---

### S10: Persistence
- price continues after move

Supports:
- ACS ↑
- OI ↓

---

### S11: Specialization
- wallet focuses on domain

Supports:
- ACS ↑

---

### S12: Consistency
- structured behavior

Supports:
- ACS ↑

---

## SECTION 3: OVERREACTION SIGNALS

### S13: Lack of Persistence
- price fails after spike

Supports:
- OI ↑

---

### S14: Weak Agent Confirmation
- no high-ACS participation

Supports:
- OI ↑

---

### S15: Excessive Move vs Liquidity
- move too large for book

Supports:
- OI ↑

---

## SECTION 4: BOUNDARY SIGNALS

### S16: Price Near 0 or 1
- extreme probability

Triggers:
- boundary logic

---

### S17: Low ACS at Boundary
- crowd likely dominant

Supports:
- fade (low price)
- avoid (high price)

---

### S18: High ACS at Boundary
- credible convergence

Supports:
- follow (high price)

---

## SECTION 5: YES / NO STRUCTURE SIGNALS

### S19: YES-side Credible Flow
- high ACS on YES

Supports:
- follow YES

---

### S20: NO-side Credible Flow
- high ACS on NO

Supports:
- follow NO

---

### S21: Resistance
- opposing side strong

Supports:
- conflict detection

---

## SECTION 6: CORE PRINCIPLE

No signal is sufficient alone.

Signals must be combined to produce:
- CPS
- ACS
- OI

which drive all decisions.