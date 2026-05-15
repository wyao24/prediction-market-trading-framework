# Hypothesis Board: Prediction Market Trader Classification

## Framework

This project models prediction-market price formation through different flow-generating archetypes rather than trying to classify every trade as simply "informed" or "uninformed."

The central idea is that alpha comes from identifying which type of process is currently driving price action, and then applying the appropriate strategy.

---

## Core Flow Archetypes

### 1. Mean-Field Crowd Flow
Diffuse, retail-like, urgency-driven, attention-sensitive flow that is best interpreted collectively rather than at the wallet level.

### 2. Conviction Shock Flow
Large, visible, directional trades placed with sufficient size to move price materially. These may reflect information, strong private conviction, or simply aggressive speculative behavior.

### 3. Stealth Accumulation Flow
Repeated, directional, often split trading by a coherent wallet or small set of wallets, suggestive of strategic position building.

---

## Meta-Hypothesis: Regime Classification

Markets alternate between different dominant flow regimes.

The main task is to determine whether current price action is better explained by:

- crowd-like mean-field behavior,
- visible conviction trading,
- or coherent stealth accumulation.

Different strategies should be applied in different regimes.

---

## H1: Crowd Urgency Overreaction

### Intuition
Retail-like participants often trade with urgency, especially in thin books and attention-heavy environments. This creates short-horizon overshoots that are not fully supported by information.

### Observable Features
- one-sided aggressive flow
- rapid price movement over a short interval
- shallow local depth
- weak wallet-level coherence
- lack of strong external information confirmation

### Prediction
Price partially mean-reverts over a short horizon.

### Strategy Type
Fade / short-horizon mean reversion

### Primary Horizon
Fast microstructure

### Failure Modes
- the move is actually information-driven
- the market is near a true repricing event
- liquidity does not recover quickly
- crowd flow cascades into a larger regime shift

---

## H2: Conviction Shock Signal

### Intuition
In prediction markets, informed or highly confident traders may not always hide. Instead, they may place large visible trades when the market is thin enough that speed and conviction matter more than stealth.

### Observable Features
- large visible trade relative to local order book depth
- immediate directional repricing
- wallet-level concentration
- potential follow-through by the same wallet or other strong wallets
- impact that persists rather than instantly reverting

### Prediction
Some conviction shocks represent genuine informational or high-conviction signals and lead to further repricing over a medium horizon.

### Strategy Type
Follow, conditional on confirmation

### Confirmation Layer
A conviction shock is not sufficient by itself. It becomes stronger when combined with:
- persistent price impact
- repeated action by the same wallet
- historically strong wallet profile
- timing near plausible information windows
- inability of opposing flow to reverse the move

### Primary Horizon
Minutes to hours, possibly longer

### Failure Modes
- large trade is simply speculative noise
- wallet is a gambler, manipulator, or non-skilled whale
- move is quickly faded by better-informed participants
- visible size attracts copy-trading without informational content

---

## H3: Stealth Accumulation

### Intuition
Some informed traders may still prefer to build positions gradually to reduce price impact, avoid attention, or preserve edge before the market fully adjusts.

### Observable Features
- repeated directional trades by the same wallet
- order splitting across time
- gradual drift rather than a single jump
- persistent but low-salience price impact
- activity concentrated in a specific market category

### Prediction
Steady accumulation by a coherent wallet can precede continued repricing and may be more informative than isolated large trades.

### Strategy Type
Follow / slow momentum / wallet shadowing

### Primary Horizon
Hours to expiration, depending on contract and timing

### Failure Modes
- pattern is too weak to distinguish from noise
- apparent persistence is just repeated speculation
- market adjusts before signal is recognized
- wallet is copying others rather than leading

---

## H4: Boundary and Longshot Bias Effects

### Intuition
Prediction-market prices near 0 or 1 may be distorted by crowd psychology, especially longshot bias, overconfidence, or panic near the payoff boundaries.

### Observable Features
- contracts trading near extreme probabilities
- asymmetric book behavior near 0/1
- persistent willingness to overpay for low-probability upside
- unstable response to moderate trades near the boundary

### Prediction
Order flow near the boundaries is not interpreted linearly. Crowd flow may become more biased, and visible conviction may carry different meaning when prices are already extreme.

### Strategy Type
Context-dependent; likely strongest as a modifier on other signals rather than a standalone strategy

### Primary Horizon
Depends on contract stage and time-to-resolution

### Failure Modes
- extreme prices are actually justified
- resolution mechanics dominate behavioral effects
- low liquidity makes boundary behavior hard to distinguish from noise

---

## H5: Wallet Specialization Edge

### Intuition
The most informative wallets may not be those with the highest raw PnL, but those with persistent success within a narrow market domain.

### Observable Features
- repeated success in one category or contract type
- early entries before repricing
- coherent directional behavior
- persistence across related markets

### Prediction
Category-specialized wallets are more likely to possess genuine informational or structural edge and are more worth tracking than generalist or one-off winners.

### Strategy Type
Wallet ranking / signal weighting / shadow-following

### Primary Horizon
Medium to long, depending on the underlying strategy

### Failure Modes
- sample size too small
- luck mistaken for edge
- strategy decay after public detection
- category edge fails to generalize

---

## Working Research Priorities

### Primary
- H2: Conviction Shock Signal
- H1: Crowd Urgency Overreaction
- H5: Wallet Specialization Edge

### Secondary
- H3: Stealth Accumulation

### Modifier / Context Layer
- H4: Boundary and Longshot Bias Effects

---

## Research Philosophy

Informed flow is best modeled at the wallet level, where persistent behavior, specialization, and timing can reveal coherent agent structure.

Retail-like flow is best modeled as a mean-field process, where collective urgency, attention, and behavioral bias generate short-horizon dislocations.

The objective is not to label all traders. The objective is to determine whether price action is currently better explained by:
- diffuse crowd behavior,
- visible conviction by a coherent agent,
- or gradual stealth accumulation.

Trading strategies should then be conditioned on that classification.