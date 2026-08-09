# Current Status

Last Updated

2026-08-07

---

# Completed

Board

- ChessBoard wrapper
- Move generation
- Undo
- FEN

Evaluation

- Feature Registry
- EvaluationSnapshot
- Evaluator
- WeightManager

Search

- Greedy
- Minimax
- AlphaBeta
- Iterative Deepening
- Move Ordering
- Transposition Table

Features

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

Evolution

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

Benchmark

- EPD parser
- EPD loader
- Single position evaluation
- Benchmark runner
- Benchmark result

Texel Tuning

Texel Tuning

- Streaming Parquet Dataset
- TrainingPosition
- EvaluationSnapshot
- NumPy Feature Vector
- Texel Loss
- Gradient Computation
- Mini-batch SGD
- Validation Loss
- Best Weight Checkpoint
- Resume Training
- ReduceLROnPlateau Scheduler
- Early Stopping
- Learning Rate Logging
- Configurable Training
- Training Dataset Builder
- Train / Validation Parquet Generation
- Feature Vector Parquet Serialization
- 100,000 position dataset generation
- Train 89,924 positions
- Validation 10,076 positions

---

# Current Training Result

## Dataset

Source

- Lichess/chess-position-evaluations

Current Dataset

- Maximum samples: 100,000
- Minimum Stockfish depth: 20
- CP limit: ±1000
- Train ratio: 0.9
- Seed: 42
- Buffer size: 5,000

Generated Dataset

- Total: 100,000
- Train: 89,924
- Validation: 10,076

Feature Vector

- Feature count: 19
- Stored in Parquet as `feature_values`
- Feature Registry metadata stored in Parquet
- Feature schema hash stored in Parquet

---

# Current Training

Configuration

- Epochs: 100
- Batch size: 1024
- Learning rate: 0.1
- Validation interval: 5
- Train loss interval: 10
- Patience: 10
- Production configuration

Training Result

- Final validation loss: 0.026262
- Best validation loss: 0.026262
- Best validation loss occurred at epoch 100

Validation Loss Trend

- Epoch 60: 0.026328
- Epoch 65: 0.026319
- Epoch 70: 0.026311
- Epoch 75: 0.026302
- Epoch 80: 0.026294
- Epoch 85: 0.026286
- Epoch 90: 0.026278
- Epoch 95: 0.026270
- Epoch 100: 0.026262

The validation loss continued to improve slowly
through the end of the 100 epoch run.

---

# Weight Benchmark

WAC Benchmark

Dataset

- data/wac.epd
- Limit: 32 positions

## Built-in Weight

Configuration

- Weight: built-in FEATURE_WEIGHTS
- Depth: 2
- Positions: 32

Result

- Solved: 6
- Accuracy: 18.8%
- Nodes: 41,160
- NPS: approximately 1,948

## Trained Weight

Configuration

- Weight: weights_trained.json
- Depth: 2
- Positions: 32

Result

- Solved: 6
- Accuracy: 18.8%
- Nodes: 41,160
- NPS: approximately 1,712

## Trained Weight / Depth 3

Configuration

- Weight: weights_trained.json
- Depth: 3
- Positions: 32

Result

- Solved: 8
- Accuracy: 25.0%
- Nodes: 474,687
- NPS: approximately 1,697
- Time: 279.59 sec

---

# Current Interpretation

The current WAC benchmark does not yet demonstrate
a clear strength improvement from the trained weights.

At depth 2, built-in and trained weights produced the
same 18.8% accuracy on the first 32 WAC positions.

The depth 3 benchmark with trained weights reached 25.0%,
but this result is not directly comparable to the depth 2 results.

The current benchmark sample is too small to draw a strong
conclusion about the quality of the trained weights.

Validation loss improvement is also very small across the
100 epoch run.

Therefore the current results should be treated as an
experimental baseline rather than a validated improvement.

---

# Current Investigation

The following questions are currently under investigation.

1. Is the current Training Dataset large and diverse enough?
2. Is the Train / Validation split sufficiently independent?
3. Is repeated tuning on the same dataset causing overfitting
   to the validation set?
4. Is the current learning rate and tuning duration sufficient?
5. Are the learned weights materially different from the
   built-in weights?
6. Does lower Texel validation loss correlate with stronger
   chess playing performance?
7. Does WAC accuracy improve when evaluated on a larger
   benchmark set?

---

# Current Constraints

Out of Scope

- NNUE
- Deep Learning
- Reinforcement Learning

---

# AI Instructions

作業前に

architecture.md

invariants.md

を確認する。

推測でコードを書き換えない。

必要なファイルは要求する。

1回の変更では1つの目的のみ扱う。

---

# Next Task

## 1. Rebuild a Larger Training Dataset

Create a new sufficiently large Training Dataset.

The new Dataset must be treated as a new experimental artifact.

Record:

- Source
- Maximum samples
- Minimum depth
- CP limit
- Train / Validation split
- Random seed
- Feature Registry
- Feature schema hash

---

## 2. Fresh Tuning Run

Run tuning from the initial built-in weights.

Do not resume from the previous trained weights.

Record:

- initial weights
- learning rate
- epochs
- batch size
- validation interval
- training loss
- validation loss
- best epoch
- final weights

---

## 3. Independent Weight Evaluation

Evaluate built-in and trained weights using the same benchmark conditions.

At minimum record:

- Weight
- Dataset
- Depth
- Positions
- Accuracy
- Nodes
- NPS
- Elapsed time

Do not compare results produced with different
benchmark conditions as if they were equivalent.

---

## 4. Benchmark Before / After Tuning

For the same WAC configuration:

```text
Built-in Weight
      ↓
Benchmark
      ↓
Freshly Tuned Weight
      ↓
Benchmark

The benchmark condition must remain identical.