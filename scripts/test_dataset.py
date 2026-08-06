from chess_ai_lab.tuning.dataset import ParquetDataset

dataset = ParquetDataset(
    "data/training/train.parquet",
)

for i, position in enumerate(dataset):
    print(position.board.fen())
    print(position.target_cp)
    print(position.source_depth)
    print()

    if i == 9:
        break