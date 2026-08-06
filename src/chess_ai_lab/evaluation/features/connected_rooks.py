import chess

CONNECTED_ROOK_BONUS = 20


def _is_connected(
    board: chess.Board,
    rook1: chess.Square,
    rook2: chess.Square,
) -> bool:
    """
    2つのルークがお互いに見えているか判定する。
    """

    file1 = chess.square_file(rook1)
    rank1 = chess.square_rank(rook1)

    file2 = chess.square_file(rook2)
    rank2 = chess.square_rank(rook2)

    # 同じFile
    if file1 == file2:
        start = min(rank1, rank2) + 1
        end = max(rank1, rank2)

        for rank in range(start, end):
            square = chess.square(file1, rank)

            if board.piece_at(square) is not None:
                return False

        return True

    # 同じRank
    if rank1 == rank2:
        start = min(file1, file2) + 1
        end = max(file1, file2)

        for file in range(start, end):
            square = chess.square(file, rank1)

            if board.piece_at(square) is not None:
                return False

        return True

    return False


def _count_connected_rooks(
    board: chess.Board,
    color: chess.Color,
) -> int:
    """
    Connected Rooks の数を返す。
    """

    rooks = list(board.pieces(chess.ROOK, color))

    if len(rooks) < 2:
        return 0

    if _is_connected(
        board,
        rooks[0],
        rooks[1],
    ):
        return 1

    return 0


def evaluate_connected_rooks(
    board: chess.Board,
) -> int:
    """
    Connected Rooks の評価。
    """

    white = _count_connected_rooks(
        board,
        chess.WHITE,
    )

    black = _count_connected_rooks(
        board,
        chess.BLACK,
    )

    return (
        white - black
    ) * CONNECTED_ROOK_BONUS