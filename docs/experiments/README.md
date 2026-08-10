# Experiments

このディレクトリは、Training、Tuning、Evolution、Benchmarkなどの重要な実験結果を再現可能な形で記録するために使用する。

## Purpose

`docs/status.md` は現在地を示す。

このディレクトリは、過去に何を試し、どの条件で、何が得られたかを残す。

したがって、`status.md` に詳細な実験履歴を蓄積しすぎない。

## Experiment Record

重要な実験では、可能な限り以下を記録する。

- Experiment ID
- Date
- Purpose
- Dataset identifier / path
- Dataset size
- Feature Registry / feature count
- Feature schema hash
- Initial weight source
- Learning rate
- Epochs
- Batch size
- Validation size
- Scheduler configuration
- Other relevant configuration
- Best validation loss
- Best epoch
- Final training loss
- Final validation loss
- Training time
- Output weight path
- WAC result
- Self-play result
- Conclusion
- Follow-up

## Reproducibility

同じ実験を比較するときは、意図した実験変数以外の条件を可能な限り揃える。

特にTraining比較では、次を明示する。

- Dataset
- Initial weights
- Feature schema
- Validation set
- Batch size
- Scheduler
- Epoch count
- Learning rate

## Interpretation

Validation LossとPlaying Strengthは別の測定値として扱う。

Validation Lossが改善しただけで「強くなった」と結論づけない。

WACやSelf Playの比較では、Search depth、Weight、Position set、Search configurationなどの条件を揃える。

## Naming

実験ファイルは、日付と目的が分かる名前を基本とする。

例：

```text
2026-08-10-lr-5.0.md
2026-08-11-epoch-comparison.md
2026-08-12-wac-trained-vs-built-in.md
```

## Relation to Status

実験完了後、現在の開発判断に影響する結果は `docs/status.md` のCurrent Training / Current Investigation / Next Taskへ必要最小限反映する。

詳細はこのディレクトリのExperiment Recordを参照する。
