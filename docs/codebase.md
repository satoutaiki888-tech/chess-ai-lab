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

        benchmark/
        
        tuning/

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

- Weight storage
- load_json
- save_json
- copy
- mutate
- to_dict
- from_dict
- to_array
- from_array
- feature_names

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

Current Features

- material
- piece_square
- mobility
- isolated_pawn
- doubled_pawn
- passed_pawn
- king_safety
- bishop_pair
- open_file
- semi_open_file
- pawn_shield
- knight_outpost
- connected_rooks
- rook_seventh
- space
- bishop_mobility
- rook_mobility
- knight_mobility
- queen_mobility

Feature Registry の実行順序は `evaluation/evaluator.py` 側の `FEATURES` を正とする。

Feature Vector はこの順序に従って生成される。

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

# benchmark/

Responsibilities

・EPD Benchmarks
・BenchmarkResult
・Performance Measurement

---

## epd.py

Responsibilities

・EPD読み込み
・EPD解析
・EPDPosition生成

Must Not

・Search
・Weight

---

## evaluator.py
Responsibilities

・1局面評価
・Best Move判定

Must Not

・EPD読込
・集計


---

## runner.py
Responsibilities

・Benchmark全体実行
・BenchmarkResult生成

Must Not

・Mutation
・Selection

---

## result.py
Responsibilities

Benchmark結果保持

positions

solved

accuracy

nodes

elapsed

nps

---

# tuning/

責務

Evaluation Weight を学習する。

Texel Tuning を中心とした学習アルゴリズムを管理する。

---

## dataset.py
Responsibilities

- Streaming Parquet Dataset
- TrainingBatch の生成
- Feature Vector の NumPy 化
- Target / Source Depth の NumPy 化
- Feature Registry metadata validation
- Feature Vector dimension validation
- TrainingPosition への互換展開

Dataset Build 済みの Feature Vector を利用する。

Must Not

- Feature の再計算
- Weight Update
- Loss 計算
- Optimization
- Search

---

## trainer.py

Responsibilities

- Training Loop
- Validation
- Best Weight Save
- Resume Training
- Scheduler Integration
- Mini-batch SGD
- Early Stopping
- Configurable Validation

Must Not

- Dataset Generation
- Feature Implementation
- Search

---

## loss.py
Responsibilities

- Texel Loss
- Target Score
- Probability Conversion

Must Not

- Dataset
- Weight Update
- Search

---

## optimizer.py

Responsibilities

- Update Weight Array
- Learning Rate
- Optimizer State

Must Not

- Dataset
- Loss
- Search

---

## gradient.py

Responsibilities

- Compute Texel gradients
- Compute gradient vector
- Accumulate gradients

Must Not

- Update weights

---

## loss_evaluator.py

Responsibilities

- Evaluate train loss
- Evaluate validation loss

Must Not

- Weight update

---

## lr_scheduler.py

Responsibilities

- ReduceLROnPlateau
- Learning Rate Scheduling

Must Not

- Weight Update
- Dataset

---

## position.py

Responsibilities

- TrainingPosition

Must Not

- Feature calculation
- Weight update

---

## evaluation_snapshot.py

Responsibilities

- Hold evaluated score
- Hold raw feature values
- Hold NumPy feature vector
- Provide immutable evaluation snapshot

Must Not

- Search
- Weight Update

---

## feature_vector.py

Responsibilities

- Snapshot ⇔ NumPy Vector conversion
- Feature ordering
- NumPy Vector との変換

Must Not

- Weight update
- Evaluation

---

## config.py

Responsibilities

- Training configuration
- Development configuration
- Production configuration

Current Configuration

- learning_rate
- epochs
- batch_size
- max_train_samples
- max_valid_samples
- patience
- train_loss_interval
- validation_interval
- best_weight_path
- output_weight_path

Must Not

- Training loop
- Weight update

---

# scripts/

Responsibilities

ライブラリを呼び出す実験コード。

Must Not

ライブラリ処理を持たない。

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

## evolve.py

Responsibilities

- evolve

---

## epd.py

Responsibilities

- epd

---

## benchmark.py

Responsibilities

- 2つの Weight を比較する
- Match 結果を表示する

Must Not

- Mutation
- Selection
- Generation

Evaluate whether benchmark.py and
selfplay_eval.py should be unified.

---

## train.py

Responsibilities

- TrainingConfig の選択
- WeightManager の生成
- Best Weight の Resume
- ParquetDataset の生成
- Trainer の実行
- 最終 Weight の保存

Must Not

- Dataset Generation
- Feature Implementation
- Training Algorithm の実装

---

## build_training_dataset.py

Responsibilities

- Lichess/chess-position-evaluations の読み込み
- Streaming Dataset 処理
- Mate 局面の除外
- Minimum Depth によるフィルタリング
- Centipawn 値の Clamp
- EvaluationSnapshot の生成
- Feature Vector の生成
- Train / Validation 分割
- Parquet への Streaming 保存

Output

- train.parquet
- valid.parquet

Stored Fields

- fen
- target_cp
- source_depth
- feature_values

Parquet metadata として以下を保存する。

- feature_names
- feature_count
- feature_schema_hash

Feature の構成を変更した場合は、この Script を再実行して Training Dataset を再生成する。

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

Evaluation
↓
Tuning

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

Learning Rate

↓

tuning/lr_scheduler.py

---

Training Loop

↓

tuning/trainer.py

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