# Scoring Framework

## Objective

Define how signals are combined into:

- Crowd Pressure Score (CPS)
- Agent Credibility Score (ACS)
- Overreaction Indicator (OI)

across different time horizons.

---

## SECTION 1: SCORE DEFINITIONS

### CPS (Crowd Pressure Score)
Measures:
- urgency
- imbalance
- dispersion

---

### ACS (Agent Credibility Score)
Measures:
- quality of participating wallets
- timing
- conviction
- persistence

---

### OI (Overreaction Indicator)
Measures:
- whether move is excessive relative to conditions

---

## SECTION 2: FAST HORIZON

### CPS_fast
Driven by:
- imbalance
- aggression
- dispersion

---

### ACS_fast
Weak signal:
- size
- early timing

---

### OI_fast
- large move
- thin liquidity
- no confirmation

---

## SECTION 3: MID HORIZON

### CPS_mid
- reversal behavior

---

### ACS_mid
- persistence
- repeated wallet behavior

---

### OI_mid
- failure to persist

---

## SECTION 4: SLOW HORIZON

### ACS_slow dominates
- repeated correctness
- wallet credibility

---

### CPS_slow weak

---

### OI_slow minimal

---

## SECTION 5: SCORE INTERPRETATION

### High CPS + High OI + Low ACS
→ Fade

---

### High ACS + Persistence
→ Follow

---

### Boundary + Low ACS
→ Fade low prices

---

### Boundary + High ACS
→ Follow high prices

---

## SECTION 6: CORE PRINCIPLE

Scores are not absolute.

They are interpreted relative to:
- each other
- context
- horizon