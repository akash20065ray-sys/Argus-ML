# 🛡️ ArgusML: Universal AI Observability & Root-Cause Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com)
[![DSA](https://img.shields.io/badge/DSA-Graph%20%7C%20Heap%20%7C%20Deque%20%7C%20Queue%20%7C%20HashMap-orange.svg)]()
[![Tests](https://img.shields.io/badge/Tests-9%20Passing-brightgreen.svg)]()

> **ArgusML** is a domain-agnostic, universal AI Observability and automated Root-Cause Diagnostic Platform. It can monitor, detect statistical data drift, and perform root-cause attribution for **ANY Machine Learning model** (Classification or Regression) across arbitrary industries, feature sets, and datasets.

---

## 🌟 Universal Capabilities

* **Domain & Model Agnostic:** Not hardcoded to any single problem. Supports Customer Churn, Financial Risk, House Price Regression, Medical Diagnostics, or custom user datasets.
* **Dynamic 4-Layer DAG Topology:** On model registration, ArgusML automatically constructs the dependency graph in $O(V + E)$ time:
  $$\text{Upstream Data Pipelines} \longrightarrow \text{Feature}_1, \dots, \text{Feature}_K \longrightarrow \text{Your Model} \longrightarrow \text{Downstream Consumer Services}$$
* **Automated Baseline Extraction:** Computes statistical distributions (mean, variance, 5-point quantiles, empirical reference sample) for all columns into a constant-time $O(1)$ **HashMap Registry**.
* **Model-Agnostic Root-Cause Analysis (RCA):** Reverse-BFS dynamically crawls upstream to pinpoint *which specific feature* drifted, while Forward-BFS determines the affected microservice **Blast Radius**.
* **One-Click CSV Model Registration:** Users can upload any custom CSV dataset from the dashboard to train, baseline, and start real-time monitoring instantly.

---

## 🧬 DSA System Architecture & Complexity Analysis

```
       UNIVERSAL PRODUCTION PREDICTION STREAM
                         │
                         ▼
       ┌──────────────────────────────────┐
       │     EventQueue (FIFO Queue)      │  <-- O(1) Circular Buffer (Decouples Ingestion from Analysis)
       └─────────────────┬────────────────┘
                         ▼
       ┌──────────────────────────────────┐
       │   MetricSlidingWindow (Deque)    │  <-- O(1) Amortized Rolling Performance & Latency Telemetry
       └─────────────────┬────────────────┘
                         ▼
       ┌──────────────────────────────────┐
       │     DriftEngine (HashMap)        │  <-- O(1) Baseline Distribution Lookups + 2-Sample KS-Test & PSI
       └─────────────────┬────────────────┘
                         ▼
       ┌──────────────────────────────────┐
       │    DependencyGraph (Dynamic DAG) │  <-- Reverse-BFS O(V+E) for Root Cause; Forward-BFS O(V+E) for Blast Radius
       └─────────────────┬────────────────┘
                         ▼
       ┌──────────────────────────────────┐
       │       AlertMaxHeap (Heap)        │  <-- O(log N) Priority Queue for Real-Time Incident Ranking
       └─────────────────┬────────────────┘
                         ▼
             GLASSERPHIC WEB DASHBOARD
```

| Component | Data Structure | Time Complexity | Real-World Engineering Purpose |
| :--- | :--- | :--- | :--- |
| **Ingestion Buffer** | **Circular FIFO Queue** (`EventQueue`) | Enqueue: $O(1)$<br>Dequeue: $O(1)$ | Prevents system backpressure during high-throughput inference surges. |
| **Rolling Telemetry** | **Double-Ended Queue** (`MetricSlidingWindow`) | Append/Evict: $O(1)$ amortized<br>Metrics: $O(1)$ | Computes rolling accuracy, precision, recall, and P99 latency over window $W$. |
| **Baseline Registry** | **Hash Map** (`ModelRegistry`) | Lookup: $O(1)$<br>Store: $O(1)$ | Stores empirical distribution quantiles and baseline training histograms for any model. |
| **Incident Priority** | **Max-Heap** (`AlertMaxHeap`) | Push: $O(\log N)$<br>Pop Max: $O(\log N)$<br>Peek: $O(1)$ | Ensures on-call teams always tackle the highest blast-radius issue first. |
| **Root-Cause / Blast** | **Directed Graph (DAG)** (`DependencyGraph`) | Reverse BFS: $O(V + E)$<br>Forward BFS: $O(V + E)$ | Maps Pipelines $\to$ Features $\to$ Models $\to$ Microservices for full-chain attribution. |

---

## 🚀 Quick Start Guide

### 1. Requirements
* Python 3.10+
* Web browser (Chrome, Edge, Firefox, Brave)

### 2. Run Automated Unit Tests (All 9 Passed)
```bash
python -m pytest backend/tests/ -v
```

### 3. Launch Platform
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
Then open: **`http://127.0.0.1:8000`** in your browser.

---

## 🧪 Out-of-the-Box Models Ready for Testing

1. **Telecom Customer Churn Predictor (`customer_churn_v1`):**
   * Features: `tenure_months`, `monthly_charges`, `support_tickets_30d`, `data_usage_gb`, `contract_type_code`
   * Blast Radius: `Retention Campaign Engine`, `CRM Notification Hub`, `Customer Success Portal`
2. **Credit Card Fraud Classifier (`fraud_detector_v1`):**
   * Features: `transaction_amount`, `foreign_ip_ratio`, `velocity_24h`, `device_trust_score`, `hour_of_day`
   * Blast Radius: `Checkout API`, `Instant Wire Transfer`, `Fraud Operations Review`
3. **Property Price Valuation Engine (`house_price_v1` - Regression!):**
   * Features: `square_feet`, `bedrooms`, `neighborhood_score`, `interest_rate_pct`, `property_age`
   * Blast Radius: `Mortgage Approval API`, `Home Equity Underwriting`, `Zillow Listing Feeder`
4. **Register Any Custom Model or CSV:**
   * Click **"+ Register Any Model / CSV"** in the header.
   * Upload your own CSV dataset or use the built-in Clinical Diabetes Risk dataset auto-fill.
   * ArgusML automatically calculates baselines, builds the dynamic DAG, and starts live monitoring!

---

## 📄 License
MIT License. Built for High-Impact Data Structures & MLOps Academic & Engineering Portfolios.
