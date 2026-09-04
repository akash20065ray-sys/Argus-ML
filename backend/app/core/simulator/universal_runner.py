"""
Universal Model Runner: Trains, hosts, and streams predictions for ANY ML model.
Supports both Classification and Regression across arbitrary domains and features.
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


class UniversalModel:
    """
    Encapsulates a trained ML model (Classifier or Regressor) with its baseline dataset.
    """

    def __init__(
        self,
        model_id: str,
        name: str,
        model_type: str,  # 'CLASSIFICATION' or 'REGRESSION'
        features: List[str],
        target_name: str,
        data_dict: Dict[str, List[float]],
        target_values: List[float],
        downstream_services: List[str],
        upstream_pipelines: List[str],
    ):
        self.model_id = model_id
        self.name = name
        self.model_type = model_type
        self.features = features
        self.target_name = target_name
        self.data_dict = data_dict
        self.target_values = target_values
        self.downstream_services = downstream_services
        self.upstream_pipelines = upstream_pipelines

        # Train model
        X = np.column_stack([data_dict[f] for f in features])
        y = np.array(target_values)

        if model_type == "REGRESSION":
            self.model = RandomForestRegressor(n_estimators=40, max_depth=6, random_state=42)
        else:
            self.model = RandomForestClassifier(n_estimators=40, max_depth=6, random_state=42)

        self.model.fit(X, y)

    def predict(self, feature_dict: Dict[str, float]) -> Tuple[Any, float]:
        vec = np.array([[feature_dict.get(f, 0.0) for f in self.features]])
        if self.model_type == "REGRESSION":
            pred = float(self.model.predict(vec)[0])
            confidence = 0.95
            return round(pred, 2), confidence
        else:
            probs = self.model.predict_proba(vec)[0]
            pred = int(np.argmax(probs))
            confidence = float(probs[pred])
            return pred, round(confidence, 4)

    def synthesize_sample(
        self,
        drift_feature: Optional[str] = None,
        drift_multiplier: float = 1.0,
    ) -> Tuple[Dict[str, float], Any]:
        """
        Synthesizes a realistic production transaction or inference record.
        Allows injecting drift into ANY feature by name.
        """
        features_sample = {}
        for f in self.features:
            arr = np.array(self.data_dict[f])
            mean = float(np.mean(arr))
            std = float(np.std(arr)) if len(arr) > 1 else 1.0

            val = float(np.random.normal(loc=mean, scale=std))
            min_v = float(np.min(arr))
            val = max(min_v * 0.5, val)

            if f == drift_feature:
                val = val * drift_multiplier

            features_sample[f] = round(val, 2)

        # Ground truth generation
        vec = np.array([[features_sample[f] for f in self.features]])
        pred, conf = self.predict(features_sample)

        # Generate realistic ground truth
        if self.model_type == "REGRESSION":
            gt = float(pred + np.random.normal(0, 15.0))
            gt = round(gt, 2)
        else:
            # Under normal conditions, ground truth matches prediction ~92-96%
            if drift_feature is not None and drift_multiplier != 1.0:
                # With severe drift, model predictions diverge from actual labels!
                gt = int(np.random.choice([0, 1], p=[0.3, 0.7]))
            else:
                gt = pred if np.random.random() < 0.94 else (1 - pred)

        return features_sample, gt


def generate_sample_models() -> List[UniversalModel]:
    """Generates 3 out-of-the-box pre-configured models across diverse domains."""
    models = []
    np.random.seed(42)
    n = 2500

    # 1. Customer Churn Predictor (SaaS / Telecom)
    tenure = np.random.exponential(scale=24.0, size=n) + 1.0
    tenure = np.clip(tenure, 1.0, 72.0)
    monthly_charges = np.random.normal(loc=65.0, scale=25.0, size=n)
    monthly_charges = np.clip(monthly_charges, 18.0, 130.0)
    support_tickets = np.random.poisson(lam=1.8, size=n).astype(float)
    data_usage = np.random.lognormal(mean=3.2, sigma=0.6, size=n)
    contract_type = np.random.choice([0.0, 1.0, 2.0], size=n, p=[0.5, 0.3, 0.2])

    churn_risk = (
        (monthly_charges > 85.0).astype(float) * 0.35
        + (support_tickets > 3.0).astype(float) * 0.40
        + (tenure < 12.0).astype(float) * 0.30
        + (contract_type == 0.0).astype(float) * 0.20
        + np.random.normal(0, 0.1, size=n)
    )
    churn_labels = (churn_risk > 0.48).astype(int).tolist()

    churn_model = UniversalModel(
        model_id="customer_churn_v1",
        name="Telecom Customer Churn Predictor",
        model_type="CLASSIFICATION",
        features=["tenure_months", "monthly_charges", "support_tickets_30d", "data_usage_gb", "contract_type_code"],
        target_name="is_churn",
        data_dict={
            "tenure_months": tenure.tolist(),
            "monthly_charges": monthly_charges.tolist(),
            "support_tickets_30d": support_tickets.tolist(),
            "data_usage_gb": data_usage.tolist(),
            "contract_type_code": contract_type.tolist(),
        },
        target_values=churn_labels,
        downstream_services=["Retention Campaign Engine", "CRM Notification Hub", "Customer Success Portal"],
        upstream_pipelines=["Billing & Plan Usage Stream", "Zendesk Support Tickets ETL"],
    )
    models.append(churn_model)

    # 2. Credit Card Fraud Model
    amt = np.random.lognormal(mean=3.8, sigma=0.85, size=n)
    foreign_ip = np.random.beta(a=0.5, b=5.0, size=n)
    velocity = np.random.poisson(lam=3.5, size=n).astype(float)
    trust_score = np.random.normal(loc=82.0, scale=12.0, size=n)
    hour = (np.random.normal(loc=14.0, scale=5.0, size=n) % 24).astype(float)

    fraud_risk = (
        (amt > 500.0) * 0.35 + (foreign_ip > 0.4) * 0.40 + (velocity > 6.0) * 0.25 + (trust_score < 40.0) * 0.30
    )
    fraud_labels = (fraud_risk > 0.45).astype(int).tolist()

    fraud_model = UniversalModel(
        model_id="fraud_detector_v1",
        name="Credit Card Fraud Classifier",
        model_type="CLASSIFICATION",
        features=["transaction_amount", "foreign_ip_ratio", "velocity_24h", "device_trust_score", "hour_of_day"],
        target_name="is_fraud",
        data_dict={
            "transaction_amount": amt.tolist(),
            "foreign_ip_ratio": foreign_ip.tolist(),
            "velocity_24h": velocity.tolist(),
            "device_trust_score": trust_score.tolist(),
            "hour_of_day": hour.tolist(),
        },
        target_values=fraud_labels,
        downstream_services=["E-Commerce Checkout API", "Instant Wire Transfer Service", "Fraud Operations Review Portal"],
        upstream_pipelines=["Core Payment Gateway Stream", "Mobile SDK Telemetry Stream"],
    )
    models.append(fraud_model)

    # 3. Real Estate Valuation (Regression!)
    sqft = np.random.normal(loc=1800.0, scale=600.0, size=n)
    sqft = np.clip(sqft, 500.0, 5000.0)
    beds = np.random.choice([1.0, 2.0, 3.0, 4.0, 5.0], size=n, p=[0.1, 0.25, 0.4, 0.2, 0.05])
    neighborhood = np.random.uniform(1.0, 10.0, size=n)
    interest_rate = np.random.normal(loc=6.5, scale=0.8, size=n)
    property_age = np.random.uniform(0.0, 50.0, size=n)

    price = (sqft * 0.18) + (beds * 35.0) + (neighborhood * 22.0) - (interest_rate * 12.0) - (property_age * 1.5)
    price = np.clip(price, 80.0, 1500.0).tolist()

    house_model = UniversalModel(
        model_id="house_price_v1",
        name="Property Price Valuation Engine",
        model_type="REGRESSION",
        features=["square_feet", "bedrooms", "neighborhood_score", "interest_rate_pct", "property_age"],
        target_name="price_in_k",
        data_dict={
            "square_feet": sqft.tolist(),
            "bedrooms": beds.tolist(),
            "neighborhood_score": neighborhood.tolist(),
            "interest_rate_pct": interest_rate.tolist(),
            "property_age": property_age.tolist(),
        },
        target_values=price,
        downstream_services=["Mortgage Approval Engine", "Home Equity Underwriting API", "Zillow Listing Price Feeder"],
        upstream_pipelines=["MLS Real Estate Feed", "Federal Reserve Macroeconomic Stream"],
    )
    models.append(house_model)

    return models
