# Current Status

Last Updated

2026-08-06

---

# Completed

Board

- ChessBoard wrapper
- Move generation
- Undo
- FEN

Evaluation

- Feature Registry
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

- EvaluationSnapshot を用いた特徴量取得
- Texel Loss の実装
- 勾配計算
- SGD Optimizer
- ミニバッチSGD
- Validation Loss計測
- Best Weight保存
- Resume Training
- ReduceLROnPlateauScheduler
- Early Stopping
- Learning Rate表示

---

# Next Task

- 長時間学習
- Weight差分可視化
- Optimizer追加（Adam等）
- 正則化

---

# Future Tasks

- 作ったAIがそこそこの強さになること
- Weight Database

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

pytest green を維持する。