from abc import ABC, abstractmethod

from chess_ai_lab.board import ChessBoard


class Player(ABC):
    """チェスプレイヤーの共通インターフェース"""

    @abstractmethod
    def choose_move(self, board: ChessBoard):
        """
        現在の局面から次の一手を選択する。

        Returns:
            chess.Move
        """
        raise NotImplementedError