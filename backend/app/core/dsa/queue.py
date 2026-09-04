"""
EventQueue: Thread-Safe Circular FIFO Queue for High-Throughput Prediction Ingestion.

DSA Complexity:
- Enqueue: O(1)
- Dequeue: O(1)
- Space: O(Capacity)
"""

import threading
import time
from typing import Any, Dict, List, Optional


class EventQueue:
    """
    Circular FIFO Queue designed for high-throughput prediction log streaming.
    Decouples ingestion HTTP requests from analytical drift processing.
    """

    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.buffer: List[Optional[Dict[str, Any]]] = [None] * capacity
        self.head = 0  # Points to the front element to dequeue
        self.tail = 0  # Points to the next empty slot to enqueue
        self.count = 0
        self.dropped_events = 0
        self.total_enqueued = 0
        self.total_dequeued = 0

        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)

    def enqueue(self, event: Dict[str, Any]) -> bool:
        """
        Pushes an incoming inference event to the queue.
        If queue is full, the oldest event is overwritten (or dropped) with a metric increment.
        Time Complexity: O(1)
        """
        with self.lock:
            if self.count == self.capacity:
                # Buffer full: drop oldest to preserve latest real-time telemetry
                self.head = (self.head + 1) % self.capacity
                self.count -= 1
                self.dropped_events += 1

            self.buffer[self.tail] = event
            self.tail = (self.tail + 1) % self.capacity
            self.count += 1
            self.total_enqueued += 1

            self.not_empty.notify()
            return True

    def dequeue(self, timeout: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """
        Pops the oldest inference event from the queue.
        Blocks until an event is available or timeout occurs.
        Time Complexity: O(1)
        """
        with self.not_empty:
            start_time = time.time()
            while self.count == 0:
                if timeout is not None:
                    elapsed = time.time() - start_time
                    remaining = timeout - elapsed
                    if remaining <= 0:
                        return None
                    self.not_empty.wait(remaining)
                else:
                    self.not_empty.wait()

            event = self.buffer[self.head]
            self.buffer[self.head] = None
            self.head = (self.head + 1) % self.capacity
            self.count -= 1
            self.total_dequeued += 1
            return event

    def dequeue_batch(self, max_batch_size: int = 100) -> List[Dict[str, Any]]:
        """
        Dequeues up to max_batch_size elements in a single lock acquisition.
        Time Complexity: O(batch_size)
        """
        events = []
        with self.lock:
            num_to_pop = min(self.count, max_batch_size)
            for _ in range(num_to_pop):
                event = self.buffer[self.head]
                self.buffer[self.head] = None
                self.head = (self.head + 1) % self.capacity
                self.count -= 1
                self.total_dequeued += 1
                if event is not None:
                    events.append(event)
        return events

    def is_empty(self) -> bool:
        with self.lock:
            return self.count == 0

    def is_full(self) -> bool:
        with self.lock:
            return self.count == self.capacity

    def size(self) -> int:
        with self.lock:
            return self.count

    def get_stats(self) -> Dict[str, Any]:
        """Returns runtime queue telemetry."""
        with self.lock:
            return {
                "capacity": self.capacity,
                "current_size": self.count,
                "utilization_pct": round((self.count / self.capacity) * 100, 2),
                "total_enqueued": self.total_enqueued,
                "total_dequeued": self.total_dequeued,
                "dropped_events": self.dropped_events,
            }
