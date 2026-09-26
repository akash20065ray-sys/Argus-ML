# 🎓 ArgusML: Master Team Viva Question Bank & Model Answers

**Project:** **ArgusML** — Universal Production AI Observability Platform  
**Target:** Final Academic Project Evaluation & Viva Defense  
**Location:** `docs/VIVA_QUESTION_BANK.md`

---

## 👥 Module Distribution & Ownership
* **Aakash (Project Lead):** Dynamic 4-Layer DAG Topology, Reverse-BFS Root Cause Attribution, Forward-BFS Blast Radius, Multi-Factor RCS Scoring.
* **Krishna (Co-Lead):** Circular FIFO Ingestion Queue, Sliding Window Deque, Two-Sample Kolmogorov-Smirnov Test, Population Stability Index (PSI).
* **Sanskar (Analytical Lead):** Binary Max-Heap Priority Queue, Composite Severity Derivation, 4-Step Retraining Validation Gate.
* **Ghanshyam (Core Systems):** In-Memory Model Registry Hash Map, Multi-Task Classification/Regression Baselines, Universal Traffic Simulator.
* **Hari (Observability & UI):** Session History Audit Drawer, 1-Click Snapshot Replay, Markdown Post-Mortem Exporter, Canvas 2D Web Dashboard.

---

## 📚 Section 1: General & Architectural Questions (Team / Lead)

### Q1. What is the fundamental problem ArgusML solves compared to standard APM tools like Prometheus or Datadog?
**Model Answer:**  
Standard APM tools only monitor infrastructure-level metrics such as CPU, RAM, and network throughput. They cannot detect semantic failure modes in machine learning where system throughput is 100% healthy, but predictions are wildly inaccurate due to statistical covariate shift. ArgusML operates at the data and algorithmic layer, monitoring statistical distributions, calculating KS/PSI drift, isolating root causes via reverse DAG traversal, and self-healing via retraining gates.

### Q2. Why is ArgusML designed as a pure in-memory DSA platform rather than using external databases or message brokers?
**Model Answer:**  
By implementing our 5 core data structures directly in memory (Circular FIFO Queue, Sliding Window Deque, Hash Map, Binary Max-Heap, and DAG), we achieve sub-millisecond telemetry compute overhead (<0.45 ms). This allows continuous real-time model observability without introducing latency or network hops to the critical inference path.

### Q3. How does the system handle high-throughput production load without memory leaks?
**Model Answer:**  
We enforce strict fixed-capacity memory bounds: `EventQueue` has a fixed capacity of 5,000 events with zero-allocation modulo pointer wrapping, `MetricSlidingWindow` maintains a fixed W=400 deque, and `ModelTestingHistory` caps audit snapshots at N=100. Any surge in traffic gracefully drops oldest unconsumed events rather than expanding memory arbitrarily.

---

## 🌲 Section 2: Questions for Aakash (Lead — DAG & Reverse-BFS RCA)

### Q4. Why did you choose Reverse-BFS over Dijkstra or DFS for Root Cause Attribution?
**Model Answer:**  
In our 4-layer dependency DAG, all dependency links between pipelines, features, and model nodes are discrete unweighted edges. Breadth-First Search (BFS) explores dependencies layer by layer in strictly optimal $O(V + E)$ time. Dijkstra would add unnecessary $O(E \log V)$ heap overhead for unweighted edges, while DFS can traverse deep into irrelevant branches. Reverse-BFS guarantees that we discover the closest upstream culprit feature with shortest topological distance first.

### Q5. Explain the mathematical derivation of your Root Cause Confidence Score (RCS).
**Model Answer:**  
RCS evaluates multi-candidate attribution using a 4-factor weighted formula:  
$$	ext{RCS} = (0.45 \cdot 	ext{DriftEvidence}) + (0.30 \cdot 	ext{AccuracyDrop}) + (0.15 \cdot 	ext{TopologyProximity}) + (0.10 \cdot 	ext{BlastImpact})$$  
`DriftEvidence` is derived from normalized KS statistic $D$ and PSI. `AccuracyDrop` measures SLA degradation. `TopologyProximity` rewards features directly connected to the model, and `BlastImpact` weights downstream microservice exposure.

### Q6. How does Forward-BFS calculate the Downstream Blast Radius?
**Model Answer:**  
Starting from the degraded Model node, Forward-BFS traverses the forward adjacency list downstream to all reachable consumer nodes. It filters for nodes of type `SERVICE` (e.g. Checkout Gateway, Reporting API) and aggregates the affected service endpoints in $O(V+E)$ time.

---

## ⚡ Section 3: Questions for Krishna (Queue, Deque & Drift Analytics)

### Q7. How does the Circular FIFO Queue operate in strict O(1) time without dynamic allocation?
**Model Answer:**  
The `EventQueue` uses a pre-allocated array of size `capacity = 5000` with head and tail integer pointers. Enqueue writes to `array[tail]` and increments tail using modulo wrapping: `tail = (tail + 1) % capacity`. Dequeue reads from `array[head]` and updates `head = (head + 1) % capacity`. All operations are $O(1)$ time with zero dynamic memory allocation.

### Q8. Explain how the Two-Sample Kolmogorov-Smirnov (KS) test works in your DriftEngine.
**Model Answer:**  
The two-sample KS test is a non-parametric statistical test that compares the empirical cumulative distribution function (eCDF) of baseline data $F_{	ext{base}}(x)$ against the sliding window $F_{	ext{prod}}(x)$. It calculates the supremum distance:  
$$D = \sup_x \left| F_{	ext{base}}(x) - F_{	ext{prod}}(x) ight|$$  
If the resulting $p$-value is below $lpha = 0.05$, we reject the null hypothesis and flag significant covariate drift.

### Q9. What is the formula for Population Stability Index (PSI), and why is it essential alongside KS?
**Model Answer:**  
PSI measures distribution divergence across quantile bins:  
$$	ext{PSI} = \sum_{i=1}^{10} (	ext{Actual}_i - 	ext{Expected}_i) \cdot \ln\left(rac{	ext{Actual}_i}{	ext{Expected}_i}ight)$$  
While KS tests absolute shape divergence, PSI quantifies population volume shifts. A $	ext{PSI} < 0.10$ indicates stability, $0.10 \le 	ext{PSI} < 0.25$ is moderate drift, and $	ext{PSI} \ge 0.25$ indicates critical covariate shift requiring automated retraining.

---

## ⛰️ Section 4: Questions for Sanskar (Max-Heap & Retraining Gate)

### Q10. Why is a Binary Max-Heap better than a sorted array or linked list for alert management?
**Model Answer:**  
An unsorted list requires $O(N)$ time to search for the highest-priority alert. A sorted array requires $O(N)$ time on every new alert insertion. A Binary Max-Heap provides the optimal balance: $O(\log N)$ insertion via `_sift_up`, $O(\log N)$ extraction of the critical alert via `_sift_down`, and $O(1)$ instantaneous inspection of the top alert via `peek()`.

### Q11. Walk through the 4 validation checks in your Automated Retraining Gate.
**Model Answer:**  
Before a candidate model is promoted to production, `evaluate_validation_gate()` checks:
1. **Data Sufficiency:** Window contains $\ge 20$ labeled samples (or synthesizes recent adaptive distribution batch).
2. **SLA Recovery:** Candidate accuracy / $R^2 \ge$ SLA target.
3. **Latency Compliance:** Inference latency $\le$ SLA threshold.
4. **Positive Improvement:** Candidate score outperforms the degraded active model score.  
If all 4 pass, version is promoted (`v1.0.0` $ightarrow$ `v1.1.0`), baselines are refreshed, and Max-Heap alerts are resolved.

### Q12. What happens if the candidate model fails the validation gate?
**Model Answer:**  
If any of the 4 validation criteria fail, the candidate model is rejected. The promotion is blocked, the active model remains deployed, node health remains in WARNING/CRITICAL state, and an escalation alert remains in the Max-Heap for manual SRE inspection.

---

## 🗂️ Section 5: Questions for Ghanshyam (Model Registry & Simulator)

### Q13. How does ModelRegistry achieve O(1) lookup across multiple models?
**Model Answer:**  
`ModelRegistry` is an in-memory Hash Map indexed by `model_id`. Each `ModelMetadata` entry contains an inner hash map `feature_baselines` mapping feature names to `EmpiricalBaseline` objects. Python's hash table provides average-case $O(1)$ insertion, retrieval, and baseline moment indexing regardless of the number of registered models.

### Q14. How does the Universal Traffic Simulator generate realistic streaming inferences?
**Model Answer:**  
The simulator runs a background daemon thread that samples feature values from empirical Gaussian distributions (mean, std) and pushes synthetic inference payloads into the `EventQueue` at 20 events/sec. When feature drift is triggered, it dynamically applies scalar multipliers (e.g. 3.5x) to shifted feature distributions in real time.

### Q15. How does the platform support both Classification and Regression models?
**Model Answer:**  
The `ModelMetadata` and `UniversalModel` classes dynamically branch based on `model_type`: for CLASSIFICATION, it evaluates Accuracy and F1-score; for REGRESSION, it evaluates Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and $R^2$ score.

---

## 📜 Section 6: Questions for Hari (History Drawer, Post-Mortems & UI)

### Q16. How does ModelTestingHistory prevent audit log spam during rapid telemetry evaluations?
**Model Answer:**  
In `history.py`, `record_session()` inspects the most recent session record. If an identical `model_id` and `event_type` occurred within a 4.0-second time window, it updates the metrics and snapshot of the top record in place rather than appending duplicate entries to the audit trail.

### Q17. How does the 1-Click Historical Snapshot Replay work without rolling back live production data?
**Model Answer:**  
Each `TestSessionRecord` stores a deep-copy JSON snapshot of `graph_snapshot` and `diagnosis_output`. When clicked in the UI, the frontend `GraphRenderer` reads that static historical snapshot onto a dedicated canvas modal, allowing full visual inspection of historical node states while background streaming telemetry continues uninterrupted.

### Q18. What sections are included in the downloadable Markdown Post-Mortem Report?
**Model Answer:**  
The report generated by `generate_incident_report()` includes:
1. Executive Incident Summary
2. Root Cause Attribution with KS/PSI statistics
3. Ranked Candidate Causes by RCS Confidence
4. Impacted Downstream Blast Radius microservices
5. Closed-Loop Remediation and Retraining Logs
