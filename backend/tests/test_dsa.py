"""
Unit Tests for Foundational Data Structures & Algorithms in ArgusML.
"""

import pytest
from backend.app.core.dsa.queue import EventQueue
from backend.app.core.dsa.deque import MetricSlidingWindow
from backend.app.core.dsa.heap import Alert, AlertMaxHeap
from backend.app.core.dsa.graph import DependencyGraph
from backend.app.core.dsa.registry import ModelMetadata, ModelRegistry


def test_event_queue_fifo_and_overflow():
    """Validates FIFO ordering and circular buffer overflow drop behavior."""
    q = EventQueue(capacity=3)
    assert q.is_empty()

    q.enqueue({"id": 1})
    q.enqueue({"id": 2})
    q.enqueue({"id": 3})
    assert q.is_full()
    assert q.size() == 3

    # Overflow: pushing 4th item should drop oldest (id: 1)
    q.enqueue({"id": 4})
    assert q.size() == 3
    assert q.dropped_events == 1

    e1 = q.dequeue()
    assert e1["id"] == 2
    e2 = q.dequeue()
    assert e2["id"] == 3
    e3 = q.dequeue()
    assert e3["id"] == 4
    assert q.is_empty()


def test_metric_sliding_window_accuracy_and_latency():
    """Tests O(1) rolling accuracy, F1, and percentile latency computations."""
    win = MetricSlidingWindow(window_size=10)

    # 8 correct, 2 incorrect
    for i in range(8):
        win.add_record({
            "prediction": 1,
            "ground_truth": 1,
            "latency_ms": 50.0 + i,
            "features": {"f1": 10.0 + i},
        })
    for i in range(2):
        win.add_record({
            "prediction": 1,
            "ground_truth": 0,
            "latency_ms": 120.0,
            "features": {"f1": 90.0},
        })

    perf = win.get_performance_metrics()
    assert perf["accuracy"] == 0.80
    assert perf["labeled_count"] == 10

    lat = win.get_latency_metrics()
    assert lat["p50"] > 0
    assert lat["p99"] >= 120.0


def test_alert_max_heap_priority_order():
    """Validates Max-Heap ordering property: highest priority alert popped first."""
    heap = AlertMaxHeap()

    a1 = Alert(priority=45.0, alert_id="a1", timestamp=1.0, model_id="m1", alert_type="DRIFT", severity_level="MEDIUM", title="Med", description="")
    a2 = Alert(priority=92.5, alert_id="a2", timestamp=2.0, model_id="m1", alert_type="ACCURACY_DROP", severity_level="CRITICAL", title="Crit", description="")
    a3 = Alert(priority=70.0, alert_id="a3", timestamp=3.0, model_id="m1", alert_type="LATENCY", severity_level="HIGH", title="High", description="")

    heap.push(a1)
    heap.push(a2)
    heap.push(a3)

    assert heap.peek().alert_id == "a2"

    top = heap.pop()
    assert top.alert_id == "a2"
    assert top.priority == 92.5

    next_top = heap.pop()
    assert next_top.alert_id == "a3"

    last_top = heap.pop()
    assert last_top.alert_id == "a1"
    assert heap.size() == 0


def test_dependency_graph_reverse_and_forward_traversal():
    """Validates reverse BFS for root cause and forward BFS for blast radius."""
    graph = DependencyGraph()

    # Add Pipeline -> Feature -> Model -> Services
    graph.add_node("pipe_etl", "PIPELINE", "ETL Stream")
    graph.add_node("feat_amount", "FEATURE", "Amount")
    graph.add_node("feat_ip", "FEATURE", "IP")
    graph.add_node("model_fraud", "MODEL", "Fraud Model")
    graph.add_node("srv_checkout", "SERVICE", "Checkout")
    graph.add_node("srv_payout", "SERVICE", "Payout")

    graph.add_edge("pipe_etl", "feat_amount")
    graph.add_edge("pipe_etl", "feat_ip")
    graph.add_edge("feat_amount", "model_fraud")
    graph.add_edge("feat_ip", "model_fraud")
    graph.add_edge("model_fraud", "srv_checkout")
    graph.add_edge("model_fraud", "srv_payout")

    # Upstream BFS from Model should find features and pipeline
    upstream = graph.get_upstream_nodes("model_fraud")
    upstream_ids = {n.node_id for n in upstream}
    assert "feat_amount" in upstream_ids
    assert "feat_ip" in upstream_ids
    assert "pipe_etl" in upstream_ids

    # Downstream BFS from Model should find the 2 microservices
    downstream = graph.get_downstream_nodes("model_fraud")
    downstream_ids = {n.node_id for n in downstream}
    assert "srv_checkout" in downstream_ids
    assert "srv_payout" in downstream_ids

    # Topological sort
    topo = graph.topological_sort()
    assert topo.index("pipe_etl") < topo.index("feat_amount")
    assert topo.index("feat_amount") < topo.index("model_fraud")
    assert topo.index("model_fraud") < topo.index("srv_checkout")
