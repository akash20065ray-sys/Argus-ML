# 🛡️ ArgusML: Capstone Presentation & Team Defense Guide

This document contains the **complete 12-slide presentation structure**, **5-member module division**, **word-for-word speaking script**, **code/file ownership breakdown**, and **viva Q&A defense answers**.

Generated Artifacts:
- **PowerPoint Presentation File:** [`ArgusML_Presentation.pptx`](file:///C:/DS_CP/ArgusML_Presentation.pptx)
- **Official Team Script PDF Document:** [`ArgusML_Team_Presentation_Script.pdf`](file:///C:/DS_CP/ArgusML_Team_Presentation_Script.pdf)

---

## 👥 1. Team Division & Module Ownership (5 Members)

| Team Member | Module & Role | DSA Concepts Implemented | Time Complexity | Source Code Files |
| :--- | :--- | :--- | :--- | :--- |
| **Aakash (Lead)** | **Dynamic 4-Layer DAG & Reverse-BFS RCA** | • Directed Acyclic Graph (DAG)<br>• Reverse-BFS Upstream Attribution<br>• Forward-BFS Downstream Blast Radius<br>• Multi-Factor RCS Confidence Formula | Reverse-BFS: **$O(V+E)$**<br>Forward-BFS: **$O(V+E)$** | [`dsa/graph.py`](file:///C:/DS_CP/backend/app/core/dsa/graph.py)<br>[`rca/engine.py`](file:///C:/DS_CP/backend/app/core/rca/engine.py)<br>[`orchestrator.py`](file:///C:/DS_CP/backend/app/core/orchestrator.py) |
| **Krishna** | **Queue, Sliding Window & Drift Engine** | • Circular FIFO Ingestion Buffer<br>• Double-Ended Queue (Deque)<br>• 2-Sample Kolmogorov-Smirnov Test<br>• Population Stability Index (PSI) | Queue Enqueue: **$O(1)$**<br>Deque Eviction: **$O(1)$**<br>KS Test: **$O(N \log N)$**<br>PSI: **$O(N + B)$** | [`dsa/queue.py`](file:///C:/DS_CP/backend/app/core/dsa/queue.py)<br>[`dsa/deque.py`](file:///C:/DS_CP/backend/app/core/dsa/deque.py)<br>[`drift/detector.py`](file:///C:/DS_CP/backend/app/core/drift/detector.py) |
| **Sanskar** | **Priority Max-Heap & Retraining Gate** | • Array-Backed Binary Max-Heap<br>• Pure `_sift_up` / `_sift_down`<br>• 4-Step Closed-Loop Validation Gate<br>• Automated Version Promotion | Push Alert: **$O(\log N)$**<br>Pop Max: **$O(\log N)$**<br>Peek Top: **$O(1)$**<br>Retrain Gate: **$O(S)$** | [`dsa/heap.py`](file:///C:/DS_CP/backend/app/core/dsa/heap.py)<br>[`universal_runner.py`](file:///C:/DS_CP/backend/app/core/simulator/universal_runner.py)<br>[`orchestrator.py`](file:///C:/DS_CP/backend/app/core/orchestrator.py) |
| **Ghanshyam** | **Model Registry & Traffic Simulator** | • In-Memory Baseline Hash Map Store<br>• Empirical Distribution Moments<br>• Multi-Task Model Management<br>• Controlled Covariate Shift Injector | Model Lookup: **$O(1)$**<br>Baseline Lookup: **$O(1)$**<br>Traffic Stream: **$O(K)$** | [`dsa/registry.py`](file:///C:/DS_CP/backend/app/core/dsa/registry.py)<br>[`traffic_simulator.py`](file:///C:/DS_CP/backend/app/core/simulator/traffic_simulator.py)<br>[`universal_runner.py`](file:///C:/DS_CP/backend/app/core/simulator/universal_runner.py) |
| **Hari** | **Session History, Reports & UI** | • Chronological Audit History<br>• 1-Click DAG Snapshot Replay<br>• Markdown Post-Mortem Generator<br>• Canvas 2D Animated Dashboard | Prepend History: **$O(1)$**<br>Snapshot Index: **$O(1)$**<br>Report Synthesize: **$O(R)$** | [`dsa/history.py`](file:///C:/DS_CP/backend/app/core/dsa/history.py)<br>[`main.py`](file:///C:/DS_CP/backend/app/main.py)<br>[`frontend/js/app.js`](file:///C:/DS_CP/frontend/js/app.js)<br>[`graph_renderer.js`](file:///C:/DS_CP/frontend/js/graph_renderer.js) |

---

## 📊 2. Slide Deck Outline (12 Slides)

1. **Slide 1:** Title Slide & Project Overview
2. **Slide 2:** Team Division & Individual Module Ownership (Mandatory 2nd Slide)
3. **Slide 3:** Problem Statement & Industry Motivation (The Silent ML Decay)
4. **Slide 4:** Core DSA Mapping & Algorithmic Complexity Table
5. **Slide 5:** End-to-End System Architecture & Data Flow Pipeline
6. **Slide 6:** Technical Deep-Dive: Aakash (Dynamic 4-Layer DAG & Reverse-BFS RCA)
7. **Slide 7:** Technical Deep-Dive: Krishna (Circular FIFO Queue, Deque & Drift Analytics)
8. **Slide 8:** Technical Deep-Dive: Sanskar (Binary Max-Heap & 4-Step Retraining Gate)
9. **Slide 9:** Technical Deep-Dive: Ghanshyam (In-Memory Baseline Hash Map & Traffic Simulator)
10. **Slide 10:** Technical Deep-Dive: Hari (History Audit Drawer, Post-Mortems & Canvas Dashboard)
11. **Slide 11:** Experimental Evaluation & 17 Unit Tests Verification
12. **Slide 12:** Conclusion, Impact & Live Demonstration

---

## 🎙️ 3. Complete Word-for-Word Speaking Script

### 🎤 Slide 1 & 2: Introduction & Team Division
**Speaker: AAKASH (Lead)**
> *"Respected professors and panel members, good morning. Today, our team is presenting **ArgusML** — a Universal Production AI Observability and Graph-Powered Root Cause Diagnostic Platform built entirely upon 5 foundational Data Structures and Algorithms.*
> 
> *In today’s presentation, we have divided the technical modules cleanly among 5 team members:*
> * *I (**Aakash**) am leading the central system orchestration, dynamic 4-layer DAG topology modeling, and Reverse-BFS root cause attribution.*
> * ***Krishna*** *will present the high-throughput circular FIFO ingestion queue, sliding window deque, and Kolmogorov-Smirnov statistical drift engine.*
> * ***Sanskar*** *will explain the binary max-heap priority queue and the closed-loop automated model retraining validation gate.*
> * ***Ghanshyam*** *will detail the in-memory hash map model registry and universal multi-model traffic simulation engine.*
> * ***Hari*** *will showcase our session history audit drawer, 1-click historical snapshot replay, and downloadable markdown post-mortem generator.*
> 
> *Let us begin with the core problem that motivated this project."*

---

### 🎤 Slide 3 & 4: Problem Statement & DSA Mapping
**Speaker: AAKASH (Lead)**
> *"Unlike traditional web servers that throw 500 internal errors when they break, machine learning models fail silently. Real-world consumer behavior shifts, causing data distributions to drift, while the model continues making confident, incorrect predictions. When a model’s accuracy drops from 95% to 65%, data engineering teams waste days manually tracing through dozens of multi-table ETL pipelines to isolate which specific feature was corrupted.*
> 
> *ArgusML solves this by implementing an entirely in-memory, pure DSA architecture with zero third-party vendor bloat. As shown in our DSA Mapping table on Slide 4, every system component maps directly to optimal theoretical complexity:*
> 1. *Circular FIFO Buffer for $O(1)$ ingestion without memory overflow.*
> 2. *Double-Ended Queue for amortized $O(1)$ rolling performance metrics.*
> 3. *In-Memory Hash Map for $O(1)$ model and baseline empirical distribution lookups.*
> 4. *Binary Max-Heap for $O(\log N)$ composite severity prioritization.*
> 5. *Dynamic Directed Acyclic Graph (DAG) for $O(V+E)$ reverse and forward BFS traversals.*
> 
> *I will now hand over to Krishna to explain how live predictions enter the system and how statistical drift is detected."*

---

### 🎤 Slide 5 & 7: Ingestion Buffer, Deque Window & Drift Engine
**Speaker: KRISHNA**
> *"Thank you, Aakash. I will now explain how ArgusML continuously watches streaming inferences and detects distribution shifts.*
> 
> *When client applications send inference payloads to `POST /api/ingest`, they enter our **Circular FIFO EventQueue** (`queue.py`). We implemented modulo pointer arithmetic so that enqueuing and dequeuing operate strictly in $O(1)$ time with a fixed capacity of 5,000 events. If an extreme traffic spike occurs, oldest unconsumed records are evicted gracefully, completely preventing memory leaks.*
> 
> *Next, a background stream processor dequeues batches into our **MetricSlidingWindow** (`deque.py`), which is an in-memory double-ended queue holding recent $W = 400$ predictions. This allows us to calculate rolling accuracy, precision, recall, and P99 latency in amortized $O(1)$ time.*
> 
> *Every 25 processed events, our **DriftEngine** (`detector.py`) executes two statistical tests against the baseline distributions stored in our Hash Map:*
> 1. ***Two-Sample Kolmogorov-Smirnov (KS) Test:*** *We compute the maximum vertical divergence $D$ between the baseline empirical cumulative distribution function (eCDF) and the sliding window in $O(N \log N)$ time. If $p < 0.05$, we flag significant covariate drift.*
> 2. ***Population Stability Index (PSI):*** *We bucket feature values across quantile bins in $O(N + B)$ time. A PSI $\ge 0.25$ indicates critical distribution shift.*
> 
> *Once drift is detected, Aakash’s DAG engine is triggered to isolate the root cause."*

---

### 🎤 Slide 6: Dynamic DAG & Root Cause Confidence Scoring (RCS)
**Speaker: AAKASH (Lead)**
> *"Once statistical drift is flagged, our **DependencyGraph** (`graph.py`) performs automated root cause attribution.*
> 
> *The DAG dynamically builds a 4-layer topology:*  
> `Upstream Pipelines → Inferred Features → Active Model → Downstream Services`.*
> 
> *We execute two Breadth-First Search traversals, both operating in $O(V + E)$ linear time:*
> 1. ***Reverse-BFS Upstream Attribution:*** *Starting at the degraded Model node, we traverse reverse adjacency lists upstream to find which specific feature node and upstream ingestion pipeline originated the corruption.*
> 2. ***Forward-BFS Downstream Blast Radius:*** *We traverse forward adjacency lists downstream from the model node to identify every production consumer API and reporting service impacted.*
> 
> *To rank candidate causes with mathematical rigor, I designed the **Root Cause Confidence Score (RCS)** formula:*  
> $\text{RCS} = (0.45 \times \text{DriftEvidence}) + (0.30 \times \text{AccuracyDrop}) + (0.15 \times \text{TopologyProximity}) + (0.10 \times \text{BlastImpact})$.  
> *This pinpoints the true culprit feature with over 85% to 95% confidence.*
> 
> *I will now hand over to Sanskar to explain how incidents are prioritized in the Max-Heap and how automated retraining cures the model."*

---

### 🎤 Slide 8: Priority Max-Heap & Retraining Validation Gate
**Speaker: SANSKAR**
> *"Thank you, Aakash. I will now explain our **AlertMaxHeap** and the **Closed-Loop Automated Model Retraining Pipeline**.*
> 
> *In production environments monitoring multiple models, alerts must be prioritized so SREs tackle the most dangerous failures first. We implemented a pure, array-backed **Binary Max-Heap** (`heap.py`) using pure `_sift_up` and `_sift_down` pointer swaps. Pushing a new incident and extracting the maximum severity incident both run in strict $O(\log N)$ time, while peeking the top incident is $O(1)$. Incidents are ranked by composite severity taking into account accuracy drop, drift magnitude, and blast radius.*
> 
> *When an incident occurs, our **Automated Retraining Engine** (`orchestrator.py`) allows 1-click remediation with a strict **4-Step Validation Gate**:*
> 1. *It collects recent sliding window observations and fits a candidate model to the drifted distribution.*
> 2. *It evaluates 4 validation criteria: Data sufficiency, Accuracy $\ge$ SLA target, Latency $\le$ SLA threshold, and positive $R^2$ score.*
> 3. *If validation passes, the candidate is promoted to production, the version is bumped (e.g. `v1.0.0` $\rightarrow$ `v1.1.0`), Hash Map baselines are refreshed, active Max-Heap alerts are resolved, and DAG node health resets to HEALTHY.*
> 
> *I will now pass to Ghanshyam to explain our Model Registry and Traffic Simulator."*

---

### 🎤 Slide 9: In-Memory Model Registry & Traffic Simulator
**Speaker: GHANSHYAM**
> *"Thank you, Sanskar. I will cover the **ModelRegistry** and our **Universal Traffic Simulation Engine**.*
> 
> *The **ModelRegistry** (`registry.py`) serves as our central in-memory Hash Map baseline store. It provides $O(1)$ constant-time lookup for model metadata, SLA thresholds, and empirical baseline distribution moments (mean, variance, min, max, and quantiles). It universally supports both **Classification models** (tracking Accuracy and F1) and **Regression models** (tracking MAE, RMSE, and $R^2$).*
> 
> *To enable comprehensive testing without external hardware, I built the **UniversalTrafficSimulator** (`traffic_simulator.py`). It runs a background streaming thread pushing realistic predictions with Gaussian noise into the EventQueue at 20 events per second. It features controlled covariate shift injection — allowing users to dynamically multiply any feature’s distribution by 3.5x or spike latency by +250ms with a single click.*
> 
> *Furthermore, our CSV upload parser automatically extracts numerical columns, fits reference models, registers baselines in HashMap, and builds dynamic DAG topologies on the fly.*
> 
> *I now hand over to Hari to present our session audit history, post-mortem generator, and user interface."*

---

### 🎤 Slide 10, 11 & 12: Session History, Post-Mortems & Live Demo
**Speaker: HARI**
> *"Thank you, Ghanshyam. I will present our **Testing & Observability Session History Drawer**, **Incident Post-Mortem Exporter**, and the front-end dashboard.*
> 
> *In production, auditability is essential. We implemented **ModelTestingHistory** (`history.py`), which maintains a thread-safe chronological record of all model registrations, live drift detections, retraining runs, and switches. New session snapshots are prepended in $O(1)$ time. With our **1-Click Historical Snapshot Replay**, clicking any card in the drawer immediately loads the exact DAG topology canvas, statistical indicators (KS/PSI), and blast radius captured during that test run.*
> 
> *Our **Incident Post-Mortem Generator** automatically exports a comprehensive Markdown report documenting the executive summary, primary culprit feature, candidate RCS confidence rankings, impacted downstream services, and remediation logs.*
> 
> *Finally, our web dashboard is built with clean Vanilla HTML5, CSS3, and an interactive Canvas 2D DAG renderer with pulsating node halos. All 17 unit tests in our Pytest suite pass with 100% success.*
> 
> *We are now ready for the live demonstration and panel questions."*

---

## 🎓 4. Expected Viva Questions & High-Scoring Defense Answers

### Q1 (For Aakash): Why did you choose Reverse-BFS over Dijkstra or DFS for Root Cause Analysis?
**High-Scoring Answer:**  
*"In our dependency DAG, all dependency relationships between upstream ETL pipelines, features, and model nodes are discrete unweighted links. Breadth-First Search (BFS) explores dependencies layer by layer in strictly optimal $O(V + E)$ time. Dijkstra would introduce unnecessary $O(E \log V)$ heap overhead for unweighted edges, while DFS can traverse deep into irrelevant non-critical branches. Reverse-BFS guarantees that we discover the closest upstream culprit feature and originating ingestion pipeline with shortest topological distance first."*

### Q2 (For Krishna): How does the Circular FIFO Queue prevent memory overflow during traffic spikes?
**High-Scoring Answer:**  
*"Our `EventQueue` allocates a fixed circular buffer of capacity $C = 5000$ using modulo pointer wrapping: `self.tail = (self.tail + 1) % self.capacity`. When the queue reaches capacity, new events overwrite the oldest unconsumed entry and increment a `dropped_events` counter. This ensures $O(1)$ constant-time ingestion while guaranteeing that memory usage never exceeds the pre-allocated buffer size."*

### Q3 (For Sanskar): Why is a Binary Max-Heap superior to an array or sorted list for incident management?
**High-Scoring Answer:**  
*"An unsorted array requires $O(N)$ linear time to search for the highest-severity alert, which is too slow in high-throughput systems. A sorted array requires $O(N)$ time on every new alert insertion. A Binary Max-Heap provides the optimal theoretical balance: $O(\log N)$ insertion via `_sift_up` and $O(\log N)$ extraction of the critical alert via `_sift_down`, while peeking the active top alert is instantaneous $O(1)$."*

### Q4 (For Ghanshyam): How does ModelRegistry achieve O(1) baseline retrieval, and how does it support multiple models?
**High-Scoring Answer:**  
*"ModelRegistry is backed by Python's in-memory Hash Map (dictionary) indexed by unique `model_id` strings. Each `ModelMetadata` record maintains an inner hash map `feature_baselines` mapping feature names to `EmpiricalBaseline` objects containing baseline sample arrays and statistical moments. Hash map bucket indexing provides $O(1)$ average-time retrieval regardless of how many models are registered in the platform."*

### Q5 (For Hari): How does the Session History Drawer capture and replay historical DAG snapshots?
**High-Scoring Answer:**  
*"When a drift incident, model switch, or retraining occurs, `ModelTestingHistory` captures a deep-copy snapshot of the graph adjacency list and node health states inside `TestSessionRecord.graph_snapshot`. When a user clicks a historical record in the UI, our frontend `GraphRenderer` reads that snapshot and replays the exact canvas topology and red-highlighted culprit nodes without needing to roll back active live production telemetry."*
