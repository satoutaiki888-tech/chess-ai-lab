
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq


# ============================================================================
# Feature metadata
# ============================================================================

DEFAULT_FEATURE_NAMES = [
    "material",
    "piece_square",
    "mobility",
    "isolated_pawn",
    "doubled_pawn",
    "passed_pawn",
    "king_safety",
    "bishop_pair",
    "open_file",
    "semi_open_file",
    "pawn_shield",
    "knight_outpost",
    "connected_rooks",
    "rook_seventh",
    "space",
    "bishop_mobility",
    "rook_mobility",
    "knight_mobility",
    "queen_mobility",
]


# ============================================================================
# Phase definitions
# ============================================================================

# Conventional non-pawn material phase weights.
#
# Queen  = 4
# Rook   = 2
# Bishop = 1
# Knight = 1
#
# Starting position:
#   2 * 4 + 4 * 2 + 4 * 1 = 24
#
# Pawns are intentionally excluded because "material phase" here is meant
# to describe the transition from middlegame to endgame based on pieces.
PIECE_PHASE_WEIGHTS = {
    "q": 4,
    "r": 2,
    "b": 1,
    "n": 1,
}


def calculate_material_phase(fen: str) -> int:
    """
    Calculate remaining non-pawn material phase from a FEN.

    Maximum is normally 24 in the initial position.
    Kings and pawns do not contribute.

    Returns:
        Integer in approximately [0, 24].
    """

    board = fen.split()[0]

    phase = 0

    for char in board:
        piece = char.lower()

        if piece in PIECE_PHASE_WEIGHTS:
            phase += PIECE_PHASE_WEIGHTS[piece]

    return phase


def game_phase_from_material_phase(
    material_phase: int,
) -> str:
    """
    Convert material phase into broad game-phase buckets.

    These boundaries are intentionally simple and interpretable.
    They can be changed later after inspecting the distribution.
    """

    if material_phase >= 20:
        return "opening"

    if material_phase >= 14:
        return "early_middlegame"

    if material_phase >= 9:
        return "middlegame"

    if material_phase >= 5:
        return "late_middlegame"

    return "endgame"


# ============================================================================
# Statistics
# ============================================================================


def safe_corr_from_sums(
    n: int,
    sum_x: float,
    sum_y: float,
    sum_x2: float,
    sum_y2: float,
    sum_xy: float,
) -> float | None:
    """Calculate Pearson correlation from accumulated sums."""

    if n <= 1:
        return None

    numerator = (
        n * sum_xy
        - sum_x * sum_y
    )

    denominator_x = (
        n * sum_x2
        - sum_x * sum_x
    )

    denominator_y = (
        n * sum_y2
        - sum_y * sum_y
    )

    if denominator_x <= 0 or denominator_y <= 0:
        return None

    denominator = np.sqrt(
        denominator_x * denominator_y
    )

    if denominator == 0:
        return None

    return float(numerator / denominator)


def basic_stats(
    values: np.ndarray,
) -> dict[str, float | int]:

    values = values.astype(
        np.float64,
        copy=False,
    )

    if values.size == 0:
        return {
            "count": 0,
        }

    return {
        "count": int(values.size),
        "mean": float(np.mean(values)),
        "std": float(np.std(values)),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "mae_from_zero": float(
            np.mean(np.abs(values))
        ),
        "zero_ratio": float(
            np.mean(values == 0)
        ),
        "positive_ratio": float(
            np.mean(values > 0)
        ),
        "negative_ratio": float(
            np.mean(values < 0)
        ),
    }


# ============================================================================
# Phase accumulator
# ============================================================================


class PhaseAccumulator:
    """
    Streaming sufficient statistics for one phase.

    We intentionally do not retain all samples in memory.

    This allows the analysis to run on the full 1M dataset while keeping
    memory usage reasonable.
    """

    def __init__(
        self,
        feature_count: int,
    ) -> None:

        self.feature_count = feature_count

        self.count = 0

        self.target_sum = 0.0
        self.target_sum2 = 0.0

        self.target_abs_sum = 0.0

        self.target_positive = 0
        self.target_negative = 0
        self.target_zero = 0

        # Feature sums.
        self.feature_sum = np.zeros(
            feature_count,
            dtype=np.float64,
        )

        # Feature squared sums.
        self.feature_sum2 = np.zeros(
            feature_count,
            dtype=np.float64,
        )

        # Feature-target cross products.
        self.feature_target_sum = np.zeros(
            feature_count,
            dtype=np.float64,
        )

        # For linear regression:
        #
        # X'X
        #
        # and
        #
        # X'y
        #
        self.xtx = np.zeros(
            (
                feature_count,
                feature_count,
            ),
            dtype=np.float64,
        )

        self.xty = np.zeros(
            feature_count,
            dtype=np.float64,
        )

        self.target_values: list[np.ndarray] = []

    def update(
        self,
        features: np.ndarray,
        target: np.ndarray,
        keep_target: bool = False,
    ) -> None:

        if features.size == 0:
            return

        n = len(target)

        self.count += n

        self.target_sum += float(
            np.sum(target)
        )

        self.target_sum2 += float(
            np.sum(target * target)
        )

        self.target_abs_sum += float(
            np.sum(np.abs(target))
        )

        self.target_positive += int(
            np.sum(target > 0)
        )

        self.target_negative += int(
            np.sum(target < 0)
        )

        self.target_zero += int(
            np.sum(target == 0)
        )

        self.feature_sum += np.sum(
            features,
            axis=0,
        )

        self.feature_sum2 += np.sum(
            features * features,
            axis=0,
        )

        self.feature_target_sum += (
            features.T @ target
        )

        self.xtx += (
            features.T @ features
        )

        self.xty += (
            features.T @ target
        )

        if keep_target:
            self.target_values.append(
                target.copy()
            )

    def merge(
        self,
        other: "PhaseAccumulator",
    ) -> None:

        self.count += other.count

        self.target_sum += other.target_sum
        self.target_sum2 += other.target_sum2
        self.target_abs_sum += other.target_abs_sum

        self.target_positive += (
            other.target_positive
        )

        self.target_negative += (
            other.target_negative
        )

        self.target_zero += (
            other.target_zero
        )

        self.feature_sum += (
            other.feature_sum
        )

        self.feature_sum2 += (
            other.feature_sum2
        )

        self.feature_target_sum += (
            other.feature_target_sum
        )

        self.xtx += other.xtx
        self.xty += other.xty

    def target_stats(self) -> dict:

        if self.count == 0:
            return {
                "count": 0,
            }

        mean = (
            self.target_sum
            / self.count
        )

        variance = (
            self.target_sum2
            / self.count
            - mean * mean
        )

        variance = max(
            variance,
            0.0,
        )

        return {
            "count": self.count,
            "mean": mean,
            "std": float(
                np.sqrt(variance)
            ),
            "mae": (
                self.target_abs_sum
                / self.count
            ),
            "positive_ratio": (
                self.target_positive
                / self.count
            ),
            "negative_ratio": (
                self.target_negative
                / self.count
            ),
            "zero_ratio": (
                self.target_zero
                / self.count
            ),
        }

    def feature_stats(
        self,
        feature_names: list[str],
    ) -> dict:

        result = {}

        if self.count == 0:
            return result

        for i, name in enumerate(
            feature_names
        ):

            mean = (
                self.feature_sum[i]
                / self.count
            )

            variance = (
                self.feature_sum2[i]
                / self.count
                - mean * mean
            )

            variance = max(
                variance,
                0.0,
            )

            corr = safe_corr_from_sums(
                self.count,
                self.feature_sum[i],
                self.target_sum,
                self.feature_sum2[i],
                self.target_sum2,
                self.feature_target_sum[i],
            )

            result[name] = {
                "mean": float(mean),
                "std": float(
                    np.sqrt(variance)
                ),
                "target_correlation": corr,
            }

        return result

    def linear_model(
        self,
        feature_names: list[str],
    ) -> dict:

        if self.count == 0:
            return {}

        # ------------------------------------------------------------------
        # Center the normal equations.
        #
        # The model is:
        #
        #   y = intercept + X beta
        #
        # We use centered X/y to avoid explicitly storing an intercept
        # column.
        # ------------------------------------------------------------------

        n = float(self.count)

        mean_x = (
            self.feature_sum
            / n
        )

        mean_y = (
            self.target_sum
            / n
        )

        centered_xtx = (
            self.xtx
            - np.outer(
                self.feature_sum,
                self.feature_sum,
            ) / n
        )

        centered_xty = (
            self.xty
            - self.feature_sum
            * self.target_sum
            / n
        )

        # Small ridge term only for numerical stability.
        ridge = 1e-8

        matrix = (
            centered_xtx
            + np.eye(
                self.feature_count
            ) * ridge
        )

        try:
            beta = np.linalg.solve(
                matrix,
                centered_xty,
            )
        except np.linalg.LinAlgError:
            beta = np.linalg.lstsq(
                matrix,
                centered_xty,
                rcond=None,
            )[0]

        intercept = (
            mean_y
            - np.dot(
                mean_x,
                beta,
            )
        )

        # Explained variance:
        #
        # SST = centered y^2
        #
        target_sst = (
            self.target_sum2
            - self.target_sum
            * self.target_sum
            / n
        )

        explained = float(
            np.dot(
                beta,
                centered_xty,
            )
        )

        if target_sst > 0:
            r2 = explained / target_sst
        else:
            r2 = 0.0

        r2 = float(
            np.clip(
                r2,
                -1.0,
                1.0,
            )
        )

        # Residual sum of squares:
        rss = max(
            target_sst - explained,
            0.0,
        )

        rmse = float(
            np.sqrt(
                rss / n
            )
        )

        # MAE cannot be recovered exactly from sufficient statistics.
        # We therefore report RMSE here and explicitly leave MAE absent.
        #
        # The global analysis already provides MAE.
        standardized_beta = (
            beta
            * np.sqrt(
                np.maximum(
                    (
                        self.feature_sum2
                        / n
                        - mean_x * mean_x
                    ),
                    0.0,
                )
            )
        )

        ranking = sorted(
            zip(
                feature_names,
                standardized_beta,
            ),
            key=lambda x: abs(x[1]),
            reverse=True,
        )

        return {
            "r2": r2,
            "rmse": rmse,
            "intercept": float(
                intercept
            ),
            "coefficients": {
                name: float(value)
                for name, value in zip(
                    feature_names,
                    beta,
                )
            },
            "standardized_coefficients": {
                name: float(value)
                for name, value in ranking
            },
        }


# ============================================================================
# FEN / phase extraction
# ============================================================================


def classify_fen(
    fen: str,
) -> tuple[str, int]:

    material_phase = (
        calculate_material_phase(fen)
    )

    game_phase = (
        game_phase_from_material_phase(
            material_phase
        )
    )

    return (
        game_phase,
        material_phase,
    )


# ============================================================================
# Dataset processing
# ============================================================================


def process_dataset(
    path: Path,
    feature_names: list[str],
    accumulators: dict[str, PhaseAccumulator],
    material_accumulators: dict[int, PhaseAccumulator],
    batch_size: int,
) -> None:

    print(f"Loading: {path}")

    parquet = pq.ParquetFile(path)

    total_rows = parquet.metadata.num_rows

    print(
        f"Rows   : {total_rows:,}"
    )

    for batch in parquet.iter_batches(
        batch_size=batch_size,
        columns=[
            "fen",
            "target_cp",
            "feature_values",
        ],
    ):

        fen_values = (
            batch["fen"]
            .to_pylist()
        )

        targets = np.asarray(
            batch["target_cp"],
            dtype=np.float64,
        )

        features = np.asarray(
            batch["feature_values"]
            .to_pylist(),
            dtype=np.float64,
        )

        if features.ndim != 2:
            raise ValueError(
                "feature_values is not 2-dimensional."
            )

        if features.shape[1] != len(
            feature_names
        ):
            raise ValueError(
                "Feature count mismatch: "
                f"{features.shape[1]} != "
                f"{len(feature_names)}"
            )

        phase_indices: dict[
            str,
            list[int],
        ] = {}

        material_indices: dict[
            int,
            list[int],
        ] = {}

        for index, fen in enumerate(
            fen_values
        ):

            game_phase, material_phase = (
                classify_fen(fen)
            )

            phase_indices.setdefault(
                game_phase,
                [],
            ).append(index)

            material_indices.setdefault(
                material_phase,
                [],
            ).append(index)

        # ---------------------------------------------------------------
        # Game phase
        # ---------------------------------------------------------------

        for phase, indices in (
            phase_indices.items()
        ):

            idx = np.asarray(
                indices,
                dtype=np.int64,
            )

            accumulators[phase].update(
                features[idx],
                targets[idx],
            )

        # ---------------------------------------------------------------
        # Material phase
        #
        # Do NOT assume material phase is limited to 0..24.
        #
        # Promoted pieces can make the conventional non-pawn material
        # phase exceed the initial-position value of 24.
        # ---------------------------------------------------------------

        for phase, indices in (
            material_indices.items()
        ):

            if phase not in material_accumulators:
                material_accumulators[
                    phase
                ] = PhaseAccumulator(
                    len(feature_names)
                )

            idx = np.asarray(
                indices,
                dtype=np.int64,
            )

            material_accumulators[
                phase
            ].update(
                features[idx],
                targets[idx],
            )


# ============================================================================
# Output
# ============================================================================


GAME_PHASE_ORDER = [
    "opening",
    "early_middlegame",
    "middlegame",
    "late_middlegame",
    "endgame",
]


def build_phase_report(
    accumulators: dict[str, PhaseAccumulator],
    feature_names: list[str],
) -> dict:

    report = {}

    for phase in GAME_PHASE_ORDER:

        accumulator = accumulators[
            phase
        ]

        report[phase] = {
            "target": (
                accumulator.target_stats()
            ),
            "features": (
                accumulator.feature_stats(
                    feature_names
                )
            ),
            "linear_model": (
                accumulator.linear_model(
                    feature_names
                )
            ),
        }

    return report


def build_material_report(
    accumulators: dict[int, PhaseAccumulator],
    feature_names: list[str],
) -> dict:

    report = {}

    for material_phase in sorted(
        accumulators.keys(),
        reverse=True,
    ):

        accumulator = accumulators[
            material_phase
        ]

        if accumulator.count == 0:
            continue

        report[str(material_phase)] = {
            "game_phase": (
                game_phase_from_material_phase(
                    material_phase
                )
            ),
            "target": (
                accumulator.target_stats()
            ),
            "features": (
                accumulator.feature_stats(
                    feature_names
                )
            ),
            "linear_model": (
                accumulator.linear_model(
                    feature_names
                )
            ),
        }

    return report


def print_game_phase_report(
    report: dict,
    feature_names: list[str],
) -> None:

    print()
    print("=" * 100)
    print("GAME PHASE ANALYSIS")
    print("=" * 100)

    for phase in GAME_PHASE_ORDER:

        data = report[phase]
        target = data["target"]

        if target["count"] == 0:
            continue

        print()
        print(
            f"[{phase}]"
        )
        print("-" * 100)

        print(
            f"Samples : "
            f"{target['count']:,}"
        )

        print(
            f"Target mean : "
            f"{target['mean']:.4f}"
        )

        print(
            f"Target std  : "
            f"{target['std']:.4f}"
        )

        print(
            f"Target MAE  : "
            f"{target['mae']:.4f}"
        )

        print(
            f"Positive    : "
            f"{target['positive_ratio']:.4%}"
        )

        print(
            f"Negative    : "
            f"{target['negative_ratio']:.4%}"
        )

        print()
        print(
            f"{'Feature':<22}"
            f"{'Mean':>12}"
            f"{'Std':>12}"
            f"{'Corr':>12}"
        )

        print("-" * 60)

        features = data["features"]

        ranking = sorted(
            (
                (
                    name,
                    values[
                        "target_correlation"
                    ],
                )
                for name, values
                in features.items()
                if values[
                    "target_correlation"
                ] is not None
            ),
            key=lambda x: abs(x[1]),
            reverse=True,
        )

        for name, corr in ranking:

            stats = features[name]

            print(
                f"{name:<22}"
                f"{stats['mean']:>12.4f}"
                f"{stats['std']:>12.4f}"
                f"{corr:>12.4f}"
            )

        model = data[
            "linear_model"
        ]

        print()
        print("Linear Baseline")
        print("-" * 60)

        print(
            f"R²   : {model['r2']:.6f}"
        )

        print(
            f"RMSE : {model['rmse']:.4f}"
        )

        print()
        print(
            "Standardized Coefficients"
        )
        print("-" * 60)

        for rank, (
            name,
            coefficient,
        ) in enumerate(
            model[
                "standardized_coefficients"
            ].items(),
            start=1,
        ):

            print(
                f"{rank:>2}. "
                f"{name:<22}"
                f"{coefficient:>12.4f}"
            )


def print_material_phase_report(
    report: dict,
) -> None:

    print()
    print("=" * 100)
    print("MATERIAL PHASE ANALYSIS")
    print("=" * 100)

    print()
    print(
        f"{'Phase':<10}"
        f"{'Game Phase':<22}"
        f"{'Samples':>12}"
        f"{'Target Mean':>14}"
        f"{'Target Std':>14}"
        f"{'R²':>12}"
    )

    print("-" * 100)

    for phase, data in report.items():

        target = data["target"]
        model = data["linear_model"]

        print(
            f"{phase:<10}"
            f"{data['game_phase']:<22}"
            f"{target['count']:>12,}"
            f"{target['mean']:>14.4f}"
            f"{target['std']:>14.4f}"
            f"{model['r2']:>12.6f}"
        )

    print()

    # ------------------------------------------------------------------
    # Most interesting feature for every material phase.
    # ------------------------------------------------------------------

    print(
        "Top Feature Correlations by Material Phase"
    )
    print("-" * 100)

    for phase, data in report.items():

        ranking = sorted(
            (
                (
                    name,
                    values[
                        "target_correlation"
                    ],
                )
                for name, values
                in data["features"].items()
                if values[
                    "target_correlation"
                ] is not None
            ),
            key=lambda x: abs(x[1]),
            reverse=True,
        )

        print()
        print(
            f"material_phase={phase} "
            f"game_phase={data['game_phase']}"
        )

        for rank, (
            name,
            corr,
        ) in enumerate(
            ranking[:10],
            start=1,
        ):

            print(
                f"{rank:>2}. "
                f"{name:<22}"
                f"r={corr:>10.6f}"
            )


# ============================================================================
# CLI
# ============================================================================


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description=(
            "Analyze chess training data by "
            "game phase and material phase."
        )
    )

    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(
            "data/training/1m"
        ),
        help=(
            "Directory containing "
            "train.parquet and valid.parquet."
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "JSON output path. "
            "Defaults to "
            "<data-dir>/phase_analysis.json."
        ),
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=10000,
        help=(
            "Parquet batch size."
        ),
    )

    return parser.parse_args()


# ============================================================================
# Main
# ============================================================================


def main() -> None:

    args = parse_args()

    train_path = (
        args.data_dir
        / "train.parquet"
    )

    valid_path = (
        args.data_dir
        / "valid.parquet"
    )

    if not train_path.exists():
        raise FileNotFoundError(
            f"Train dataset not found: "
            f"{train_path}"
        )

    if not valid_path.exists():
        raise FileNotFoundError(
            f"Validation dataset not found: "
            f"{valid_path}"
        )

    feature_names = (
        DEFAULT_FEATURE_NAMES
    )

    game_phase_accumulators = {
        phase: PhaseAccumulator(
            len(feature_names)
        )
        for phase in GAME_PHASE_ORDER
    }

    material_phase_accumulators: dict[
        int,
        PhaseAccumulator,
    ] = {}

    print()
    print(
        "Running Phase Analysis..."
    )

    print()
    print(
        "Processing training dataset..."
    )

    process_dataset(
        train_path,
        feature_names,
        game_phase_accumulators,
        material_phase_accumulators,
        args.batch_size,
    )

    print()
    print(
        "Processing validation dataset..."
    )

    process_dataset(
        valid_path,
        feature_names,
        game_phase_accumulators,
        material_phase_accumulators,
        args.batch_size,
    )

    print()
    print(
        "Building reports..."
    )

    game_phase_report = (
        build_phase_report(
            game_phase_accumulators,
            feature_names,
        )
    )

    material_phase_report = (
        build_material_report(
            material_phase_accumulators,
            feature_names,
        )
    )

    print_game_phase_report(
        game_phase_report,
        feature_names,
    )

    print_material_phase_report(
        material_phase_report,
    )

    report = {
        "dataset": {
            "data_dir": str(
                args.data_dir
            ),
            "feature_count": len(
                feature_names
            ),
            "feature_names": (
                feature_names
            ),
        },
        "phase_definition": {
            "material_phase_weights": (
                PIECE_PHASE_WEIGHTS
            ),
            "maximum_material_phase": 24,
            "game_phase_boundaries": {
                "opening": "20-24",
                "early_middlegame": "14-19",
                "middlegame": "9-13",
                "late_middlegame": "5-8",
                "endgame": "0-4",
            },
        },
        "game_phase": game_phase_report,
        "material_phase": (
            material_phase_report
        ),
    }

    output_path = (
        args.output
        if args.output is not None
        else (
            args.data_dir
            / "phase_analysis.json"
        )
    )

    output_path.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print()
    print("=" * 100)
    print(
        f"Phase analysis JSON saved: "
        f"{output_path}"
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
