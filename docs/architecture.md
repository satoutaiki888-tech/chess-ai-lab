# Architecture

## Purpose

この文書は chess-ai-lab の現在のアーキテクチャを定義する。

ここに書かれている内容は「現在の設計」であり、
実装予定やアイデアは含めない。

---

# Layer Architecture

依存方向は以下で固定する。

```
Board
↓
Evaluation
↓
Search

Search
↓
Benchmark

Search
↓
Self Play

Evaluation
↓
Tuning

Evaluation
↓
Evolution
```

上位レイヤーは下位レイヤーを利用できる。

下位レイヤーは上位レイヤーを参照してはならない。

Tuning と Evolution は Evaluation を利用するが、
Search への依存を必須としない。

---

# Layer Responsibilities

## Board

盤面管理のみを担当する。

Responsibilities

- python-chessによる盤面管理
- 合法手生成
- FEN取得
- 手の適用
- Undo
- 終局判定

Boardは以下を行わない。

Evaluation
Search
Weight管理

---

## Evaluation

Responsibilities

- 盤面の数値評価
- Featureの実行
- Feature Registryの管理
- Weightの適用
- EvaluationSnapshotの生成

Evaluator だけが Feature と Weight を統合する。

Evaluation は Search を行わない。

---

## Search

Responsibilities

- 最善手探索
- ノード数管理
- AlphaBeta
- Iterative Deepening

SearchはFeatureを直接利用しない。

SearchはEvaluatorのみ利用する。

---

## Self Play

Responsibilities

- Engine同士の対局
- Match実行
- 対局結果の取得

Self PlayはWeightを変更しない。

---

## Evolution

Responsibilities

- Weightの進化
- Mutation
- Match
- Selection
- Generation管理
- Evolution結果の保存

Flow

Runner
    ↓
Evolution Strategy
    ↓
Mutation
    ↓
Match
    ↓
Selection
    ↓
EvolutionResult

Runner

- 世代管理
- Weight保存
- Evolutionログ
- 実験実行

Runner は進化アルゴリズムを実装しない。

Evolution Strategy

- 1世代だけ進化させる

Examples

- SimpleEvolutionStrategy
- (Future) TournamentStrategy
- (Future) GeneticStrategy

Strategy は

- Weight保存
- Generation管理
- Evolutionログ

を行わない。

---

## Benchmark

Responsibilities

Engine の性能・強さを測定する。

EPD 読み込み
局面ごとの探索
正解手との比較
Accuracy
Nodes
NPS
Elapsed Time

Must Not

・Weight Mutation
・Selection
・Evolution

---

## Tuning

Responsibilities

- Parquet Datasetの読み込み
- TrainingPositionの生成
- EvaluationSnapshotの生成
- Feature Vectorの利用
- Texel Loss
- Gradient計算
- Mini-batch SGD
- Validation
- Learning Rate Scheduling
- Best Weight保存
- Resume Training
- Early Stopping

Must Not

- AlphaBeta探索
- 対局管理
- Feature実装

---

# Evaluation Architecture

構造は以下で固定する。

```
Board
        │
        ▼
 Feature Registry
        │
        ▼
     Evaluator
      ├── WeightManager
      └── EvaluationSnapshot
```

FeatureはWeightを知らない。

WeightManagerはFeatureを知らない。

Evaluatorのみ両者を利用する。

---

# Feature Design

1 Feature = 1 File

Featureはraw scoreのみ返す。

Featureは状態を保持してはならない。

Featureの実行順序は FEATURES Registry によって決定する。

Feature Vectorの順序はWeightの順序と一致しなければならない。

---

# Feature Registry

Feature の実行順序と Weight の対応関係は `FEATURES` によって定義する。

現在の Feature Registry は以下の順序を正とする。

1. material
2. piece_square
3. mobility
4. isolated_pawn
5. doubled_pawn
6. passed_pawn
7. king_safety
8. bishop_pair
9. open_file
10. semi_open_file
11. pawn_shield
12. knight_outpost
13. connected_rooks
14. rook_seventh
15. space
16. bishop_mobility
17. rook_mobility
18. knight_mobility
19. queen_mobility

Feature Vector のインデックスはこの順序に依存する。

Feature の追加・削除・並び替えを行った場合、Weight と Training Dataset の互換性を確認する必要がある。

---

# Training Data Architecture

Training DatasetはParquet形式で保存する。

現在のデータ形式は以下とする。

train.parquet
valid.parquet

columns:
- fen
- target_cp
- source_depth
- feature_values

target_cp はStockfish由来の評価値を学習対象として使用する。

source_depth は元評価の深さを保持する。

feature_values はDataset生成時点で計算されたFeature Vectorを保持する。

---

# Search Architecture

SearchPlayerはEvaluatorのみ保持する。

```
SearchPlayer

↓

Evaluator

↓

Board
```

SearchがFeatureを直接呼ぶことは禁止。

---

# WeightManager

Responsibilities

- Weight保持
- Weight取得
- Weight更新
- JSON保存
- JSON読込
- Copy
- Mutation
- NumPy変換

のみ責務とする。

# Tuning Flow

Training Dataset の構築と Training は分離する。

Dataset Build は学習用データを生成する処理であり、
Training は生成済み Dataset を利用して Weight を最適化する処理である。

---

## Dataset Build

```text
Lichess Dataset
      │
      ▼
build_training_dataset.py
      │
      ▼
FEN / Target / Source Depth
      │
      ▼
Evaluator
      │
      ▼
EvaluationSnapshot
      │
      ▼
Feature Vector
      │
      ▼
Parquet Dataset
```

Dataset Build の責務は、元データから学習可能な Parquet Dataset を生成することである。

Parquet Dataset には以下を保存する。

* fen
* target_cp
* source_depth
* feature_values

さらに Parquet metadata に Feature Registry の情報を保存する。

* feature_names
* feature_count
* feature_schema_hash

Dataset Build は Streaming Dataset を利用し、
必要な局面だけを前処理して Parquet に保存する。

現在の Dataset Build の標準条件は以下である。

* minimum depth: 20
* cp limit: ±1000
* train ratio: 0.9
* seed: 42
* buffer size: 5000
* maximum samples: 500000

これらは実験ごとに変更可能であり、
実験結果とともに記録する。

Feature の構成を変更した場合、
対応する Training Dataset を再生成する。

---

## Training

Training は Dataset Build 済みの Parquet Dataset を利用する。

```text
ParquetDataset
      │
      ▼
NumPy Feature Matrix
      │
      ▼
In-Memory Training Data
      │
      ├──────────────┐
      ▼              ▼
Mini-batch SGD    Loss Evaluation
      │              │
      ▼              ▼
WeightManager    Validation
      │              │
      └──────┬───────┘
             ▼
      LR Scheduler
             │
             ▼
       Best Weight
```

Training 時には Feature を再計算しない。

Parquet に保存された Feature Vector をそのまま NumPy 配列として利用する。

Training 開始時に Dataset を読み込み、
Training 用 Feature Matrix と Target 配列をメモリ上に保持する。

これにより、各 epoch で Parquet を再読み込みする必要をなくす。

---

## Training Data Cache

Training Dataset の読み込みは Training 開始時に一度だけ行う。

```text
Parquet
   │
   ▼
ParquetDataset
   │
   ▼
Feature Matrix + Target
   │
   ▼
Memory
   │
   ├── Epoch 1
   ├── Epoch 2
   ├── Epoch 3
   ├── ...
   └── Epoch N
```

Training Dataset は読み取り専用データとして扱う。

Training 中に Dataset の Feature Vector や Target を変更してはならない。

Training の各 epoch は、メモリ上の NumPy 配列を Mini-batch に分割して処理する。

Dataset のロード時間と Training epoch の処理時間は分離して考える。

---

## Mini-batch Training

Trainer は Training Dataset 全体を一度に Optimizer に渡さない。

Feature Matrix を batch_size 単位に分割する。

```text
Feature Matrix
      │
      ├── Batch 1
      ├── Batch 2
      ├── Batch 3
      ├── ...
      └── Batch N
             │
             ▼
          Evaluation
             │
             ▼
          Gradient
             │
             ▼
          Optimizer
```

各 batch では以下を行う。

1. Feature Matrix と Weight の行列積
2. Texel Gradient の計算
3. Gradient の batch 平均
4. Optimizer による Weight 更新

epoch 完了後に Weight Vector を WeightManager と同期する。

---

## Validation

Validation Dataset は Training Dataset と分離して保持する。

Validation は Weight 更新を行わない。

```text
Validation Feature Matrix
          │
          ▼
       Evaluation
          │
          ▼
       Texel Loss
```

Validation Loss は Learning Rate Scheduler と Early Stopping の判定に利用する。

Validation Dataset は Training Dataset と同じ Feature Registry によって生成されていなければならない。

---

## Training Configuration

Training の実験条件は `TrainingConfig` に集約する。

主な設定項目は以下である。

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

Development 用設定と Production 用設定を分離する。

Training の実験結果を比較する場合は、
Learning Rate だけでなく Dataset、Epochs、Batch Size、Validation 条件も記録する。

---

## Training Performance

Training の性能改善では、まずデータアクセスコストを削減する。

優先順位は以下とする。

```text
Parquet I/O
    ↓
Dataset Conversion
    ↓
NumPy Vectorization
    ↓
Gradient Calculation
    ↓
Optimizer
```

Dataset が一度メモリにロードされた後は、
epoch ごとの Dataset I/O を発生させない。

大量データ処理では Python の逐次ループよりも
NumPy によるベクトル演算を優先する。

Training Benchmark では少なくとも以下を区別する。

* Dataset
* Evaluation
* Gradient
* Optimizer
* Total

```
```


---

# EvaluationSnapshot

EvaluationSnapshotは学習用の評価結果を保持する。

保持するもの

- total
- raw_features
- feature_vector

feature_vector は FEATURES の順番で生成される。

raw_features はFeature名とraw scoreの対応を保持する。

学習ではFeature VectorをGradient計算に利用する。

---

# Training Dataset Compatibility

Training Dataset と現在の Feature Registry の互換性は、
Training 開始時に検証する。

Parquet metadata に保存された

* feature_names
* feature_count
* feature_schema_hash

を現在の `FEATURES` Registry と比較する。

以下のいずれかが一致しない場合、
Training を開始してはならない。

* Feature 数
* Feature 名
* Feature 順序
* Feature Schema Hash

Feature Registry の変更は、
Training Dataset の Feature Vector の意味を変更する可能性がある。

したがって Feature の

* 追加
* 削除
* 並び替え
* 計算内容の変更

を行った場合は、原則として Training Dataset を再生成する。

---

# Experiment Artifacts

Training 実験では、Dataset と Weight を別々の成果物として扱う。

Dataset Artifact

* train.parquet
* valid.parquet
* Dataset build parameters
* Feature Registry
* Feature schema hash
* sample counts

Training Artifact

* initial weight
* learning rate
* epochs
* batch size
* validation interval
* train loss
* validation loss
* best epoch
* best weight
* final weight

異なる Dataset や異なる Benchmark 条件で得られた結果を、
同一条件の実験結果として比較してはならない。

```
```
---

# Dependency Rules

許可

Board
← Evaluation
← Search
← SelfPlay
← Evolution

禁止

Evaluation → Search

Feature → WeightManager

Feature → Search

Search → Feature

Evolution → Feature

Board → Evaluation

Board → Search
