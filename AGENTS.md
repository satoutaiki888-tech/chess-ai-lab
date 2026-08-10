# AI Development Guide

## Purpose

このファイルは、AIが `chess-ai-lab` の作業を開始するときの入口である。

このファイルは詳細な設計仕様を持たない。設計・不変条件・現在地・コード責務は `docs/` の各文書を参照する。

## Reading Order

通常の実装では、次の順で読む。

1. `docs/architecture.md` — レイヤー構造・責務・依存方向
2. `docs/invariants.md` — 絶対に守る不変条件
3. `docs/codebase.md` — ファイルごとの責務・現在の実装構造
4. `docs/status.md` — 現在の開発フェーズ・次のタスク
5. `docs/ai_workflow.md` — AIの作業手順・報告ルール

Evaluationを変更する場合は、上記に加えて `docs/evaluation.md` を必ず読む。

設計判断の背景を確認する必要がある場合は `docs/decisions.md` を参照する。

## Core Rules

- 仕様が不足している場合、推測で実装しない。
- 変更前に関連する設計・不変条件・現在地・コードを確認する。
- 1回の変更では1つの目的だけを扱う。
- 依頼されていないリファクタリングを行わない。
- 既存の設計境界を勝手に変更しない。
- Architecture変更が必要なら、実装前に提案して合意を得る。
- `src` を変更したら、関連するTestを追加・更新し、実行する。
- 既存Testを理由なく削除・弱体化しない。
- 既存の未コミット変更を勝手に変更・削除しない。
- 実装後はGit diffを確認し、意図しない変更がないことを確認する。

## Architecture Change

設計変更が必要になった場合は実装を止め、少なくとも以下を提示する。

- 変更理由
- 現在の設計上の問題
- 提案する変更
- 影響範囲
- 代替案
- `architecture.md` / `invariants.md` / `evaluation.md` への影響

合意前に設計変更を実装しない。

## Documentation

Documentationはコード・Testと同じ成果物として扱う。

次のような知見を得た場合は、必要最小限のDocumentation更新を提案する。

- 設計が曖昧だった
- 既存ルールが不足していた
- 誤解を招く記述があった
- AIが推測を必要とした
- 設計上の重要な判断を新たに行った
- `status.md` の現在地・次タスクが変化した

ただし、依頼されていない大規模なDocumentation整理は行わない。

## Completion Report

作業完了時には、少なくとも次を報告する。

- 変更ファイル
- 各変更の概要と理由
- 影響範囲
- 実行したTestと結果
- Git diff確認結果
- 未解決事項
- 依頼外に発生した差異
