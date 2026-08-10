# Codebase

## Purpose

この文書は `chess-ai-lab` のコードベース全体を説明する。

目的は以下の3つである。

- 各ファイルの責務を明確にする
- AIが変更対象のファイルを正しく判断できるようにする
- 責務の重複・不要な依存・無関係な変更を防ぐ

この文書は「どのコードがどの責務を持つか」を定義する。

設計上の不変条件は `docs/invariants.md`、
現在のアーキテクチャは `docs/architecture.md`、
現在の進捗と次の作業は `docs/status.md`
を正とする。

---

# Directory Structure

```
src/
└── chess_ai_lab/
    ├── board.py
    │
    ├── evaluation/
    │   ├── evaluator.py
    │   ├── result.py
    │   ├── weight_manager.py
    │   └── features/
    │
    ├── engine/
    │   ├── player.py
    │   ├── search.py
    │   ├── greedy.py
    │   ├── minimax.py
    │   ├── alphabeta.py
    │   ├── iterative.py
    │   ├── move_ordering.py
    │   └── transposition.py
    │
    ├── evolution/
    │   ├── match.py
    │   ├── selection.py
    │   ├── evolution.py
    │   ├── runner.py
    │   ├── strategy.py
    │   ├── simple_strategy.py
    │   └── config.py
    │
    ├── benchmark/
    │   ├── epd.py
    │   ├── evaluator.py
    │   ├── runner.py
    │   └── result.py
    │
    └── tuning/
        ├── dataset.py
        ├── trainer.py
        ├── loss.py
        ├── loss_evaluator.py
        ├── gradient.py
        ├── optimizer.py
        ├── lr_scheduler.py
        ├── position.py
        ├── evaluation_snapshot.py
        ├── feature_vector.py
        ├── weight_vector.py
        ├── config.py
        └── benchmark.py

tests/

scripts/
```

---

# Source Tree

# board.py

## Responsibilities

* `python-chess` を利用した盤面管理
* Board state の保持
* 合法手生成
* 手の適用
* Undo
* FEN取得
* 終局判定

## Must Not

* Evaluation
* Search
* Weight management
* Training
* Evolution

---

# evaluation/

## Responsibilities

評価関数全体を管理する。

主な責務は以下である。

* Feature Registry
* Feature execution
* Weight application
* EvaluationSnapshot
* Weight management

---

## evaluator.py

## Responsibilities

* Feature Registry の実行
* Feature raw score の取得
* Weight の取得
* Weight 適用後の `EvaluationResult` 生成
* 最終評価値の計算
* `EvaluationSnapshot` の生成
* 学習用 Feature Vector の生成

`Evaluator` は Feature と Weight を統合する主要コンポーネントである。

`evaluate_detail()` は Feature ごとの
weighted score と total を `EvaluationResult` として返す。

`snapshot()` は Dataset Build や学習用途のために、

* total
* raw_features
* feature_vector

を `EvaluationSnapshot` として返す。

## Must Not

* Search
* Self Play
* Evolution
* Training loop
* Weight の永続化

---

## result.py

## Responsibilities

Feature ごとの評価結果と最終評価値を保持する。

主な責務:

* Feature ごとの weighted score の保持
* Feature 名と評価値の対応管理
* 全 Feature の評価値の合計管理

`Evaluator.evaluate_detail()` が生成する評価結果のデータ構造として利用する。

## Must Not

* Feature calculation
* Weight management
* Search
* Training
* Evolution

---

## weight_manager.py

## Responsibilities

* Weight の保持
* Weight の取得
* Weight の更新
* JSON load
* JSON save
* Copy
* Mutation
* Dictionary conversion
* NumPy array conversion
* Feature name 管理

## Must Not

* Board evaluation
* Search
* Self Play
* Training loop

---

# evaluation/features/

## Responsibilities

個別の評価 Feature を実装する。

Feature は raw score を返し、
Weight や最終評価値を管理しない。

Feature の実行順序と Feature Vector の順序は
`FEATURES` Registry を正とする。

## Feature File Design

現在の実装では、

1 Registry entry = 1 independent feature calculation

であり、必ずしも

1 Feature = 1 File

ではない。

複数の関連 Feature を1ファイルにまとめる場合がある。

現在の構成では、例えば以下のように複数の Registry entry が
同一モジュールに実装されている。

pawn_structure.py
├── evaluate_isolated_pawn
├── evaluate_doubled_pawn
└── evaluate_passed_pawn

rook_file.py
├── evaluate_open_file
└── evaluate_semi_open_file
Current Feature Registry

FEATURES に登録されている Feature は以下の19個である。

material
piece_square
mobility
isolated_pawn
doubled_pawn
passed_pawn
king_safety
bishop_pair
open_file
semi_open_file
pawn_shield
knight_outpost
connected_rooks
rook_seventh
space
bishop_mobility
rook_mobility
knight_mobility
queen_mobility

Feature Vector のインデックスは、この Registry の順序に従う。

Current Feature Modules
features/
├── material.py
├── piece_square.py
├── mobility.py
├── pawn_structure.py
├── king_safety.py
├── bishop_pair.py
├── rook_file.py
├── pawn_shield.py
├── knight_outpost.py
├── connected_rooks.py
├── rook_seventh.py
├── space.py
├── bishop_mobility.py
├── rook_mobility.py
├── knight_mobility.py
└── queen_mobility.py
Must Not
WeightManager を直接利用しない
Search を行わない
Weight を変更しない
Board state を変更しない
他 Feature の計算結果に依存しない

---

# engine/

## Responsibilities

Chess search を担当する。

* Move search
* Node counting
* Move ordering
* Alpha-Beta
* Iterative Deepening
* Transposition Table

Search は `Evaluator` を通して局面を評価する。

Feature を直接利用しない。

---

## player.py

## Responsibilities

Search player のインターフェースを定義する。

主なインターフェース:

```text
choose_move(board)
```

## Must Not

* Feature の直接実行
* Weight の直接管理

---

## search.py

## Responsibilities

Search の基底クラスを提供する。

* Evaluator の保持
* Node Counter
* Search 共通処理

## Must Not

* Feature の直接実行
* Weight の変更

---

## greedy.py

## Responsibilities

Greedy search を実装する。

---

## minimax.py

## Responsibilities

Minimax search を実装する。

---

## alphabeta.py

## Responsibilities

Alpha-Beta search を実装する。

---

## iterative.py

## Responsibilities

Iterative Deepening を実装する。

---

## move_ordering.py

## Responsibilities

Search の Move Ordering を実装する。

---

## transposition.py

## Responsibilities

Transposition Table を管理する。

---

# evolution/

## Responsibilities

Evaluation Weight の進化を担当する。

主な構成:

```text
Parent
  ↓
Mutation
  ↓
Match
  ↓
Selection
  ↓
EvolutionResult
```

---

## match.py

## Responsibilities

* Self Play
* MatchResult
* `play_game()`
* `play_match()`

## Must Not

* Mutation
* Selection
* Weight Save
* Generation management

---

## selection.py

## Responsibilities

* MatchResult の評価
* Parent / Child の採用判定

## Must Not

* Self Play
* Mutation
* Weight Save
* Generation management

---

## evolution.py

## Responsibilities

* Mutation
* Match
* Selection
* `evolve_once()`
* `evolve()`

## Must Not

* JSON Save
* CLI
* Benchmark
* Generation logging

---

## runner.py

## Responsibilities

* Evolution 実行
* Strategy 呼び出し
* Generation 管理
* Weight 保存
* Evolution ログ

## Must Not

* Mutation の実装
* Match の実装
* Selection の実装
* Evaluation の実装
* Search の実装

---

## strategy.py

## Responsibilities

Evolution Strategy のインターフェースを定義する。

## Rule

```text
1 Strategy = 1 Evolution Algorithm
```

Examples:

* SimpleEvolutionStrategy
* TournamentStrategy
* GeneticStrategy

Strategy は1世代の進化処理を担当する。

## Must Not

* Weight 保存
* Generation 管理
* Evolution ログ

---

## simple_strategy.py

## Responsibilities

現在採用している Evolution Strategy を実装する。

Flow:

```text
Parent
  ↓
Mutate
  ↓
Match
  ↓
Selection
  ↓
EvolutionResult
```

## Must Not

* Weight 保存
* Generation 管理
* Evolution ログ

---

## config.py

## Responsibilities

Evolution 実験の設定を保持する。

主な設定:

* generations
* games
* depth
* mutation_amount
* random_seed

## Must Not

* Mutation
* Match
* Search
* Save

---

# benchmark/

## Responsibilities

Engine の性能・探索精度を測定する。

主な責務:

* EPD loading
* Position evaluation
* Best move comparison
* Accuracy
* Nodes
* NPS
* Elapsed time
* BenchmarkResult

Benchmark は Weight を変更しない。

---

## epd.py

## Responsibilities

* EPD 読み込み
* EPD 解析
* EPDPosition 生成

## Must Not

* Search implementation
* Weight mutation

---

## evaluator.py

## Responsibilities

* 1局面の探索
* Best Move 判定
* Position-level benchmark result の生成

## Must Not

* EPD file loading
* Result aggregation
* Mutation
* Selection

---

## runner.py

## Responsibilities

* Benchmark 全体の実行
* 複数局面の処理
* `BenchmarkResult` の生成

## Must Not

* Mutation
* Selection
* Evolution

---

## result.py

## Responsibilities

Benchmark 結果を保持する。

主な値:

* positions
* solved
* accuracy
* nodes
* elapsed
* nps

---

# tuning/

## Responsibilities

Evaluation Weight をデータから学習する。

現在は Texel Tuning を中心とする。

主な処理:

```text
Parquet Dataset
      ↓
NumPy Feature Matrix
      ↓
Mini-batch SGD
      ↓
Gradient
      ↓
Optimizer
      ↓
Updated Weight
```

Training は Dataset Build と分離されている。

---

## dataset.py

## Responsibilities

Parquet Training Dataset を読み込む。

主な責務:

* Parquet 読み込み
* `TrainingBatch` 生成
* Feature Matrix の NumPy 化
* Target の NumPy 化
* Source Depth の NumPy 化
* Feature Registry metadata validation
* Feature Vector dimension validation
* `TrainingPosition` への互換展開
* Dataset の in-memory cache

Dataset Build 済みの Feature Vector を利用する。

Training 中に Feature を再計算しない。

## Must Not

* Feature の再計算
* Weight Update
* Loss Calculation
* Optimization
* Search

---

## trainer.py

## Responsibilities

Training 全体を管理する。

主な責務:

* Training Loop
* Dataset の初期ロード
* In-memory NumPy Array の準備
* Mini-batch SGD
* Validation
* Loss Evaluation
* Learning Rate Scheduler
* Best Weight Checkpoint
* Early Stopping
* Training 結果のログ

現在の Training は開始時に Dataset をメモリへロードし、
各 epoch では NumPy 配列を再利用する。

これにより epoch ごとの Parquet I/O を発生させない。

## Must Not

* Dataset Generation
* Feature Implementation
* Search
* Self Play

---

## loss.py

## Responsibilities

Texel Loss に関する数学処理を提供する。

* Score → Probability conversion
* Target probability conversion
* Texel Loss

## Must Not

* Dataset access
* Weight update
* Search

---

## loss_evaluator.py

## Responsibilities

* Training Loss の計算
* Validation Loss の計算

Weight を更新せず、現在の Weight に対する Loss を評価する。

## Must Not

* Weight Update
* Dataset Generation
* Search

---

## gradient.py

## Responsibilities

* Texel gradient の計算
* Gradient vector の生成
* Batch gradient の計算

## Must Not

* Weight update
* Optimizer state management

---

## optimizer.py

## Responsibilities

* Weight Array の更新
* Learning Rate の保持
* Optimizer state の管理

現在の主な Optimizer:

* SGD

## Must Not

* Dataset access
* Loss calculation
* Gradient calculation
* Search

---

## lr_scheduler.py

## Responsibilities

Learning Rate のスケジューリング。

現在の方式:

* ReduceLROnPlateau

主な責務:

* Validation Loss の監視
* Learning Rate の削減
* Minimum Learning Rate の制御

## Must Not

* Weight Update
* Dataset access
* Loss calculation

---

## position.py

## Responsibilities

`TrainingPosition` データ構造を提供する。

保持対象:

* Board
* Target CP
* Source Depth
* Feature Values

## Must Not

* Feature calculation
* Weight update
* Search

---

## evaluation_snapshot.py

## Responsibilities

学習用の Evaluation Snapshot を保持する。

主な情報:

* total
* raw_features
* feature_vector

Feature Vector は Feature Registry の順序で保持する。

## Must Not

* Search
* Weight Update

---

## feature_vector.py

## Responsibilities

EvaluationSnapshot と NumPy Feature Vector の変換を管理する。

主な責務:

* Feature ordering
* Snapshot → NumPy Vector
* NumPy Vector → Feature representation

## Must Not

* Weight update
* Evaluation execution

---

## weight_vector.py

## Responsibilities

Training 用 Weight の NumPy 表現を管理する。

主な責務:

* WeightManager → NumPy Array
* NumPy Array → WeightManager
* Optimizer が扱う Weight Vector の提供

## Must Not

* Feature calculation
* Loss calculation
* Search

---

## config.py

## Responsibilities

Training 実験の設定を保持する。

主な設定:

* learning_rate
* epochs
* batch_size
* max_train_samples
* max_valid_samples
* patience
* train_loss_interval
* validation_interval
* best_weight_path
* output_weight_path

Development 用と Production 用の設定を分離する。

## Must Not

* Training loop
* Weight update
* Dataset generation

---

## benchmark.py

## Responsibilities

Training 処理の性能を測定する。

主な計測項目:

* Dataset
* Evaluation
* Gradient
* Optimizer
* Total

現在の Training では Dataset が事前にメモリへロードされるため、
epoch 内の Dataset コストは基本的に発生しない。

---

# scripts/

## Responsibilities

ライブラリを呼び出して実験を実行する。

Scripts は実験の入口であり、
本体のアルゴリズムを実装しない。

## Must Not

* Core library logic
* Feature implementation
* Search implementation
* Training algorithm implementation
* Evolution algorithm implementation

---

## selfplay_eval.py

## Responsibilities

* 2つの Weight を比較する
* Self Play を実行する
* Match 結果を表示する

## Must Not

* Mutation
* Selection
* Generation management

---

## evolve.py

## Responsibilities

Evolution 実験を開始する。

Evolution library を呼び出し、
結果を表示・保存する。

---

## epd.py

## Responsibilities

EPD 関連処理の CLI entry point。

---

## benchmark.py

## Responsibilities

* 2つの Weight を比較する
* Benchmark を実行する
* Match / benchmark 結果を表示する

## Must Not

* Mutation
* Selection
* Generation management

`benchmark.py` と `selfplay_eval.py` の責務には一部重複がある。

統合は将来の整理候補だが、
現在は不要なリファクタリングを行わない。

---

## train.py

## Responsibilities

* TrainingConfig の選択
* WeightManager の生成
* `--fresh` / Resume の選択
* Training Dataset Directory の選択
* `ParquetDataset` の生成
* Trainer の実行
* 最終 Weight の保存

## Must Not

* Dataset Generation
* Feature Implementation
* Training Algorithm の実装

---

## build_training_dataset.py

## Responsibilities

Training Dataset を生成する。

主な処理:

* `Lichess/chess-position-evaluations` の読み込み
* Streaming Dataset 処理
* Mate 局面の除外
* Minimum Depth filtering
* Centipawn Clamp
* EvaluationSnapshot の生成
* Feature Vector の生成
* Train / Validation split
* Parquet streaming write

## Output

```text
train.parquet
valid.parquet
```

## Stored Fields

```text
fen
target_cp
source_depth
feature_values
```

## Parquet Metadata

```text
feature_names
feature_count
feature_schema_hash
```

Feature Registry を変更した場合は、
対応する Training Dataset を再生成する。

---

# tests/

## Responsibilities

pytest によるコード検証を行う。

## Rules

* src の変更には対応する Test を追加・更新する
* Bug 修正には可能な限り再発防止 Test を追加する
* 既存 Test を理由なく削除しない

---

# Dependency Map

```text
Board
  ↓
Evaluation
  ↓
Search
```

```text
Search
  ↓
Benchmark
```

```text
Search
  ↓
Self Play
  ↓
Evolution
```

```text
Evaluation
  ↓
Tuning
```

```text
Evaluation
  ↓
Evolution
```

Tuning と Evolution は Evaluation を利用する。

Tuning と Evolution は Search への依存を必須としない。

---

# Where To Change

## 新しい Evaluation Feature

```text
src/chess_ai_lab/evaluation/features/
```

Feature Registry の変更が必要な場合:

```text
src/chess_ai_lab/evaluation/evaluator.py
```

Feature Registry を変更した場合は、
Training Dataset の互換性を確認する。

---

## Weight 管理

```text
src/chess_ai_lab/evaluation/weight_manager.py
```

---

## Search 改善

```text
src/chess_ai_lab/engine/
```

---

## Move Ordering 改善

```text
src/chess_ai_lab/engine/move_ordering.py
```

---

## Transposition Table 改善

```text
src/chess_ai_lab/engine/transposition.py
```

---

## Self Play 改善

```text
src/chess_ai_lab/evolution/match.py
```

---

## Evolution Algorithm 改善

```text
src/chess_ai_lab/evolution/strategy.py
src/chess_ai_lab/evolution/simple_strategy.py
```

---

## Evolution 実験設定

```text
src/chess_ai_lab/evolution/config.py
```

---

## Benchmark 改善

```text
src/chess_ai_lab/benchmark/
```

---

## Training Dataset 生成

```text
scripts/build_training_dataset.py
```

---

## Training Dataset 読み込み・Cache

```text
src/chess_ai_lab/tuning/dataset.py
```

---

## Training Loop

```text
src/chess_ai_lab/tuning/trainer.py
```

---

## Texel Loss

```text
src/chess_ai_lab/tuning/loss.py
src/chess_ai_lab/tuning/loss_evaluator.py
```

---

## Gradient

```text
src/chess_ai_lab/tuning/gradient.py
```

---

## Optimizer

```text
src/chess_ai_lab/tuning/optimizer.py
```

---

## Learning Rate

```text
src/chess_ai_lab/tuning/lr_scheduler.py
```

---

## Training Configuration

```text
src/chess_ai_lab/tuning/config.py
```

---

## Training Performance

```text
src/chess_ai_lab/tuning/benchmark.py
```

---

## Bug Fix

原則として、Bug の責務を持つファイルだけを変更する。

責務を跨ぐ変更が必要な場合は、
変更理由と影響範囲を明確にする。

---

# AI Instructions

コード変更前に以下を確認する。

1. `docs/invariants.md`
2. `docs/architecture.md`
3. `docs/status.md`
4. 関連する既存コード
5. 関連する Test

変更前に、今回の変更の責務と対象ファイルを特定する。

---

## Change Scope

1回の作業では1つの目的だけを扱う。

明示的に要求されていない変更を追加しない。

特に以下を勝手に行わない。

* 無関係なリファクタリング
* 命名変更
* API変更
* ファイル構成変更
* 設計変更
* 依存関係変更
* パフォーマンス最適化
* コードスタイルの全面変更

---

## Responsibility Rule

変更対象の責務が既存ファイルに明確に存在する場合、
新しいファイルを作成せず既存ファイルを変更する。

責務が複数ファイルにまたがる場合は、
どのファイルに責務を置くべきかを確認してから変更する。

責務が不明確な場合は推測せず、相談する。

---

## Testing Rule

src を変更した場合は、
対応する Test を追加または更新する。

Bug 修正では再発防止 Test を優先する。

---

## Documentation Rule

設計を変更した場合:

```text
architecture.md
invariants.md
```

を確認・更新する。

実装が一区切りした場合:

```text
status.md
```

を更新する。

Codebase の責務やファイル構成が変わった場合:

```text
codebase.md
```

を更新する。

---

## Final Report

実装後は以下を明示する。

* 変更したファイル
* 各ファイルの変更内容
* 変更理由
* 影響範囲
* 実行した Test
* Test 結果
* 未解決の問題

Git 操作を行った場合は、
その操作内容も明示する。
