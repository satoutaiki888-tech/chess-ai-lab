# Invariants

## Purpose

この文書は `chess-ai-lab` において常に維持されるべき設計・開発上の不変条件（Invariants）を定義する。

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

Search
↓
Benchmark

Search
↓
Self Play

Evaluation
↓
Tuning

Evaluation
↓
Evolution

逆方向の依存は禁止。

レイヤーは上