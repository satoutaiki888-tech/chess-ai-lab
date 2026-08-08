from __future__ import annotations

import numpy as np

from chess_ai_lab.evaluation.weight_manager import (
    WeightManager,
)


class WeightVector:
    """
    学習専用のWeightベクトル。

    WeightManagerの辞書をNumPy配列としてキャッシュし、
    SGD更新を高速化する。
    """

    def __init__(
        self,
        weight_manager: WeightManager,
    ):
        self._weight_manager = weight_manager

        self._weights = (
            weight_manager.to_array()
        )

    @property
    def array(self) -> np.ndarray:
        """
        NumPy配列を返す。
        """
        return self._weights

    def apply_gradient(
        self,
        gradients: np.ndarray,
        learning_rate: float,
    ) -> None:
        """
        SGD更新を行う。
        """

        self._weights -= (
            learning_rate
            * gradients
        )

    def sync_to_manager(self) -> None:
        """
        WeightManagerへ同期する。
        """

        self._weight_manager.from_array(
            self._weights
        )