"""
Credit Card Fraud Model: Production Reference Classifier & Baseline Generator.

Features:
- transaction_amount (Float): Dollar transaction size
- foreign_ip_ratio (Float): Ratio of requests from untrusted foreign IPs [0.0 - 1.0]
- velocity_24h (Float): Card transactions in past 24 hours
- device_trust_score (Float): Trust rating from fingerprinting [0.0 - 100.0]
- hour_of_day (Float): Time of transaction [0 - 23]
"""

from typing import Any, Dict, List, Tuple
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class FraudDetectionModel:
    """
    Simulated Credit Card Fraud Detection Classifier.
    Trained on synthetic banking data to achieve ~95% baseline accuracy.
    """

    FEATURES = [
        "transaction_amount",
        "foreign_ip_ratio",
        "velocity_24h",
        "device_trust_score",
        "hour_of_day",
    ]

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, max_depth=6, random_state=42)
        self.is_trained = False
        self.baseline_data: Dict[str, List[float]] = {}

    def generate_synthetic_data(
        self,
        n_samples: int = 3000,
        amount_multiplier: float = 1.0,
        foreign_ip_shift: float = 0.0,
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, List[float]]]:
        """
        Generates realistic credit card transactions with controlled distribution parameters.
        """
        np.random.seed(42 if amount_multiplier == 1.0 and foreign_ip_shift == 0.0 else None)

        # Baseline distributions
        # transaction_amount: log-normal distribution with typical small retail transactions
        base_amounts = np.random.lognormal(mean=3.8, sigma=0.85, size=n_samples) * amount_multiplier
        base_amounts = np.clip(base_amounts, 2.0, 8000.0)

        # foreign_ip_ratio: Beta distribution skewed towards 0 for domestic users
        foreign_ips = np.random.beta(a=0.5, b=5.0, size=n_samples) + foreign_ip_shift
        foreign_ips = np.clip(foreign_ips, 0.0, 1.0)

        # velocity_24h: Poisson distribution
        velocity = np.random.poisson(lam=3.5, size=n_samples).astype(float)

        # device_trust_score: Normal distribution centered at 85
        device_trust = np.random.normal(loc=82.0, scale=12.0, size=n_samples)
        device_trust = np.clip(device_trust, 0.0, 100.0)

        # hour_of_day: Normal distribution centered around midday/evening
        hours = (np.random.normal(loc=14.0, scale=5.0, size=n_samples) % 24).astype(float)

        # Ground truth fraud generation logic (fraudsters exhibit high velocity, foreign IPs, unusual amounts)
        fraud_risk = (
            (base_amounts > 500.0).astype(float) * 0.35
            + (foreign_ips > 0.4).astype(float) * 0.40
            + (velocity > 6.0).astype(float) * 0.25
            + (device_trust < 40.0).astype(float) * 0.30
            + np.random.normal(0, 0.1, size=n_samples)
        )
        labels = (fraud_risk > 0.45).astype(int)

        feature_matrix = np.column_stack(
            [base_amounts, foreign_ips, velocity, device_trust, hours]
        )

        data_dict = {
            "transaction_amount": base_amounts.tolist(),
            "foreign_ip_ratio": foreign_ips.tolist(),
            "velocity_24h": velocity.tolist(),
            "device_trust_score": device_trust.tolist(),
            "hour_of_day": hours.tolist(),
        }

        return feature_matrix, labels, data_dict

    def train_baseline_model(self) -> Dict[str, Any]:
        """
        Trains the reference model on clean baseline data and saves baseline distributions.
        """
        X, y, data_dict = self.generate_synthetic_data(n_samples=4000)
        self.baseline_data = data_dict

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42
        )
        self.model.fit(X_train, y_train)
        self.is_trained = True

        acc = self.model.score(X_test, y_test)
        return {
            "baseline_accuracy": round(float(acc), 4),
            "feature_names": self.FEATURES,
            "training_samples": len(X_train),
            "test_samples": len(X_test),
        }

    def predict(self, feature_dict: Dict[str, float]) -> Tuple[int, float]:
        """
        Predicts fraud (1) or legit (0) and returns confidence probability.
        """
        if not self.is_trained:
            self.train_baseline_model()

        vec = np.array([[feature_dict[f] for f in self.FEATURES]])
        probs = self.model.predict_proba(vec)[0]
        pred = int(np.argmax(probs))
        confidence = float(probs[pred])
        return pred, confidence
