# Codebase

## Purpose

この文書は chess-ai-lab のコードベース全体を説明する。

目的は

- 各ファイルの責務を明確にする
- AIが適切なファイルを探せるようにする
- 責務の重複を防ぐ

である。

---

# Directory Structure

src/

    chess_ai_lab/

        board.py

        evaluation/

        engine/

        evolution/

tests/

scripts/

---

# Source Tree

## board.py

Layer

Board

Responsibilities

- python-chess wrapper
- Board state
- Move generation
- Undo
- FEN
- Game over

Must Not

- Evaluation
- Search
- Weight

---

# evaluation/

責務

評価関数。

Evaluator と Feature を管理する。

---

## evaluator.py

Responsibilities

- Execute Features
- Get Weights
- Compute Final Score

Must Not

- Search
- Self Play
- Evolution

---

## weight_manager.py

Responsibilities

- Manage Weights
- Save
- Load
- Copy
- Mutate

Must Not

- Evaluate
- Search
- Self Play

---

## features/

Responsibilities

個別Feature。

Rule

1 Feature = 1 File

Current Files

material.py

mobility.py

piece_square.py

pawn_structure.py

king_safety.py

bishop_pair.py

pawn_shield.py

rook_file.py

connected_rooks.py

rook_seventh.py

space.py

bishop_mobility.py

knight_mobility.py

rook_mobility.py

queen_mobility.py

knight_outpost.py

mobility_utils.py

---

# engine/

責務

探索アルゴリズム。

---

## player.py

Interface

choose_move(board)

---

## search.py

Base class。

Responsibilities

- Hold Evaluator
- Node Counter

---

## greedy.py

Greedy Search

---

## minimax.py

Minimax

---

## alphabeta.py

Alpha Beta Search

---

## iterative.py

Iterative Deepening

---

## move_ordering.py

Move Ordering

---

## transposition.py

Transposition Table

---

# evolution/

責務

Weight Evolution。

---

## match.py

Responsibilities

- Self Play
- MatchResult
- play_game()
- play_match()

---

## selection.py

Responsibilities

- MatchResult を評価する
- Parent / Child の採用判定

Must Not

- Self Play
- Mutation
- Weight Save

---

## evolution.py

Responsibilities

- mutate()
- play_match()
- selection()
- evolve_once()
- evolve()

Must Not

- JSON Save
- CLI
- Benchmark

---

## runner.py

Responsibilities

- Evolution実行
- Evolution Strategy 呼び出し
- Generation管理
- Weight保存
- Evolutionログ

Must Not

- Mutation
- Match
- Selection
- Evaluation
- Search

---

## strategy.py

Responsibilities

Evolution Strategy のインターフェース。

Rule

1 Strategy = 1 Evolution Algorithm

Examples

- SimpleEvolutionStrategy
- TournamentStrategy
- GeneticStrategy

---

## simple_strategy.py

Responsibilities

現在採用している進化アルゴリズム。

Flow

Parent

↓

Mutate

↓

Match

↓

Selection

↓

EvolutionResult

Must Not

- Weight保存
- Generation管理
- Evolutionログ

---

## config.py

Responsibilities

Evolution実験の設定。

Examples

- generations
- games
- depth
- mutation_amount
- random_seed

Must Not

- Mutation
- Match
- Search
- Save

---

# scripts/

責務

実験コード。

ライブラリではない。

---

## selfplay_eval.py

Responsibilities

- 2つの Weight を比較する
- Match 結果を表示する

Must Not

- Mutation
- Selection
- Generation

---

# tests/

責務

pytest

Rule

src の変更には対応する Test を追加する。

---

# Dependency Map

Board

↓

Evaluation

↓

Search

↓

Self Play

↓

Evolution

---

# Where To Change

新しい評価関数

↓

evaluation/features/

---

Weight管理

↓

weight_manager.py

---

探索改善

↓

engine/

---

Self Play改善

↓

evolution/

---

Benchmark

↓

scripts/

---

Bug Fix

対象責務のファイルのみ変更する。

責務を跨ぐ変更は禁止。

---

# AI Instructions

コード変更前に

対象責務のファイルを確認する。

変更範囲を最小限にする。

責務が分からない場合は

新しいファイルを作る前に相談する。