"""
ModelRegistry: Universal HashMap-Based Fast In-Memory Store for Any ML Model.

DSA Complexity:
- Get / Put Model: O(1)
- Get / Put Baseline: O(1)
- Space: O(num_models * num_features)
"""

from dataclasses import dataclass, field
import threading
from typing import Any, Dict, List, Optional
import numpy as np


@dataclass
class FeatureBaseline:
    name: str
    feature_type: str  # 'NUMERICAL', 'CATEGORICAL'
    mean: float
    std: float
    min_val: float
    max_val: float
    quantiles: List[float]  # e.g. 10th, 25th, 50th, 75th, 90th
    baseline_samples: List[float] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "feature_type": self.feature_type,
            "mean": self.mean,
            "std": self.std,
            "min_val": self.min_val,
            "max_val": self.max_val,
            "quantiles": self.quantiles,
            "sample_count": len(self.baseline_samples),
        }


@dataclass
class ModelMetadata:
    model_id: str
    name: str
    version: str
    description: str
    model_type: str  # 'CLASSIFICATION' or 'REGRESSION'
    features: List[str]
    target_name: str
    downstream_services: List[str] = field(default_factory=list)
    upstream_pipelines: List[str] = field(default_factory=list)
    sla_min_accuracy: float = 0.85
    sla_max_p99_latency_ms: float = 200.0
    sla_max_drift_pvalue: float = 0.05
    feature_baselines: Dict[str, FeatureBaseline] = field(default_factory=dict)
    active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "model_type": self.model_type,
            "features": self.features,
            "target_name": self.target_name,
            "downstream_services": self.downstream_services,
            "upstream_pipelines": self.upstream_pipelines,
            "sla": {
                "min_accuracy": self.sla_min_accuracy,
                "max_p99_latency_ms": self.sla_max_p99_latency_ms,
                "max_drift_pvalue": self.sla_max_drift_pvalue,
            },
            "feature_count": len(self.features),
            "active": self.active,
        }


class ModelRegistry:
    """
    Universal HashMap-based registry supporting ANY ML model and feature schema.
    """

    def __init__(self):
        self.models: Dict[str, ModelMetadata] = {}
        self.lock = threading.Lock()

    def register_model(self, metadata: ModelMetadata):
        """Stores model metadata in HashMap. O(1) time."""
        with self.lock:
            self.models[metadata.model_id] = metadata

    def get_model(self, model_id: str) -> Optional[ModelMetadata]:
        """O(1) lookup."""
        with self.lock:
            return self.models.get(model_id)

    def register_feature_baseline(
        self,
        model_id: str,
        feature_name: str,
        samples: List[float],
        feature_type: str = "NUMERICAL",
    ):
        """
        Calculates and stores empirical distribution statistics for drift comparison.
        """
        arr = np.array(samples, dtype=float)
        arr = arr[~np.isnan(arr)]
        if len(arr) == 0:
            return

        mean = float(np.mean(arr))
        std = float(np.std(arr)) if len(arr) > 1 else 0.0
        min_v = float(np.min(arr))
        max_v = float(np.max(arr))
        quantiles = [float(q) for q in np.percentile(arr, [10, 25, 50, 75, 90])]

        baseline = FeatureBaseline(
            name=feature_name,
            feature_type=feature_type,
            mean=round(mean, 4),
            std=round(std, 4),
            min_val=round(min_v, 4),
            max_val=round(max_v, 4),
            quantiles=quantiles,
            baseline_samples=list(samples[:600]),  # Keep reference sample for KS-test
        )

        with self.lock:
            if model_id in self.models:
                self.models[model_id].feature_baselines[feature_name] = baseline

    def register_from_dataset(
        self,
        model_id: str,
        name: str,
        model_type: str,
        data_dict: Dict[str, List[float]],
        target_name: str,
        downstream_services: Optional[List[str]] = None,
        upstream_pipelines: Optional[List[str]] = None,
        sla_min_accuracy: float = 0.85,
        sla_max_p99_latency_ms: float = 200.0,
        description: str = "",
    ) -> ModelMetadata:
        """
        Universal registration helper: automatically extracts feature schema
        and computes baselines from any dictionary of feature columns.
        """
        features = [k for k in data_dict.keys() if k != target_name]

        metadata = ModelMetadata(
            model_id=model_id,
            name=name,
            version="1.0.0",
            description=description or f"{name} ({model_type})",
            model_type=model_type,
            features=features,
            target_name=target_name,
            downstream_services=downstream_services or ["Production API Gateway", "Core Business Dashboard"],
            upstream_pipelines=upstream_pipelines or ["Real-time Ingestion Stream ETL"],
            sla_min_accuracy=sla_min_accuracy,
            sla_max_p99_latency_ms=sla_max_p99_latency_ms,
        )

        self.register_model(metadata)

        # Compute baselines for every feature automatically
        for feat_name in features:
            samples = data_dict[feat_name]
            self.register_feature_baseline(model_id, feat_name, samples)

        return metadata

    def get_feature_baseline(
        self, model_id: str, feature_name: str
    ) -> Optional[FeatureBaseline]:
        with self.lock:
            model = self.models.get(model_id)
            if model:
                return model.feature_baselines.get(feature_name)
            return None

    def list_models(self) -> List[Dict[str, Any]]:
        with self.lock:
            return [m.to_dict() for m in self.models.values()]
