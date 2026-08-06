# Evaluation System

## Purpose

Evaluation は盤面を数値で評価する責務を持つ。

Search は Evaluation を利用するが、
Evaluation は Search を知らない。

Evaluation の目的は

- 局面の良し悪しを数値化すること
- Feature を独立して追加・改善できること
- Weight Evolution の対象を明確にすること

である。

---

# Architecture

Evaluation の構造は以下で固定する。

Board

↓

Evaluator

↓

Feature Registry

↓

Feature

↓

Raw Score

↓

Weight

↓

Final Score

---

# Responsibilities

## Evaluator

責務

- Feature を実行する
- Weight を取得する
- 最終評価値を計算する

Evaluator は Feature の実装詳細を知らない。

---

## Feature

責務

盤面から

1つの評価値

を計算する。

Feature は

raw score

のみ返す。

Weight を掛けない。

---

## WeightManager

責務

Feature Weight の管理。

Weight の保存・読込・複製・突然変異を担当する。

評価計算は行わない。

---

# Evaluation Formula

最終評価値

score = Σ(raw_feature × weight)

Weight は Evaluator が適用する。

---

# Feature Rules

各 Feature は

1ファイル

1責務

とする。

例

material.py

bishop_pair.py

space.py

など。

---

# Feature Requirements

Feature は

- Board を変更しない
- Weight を知らない
- Search を知らない
- 他 Feature を知らない

---

# Current Features

## Material

目的

駒得・駒損を評価する。

---

## Piece Square

目的

駒配置を評価する。

---

## Mobility

目的

合法手数を評価する。

---

## Pawn Structure

目的

Pawn Structure を評価する。

現在

- Isolated Pawn
- Doubled Pawn
- Passed Pawn

---

## King Safety

目的

King の安全性を評価する。

---

## Bishop Pair

目的

Bishop Pair の価値を評価する。

---

## Pawn Shield

目的

King 前の Pawn Shield を評価する。

---

## Rook File

目的

Open File を評価する。

---

## Connected Rooks

目的

Connected Rooks を評価する。

---

## Rook Seventh

目的

7段目支配を評価する。

---

## Space

目的

Space Advantage を評価する。

---

## Knight Outpost

目的

Knight Outpost を評価する。

---

# Future Features

将来的に追加候補

King Activity

Weak Squares

Pinned Pieces

Trapped Pieces

Initiative

Tempo

Piece Coordination

Center Control

---

# Weight Evolution

Weight Evolution の対象は

Feature Weight

のみである。

Feature のアルゴリズムは Evolution の対象外。

---

# Non Goals

Evaluation は

探索

学習

Weight Mutation

を行わない。

これらは別レイヤーの責務である。