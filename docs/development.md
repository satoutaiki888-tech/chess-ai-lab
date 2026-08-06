# Development Rules

## Purpose

この文書は chess-ai-lab の開発ルールを定義する。

対象は人間・AIの両方である。

目的は

- 品質維持
- 設計維持
- AIとの共同開発効率向上

である。

---

# Fundamental Rules

## Correctness First

最優先は正しく動くことである。

速度最適化は正しさを犠牲にしてはならない。

---

## Preserve Architecture

architecture.md と invariants.md を守る。

設計変更は機能追加とは別タスクとして扱う。

---

## Small Changes

1回の変更では1つの目的だけを扱う。

悪い例

- AlphaBeta改善
- Feature追加
- Weight変更

を同時に行う。

良い例

- AlphaBeta改善のみ

---

## Ask Before Assuming

不足しているコードや仕様は推測しない。

必要なファイルがある場合は要求する。

分からないことは質問する。

---

# Testing

Feature追加時は対応するTestを追加する。

Bug修正時は再発防止Testを追加する。

pytest が Green の状態を維持する。

既存Testを削除しない。

---

# Refactoring

リファクタリングでは

動作を変更しない。

設計変更が含まれる場合は

別タスクに分離する。

---

# Performance

性能改善では

Benchmarkで比較する。

改善を推測で判断しない。

速度より正確性を優先する。

---

# AI Collaboration

AIは以下を守る。

- 推測でコードを書き換えない。
- 必要なファイルは要求する。
- 小さい差分で実装する。
- 既存設計を尊重する。
- 既存コードを理由なく書き換えない。
- 不要なリファクタリングを行わない。

---

# Code Review Checklist

変更前に確認する。

- architecture.md を守っているか
- invariants.md を守っているか
- pytest は通るか
- テスト追加は必要か
- 責務は混ざっていないか

---

# Commit Policy

1コミット = 1目的

例

✔ Add bishop mobility feature

✔ Fix alpha-beta bug

✘ Add bishop mobility + refactor evaluator + optimize search

---

# Documentation

設計変更時は

architecture.md

または

invariants.md

を更新する。

機能追加時は

必要に応じて docs を更新する。

---

# Current Development Stage

現在は

Weight Evolution Foundation

を開発中である。

NNUE

Deep Learning

Reinforcement Learning

は対象外。

これらを前提とした設計変更は行わない。

# Existing Code

動いているコードは資産である。

変更は必要最小限とする。

既存コードを書き換える場合は

- 理由
- 影響範囲
- 必要性

を説明できなければならない。