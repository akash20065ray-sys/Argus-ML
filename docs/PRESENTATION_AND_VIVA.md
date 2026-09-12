# 🎓 ArgusML: Presentation Deck & Viva Defense Guide

> **Slide-by-Slide Presentation Structure & Evaluator Defense Strategy**  
> *Location:* `docs/PRESENTATION_AND_VIVA.md`

---

## 📽️ Recommended Slide Deck Structure (10 Slides)

### Slide 1: Title & Identity
* **Project Name:** ArgusML
* **Subtitle:** Universal Production AI Observability & Graph-Powered Root Cause Diagnostic Platform
* **Key Phrase:** *Bridging Modern MLOps with Core Data Structures & Algorithms*

### Slide 2: The Problem (Silent Model Failure)
* When machine learning models are deployed, real-world data shifts over time (**Covariate Shift & Concept Drift**).
* Models continue running and returning 200 OK responses, but accuracy plummets.
* Existing monitoring tools only say: *"Your model is failing"* without explaining **WHY** or **WHICH FEATURE** caused it.

### Slide 3: The Solution (ArgusML Overview)
* Continuous statistical drift watchdog (KS-test & PSI).
* Automated **Root-Cause Attribution** to pinpoint the culprit feature and upstream pipeline.
* **Blast Radius Calculation** to identify affected downstream microservices.
* **Max-Heap Prioritization** to eliminate alert fatigue.

### Slide 4: Unified System Architecture
* Walk through the 5 layers:
  `Ingestion (Queue) → Sliding Telemetry (Deque) → Drift Watchdog (HashMap) → RCA & Blast Radius (DAG) → Alert Ranking (Max-Heap) → Dashboard`

### Slide 5: The 5-DSA Algorithmic Spine (The Core Tech)
* **Circular FIFO Queue:** $O(1)$ async ingestion buffer.
* **Deque:** $O(1)$ amortized rolling accuracy and latency quantiles.
* **HashMap:** $O(1)$ empirical baseline distribution store.
* **Binary Max-Heap:** $O(\log N)$ priority queue ranking active failures.
* **Dependency DAG:** $O(V + E)$ Reverse-BFS for Root Cause & Forward-BFS for Blast Radius.

### Slide 6: Statistical Drift Detection Math
* **Two-Sample Kolmogorov-Smirnov Test:** $D = \sup_x |F_{\text{base}}(x) - F_{\text{prod}}(x)|$ ($p < 0.05$).
* **Population Stability Index (PSI):** $\sum (A_i - E_i) \ln(A_i / E_i)$ with 10 empirical bins.

### Slide 7: Graph-Powered Root Cause Analysis (RCA)
* How **Reverse-BFS** traverses from the degraded model node to find the culprit feature (`monthly_charges`, $D=0.485$).
* How **Forward-BFS** computes the blast radius on downstream consumer services (`Retention API`, `CRM Hub`).

### Slide 8: Universal Multi-Model & CSV Ingestion
* 100% domain-agnostic (Classification & Regression).
* Pre-configured domains: *Telecom Churn*, *Credit Card Fraud*, *Real Estate Valuation*.
* Upload **any CSV dataset** to auto-baseline and build the dynamic DAG.

### Slide 9: Live Interactive Dashboard
* HTML5 Canvas DAG topology with animated signal pulses and glowing node health states.
* Real-time rolling KPI cards.
* 1-Click dynamic chaos injection bar.
* 1-Click Root-Cause diagnostic modal.

### Slide 10: Verification & Results
* 10/10 passing unit tests in `pytest`.
* Sub-millisecond latency budgets ($< 1.5\text{ ms}$ ingestion).
* Live demonstration on `http://127.0.0.1:8000`.

---

## 🎯 The 60-Second Viva Elevator Pitch

> *"Good morning. I built **ArgusML**, an intelligent, universal AI observability and root-cause diagnostic platform for machine learning models in production.*
>
> *When ML models are deployed, data drift causes them to silently fail. ArgusML ingests production prediction events into a **Circular FIFO Queue** in $O(1)$ time, evaluates rolling accuracy and latency percentiles in $O(1)$ amortized time via a **Deque**, and detects statistical drift using **Two-Sample Kolmogorov-Smirnov tests** against baselines stored in a **HashMap**.*
>
> *When degradation occurs, it traverses a **4-layer Dependency DAG** using **Reverse-BFS** to isolate the exact culprit feature and corrupted pipeline in $O(V+E)$ time, calculates the downstream microservice blast radius via **Forward-BFS**, and prioritizes critical incidents in a **Binary Max-Heap**.*
>
> *The system is 100% domain-agnostic, supports any CSV dataset or model type, and is backed by a full suite of 10 passing unit tests and an interactive canvas visualizer."*
