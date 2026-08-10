# AI Collaboration Workflow

## Purpose

この文書は、AIが `chess-ai-lab` で安全かつ一貫して開発するための作業手順を定義する。

詳細な設計仕様は `architecture.md`、不変条件は `invariants.md`、現在地は `status.md` を参照する。

---

# 1. Task Classification

作業開始時に、依頼を次のいずれかに分類する。

- Bug Fix
- Feature
- Refactor
- Performance
- Evaluation
- Training
- Evolution
- Benchmark
- Documentation
- Architecture Change

複数にまたがる場合でも、依頼された主目的を明確にする。

Architecture Changeが含まれる場合は、通常の実装タスクとして扱わず、設計確認を先に行う。

---

# 2. Understand Before Editing

通常は次の順で確認する。

1. `docs/architecture.md`
2. `docs/invariants.md`
3. `docs/codebase.md`
4. `docs/status.md`
5. 関連するSource
6. 関連するTest

Evaluationを変更する場合は `docs/evaluation.md` も読む。

設計判断の背景が必要な場合は `docs/decisions.md` を読む。

すでに十分な情報がある場合は、不要な全Repository探索を行わない。

---

# 3. Determine Scope

実装前に、少なくとも次を明確にする。

- 目的
- 変更対象
- 変更しない範囲
- 関連する不変条件
- 必要なTest

依頼されていない改善を同時に行わない。

特に次を「ついでに」変更しない。

- 命名
- ファイル構成
- API
- Architecture
- 依存関係
- Performance
- Coding Style

必要なら別Taskとして提案する。

---

# 4. Missing Information

仕様・コード・Testが不足していて正しい実装を決められない場合は推測しない。

必要な情報を明示して要求する。

特に次の場合は停止する。

- 仕様が複数解釈できる
- Architectureとの整合性を判断できない
- 既存APIの意図が不明
- 既存Testだけでは期待動作を判断できない
- 破壊的変更の可否が不明

---

# 5. Architecture Change

実装中にArchitecture変更が必要だと判明した場合は、そのまま変更しない。

次を整理して提案する。

1. 現在の設計
2. 問題点
3. なぜ既存設計では解決できないか
4. 提案する設計
5. 影響範囲
6. 代替案
7. Documentationへの影響

合意後にArchitecture変更を実装する。

---

# 6. Implementation

実装は最小限の変更で行う。

原則：

- 既存の設計境界を尊重する
- 既存コードを資産として扱う
- 同じ目的をより小さい変更で達成できるなら小さい方を選ぶ
- 新しい抽象化は必要性を説明できる場合だけ追加する
- 一時的なDebug codeを残さない

---

# 7. Tests

`src` を変更した場合は、関連するTestを確認する。

必要に応じて、次を行う。

- 新しい挙動のTest追加
- Bug再発防止Test追加
- 既存Test更新
- Regression確認

Testが既存仕様と矛盾している場合、Testを単純に変更して通すのではなく、仕様を確認する。

Architecture上の不変条件を変更しない修正では、可能な限り既存のTest構造を維持する。

---

# 8. Documentation

コード変更によって現在地が変わった場合、`docs/status.md` の更新が必要か確認する。

新しい設計判断が生じた場合、`docs/decisions.md` に記録する必要があるか確認する。

設計仕様そのものが変わった場合は、該当する以下を更新する。

- `architecture.md`
- `invariants.md`
- `evaluation.md`

Documentation変更は、コード変更と同様に目的を明確にして行う。

---

# 9. Git / Diff

実装後はGit diffを確認する。

確認事項：

- 意図したファイルだけ変更されているか
- 不要なFormatting変更がないか
- Debug codeがないか
- Testが意図せず弱くなっていないか
- Documentationと実装に矛盾がないか

既存の未コミット変更がある場合、それを自分の変更と混同しない。

ユーザーの変更を勝手に削除・整理・上書きしない。

---

# 10. Completion Report

完了報告では、次の順で簡潔に説明する。

## Changed

変更したファイルと変更内容。

## Reason

なぜ変更したか。

## Impact

他コンポーネントへの影響。

## Tests

実行したTestと結果。

## Diff

意図しない変更がないことを確認したか。

## Documentation

更新したDocumentation、または更新不要と判断した理由。

## Unresolved

未解決事項、既知の制約、追加で必要な作業。

## Out of Scope

依頼外だが発見した改善候補があれば、実装せず別Taskとして記録する。

---

# 11. Handoff Between AIs

別のAIが作業を引き継げる状態を維持する。

引き継ぎに必要な情報は、会話だけに依存させない。

少なくとも次をRepository側に残す。

- 設計 → `architecture.md`
- 不変条件 → `invariants.md`
- 現在地 → `status.md`
- コード責務 → `codebase.md`
- Evaluation仕様 → `evaluation.md`
- 設計判断 → `decisions.md`
- AI作業ルール → `AGENTS.md` / `ai_workflow.md`

過去の会話を知らなくても、Repositoryを読めば安全に作業を再開できる状態を目標とする。

---

# 12. Continuous Improvement

AIとの協働中に、同じ質問・同じ誤解・同じ判断ミスが繰り返された場合、それを個別回答だけで終わらせない。

必要最小限のDocumentation改善を提案する。

ただし、Documentation改善そのものを理由に無関係な設計整理を行わない。

目的はDocumentationを増やすことではなく、将来のAIがより少ない推測で正しく作業できる状態を作ることである。
