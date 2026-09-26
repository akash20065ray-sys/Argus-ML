# 🛡️ ArgusML: Capstone Presentation & Team Defense Guide

This document contains the **complete 13-slide presentation structure**, **5-member module division**, **word-for-word speaking script**, **code/file ownership breakdown**, and **viva Q&A defense answers**.

Generated Artifacts in Downloads:
- **PowerPoint Presentation File:** `ArgusML_Presentation.pptx` (CrimsonOrbit High-Contrast Theme)
- **Official Team Script PDF Document:** `ArgusML_Team_Presentation_Script.pdf`
- **Team Viva Question Bank PDF Document:** `ArgusML_Team_Viva_Question_Bank.pdf`

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

## 📊 2. Slide Deck Outline (13 Slides - CrimsonOrbit Theme)

1. **Slide 1:** Title Slide & Project Overview
2. **Slide 2:** Problem Statement & Industry Motivation (The Silent ML Decay)
3. **Slide 3:** Literature Review & Theoretical Positioning (Academic Survey & Prior Art)
4. **Slide 4:** Proposed Solution & Core System Novelties
5. **Slide 5:** System Architecture & Master Telemetry Pipeline (5 Distinct Layer Cards)
6. **Slide 6:** Core DSA Mapping & Algorithmic Complexity Table
7. **Slide 7:** Technical Deep-Dive: Krishna (Circular FIFO Queue, Deque & Drift Analytics)
8. **Slide 8:** Technical Deep-Dive: Aakash (Dynamic 4-Layer DAG & Reverse-BFS RCA)
9. **Slide 9:** Technical Deep-Dive: Sanskar (Binary Max-Heap & 4-Step Retraining Gate)
10. **Slide 10:** Technical Deep-Dive: Ghanshyam (In-Memory Baseline Hash Map & Traffic Simulator)
11. **Slide 11:** Technical Deep-Dive: Hari (History Audit Drawer, Post-Mortems & Canvas Dashboard)
12. **Slide 12:** Team Division & Individual Module Ownership
13. **Slide 13:** Experimental Evaluation, Conclusion & Live Demonstration

---

## 🎙️ 3. Complete Word-for-Word Speaking Script

### 🎤 Slide 1: Title & Overview
**Speaker: AAKASH (Lead)**
> *"Respected professors and panel members, good morning. Today, our team is presenting **ArgusML** — a Universal Production AI Observability and Graph-Powered Root Cause Diagnostic Platform built entirely upon 5 foundational Data Structures and Algorithms.*
> 
> *Modern enterprises deploy hundreds of machine learning models to production, but managing their reliability remains an unsolved challenge. Our goal with ArgusML was to build a pure, in-memory watchdog engine capable of sub-millisecond telemetry, automated statistical drift detection, topological root cause attribution, and closed-loop self-healing without relying on heavy third-party vendor stacks.*
> 
> *Let us begin by examining the core problem that motivated this capstone project."*

---

### 🎤 Slide 2: Problem Statement & Industry Motivation
**Speaker: AAKASH (Lead)**
> *"Unlike traditional software services that crash with HTTP 500 errors when a bug occurs, machine learning models fail silently. As real-world customer behavior or sensor calibrations evolve, input distributions drift away from the training baseline. The model continues to output confident predictions, but its real-world accuracy silently collapses from 95% down to 65%.*
> 
> *When an accuracy drop is eventually discovered, data engineering teams face three severe bottlenecks:*
> 1. *Manual Root-Cause Isolation: Engineers take days manually inspecting upstream multi-table ETL pipelines to find which specific feature became corrupted.*
> 2. *SRE Alert Fatigue: Generic monitoring tools flood engineers with hundreds of uncorrelated metric alerts without composite severity prioritization.*
> 3. *Manual Retraining Hazards: Models are retrained manually without strict validation gates, often accidentally promoting regressed candidates to production.*
> 
> *Let us examine how academic literature and existing tools approach this problem."*

---

### 🎤 Slide 3: Literature Review & Theoretical Positioning
**Speaker: AAKASH (Lead)**
> *"In our literature survey, we analyzed classical distribution shift paradigms:*
> * *Covariate Shift, established by Shimodaira (2000), where input feature distributions $P(X)$ drift while conditional output relationships $P(Y|X)$ remain fixed.*
> * *Concept Drift, formalized by Widmer and Kubat (1996), where relationships $P(Y|X)$ change over time due to external real-world shocks.*
> 
> *We evaluated several statistical distance metrics, including Wasserstein Distance, KL Divergence, the 2-Sample Kolmogorov-Smirnov test, and Population Stability Index (PSI). We selected the KS-test and PSI because the KS-test provides a non-parametric empirical CDF distance with rigorous p-value thresholds in $O(N \log N)$ time, while PSI delivers robust quantile-binned stability measurements in $O(N + B)$ time.*
> 
> *When comparing ArgusML against existing tools like Evidently AI and Datadog APM, existing solutions are either offline batch profile generators or infrastructure-only monitors. ArgusML is novel because it introduces an entirely in-memory DSA architecture and is the first system to integrate statistical tests with 4-layer dependency DAG Reverse-BFS for automated upstream attribution.*
> 
> *Let us now look at the proposed ArgusML solution."*

---

### 🎤 Slide 4 & 5: Proposed Solution & System Architecture
**Speaker: AAKASH (Lead)**
> *"ArgusML introduces a 5-pillar in-memory architecture designed for microsecond telemetry and automated remediation:*
> 1. *A Pure In-Memory DSA Core executing in under 0.45 ms overhead.*
> 2. *A Real-Time Drift Watchdog running KS-test and PSI evaluations every 25 streaming events.*
> 3. *Topological Root Cause Attribution isolating corrupted features via Reverse-BFS.*
> 4. *A Priority Max-Heap Queue ranking incidents by composite mathematical severity.*
> 5. *A 4-Step Closed-Loop Retraining Validation Gate promoting recovered models with zero downtime.*
> 
> *As shown in our 5-layer System Architecture on Slide 5, live predictions flow seamlessly from the Ingestion Queue through the Metric Sliding Window, into the Statistical Drift Engine, across the Dynamic Dependency Graph, and finally into the Priority Alert Max-Heap.*
> 
> *I will now hand over to Krishna to present the DSA foundations and the Ingestion/Drift engine."*

---

### 🎤 Slide 6 & 7: Core DSA Mapping, Ingestion Buffer & Drift Analytics
**Speaker: KRISHNA**
> *"Thank you, Aakash. As shown on Slide 6, every ArgusML module maps directly to optimal theoretical complexity:*
> * *EventQueue operates in strict $O(1)$ time with fixed circular buffer memory.*
> * *MetricSlidingWindow provides amortized $O(1)$ compute across rolling windows.*
> * *ModelRegistry provides $O(1)$ average-time baseline and SLA lookups.*
> * *AlertMaxHeap guarantees $O(\log N)$ push and extraction bounds.*
> * *DependencyGraph traverses upstream and downstream topology in $O(V + E)$ linear time.*
> 
> *On Slide 7, I will explain the Ingestion and Drift modules:*
> * *When live predictions arrive at `POST /api/ingest`, our **Circular FIFO EventQueue** (`queue.py`) buffers events using modulo arithmetic: `tail = (tail + 1) % capacity`. It holds 5,000 events with zero memory allocation overflow.*
> * *Our **MetricSlidingWindow** (`deque.py`) maintains recent $W = 400$ inferences, continuously updating rolling accuracy, precision, recall, and P99 latency in amortized $O(1)$ time.*
> * *Every 25 events, our **DriftEngine** (`detector.py`) executes two statistical tests against baseline distributions: the 2-Sample Kolmogorov-Smirnov test ($D = \sup |F_{\text{base}}(x) - F_{\text{prod}}(x)|$, $p < 0.05$) and PSI across 10 quantile bins ($\text{PSI} \ge 0.25$ indicates critical drift).*
> 
> *Once drift is detected, Aakash's DAG engine triggers root cause attribution."*

---

### 🎤 Slide 8: Dynamic DAG & Root Cause Confidence Scoring (RCS)
**Speaker: AAKASH (Lead)**
> *"Thank you, Krishna. On Slide 8, I will explain our **Dynamic Dependency DAG** (`graph.py`) and the **Root Cause Confidence Scoring (RCS)** engine.*
> 
> *The graph dynamically builds a 4-layer topology:*  
> `Upstream Pipelines → Inferred Features → Active Model → Downstream Services`.*
> 
> *When model performance degrades, we execute two Breadth-First Search traversals in $O(V + E)$ time:*
> 1. ***Reverse-BFS Upstream Attribution:*** *Starting at the degraded Model node, we traverse reverse adjacency lists upstream to pinpoint the culprit drifting feature and its originating ETL ingestion source.*
> 2. ***Forward-BFS Downstream Blast Radius:*** *Starting from the model node, we traverse forward adjacency lists to compute the exact set of impacted downstream microservices and APIs.*
> 
> *To provide mathematical certainty, I formulated the **Root Cause Confidence Score (RCS)**:*  
> $\text{RCS} = (0.45 \times \text{DriftEvidence}) + (0.30 \times \text{AccuracyDrop}) + (0.15 \times \text{TopologyProximity}) + (0.10 \times \text{BlastImpact})$.  
> *This isolates the primary culprit feature with over 85% to 95% confidence.*
> 
> *I now invite Sanskar to explain the Priority Max-Heap and automated retraining."*

---

### 🎤 Slide 9: Incident Priority Max-Heap & 4-Step Retraining Gate
**Speaker: SANSKAR**
> *"Thank you, Aakash. On Slide 9, I will present our **AlertMaxHeap** (`heap.py`) and the **Closed-Loop Automated Retraining Pipeline** (`orchestrator.py`).*
> 
> *To prevent SRE alert fatigue in multi-model environments, we implemented a pure, array-backed **Binary Max-Heap** using custom `_sift_up` and `_sift_down` methods. Pushing new incidents and extracting the critical top incident both execute in strict $O(\log N)$ time, while peeking is $O(1)$. Incidents are prioritized by composite severity taking into account accuracy drop, drift magnitude, and blast radius.*
> 
> *When an incident requires remediation, our 1-Click Retraining Engine executes a **4-Step Validation Gate**:*
> 1. *Verifies observation sufficiency in the sliding window.*
> 2. *Re-fits model decision boundaries to the shifted distribution.*
> 3. *Validates candidate accuracy $\ge$ SLA target, latency $\le$ SLA threshold, and positive $R^2$.*
> 4. *Promotes the candidate to production with zero downtime, bumps the version (e.g. `v1.0.0` $\rightarrow$ `v1.1.0`), refreshes baseline distributions in HashMap, resolves Max-Heap alerts, and resets DAG node health to HEALTHY.*
> 
> *I now pass to Ghanshyam to cover the Model Registry and Traffic Simulator."*

---

### 🎤 Slide 10: In-Memory Baseline Registry & Traffic Simulator
**Speaker: GHANSHYAM**
> *"Thank you, Sanskar. On Slide 10, I will present the **ModelRegistry** (`registry.py`) and our **Universal Traffic Simulator** (`traffic_simulator.py`).*
> 
> *The **ModelRegistry** is our in-memory Hash Map baseline store, providing $O(1)$ constant-time lookup for model metadata, SLA thresholds, and empirical baseline distribution moments (mean, variance, min, max, and quantiles). It universally supports both **Classification** and **Regression** models.*
> 
> *To thoroughly validate the system under real-world conditions, I built the **UniversalTrafficSimulator**. It streams synthetic inference events into the EventQueue at 20 events per second with Gaussian distribution noise. It features an interactive Covariate Shift Injector — allowing users to scale any feature's distribution by 3.5x or spike latency by +250ms with a single click to trigger live drift.*
> 
> *Additionally, our CSV parser automatically extracts numerical columns, fits reference models, registers baselines in HashMap, and generates dynamic DAG topologies on the fly.*
> 
> *I now hand over to Hari to present session history, post-mortems, and our user interface."*

---

### 🎤 Slide 11: History Drawer, Post-Mortems & Canvas Dashboard
**Speaker: HARI**
> *"Thank you, Ghanshyam. On Slide 11, I will present our **ModelTestingHistory** (`history.py`), **Incident Post-Mortem Generator**, and the frontend dashboard.*
> 
> *In production environments, full auditability is critical. We built a thread-safe chronological session drawer that captures all model tests, drift alerts, registrations, and retraining runs with $O(1)$ prepend operations. With our **1-Click DAG Snapshot Replay**, clicking any card in the drawer immediately loads the exact historical DAG topology, statistical indicators (KS/PSI), and blast radius captured during that run.*
> 
> *Our **Post-Mortem Engine** automatically compiles and downloads a comprehensive Markdown post-mortem report documenting executive summaries, culprit feature rankings, and automated remediation logs.*
> 
> *Finally, our dashboard is built with clean Vanilla HTML5, CSS3, and an interactive Canvas 2D DAG renderer with pulsating node health halos.*
> 
> *I will now pass back to Aakash for the team breakdown and experimental conclusion."*

---

### 🎤 Slide 12 & 13: Team Contribution Breakdown, Evaluation & Live Demo
**Speaker: AAKASH (Lead)**
> *"On Slide 12, we summarize our team's module ownership and code contributions across the 5 core DSA components.*
> 
> *On Slide 13, we present our experimental evaluation results:*
> * *All 17 unit tests in our Pytest suite pass with 100% success across all DSA modules.*
> * *Telemetry compute overhead averages under 0.45 ms per prediction, preserving live API throughput.*
> * *Reverse-BFS RCA achieved 100% accuracy in isolating culprit features across simulated drift scenarios.*
> * *Automated retraining recovered model accuracy from 68% back to 96% with zero downtime.*
> 
> *We are now excited to demonstrate the live ArgusML platform running at `http://127.0.0.1:8000` and look forward to your questions."*

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
