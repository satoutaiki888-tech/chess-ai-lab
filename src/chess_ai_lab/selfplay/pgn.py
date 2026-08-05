import chess.pgn


def save_game(board, filename: str):
    """
    対局をPGN形式で保存する。

    Parameters
    ----------
    board : chess.Board
        対局終了後の Board
    filename : str
        保存先ファイル名
    """

    game = chess.pgn.Game.from_board(board)

    with open(filename, "w", encoding="utf-8") as f:
        print(game, file=f)