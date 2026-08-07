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

---

# Next Task

- Snapshot Parquet Cache
- Snapshot Streaming Dataset
- Long Training Benchmark
- Weight Comparison
- Self Play Evaluation
- Weight Difference Visualization
- Adam Optimizer
- Regularization

---

# Future Tasks

- より強い評価関数
- Weight Database
- Feature Cache Versioning
- Snapshot Compression
- Parallel Training
- Distributed Self Play

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