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

---

# In Progress

Evolution

現在

MatchResult が

white_wins

black_wins

draws

になっている。

これはWeight Evolutionには適さない。

---

# Next Task

MatchResult を

parent_wins

child_wins

draws

へ変更する。

その後

play_match()

selfplay_eval.py

を新仕様へ対応する。

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

# Known Issues

MatchResult が色基準である。

Weight比較では

親

子

基準へ変更する必要がある。

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