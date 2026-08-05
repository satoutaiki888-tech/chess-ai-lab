import chess


class ChessBoard:
    """python-chess の Board をラップするクラス"""

    def __init__(self):
        self._board = chess.Board()

    def reset(self):
        """初期局面に戻す"""
        self._board.reset()

    def push(self, move):
        """指し手を適用する"""
        self._board.push(move)

    def pop(self):
        """最後の指し手を取り消す"""
        return self._board.pop()

    def legal_moves(self):
        """合法手一覧を返す"""
        return list(self._board.legal_moves)

    def fen(self):
        """FEN文字列を返す"""
        return self._board.fen()

    def is_game_over(self):
        """終局判定"""
        return self._board.is_game_over()

    def turn(self):
        """手番を返す（True=白, False=黒）"""
        return self._board.turn

    def board(self):
        """内部の Board オブジェクトを返す"""
        return self._board


if __name__ == "__main__":
    board = ChessBoard()
    print(board.board())