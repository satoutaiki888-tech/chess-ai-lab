from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq


# ---------------------------------------------------------------------------
# Feature / dataset metadata
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TARGET_CLAMP = 1000.0

FEATURE_BIN_COUNT = 10

DEPTH_BUCKETS = [
    (20, 24),
    (25, 29),
    (30, 34),
    (35, 39),
    (40, 49),
    (50, 69),
    (70, 99),
    (100, float("inf")),
]


# ---------------------------------------------------------------------------
# Statistics helpers
# ---------------------------------------------------------------------------


def percentile_dict(
    values: np.ndarray,
) -> dict[str, float]:
    """Return useful percentiles for a numeric array."""

    if values.size == 0:
        return {}

    percentiles = [
        0,
        1,
        5,
        10,
        25,
        50,
        75,
        90,
        95,
        99,
        100,
    ]

    return {
        f"p{p}": float(np.percentile(values, p))
        for p in percentiles
    }


def basic_stats(
    values: np.ndarray,
) -> dict[str, float | int]:
    """Return basic descriptive statistics."""

    values = values.astype(np.float64, copy=False)

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
        "abs_mean": float(np.mean(np.abs(values))),
        "zero_ratio": float(np.mean(values == 0)),
        **percentile_dict(values),
    }


def correlation(
    x: np.ndarray,
    y: np.ndarray,
) -> float | None:
    """Pearson correlation."""

    if x.size == 0 or y.size == 0:
        return None

    x_std = np.std(x)
    y_std = np.std(y)

    if x_std == 0 or y_std == 0:
        return None

    return float(np.corrcoef(x, y)[0, 1])


def rank_correlation(
    x: np.ndarray,
    y: np.ndarray,
) -> float | None:
    """
    Spearman-like rank correlation.

    Implemented without scipy so that the analysis script does not require
    another dependency.
    """

    if x.size == 0 or y.size == 0:
        return None

    if np.std(x) == 0 or np.std(y) == 0:
        return None

    x_order = np.argsort(np.argsort(x))
    y_order = np.argsort(np.argsort(y))

    return correlation(
        x_order.astype(np.float64),
        y_order.astype(np.float64),
    )


def histogram(
    values: np.ndarray,
    bins: list[float],
) -> dict[str, int]:
    """Return histogram counts using explicit bin boundaries."""

    counts, edges = np.histogram(
        values,
        bins=np.asarray(bins, dtype=np.float64),
    )

    result = {}

    for index, count in enumerate(counts):
        left = edges[index]
        right = edges[index + 1]

        result[f"[{left:g}, {right:g})"] = int(count)

    return result


# ---------------------------------------------------------------------------
# Parquet loading
# ---------------------------------------------------------------------------


def load_dataset(
    path: Path,
) -> tuple[dict, np.ndarray, np.ndarray, list[str], np.ndarray]:

    print(f"Loading: {path}")

    table = pq.read_table(
        path,
        columns=[
            "target_cp",
            "source_depth",
            "feature_values",
        ],
    )

    print(f"Rows   : {table.num_rows:,}")

    metadata = table.schema.metadata or {}

    feature_names = DEFAULT_FEATURE_NAMES

    raw_names = metadata.get(
        b"chess_ai_lab.feature_names"
    )

    if raw_names is not None:
        feature_names = json.loads(
            raw_names.decode("utf-8")
        )

    target_cp = np.asarray(
        table["target_cp"].to_numpy(),
        dtype=np.float64,
    )

    source_depth = np.asarray(
        table["source_depth"].to_numpy(),
        dtype=np.float64,
    )

    feature_matrix = np.asarray(
        table["feature_values"].to_pylist(),
        dtype=np.float64,
    )

    if feature_matrix.ndim != 2:
        raise ValueError(
            "feature_values could not be converted "
            "to a 2D matrix."
        )

    if feature_matrix.shape[1] != len(feature_names):
        raise ValueError(
            "Feature count mismatch: "
            f"metadata={len(feature_names)}, "
            f"matrix={feature_matrix.shape[1]}"
        )

    return (
        metadata,
        target_cp,
        source_depth,
        feature_names,
        feature_matrix,
    )


# ---------------------------------------------------------------------------
# Basic dataset analysis
# ---------------------------------------------------------------------------


def analyze_dataset(
    path: Path,
) -> dict:

    (
        metadata,
        target_cp,
        source_depth,
        feature_names,
        feature_matrix,
    ) = load_dataset(path)

    sample_count = len(target_cp)

    result: dict = {
        "path": str(path),
        "sample_count": sample_count,
        "feature_count": len(feature_names),
        "feature_names": feature_names,
        "metadata": {},
        "target_cp": {},
        "source_depth": {},
        "features": {},
        "feature_target_correlations": {},
    }

    for key, value in metadata.items():

        decoded_key = key.decode("utf-8")

        try:
            decoded_value = value.decode("utf-8")
        except UnicodeDecodeError:
            decoded_value = repr(value)

        result["metadata"][decoded_key] = decoded_value

    # ------------------------------------------------------------------
    # Target
    # ------------------------------------------------------------------

    result["target_cp"] = basic_stats(target_cp)

    result["target_cp"]["histogram"] = histogram(
        target_cp,
        bins=[
            -1000,
            -800,
            -600,
            -400,
            -200,
            -100,
            -50,
            0,
            50,
            100,
            200,
            400,
            600,
            800,
            1000.000001,
        ],
    )

    result["target_cp"]["positive_ratio"] = float(
        np.mean(target_cp > 0)
    )

    result["target_cp"]["negative_ratio"] = float(
        np.mean(target_cp < 0)
    )

    result["target_cp"]["zero_ratio"] = float(
        np.mean(target_cp == 0)
    )

    result["target_cp"]["clamp_negative_ratio"] = float(
        np.mean(target_cp <= -TARGET_CLAMP)
    )

    result["target_cp"]["clamp_positive_ratio"] = float(
        np.mean(target_cp >= TARGET_CLAMP)
    )

    # ------------------------------------------------------------------
    # Source depth
    # ------------------------------------------------------------------

    result["source_depth"] = basic_stats(
        source_depth
    )

    unique_depths, depth_counts = np.unique(
        source_depth,
        return_counts=True,
    )

    result["source_depth"]["distribution"] = {
        str(int(depth)): int(count)
        for depth, count in zip(
            unique_depths,
            depth_counts,
        )
    }

    # ------------------------------------------------------------------
    # Feature statistics
    # ------------------------------------------------------------------

    feature_target_correlations = []

    for index, name in enumerate(feature_names):

        values = feature_matrix[:, index]

        stats = basic_stats(values)

        stats["unique_count"] = int(
            np.unique(values).size
        )

        stats["constant"] = bool(
            np.all(values == values[0])
        )

        stats["near_zero_ratio"] = float(
            np.mean(np.abs(values) < 1e-8)
        )

        stats["nan_count"] = int(
            np.isnan(values).sum()
        )

        stats["inf_count"] = int(
            np.isinf(values).sum()
        )

        stats["target_correlation"] = correlation(
            values,
            target_cp,
        )

        stats["target_rank_correlation"] = rank_correlation(
            values,
            target_cp,
        )

        result["features"][name] = stats

        feature_target_correlations.append(
            (
                name,
                stats["target_correlation"],
            )
        )

    valid_correlations = [
        (name, corr)
        for name, corr in feature_target_correlations
        if corr is not None
    ]

    valid_correlations.sort(
        key=lambda item: abs(item[1]),
        reverse=True,
    )

    result["feature_target_correlations"] = {
        name: corr
        for name, corr in valid_correlations
    }

    # ------------------------------------------------------------------
    # Feature-feature correlations
    # ------------------------------------------------------------------

    correlation_matrix = np.corrcoef(
        feature_matrix,
        rowvar=False,
    )

    result["feature_correlations"] = {}

    for i, name_i in enumerate(feature_names):

        result["feature_correlations"][name_i] = {
            name_j: float(correlation_matrix[i, j])
            for j, name_j in enumerate(feature_names)
        }

    strong_pairs = []

    for i in range(len(feature_names)):

        for j in range(i + 1, len(feature_names)):

            corr = correlation_matrix[i, j]

            if abs(corr) >= 0.80:

                strong_pairs.append(
                    {
                        "feature_a": feature_names[i],
                        "feature_b": feature_names[j],
                        "correlation": float(corr),
                    }
                )

    strong_pairs.sort(
        key=lambda item: abs(
            item["correlation"]
        ),
        reverse=True,
    )

    result["strong_feature_correlations"] = strong_pairs

    return result


# ---------------------------------------------------------------------------
# Stage 2: Feature -> Target relationship
# ---------------------------------------------------------------------------


def analyze_feature_target_shape(
    feature_matrix: np.ndarray,
    target_cp: np.ndarray,
    feature_names: list[str],
) -> dict:
    """
    Analyze whether a feature has a linear or nonlinear relationship
    with the target.

    The feature is divided into quantile bins and the target mean/std
    is calculated for every bin.
    """

    result = {}

    for index, name in enumerate(feature_names):

        x = feature_matrix[:, index]

        finite_mask = np.isfinite(x) & np.isfinite(target_cp)

        x = x[finite_mask]
        y = target_cp[finite_mask]

        if x.size == 0 or np.std(x) == 0:
            result[name] = {}
            continue

        quantiles = np.linspace(
            0.0,
            1.0,
            FEATURE_BIN_COUNT + 1,
        )

        edges = np.quantile(
            x,
            quantiles,
        )

        edges = np.unique(edges)

        if len(edges) < 2:
            result[name] = {}
            continue

        bins = []

        for bin_index in range(len(edges) - 1):

            left = edges[bin_index]
            right = edges[bin_index + 1]

            if bin_index == len(edges) - 2:
                mask = (
                    (x >= left)
                    & (x <= right)
                )
            else:
                mask = (
                    (x >= left)
                    & (x < right)
                )

            if not np.any(mask):
                continue

            target_values = y[mask]

            bins.append(
                {
                    "bin": bin_index,
                    "feature_min": float(left),
                    "feature_max": float(right),
                    "count": int(mask.sum()),
                    "feature_mean": float(
                        np.mean(x[mask])
                    ),
                    "target_mean": float(
                        np.mean(target_values)
                    ),
                    "target_std": float(
                        np.std(target_values)
                    ),
                    "target_median": float(
                        np.median(target_values)
                    ),
                    "target_abs_mean": float(
                        np.mean(np.abs(target_values))
                    ),
                }
            )

        target_means = np.asarray(
            [
                item["target_mean"]
                for item in bins
            ],
            dtype=np.float64,
        )

        if target_means.size >= 2:

            target_range = float(
                np.max(target_means)
                - np.min(target_means)
            )

        else:
            target_range = 0.0

        result[name] = {
            "bin_count": len(bins),
            "bins": bins,
            "target_mean_range_across_bins": target_range,
            "pearson": correlation(x, y),
            "rank_correlation": rank_correlation(x, y),
        }

    return result


# ---------------------------------------------------------------------------
# Stage 2: Feature x depth
# ---------------------------------------------------------------------------


def analyze_feature_depth_interaction(
    feature_matrix: np.ndarray,
    target_cp: np.ndarray,
    source_depth: np.ndarray,
    feature_names: list[str],
) -> dict:
    """
    Measure feature-target correlation at different source depths.
    """

    result = {}

    for feature_index, feature_name in enumerate(feature_names):

        feature_values = feature_matrix[:, feature_index]

        buckets = []

        for depth_min, depth_max in DEPTH_BUCKETS:

            mask = source_depth >= depth_min

            if np.isfinite(depth_max):
                mask &= source_depth <= depth_max

            x = feature_values[mask]
            y = target_cp[mask]

            if x.size == 0:
                continue

            buckets.append(
                {
                    "depth_min": depth_min,
                    "depth_max": (
                        None
                        if not np.isfinite(depth_max)
                        else depth_max
                    ),
                    "count": int(x.size),
                    "feature_mean": float(
                        np.mean(x)
                    ),
                    "feature_std": float(
                        np.std(x)
                    ),
                    "target_mean": float(
                        np.mean(y)
                    ),
                    "target_std": float(
                        np.std(y)
                    ),
                    "correlation": correlation(
                        x,
                        y,
                    ),
                }
            )

        result[feature_name] = buckets

    return result


# ---------------------------------------------------------------------------
# Stage 2: Clamp analysis
# ---------------------------------------------------------------------------


def analyze_clamp_effect(
    feature_matrix: np.ndarray,
    target_cp: np.ndarray,
    feature_names: list[str],
) -> dict:
    """
    Compare feature correlations on:

        all samples
        non-clamped samples
        positive-clamped samples
        negative-clamped samples
    """

    masks = {
        "all": np.ones(
            target_cp.shape,
            dtype=bool,
        ),
        "non_clamped": (
            (target_cp > -TARGET_CLAMP)
            & (target_cp < TARGET_CLAMP)
        ),
        "positive_clamped": (
            target_cp >= TARGET_CLAMP
        ),
        "negative_clamped": (
            target_cp <= -TARGET_CLAMP
        ),
    }

    result = {}

    for feature_index, feature_name in enumerate(feature_names):

        x = feature_matrix[:, feature_index]

        feature_result = {}

        for mask_name, mask in masks.items():

            x_masked = x[mask]
            y_masked = target_cp[mask]

            feature_result[mask_name] = {
                "count": int(mask.sum()),
                "correlation": correlation(
                    x_masked,
                    y_masked,
                ),
            }

        result[feature_name] = feature_result

    return result


# ---------------------------------------------------------------------------
# Stage 2: Outlier analysis
# ---------------------------------------------------------------------------


def analyze_feature_outliers(
    feature_matrix: np.ndarray,
    feature_names: list[str],
) -> dict:
    """
    Identify extreme feature values using the 1st / 99th percentile.
    """

    result = {}

    for index, name in enumerate(feature_names):

        values = feature_matrix[:, index]

        p1, p99 = np.percentile(
            values,
            [1, 99],
        )

        low_mask = values < p1
        high_mask = values > p99

        result[name] = {
            "p1": float(p1),
            "p99": float(p99),
            "low_outlier_count": int(
                low_mask.sum()
            ),
            "high_outlier_count": int(
                high_mask.sum()
            ),
            "low_outlier_ratio": float(
                np.mean(low_mask)
            ),
            "high_outlier_ratio": float(
                np.mean(high_mask)
            ),
        }

    return result


# ---------------------------------------------------------------------------
# Stage 2: Linear baseline
# ---------------------------------------------------------------------------


def fit_linear_baseline(
    feature_matrix: np.ndarray,
    target_cp: np.ndarray,
    feature_names: list[str],
) -> dict:
    """
    Fit a simple standardized linear regression using NumPy.

    This is deliberately only a diagnostic baseline.
    It is NOT the training model.
    """

    finite_mask = (
        np.isfinite(target_cp)
        & np.all(
            np.isfinite(feature_matrix),
            axis=1,
        )
    )

    x = feature_matrix[finite_mask]
    y = target_cp[finite_mask]

    means = np.mean(x, axis=0)
    stds = np.std(x, axis=0)

    safe_stds = np.where(
        stds == 0,
        1.0,
        stds,
    )

    x_standardized = (
        x - means
    ) / safe_stds

    design = np.column_stack(
        [
            np.ones(len(x_standardized)),
            x_standardized,
        ]
    )

    coefficients, _, _, _ = np.linalg.lstsq(
        design,
        y,
        rcond=None,
    )

    prediction = design @ coefficients

    residual = y - prediction

    total_ss = np.sum(
        (y - np.mean(y)) ** 2
    )

    residual_ss = np.sum(
        residual ** 2
    )

    r_squared = (
        1.0 - residual_ss / total_ss
        if total_ss > 0
        else 0.0
    )

    coefficient_rows = []

    for index, name in enumerate(feature_names):

        coefficient_rows.append(
            {
                "feature": name,
                "standardized_coefficient": float(
                    coefficients[index + 1]
                ),
                "abs_coefficient": float(
                    abs(coefficients[index + 1])
                ),
            }
        )

    coefficient_rows.sort(
        key=lambda item: item["abs_coefficient"],
        reverse=True,
    )

    return {
        "intercept": float(
            coefficients[0]
        ),
        "r_squared": float(r_squared),
        "rmse": float(
            np.sqrt(
                np.mean(residual ** 2)
            )
        ),
        "mae": float(
            np.mean(np.abs(residual))
        ),
        "coefficients": coefficient_rows,
    }


# ---------------------------------------------------------------------------
# Stage 2: Residual information
# ---------------------------------------------------------------------------


def analyze_residual_correlations(
    feature_matrix: np.ndarray,
    target_cp: np.ndarray,
    feature_names: list[str],
) -> dict:
    """
    Fit the linear baseline and measure feature correlation with residuals.

    This helps identify features whose useful information is not captured
    by the simple global linear relationship.
    """

    finite_mask = (
        np.isfinite(target_cp)
        & np.all(
            np.isfinite(feature_matrix),
            axis=1,
        )
    )

    x = feature_matrix[finite_mask]
    y = target_cp[finite_mask]

    means = np.mean(x, axis=0)
    stds = np.std(x, axis=0)

    safe_stds = np.where(
        stds == 0,
        1.0,
        stds,
    )

    x_standardized = (
        x - means
    ) / safe_stds

    design = np.column_stack(
        [
            np.ones(len(x_standardized)),
            x_standardized,
        ]
    )

    coefficients, _, _, _ = np.linalg.lstsq(
        design,
        y,
        rcond=None,
    )

    prediction = design @ coefficients

    residual = y - prediction

    rows = []

    for index, name in enumerate(feature_names):

        corr = correlation(
            x[:, index],
            residual,
        )

        rows.append(
            {
                "feature": name,
                "residual_correlation": (
                    None
                    if corr is None
                    else float(corr)
                ),
                "abs_residual_correlation": (
                    None
                    if corr is None
                    else float(abs(corr))
                ),
            }
        )

    rows = [
        row
        for row in rows
        if row["residual_correlation"] is not None
    ]

    rows.sort(
        key=lambda row: row[
            "abs_residual_correlation"
        ],
        reverse=True,
    )

    return {
        "residual_mean": float(
            np.mean(residual)
        ),
        "residual_std": float(
            np.std(residual)
        ),
        "residual_mae": float(
            np.mean(np.abs(residual))
        ),
        "feature_correlations": rows,
    }


# ---------------------------------------------------------------------------
# Stage 2 master analysis
# ---------------------------------------------------------------------------


def analyze_stage2(
    target_cp: np.ndarray,
    source_depth: np.ndarray,
    feature_matrix: np.ndarray,
    feature_names: list[str],
) -> dict:

    print()
    print("Running Stage 2 analysis...")

    print("  - Feature/target shape")
    feature_target_shape = (
        analyze_feature_target_shape(
            feature_matrix,
            target_cp,
            feature_names,
        )
    )

    print("  - Feature/depth interaction")
    feature_depth = (
        analyze_feature_depth_interaction(
            feature_matrix,
            target_cp,
            source_depth,
            feature_names,
        )
    )

    print("  - Clamp effect")
    clamp_effect = analyze_clamp_effect(
        feature_matrix,
        target_cp,
        feature_names,
    )

    print("  - Feature outliers")
    outliers = analyze_feature_outliers(
        feature_matrix,
        feature_names,
    )

    print("  - Linear baseline")
    linear_baseline = fit_linear_baseline(
        feature_matrix,
        target_cp,
        feature_names,
    )

    print("  - Residual correlations")
    residual_analysis = analyze_residual_correlations(
        feature_matrix,
        target_cp,
        feature_names,
    )

    return {
        "feature_target_shape": feature_target_shape,
        "feature_depth_interaction": feature_depth,
        "clamp_effect": clamp_effect,
        "feature_outliers": outliers,
        "linear_baseline": linear_baseline,
        "residual_analysis": residual_analysis,
    }


# ---------------------------------------------------------------------------
# Stage 2 human-readable report
# ---------------------------------------------------------------------------


def print_stage2_report(
    stage2: dict,
) -> None:

    print()
    print("=" * 80)
    print("Stage 2 Analysis")
    print("=" * 80)

    # ------------------------------------------------------------------
    # Linear baseline
    # ------------------------------------------------------------------

    baseline = stage2["linear_baseline"]

    print()
    print("Linear Baseline")
    print("-" * 80)

    print(
        f"R²            : "
        f"{baseline['r_squared']:.6f}"
    )

    print(
        f"RMSE          : "
        f"{baseline['rmse']:.4f}"
    )

    print(
        f"MAE           : "
        f"{baseline['mae']:.4f}"
    )

    print()
    print("Standardized Coefficients")
    print("-" * 80)

    for rank, row in enumerate(
        baseline["coefficients"],
        start=1,
    ):

        print(
            f"{rank:>2}. "
            f"{row['feature']:<22}"
            f" coef={row['standardized_coefficient']:>10.4f}"
        )

    # ------------------------------------------------------------------
    # Residual correlations
    # ------------------------------------------------------------------

    residual = stage2["residual_analysis"]

    print()
    print("Residual Feature Correlations")
    print("-" * 80)

    print(
        f"Residual std : "
        f"{residual['residual_std']:.4f}"
    )

    print(
        f"Residual MAE : "
        f"{residual['residual_mae']:.4f}"
    )

    for rank, row in enumerate(
        residual["feature_correlations"],
        start=1,
    ):

        print(
            f"{rank:>2}. "
            f"{row['feature']:<22}"
            f" r={row['residual_correlation']:.6f}"
        )

    # ------------------------------------------------------------------
    # Feature shape summary
    # ------------------------------------------------------------------

    print()
    print("Feature / Target Nonlinear Shape")
    print("-" * 80)

    print(
        f"{'Feature':<22}"
        f"{'Pearson':>12}"
        f"{'Rank':>12}"
        f"{'Bin Target Range':>18}"
    )

    print("-" * 80)

    for name, analysis in (
        stage2["feature_target_shape"].items()
    ):

        if not analysis:
            continue

        pearson = analysis["pearson"]
        rank_corr = analysis["rank_correlation"]
        target_range = (
            analysis[
                "target_mean_range_across_bins"
            ]
        )

        print(
            f"{name:<22}"
            f"{pearson:>12.4f}"
            f"{rank_corr:>12.4f}"
            f"{target_range:>18.2f}"
        )

    # ------------------------------------------------------------------
    # Clamp effect
    # ------------------------------------------------------------------

    print()
    print("Clamp Effect")
    print("-" * 80)

    print(
        f"{'Feature':<22}"
        f"{'All':>12}"
        f"{'NonClamp':>12}"
        f"{'PosClamp':>12}"
        f"{'NegClamp':>12}"
    )

    print("-" * 80)

    for name, analysis in (
        stage2["clamp_effect"].items()
    ):

        def fmt(key: str) -> str:

            value = analysis[key]["correlation"]

            if value is None:
                return "N/A"

            return f"{value:.4f}"

        print(
            f"{name:<22}"
            f"{fmt('all'):>12}"
            f"{fmt('non_clamped'):>12}"
            f"{fmt('positive_clamped'):>12}"
            f"{fmt('negative_clamped'):>12}"
        )

    # ------------------------------------------------------------------
    # Outliers
    # ------------------------------------------------------------------

    print()
    print("Feature Outliers")
    print("-" * 80)

    print(
        f"{'Feature':<22}"
        f"{'P1':>12}"
        f"{'P99':>12}"
        f"{'Low %':>12}"
        f"{'High %':>12}"
    )

    print("-" * 80)

    for name, stats in (
        stage2["feature_outliers"].items()
    ):

        print(
            f"{name:<22}"
            f"{stats['p1']:>12.3f}"
            f"{stats['p99']:>12.3f}"
            f"{stats['low_outlier_ratio']:>12.4%}"
            f"{stats['high_outlier_ratio']:>12.4%}"
        )

    # ------------------------------------------------------------------
    # Depth interaction
    # ------------------------------------------------------------------

    print()
    print("Feature / Depth Correlation")
    print("-" * 80)

    for feature_name, buckets in (
        stage2[
            "feature_depth_interaction"
        ].items()
    ):

        print()
        print(feature_name)

        for bucket in buckets:

            depth_max = bucket["depth_max"]

            if depth_max is None:
                depth_label = (
                    f"{bucket['depth_min']}+"
                )
            else:
                depth_label = (
                    f"{bucket['depth_min']}-"
                    f"{int(depth_max)}"
                )

            corr = bucket["correlation"]

            if corr is None:
                corr_text = "N/A"
            else:
                corr_text = f"{corr:.4f}"

            print(
                f"  depth={depth_label:<8}"
                f" n={bucket['count']:>7,}"
                f" corr={corr_text:>8}"
                f" target_mean={bucket['target_mean']:>9.2f}"
            )


# ---------------------------------------------------------------------------
# Train / validation comparison
# ---------------------------------------------------------------------------


def compare_datasets(
    train: dict,
    valid: dict,
) -> dict:

    result = {
        "train_samples": train["sample_count"],
        "valid_samples": valid["sample_count"],
        "sample_ratio_valid": (
            valid["sample_count"]
            / (
                train["sample_count"]
                + valid["sample_count"]
            )
        ),
        "target_mean_difference": (
            valid["target_cp"]["mean"]
            - train["target_cp"]["mean"]
        ),
        "target_std_difference": (
            valid["target_cp"]["std"]
            - train["target_cp"]["std"]
        ),
        "depth_mean_difference": (
            valid["source_depth"]["mean"]
            - train["source_depth"]["mean"]
        ),
        "feature_mean_difference": {},
        "feature_std_difference": {},
    }

    for feature_name in train["feature_names"]:

        train_feature = train["features"][
            feature_name
        ]

        valid_feature = valid["features"][
            feature_name
        ]

        result["feature_mean_difference"][
            feature_name
        ] = (
            valid_feature["mean"]
            - train_feature["mean"]
        )

        result["feature_std_difference"][
            feature_name
        ] = (
            valid_feature["std"]
            - train_feature["std"]
        )

    return result


# ---------------------------------------------------------------------------
# Human-readable Stage 1 report
# ---------------------------------------------------------------------------


def print_report(
    train: dict,
    valid: dict,
    comparison: dict,
) -> None:

    print()
    print("=" * 80)
    print("Training Dataset Analysis")
    print("=" * 80)

    print()
    print("Dataset")
    print("-" * 80)

    print(
        f"Train samples : "
        f"{train['sample_count']:,}"
    )

    print(
        f"Valid samples : "
        f"{valid['sample_count']:,}"
    )

    print(
        f"Total samples : "
        f"{train['sample_count'] + valid['sample_count']:,}"
    )

    print(
        f"Feature count : "
        f"{train['feature_count']}"
    )

    print()
    print("Target CP")
    print("-" * 80)

    target = train["target_cp"]

    print(
        f"Mean          : {target['mean']:.4f}"
    )

    print(
        f"Std           : {target['std']:.4f}"
    )

    print(
        f"Min           : {target['min']:.1f}"
    )

    print(
        f"Median        : {target['p50']:.1f}"
    )

    print(
        f"Max           : {target['max']:.1f}"
    )

    print(
        f"Zero ratio    : "
        f"{target['zero_ratio']:.4%}"
    )

    print(
        f"Positive      : "
        f"{target['positive_ratio']:.4%}"
    )

    print(
        f"Negative      : "
        f"{target['negative_ratio']:.4%}"
    )

    print(
        f"Clamp <=-1000: "
        f"{target['clamp_negative_ratio']:.4%}"
    )

    print(
        f"Clamp >=1000 : "
        f"{target['clamp_positive_ratio']:.4%}"
    )

    print()
    print("Source Depth")
    print("-" * 80)

    depth = train["source_depth"]

    print(
        f"Mean          : {depth['mean']:.3f}"
    )

    print(
        f"Std           : {depth['std']:.3f}"
    )

    print(
        f"Min           : {depth['min']:.0f}"
    )

    print(
        f"Median        : {depth['p50']:.0f}"
    )

    print(
        f"Max           : {depth['max']:.0f}"
    )

    print()
    print("Features")
    print("-" * 80)

    print(
        f"{'Feature':<22}"
        f"{'Mean':>12}"
        f"{'Std':>12}"
        f"{'Min':>12}"
        f"{'Median':>12}"
        f"{'Max':>12}"
        f"{'Corr':>12}"
    )

    print("-" * 80)

    for name in train["feature_names"]:

        stats = train["features"][name]

        corr = stats["target_correlation"]

        corr_text = (
            f"{corr:.4f}"
            if corr is not None
            else "N/A"
        )

        print(
            f"{name:<22}"
            f"{stats['mean']:>12.4f}"
            f"{stats['std']:>12.4f}"
            f"{stats['min']:>12.4f}"
            f"{stats['p50']:>12.4f}"
            f"{stats['max']:>12.4f}"
            f"{corr_text:>12}"
        )

    print()
    print("Strong Feature Correlations |r| >= 0.80")
    print("-" * 80)

    pairs = train["strong_feature_correlations"]

    if not pairs:
        print("None")

    for pair in pairs:

        print(
            f"{pair['feature_a']:<22}"
            f" <-> "
            f"{pair['feature_b']:<22}"
            f" r={pair['correlation']:.4f}"
        )

    print()
    print("Feature / Target Correlation Ranking")
    print("-" * 80)

    for rank, (name, corr) in enumerate(
        train["feature_target_correlations"].items(),
        start=1,
    ):

        print(
            f"{rank:>2}. "
            f"{name:<22}"
            f" r={corr:.6f}"
        )

    print()
    print("Train / Validation Difference")
    print("-" * 80)

    print(
        f"Target mean diff : "
        f"{comparison['target_mean_difference']:.6f}"
    )

    print(
        f"Target std diff  : "
        f"{comparison['target_std_difference']:.6f}"
    )

    print(
        f"Depth mean diff  : "
        f"{comparison['depth_mean_difference']:.6f}"
    )

    print()
    print("Feature mean differences (valid - train)")
    print("-" * 80)

    for name, difference in (
        comparison["feature_mean_difference"].items()
    ):

        print(
            f"{name:<22}"
            f"{difference:>12.6f}"
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description=(
            "Statistically analyze the chess-ai-lab "
            "training/validation Parquet datasets."
        )
    )

    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/training/1m"),
        help=(
            "Directory containing train.parquet "
            "and valid.parquet."
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Optional JSON output path. "
            "Defaults to <data-dir>/analysis.json."
        ),
    )

    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:

    args = parse_args()

    train_path = (
        args.data_dir / "train.parquet"
    )

    valid_path = (
        args.data_dir / "valid.parquet"
    )

    if not train_path.exists():
        raise FileNotFoundError(
            f"Train dataset not found: {train_path}"
        )

    if not valid_path.exists():
        raise FileNotFoundError(
            f"Validation dataset not found: {valid_path}"
        )

    print()
    print("Analyzing training dataset...")
    train = analyze_dataset(train_path)

    print()
    print("Analyzing validation dataset...")
    valid = analyze_dataset(valid_path)

    comparison = compare_datasets(
        train,
        valid,
    )

    print_report(
        train,
        valid,
        comparison,
    )

    # ------------------------------------------------------------------
    # Stage 2
    #
    # Stage 2 is run on the complete 1M-position dataset.
    # This avoids introducing an artificial train/valid difference into
    # the exploratory statistics.
    # ------------------------------------------------------------------

    print()
    print("Loading complete dataset for Stage 2...")

    (
        _,
        train_target,
        train_depth,
        train_feature_names,
        train_features,
    ) = load_dataset(train_path)

    (
        _,
        valid_target,
        valid_depth,
        valid_feature_names,
        valid_features,
    ) = load_dataset(valid_path)

    if train_feature_names != valid_feature_names:
        raise ValueError(
            "Train/validation feature schemas differ."
        )

    all_target = np.concatenate(
        [
            train_target,
            valid_target,
        ]
    )

    all_depth = np.concatenate(
        [
            train_depth,
            valid_depth,
        ]
    )

    all_features = np.vstack(
        [
            train_features,
            valid_features,
        ]
    )

    stage2 = analyze_stage2(
        all_target,
        all_depth,
        all_features,
        train_feature_names,
    )

    print_stage2_report(
        stage2,
    )

    # ------------------------------------------------------------------
    # JSON
    # ------------------------------------------------------------------

    output_path = (
        args.output
        if args.output is not None
        else args.data_dir / "analysis.json"
    )

    report = {
        "stage": 2,
        "train": train,
        "valid": valid,
        "comparison": comparison,
        "stage2": stage2,
    }

    output_path.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print()
    print("=" * 80)
    print(
        f"Analysis JSON saved: {output_path}"
    )
    print("=" * 80)


if __name__ == "__main__":
    main()