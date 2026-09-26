"""
Root-Cause Analysis (RCA) Engine: Evidence-Based Root Cause Confidence Scoring (RCS).

DSA & Algorithmic Principles:
- Traverses Graph Upstream (Reverse BFS, O(V + E)) to discover candidate features and pipelines.
- Traverses Graph Downstream (Forward BFS, O(V + E)) to quantify affected Blast Radius.
- Evaluates multi-factor Root Cause Confidence Scores (RCS) across all candidates.
- Prioritizes top candidate incidents in Binary Max-Heap (O(log N)).
"""

import time
from typing import Any, Dict, List, Optional
from ..dsa.graph import DependencyGraph, GraphNode
from ..dsa.heap import Alert, AlertMaxHeap


class RootCauseAnalysisEngine:
    """
    Evidence-based root cause analysis engine that evaluates statistical drift,
    dependency graph topology, performance degradation, and blast radius to rank
    candidate root causes with Root Cause Confidence Scores (RCS).
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
        rcs_weights: Optional[Dict[str, float]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluates model telemetry, discovers upstream candidate features via Reverse-BFS,
        computes Root Cause Confidence Scores (RCS) for all candidates, evaluates downstream
        blast radius via Forward-BFS, and schedules prioritized alerts in the Max-Heap.
        """
        weights = rcs_weights or {
            "w_drift": 0.45,
            "w_perf": 0.30,
            "w_proximity": 0.15,
            "w_blast": 0.10,
        }

        current_acc = current_metrics.get("accuracy", 1.0)
        p99_lat = current_metrics.get("p99", 0.0)
        acc_drop = max(0.0, sla_min_accuracy - current_acc)
        is_accuracy_violation = current_acc < sla_min_accuracy

        evaluated_features = drift_results.get("evaluated_features", {})
        top_drifts = drift_results.get("top_drifting_features", [])
        has_drift = len(top_drifts) > 0

        # If model is operating within SLA and no drift is detected, mark healthy
        if not is_accuracy_violation and not has_drift:
            self.graph.set_node_health(model_id, "HEALTHY")
            return None

        # 1. GRAPH TRAVERSAL: Upstream Dependency Discovery (Reverse-BFS, O(V + E))
        upstream_nodes = self.graph.get_upstream_nodes(model_id)
        upstream_features = {
            n.node_id: n for n in upstream_nodes if n.node_type == "FEATURE"
        }

        # 2. GRAPH TRAVERSAL: Downstream Blast Radius (Forward-BFS, O(V + E))
        downstream_nodes = self.graph.get_downstream_nodes(model_id)
        blast_radius = [
            f"{n.name} ({n.node_type})"
            for n in downstream_nodes
            if n.node_type in ["SERVICE", "MODEL"]
        ]
        blast_impact_norm = min(1.0, len(blast_radius) / 4.0)

        # 3. MULTI-CANDIDATE ROOT CAUSE CONFIDENCE SCORING (RCS)
        feature_drift_dict: Dict[str, Dict[str, Any]] = dict(evaluated_features)
        for item in top_drifts:
            f = item.get("feature")
            if f and f not in feature_drift_dict:
                feature_drift_dict[f] = item

        candidate_causes = []
        for feat_name, drift_info in feature_drift_dict.items():
            node_id = f"feat_{feat_name}" if not feat_name.startswith("feat_") else feat_name
            clean_feat = feat_name.replace("feat_", "")

            # Only consider features that are upstream dependencies of this model
            if upstream_features and (node_id not in upstream_features and clean_feat not in upstream_features and feat_name not in upstream_features):
                continue

            ks = float(drift_info.get("ks_statistic", 0.0))
            psi = float(drift_info.get("psi", 0.0))
            p_val = float(drift_info.get("p_value", 1.0))
            mean_shift = float(drift_info.get("mean_shift_pct", 0.0))
            is_drifting = drift_info.get("drift_detected", False)

            # Component 1: Drift Evidence Score [0.0 - 1.0]
            drift_score = (0.5 * min(1.0, ks / 0.45)) + (0.5 * min(1.0, psi / 0.35))

            # Component 2: Performance Drop Correlation [0.0 - 1.0]
            perf_drop_norm = min(1.0, acc_drop / 0.15) if is_accuracy_violation else 0.0

            # Component 3: Dependency Proximity [0.0 - 1.0]
            proximity_score = 1.0 if is_drifting else 0.4

            # Compute Composite RCS [0.0 - 100.0]
            raw_rcs = (
                (weights["w_drift"] * drift_score)
                + (weights["w_perf"] * perf_drop_norm)
                + (weights["w_proximity"] * proximity_score)
                + (weights["w_blast"] * blast_impact_norm)
            ) * 100.0

            confidence_pct = round(min(99.0, max(5.0, raw_rcs)), 1)

            # Trace originating upstream pipeline
            upstream_source = "Data Ingestion Stream ETL"
            for rev_edge in self.graph.reverse_adj.get(node_id, []):
                if rev_edge.source_id in self.graph.nodes:
                    upstream_source = self.graph.nodes[rev_edge.source_id].name

            # Update feature node health in dynamic DAG
            node_health = "CRITICAL" if (is_drifting and ks > 0.35) else "WARNING" if is_drifting else "HEALTHY"
            self.graph.set_node_health(
                node_id,
                node_health,
                {"ks": ks, "psi": psi, "confidence": confidence_pct, "mean_shift": mean_shift},
            )

            candidate_causes.append({
                "feature": clean_feat,
                "confidence_score": confidence_pct,
                "ks_statistic": round(ks, 4),
                "psi": round(psi, 4),
                "p_value": round(p_val, 4),
                "mean_shift_pct": mean_shift,
                "upstream_source": upstream_source,
                "drift_detected": is_drifting,
            })

        # Sort candidates descending by confidence score
        candidate_causes.sort(key=lambda x: x["confidence_score"], reverse=True)

        # Select primary candidate root cause
        primary_candidate = candidate_causes[0] if candidate_causes else None

        # 4. COMPOSITE SEVERITY SCORING (For Max-Heap Priority Ranking)
        top_conf = primary_candidate["confidence_score"] if primary_candidate else 20.0
        composite_priority = (
            (acc_drop * 100.0 * 0.45)
            + (top_conf * 0.35)
            + (min(len(blast_radius), 5) * 4.0)
        )
        composite_priority = min(100.0, max(10.0, composite_priority))

        severity_level = "LOW"
        if composite_priority >= 70.0 or (is_accuracy_violation and current_acc < 0.80):
            severity_level = "CRITICAL"
        elif composite_priority >= 45.0 or is_accuracy_violation:
            severity_level = "HIGH"
        elif composite_priority >= 25.0:
            severity_level = "MEDIUM"

        # Update model node health in graph
        self.graph.set_node_health(
            model_id,
            severity_level,
            {"accuracy": current_acc, "p99_latency": p99_lat, "drop": round(acc_drop * 100, 1)},
        )

        # 5. REMEDIATION RECOMMENDATION
        remediation_steps = []
        if primary_candidate and primary_candidate["drift_detected"]:
            f_name = primary_candidate["feature"]
            remediation_steps.append(
                f"1. [Retraining] Trigger candidate model retrain on recent distribution window containing '{f_name}'."
            )
            remediation_steps.append(
                f"2. [Validation Gate] Verify retrained candidate passes accuracy and drift threshold gates before promotion."
            )
            remediation_steps.append(
                f"3. [Pipeline Check] Inspect upstream ingestion source '{primary_candidate['upstream_source']}' for schema changes."
            )
        else:
            remediation_steps.append(
                "1. [Inspection] Investigate recent label delay and infrastructure latency."
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
            "candidate_root_causes": candidate_causes,
            "root_cause": {
                "culprit_feature": primary_candidate["feature"] if primary_candidate else "Unknown",
                "confidence_score": primary_candidate["confidence_score"] if primary_candidate else 0.0,
                "ks_statistic": primary_candidate.get("ks_statistic", 0.0) if primary_candidate else 0.0,
                "psi": primary_candidate.get("psi", 0.0) if primary_candidate else 0.0,
                "mean_shift_pct": primary_candidate.get("mean_shift_pct", 0.0) if primary_candidate else 0.0,
                "upstream_source": primary_candidate["upstream_source"] if primary_candidate else "Data Ingestion Stream ETL",
                "diagnosis": (
                    f"Candidate feature '{primary_candidate['feature']}' identified with {primary_candidate['confidence_score']}% confidence "
                    f"(Shift: {primary_candidate.get('mean_shift_pct', 0)}%, KS: {primary_candidate.get('ks_statistic', 0)}, PSI: {primary_candidate.get('psi', 0)}), "
                    f"correlating with a {round(acc_drop * 100, 1)}% accuracy drop."
                    if primary_candidate and primary_candidate["drift_detected"]
                    else "Performance degradation without detected single-feature drift."
                ),
            },
            "blast_radius": blast_radius,
            "remediation": "\n".join(remediation_steps),
        }

        # 6. SCHEDULE IN MAX-HEAP PRIORITY QUEUE (O(log N))
        alert = Alert(
            priority=composite_priority,
            alert_id=f"alert_{model_id}_{int(time.time() // 60)}",
            timestamp=time.time(),
            model_id=model_id,
            alert_type="PERFORMANCE_AND_DATA_DRIFT" if (primary_candidate and primary_candidate["drift_detected"]) else "PERFORMANCE_DROP",
            severity_level=severity_level,
            title=f"{severity_level} Degradation: {model_id}",
            description=diagnosis_report["root_cause"]["diagnosis"],
            root_cause=diagnosis_report["root_cause"],
            blast_radius=blast_radius,
            remediation=diagnosis_report["remediation"],
        )
        self.alert_heap.push(alert)

        return diagnosis_report
