"""
ModelTestingHistory: Chronological Audit & Testing Session History for ArgusML.

Maintains historical session logs of model registrations, live drift detections,
RCA graph diagnoses, and retraining runs with snapshots.
"""

from dataclasses import dataclass, field
import threading
import time
from typing import Any, Dict, List, Optional


@dataclass
class TestSessionRecord:
    __test__ = False
    session_id: str
    timestamp: float
    formatted_time: str
    model_id: str
    model_name: str
    event_type: str  # 'REGISTERED', 'TESTED_NORMAL', 'DRIFT_DETECTED', 'RETRAINED', 'SWITCHED'
    summary: str
    accuracy: Optional[float] = None
    p99_latency_ms: Optional[float] = None
    culprit_feature: Optional[str] = None
    severity_level: str = "HEALTHY"  # 'HEALTHY', 'WARNING', 'CRITICAL'
    diagnosis_output: Optional[Dict[str, Any]] = None
    graph_snapshot: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "formatted_time": self.formatted_time,
            "model_id": self.model_id,
            "model_name": self.model_name,
            "event_type": self.event_type,
            "summary": self.summary,
            "accuracy": self.accuracy,
            "p99_latency_ms": self.p99_latency_ms,
            "culprit_feature": self.culprit_feature,
            "severity_level": self.severity_level,
            "diagnosis_output": self.diagnosis_output,
            "graph_snapshot": self.graph_snapshot,
        }


class ModelTestingHistory:
    """
    Chronological Model Testing & Observability Session History.
    Maintains historical test snapshots and outputs in memory (Max capacity N).
    """

    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.history: List[TestSessionRecord] = []
        self.lock = threading.Lock()

    def record_session(
        self,
        model_id: str,
        model_name: str,
        event_type: str,
        summary: str,
        accuracy: Optional[float] = None,
        p99_latency_ms: Optional[float] = None,
        culprit_feature: Optional[str] = None,
        severity_level: str = "HEALTHY",
        diagnosis_output: Optional[Dict[str, Any]] = None,
        graph_snapshot: Optional[Dict[str, Any]] = None,
    ) -> TestSessionRecord:
        with self.lock:
            ts = time.time()
            fmt_time = time.strftime("%I:%M:%S %p - %b %d", time.localtime(ts))
            session_id = f"sess_{int(ts * 1000)}_{len(self.history)}"

            # Avoid recording identical rapid duplicate drift logs within 5 seconds
            if self.history and self.history[0].model_id == model_id and self.history[0].event_type == event_type:
                if ts - self.history[0].timestamp < 4.0:
                    # Update latest snapshot in place
                    self.history[0].accuracy = accuracy
                    self.history[0].p99_latency_ms = p99_latency_ms
                    self.history[0].diagnosis_output = diagnosis_output
                    self.history[0].graph_snapshot = graph_snapshot
                    return self.history[0]

            record = TestSessionRecord(
                session_id=session_id,
                timestamp=ts,
                formatted_time=fmt_time,
                model_id=model_id,
                model_name=model_name,
                event_type=event_type,
                summary=summary,
                accuracy=accuracy,
                p99_latency_ms=p99_latency_ms,
                culprit_feature=culprit_feature,
                severity_level=severity_level,
                diagnosis_output=diagnosis_output,
                graph_snapshot=graph_snapshot,
            )

            # Insert at front (most recent first)
            self.history.insert(0, record)
            if len(self.history) > self.capacity:
                self.history.pop()

            return record

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.lock:
            return [rec.to_dict() for rec in self.history[:limit]]

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            for rec in self.history:
                if rec.session_id == session_id:
                    return rec.to_dict()
            return None

    def clear(self):
        with self.lock:
            self.history.clear()
