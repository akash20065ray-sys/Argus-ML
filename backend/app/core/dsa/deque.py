"""
MetricSlidingWindow: Deque-based Rolling Window for O(1) Amortized Telemetry Updates.

DSA Complexity:
- Add Event / Evict Oldest: O(1) amortized
- Rolling Accuracy / F1: O(1) lookup
- Rolling Latency P99: O(W log W) or O(W) with quickselect
- Space: O(W * num_features)
"""

from collections import deque
import threading
from typing import Any, Dict, List, Optional
import numpy as np


class MetricSlidingWindow:
    """
    Sliding window using a double-ended queue (Deque) to maintain rolling performance
    and operational metrics over the most recent W predictions.
    """

    def __init__(self, window_size: int = 500):
        self.window_size = window_size
        self.lock = threading.Lock()

        # Deque of recent inference records
        # Each record: {
        #   "event_id": str,
        #   "timestamp": float,
        #   "prediction": int,
        #   "ground_truth": Optional[int],
        #   "latency_ms": float,
        #   "features": Dict[str, float]
        # }
        self.window: deque = deque(maxlen=window_size)

        # Deques per feature for drift testing window
        self.feature_windows: Dict[str, deque] = {}

        # Rolling confusion matrix counters (for events with ground truth)
        self.tp = 0
        self.fp = 0
        self.tn = 0
        self.fn = 0
        self.labeled_count = 0
        self.total_processed = 0

    def add_record(self, record: Dict[str, Any]):
        """
        Appends a new record to the right of the Deque.
        If the deque exceeds window_size, deque automatically drops the left-most (oldest) item.
        We update rolling metrics in O(1) amortized time.
        """
        with self.lock:
            self.total_processed += 1

            # If window is at capacity, the next append will evict the leftmost item
            if len(self.window) == self.window_size:
                evicted = self.window[0]
                self._remove_from_counts(evicted)

            self.window.append(record)
            self._add_to_counts(record)

            # Update feature deques
            features = record.get("features", {})
            for feat_name, val in features.items():
                if feat_name not in self.feature_windows:
                    self.feature_windows[feat_name] = deque(maxlen=self.window_size)
                self.feature_windows[feat_name].append(val)

    def _add_to_counts(self, record: Dict[str, Any]):
        gt = record.get("ground_truth")
        pred = record.get("prediction")

        if gt is not None and pred is not None:
            self.labeled_count += 1
            if gt == 1 and pred == 1:
                self.tp += 1
            elif gt == 0 and pred == 1:
                self.fp += 1
            elif gt == 0 and pred == 0:
                self.tn += 1
            elif gt == 1 and pred == 0:
                self.fn += 1

    def _remove_from_counts(self, record: Dict[str, Any]):
        gt = record.get("ground_truth")
        pred = record.get("prediction")

        if gt is not None and pred is not None:
            self.labeled_count = max(0, self.labeled_count - 1)
            if gt == 1 and pred == 1:
                self.tp = max(0, self.tp - 1)
            elif gt == 0 and pred == 1:
                self.fp = max(0, self.fp - 1)
            elif gt == 0 and pred == 0:
                self.tn = max(0, self.tn - 1)
            elif gt == 1 and pred == 0:
                self.fn = max(0, self.fn - 1)

    def get_performance_metrics(self) -> Dict[str, float]:
        """
        Computes rolling accuracy, precision, recall, and F1 score.
        Time Complexity: O(1)
        """
        with self.lock:
            if self.labeled_count == 0:
                return {
                    "accuracy": 1.0,
                    "precision": 1.0,
                    "recall": 1.0,
                    "f1_score": 1.0,
                    "sample_count": len(self.window),
                    "labeled_count": 0,
                }

            accuracy = (self.tp + self.tn) / self.labeled_count
            precision = self.tp / (self.tp + self.fp) if (self.tp + self.fp) > 0 else 0.0
            recall = self.tp / (self.tp + self.fn) if (self.tp + self.fn) > 0 else 0.0
            f1 = (
                2 * (precision * recall) / (precision + recall)
                if (precision + recall) > 0
                else 0.0
            )

            return {
                "accuracy": round(float(accuracy), 4),
                "precision": round(float(precision), 4),
                "recall": round(float(recall), 4),
                "f1_score": round(float(f1), 4),
                "sample_count": len(self.window),
                "labeled_count": self.labeled_count,
            }

    def get_latency_metrics(self) -> Dict[str, float]:
        """
        Calculates P50, P95, and P99 latencies over current window.
        """
        with self.lock:
            if not self.window:
                return {"p50": 0.0, "p95": 0.0, "p99": 0.0, "mean": 0.0}

            latencies = [r.get("latency_ms", 0.0) for r in self.window]
            p50 = float(np.percentile(latencies, 50))
            p95 = float(np.percentile(latencies, 95))
            p99 = float(np.percentile(latencies, 99))
            mean = float(np.mean(latencies))

            return {
                "p50": round(p50, 2),
                "p95": round(p95, 2),
                "p99": round(p99, 2),
                "mean": round(mean, 2),
            }

    def get_feature_samples(self, feature_name: str) -> List[float]:
        """Returns current window samples for a given feature."""
        with self.lock:
            if feature_name in self.feature_windows:
                return list(self.feature_windows[feature_name])
            return []

    def get_all_feature_samples(self) -> Dict[str, List[float]]:
        with self.lock:
            return {f: list(q) for f, q in self.feature_windows.items()}

    def clear(self):
        with self.lock:
            self.window.clear()
            self.feature_windows.clear()
            self.tp = self.fp = self.tn = self.fn = 0
            self.labeled_count = 0
