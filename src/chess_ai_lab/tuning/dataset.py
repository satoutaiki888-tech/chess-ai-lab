from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterator


@dataclass(slots=True)
class PositionSample:
    """
    Texel Tuning 用の1局面。

    Parameters
    ----------
    fen
        Position FEN.
    cp
        Stockfish centipawn evaluation.
    mate
        Mate score if available.
    """

    fen: str
    cp: int | None
    mate: int | None


class PositionDataset(ABC):
    """
    Position dataset interface.

    Responsibilities
    ----------------
    - Supply training positions.
    - Support sequential iteration.

    Must Not
    --------
    - Weight update
    - Loss calculation
    - Optimization
    """

    @abstractmethod
    def __iter__(self) -> Iterator[PositionSample]:
        """Yield PositionSample objects."""
        raise NotImplementedError