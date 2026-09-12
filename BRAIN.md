# 🧠 ArgusML: System Brain & Technical Knowledge Base

> **Official Comprehensive Technical Specification & Engineering Reference**  
> *Project:* **ArgusML** (`argus-ml`)  
> *Corpus:* `akash20065ray-sys/Argus-ML`  
> *Workspace:* `c:\DS_CP`

---

## 📑 Table of Contents
1. [Executive Summary & Core Mission](#1-executive-summary--core-mission)
2. [Statistical & MLOps Theory](#2-statistical--mlops-theory)
3. [The 5-DSA Architectural Spine](#3-the-5-dsa-architectural-spine)
4. [Mathematical Formulations & Scoring Models](#4-mathematical-formulations--scoring-models)
5. [Graph-Powered Root Cause & Blast Radius Traversal](#5-graph-powered-root-cause--blast-radius-traversal)
6. [API Specifications & Data Contracts](#6-api-specifications--data-contracts)
7. [Automated Verification & Test Matrix](#7-automated-verification--test-matrix)
8. [Viva & Technical Interview Cheatsheet (Top 10 Q&A)](#8-viva--technical-interview-cheatsheet-top-10-qa)

---

## 1. Executive Summary & Core Mission

Machine learning models are static artifacts deployed into dynamic, non-stationary real-world environments. Over time, customer behavior shifts, macroeconomic factors fluctuate, and data pipelines corrupt feature distributions. This leads to **Silent Model Failure**—where the model outputs predictions without throwing runtime exceptions, but the predictions are statistically invalid and degrade business KPIs.

**ArgusML** solves this by providing:
1. **High-Throughput Asynchronous Ingestion:** Decoupled buffer for production prediction logging.
2. **Real-Time Rolling Telemetry:** Constant-time sliding window metric updates.
3. **Continuous Statistical Drift Watchdog:** Kolmogorov-Smirnov tests and Population Stability Index (PSI) benchmarking against training baselines.
4. **Graph-Powered Root Cause Analysis (RCA):** Reverse DAG traversal to isolate culprit features and corrupted upstream pipelines.
5. **Blast Radius Calculation:** Forward DAG traversal to quantify affected downstream microservices.
6. **Prioritized Incident Triage:** Max-Heap priority queue ensuring high-severity issues are addressed first.

```
       ┌───────────────────────────────────────────────────────────────┐
       │                  ARGUSML TELEMETRY PIPELINE                   │
       ├───────────────────────────────────────────────────────────────┤
       │ Ingestion ──► Sliding Window ──► Drift Engine ──► RCA Engine  │
       │  (Queue)         (Deque)           (HashMap)        (DAG)     │
       │                                                       │       │
       │                                                       ▼       │
       │ Visual Dashboard ◄─────────────────────────── Priority Queue  │
       │  (Canvas DAG)                                  (Max-Heap)     │
       └───────────────────────────────────────────────────────────────┘
```

---

## 2. Statistical & MLOps Theory

### 2.1 Types of Distribution Shifts
ArgusML detects three primary categories of production degradation:

1. **Covariate Shift ($P(X)$ changes, $P(Y|X)$ remains constant):**
   * The distribution of input features shifts (e.g., inflation increases transaction amounts), but the relationship between features and labels remains the same.
2. **Concept Drift ($P(Y|X)$ changes, $P(X)$ remains constant):**
   * The real-world definition of the target changes (e.g., fraudsters adopt new evasion techniques, making previously safe transaction patterns fraudulent).
3. **Prior Probability Shift ($P(Y)$ changes):**
   * The prevalence of positive labels shifts (e.g., economic crisis increasing default rates across all applicant tiers).

---

### 2.2 Statistical Drift Metrics Used in ArgusML

#### A. Two-Sample Kolmogorov-Smirnov (KS) Test
Used for **continuous numerical feature drift** (e.g., `monthly_charges`, `transaction_amount`, `square_feet`).

The KS statistic $D$ represents the maximum vertical divergence between the empirical cumulative distribution function (eCDF) of the baseline training distribution $F_{\text{base}}(x)$ and the production sliding window $F_{\text{prod}}(x)$:

$$D = \sup_{x} \left| F_{\text{base}}(x) - F_{\text{prod}}(x) \right|$$

* **Null Hypothesis ($H_0$):** Production data and baseline data are drawn from the identical continuous distribution.
* **Significance Level ($\alpha$):** $0.05$
* **Decision Rule:**
  $$\text{Drift Flagged} \iff p\text{-value} < 0.05 \quad \text{and} \quad D > 0.15$$

---

#### B. Population Stability Index (PSI)
Used to measure the overall shift between a reference population and a live production sample across $B$ empirical quantile bins (default $B = 10$):

$$\text{PSI} = \sum_{i=1}^{B} \left( \text{Actual}_i - \text{Expected}_i \right) \times \ln\left( \frac{\text{Actual}_i}{\text{Expected}_i} \right)$$

* Where:
  * $\text{Actual}_i$: Proportion of observations in bin $i$ from the live sliding window.
  * $\text{Expected}_i$: Proportion of observations in bin $i$ from the training baseline dataset.
  * A smoothing constant $\epsilon = 10^{-4}$ is added to prevent division by zero or $\ln(0)$.

| PSI Range | Severity Classification | Action Taken by ArgusML |
| :--- | :--- | :--- |
| $\text{PSI} < 0.10$ | **HEALTHY (Green)** | No significant distribution change. |
| $0.10 \le \text{PSI} < 0.25$ | **WARNING (Amber)** | Moderate shift; monitor closely. |
| $\text{PSI} \ge 0.25$ | **CRITICAL (Red)** | Significant distribution drift; triggers RCA & Max-Heap alert. |

---

## 3. The 5-DSA Architectural Spine

Every architectural component in ArgusML is paired with a specific Data Structure to guarantee optimal asymptotic time and space complexity:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           5-DSA ARCHITECTURAL MAPPING                                   │
├─────────────────────┬───────────────────┬───────────────────────────┬───────────────────┤
│ Component           │ Data Structure    │ Time Complexity           │ Space Complexity  │
├─────────────────────┼───────────────────┼───────────────────────────┼───────────────────┤
│ Ingestion Buffer    │ Circular FIFO     │ Enqueue: O(1)             │ O(Capacity)       │
│                     │ Queue             │ Dequeue: O(1)             │                   │
├─────────────────────┼───────────────────┼───────────────────────────┼───────────────────┤
│ Rolling Telemetry   │ Double-Ended      │ Append/Evict: O(1) amort. │ O(W × Features)   │
│                     │ Queue (Deque)     │ Rolling Acc: O(1)         │                   │
├─────────────────────┼───────────────────┼───────────────────────────┼───────────────────┤
│ Baseline Catalog    │ Hash Map (`dict`) │ Lookup: O(1)              │ O(Models × Feats) │
│                     │                   │ Store: O(1)               │                   │
├─────────────────────┼───────────────────┼───────────────────────────┼───────────────────┤
│ Alert Ranking       │ Binary Max-Heap   │ Push: O(log N)            │ O(N)              │
│                     │                   │ Pop Max: O(log N)         │                   │
│                     │                   │ Peek: O(1)                │                   │
├─────────────────────┼───────────────────┼───────────────────────────┼───────────────────┤
│ Dependency & RCA    │ Directed Acyclic  │ Reverse BFS: O(V + E)     │ O(V + E)          │
│                     │ Graph (DAG)       │ Forward BFS: O(V + E)     │                   │
└─────────────────────┴───────────────────┴───────────────────────────┴───────────────────┘
```

---

### Detailed Implementation Breakdown:

#### 1. `EventQueue` (`backend/app/core/dsa/queue.py`)
* **Underlying Structure:** Fixed-size array with `head` and `tail` pointers.
* **Thread-Safety:** Mutex locking with `threading.Condition` variable (`not_empty`).
* **Overflow Handling:** When full, oldest item is overwritten with an atomic drop counter increment, preserving the freshest telemetry without blocking inference producers.

#### 2. `MetricSlidingWindow` (`backend/app/core/dsa/deque.py`)
* **Underlying Structure:** `collections.deque` with `maxlen=W` (default $W=400$) paired with feature-specific sub-deques.
* **Rolling Metric Update Algorithm ($O(1)$ amortized):**
  * When adding event $E_{\text{new}}$ to a full window:
    1. Read and evict oldest record $E_{\text{old}} = \text{window}[0]$.
    2. Decrement corresponding confusion matrix counter ($TP, FP, TN, FN$) in $O(1)$.
    3. Append $E_{\text{new}}$ and increment corresponding counter in $O(1)$.
    4. Compute accuracy: $\text{Accuracy} = \frac{TP + TN}{TP + FP + TN + FN}$ in $O(1)$.

#### 3. `ModelRegistry` (`backend/app/core/dsa/registry.py`)
* **Underlying Structure:** Hash Map (`Dict[str, ModelMetadata]`).
* **Baseline Extraction:** Automatically computes 5-point percentiles ($P_{10}, P_{25}, P_{50}, P_{75}, P_{90}$), mean, variance, and 600 reference samples per feature upon model registration.

#### 4. `AlertMaxHeap` (`backend/app/core/dsa/heap.py`)
* **Underlying Structure:** Array-backed complete binary tree satisfying parent dominance invariant:
  $$\text{Heap}[\text{parent}(i)].\text{priority} \ge \text{Heap}[i].\text{priority}, \quad \forall i > 0$$
* **Index Arithmetic:**
  * $\text{parent}(i) = \lfloor \frac{i - 1}{2} \rfloor$
  * $\text{left\_child}(i) = 2i + 1$
  * $\text{right\_child}(i) = 2i + 2$
* **Custom Heap Operations:** Pure `_sift_up(i)` and `_sift_down(i)` routines with an index lookup map `Dict[alert_id, int]` enabling $O(1)$ alert existence checks.

#### 5. `DependencyGraph` (`backend/app/core/dsa/graph.py`)
* **Underlying Structure:** Adjacency list using double HashMaps:
  * `forward_adj: Dict[str, List[GraphEdge]]` ($u \to v$)
  * `reverse_adj: Dict[str, List[GraphEdge]]` ($v \gets u$)
* **Topology Schema:**
  $$\text{Layer 1: Pipeline} \longrightarrow \text{Layer 2: Feature} \longrightarrow \text{Layer 3: Model} \longrightarrow \text{Layer 4: Service}$$

---

## 4. Mathematical Formulations & Scoring Models

### 4.1 Composite Severity & Heap Priority Score
When a model anomaly or drift is evaluated, ArgusML calculates a **Composite Severity Score** ($S \in [10, 100]$) to determine its priority key in the `AlertMaxHeap`:

$$S = \min\left(100.0, \; \max\left(10.0, \; (w_{\text{acc}} \cdot \Delta\text{Accuracy} \cdot 100) + (w_{\text{drift}} \cdot \text{CulpritScore}) + (w_{\text{blast}} \cdot N_{\text{downstream}})\right)\right)$$

* **Weights:**
  * $w_{\text{acc}} = 0.50$ (Accuracy drop penalty)
  * $w_{\text{drift}} = 0.30$ (Statistical feature drift magnitude)
  * $w_{\text{blast}} = 4.0$ (Downstream service impact multiplier)
* **Where:**
  $$\Delta\text{Accuracy} = \max(0, \; \text{SLA}_{\text{min\_accuracy}} - \text{Accuracy}_{\text{current}})$$
  $$\text{CulpritScore} = (D_{\text{KS}} \times 50.0) + (\min(\text{PSI}, 1.0) \times 50.0)$$
  $$N_{\text{downstream}} = \min(5, \; |\text{BlastRadius}|)$$

### 4.2 Severity Classification Tier
$$\text{Tier} = \begin{cases} 
\text{CRITICAL} & \text{if } S \ge 75.0 \text{ or } \text{Accuracy} < 0.80 \\
\text{HIGH} & \text{if } 50.0 \le S < 75.0 \text{ or } \Delta\text{Accuracy} > 0 \\
\text{MEDIUM} & \text{if } 30.0 \le S < 50.0 \\
\text{LOW} & \text{otherwise}
\end{cases}$$

---

## 5. Graph-Powered Root Cause & Blast Radius Traversal

```
   [Upstream Data Pipelines]
        │
        ▼ (EXTRACTS)
   [Feature Nodes (1...K)]  ◄─── Reverse-BFS finds drifting feature (Root Cause)
        │
        ▼ (FEEDS)
   [Active Model Node]      ◄─── Degradation Trigger
        │
        ▼ (CONSUMES)
   [Downstream Services]    ◄─── Forward-BFS finds impacted systems (Blast Radius)
```

### 5.1 Root Cause Attribution (Reverse-BFS Algorithm)
When model $M$ suffers an SLA drop or drift trigger:
1. Initialize queue $Q = [M]$, $\text{visited} = \{M\}$, $\text{candidates} = []$.
2. While $Q$ is not empty:
   * Pop node $u = Q.\text{popleft}()$.
   * For each incoming edge $(v, u) \in \text{reverse\_adj}[u]$:
     * If $v \notin \text{visited}$:
       * Mark $v$ as visited and push to $Q$.
       * If $v.\text{type} == \text{"FEATURE"}$, add $v$ to $\text{candidates}$.
3. For each candidate feature in $\text{candidates}$:
   * Query `DriftEngine` evaluation results ($D_{\text{KS}}, p\text{-val}, \text{PSI}$).
   * Rank features descending by $\text{Score} = D_{\text{KS}} + \text{PSI}$.
   * The feature with $\max(\text{Score})$ is isolated as the **Primary Culprit Feature**.
4. Traverse one step further in `reverse_adj` from the Culprit Feature to identify the feeding **Upstream Data Ingestion Pipeline**.

### 5.2 Blast Radius Calculation (Forward-BFS Algorithm)
1. Initialize queue $Q = [M]$, $\text{visited} = \{M\}$, $\text{impacted} = []$.
2. While $Q$ is not empty:
   * Pop node $u = Q.\text{popleft}()$.
   * For each outgoing edge $(u, v) \in \text{forward\_adj}[u]$:
     * If $v \notin \text{visited}$:
       * Mark $v$ as visited and push to $Q$.
       * If $v.\text{type} == \text{"SERVICE"}$, add $v.\text{name}$ to $\text{impacted}$.
3. Return list $\text{impacted}$ as the **Downstream Blast Radius**.

---

## 6. API Specifications & Data Contracts

### Core REST Endpoints

| Endpoint | Method | Payload / Params | Response | Description |
| :--- | :--- | :--- | :--- | :--- |
| `/api/dashboard` | `GET` | None | JSON telemetry bundle | Aggregated rolling metrics, DAG topology, drift table, and top Max-Heap alerts. |
| `/api/models` | `GET` | None | List of model objects | Catalog of registered models in HashMap. |
| `/api/models/select` | `POST` | `{"model_id": "customer_churn_v1"}` | `{"status": "SUCCESS"}` | Switches active model and dynamically rebuilds DAG. |
| `/api/models/upload-csv`| `POST` | `multipart/form-data` (file, metadata) | Registered model JSON | Uploads any CSV dataset, extracts baselines, and builds dynamic DAG. |
| `/api/models/register` | `POST` | JSON dataset & schema | Registered model JSON | Programmatically registers custom model & baselines. |
| `/api/ingest` | `POST` | `{"model_id": "...", "features": {...}, "prediction": 1}` | `{"enqueued": true}` | Enqueues live inference record into `EventQueue`. |
| `/api/simulate/drift-feature` | `POST` | `{"feature_name": "monthly_charges", "multiplier": 3.5}` | `{"status": "SUCCESS"}` | Injects dynamic covariate shift into specified feature. |
| `/api/simulate/reset` | `POST` | None | `{"status": "SUCCESS"}` | Resets sliding window, alerts, and node healths to baseline. |
| `/api/alerts/{id}/resolve` | `POST` | Alert ID path param | `{"success": true}` | Resolves and clears alert from Max-Heap. |

---

## 7. Automated Verification & Test Matrix

All test cases are located in `backend/tests/` and run via `pytest`:

```
============================= test session starts =============================
backend/tests/test_drift_rca.py::test_ks_test_and_psi_detection           PASSED [ 10%]
backend/tests/test_drift_rca.py::test_rca_engine_pinpoints_culprit_feature  PASSED [ 20%]
backend/tests/test_dsa.py::test_event_queue_fifo_and_overflow             PASSED [ 30%]
backend/tests/test_dsa.py::test_metric_sliding_window_accuracy_and_latency PASSED [ 40%]
backend/tests/test_dsa.py::test_alert_max_heap_priority_order             PASSED [ 50%]
backend/tests/test_dsa.py::test_dependency_graph_reverse_and_forward_traversal PASSED [ 60%]
backend/tests/test_universal_models.py::test_clean_default_startup        PASSED [ 70%]
backend/tests/test_universal_models.py::test_load_sample_models_on_demand PASSED [ 80%]
backend/tests/test_universal_models.py::test_switch_model_rebuilds_dag    PASSED [ 90%]
backend/tests/test_universal_models.py::test_register_any_custom_model_from_dataset PASSED [100%]
============================= 10 passed in 2.15s ==============================
```

---

## 8. Viva & Technical Interview Cheatsheet (Top 10 Q&A)

### Q1: Why did you use a Circular Queue instead of Python’s built-in `list` for event ingestion?
> **Answer:** Appending and popping from the beginning of a standard Python list takes $O(N)$ time because all subsequent elements must be shifted in memory. A Circular Queue uses modular arithmetic (`(head + 1) % capacity`) with fixed pointers, guaranteeing true $O(1)$ constant time for both enqueue and dequeue operations while bounding memory usage.

### Q2: How does your Deque calculate rolling accuracy in $O(1)$ amortized time?
> **Answer:** Instead of re-iterating over the entire window of size $W$ on every new prediction ($O(W)$), we maintain rolling counters for True Positives, False Positives, True Negatives, and False Negatives. When an element is evicted from the left, its contribution is subtracted in $O(1)$, and the new incoming record is added in $O(1)$.

### Q3: What is the difference between the KS-test and PSI in your drift engine?
> **Answer:** The Kolmogorov-Smirnov test is a non-parametric statistical hypothesis test that compares continuous empirical cumulative distribution functions and returns a rigorous $p$-value. Population Stability Index (PSI) is an information-theoretic metric that discretizes populations into quantile bins to measure population shift magnitude ($\sum (A_i - E_i) \ln(A_i / E_i)$). ArgusML combines both for robust drift attribution.

### Q4: Why is the Dependency Topology modeled as a DAG rather than an undirected graph?
> **Answer:** Dependencies in production systems have a strict directional causal flow: `Data Sources extract into Features → Features feed Models → Models authorize Downstream Services`. A Directed Acyclic Graph (DAG) prevents cyclic loops and enables Topological Sorting (Kahn’s algorithm) and distinct upstream (Root Cause) and downstream (Blast Radius) traversals.

### Q5: How does Reverse-BFS find the root cause?
> **Answer:** When an active model flags a performance violation, Reverse-BFS traverses incoming edges from the Model node backwards to all connected Feature nodes in $O(V + E)$ time. It then evaluates the statistical drift score ($D_{\text{KS}} + \text{PSI}$) of each connected feature to pinpoint the primary driver of error.

### Q6: What is Blast Radius?
> **Answer:** Blast Radius represents the downstream cascade of microservices, APIs, and business applications that depend on the degrading model's output (e.g., `Checkout API`, `Instant Wire Transfer Service`). ArgusML calculates this via Forward-BFS starting from the degraded model node.

### Q7: Why use a Max-Heap for alert management?
> **Answer:** In high-traffic production systems with dozens of models, alert fatigue is a critical problem. A Max-Heap dynamically ranks incidents by their composite severity score in $O(\log N)$ insert/extract time, ensuring that on-call engineers are always presented with the highest blast-radius failure at the top of the stack ($O(1)$ peek).

### Q8: Is ArgusML tied to any specific dataset or domain?
> **Answer:** No. ArgusML is completely domain-agnostic and universal. It supports both Classification and Regression tasks across arbitrary feature sets. Users can upload any CSV dataset or connect external models via our REST API.

### Q9: What happens when you upload a new CSV dataset?
> **Answer:** The platform dynamically parses the columns, trains or fits a reference model, computes empirical 5-point quantiles and reference histograms for all numerical features in the HashMap store, dynamically constructs the 4-layer DAG topology, and initiates live monitoring.

### Q10: What are the primary system bottlenecks and how does ArgusML mitigate them?
> **Answer:** The primary bottleneck in real-time observability is analytical compute overhead during high-frequency ingestion. ArgusML mitigates this by decoupling HTTP ingestion (`EventQueue` circular buffer) from batch analytical workers (`MetricSlidingWindow` and periodic 25-event drift evaluation intervals).
