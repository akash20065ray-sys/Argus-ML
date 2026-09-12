import pytest
from backend.app.core.orchestrator import ArgusSystem


def test_automated_model_retraining_flow():
    system = ArgusSystem()
    system.load_sample_models()
    system.switch_active_model("customer_churn_v1")

    # Verify initial version
    meta_before = system.registry.get_model("customer_churn_v1")
    assert meta_before.version in ["1.0.0", "v1.0.0"]

    # Inject feature drift to simulate degradation
    system.simulator.set_feature_drift("monthly_charges", 3.5)

    # Simulate batch of telemetry through pipeline
    for _ in range(30):
        event = system.simulator.generate_single_event()
        system.queue.enqueue(event)

    # Process stream batch
    batch = system.queue.dequeue_batch(30)
    for ev in batch:
        system.sliding_window.add_record(ev)

    # Trigger evaluation
    system._evaluate_telemetry()

    # Verify alert was created in Max-Heap
    alerts = system.alert_heap.get_top_k(5)
    assert len(alerts) > 0

    # Retrain active model via 1-Click trigger
    retrain_res = system.retrain_active_model()
    assert retrain_res["status"] == "SUCCESS"
    assert retrain_res["model_id"] == "customer_churn_v1"
    assert retrain_res["new_version"] == "v1.1.0"
    assert retrain_res["alerts_resolved_count"] > 0

    # Verify registry version updated
    meta_after = system.registry.get_model("customer_churn_v1")
    assert meta_after.version == "v1.1.0"

    # Verify alerts cleared
    assert len(system.alert_heap.get_top_k(5)) == 0


def test_incident_post_mortem_report_generation():
    system = ArgusSystem()
    system.load_sample_models()
    system.switch_active_model("fraud_detector_v1")

    # Inject drift and evaluate
    system.simulator.set_feature_drift("transaction_amount", 4.0)
    for _ in range(30):
        event = system.simulator.generate_single_event()
        system.sliding_window.add_record(event)
    system._evaluate_telemetry()

    # Generate Markdown Incident Post-Mortem Report
    report = system.generate_incident_report(alert_id="INC-TEST-001")

    assert "# 🚨 ArgusML Incident Post-Mortem Report" in report
    assert "INC-TEST-001" in report
    assert "fraud_detector_v1" in report
    assert "transaction_amount" in report
    assert "Downstream Blast Radius" in report
    assert "Remediation & Action Plan" in report
