from dataclasses import dataclass
from pathlib import Path
import chess

@dataclass(slots=True, frozen=True)
class EPDPosition:
    """
    EPDの1問。
    """

    epd: str
    best_moves: list[chess.Move]
    position_id: str


def parse_epd(line: str) -> EPDPosition:
    """
    EPD1行を読み込む。
    """

    line = line.strip()

    if not line:
        raise ValueError("Empty EPD line.")

    board = chess.Board()

    operations = board.set_epd(line)

    return EPDPosition(
        epd=line,
        best_moves=operations.get("bm", []),
        position_id=operations.get("id", ""),
    )
    
def load_epd(
    path: str | Path,
) -> list[EPDPosition]:
    """
    EPDファイルを読み込む。

    Parameters
    ----------
    path
        EPDファイルへのパス。

    Returns
    -------
    list[EPDPosition]
    """

    path = Path(path)

    positions: list[EPDPosition] = []

    with path.open("r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            positions.append(
                parse_epd(line)
            )

    return positions

if __name__ == "__main__":

    positions = load_epd("data/wac.epd")

    print(f"{len(positions)} positions loaded.")
    print()

    first = positions[0]

    print(first.position_id)
    print(first.best_moves)