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

- python-chess のラッパー
- 盤面状態の管理
- 合法手生成
- FEN取得
- 終局判定

Boardは評価や探索を行わない。

---

## Evaluation

責務

- 盤面を数値評価する
- Featureを集約する
- Weightを適用する

Evaluationは探索を行わない。

---

## Search

責務

- 最善手探索
- ノード数管理
- AlphaBeta
- Iterative Deepening

SearchはFeatureを直接利用しない。

SearchはEvaluatorのみ利用する。

---

## Self Play

責務

- Engine同士を対局させる
- ベンチマークを行う

Self PlayはWeightを変更しない。

---

## Evolution

Responsibilities

- Evolution Strategy が1世代の進化を実装する
- Runner が進化実験を実行する
- Match が自己対局を行う
- Selection がWeight採用を判定する

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

- Streaming Datasetを読む
- TrainingPositionを供給する
- Texel Lossを計算する
- EvaluationSnapshotを生成する
- Feature Vectorを扱う
- Gradientを集計する
- SGDでWeight更新する
- Learning Rate Schedulerを適用する
- Best Weightを保存する
- Resume Trainingを行う

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

詳しくはevaluation.mdに記す。

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

# Weight Evolution

WeightManager

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

```
ParquetDataset
        ▼
TrainingPosition
        ▼
Evaluator
        ▼
EvaluationSnapshot
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
---

# EvaluationSnapshot

EvaluationSnapshot は学習専用データである。

保持するもの

- total
- raw_features
- feature_vector

feature_vector は FEATURES の順番で保持する。

学習では feature_vector を使用する。

raw_features は可視化・デバッグ用途とする。

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
