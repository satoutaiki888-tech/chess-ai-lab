# Invariants

## Purpose

この文書は chess-ai-lab において常に維持されるべき設計・開発上の不変条件（Invariants）を定義する。

ここに記載された内容は、リファクタリング・機能追加・最適化を行っても維持されなければならない。

設計変更を行う場合は、この文書を先に更新し、合意を得てから実装を変更する。

---

# Architecture

## Layer Separation

以下の依存方向は変更しない。

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

逆方向の依存は禁止。

レイヤーは上位から下位へのみ依存する。
Tuning と Evolution は Evaluation を利用するが、Search への依存を必須としない。

---

## Single Responsibility

各レイヤーは責務を混在させない。

Board

- 盤面管理のみ

Evaluation

- 盤面評価のみ

Search

- 探索のみ

Self Play

- 対局のみ

Evolution

- Weight改善のみ

Tuning

- 学習のみ

---

# Evaluation

EvaluatorだけがSnapshotとWeightを統合する。

FeatureはWeightを知らない。

WeightManagerはFeatureを知らない。

Featureはraw scoreのみ返す。

FeatureからEvaluatorを呼ばない。

---

# Feature

1 Feature = 1 File

Feature同士は依存しない。

Featureは副作用を持たない。

FeatureはBoardを変更しない。

---

# Search

SearchはEvaluatorのみ利用する。

SearchからFeatureを直接呼ばない。

SearchはWeightManagerを知らない。

SearchはBoardを書き換えない。

探索中にWeightを変更しない。

---

# Weight

WeightManagerはWeight管理だけを担当する。

- Weight取得
- Weight更新
- JSON保存
- JSON読込
- Copy
- Mutation
- NumPy変換

WeightManagerは

- Search
- Self Play
- Evolution

を行わない。

---

# Evolution

EvolutionはWeight改善のみを担当する。

- Matchは勝敗のみ決定する。
- Selectionは採用のみ決定する。
- MutationはWeightの生成のみ行う。

Evolutionは

- Evaluation
- Search
- Feature

を変更しない。

進化アルゴリズムは Strategy として実装する。

Runner は Strategy のみを利用する。

Runner に進化アルゴリズムを書いてはならない。

Strategy は

- Weight保存
- Generation管理
- Evolutionログ

を行ってはならない。

Evolution実験の設定は EvolutionConfig に集約する。
---

# Training Components

- Dataset は学習データを供給するだけ
- LossEvaluator は Loss を計算するだけ
- Optimizer は Weight を更新するだけ、勾配計算を行わない。
- Scheduler は Learning Rate を更新するだけ
- Trainer だけが学習ループを持つ
Trainerだけが

- Optimizer
- Scheduler
- LossEvaluator

を協調させる。

---

# Training Dataset

## Dataset Generation

Training Dataset は `build_training_dataset.py` によって生成する。

Dataset Build と Training は別の処理として扱う。

Dataset Build は

- 元データの読み込み
- 局面のフィルタリング
- Target Score の前処理
- Feature Vector の生成
- Parquet への保存

を担当する。

Trainer は元データセットから Feature を再計算してはならない。

---

## Feature Vector Consistency

Parquet に保存された Feature Vector は、Dataset Build 時点の Feature Registry に対応する。

Feature の

- 追加
- 削除
- 順序変更
- Feature の計算内容の変更

を行った場合、既存の Training Dataset をそのまま使用してはならない。

必要に応じて Training Dataset を再生成する。

---

## Feature / Weight Compatibility

Feature Vector の次元数と Weight の次元数は一致しなければならない。

Feature Registry の順序と Weight の順序は一致しなければならない。

異なる Feature Registry から生成された Dataset と Weight を組み合わせて学習してはならない。

---

# EvaluationSnapshot

EvaluationSnapshot は Evaluation 結果を学習用 Feature Vector に変換するためのデータ構造である。

保持するもの

- total
- raw_features
- feature_vector

Dataset Build 時に Evaluator が EvaluationSnapshot を生成する。

生成された feature_vector は Training Dataset に保存される。

Training 時には保存済みの Feature Vector を利用し、Feature の再計算を行わない。

EvaluationSnapshot 自体は探索処理では利用しない。
---

# Scripts

scriptsはライブラリロジックを持たない。

scriptsが行うのは

- 入力
- ライブラリ呼び出し
- 結果表示

のみとする。

---

# Performance

大量データ処理では可能な限り
NumPyによるベクトル演算を利用する。

Pythonループは必要な場合のみ使用する。

---

# Development

## Preserve Architecture

architecture.md と本書を守る。

設計変更は機能追加とは別タスクとして扱う。

---

## Small Changes

1回の変更では1つの目的だけを扱う。

設計変更と機能追加を同時に行わない。

変更は小さい単位で行う。

---

## Ask Before Assuming

不足している仕様やコードは推測しない。

必要なコードは要求する。

分からないことは質問する。

---

## Existing Code

動いているコードは資産である。

既存コードを書き換える場合は

- 理由
- 影響範囲
- 必要性

を説明できなければならない。

変更は必要最小限とする。

---

## Testing

srcを変更した場合は、対応するTestを追加または更新する。

Bug修正では再発防止Testを追加する。

既存Testは削除しない。

---

## Documentation

architecture.md と invariants.md は設計変更時のみ更新する。

status.md は開発の一区切りで更新する。

---

## Development Status

現在の開発方針・進捗・次に行う作業は status.md を唯一の正とする。

AIは実装前に status.md を確認し、現在の開発フェーズと次のタスクを把握する。

status.md は実装が一区切りしたタイミングで更新する。

---

## Commit

1コミット = 1目的

例

✓ Add bishop mobility feature

✓ Fix alpha-beta bug

✗ Add bishop mobility + optimize search

---

# AI Collaboration

AIは本書を前提として実装する。

AIは

- 推測で設計変更しない。
- 推測で既存コードを書き換えない。
- 必要なコードは要求する。
- 小さい差分で実装する。
- 責務を混在させない。
- 本書に反する変更を提案しない。

設計変更が必要な場合は、実装前に理由を説明する。