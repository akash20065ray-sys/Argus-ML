# Project Context & Persistent Memory: ArgusML

This file is automatically loaded into memory across all sessions in this workspace (`c:\DS_CP`).

## 🛡️ Project Identity & Overview
* **Project Name:** **ArgusML** (`argus-ml`)
* **Core Concept:** Universal Production AI Observability & Graph-Powered Root Cause Diagnostic Platform.
* **One-Line Pitch:** A system that continuously watches deployed ML models, detects real-world data and performance drift, identifies exact root causes via reverse DAG traversal, and alerts users via a Max-Heap before models fail.

---

## 🧬 Core DSA Architecture (5 Foundational Data Structures)
1. **Circular FIFO Queue (`EventQueue` - `backend/app/core/dsa/queue.py`):**
   * High-throughput asynchronous prediction ingestion buffer ($O(1)$ enqueue/dequeue).
2. **Double-Ended Queue (`MetricSlidingWindow` - `backend/app/core/dsa/deque.py`):**
   * Sliding window over recent predictions for $O(1)$ amortized rolling accuracy, precision, recall, and P99 latency.
3. **Hash Map (`ModelRegistry` - `backend/app/core/dsa/registry.py`):**
   * $O(1)$ constant-time lookup for model metadata, SLA thresholds, and empirical baseline distributions.
4. **Binary Max-Heap (`AlertMaxHeap` - `backend/app/core/dsa/heap.py`):**
   * Priority queue with pure `_sift_up` and `_sift_down` implementations for ranking incidents by composite severity.
5. **Directed Acyclic Graph (`DependencyGraph` - `backend/app/core/dsa/graph.py`):**
   * Dynamically constructs 4-layer topology: `Pipelines → Features → Model → Downstream Services`.
   * **Reverse-BFS ($O(V+E)$):** Upstream root-cause attribution to isolate culprit features.
   * **Forward-BFS ($O(V+E)$):** Downstream traversal to quantify service Blast Radius.

---

## 🚀 How to Run & Test
* **Run Backend Server:**
  ```bash
  python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
  ```
* **Open Dashboard:** Open `http://127.0.0.1:8000` in browser.
* **Run Unit Tests (All 12 Passed):**
  ```bash
  python -m pytest backend/tests/ -v
  ```
* **Test Custom External ML Model:**
  ```bash
  python examples/test_your_own_model.py
  ```

---

## 📂 Model Management & Clean Startup
* **Clean Default Startup:** The platform boots into a pristine, clean workspace state without any pre-loaded dummy sample models forced on the home page.
* **Custom Model Registration:** Supported via `POST /api/models/upload-csv` or `POST /api/models/register`, or via Python client script (`examples/test_your_own_model.py`).
* **Optional Demo Models:** Can be loaded on demand via `POST /api/models/load-samples` or clicking the "Load Optional Demo Showcase" button. Available demo templates:
  1. `customer_churn_v1` (Telecom Customer Churn - Classification)
  2. `fraud_detector_v1` (Financial Credit Card Fraud - Classification)
  3. `house_price_v1` (Real Estate Valuation - Regression)

---

## ⚡ Active Advanced Features (Phases 7 & 8)
* **Phase 7: 1-Click Automated Model Retraining Trigger:**
  * Re-fits model on sliding window + baseline data, computes recovered accuracy/R², updates HashMap baseline distributions, bumps version (`v1.0.0` &rarr; `v1.1.0`), resolves alerts in Max-Heap, and resets node health to `HEALTHY`.
* **Phase 8: Downloadable Markdown Incident Post-Mortem Report:**
  * Exports comprehensive incident post-mortem markdown report documenting root cause attribution, statistical drift indicators (KS/PSI), blast radius, and automated remediation logs.

---

## ⏳ Optional Future Extension
* **Phase 9:** Webhook notifications (Slack / Discord / PagerDuty / Email).
