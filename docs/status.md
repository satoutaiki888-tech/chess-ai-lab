# Current Status

Last Updated

2026-08-10

---

# Current Phase

## Phase

AI Collaboration Infrastructure / Documentation Organization

## Current State

The core Board, Evaluation, Search, Evolution, Benchmark, and Texel Tuning foundations are implemented.

The current development focus is improving reproducibility, documentation, testing discipline, and AI collaboration so future implementation work can be resumed without relying on previous chat history.

The runtime implementation is not changed by this documentation phase.

---

# Current Focus

1. Maintain the AI development entry and workflow documentation.
2. Keep architecture and invariants synchronized with the actual implementation.
3. Improve Test coverage and architecture verification.
4. Record important Training / Tuning / Benchmark experiments in `docs/experiments/`.
5. Keep this file focused on current state and next actions rather than historical experiment detail.

---

# Completed

## Board

- ChessBoard wrapper
- Move generation
- Undo
- FEN

## Evaluation

- Feature Registry
- EvaluationSnapshot
- Evaluator
- WeightManager

## Search

- Greedy
- Minimax
- AlphaBeta
- Iterative Deepening
- Move Ordering
- Transposition Table

## Features

- Material
- Piece Square
- Mobility
- Pawn Structure
- King Safety
- Bishop Pair
- Pawn Shield
- Rook File
- Connected Rooks
- Rook Seventh
- Space
- Knight Outpost
- Bishop Mobility
- Knight Mobility
- Rook Mobility
- Queen Mobility

## Evolution

- Match Library
- Selection
- Evolution
- Evolution Runner
- Evolution Strategy
- Evolution Config
- Weight Save
- Generation Save
- JSON Evolution Log
- Resume Foundation

## Benchmark

- EPD parser
- EPD loader
- Single position evaluation
- Benchmark runner
- Benchmark result

## Texel Tuning

- Parquet Dataset
- TrainingBatch
- In-memory Dataset Cache
- TrainingPosition
- EvaluationSnapshot
- NumPy Feature Vector
- Texel Loss
- Gradient Computation
- Mini-batch SGD
- Validation Loss
- Best Weight Checkpoint
- Resume Training
- Fresh Training
- ReduceLROnPlateau Scheduler
- Early Stopping
- Learning Rate Logging
- Configurable Training
- Configurable Training Dataset Directory
- Training Dataset Builder
- Train / Validation Parquet Generation
- Feature Vector Parquet Serialization
- Feature Registry metadata
- Feature schema validation
- 500,000 position dataset generation
- Train 449,662 positions
- Validation 50,338 positions

---

# Current Training Result

## Dataset

Source

- Lichess/chess-position-evaluations

Current Dataset

- Maximum samples: 500,000
- Minimum Stockfish depth: 20
- CP limit: ±1000
- Train ratio: 0.9
- Seed: 42
- Buffer size: 5,000

Generated Dataset

- Total: 500,000
- Train: 449,662
- Validation: 50,338

Feature Vector

- Feature count: 19
- Stored in Parquet as `feature_values`
- Feature Registry metadata stored in Parquet
- Feature schema hash stored in Parquet

---

## Dataset Loading

Training and validation datasets are loaded into memory before the first training epoch.

Training Dataset

- 449,662 samples
- Initial load: approximately 6.4–6.8 sec

Validation Dataset

- 50,338 samples
- Current training configuration loads 10,000 validation samples
- Initial load: approximately 0.6–0.7 sec

After loading, the dataset is reused across epochs.

The Parquet files are not reopened for every epoch.

This removes repeated Parquet I/O from the main training loop.

---

## Training Configuration

### Last Recorded Experiment

- Fresh training
- Dataset: `data/training_500k`
- Learning rate: 1.0
- Epochs: 100
- Batch size: 1024
- Training samples: 449,662
- Validation samples: 10,000
- Validation interval: 5
- Train loss interval: 10
- Patience: 10

### Current Code Configuration

The current `PRODUCTION_CONFIG` is:

- Learning rate: 5.0
- Epochs: 100
- Batch size: 4096
- Training samples: unlimited (`None`)
- Validation samples: 10,000
- Validation interval: 5
- Train loss interval: 10
- Patience: 10

The current production configuration is defined in `src/chess_ai_lab/tuning/config.py`.

The training entry point uses `PRODUCTION_CONFIG` directly.

Therefore, the last recorded LR=1.0 experiment and the current default training configuration must be treated as separate states.

Initial weights for a fresh run are the built-in evaluation weights.

Training can also resume from `weights/best_weight.json` when `--fresh` is not specified.

Initial weights

- Built-in evaluation weights
- Training started with `--fresh`

---

## Training Result

Best validation loss

- Validation loss: 0.024605
- Epoch: 100

Final training loss

- Train loss: 0.024462

Final validation loss

- Validation loss: 0.024605

The LR=1.0 experiment improved validation loss relative to the earlier LR=0.1 experiment.

However, the difference in validation loss alone does not establish a corresponding increase in playing strength.

Detailed experiment information belongs in `docs/experiments/`.

---

## Training Performance

Previous implementation

- Dataset was reopened/read during training epochs
- 100 epoch experiments took several minutes

Current implementation

- Dataset loaded once into memory
- Training data reused across epochs
- Dataset processing is effectively removed from epoch timing

Typical epoch benchmark

- Total: approximately 0.03–0.08 sec
- Evaluation: approximately 0.006–0.017 sec
- Gradient: approximately 0.024–0.059 sec
- Optimizer: approximately 0.000–0.002 sec

The current bottleneck is gradient computation, not Parquet loading.

This makes repeated hyperparameter experiments substantially cheaper.

---

# Next Tasks

## Immediate

- Add or strengthen architecture verification Tests where dependency rules can be checked mechanically.
- Keep Test guidance in `docs/testing.md` synchronized with actual Test structure.
- Record new Training / Tuning experiments under `docs/experiments/`.

## Evaluation / Training

- Validate current `PRODUCTION_CONFIG` with Learning Rate = 5.0.
- Run controlled Learning Rate comparisons under identical conditions.
- Evaluate promising trained weights with identical WAC / Self-play conditions before drawing playing-strength conclusions.

## Documentation

- Keep `architecture.md`, `invariants.md`, and `codebase.md` aligned with implementation.
- Update this file when a development milestone or current task changes.
- Do not accumulate detailed historical experiment logs here; use `docs/experiments/` instead.

---

# Important Notes

- `docs/AI_CONTEXT.md` is the project-level AI context entry.
- `AGENTS.md` defines AI development rules.
- `docs/ai_workflow.md` defines the AI collaboration workflow.
- `docs/decisions.md` records important design rationale.
- `docs/testing.md` defines Test strategy.
- `docs/experiments/` contains detailed experiment records.
- `docs/changelog.md` contains important project-level changes.

When these documents conflict, do not guess. Stop and reconcile the source of truth explicitly.
