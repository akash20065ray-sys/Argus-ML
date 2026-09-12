# 🛡️ ArgusML: Universal Production AI Observability & Root-Cause Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![DSA Core](https://img.shields.io/badge/DSA-Queue%20%7C%20Deque%20%7C%20HashMap%20%7C%20Heap%20%7C%20DAG-FF6B6B)]()
[![Tests](https://img.shields.io/badge/Tests-10%2F10%20Passing-00F2A9)]()
[![Architecture](https://img.shields.io/badge/Architecture-Universal%20MLOps-8E2DE2)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **ArgusML** is an all-in-one, domain-agnostic production AI Observability and automated Root-Cause Diagnostic Platform. Powered by five foundational Data Structures & Algorithms (DSA), it continuously monitors deployed machine learning models, detects real-world feature and performance drift in real time, isolates culprit features via reverse DAG traversal, and prioritizes critical failures in a Max-Heap before models cause business harm.

---

## 📑 Master Table of Contents
1. [Platform Overview & Core Concept](#-platform-overview--core-concept)
2. [Unified System Architecture](#-unified-system-architecture)
3. [The 5-DSA Algorithmic Spine & Complexity Analysis](#-the-5-dsa-algorithmic-spine--complexity-analysis)
4. [Statistical Drift Detection Engine (KS-Test & PSI)](#-statistical-drift-detection-engine-ks-test--psi)
5. [Graph-Powered Root Cause Analysis (RCA) & Blast Radius](#-graph-powered-root-cause-analysis-rca--blast-radius)
6. [Universal & Model-Agnostic Ingestion](#-universal--model-agnostic-ingestion)
7. [Full-Stack Glassmorphic Dashboard](#-full-stack-glassmorphic-dashboard)
8. [Quick Start & Step-by-Step Execution](#-quick-start--step-by-step-execution)
9. [Automated Verification & Unit Test Suite](#-automated-verification--unit-test-suite)
10. [Repository File Structure](#-repository-file-structure)

---

## 🌟 Platform Overview & Core Concept

When Machine Learning models are deployed in production, real-world data distributions change dynamically due to macroeconomic shifts, seasonal behaviors, or corrupted upstream data pipelines. This leads to **Silent Model Degradation**—where inference endpoints continue returning HTTP 200 responses, but predictions become inaccurate and dangerous.

```
       TRADITIONAL MONITORING                        ARGUSML ALL-IN-ONE OBSERVABILITY
  ┌───────────────────────────────┐            ┌───────────────────────────────────────────────┐
  │ "Your model accuracy dropped" │    VS      │ 1. Identifies EXACT drifting feature (Amount) │
  │ (Vague, no cause, no triage)  │            │ 2. Pinpoints corrupted ETL Pipeline           │
  │                               │            │ 3. Traces affected Downstream Microservices   │
  │                               │            │ 4. Ranks incident in Max-Heap Priority Queue  │
  └───────────────────────────────┘            └───────────────────────────────────────────────┘
```

---

## 🏗️ Unified System Architecture

ArgusML organizes the full telemetry lifecycle into an all-in-one decoupled streaming pipeline:

```
                          PRODUCTION PREDICTION STREAM (REST / SDK)
                                             │
                                             ▼
             ┌───────────────────────────────────────────────────────────────┐
             │ Layer 1: Ingestion Buffer (DSA: Circular FIFO Queue)          │
             │ - O(1) Enqueue/Dequeue ring buffer                            │
             │ - Thread-safe mutex lock with condition variable              │
             │ - Decouples inference HTTP requests from analytical workers   │
             └───────────────────────────────┬───────────────────────────────┘
                                             │ Asynchronous Worker
                                             ▼
             ┌───────────────────────────────────────────────────────────────┐
             │ Layer 2: Sliding-Window Telemetry (DSA: Deque)                │
             │ - O(1) Amortized rolling accuracy, precision, recall, and F1 │
             │ - Rolling P50, P95, P99 latency percentiles                   │
             │ - Sliding window over last W predictions (default W=400)      │
             └───────────────────────────────┬───────────────────────────────┘
                                             │ Periodic Evaluation (Every 25 Events)
                                             ▼
             ┌───────────────────────────────────────────────────────────────┐
             │ Layer 3: Statistical Drift Watchdog (DSA: Hash Map)           │
             │ - O(1) Baseline empirical distribution retrieval              │
             │ - Two-Sample Kolmogorov-Smirnov (KS-Test: D-stat, p-value)   │
             │ - Population Stability Index (PSI with 10 empirical bins)     │
             └───────────────────────────────┬───────────────────────────────┘
                                             │ Anomaly / Drift Flagged
                                             ▼
             ┌───────────────────────────────────────────────────────────────┐
             │ Layer 4: Root-Cause & Blast Radius (DSA: Dependency DAG)      │
             │ - 4-Layer Dynamic Topology: Pipelines -> Feats -> Model -> Srv│
             │ - Reverse-BFS O(V+E): Upstream culprit feature attribution    │
             │ - Forward-BFS O(V+E): Downstream service blast radius         │
             └───────────────────────────────┬───────────────────────────────┘
                                             │ Composite Severity Score
                                             ▼
             ┌───────────────────────────────────────────────────────────────┐
             │ Layer 5: Priority Incident Queue (DSA: Binary Max-Heap)       │
             │ - O(log N) Priority queue ranking active incidents            │
             │ - Sifts highest-priority business risk to root of heap        │
             └───────────────────────────────┬───────────────────────────────┘
                                             ▼
                        INTERACTIVE GLASSMORPHIC DASHBOARD
                (Canvas DAG Renderer, Live KPIs, RCA Diagnostic Modal)
```

---

## 🧬 The 5-DSA Algorithmic Spine & Complexity Analysis

ArgusML’s performance is grounded in 5 classical Data Structures, each rigorously chosen to eliminate performance bottlenecks:

| Component | Data Structure | Time Complexity | Space Complexity | Real-World Engineering Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **`EventQueue`** | Circular FIFO Buffer | Enqueue: $O(1)$<br>Dequeue: $O(1)$ | $O(\text{Capacity})$ | Thread-safe ring buffer preventing backpressure during inference traffic spikes. |
| **`MetricSlidingWindow`** | Double-Ended Queue (Deque) | Append/Evict: $O(1)$ amort.<br>Accuracy Lookup: $O(1)$ | $O(W \times K)$ | Computes rolling metrics over window $W$ in $O(1)$ amortized time by updating confusion counters. |
| **`ModelRegistry`** | Hash Map (`dict`) | Get: $O(1)$<br>Put: $O(1)$ | $O(M \times K)$ | Constant-time access to model metadata, SLA thresholds, and empirical baseline distributions. |
| **`AlertMaxHeap`** | Binary Max-Heap | Push: $O(\log N)$<br>Pop Max: $O(\log N)$<br>Peek: $O(1)$ | $O(N)$ | Custom sift-up/down heap prioritizing active incidents by severity score to prevent alert fatigue. |
| **`DependencyGraph`** | Adjacency List (DAG) | Reverse BFS: $O(V + E)$<br>Forward BFS: $O(V + E)$ | $O(V + E)$ | Models architectural topology for upstream root-cause diagnosis and downstream blast-radius impact. |

---

## 📊 Statistical Drift Detection Engine (KS-Test & PSI)

### 1. Two-Sample Kolmogorov-Smirnov (KS) Test
Evaluates whether the continuous feature distribution in the live sliding window $F_{\text{prod}}(x)$ has drifted from the training baseline distribution $F_{\text{base}}(x)$:

$$D = \sup_{x} \left| F_{\text{base}}(x) - F_{\text{prod}}(x) \right|$$

$$\text{Drift Flagged} \iff p\text{-value} < 0.05 \quad \text{and} \quad D > 0.15$$

### 2. Population Stability Index (PSI)
Measures population shift across $B=10$ empirical quantile bins:

$$\text{PSI} = \sum_{i=1}^{B} \left( \text{Actual}_i - \text{Expected}_i \right) \times \ln\left( \frac{\text{Actual}_i}{\text{Expected}_i} \right)$$

* $\text{PSI} < 0.10$: **Stable (Healthy)**
* $0.10 \le \text{PSI} < 0.25$: **Moderate Drift (Warning)**
* $\text{PSI} \ge 0.25$: **Significant Shift (Critical Alert)**

---

## 🌐 Graph-Powered Root Cause Analysis (RCA) & Blast Radius

ArgusML dynamically constructs a 4-layer Directed Acyclic Graph (DAG) for every model:

```
  [Data Pipeline] ──(EXTRACTS)──► [Feature Nodes] ──(FEEDS)──► [Model Node] ──(CONSUMES)──► [Downstream Services]
                                         ▲                            │
                                         │                            ▼
                             Reverse-BFS: Root Cause       Forward-BFS: Blast Radius
```

1. **Reverse-BFS (Root Cause Attribution):**
   * Crawls incoming edges backwards from the degraded Model node to its constituent Feature nodes in $O(V+E)$ time.
   * Ranks features by statistical drift magnitude ($\text{Score} = D_{\text{KS}} + \text{PSI}$) to pinpoint the **Culprit Feature** and the upstream pipeline feeding it.
2. **Forward-BFS (Blast Radius Calculation):**
   * Traverses outgoing edges forward from the Model node to discover all affected downstream APIs and microservices (e.g., `Checkout API`, `Instant Wire Transfer Service`).
3. **Composite Severity Formulation:**
   $$\text{Severity Score} = \min\left(100.0, \; (0.50 \cdot \Delta\text{Accuracy} \cdot 100) + (0.30 \cdot \text{DriftScore}) + (4.0 \cdot N_{\text{downstream}})\right)$$

---

## 🚀 Universal & Model-Agnostic Ingestion

ArgusML is **100% domain-agnostic** and supports **ANY** Classification or Regression model:

* **3 Built-in Reference Models:**
  1. *Telecom Customer Churn Predictor* (`customer_churn_v1` — Classification)
  2. *Credit Card Fraud Classifier* (`fraud_detector_v1` — Classification)
  3. *Property Price Valuation Engine* (`house_price_v1` — **Regression**)
* **Bring-Your-Own-Data (CSV Upload):**
  * Upload any custom CSV file via the dashboard or `POST /api/models/upload-csv`.
  * ArgusML automatically infers columns, extracts baselines into the **HashMap**, trains a reference classifier/regressor, and builds the dynamic **DAG**.
* **Direct Python SDK Ingestion:**
  * Log predictions directly from external code, Jupyter Notebooks, or cloud endpoints using `examples/test_your_own_model.py`.

---

## 🖥️ Full-Stack Glassmorphic Dashboard

The platform serves a modern dark-mode web application from `http://127.0.0.1:8000`:

* **Live Telemetry Strip:** Real-time rolling Accuracy, P99 Latency, Active Drift Status, and Circular Queue Utilization.
* **Interactive HTML5 Canvas DAG Visualizer:** Real-time animated nodes with health glows (**Green** = Healthy, **Amber** = Warning, **Pulsing Crimson** = Critical Failure).
* **Dynamic Feature Drift Injector:** Auto-generates 1-click chaos injection buttons for *each feature of the active model*.
* **Max-Heap Incident Queue:** Real-time priority alert stack with 1-click **Root-Cause Diagnostic Modal** displaying culprit metrics and remediation action plans.

---

## ⚡ Quick Start & Step-by-Step Execution

### 1. Prerequisites
* Python 3.10 or higher
* Modern web browser (Chrome, Edge, Firefox, Brave)

### 2. Run Automated Unit Tests (10/10 Passing)
```bash
python -m pytest backend/tests/ -v
```

### 3. Launch the Platform
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
Open [**`http://127.0.0.1:8000`**](http://127.0.0.1:8000) in your browser.

### 4. Test with Your Own Python Model
In a separate terminal, run:
```bash
python examples/test_your_own_model.py
```
Watch ArgusML register the new model, stream live inferences, inject macroeconomic drift, and pop a critical alert in the Max-Heap!

---

## 🧪 Automated Verification & Unit Test Suite

All 10 unit tests in `backend/tests/` validate algorithmic invariants and drift mechanics:

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

## 📂 Repository File Structure

```
c:/DS_CP/
├── backend/
│   ├── app/
│   │   ├── api/                     # REST API routing layer
│   │   ├── core/
│   │   │   ├── dsa/                 # 5 Foundational Data Structure implementations
│   │   │   │   ├── queue.py         # Circular FIFO EventQueue
│   │   │   │   ├── deque.py         # MetricSlidingWindow
│   │   │   │   ├── heap.py          # AlertMaxHeap Priority Queue
│   │   │   │   ├── graph.py         # Dynamic Dependency DAG
│   │   │   │   └── registry.py      # HashMap Model Registry
│   │   │   ├── drift/
│   │   │   │   └── detector.py      # Two-Sample KS-Test & PSI Drift Engine
│   │   │   ├── rca/
│   │   │   │   └── engine.py        # Automated Root-Cause Diagnostic Engine
│   │   │   ├── simulator/
│   │   │   │   ├── universal_runner.py   # Multi-model host (Classification/Regression)
│   │   │   │   └── traffic_simulator.py  # Live prediction & chaos streaming simulator
│   │   │   └── orchestrator.py      # Central ArgusSystem Coordinator
│   │   └── main.py                  # FastAPI Application Entrypoint
│   └── tests/                       # Pytest Automated Test Suite
│       ├── test_dsa.py              # DSA unit tests
│       ├── test_drift_rca.py        # Drift & RCA unit tests
│       └── test_universal_models.py # Multi-model & clean startup unit tests
├── examples/
│   └── test_your_own_model.py       # Python Client SDK demo for external models
├── frontend/                        # Glassmorphic Dark Dashboard
│   ├── css/style.css                # Vanilla CSS design tokens & animations
│   ├── js/
│   │   ├── app.js                   # Client state controller & polling
│   │   └── graph_renderer.js        # Canvas DAG Topology Visualizer
│   └── index.html                   # Master Dashboard Single Page Application
├── BRAIN.md                         # Complete Technical Specification & Viva Q&A Cheatsheet
├── GEMINI.md                        # Persistent workspace memory file
├── README.md                        # All-in-One Master Platform Overview
└── .gitignore                       # Clean repository exclusions
```

---

## 📄 License
MIT License. Built as an Enterprise-Grade Production AI Observability & Graph-Powered Root Cause Diagnostic Platform.
