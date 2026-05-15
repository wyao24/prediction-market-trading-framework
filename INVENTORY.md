# Repository Inventory

## Original Top-Level Files

- `README.md` -> moved to `docs/research/framework_overview.md`
- `project_scope.md` -> moved to `docs/research/project_scope.md`
- `hypotheses.md` -> moved to `docs/research/hypotheses.md`
- `system_architecture.md` -> moved to `docs/architecture/system_architecture.md`
- `regime_and_signal_map.md` -> moved to `docs/strategy/regime_and_signal_map.md`
- `signal_matrix.md` -> moved to `docs/strategy/signal_matrix.md`
- `scoring_framework.md` -> moved to `docs/strategy/scoring_framework.md`
- `decision_engine.md` -> moved to `docs/strategy/decision_engine.md`
- `trade_lifecycle.md` -> moved to `docs/strategy/trade_lifecycle.md`
- `wallet_scoring_rubric.md` -> moved to `docs/strategy/wallet_scoring_rubric.md`
- `probability_weighted_framework.md` -> moved to `docs/strategy/probability_weighted_framework.md`
- `evaluation_framework.md` -> moved to `docs/strategy/evaluation_framework.md`
- `Deep-Research-on-Translating-Equity-Financial-Research-to-Prediction-Markets.txt` -> moved to `reports/Deep-Research-on-Translating-Equity-Financial-Research-to-Prediction-Markets.txt`

## Files Moved

- Research overview and project-scoping docs moved into `docs/research/`.
- System design doc moved into `docs/architecture/`.
- Signal, scoring, decision, sizing, lifecycle, and evaluation docs moved into `docs/strategy/`.
- Long-form external research note moved into `reports/`.

## Ambiguous or Missing Items

- `new_wallet_classification.md` is referenced by the old research overview but is not present in the repository.
- No notebooks, raw datasets, generated datasets, PDFs, or figures were present at implementation time.
- Several legacy research files contain visible encoding artifacts. The scaffold preserves them and documents the issue rather than rewriting research content aggressively.

## Naming and Reference Mismatches

- `framework_overview.md` references `new_wallet_classification.md`, which is missing.
- `framework_overview.md` references `probability_sizing_framework.md`, but the repository contains `probability_weighted_framework.md`.
- `framework_overview.md` references `combined_decision_engine.md`, but the repository contains `decision_engine.md`.

## Possible Duplicates

- No exact duplicates were found.
- `docs/research/framework_overview.md` overlaps conceptually with the lower-level strategy documents but serves as a high-level map rather than a duplicate source of truth.

## Recommended Next Cleanup Steps

- Normalize the moved Markdown research files to clean UTF-8 text and remove remaining mojibake artifacts.
- Add a concise architecture overview in `docs/architecture/` that references the new Python modules directly.
- Split long-form research documents into smaller note-sized documents only after the implementation surface stabilizes.

## Recommended Implementation Priorities

- Replace synthetic inputs with historical replay adapters.
- Add richer wallet-history modeling and cold-start wallet handling.
- Add better paper-simulation assumptions for scaling, exits, and capital tracking.
- Expand evaluation by strategy-context bucket over real replay samples.

