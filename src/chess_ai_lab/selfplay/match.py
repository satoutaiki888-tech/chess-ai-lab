import random

from chess_ai_lab.board import ChessBoard
from chess_ai_lab.selfplay.pgn import save_game


class RandomPlayer:
    """合法手からランダムに1手選ぶプレイヤー"""

    def choose_move(self, board: ChessBoard):
        moves = board.legal_moves()
        return random.choice(moves)


def main():
    board = ChessBoard()
    player = RandomPlayer()

    print(board.board())
    print()

    while not board.is_game_over():
        move = player.choose_move(board)
        print(move)

        board.push(move)

        print(board.board())
        print()

    save_game(board.board(), "random_vs_random.pgn")

    print("Game Over")
    print("PGN saved: random_vs_random.pgn")


if __name__ == "__main__":
    main()