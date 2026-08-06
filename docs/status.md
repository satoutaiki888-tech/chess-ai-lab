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

- Streaming Parquet Dataset
- EvaluationSnapshot
- Texel Loss
- Gradient Accumulation
- SGD Optimizer
- Mini-batch SGD
- Validation Loss
- Best Weight Checkpoint
- Resume Training
- ReduceLROnPlateau Scheduler
- Early Stopping
- Learning Rate Logging

---

# Next Task

- 長時間学習
- 学習結果のWeight比較
- Self Playによる評価
- Weight差分可視化
- Optimizer追加（Adam等）
- 正則化

---

# Future Tasks

- より強い評価関数
- Weight Database
- Evolutionとの統合評価

---

# Current Constraints

現在は

Weight Evolution基盤

のみ実装対象。

NNUE

Neural Network

Reinforcement Learning

は対象外。

---

# AI Instructions

作業前に

architecture.md

invariants.md

を確認する。

推測でコードを書き換えない。

必要なファイルは要求する。

1回の変更では1つの目的のみ扱う。