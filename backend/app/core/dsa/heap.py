"""
AlertMaxHeap: Priority Queue (Max-Heap) for Dynamic Model Alert Prioritization.

DSA Implementation:
- Implemented from foundational principles with binary heap array, sift_up, and sift_down.
- Time Complexity:
  - Push (insert): O(log N)
  - Pop Max (extract root): O(log N)
  - Peek Max: O(1)
  - Get Top K: O(K log N)
- Space: O(N)
"""

from dataclasses import dataclass, field
import threading
import time
from typing import Any, Dict, List, Optional


@dataclass(order=True)
class Alert:
    # Priority key for Max-Heap comparison
    priority: float
    alert_id: str = field(compare=False)
    timestamp: float = field(compare=False)
    model_id: str = field(compare=False)
    alert_type: str = field(compare=False)  # 'DATA_DRIFT', 'PERFORMANCE_DROP', 'LATENCY_SPIKE'
    severity_level: str = field(compare=False)  # 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
    title: str = field(compare=False)
    description: str = field(compare=False)
    root_cause: Optional[Dict[str, Any]] = field(default=None, compare=False)
    blast_radius: List[str] = field(default_factory=list, compare=False)
    remediation: str = field(default="", compare=False)
    status: str = field(default="ACTIVE", compare=False)  # 'ACTIVE', 'ACKNOWLEDGED', 'RESOLVED'

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "priority": round(self.priority, 2),
            "timestamp": self.timestamp,
            "model_id": self.model_id,
            "alert_type": self.alert_type,
            "severity_level": self.severity_level,
            "title": self.title,
            "description": self.description,
            "root_cause": self.root_cause,
            "blast_radius": self.blast_radius,
            "remediation": self.remediation,
            "status": self.status,
        }


class AlertMaxHeap:
    """
    Max-Heap where root contains the highest priority (most severe) production alert.
    Prevents alert fatigue by ensuring on-call engineers address the highest blast-radius issue first.
    """

    def __init__(self):
        self.heap: List[Alert] = []
        self.index_map: Dict[str, int] = {}  # alert_id -> index in heap for O(1) existence checks
        self.lock = threading.Lock()

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left_child(self, i: int) -> int:
        return 2 * i + 1

    def _right_child(self, i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int):
        self.index_map[self.heap[i].alert_id] = j
        self.index_map[self.heap[j].alert_id] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _sift_up(self, i: int):
        """Restores Max-Heap invariant upwards: parent >= child."""
        parent = self._parent(i)
        while i > 0 and self.heap[i].priority > self.heap[parent].priority:
            self._swap(i, parent)
            i = parent
            parent = self._parent(i)

    def _sift_down(self, i: int):
        """Restores Max-Heap invariant downwards."""
        n = len(self.heap)
        max_idx = i

        left = self._left_child(i)
        if left < n and self.heap[left].priority > self.heap[max_idx].priority:
            max_idx = left

        right = self._right_child(i)
        if right < n and self.heap[right].priority > self.heap[max_idx].priority:
            max_idx = right

        if max_idx != i:
            self._swap(i, max_idx)
            self._sift_down(max_idx)

    def push(self, alert: Alert):
        """
        Inserts a new alert into the Max-Heap in O(log N) time.
        If an alert with the same ID already exists, its priority is updated in place.
        """
        with self.lock:
            if alert.alert_id in self.index_map:
                # Update existing alert
                idx = self.index_map[alert.alert_id]
                old_priority = self.heap[idx].priority
                self.heap[idx] = alert
                if alert.priority > old_priority:
                    self._sift_up(idx)
                else:
                    self._sift_down(idx)
                return

            self.heap.append(alert)
            idx = len(self.heap) - 1
            self.index_map[alert.alert_id] = idx
            self._sift_up(idx)

    def pop(self) -> Optional[Alert]:
        """
        Extracts and returns the highest priority alert in O(log N) time.
        """
        with self.lock:
            if not self.heap:
                return None

            max_alert = self.heap[0]
            last_item = self.heap.pop()
            del self.index_map[max_alert.alert_id]

            if self.heap:
                self.heap[0] = last_item
                self.index_map[last_item.alert_id] = 0
                self._sift_down(0)

            return max_alert

    def peek(self) -> Optional[Alert]:
        """Returns the top alert without removing it in O(1) time."""
        with self.lock:
            return self.heap[0] if self.heap else None

    def get_top_k(self, k: int = 10) -> List[Dict[str, Any]]:
        """
        Returns top K active alerts sorted descending by priority.
        """
        with self.lock:
            # We copy and sort the top items without destroying the heap
            sorted_alerts = sorted(self.heap, key=lambda x: x.priority, reverse=True)
            return [a.to_dict() for a in sorted_alerts[:k]]

    def resolve(self, alert_id: str) -> bool:
        """Removes or marks an alert as resolved."""
        with self.lock:
            if alert_id not in self.index_map:
                return False
            idx = self.index_map[alert_id]
            self.heap[idx].status = "RESOLVED"
            return True

    def clear(self):
        with self.lock:
            self.heap.clear()
            self.index_map.clear()

    def size(self) -> int:
        with self.lock:
            return len(self.heap)
