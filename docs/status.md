# Current Status

Last Updated

2026-08-06

---

# Current Phase

Weight Evolution Foundation

目的

Weight Evolution の基盤を完成させる。

現時点では

Human Designed Features

↓

Weight Evolution

↓

Selection

までを対象とする。

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

- Match Library (initial implementation)
- Selection 
- Evolution (evolve_once / evolve) 

---

# Next Task

- Weight 保存フロー
- Generation 管理
- Evolution ログ
- 長時間 Evolution 実験

---

# Future Tasks

Generation管理

Tournament

Weight保存

Benchmark改善

Automatic Evolution

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