# Testing Guide

## Purpose

この文書は、`chess-ai-lab` のTest方針と、変更時にどの範囲を確認するかを定義する。

Testは単に実装を通すためのものではなく、Architectureと不変条件を守るための検証手段でもある。

---

# 1. General Rules

- `src` を変更したら、関連するTestを確認する。
- 新しい挙動には可能な限りTestを追加する。
- Bug修正では再発防止Testを追加する。
- 既存Testを理由なく削除・弱体化しない。
- Testを通すためだけに実装を不自然に変更しない。
- Testが仕様と矛盾している場合は、仕様を確認してからTestを変更する。
- Architecture変更では、変更前後の境界をTestで確認できるようにする。

---

# 2. Test Categories

## Unit Test

単一の関数・クラス・小さな責務を検証する。

例：

- Board operation
- Feature calculation
- Weight conversion
- Loss calculation
- Gradient calculation
- Optimizer update

## Integration Test

複数Componentが設計どおり接続されることを検証する。

例：

- Board → Evaluator
- Evaluator → Search
- Dataset → Trainer
- Evolution → Match / Selection

## Regression Test

過去に発生したBugや重要な仕様が再発しないことを検証する。

Bug修正では、可能ならBugを再現するTestを先に追加する。

## Benchmark

速度・探索性能・Training性能・Playing Strengthなどの測定。

Benchmarkは通常のCorrectness Testとは別物として扱う。

Benchmark結果だけでCorrectnessを証明しない。

---

# 3. Area-Specific Guidance

## Board

Board変更では少なくとも関連する以下を確認する。

- 合法手生成
- Move適用
- Undo
- FEN
- 終局状態

BoardはEvaluation / Searchの責務を持たないことも確認する。

## Evaluation

Evaluation変更では、必要に応じて `docs/evaluation.md` を確認する。

確認対象：

- Feature calculation
- Feature Registry order
- Weight application
- EvaluationResult
- EvaluationSnapshot
- Feature Vector
- Weight Vector
- Score convention

Feature Registryの変更ではDataset compatibilityへの影響も確認する。

## Search

Search変更では、少なくとも関連する以下を確認する。

- Best move
- Search depth
- Terminal position
- Node counting
- Alpha-Beta pruning
- Move ordering
- Transposition Table

SearchがFeatureを直接呼び出していないこと、WeightManagerを直接扱っていないことも確認する。

## Evolution

Evolution変更では、以下の責務分離を確認する。

- Mutation
- Match
- Selection
- Strategy
- Runner
- Generation management
- Weight persistence

StrategyとRunnerの責務が混ざっていないことを確認する。

## Benchmark

Benchmark変更では、結果計算と実行管理の責務分離を確認する。

Benchmark結果を比較する場合は、少なくとも以下の条件を揃える。

- Dataset
- Position set
- Search depth
- Weight
- Search configuration

## Training / Tuning

Training変更では、以下を確認する。

- Dataset loading
- Feature schema validation
- Feature Vector dimensions
- Target / source depth alignment
- Loss
- Gradient
- Optimizer
- Scheduler
- Validation
- Checkpoint
- Resume / Fresh mode

Training中にFeatureを再計算していないこと、Dataset CacheがWeightを保持していないことも重要な不変条件である。

---

# 4. Architecture Tests

Architecture上の重要な依存ルールは、可能なものから自動Testにする。

特に次の逆方向依存を許可しない。

- Board → Evaluation
- Board → Search
- Feature → Search
- Feature → WeightManager
- Search → Feature
- Search → WeightManager
- Evolution → Runner
- Optimizer → Gradient calculation

文書だけで守るのではなく、機械的に検出できるルールはTestで守ることを目指す。

---

# 5. Dataset Compatibility Tests

Feature Registryを変更した場合、Datasetとの互換性を必ず確認する。

少なくとも以下を検証する。

- Feature count
- Feature names
- Feature order
- Feature schema hash
- Feature Vector dimension
- Weight Vector dimension

不一致の場合はTraining開始を拒否することが期待される。

---

# 6. Test Execution

実装後は、まず変更対象に近いTestを実行し、その後必要に応じて広い範囲のTestを実行する。

典型的な順序：

1. 変更対象のUnit Test
2. 関連するIntegration / Regression Test
3. 必要に応じて全Test
4. 必要に応じてBenchmark

実行したTestと結果は完了報告に記録する。

---

# 7. When Tests Are Missing

関連Testが存在しない場合、まず既存Test構造を確認する。

重要な仕様ならTest追加を提案する。

ただし、依頼されたBug FixやFeatureと無関係なTest基盤の大規模整理を同時に行わない。

---

# 8. Test and Documentation Relationship

Testで初めて明らかになった重要な不変条件は、必要に応じて `docs/invariants.md` に反映する。

Testで重要な設計判断が明らかになった場合は、`docs/decisions.md` に記録することを検討する。

TestはDocumentationの代替ではなく、Documentationに書かれた重要ルールを実行可能な形で補強するものとする。
