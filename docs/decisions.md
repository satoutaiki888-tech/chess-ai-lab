# Design Decisions

## Purpose

この文書は、`chess-ai-lab` の重要な設計判断と、その理由を記録する。

`architecture.md` は「現在の設計」を、`invariants.md` は「破ってはいけない条件」を定義する。一方、この文書では「なぜその設計を採用したか」を残す。

目的は、将来のAIや開発者が過去の判断を推測せずに済むようにすることである。

---

# Decision 001 — Layer Separation

## Decision

Board、Evaluation、Search、Evolution、Benchmark、Tuningを責務ごとに分離する。

依存方向を明確にし、上位レイヤーから下位レイヤーへの依存を基本とする。

## Reason

各領域の変更が他領域へ不必要に波及することを防ぎ、Evaluation・Search・Training・Evolutionを独立して検証できるようにするため。

## Consequence

- FeatureはSearchを知らない
- SearchはFeatureを直接実行しない
- SearchはEvaluatorを通して評価する
- TuningはSearchに依存しない
- EvolutionのMatch / Selection / Mutation / Runnerの責務を分離する

---

# Decision 002 — Feature Registry Order Is Semantic

## Decision

Feature Registryの順序をFeature VectorとWeight Vectorの意味として扱う。

## Reason

Training Datasetに保存されたFeature VectorとWeight Vectorは同じFeature順序を前提とするため。

## Consequence

Featureの追加・削除・並べ替えは単なる実装変更ではない。Dataset互換性に影響する。

Feature Registry metadataとschema validationによって不一致を検出する。

---

# Decision 003 — Training Uses Precomputed Feature Vectors

## Decision

Training Dataset Build時にFeatureを計算し、ParquetへFeature Vectorを保存する。Training中にFeatureを再計算しない。

## Reason

Training処理とDataset Buildを分離し、EpochごとのBoard / Feature計算を避けるため。また、同じDatasetを使うTraining実験を再現可能にするため。

## Consequence

DatasetはFeature Registry metadataとschema hashを持つ。現在のEvaluation側とDataset側のFeature schemaが一致しなければTrainingを開始できない。

---

# Decision 004 — In-Memory Training Dataset Cache

## Decision

Training開始時にParquet DatasetをNumPy配列へロードし、Epoch間で再利用する。

## Reason

EpochごとのParquet I/Oを避け、Training性能を改善するため。

## Constraint

CacheはTrainingの数学的意味を変更してはいけない。WeightはDataset Cacheに含めず、現在のWeight Vectorを各Epochで利用する。

## Consequence

Dataset I/OはTraining Loopの主要なボトルネックではなくなり、現在はGradient computationが主な性能ボトルネックとなる。

---

# Decision 005 — Evolution Strategy Is Separate From Runner

## Decision

Evolution AlgorithmはStrategy / Evolution側に置き、Runnerは実行・Generation管理・保存・ログを担当する。

## Reason

Evolution Algorithmと実験実行環境を分離し、複数Strategyを交換可能にするため。

## Consequence

StrategyはWeight保存やGeneration管理を行わない。RunnerはMutation / Match / Selectionの実装を持たない。

---

# Decision 006 — Documentation Is a Development Artifact

## Decision

Code、Test、Documentationを同じ開発成果物として扱う。

## Reason

AIとの長期的な共同開発では、会話だけに設計判断や現在地を依存すると、AIが入れ替わった際に重要な文脈が失われるため。

## Consequence

重要な設計判断はDocumentationに残す。曖昧な仕様やAIが推測を必要とした箇所は、必要最小限のDocumentation改善につなげる。

---

# Updating This Document

新しい設計判断が発生した場合は、次を記録する。

- Decision
- Reason
- Consequence
- 必要に応じてAlternatives / Rejected alternatives

既存のDecisionを変更する場合は、単純に履歴を消すのではなく、現在の設計との関係が分かるように更新する。

大きな設計判断が増えた場合は、このファイルを個別ADRへ分割することを検討する。
