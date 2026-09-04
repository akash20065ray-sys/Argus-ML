"""
ArgusML Client Example: How to connect and test ANY of your own ML models.

This script demonstrates:
1. Training your own custom ML model (e.g. Loan Default Predictor or any custom model).
2. Registering your model and baseline training distribution with ArgusML.
3. Streaming live inference events to ArgusML.
4. Injecting real data drift to watch ArgusML catch it in real time!
"""

import time
import numpy as np
import requests
from sklearn.ensemble import RandomForestClassifier

ARGUS_URL = "http://127.0.0.1:8000"


def main():
    print("=" * 60)
    print("Step 1: Training YOUR OWN Custom ML Model (Loan Default Risk)")
    print("=" * 60)

    np.random.seed(42)
    n = 2000

    # 1. Your custom training dataset
    applicant_income = np.random.lognormal(mean=10.5, sigma=0.5, size=n)  # ~$36,000 avg
    credit_score = np.random.normal(loc=680.0, scale=60.0, size=n)
    credit_score = np.clip(credit_score, 300.0, 850.0)
    loan_amount = np.random.lognormal(mean=9.8, sigma=0.6, size=n)        # ~$18,000 avg
    debt_to_income = (loan_amount / applicant_income) * 100.0

    # Target: default risk (1 = default, 0 = paid)
    risk = (
        (credit_score < 580).astype(float) * 0.45
        + (debt_to_income > 40.0).astype(float) * 0.35
        + (applicant_income < 25000).astype(float) * 0.25
        + np.random.normal(0, 0.1, size=n)
    )
    labels = (risk > 0.42).astype(int)

    # Train your model
    X_train = np.column_stack([applicant_income, credit_score, loan_amount, debt_to_income])
    model = RandomForestClassifier(n_estimators=30, max_depth=5, random_state=42)
    model.fit(X_train, labels)
    train_acc = model.score(X_train, labels)
    print(f"Model trained successfully! Baseline Accuracy: {train_acc * 100:.1f}%\n")

    # 2. Register YOUR model with ArgusML
    print("=" * 60)
    print("Step 2: Registering Model & Baselines with ArgusML Platform")
    print("=" * 60)

    register_payload = {
        "model_id": "loan_default_v1",
        "name": "Consumer Loan Default Predictor",
        "model_type": "CLASSIFICATION",
        "target_name": "is_default",
        "target_values": labels.tolist(),
        "data": {
            "applicant_income": applicant_income.tolist(),
            "credit_score": credit_score.tolist(),
            "loan_amount": loan_amount.tolist(),
            "debt_to_income": debt_to_income.tolist(),
        },
        "downstream_services": [
            "Online Loan Origination API",
            "Credit Card Auto-Approval Service",
            "Underwriting Executive Dashboard",
        ],
        "upstream_pipelines": [
            "Equifax Bureau Ingestion Stream",
            "Bank Core Ledger ETL",
        ],
        "sla_min_accuracy": 0.85,
        "sla_max_p99_latency_ms": 180.0,
    }

    try:
        res = requests.post(f"{ARGUS_URL}/api/models/register", json=register_payload)
        print("Registration Response:", res.json()["status"])
    except Exception as e:
        print(f"Failed to connect to ArgusML at {ARGUS_URL}. Is the server running? Error: {e}")
        return

    # 3. Stream Normal Inferences
    print("\n" + "=" * 60)
    print("Step 3: Streaming Normal Inferences into ArgusML Ingestion Queue")
    print("=" * 60)

    feature_names = ["applicant_income", "credit_score", "loan_amount", "debt_to_income"]

    for i in range(30):
        # Generate new live customer
        inc = float(np.random.lognormal(mean=10.5, sigma=0.5))
        cs = float(np.clip(np.random.normal(loc=680.0, scale=60.0), 300, 850))
        amt = float(np.random.lognormal(mean=9.8, sigma=0.6))
        dti = float((amt / inc) * 100.0)

        feats = {
            "applicant_income": round(inc, 2),
            "credit_score": round(cs, 1),
            "loan_amount": round(amt, 2),
            "debt_to_income": round(dti, 2),
        }

        # Model predicts
        pred = int(model.predict([[inc, cs, amt, dti]])[0])

        # Send to ArgusML
        event = {
            "model_id": "loan_default_v1",
            "features": feats,
            "prediction": pred,
            "ground_truth": pred,  # normal accuracy
            "latency_ms": float(round(np.random.normal(45, 5), 2)),
        }
        requests.post(f"{ARGUS_URL}/api/ingest", json=event)

    print("Successfully streamed 30 normal inferences! Check dashboard at http://127.0.0.1:8000")

    # 4. Inject Real World Drift into credit_score
    print("\n" + "=" * 60)
    print("Step 4: Injecting Covariate Shift (Macroeconomic Recession: Credit Scores Drop -25%)")
    print("=" * 60)

    for i in range(50):
        inc = float(np.random.lognormal(mean=10.5, sigma=0.5))
        # Severe shift in credit scores (simulating economic crisis)
        cs = float(np.clip(np.random.normal(loc=520.0, scale=40.0), 300, 850))
        amt = float(np.random.lognormal(mean=9.8, sigma=0.6))
        dti = float((amt / inc) * 100.0)

        feats = {
            "applicant_income": round(inc, 2),
            "credit_score": round(cs, 1),
            "loan_amount": round(amt, 2),
            "debt_to_income": round(dti, 2),
        }

        pred = int(model.predict([[inc, cs, amt, dti]])[0])
        # Actual ground truth diverges because world changed!
        gt = 1 if cs < 580 else 0

        event = {
            "model_id": "loan_default_v1",
            "features": feats,
            "prediction": pred,
            "ground_truth": gt,
            "latency_ms": float(round(np.random.normal(55, 8), 2)),
        }
        requests.post(f"{ARGUS_URL}/api/ingest", json=event)
        time.sleep(0.04)

    print("\n" + "!" * 60)
    print("DRIFT INJECTED! Check your browser at http://127.0.0.1:8000")
    print("ArgusML will detect credit_score drift, highlight it on the DAG, and pop a CRITICAL alert!")
    print("!" * 60)


if __name__ == "__main__":
    main()
