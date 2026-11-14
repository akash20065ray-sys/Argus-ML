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
    assert retrain_res["gate_status"] == "PASS"
    assert retrain_res["model_id"] == "customer_churn_v1"
    assert retrain_res["new_version"] == "v1.1.0"
    assert retrain_res["alerts_resolved_count"] > 0
    assert "validation_report" in retrain_res
    assert len(retrain_res["validation_report"]["checks"]) == 4

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
    assert "Downstream Blast Radius" in report
    assert "Closed-Loop Remediation & Validation Gate" in report
    assert "Algorithmic Complexity & Telemetry Architecture" in report


def test_retrained_dataset_csv_export_with_provenance():
    """
    Validates that retraining dynamically fuses baseline and streaming telemetry,
    and exports a verifiable CSV with full row provenance.
    """
    import csv
    import io

    system = ArgusSystem()
    system.load_sample_models()
    system.switch_active_model("customer_churn_v1")

    model_before = system.models_map["customer_churn_v1"]
    base_rows = len(model_before.target_values)

    # Initial CSV export before retraining
    csv_raw_before = model_before.export_csv(include_provenance=True)
    reader_before = list(csv.DictReader(io.StringIO(csv_raw_before)))
    assert len(reader_before) == base_rows
    assert "_provenance" in reader_before[0]
    assert all(r["_provenance"] == "baseline" for r in reader_before)

    # Inject drift and collect streaming events
    system.simulator.set_feature_drift("monthly_charges", 3.0)
    for _ in range(40):
        ev = system.simulator.generate_single_event()
        system.sliding_window.add_record(ev)

    system._evaluate_telemetry()

    # Retrain
    retrain_res = system.retrain_active_model()
    assert retrain_res["status"] == "SUCCESS"
    assert retrain_res["gate_status"] == "PASS"
    assert retrain_res["baseline_samples_count"] == base_rows
    assert retrain_res["telemetry_samples_count"] > 0
    assert "dataset_export_url" in retrain_res

    # Model after retraining
    model_after = system.models_map["customer_churn_v1"]
    csv_raw_after = model_after.export_csv(include_provenance=True)
    reader_after = list(csv.DictReader(io.StringIO(csv_raw_after)))

    assert len(reader_after) == base_rows + retrain_res["telemetry_samples_count"]
    baseline_tags = sum(1 for r in reader_after if r["_provenance"] == "baseline")
    stream_tags = sum(1 for r in reader_after if r["_provenance"] == "live_sliding_window")

    assert baseline_tags == base_rows
    assert stream_tags == retrain_res["telemetry_samples_count"]

