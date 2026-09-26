"""
Unit Tests for Statistical Drift and Root-Cause Analysis (RCA).
"""

import numpy as np
import pytest
from backend.app.core.drift.detector import DriftEngine, calculate_psi, run_ks_test
from backend.app.core.dsa.graph import DependencyGraph
from backend.app.core.dsa.heap import AlertMaxHeap
from backend.app.core.rca.engine import RootCauseAnalysisEngine


def test_ks_test_and_psi_detection():
    """Validates that identical distributions pass and shifted distributions fail."""
    np.random.seed(42)
    baseline = np.random.normal(loc=100.0, scale=15.0, size=500).tolist()
    similar = np.random.normal(loc=100.2, scale=14.9, size=500).tolist()
    drifted = np.random.normal(loc=160.0, scale=35.0, size=500).tolist()

    # Similar should have high p-value and low PSI
    ks_stat_sim, p_val_sim, is_drift_sim = run_ks_test(baseline, similar)
    psi_sim = calculate_psi(np.array(baseline), np.array(similar))
    assert not is_drift_sim
    assert psi_sim < 0.10

    # Drifted should trigger KS drift and high PSI
    ks_stat_drift, p_val_drift, is_drift_true = run_ks_test(baseline, drifted)
    psi_drift = calculate_psi(np.array(baseline), np.array(drifted))
    assert is_drift_true
    assert p_val_drift < 0.001
    assert psi_drift > 0.25


def test_rca_engine_pinpoints_culprit_feature():
    """Validates that RCA engine identifies the exact drifting feature and blast radius."""
    graph = DependencyGraph()
    alert_heap = AlertMaxHeap()

    # Build graph
    graph.add_node("src_payments", "PIPELINE", "Payments ETL")
    graph.add_node("feat_amount", "FEATURE", "Amount")
    graph.add_node("feat_velocity", "FEATURE", "Velocity")
    graph.add_node("model_fraud", "MODEL", "Fraud Model")
    graph.add_node("srv_checkout", "SERVICE", "Checkout Service")

    graph.add_edge("src_payments", "feat_amount")
    graph.add_edge("src_payments", "feat_velocity")
    graph.add_edge("feat_amount", "model_fraud")
    graph.add_edge("feat_velocity", "model_fraud")
    graph.add_edge("model_fraud", "srv_checkout")

    rca = RootCauseAnalysisEngine(graph, alert_heap)

    # Simulate drift test results where feat_amount drifted significantly
    mock_drift = {
        "top_drifting_features": [
            {
                "feature": "amount",
                "ks_statistic": 0.45,
                "psi": 0.38,
                "mean_shift_pct": 280.0,
                "severity": "CRITICAL",
                "drift_detected": True,
            }
        ]
    }

    perf_metrics = {"accuracy": 0.72, "p99": 140.0}
    diagnosis = rca.diagnose_model(
        model_id="model_fraud",
        current_metrics=perf_metrics,
        sla_min_accuracy=0.88,
        drift_results=mock_drift,
    )

    assert diagnosis is not None
    assert diagnosis["root_cause"]["culprit_feature"] == "amount"
    assert diagnosis["root_cause"]["confidence_score"] > 50.0
    assert diagnosis["severity_level"] == "CRITICAL"
    assert "Checkout Service (SERVICE)" in diagnosis["blast_radius"]

    # Verify that a critical alert was pushed to the Max-Heap
    top_alert = alert_heap.peek()
    assert top_alert is not None
    assert top_alert.severity_level == "CRITICAL"
    assert top_alert.model_id == "model_fraud"


def test_multi_candidate_rcs_confidence_ranking():
    """Validates that RCA engine ranks multiple candidate features by RCS confidence score."""
    graph = DependencyGraph()
    alert_heap = AlertMaxHeap()

    graph.add_node("feat_amt", "FEATURE", "Amount")
    graph.add_node("feat_ip", "FEATURE", "IP Ratio")
    graph.add_node("feat_age", "FEATURE", "Age")
    graph.add_node("model_1", "MODEL", "Model 1")

    graph.add_edge("feat_amt", "model_1")
    graph.add_edge("feat_ip", "model_1")
    graph.add_edge("feat_age", "model_1")

    rca = RootCauseAnalysisEngine(graph, alert_heap)

    mock_drift = {
        "evaluated_features": {
            "amt": {
                "feature": "amt",
                "ks_statistic": 0.52,
                "psi": 0.44,
                "mean_shift_pct": 310.0,
                "drift_detected": True,
            },
            "ip": {
                "feature": "ip",
                "ks_statistic": 0.22,
                "psi": 0.12,
                "mean_shift_pct": 40.0,
                "drift_detected": True,
            },
            "age": {
                "feature": "age",
                "ks_statistic": 0.04,
                "psi": 0.02,
                "mean_shift_pct": 2.0,
                "drift_detected": False,
            },
        }
    }

    diagnosis = rca.diagnose_model(
        model_id="model_1",
        current_metrics={"accuracy": 0.70, "p99": 50.0},
        sla_min_accuracy=0.85,
        drift_results=mock_drift,
    )

    assert diagnosis is not None
    candidates = diagnosis["candidate_root_causes"]
    assert len(candidates) == 3

    # Ensure ranked in descending order of RCS
    assert candidates[0]["feature"] == "amt"
    assert candidates[1]["feature"] == "ip"
    assert candidates[2]["feature"] == "age"
    assert candidates[0]["confidence_score"] > candidates[1]["confidence_score"] > candidates[2]["confidence_score"]
