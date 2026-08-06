# AI Context

## Purpose

このファイルは AI が最初に読むファイルである。

目的は

- プロジェクトの入口を提供する
- 読むべきドキュメントを案内する
- 現在の開発フェーズを共有する

詳細な設計は各ドキュメントを参照する。

---

# Reading Order

AIは以下の順で情報を今すぐ読む。

1. architecture.md
   レイヤー構造・責務を理解する。

2. invariants.md
   絶対に破ってはいけない設計を理解する。

3. codebase.md
   各ファイルの責務を確認する。

4. status.md
   現在の開発状況を把握する。

5. evaluation.md
   Evaluationを変更する場合のみ参照する。

---

# Current Phase

Weight Evolution Foundation

現在は Weight Evolution の基盤を構築している。

---

# AI Working Rules

実装前に設計を確認する。

推測でコードを書き換えない。

不足するコードは要求する。

1回の変更では1つの目的のみ扱う。

不要なリファクタリングを行わない。

---

# When Architecture Changes

設計変更が必要な場合は

実装より先に

architecture.md

または

invariants.md

の変更を提案する。

---

# Source of Truth

設計は architecture.md を唯一の正とする。

不変条件は invariants.md を唯一の正とする。

現在の状態は status.md を唯一の正とする。

開発ルールは development.md を唯一の正とする。

## Continuous Documentation Improvement

このプロジェクトでは、コードだけでなく `docs/` も成果物である。

AIとの共同開発を通して、

- 曖昧な設計
- 不足しているルール
- 誤解を招く表現
- AIが推測を必要とした箇所

を発見した場合は、コード変更だけでなくドキュメントの改善も提案する。

同じ問題を繰り返さないことを目的とし、
必要最小限の変更で docs を継続的に改善する。

## Project Philosophy

このプロジェクトでは、

- コード
- テスト
- ドキュメント

を同じ価値を持つ成果物として扱う。

AIとの共同開発で得られた知見は、
必要に応じて docs に反映し、
将来の開発効率と品質を継続的に改善する。
特にstatusにまとめられている今後のタスクは随時更新していくことになる。