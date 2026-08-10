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

AIは以下の順で情報を読む。

1. `docs/architecture.md`
   レイヤー構造・責務を理解する。

2. `docs/invariants.md`
   絶対に破ってはいけない設計を理解する。

3. `docs/codebase.md`
   各ファイルの責務を確認する。

4. `docs/status.md`
   現在の開発状況を把握する。

5. `docs/ai_workflow.md`
   AIの作業手順・変更範囲・報告ルールを確認する。

6. `docs/evaluation.md`
   Evaluationを変更する場合のみ参照する。

7. `docs/decisions.md`
   設計判断の背景を確認する必要がある場合に参照する。

Repositoryのルートにある `AGENTS.md` はAI作業の入口と基本ルールを定義する。

---

# AI Working Rules

実装前に設計を確認する。

推測でコードを書き換えない。

不足するコード・仕様は要求する。

1回の変更では1つの目的のみ扱う。

不要なリファクタリングを行わない。

既存の未コミット変更を勝手に変更・削除しない。

`src` を変更した場合は関連するTestを確認し、必要なTestを追加・更新して実行する。

実装後はGit diffを確認する。

---

# When Architecture Changes

設計変更が必要な場合は、実装より先に変更を提案する。

必要に応じて

- `architecture.md`
- `invariants.md`
- `evaluation.md`

の変更内容を先に整理し、合意を得てから実装する。

---

# Source of Truth

設計は `architecture.md` を唯一の正とする。

不変条件は `invariants.md` を唯一の正とする。

現在の状態・今後のタスクは `status.md` を唯一の正とする。

AIの作業ルールは `AGENTS.md` と `docs/ai_workflow.md` を正とする。

Evaluationの詳細仕様は `evaluation.md` を正とする。

設計判断の背景は `decisions.md` を参照する。

---

# Continuous Documentation Improvement

このプロジェクトでは、コードだけでなく `docs/` も成果物である。

AIとの共同開発を通して、

- 曖昧な設計
- 不足しているルール
- 誤解を招く表現
- AIが推測を必要とした箇所
- 新しく発生した重要な設計判断

を発見した場合は、コード変更だけでなくドキュメントの改善も提案する。

同じ問題を繰り返さないことを目的とし、必要最小限の変更で docs を継続的に改善する。

特に `status.md` にまとめられている現在の状態と今後のタスクは、開発の進行に合わせて随時更新する。

---

# Project Philosophy

このプロジェクトでは、

- コード
- テスト
- ドキュメント

を同じ価値を持つ成果物として扱う。

AIとの共同開発で得られた知見は、必要に応じて docs に反映し、将来の開発効率と品質を継続的に改善する。

将来別のAIが作業を引き継ぐ場合でも、過去の会話を知らなくてもRepositoryから安全に現在地と設計意図を理解できる状態を目標とする。
