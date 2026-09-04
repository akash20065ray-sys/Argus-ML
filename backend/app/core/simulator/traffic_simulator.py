"""
Universal Traffic & Drift Simulator:
Streams live inferences for ANY active ML model and allows injecting drift into ANY feature dynamically.
"""

import threading
import time
from typing import Any, Dict, Optional
import uuid
import numpy as np
from ..dsa.queue import EventQueue
from .universal_runner import UniversalModel


class UniversalTrafficSimulator:
    """
    Streaming worker that pushes live inference records for the active UniversalModel into EventQueue.
    Supports dynamic, feature-level covariate shift on demand.
    """

    def __init__(self, event_queue: EventQueue, initial_model: UniversalModel):
        self.queue = event_queue
        self.current_model = initial_model
        self.is_running = False
        self.events_per_second = 10.0
        self.worker_thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()

        # Dynamic drift configuration
        self.drift_feature: Optional[str] = None
        self.drift_multiplier: float = 1.0
        self.latency_base: float = 45.0
        self.generated_count = 0

    def start(self):
        with self.lock:
            if not self.is_running:
                self.is_running = True
                self.worker_thread = threading.Thread(
                    target=self._run_loop, daemon=True
                )
                self.worker_thread.start()

    def stop(self):
        with self.lock:
            self.is_running = False

    def switch_model(self, model: UniversalModel):
        """Switches the active model being simulated."""
        with self.lock:
            self.current_model = model
            self.drift_feature = None
            self.drift_multiplier = 1.0
            self.latency_base = 45.0

    def set_feature_drift(self, feature_name: Optional[str], multiplier: float = 1.0):
        """Injects covariate shift into ANY specified feature name."""
        with self.lock:
            self.drift_feature = feature_name
            self.drift_multiplier = multiplier

    def set_latency_spike(self, is_spiked: bool):
        with self.lock:
            self.latency_base = 280.0 if is_spiked else 45.0

    def reset(self):
        with self.lock:
            self.drift_feature = None
            self.drift_multiplier = 1.0
            self.latency_base = 45.0

    def get_status(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "is_running": self.is_running,
                "model_id": self.current_model.model_id,
                "model_name": self.current_model.name,
                "drift_feature": self.drift_feature,
                "drift_multiplier": self.drift_multiplier,
                "is_drifting": self.drift_feature is not None and self.drift_multiplier != 1.0,
                "latency_spiked": self.latency_base > 100.0,
                "events_per_second": self.events_per_second,
                "generated_count": self.generated_count,
            }

    def generate_single_event(self) -> Dict[str, Any]:
        with self.lock:
            model = self.current_model
            d_feat = self.drift_feature
            d_mult = self.drift_multiplier
            lat_base = self.latency_base

        features, ground_truth = model.synthesize_sample(
            drift_feature=d_feat, drift_multiplier=d_mult
        )
        pred, confidence = model.predict(features)

        latency = float(np.random.normal(loc=lat_base, scale=12.0))
        latency = max(12.0, latency)

        return {
            "event_id": f"evt_{uuid.uuid4().hex[:8]}",
            "model_id": model.model_id,
            "timestamp": time.time(),
            "features": features,
            "prediction": pred,
            "confidence": round(confidence, 4),
            "ground_truth": ground_truth,
            "latency_ms": round(latency, 2),
        }

    def _run_loop(self):
        while self.is_running:
            delay = 1.0 / max(1.0, self.events_per_second)
            event = self.generate_single_event()
            self.queue.enqueue(event)
            with self.lock:
                self.generated_count += 1
            time.sleep(delay)
