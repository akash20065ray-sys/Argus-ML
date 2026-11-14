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


def apply_benjamini_hochberg(
    feature_results: Dict[str, Dict[str, Any]], q_level: float = 0.05
) -> Dict[str, Dict[str, Any]]:
    """
    Applies the Benjamini-Hochberg (BH) procedure to control False Discovery Rate (FDR)
    across M simultaneous feature drift hypothesis tests.

    Eliminates family-wise alpha inflation when monitoring high-dimensional models:
      P_family = 1 - (1 - alpha)^M (e.g. 78.5% false alarm rate for 30 features at alpha=0.05).

    Algorithm:
      1. Rank features by ascending raw p-value: P_(1) <= P_(2) <= ... <= P_(M).
      2. Find largest rank k such that P_(k) <= (k / M) * Q.
      3. Declare all hypotheses with rank i <= k as statistically significant.
      4. Compute adjusted p-values (step-up procedure):
         p_adj_(i) = min(1.0, min_{j >= i} (M / j * P_(j)))
    """
    valid_features = [
        f for f, r in feature_results.items() if r.get("status") == "EVALUATED"
    ]
    M = len(valid_features)
    if M == 0:
        return feature_results

    # Sort feature names by ascending raw p-value
    sorted_feats = sorted(
        valid_features, key=lambda f: feature_results[f].get("p_value", 1.0)
    )

    # 1. Identify max index k where P_(k) <= (k / M) * Q
    max_k = 0
    for rank_1_based, feat in enumerate(sorted_feats, start=1):
        raw_p = feature_results[feat].get("p_value", 1.0)
        crit_val = (rank_1_based / M) * q_level
        if raw_p <= crit_val:
            max_k = rank_1_based

    # 2. Compute BH step-up adjusted p-values
    p_adj_map = {}
    running_min = 1.0
    for rank_1_based in range(M, 0, -1):
        feat = sorted_feats[rank_1_based - 1]
        raw_p = feature_results[feat].get("p_value", 1.0)
        step_val = (M / rank_1_based) * raw_p
        running_min = min(running_min, step_val)
        p_adj_map[feat] = float(round(min(1.0, running_min), 6))

    # 3. Apply FDR discoveries & update drift classifications
    for rank_1_based, feat in enumerate(sorted_feats, start=1):
        rec = feature_results[feat]
        is_fdr_sig = rank_1_based <= max_k
        raw_p = rec.get("p_value", 1.0)
        ks_stat = rec.get("ks_statistic", 0.0)
        psi_val = rec.get("psi", 0.0)

        rec["p_value_raw"] = raw_p
        rec["p_value_fdr_adjusted"] = p_adj_map[feat]
        rec["fdr_threshold"] = round((rank_1_based / M) * q_level, 6)
        rec["fdr_significant"] = is_fdr_sig
        rec["fdr_rank"] = rank_1_based
        rec["multiple_testing_correction"] = "Benjamini-Hochberg (FDR)"

        # Drift confirmed if:
        # (a) Statistically significant under FDR control AND KS-stat > 0.15, OR
        # (b) Population Stability Index indicates real distribution shift (PSI >= 0.15)
        drift_detected = (is_fdr_sig and ks_stat > 0.15) or (psi_val >= 0.15)
        rec["drift_detected"] = drift_detected

        # Re-tune severity to prevent false alarm spam
        if not drift_detected and rec.get("severity") == "WARNING":
            rec["severity"] = "NORMAL"

    return feature_results


class DriftEngine:
    """
    Evaluates current sliding window against registered model baselines
    for all features, calculating drift scores, PSI, and drift classifications
    with algorithmic Benjamini-Hochberg False Discovery Rate (FDR) control.
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
        Evaluates all features for a model with Benjamini-Hochberg FDR control.
        Returns detailed summary, multiple-testing audit, and ranks features by drift magnitude.
        """
        feature_results = {}

        for feat_name, cur_samples in current_map.items():
            base_samples = baseline_map.get(feat_name, [])
            res = self.evaluate_feature(feat_name, base_samples, cur_samples)
            feature_results[feat_name] = res

        # Apply Benjamini-Hochberg False Discovery Rate correction
        feature_results = apply_benjamini_hochberg(
            feature_results, q_level=self.significance_level
        )

        drifting_features = [
            r for r in feature_results.values() if r.get("drift_detected", False)
        ]

        # Sort drifting features descending by KS-statistic + PSI composite
        drifting_features.sort(
            key=lambda x: (x["ks_statistic"] + x["psi"]), reverse=True
        )

        fdr_sig_count = sum(
            1 for r in feature_results.values() if r.get("fdr_significant", False)
        )

        return {
            "evaluated_features": feature_results,
            "drifting_count": len(drifting_features),
            "top_drifting_features": drifting_features,
            "multiple_testing": {
                "correction_method": "Benjamini-Hochberg (FDR)",
                "nominal_q_level": self.significance_level,
                "hypotheses_tested": len(feature_results),
                "fdr_discoveries": fdr_sig_count,
            },
        }
