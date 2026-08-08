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

# Next Task

## 1. Training Dataset / Trainer Integration

- Parquet に保存した feature_values を ParquetDataset が読み込む
- Trainer が保存済み Feature Vector を直接利用する
- Training 中の Feature 再計算を完全に排除する
- Feature Vector と Weight の次元数を検証する
- Feature Registry のバージョン不一致を検出できるようにする

## 2. Training Benchmark

- 100,000 positions を使用した長時間 Training Benchmark
- Dataset / Evaluation / Gradient / Optimizer の実測
- Feature 再計算方式との速度比較
- Parquet Feature Vector 方式の速度確認

## 3. Weight Evaluation

- Weight Comparison
- Self Play Evaluation
- Weight Difference Visualization

---

# Future Tasks

- より強い評価関数
- Weight Database
- Feature Cache Versioning
- Snapshot Compression
- Parallel Training
- Distributed Self Play

---

# Current Training Result

Dataset

- Source: Lichess/chess-position-evaluations
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

Training

- Epochs: 100
- Batch size: 1024
- Learning rate: 0.1
- Final validation loss: 0.026720
- Best validation loss during this run: 0.026720

Performance

Parquet access and batch preparation are now substantially faster than the previous on-the-fly feature evaluation approach.

Detailed benchmark comparison remains a future task.

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