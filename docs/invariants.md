# Invariants

## Purpose

この文書は chess-ai-lab の不変条件 (Invariants) を定義する。

ここに記載された内容は、リファクタリング・機能追加・最適化を行っても維持されなければならない。

設計変更を行う場合は、この文書を先に更新し、合意を得てから実装を変更する。

---

# Layer Separation

以下の依存方向は変更しない。

Board

↓

Evaluation

↓

Search

↓

Self Play

↓

Evolution

逆方向の依存は禁止。

---

# Single Responsibility

各レイヤーは責務を混在させない。

Board

盤面管理のみ。

Evaluation

盤面評価のみ。

Search

探索のみ。

Self Play

対局のみ。

Evolution

Weight改善のみ。

---

# Evaluation

EvaluatorだけがWeightを適用する。

FeatureはWeightを知らない。

WeightManagerはFeatureを知らない。

Featureはraw scoreのみ返す。

FeatureからEvaluatorを呼ばない。

---

# Feature Rules

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

WeightManagerは

- 探索
- Self Play
- Evolution

を行わない。

---

# Evolution

EvolutionはWeightを比較する。

Evaluationそのものを書き換えない。

Featureを変更しない。

探索アルゴリズムを変更しない。

---

# Testing

新機能追加時はTestを追加する。

既存Testを削除してはならない。

pytest greenを維持する。

---

# Development Rules

推測で既存コードを書き換えない。

必要なコードは要求する。

小さい単位で変更する。

動いているコードを理由なく変更しない。

設計変更と機能追加を同時に行わない。

1回の変更では1つの目的だけを扱う。

---

# AI Collaboration Rules

AIは

- この文書を前提として実装する。
- 不足する情報は質問する。
- 推測で設計変更しない。
- Invariantに反する変更を提案しない。
- 設計変更が必要な場合は、実装前に理由を説明する。