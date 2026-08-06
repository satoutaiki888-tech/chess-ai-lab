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

↓

Self Play

↓

Evolution

逆方向の依存は禁止。

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

---

# Evaluation

EvaluatorだけがWeightを適用する。

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

---

# Scripts

scriptsはライブラリロジックを持たない。

scriptsが行うのは

- 入力
- ライブラリ呼び出し
- 結果表示

のみとする。

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

pytest Greenを維持する。

---

## Documentation

ドキュメントは実装のたびに更新しなくてもよい。

実装が一区切りしたタイミングでまとめて更新する。

設計変更を伴う場合は、対応するドキュメントも同時に更新する。

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