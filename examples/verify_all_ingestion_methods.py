"""
ArgusML Ingestion Verification Script:
Tests all 5 model ingestion and registration methods against the running platform.
"""

import io
import time
import requests
import numpy as np
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"


def print_step(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_method_1_demo_showcase():
    print_step("METHOD 1: Load 1-Click Demo Showcase Templates")
    res = requests.post(f"{BASE_URL}/api/models/load-samples")
    print("Status Code:", res.status_code)
    data = res.json()
    print("Response:", data)
    
    # Query dashboard
    dash = requests.get(f"{BASE_URL}/api/dashboard").json()
    print(f"Active Model: {dash['active_model']['name']} ({dash['active_model']['model_id']})")
    print(f"Available Models: {[m['model_id'] for m in dash['available_models']]}")
    assert dash['active_model'] is not None
    print("[PASS] Method 1 Successful!")


def test_method_2_json_rest_api():
    print_step("METHOD 2: Programmatic REST API Registration (JSON Payload)")
    
    np.random.seed(101)
    n = 300
    income = np.random.normal(55000, 12000, size=n).tolist()
    credit_score = np.random.normal(700, 50, size=n).tolist()
    loan_amt = np.random.normal(15000, 4000, size=n).tolist()
    labels = [1 if (cs < 650 or inc < 35000) else 0 for cs, inc in zip(credit_score, income)]

    payload = {
        "model_id": "auto_loan_risk_v2",
        "name": "Auto Loan Underwriting Classifier",
        "model_type": "CLASSIFICATION",
        "target_name": "defaulted",
        "target_values": labels,
        "data": {
            "applicant_income": income,
            "credit_score": credit_score,
            "loan_amount": loan_amt,
        },
        "downstream_services": ["Dealer Financing API", "Credit Bureau Underwriter"],
        "upstream_pipelines": ["Experian Credit Stream", "Applicant Portal ETL"],
        "sla_min_accuracy": 0.85,
        "sla_max_p99_latency_ms": 150.0,
    }

    res = requests.post(f"{BASE_URL}/api/models/register", json=payload)
    print("Status Code:", res.status_code)
    data = res.json()
    print(f"Registered Model: {data['model']['model_id']} | Features Inferred: {data['model']['features']}")
    
    dash = requests.get(f"{BASE_URL}/api/dashboard").json()
    print(f"Active Model Switched To: {dash['active_model']['model_id']}")
    assert dash['active_model']['model_id'] == "auto_loan_risk_v2"
    print("[PASS] Method 2 Successful!")


def test_method_3_live_prediction_ingestion():
    print_step("METHOD 3: Live Prediction Ingestion Stream (/api/ingest)")
    
    print("Streaming 20 live inference transactions into Circular FIFO EventQueue...")
    for i in range(20):
        event_payload = {
            "model_id": "auto_loan_risk_v2",
            "features": {
                "applicant_income": float(round(np.random.normal(55000, 12000), 2)),
                "credit_score": float(round(np.random.normal(700, 50), 1)),
                "loan_amount": float(round(np.random.normal(15000, 4000), 2)),
            },
            "prediction": 0,
            "confidence": 0.96,
            "ground_truth": 0,
            "latency_ms": float(round(np.random.normal(42, 4), 2)),
        }
        res = requests.post(f"{BASE_URL}/api/ingest", json=event_payload)
        assert res.status_code == 200
        time.sleep(0.02)
    
    dash = requests.get(f"{BASE_URL}/api/dashboard").json()
    print(f"Queue Telemetry -> Processed: {dash['queue_stats']['total_dequeued']} | Current Size: {dash['queue_stats']['current_size']}")
    print(f"Rolling Accuracy: {dash['performance'].get('accuracy', 1.0) * 100:.1f}%")
    print("[PASS] Method 3 Successful!")


def test_method_4_csv_file_upload():
    print_step("METHOD 4: Browser Multipart CSV File Upload (/api/models/upload-csv)")
    
    # Create an in-memory CSV dataset
    n = 400
    df = pd.DataFrame({
        "temperature_c": np.random.normal(24.0, 3.5, size=n).round(2),
        "vibration_hz": np.random.normal(120.0, 15.0, size=n).round(2),
        "pressure_psi": np.random.normal(45.0, 6.0, size=n).round(2),
        "operating_hours": np.random.uniform(100, 5000, size=n).round(1),
        "failure_risk": (np.random.normal(0, 1, size=n) > 1.2).astype(int),
    })

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    
    files = {
        "file": ("turbine_sensor_data.csv", io.BytesIO(csv_bytes), "text/csv"),
    }
    form_data = {
        "model_id": "wind_turbine_monitor_v1",
        "name": "Industrial Turbine Failure Predictor",
        "model_type": "CLASSIFICATION",
        "target_column": "failure_risk",
        "downstream_services_str": "Factory SCADA Alert Hub, Maintenance Dispatch API",
        "upstream_pipelines_str": "IoT Sensor MQTT Gateway, Modbus Ingestion ETL",
    }

    res = requests.post(f"{BASE_URL}/api/models/upload-csv", files=files, data=form_data)
    print("Status Code:", res.status_code)
    data = res.json()
    print("Upload Result:", data)
    
    dash = requests.get(f"{BASE_URL}/api/dashboard").json()
    print(f"Active Model Switched To: {dash['active_model']['model_id']}")
    print(f"Topology Nodes Built: {len(dash['graph']['nodes'])}")
    assert dash['active_model']['model_id'] == "wind_turbine_monitor_v1"
    print("[PASS] Method 4 Successful!")


def test_method_5_standby_unload():
    print_step("METHOD 5: Unload & Return to Clean Standby Mode (/api/models/unload)")
    res = requests.post(f"{BASE_URL}/api/models/unload")
    print("Unload Status:", res.json())
    
    dash = requests.get(f"{BASE_URL}/api/dashboard").json()
    print("Active Model in Standby:", dash['active_model'])
    print("Graph Nodes in Standby:", len(dash['graph']['nodes']))
    assert dash['active_model'] is None
    assert len(dash['graph']['nodes']) == 0
    print("[PASS] Method 5 Standby & Unload Verified!")


def main():
    print("\n" + "#" * 70)
    print("  ARGUSML UNIVERSAL INGESTION TEST SUITE")
    print("#" * 70)
    
    # 1. Health check
    h = requests.get(f"{BASE_URL}/api/health").json()
    print("Server Health Check:", h)
    
    # Run tests
    test_method_1_demo_showcase()
    test_method_2_json_rest_api()
    test_method_3_live_prediction_ingestion()
    test_method_4_csv_file_upload()
    test_method_5_standby_unload()
    
    print("\n" + "#" * 70)
    print("  ALL 5 INGESTION METHODS TESTED & VERIFIED WITH 100% SUCCESS!")
    print("#" * 70 + "\n")


if __name__ == "__main__":
    main()
