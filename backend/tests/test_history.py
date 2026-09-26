"""
Unit Tests for ModelTestingHistory and Session Snapshot Inspection in ArgusML.
"""

import pytest
from backend.app.core.dsa.history import ModelTestingHistory, TestSessionRecord
from backend.app.core.orchestrator import ArgusSystem


def test_model_testing_history_recording():
    """Validates chronological recording, capacity eviction, and lookup in history."""
    history = ModelTestingHistory(capacity=5)
    assert len(history.get_history()) == 0

    # Record 3 events
    rec1 = history.record_session(
        model_id="model_a",
        model_name="Model Alpha",
        event_type="REGISTERED",
        summary="Registered Model Alpha",
        severity_level="HEALTHY",
        graph_snapshot={"nodes": [{"id": "model_a"}]},
    )
    assert rec1.session_id.startswith("sess_")
    assert len(history.get_history()) == 1

    rec2 = history.record_session(
        model_id="model_a",
        model_name="Model Alpha",
        event_type="DRIFT_DETECTED",
        summary="Critical drift in feature_x",
        accuracy=0.68,
        p99_latency_ms=85.0,
        culprit_feature="feature_x",
        severity_level="CRITICAL",
        diagnosis_output={"culprit": "feature_x"},
        graph_snapshot={"nodes": [{"id": "model_a"}, {"id": "feature_x"}]},
    )

    all_history = history.get_history()
    assert len(all_history) == 2
    # Most recent first
    assert all_history[0]["session_id"] == rec2.session_id
    assert all_history[0]["culprit_feature"] == "feature_x"
    assert all_history[0]["severity_level"] == "CRITICAL"

    # Test single session lookup
    looked_up = history.get_session(rec2.session_id)
    assert looked_up is not None
    assert looked_up["accuracy"] == 0.68
    assert looked_up["graph_snapshot"]["nodes"][1]["id"] == "feature_x"


def test_history_capacity_overflow():
    """Tests circular eviction when capacity limit is reached."""
    history = ModelTestingHistory(capacity=3)
    for i in range(5):
        history.record_session(
            model_id=f"model_{i}",
            model_name=f"Model {i}",
            event_type="REGISTERED",
            summary=f"Run {i}",
        )

    records = history.get_history()
    assert len(records) == 3
    # Latest should be model_4, model_3, model_2
    assert records[0]["model_id"] == "model_4"
    assert records[2]["model_id"] == "model_2"


def test_orchestrator_history_lifecycle():
    """Tests end-to-end recording of sessions in ArgusSystem during model lifecycle."""
    system = ArgusSystem(window_size=50)

    # 1. Load samples
    system.load_sample_models()
    summary = system.get_dashboard_summary()
    assert "session_history" in summary
    assert len(summary["session_history"]) >= 1
    latest = summary["session_history"][0]
    assert latest["event_type"] in ["DEMO_LOADED", "SWITCHED"]

    # 2. Retrain model
    retrain_res = system.retrain_active_model()
    assert retrain_res["status"] == "SUCCESS"

    summary2 = system.get_dashboard_summary()
    assert summary2["session_history"][0]["event_type"] == "RETRAINED"
    assert "retraining_report" in summary2["session_history"][0]["diagnosis_output"]
