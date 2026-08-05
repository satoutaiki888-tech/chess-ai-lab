import time

from chess_ai_lab.board import ChessBoard
from chess_ai_lab.engine.minimax import MinimaxPlayer
from chess_ai_lab.engine.alphabeta import AlphaBetaPlayer


def run(player, name):

    board = ChessBoard()

    start = time.time()

    move = player.choose_move(board)

    elapsed = time.time() - start

    print(name)
    print("move:", move)
    print("nodes:", player.nodes)
    print("time:", round(elapsed, 4))
    print()


def main():

    run(
        MinimaxPlayer(depth=3),
        "Minimax depth=3",
    )

    run(
        AlphaBetaPlayer(depth=3),
        "AlphaBeta depth=3",
    )


if __name__ == "__main__":
    main()