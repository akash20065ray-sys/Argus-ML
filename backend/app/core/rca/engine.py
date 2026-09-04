"""
Root-Cause Analysis (RCA) Engine: Connects Graph Topology, Drift Metrics, and Performance Degradation.

DSA Application:
- Traverses Graph Upstream (Reverse BFS) to locate culprit features and corrupt data pipelines.
- Traverses Graph Downstream (Forward BFS) to calculate affected Blast Radius.
- Uses Max-Heap to schedule the resulting prioritized alert.
"""

import time
from typing import Any, Dict, List, Optional
from ..dsa.graph import DependencyGraph, GraphNode
from ..dsa.heap import Alert, AlertMaxHeap


class RootCauseAnalysisEngine:
    """
    Automated diagnostic engine that connects model performance drops
    to underlying data drift and upstream pipeline causes.
    """

    def __init__(self, graph: DependencyGraph, alert_heap: AlertMaxHeap):
        self.graph = graph
        self.alert_heap = alert_heap

    def diagnose_model(
        self,
        model_id: str,
        current_metrics: Dict[str, float],
        sla_min_accuracy: float,
        drift_results: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """
        Diagnoses whether a model is degrading, pinpoints the root cause feature,
        calculates blast radius, and pushes prioritized alert to the Max-Heap.
        """
        current_acc = current_metrics.get("accuracy", 1.0)
        p99_lat = current_metrics.get("p99", 0.0)
        acc_drop = max(0.0, sla_min_accuracy - current_acc)
        is_accuracy_violation = current_acc < sla_min_accuracy

        top_drifts = drift_results.get("top_drifting_features", [])
        has_drift = len(top_drifts) > 0

        # If model is operating within SLA and no major drift, mark healthy
        if not is_accuracy_violation and not has_drift:
            self.graph.set_node_health(model_id, "HEALTHY")
            return None

        # 1. GRAPH TRAVERSAL: Upstream Root-Cause Discovery
        upstream_nodes = self.graph.get_upstream_nodes(model_id)
        upstream_feature_ids = {
            n.node_id: n for n in upstream_nodes if n.node_type == "FEATURE"
        }
        upstream_pipeline_ids = {
            n.node_id: n for n in upstream_nodes if n.node_type == "PIPELINE"
        }

        # 2. CULPRIT FEATURE ATTRIBUTION
        culprit_feature = None
        culprit_pipeline = None
        culprit_score = 0.0

        for drift_item in top_drifts:
            feat_name = drift_item["feature"]
            node_id = f"feat_{feat_name}"
            # Check if this drifting feature is an upstream dependency of our model
            if node_id in upstream_feature_ids:
                ks = drift_item.get("ks_statistic", 0.0)
                psi = drift_item.get("psi", 0.0)
                score = (ks * 50.0) + (min(psi, 1.0) * 50.0)
                if score > culprit_score:
                    culprit_score = score
                    culprit_feature = drift_item
                    # Update node health in graph
                    self.graph.set_node_health(
                        node_id,
                        "CRITICAL" if drift_item["severity"] == "CRITICAL" else "WARNING",
                        {"ks": ks, "psi": psi, "mean_shift": drift_item.get("mean_shift_pct")},
                    )

                    # Find the specific pipeline feeding this feature via reverse edge
                    for rev_edge in self.graph.reverse_adj.get(node_id, []):
                        if rev_edge.source_id in self.graph.nodes:
                            culprit_pipeline = self.graph.nodes[rev_edge.source_id].name

        # 3. GRAPH TRAVERSAL: Downstream Blast Radius
        downstream_nodes = self.graph.get_downstream_nodes(model_id)
        blast_radius = [
            f"{n.name} ({n.node_type})"
            for n in downstream_nodes
            if n.node_type in ["SERVICE", "MODEL"]
        ]

        # 4. COMPOSITE SEVERITY SCORING (For Max-Heap Priority)
        # Severity = (Accuracy Drop * 50) + (Culprit Drift * 30) + (Downstream Count * 10)
        composite_priority = (
            (acc_drop * 100.0 * 0.5)
            + (min(culprit_score, 100.0) * 0.3)
            + (min(len(blast_radius), 5) * 4.0)
        )
        composite_priority = min(100.0, max(10.0, composite_priority))

        severity_level = "LOW"
        if composite_priority >= 75.0 or (is_accuracy_violation and current_acc < 0.80):
            severity_level = "CRITICAL"
        elif composite_priority >= 50.0 or is_accuracy_violation:
            severity_level = "HIGH"
        elif composite_priority >= 30.0:
            severity_level = "MEDIUM"

        # Update model node health in graph
        self.graph.set_node_health(
            model_id,
            severity_level,
            {"accuracy": current_acc, "p99_latency": p99_lat, "drop": round(acc_drop * 100, 1)},
        )

        # 5. REMEDIATION RECOMMENDATION
        remediation_steps = []
        if culprit_feature:
            f_name = culprit_feature['feature']
            remediation_steps.append(
                f"1. [Retraining] Trigger scheduled retrain using recent production distribution for feature '{f_name}'."
            )
            remediation_steps.append(
                f"2. [Pipeline Check] Inspect upstream ingestion pipeline '{culprit_pipeline or 'Data Ingestion'} for schema or upstream provider change."
            )
            remediation_steps.append(
                f"3. [Fallback] Fallback to shadow rule-based heuristic for high-risk predictions until retrain validation completes."
            )
        else:
            remediation_steps.append(
                "1. [Inspection] Investigate recent label delay and latency spikes."
            )

        diagnosis_report = {
            "model_id": model_id,
            "timestamp": time.time(),
            "severity_level": severity_level,
            "priority_score": round(composite_priority, 2),
            "performance_summary": {
                "current_accuracy": current_acc,
                "sla_target": sla_min_accuracy,
                "accuracy_drop_pct": round(acc_drop * 100, 2),
                "p99_latency_ms": p99_lat,
            },
            "root_cause": {
                "culprit_feature": culprit_feature["feature"] if culprit_feature else "Unknown",
                "ks_statistic": culprit_feature.get("ks_statistic") if culprit_feature else 0.0,
                "psi": culprit_feature.get("psi") if culprit_feature else 0.0,
                "mean_shift_pct": culprit_feature.get("mean_shift_pct") if culprit_feature else 0.0,
                "upstream_source": culprit_pipeline or "Transaction Stream ETL",
                "diagnosis": (
                    f"Feature '{culprit_feature['feature']}' suffered a severe distribution shift "
                    f"(Shift: {culprit_feature.get('mean_shift_pct', 0)}%, KS: {culprit_feature.get('ks_statistic', 0)}), "
                    f"leading to a {round(acc_drop * 100, 1)}% accuracy drop."
                    if culprit_feature
                    else "Performance degradation without detected single-feature drift."
                ),
            },
            "blast_radius": blast_radius,
            "remediation": "\n".join(remediation_steps),
        }

        # 6. PUSH TO MAX-HEAP
        alert = Alert(
            priority=composite_priority,
            alert_id=f"alert_{model_id}_{int(time.time() // 60)}",
            timestamp=time.time(),
            model_id=model_id,
            alert_type="PERFORMANCE_AND_DATA_DRIFT" if culprit_feature else "PERFORMANCE_DROP",
            severity_level=severity_level,
            title=f"{severity_level} Degradation: {model_id}",
            description=diagnosis_report["root_cause"]["diagnosis"],
            root_cause=diagnosis_report["root_cause"],
            blast_radius=blast_radius,
            remediation=diagnosis_report["remediation"],
        )
        self.alert_heap.push(alert)

        return diagnosis_report
