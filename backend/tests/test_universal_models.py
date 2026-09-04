"""
Unit Tests for Universal, Model-Agnostic Observability in ArgusML.
"""

import numpy as np
import pytest
from backend.app.core.orchestrator import ArgusSystem


def test_clean_default_startup():
    """Validates that platform starts with a clean workspace (no sample models forced)."""
    sys = ArgusSystem(window_size=200)
    assert sys.active_model_id is None
    assert len(sys.registry.list_models()) == 0


def test_load_sample_models_on_demand():
    """Validates that diverse sample models can be loaded on demand."""
    sys = ArgusSystem(window_size=200)
    sys.load_sample_models()
    models = sys.registry.list_models()
    model_ids = {m["model_id"] for m in models}

    assert "customer_churn_v1" in model_ids
    assert "fraud_detector_v1" in model_ids
    assert "house_price_v1" in model_ids


def test_switch_model_rebuilds_dag():
    """Validates that switching models dynamically updates the DAG topology and features."""
    sys = ArgusSystem(window_size=200)
    sys.load_sample_models()

    # 1. Switch to House Price Regressor
    sys.switch_active_model("house_price_v1")
    graph_dict = sys.graph.to_dict()
    node_names = {n["name"] for n in graph_dict["nodes"]}

    assert "Square Feet" in node_names
    assert "Bedrooms" in node_names
    assert "Mortgage Approval Engine" in node_names

    # 2. Switch to Customer Churn
    sys.switch_active_model("customer_churn_v1")
    graph_dict2 = sys.graph.to_dict()
    node_names2 = {n["name"] for n in graph_dict2["nodes"]}

    assert "Monthly Charges" in node_names2
    assert "Tenure Months" in node_names2
    assert "Retention Campaign Engine" in node_names2


def test_register_any_custom_model_from_dataset():
    """Validates registering a completely new custom model with arbitrary feature names."""
    sys = ArgusSystem(window_size=200)
    np.random.seed(42)
    n = 500

    # Custom Medical Dataset: Diabetes Risk
    glucose = np.random.normal(110.0, 20.0, size=n).tolist()
    bmi = np.random.normal(26.0, 4.0, size=n).tolist()
    insulin = np.random.lognormal(2.5, 0.5, size=n).tolist()
    age = np.random.uniform(20.0, 70.0, size=n).tolist()
    labels = (np.array(glucose) > 130.0).astype(int).tolist()

    meta = sys.register_custom_model(
        model_id="diabetes_risk_v1",
        name="Clinical Diabetes Risk Predictor",
        model_type="CLASSIFICATION",
        data_dict={
            "glucose_level": glucose,
            "bmi_index": bmi,
            "serum_insulin": insulin,
            "patient_age": age,
        },
        target_name="has_diabetes",
        target_values=labels,
        downstream_services=["Hospital Alert System", "Patient Portal API"],
        upstream_pipelines=["Lab Test Results Pipeline"],
    )

    assert meta.model_id == "diabetes_risk_v1"
    assert sys.active_model_id == "diabetes_risk_v1"

    # Verify HashMap baselines computed
    base_glucose = sys.registry.get_feature_baseline("diabetes_risk_v1", "glucose_level")
    assert base_glucose is not None
    assert base_glucose.mean > 100.0

    # Verify DAG automatically built
    graph_dict = sys.graph.to_dict()
    node_ids = {n["id"] for n in graph_dict["nodes"]}
    assert "feat_glucose_level" in node_ids
    assert "feat_bmi_index" in node_ids
    assert "diabetes_risk_v1" in node_ids
    assert "srv_0" in node_ids  # Hospital Alert System
