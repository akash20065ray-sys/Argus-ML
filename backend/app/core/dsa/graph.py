"""
DependencyGraph: Directed Acyclic Graph (DAG) for Root-Cause Attribution & Blast Radius.

DSA Graph Algorithms:
- Adjacency List representation
- Reverse BFS/DFS: Upstream dependency tracing for Root Cause Analysis (RCA)
- Forward BFS/DFS: Downstream traversal for Blast Radius calculation
- Kahn's Algorithm: Topological sort and cycle detection
- Space: O(V + E), Traversal: O(V + E)
"""

from collections import deque
from dataclasses import dataclass, field
import threading
from typing import Any, Dict, List, Optional, Set


@dataclass
class GraphNode:
    node_id: str
    node_type: str  # 'PIPELINE', 'FEATURE', 'MODEL', 'SERVICE'
    name: str
    health: str = "HEALTHY"  # 'HEALTHY', 'WARNING', 'CRITICAL'
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.node_id,
            "type": self.node_type,
            "name": self.name,
            "health": self.health,
            "metadata": self.metadata,
        }


@dataclass
class GraphEdge:
    source_id: str
    target_id: str
    relationship: str = "FEEDS"  # 'FEEDS', 'CONSUMES', 'DEPENDS_ON'
    weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source_id,
            "target": self.target_id,
            "relationship": self.relationship,
            "weight": self.weight,
        }


class DependencyGraph:
    """
    Architectural Dependency Topology representing:
    Data Pipeline -> Feature -> Model -> Downstream Microservice
    """

    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.forward_adj: Dict[str, List[GraphEdge]] = {}  # source -> list of outgoing edges
        self.reverse_adj: Dict[str, List[GraphEdge]] = {}  # target -> list of incoming edges
        self.lock = threading.Lock()

    def add_node(
        self,
        node_id: str,
        node_type: str,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> GraphNode:
        with self.lock:
            if node_id not in self.nodes:
                node = GraphNode(
                    node_id=node_id,
                    node_type=node_type,
                    name=name,
                    metadata=metadata or {},
                )
                self.nodes[node_id] = node
                self.forward_adj[node_id] = []
                self.reverse_adj[node_id] = []
                return node
            else:
                self.nodes[node_id].name = name
                if metadata:
                    self.nodes[node_id].metadata.update(metadata)
                return self.nodes[node_id]

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relationship: str = "FEEDS",
        weight: float = 1.0,
    ):
        with self.lock:
            if source_id not in self.nodes or target_id not in self.nodes:
                raise ValueError(f"Both nodes must exist: {source_id} -> {target_id}")

            edge = GraphEdge(source_id, target_id, relationship, weight)
            # Avoid duplicate edges
            if not any(e.target_id == target_id for e in self.forward_adj[source_id]):
                self.forward_adj[source_id].append(edge)
                self.reverse_adj[target_id].append(edge)

    def set_node_health(self, node_id: str, health: str, metadata_update: Optional[Dict[str, Any]] = None):
        with self.lock:
            if node_id in self.nodes:
                self.nodes[node_id].health = health
                if metadata_update:
                    self.nodes[node_id].metadata.update(metadata_update)

    def get_upstream_nodes(self, start_node_id: str) -> List[GraphNode]:
        """
        Reverse-BFS: Traverses backwards from a node (e.g. Model) to find all
        upstream dependencies (Features, Data Pipelines) that could cause degradation.
        Time Complexity: O(V + E)
        """
        with self.lock:
            if start_node_id not in self.nodes:
                return []

            visited: Set[str] = set()
            queue: deque = deque([start_node_id])
            upstream_nodes: List[GraphNode] = []

            while queue:
                current_id = queue.popleft()
                if current_id != start_node_id and current_id not in visited:
                    visited.add(current_id)
                    upstream_nodes.append(self.nodes[current_id])

                for incoming_edge in self.reverse_adj.get(current_id, []):
                    parent_id = incoming_edge.source_id
                    if parent_id not in visited:
                        queue.append(parent_id)

            return upstream_nodes

    def get_downstream_nodes(self, start_node_id: str) -> List[GraphNode]:
        """
        Forward-BFS: Traverses forwards from a node to find the complete
        BLAST RADIUS (downstream models, consumer microservices, user interfaces).
        Time Complexity: O(V + E)
        """
        with self.lock:
            if start_node_id not in self.nodes:
                return []

            visited: Set[str] = set()
            queue: deque = deque([start_node_id])
            downstream_nodes: List[GraphNode] = []

            while queue:
                current_id = queue.popleft()
                if current_id != start_node_id and current_id not in visited:
                    visited.add(current_id)
                    downstream_nodes.append(self.nodes[current_id])

                for outgoing_edge in self.forward_adj.get(current_id, []):
                    child_id = outgoing_edge.target_id
                    if child_id not in visited:
                        queue.append(child_id)

            return downstream_nodes

    def topological_sort(self) -> List[str]:
        """
        Kahn's Algorithm for Topological Sorting:
        Verifies DAG property and returns evaluation order.
        Time Complexity: O(V + E)
        """
        with self.lock:
            in_degree = {nid: len(self.reverse_adj[nid]) for nid in self.nodes}
            queue = deque([nid for nid, deg in in_degree.items() if deg == 0])
            topo_order = []

            while queue:
                curr = queue.popleft()
                topo_order.append(curr)
                for edge in self.forward_adj[curr]:
                    in_degree[edge.target_id] -= 1
                    if in_degree[edge.target_id] == 0:
                        queue.append(edge.target_id)

            if len(topo_order) != len(self.nodes):
                raise ValueError("Graph contains a cycle! Invalid DAG topology.")

            return topo_order

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the graph topology for web visualization."""
        with self.lock:
            nodes_list = [node.to_dict() for node in self.nodes.values()]
            edges_list = []
            for edge_list in self.forward_adj.values():
                for edge in edge_list:
                    edges_list.append(edge.to_dict())

            return {"nodes": nodes_list, "edges": edges_list}

    def clear(self):
        """Clears all nodes and edges from the graph."""
        with self.lock:
            self.nodes.clear()
            self.forward_adj.clear()
            self.reverse_adj.clear()

    def build_topology_for_model(self, model_meta: Any):
        """
        Dynamically constructs the 4-layer DAG topology for ANY given model metadata.
        Layer 1: Upstream Data Ingestion Pipelines
        Layer 2: Features of this specific model
        Layer 3: The Model node
        Layer 4: Downstream Consumer Services (Blast Radius)
        """
        self.clear()

        # 1. Add Upstream Pipelines
        pipelines = getattr(model_meta, "upstream_pipelines", []) or ["Primary Ingestion Stream ETL"]
        pipe_ids = []
        for i, pipe_name in enumerate(pipelines):
            pid = f"pipe_{i}"
            self.add_node(pid, "PIPELINE", pipe_name)
            pipe_ids.append(pid)

        # 2. Add Model Node
        model_id = model_meta.model_id
        self.add_node(
            model_id,
            "MODEL",
            model_meta.name,
            {"version": model_meta.version, "type": model_meta.model_type},
        )

        # 3. Add Feature Nodes & connect with pipelines and model
        features = model_meta.features
        for i, feat_name in enumerate(features):
            fid = f"feat_{feat_name}"
            # Clean label for presentation
            clean_name = feat_name.replace("_", " ").title()
            self.add_node(fid, "FEATURE", clean_name)

            # Connect pipeline -> feature
            chosen_pipe = pipe_ids[i % len(pipe_ids)]
            self.add_edge(chosen_pipe, fid, "EXTRACTS")

            # Connect feature -> model
            self.add_edge(fid, model_id, "FEEDS")

        # 4. Add Downstream Services & connect with model
        services = getattr(model_meta, "downstream_services", []) or ["Production API Gateway", "Core Business Dashboard"]
        for i, srv_name in enumerate(services):
            sid = f"srv_{i}"
            self.add_node(sid, "SERVICE", srv_name)
            self.add_edge(model_id, sid, "CONSUMES")

