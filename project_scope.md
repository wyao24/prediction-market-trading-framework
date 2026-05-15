# Project Scope: Prediction Market Trader Classification Strategy

## Objective

Develop high-conviction trading strategies for prediction markets based on identifying and exploiting differences between informed and uninformed (retail-like) order flow.

This project focuses on conceptual development, hypothesis refinement, and signal specification — not implementation.

---

## Target Market

Primary focus: Polymarket

Rationale:
- High retail participation
- Greater behavioral noise and inefficiency
- Richer order flow signals for trader classification

Markets of interest:
- Event-driven binary contracts
- Short- to medium-horizon resolution (hours to weeks)

Kalshi is considered a secondary environment for future validation and robustness testing.

---

## Core Hypothesis

Prediction markets — particularly retail-dominated ones — contain structurally identifiable uninformed flow (e.g., attention-driven, emotional, or urgency-based trading) that generates temporary mispricings.

These mispricings can be systematically detected using order flow and market microstructure signals, and exploited via:

- Mean reversion (fading uninformed flow), and/or  
- Flow-following (tracking informed participants)

---

## Research Approach

The project will follow a broad-to-narrow methodology:

1. Generate a wide set of hypotheses about trader behavior and market inefficiencies  
2. Translate each hypothesis into observable signals  
3. Critically evaluate and eliminate weak or redundant ideas  
4. Refine a small number of high-conviction strategies  

A hybrid approach will be used, allowing multiple strategy types to coexist and compete.

---

## Constraints

- No reliance on fundamental valuation models
- Prices represent probabilities in [0, 1]
- Markets may be thin, fragmented, and retail-dominated
- Information arrival is discrete and event-driven
- Resolution mechanics (rules, wording, timing) may affect pricing

---

## Time Horizon

To be determined on a per-hypothesis basis.

Different strategies may operate on different time scales:
- Microstructure (seconds–minutes)
- Short-term (minutes–hours)
- Event-driven (hours–days)

---

## Success Criteria

A successful outcome of this project is:

- 2–3 high-conviction trading strategies
- Each strategy has:
  - Precise, testable signal definitions
  - Clear economic intuition
  - Identified source of edge
  - Explicit failure modes

- Strategies are sufficiently specified to be:
  - Backtestable
  - Implementable in a later phase

---

## Non-Goals

- No immediate focus on execution systems or infrastructure
- No premature parameter tuning or optimization
- No overfitting to specific historical examples

---

## Key Open Questions

- Can informed trading be reliably detected without a fundamental anchor?
- How do we distinguish fast-reacting retail from genuinely informed traders?
- When does order flow reflect information vs noise?
- How does time-to-resolution affect signal reliability?
- Are order book signals sufficient, or is external data required?
- How do different market categories affect behavior?

---