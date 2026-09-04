"""
Statistical Drift Detection Engine.

Implements:
1. Two-Sample Kolmogorov-Smirnov (KS) Test for continuous numerical distribution drift.
2. Population Stability Index (PSI) for binned population shift.
3. Quantile shift analysis (Mean, Median, Variance delta).
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
from scipy import stats


def calculate_psi(
    expected: np.ndarray, actual: np.ndarray, num_bins: int = 10
) -> float:
    """
    Computes Population Stability Index (PSI) between baseline (expected)
    and production window (actual).

    PSI Thresholds:
      PSI < 0.10 -> No shift (Green)
      0.10 <= PSI < 0.25 -> Moderate shift (Amber)
      PSI >= 0.25 -> Significant drift (Red)
    """
    if len(expected) < 10 or len(actual) < 10:
        return 0.0

    # Determine bin edges from reference/expected dataset
    percentiles = np.linspace(0, 100, num_bins + 1)
    bin_edges = np.percentile(expected, percentiles)
    # Add tiny epsilon to avoid bin edge collision
    bin_edges[0] -= 1e-5
    bin_edges[-1] += 1e-5
    bin_edges = np.unique(bin_edges)

    if len(bin_edges) < 2:
        return 0.0

    # Calculate frequencies in each bin
    expected_counts, _ = np.histogram(expected, bins=bin_edges)
    actual_counts, _ = np.histogram(actual, bins=bin_edges)

    # Convert to proportions with smoothing to avoid log(0) or division by zero
    expected_pct = (expected_counts + 1e-4) / (len(expected) + 1e-4 * len(expected_counts))
    actual_pct = (actual_counts + 1e-4) / (len(actual) + 1e-4 * len(actual_counts))

    # PSI calculation
    psi_value = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
    return float(round(max(0.0, psi_value), 4))


def run_ks_test(
    baseline_samples: List[float], current_samples: List[float]
) -> Tuple[float, float, bool]:
    """
    Performs 2-Sample Kolmogorov-Smirnov test.
    Returns: (ks_statistic, p_value, is_drift_detected)
    """
    if len(baseline_samples) < 20 or len(current_samples) < 20:
        return 0.0, 1.0, False

    b_arr = np.array(baseline_samples, dtype=float)
    c_arr = np.array(current_samples, dtype=float)

    # Clean NaNs or Infs
    b_arr = b_arr[~np.isnan(b_arr)]
    c_arr = c_arr[~np.isnan(c_arr)]

    if len(b_arr) < 20 or len(c_arr) < 20:
        return 0.0, 1.0, False

    ks_stat, p_val = stats.ks_2samp(b_arr, c_arr)
    is_drift = bool(p_val < 0.05 and ks_stat > 0.15)

    return float(round(ks_stat, 4)), float(round(p_val, 6)), is_drift


class DriftEngine:
    """
    Evaluates current sliding window against registered model baselines
    for all features, calculating drift scores, PSI, and drift classifications.
    """

    def __init__(self, significance_level: float = 0.05):
        self.significance_level = significance_level

    def evaluate_feature(
        self,
        feature_name: str,
        baseline_samples: List[float],
        current_samples: List[float],
    ) -> Dict[str, Any]:
        """
        Runs comprehensive statistical tests comparing baseline vs current window.
        """
        if not baseline_samples or not current_samples:
            return {
                "feature": feature_name,
                "status": "INSUFFICIENT_DATA",
                "ks_statistic": 0.0,
                "p_value": 1.0,
                "psi": 0.0,
                "drift_detected": False,
                "severity": "NORMAL",
                "current_mean": 0.0,
                "baseline_mean": 0.0,
                "mean_shift_pct": 0.0,
            }

        b_arr = np.array(baseline_samples)
        c_arr = np.array(current_samples)

        ks_stat, p_val, is_ks_drift = run_ks_test(baseline_samples, current_samples)
        psi_val = calculate_psi(b_arr, c_arr)

        b_mean = float(np.mean(b_arr))
        c_mean = float(np.mean(c_arr))
        shift_pct = (
            ((c_mean - b_mean) / abs(b_mean)) * 100 if abs(b_mean) > 1e-6 else 0.0
        )

        # Composite severity calculation
        severity = "NORMAL"
        if psi_val >= 0.25 or (p_val < 0.001 and ks_stat > 0.35):
            severity = "CRITICAL"
        elif psi_val >= 0.10 or (p_val < 0.05 and ks_stat > 0.20):
            severity = "WARNING"

        drift_detected = is_ks_drift or (psi_val >= 0.15)

        return {
            "feature": feature_name,
            "status": "EVALUATED",
            "ks_statistic": ks_stat,
            "p_value": p_val,
            "psi": psi_val,
            "drift_detected": drift_detected,
            "severity": severity,
            "current_mean": round(c_mean, 2),
            "baseline_mean": round(b_mean, 2),
            "mean_shift_pct": round(shift_pct, 2),
            "sample_size": len(current_samples),
        }

    def evaluate_all(
        self,
        baseline_map: Dict[str, List[float]],
        current_map: Dict[str, List[float]],
    ) -> Dict[str, Any]:
        """
        Evaluates all features for a model.
        Returns detailed summary and ranks features by drift magnitude.
        """
        feature_results = {}
        drifting_features = []

        for feat_name, cur_samples in current_map.items():
            base_samples = baseline_map.get(feat_name, [])
            res = self.evaluate_feature(feat_name, base_samples, cur_samples)
            feature_results[feat_name] = res
            if res["drift_detected"]:
                drifting_features.append(res)

        # Sort drifting features descending by KS-statistic + PSI composite
        drifting_features.sort(
            key=lambda x: (x["ks_statistic"] + x["psi"]), reverse=True
        )

        return {
            "evaluated_features": feature_results,
            "drifting_count": len(drifting_features),
            "top_drifting_features": drifting_features,
        }
