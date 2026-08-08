# Architecture

## Purpose

この文書は chess-ai-lab の現在のアーキテクチャを定義する。

ここに書かれている内容は「現在の設計」であり、
実装予定やアイデアは含めない。

---

# Layer Architecture

依存方向は以下のみとする。

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

---

# Layer Responsibilities

## Board

責務

- python-chess による盤面管理
- 合法手生成
- FEN取得
- 終局判定

Boardは評価や探索を行わない。

---

## Evaluation

Responsibilities

- 盤面の数値評価
- Featureの実行
- Feature Registryの管理
- Weightの適用
- EvaluationSnapshotの生成

Evaluationは探索を行わない。

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

・EPD読込
・局面評価
・探索性能測定
・客観的な強さ測定

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

## Dataset Build

```
Lichess Dataset
▼
build_training_dataset.py
▼
FEN
▼
Evaluator
▼
EvaluationSnapshot
▼
Feature Vector
▼
Parquet
```
Dataset Build の責務は、元データから学習可能な Parquet Dataset を生成することである。

Parquet Dataset には以下を保存する。

- fen
- target_cp
- source_depth
- feature_values

Feature Vector は Dataset Build 時点の Feature Registry に基づいて生成される。

そのため Feature の構成を変更した場合、学習用 Parquet Dataset を再生成する。

---

## Training
```
ParquetDataset
▼
TrainingPosition / Feature Vector
▼
Gradient
▼
Optimizer
▼
WeightManager
▼
LossEvaluator
▼
ReduceLROnPlateau
▼
Best Weight
```

Training は元データから Feature を再計算する責務を持たない。

Dataset Build で生成された Feature Vector を学習に利用する。

---

## Dataset / Weight Separation

Training Dataset と Weight は独立した成果物として扱う。

Feature の変更は Weight の変更とは別の変更である。

Feature の追加・削除・順序変更を行った場合は、対応する Training Dataset を再生成する。

既存の Weight を新しい Feature Vector にそのまま適用してはならない。

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
