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

# # AI Collaboration

AIはarchitecture.md を前提として実装する。

AIは開発者の代わりに設計判断を行うのではなく、合意された設計を実装する。

## Before Implementation

AIは実装前に以下を確認する。

* invariants.md
* architecture.md
* status.md
* 関連する既存コード
* 関連するTest

AIは、現在の実装・設計・依存関係を確認せずにコードを変更してはならない。

AIは実装前に、今回の変更の目的と変更範囲を明確にする。

変更範囲が不明確な場合、推測して実装を開始してはならない。

---

## Change Scope

1回の作業では1つの目的だけを扱う。

AIは明示的に要求されていない変更を行ってはならない。

以下のような変更は、要求されていない限り行わない。

* 無関係なリファクタリング
* 命名変更
* ファイル構成の変更
* API変更
* 設計変更
* 依存関係の変更
* パフォーマンス最適化
* コードスタイルの全面的な変更

「より良い実装」にすることを理由として、要求されていない変更を追加してはならない。

---

## Design Changes

設計変更が必要な場合、AIは実装前に

* 変更理由
* 現在の設計上の問題
* 変更対象
* 影響範囲
* 代替案
* invariants.md / architecture.md への影響

を説明する。

設計変更は、合意されるまで実装してはならない。

設計変更と機能追加を同時に行ってはならない。

---

## Implementation

実装は必要最小限の差分で行う。

AIは既存コードを尊重し、動作しているコードを理由なく書き換えてはならない。

既存コードを書き換える場合は、その理由と必要性を説明できなければならない。

AIは本書に反する変更を行ってはならない。

---

## After Implementation

実装後、AIは以下を確認する。

* 変更したファイル
* 各ファイルの変更理由
* 主要な変更内容
* 変更による影響範囲
* 実行したTest
* Test結果
* 未解決の問題

AIは、実装した内容と実際の変更内容に差異がないことを確認する。

---

## Diff Review

AIがリポジトリを直接変更できる場合でも、変更後のdiffを確認する。

意図していない変更が含まれている場合、その変更を残したまま作業を完了してはならない。

AIは変更したファイルを明示する。

AIは無関係な変更を自動的に修正・整理・削除してはならない。

---

## Git

AIは明示的な指示がない限り、以下を行ってはならない。

* commit
* push
* force push
* branchの削除
* historyの書き換え
* ユーザーの変更の破棄
* resetによる変更の破棄

AIは既存の未コミット変更を勝手に変更・削除してはならない。

Commitを行う場合は、

* 1コミット = 1目的
* 変更内容とcommit messageが一致している

ことを確認する。

---

## Human Approval

AIがコードを実装することと、その変更を採用することは別である。

AIは実装を完了した時点で、変更が自動的に採用されたものとはみなさない。

最終的な設計判断・変更の採用判断は開発者が行う。

特に以下については、AIが独自に判断して変更してはならない。

* Architecture
* Evaluation設計
* Feature設計
* Weight設計
* Search設計
* Evolution設計
* Training設計
* データ形式
* 実験方針

---

## Experimental Development

実験的な変更は、安定した実装と区別する。

AIは実験結果を理由として、既存の設計やWeightを自動的に変更してはならない。

実験では

* 実験目的
* 使用した設定
* 変更したWeight
* 使用したDataset
* 対局条件
* 評価方法
* 結果

を可能な限り再現可能な形で記録する。

実験結果から本実装へ変更を反映する場合は、別の変更として扱う。

---

## Uncertainty

AIが仕様・設計・既存実装について確信を持てない場合は、推測して変更してはならない。

不明点を明示し、必要な情報を要求する。

AIは「おそらく」「一般的には」といった推測だけを根拠として、既存設計を変更してはならない。
