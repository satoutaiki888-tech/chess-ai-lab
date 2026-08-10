# Changelog

このファイルは、プロジェクトの重要な変更を時系列で簡潔に記録する。

詳細な設計理由は `docs/decisions.md`、現在地は `docs/status.md`、実験条件と結果は `docs/experiments/` を参照する。

---

## 2026-08-10

### AI Collaboration Documentation

- Added `AGENTS.md` as the AI development entry guide.
- Added `docs/ai_workflow.md` for the standard AI collaboration workflow.
- Added `docs/decisions.md` to preserve important design rationale.
- Updated `docs/AI_CONTEXT.md` to align the existing AI context with the new documentation structure.
- Added `docs/testing.md` for Test strategy and architecture verification guidance.
- Added `docs/experiments/README.md` for reproducible experiment records.
- Added the recorded LR=1.0 training experiment to `docs/experiments/2026-08-09-lr-1.0.md`.

These changes are documentation-only and do not change runtime behavior.

---

## Maintenance Rule

Changelogには重要な変更だけを記録する。

細かな実装変更や各Experimentの詳細は、それぞれの適切なDocumentationを参照する。
