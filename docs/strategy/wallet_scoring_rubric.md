# Wallet Scoring Rubric

## Objective

Assign each wallet an Agent Credibility Score (ACS) based on:

- timing
- size
- historical behavior
- specialization
- consistency

---

## SECTION 1: FILTERING LAYER

Only score wallets that:

- trade meaningful size relative to liquidity
- participate more than once
- show directional commitment

---

## SECTION 2: SCORING COMPONENTS

### 1. Timing (Highest Weight)

#### Local Timing
- entry before price move

#### Historical Timing
- consistently early across trades

---

### 2. Size / Conviction

- trade size relative to depth
- concentrated exposure

---

### 3. PnL (Low Weight)

- consistent profitability
- normalized (avoid longshot bias)

---

### 4. Specialization

- focused on specific category
- consistent domain behavior

---

### 5. Consistency

- repeated structured behavior
- similar trade patterns

---

## SECTION 3: CONTEXT ADJUSTMENTS

### Category
- retail-heavy → stricter threshold
- info-heavy → lower threshold

---

### Sample Size
- fewer trades → reduce confidence

---

### Time Decay
- recent behavior weighted more

---

## SECTION 4: OUTPUT

Wallet assigned:

- High ACS → follow candidate
- Medium ACS → monitor
- Low ACS → ignore

---

## SECTION 5: CORE PRINCIPLE

Wallets are not labeled as “retail” or “informed”.

Instead:

> they are assigned a dynamic credibility score based on behavior