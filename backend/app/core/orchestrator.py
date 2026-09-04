"""
Universal ArgusSystem Orchestrator:
Coordinates EventQueue, MetricWindow, DriftEngine, Dynamic DependencyGraph,
Root-Cause Diagnostics, and Max-Heap Alert Prioritization for ANY ML Model.
"""

import threading
import time
from typing import Any, Dict, List, Optional

from .dsa.deque import MetricSlidingWindow
from .dsa.graph import DependencyGraph
from .dsa.heap import AlertMaxHeap
from .dsa.queue import EventQueue
from .dsa.registry import ModelMetadata, ModelRegistry
from .drift.detector import DriftEngine
from .rca.engine import RootCauseAnalysisEngine
from .simulator.universal_runner import UniversalModel, generate_sample_models
from .simulator.traffic_simulator import UniversalTrafficSimulator


class ArgusSystem:
    """
    Central orchestration engine for Universal ML Model Observability.
    """

    def __init__(self, window_size: int = 400):
        # 1. DSA Components
        self.queue = EventQueue(capacity=5000)
        self.sliding_window = MetricSlidingWindow(window_size=window_size)
        self.alert_heap = AlertMaxHeap()
        self.graph = DependencyGraph()
        self.registry = ModelRegistry()

        # 2. Analytical Engines
        self.drift_engine = DriftEngine(significance_level=0.05)
        self.rca_engine = RootCauseAnalysisEngine(self.graph, self.alert_heap)

        # 3. Model Inventory & Simulator
        self.models_map: Dict[str, UniversalModel] = {}
        self.active_model_id: Optional[str] = None
        self.simulator: Optional[UniversalTrafficSimulator] = None

        # Background stream processor thread
        self.is_processing = False
        self.processor_thread: Optional[threading.Thread] = None

        # Telemetry state
        self.latest_drift_results: Dict[str, Any] = {}
        self.latest_diagnosis: Optional[Dict[str, Any]] = None
        self.events_since_drift_check = 0

    def load_sample_models(self):
        """Loads optional sample models only when explicitly requested by user."""
        sample_models = generate_sample_models()
        for m in sample_models:
            self.models_map[m.model_id] = m
            self.registry.register_from_dataset(
                model_id=m.model_id,
                name=m.name,
                model_type=m.model_type,
                data_dict=m.data_dict,
                target_name=m.target_name,
                downstream_services=m.downstream_services,
                upstream_pipelines=m.upstream_pipelines,
            )
        self.switch_active_model(sample_models[0].model_id)

    def switch_active_model(self, model_id: str) -> bool:
        """
        Switches the actively monitored model.
        Dynamically rebuilds DAG topology and resets sliding window.
        """
        if model_id not in self.models_map:
            return False

        self.active_model_id = model_id
        model = self.models_map[model_id]
        meta = self.registry.get_model(model_id)

        # 1. Switch simulator
        if self.simulator is None:
            self.simulator = UniversalTrafficSimulator(self.queue, model)
            if self.is_processing:
                self.simulator.start()
        else:
            self.simulator.switch_model(model)

        # 2. Clear telemetry window and alerts
        self.sliding_window.clear()
        self.alert_heap.clear()
        self.latest_drift_results = {}
        self.latest_diagnosis = None
        self.events_since_drift_check = 0

        # 3. Dynamically rebuild DAG topology for this model
        if meta:
            self.graph.build_topology_for_model(meta)

        return True

    def register_custom_model(
        self,
        model_id: str,
        name: str,
        model_type: str,
        data_dict: Dict[str, List[float]],
        target_name: str,
        target_values: List[float],
        downstream_services: Optional[List[str]] = None,
        upstream_pipelines: Optional[List[str]] = None,
        sla_min_accuracy: float = 0.85,
        sla_max_p99_latency_ms: float = 200.0,
    ) -> ModelMetadata:
        """
        Registers ANY user-supplied ML model and dataset.
        Trains model, registers feature baselines in HashMap, and builds dynamic DAG.
        """
        downstream = downstream_services or ["Production API Gateway", "Core Business Reporting Service"]
        upstream = upstream_pipelines or ["Kafka Stream ETL Ingestion"]
        features = [k for k in data_dict.keys() if k != target_name]

        # Create UniversalModel
        u_model = UniversalModel(
            model_id=model_id,
            name=name,
            model_type=model_type,
            features=features,
            target_name=target_name,
            data_dict=data_dict,
            target_values=target_values,
            downstream_services=downstream,
            upstream_pipelines=upstream,
        )
        self.models_map[model_id] = u_model

        # Register in HashMap baseline store
        meta = self.registry.register_from_dataset(
            model_id=model_id,
            name=name,
            model_type=model_type,
            data_dict=data_dict,
            target_name=target_name,
            downstream_services=downstream,
            upstream_pipelines=upstream,
            sla_min_accuracy=sla_min_accuracy,
            sla_max_p99_latency_ms=sla_max_p99_latency_ms,
        )

        # Automatically switch to the newly registered model
        self.switch_active_model(model_id)
        return meta

    def start(self):
        """Starts background stream processing and simulator."""
        if not self.is_processing:
            self.is_processing = True
            self.processor_thread = threading.Thread(
                target=self._process_stream_loop, daemon=True
            )
            self.processor_thread.start()
            if self.simulator:
                self.simulator.start()

    def stop(self):
        self.is_processing = False
        if self.simulator:
            self.simulator.stop()

    def _process_stream_loop(self):
        while self.is_processing:
            batch = self.queue.dequeue_batch(max_batch_size=20)
            if not batch:
                time.sleep(0.05)
                continue

            for event in batch:
                # Only record events for currently active model
                if event.get("model_id") == self.active_model_id:
                    self.sliding_window.add_record(event)
                    self.events_since_drift_check += 1

            # Run analytical drift evaluation and RCA every 25 processed events
            if self.events_since_drift_check >= 25:
                self._evaluate_telemetry()
                self.events_since_drift_check = 0

    def _evaluate_telemetry(self):
        model_meta = self.registry.get_model(self.active_model_id)
        if not model_meta:
            return

        baseline_map = {
            f: model_meta.feature_baselines[f].baseline_samples
            for f in model_meta.features
            if f in model_meta.feature_baselines
        }
        current_map = self.sliding_window.get_all_feature_samples()

        # 1. Run statistical drift analysis
        drift_res = self.drift_engine.evaluate_all(baseline_map, current_map)
        self.latest_drift_results = drift_res

        # 2. Get current rolling performance and latency metrics
        perf_metrics = self.sliding_window.get_performance_metrics()
        lat_metrics = self.sliding_window.get_latency_metrics()
        perf_metrics.update(lat_metrics)

        # 3. Trigger Root-Cause Analysis via Dependency Graph
        diagnosis = self.rca_engine.diagnose_model(
            model_id=self.active_model_id,
            current_metrics=perf_metrics,
            sla_min_accuracy=model_meta.sla_min_accuracy,
            drift_results=drift_res,
        )
        if diagnosis:
            self.latest_diagnosis = diagnosis

    def get_dashboard_summary(self) -> Dict[str, Any]:
        perf = self.sliding_window.get_performance_metrics()
        latency = self.sliding_window.get_latency_metrics()
        queue_stats = self.queue.get_stats()
        sim_status = self.simulator.get_status() if self.simulator else None
        top_alerts = self.alert_heap.get_top_k(5)
        graph_dict = self.graph.to_dict()
        active_meta = self.registry.get_model(self.active_model_id) if self.active_model_id else None

        return {
            "timestamp": time.time(),
            "active_model": active_meta.to_dict() if active_meta else None,
            "available_models": self.registry.list_models(),
            "performance": perf,
            "latency": latency,
            "queue_stats": queue_stats,
            "simulation": sim_status,
            "top_alerts": top_alerts,
            "graph": graph_dict,
            "drift_summary": self.latest_drift_results,
            "latest_diagnosis": self.latest_diagnosis,
        }

    def reset_metrics(self):
        self.sliding_window.clear()
        self.alert_heap.clear()
        self.latest_diagnosis = None
        self.latest_drift_results = {}
        if self.simulator:
            self.simulator.reset()
        for node_id in self.graph.nodes:
            self.graph.set_node_health(node_id, "HEALTHY")
