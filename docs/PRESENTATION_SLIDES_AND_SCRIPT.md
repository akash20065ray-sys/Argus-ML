# 🛡️ ArgusML: Capstone Presentation & Team Defense Guide

This document contains the **complete 14-slide presentation structure**, **5-member module division**, **word-for-word speaking script**, **code/file ownership breakdown**, and **viva Q&A defense answers**.

Generated Artifacts in Downloads & Desktop:
- **PowerPoint Presentation File:** `ArgusML_Final_Presentation.pptx` & `ArgusML_Presentation.pptx` (CrimsonOrbit High-Contrast Theme)
- **Official Team Script PDF Document:** `ArgusML_Team_Presentation_Script.pdf`
- **Team Viva Question Bank PDF Document:** `ArgusML_Team_Viva_Question_Bank.pdf`

---

## 👥 1. Team Division & Module Ownership (5 Members)

| Roll No. | Name | PRN | Module & Role | DSA Concepts Implemented | Time Complexity |
| :---: | :--- | :---: | :--- | :--- | :---: |
| **9** | **Akash Kumar (Lead)** | **1251010761** | **Dynamic 4-Layer DAG & Reverse-BFS RCA** | • Directed Acyclic Graph (DAG)<br>• Reverse-BFS Upstream Attribution<br>• Forward-BFS Downstream Blast Radius<br>• Multi-Factor RCS Confidence Formula | Reverse-BFS: **$O(V+E)$**<br>Forward-BFS: **$O(V+E)$** |
| **7** | **Aher Krishna Gorakh** | **1251010727** | **Queue, Sliding Window & Drift Engine** | • Circular FIFO Ingestion Buffer<br>• Double-Ended Queue (Deque)<br>• 2-Sample Kolmogorov-Smirnov Test<br>• Population Stability Index (PSI) | Queue Enqueue: **$O(1)$**<br>Deque Eviction: **$O(1)$**<br>KS Test: **$O(N \log N)$**<br>PSI: **$O(N + B)$** |
| **38** | **Bhargude Sanskar Sandip** | **1251010716** | **Priority Max-Heap & Retraining Gate** | • Array-Backed Binary Max-Heap<br>• Pure `_sift_up` / `_sift_down`<br>• 4-Step Closed-Loop Validation Gate<br>• Automated Version Promotion | Push Alert: **$O(\log N)$**<br>Pop Max: **$O(\log N)$**<br>Peek Top: **$O(1)$**<br>Retrain Gate: **$O(S)$** |
| **4** | **Agaldare Ghansham Dilip** | **1251010321** | **Model Registry & Traffic Simulator** | • In-Memory Baseline Hash Map Store<br>• Empirical Distribution Moments<br>• Multi-Task Model Management<br>• Controlled Covariate Shift Injector | Model Lookup: **$O(1)$**<br>Baseline Lookup: **$O(1)$**<br>Traffic Stream: **$O(K)$** |
| **49** | **Hari Ratnakar Birare** | **1251010693** | **Session History, Reports & UI** | • Chronological Audit History<br>• 1-Click DAG Snapshot Replay<br>• Markdown Post-Mortem Generator<br>• Canvas 2D Animated Dashboard | Prepend History: **$O(1)$**<br>Snapshot Index: **$O(1)$**<br>Report Synthesize: **$O(R)$** |

---

## 📊 2. Slide Deck Outline (14 Slides - CrimsonOrbit Theme)

1. **Slide 1:** Title Slide (VIT Pune, ARGUSML, Presented by: GROUP - 9, Guide: Prof. Sheela)
2. **Slide 2:** Team Members (Roll No, Name, PRN Table)
3. **Slide 3:** Problem Statement & Industry Motivation (The Silent ML Decay, 1-Page Comprehensive)
4. **Slide 4:** Literature Review & Comparative Taxonomy (Structured Table Format)
5. **Slide 5:** Proposed Solution & Architectural Novelties (6 Core Pillars)
6. **Slide 6:** System Architecture & Master Telemetry Pipeline (5-Layer Diagram Flow)
7. **Slide 7:** Core DSA Mapping & Algorithmic Complexity Matrix Table
8. **Slide 8:** Technical Deep-Dive: Krishna (Circular FIFO Queue, Deque & Drift Analytics)
9. **Slide 9:** Technical Deep-Dive: Akash (Dynamic 4-Layer DAG & Reverse-BFS RCA)
10. **Slide 10:** Technical Deep-Dive: Sanskar (Binary Max-Heap & 4-Step Retraining Gate)
11. **Slide 11:** Technical Deep-Dive: Ghanshyam (In-Memory Baseline Hash Map & Traffic Simulator)
12. **Slide 12:** Technical Deep-Dive: Hari (History Audit Drawer, Post-Mortems & Canvas Dashboard)
13. **Slide 13:** Team Division & Individual Module Ownership Matrix
14. **Slide 14:** Experimental Validation, Conclusion & Live Demonstration Guide

---

## 🎙️ 3. Complete Word-for-Word Speaking Script

### 🎤 Slide 1 & 2: Title & Team Members
**Speaker: AKASH (Lead)**
> *"Respected guide Prof. Sheela and honorable panel members, good morning. Today, our team — Group 9 — is presenting **ArgusML**: A Universal Production AI Observability and Graph-Powered Root Cause Diagnostic Platform built upon 5 foundational Data Structures and Algorithms.*
> 
> *Our team members are Ghansham (Roll No. 4), Krishna (Roll No. 7), myself Akash (Roll No. 9), Sanskar (Roll No. 38), and Hari (Roll No. 49).*
> 
> *Let us begin with the critical industry problem that motivated our project."*

---

### 🎤 Slide 3: Problem Statement & Industry Motivation
**Speaker: AKASH (Lead)**
> *"Unlike traditional software services that fail loudly with runtime crashes or explicit HTTP 500 status codes, deployed Machine Learning (ML) models fail silently.*
> 
> *When live streaming customer data experiences covariate shift or concept drift, the inference microservice continues returning HTTP 200 OK with valid prediction floats. However, the underlying mapping between input features and target labels collapses, causing silent multi-million dollar revenue losses.*
> 
> *Furthermore, traditional APM tools like Datadog or Prometheus only monitor CPU and RAM — they are mathematically blind to statistical distribution drift. When a model decays, data engineering teams spend days manually writing SQL queries across multi-table ETL graphs to isolate the culprit feature.*
> 
> *ArgusML was engineered to solve this silent failure mode in real time."*

---

### 🎤 Slide 4: Literature Review & Comparative Taxonomy
**Speaker: AKASH (Lead)**
> *"As shown in our Literature Review Taxonomy on Slide 4, modern monitoring frameworks remain divided:*
> 1. *Traditional APMs (Datadog, Prometheus) monitor system health but have zero statistical drift detection and no ML DAG topology.*
> 2. *Offline Batch Profilers (EvidentlyAI, Great Expectations) calculate statistical profiles but operate out-of-band on static files, lack dynamic DAG awareness, and cannot triage alerts in real time.*
> 3. *ArgusML unites real-time statistical hypothesis testing (KS-test and PSI) with a 4-layer dynamic dependency DAG and a binary max-heap priority queue, executing entirely in-memory with sub-0.45 ms latency."*

---

### 🎤 Slide 5 & 6: Proposed Solution & System Architecture
**Speaker: AKASH (Lead)**
> *"ArgusML introduces 6 core architectural innovations:*
> 1. *A Pure In-Memory DSA Core executing in under 0.45 ms overhead.*
> 2. *A Real-Time Statistical Drift Engine running KS and PSI tests every 25 streaming events.*
> 3. *Topological Root Cause Attribution isolating corrupted features via Reverse-BFS in $O(V+E)$ time.*
> 4. *A Binary Max-Heap Queue prioritizing active incidents in $O(\log N)$ time.*
> 5. *A 4-Step Closed-Loop Retraining Validation Gate promoting recovered models with zero downtime.*
> 6. *A Chronological Session Audit Drawer with 1-click historical snapshot replay and downloadable post-mortems.*
> 
> *As shown in our 5-Layer Master Pipeline on Slide 6, live inference traffic enters the Ingestion Buffer, updates the Rolling Telemetry Window, triggers the Statistical Drift Engine, traverses the Dependency Graph, and populates the Priority Alert Heap.*
> 
> *I will now hand over to Krishna to present the DSA Foundations and the Ingestion/Drift modules."*

---

### 🎤 Slide 7 & 8: Core DSA Mapping, Ingestion Buffer & Drift Engine
**Speaker: KRISHNA**
> *"Thank you, Akash. As shown on Slide 7, every ArgusML module maps directly to optimal theoretical complexity bounds:*
> * *EventQueue operates in strict $O(1)$ time using modulo pointer wrapping over a pre-allocated array of capacity 5,000 to prevent memory leaks during traffic bursts.*
> * *MetricSlidingWindow uses a double-ended queue to maintain running confusion matrix accumulators in amortized $O(1)$ time over window $W = 400$.*
> 
> *On Slide 8, our Statistical Drift Engine combines the Two-Sample Kolmogorov-Smirnov Test ($O(N \log N)$) to detect empirical CDF divergence and the Population Stability Index (PSI, $O(N+B)$) to quantify quantile shift. Evaluating drift every 25 events guarantees statistical confidence while preserving sub-millisecond throughput.*
> 
> *I now invite Akash to explain the Dependency Graph and Reverse-BFS attribution."*

---

### 🎤 Slide 9: Dynamic Dependency DAG & Reverse-BFS Attribution
**Speaker: AKASH (Lead)**
> *"Thank you, Krishna. On Slide 9, ArgusML models production machine learning dependencies as a 4-layer Directed Acyclic Graph (DAG): `Pipelines → Features → Model → Downstream Services`.*
> 
> *When a model becomes degraded, our Reverse-BFS algorithm starts from the model node and traverses upstream edges in $O(V+E)$ time to identify candidate features. We compute a multi-factor Root Cause Score (RCS):*
> $$\text{RCS} = 0.45 \cdot \text{Drift} + 0.30 \cdot \text{PerfDrop} + 0.15 \cdot \text{Topology} + 0.10 \cdot \text{Blast}$$
> *The candidate feature maximizing RCS is isolated as the primary culprit with over 86% confidence.*
> 
> *I now hand over to Sanskar to explain the Priority Max-Heap and Retraining Gate."*

---

### 🎤 Slide 10: Binary Max-Heap & Automated Retraining Gate
**Speaker: SANSKAR**
> *"Thank you, Akash. On Slide 10, to protect engineers from alert fatigue, we built a pure array-backed Binary Max-Heap without external libraries. Push and pop-max operate in $O(\log N)$ time using custom `_sift_up` and `_sift_down` algorithms.*
> 
> *When an incident requires remediation, our 4-Step Validation Gate automatically:*
> 1. *Re-fits model parameters to the recent drifted distribution.*
> 2. *Validates that Candidate Accuracy $\ge$ SLA and P99 Latency $\le$ SLA threshold.*
> 3. *Ensures candidate strictly outperforms the degraded active model.*
> 4. *Promotes the model to production with zero downtime ($v1.0.0 \to v1.1.0$), refreshes HashMap baselines, resolves heap alerts, and restores DAG health.*
> 
> *I now invite Ghanshyam to present the Model Registry and Traffic Simulator."*

---

### 🎤 Slide 11: In-Memory Model Registry & Traffic Simulator
**Speaker: GHANSHYAM**
> *"Thank you, Sanskar. On Slide 11, our ModelRegistry is an in-memory Hash Map providing $O(1)$ average-time lookup for model metadata and baseline distribution moments (mean, variance, decile quantiles) across both classification and regression models.*
> 
> *Our Universal Traffic Simulator streams synthetic predictions at 15–25 events/sec with Gaussian noise. It features an interactive Covariate Shift Injector that allows evaluating drift detection and Reverse-BFS isolation on demand.*
> 
> *I now invite Hari to present the History Drawer, Post-Mortems, and Dashboard."*

---

### 🎤 Slide 12: Session History Drawer, Post-Mortems & Dashboard
**Speaker: HARI**
> *"Thank you, Ghanshyam. On Slide 12, our thread-safe ModelTestingHistory implements a chronological audit drawer with $O(1)$ prepend.*
> 
> *Engineers can click any past session to trigger a 1-Click DAG Snapshot Replay, rendering the exact historical graph state and culprit highlighting. The engine also exports comprehensive Markdown Post-Mortems documenting root cause attribution, statistical indicators, and remediation logs.*
> 
> *Our dashboard is built with Vanilla CSS3 glassmorphism and HTML5 Canvas 2D for high-DPI topological visualization.*
> 
> *I now invite Akash to conclude with our experimental evaluation."*

---

### 🎤 Slide 13 & 14: Experimental Results, Conclusion & Live Demo
**Speaker: AKASH (Lead)**
> *"To conclude, our complete implementation was validated with a 17-test Pytest test suite covering all data structures and lifecycle transitions with 100% pass rate.*
> 
> *Key benchmark highlights:*
> * *Telemetry Overhead:* $<0.45\text{ ms}$ compute latency.
> * *RCA Attribution Precision:* $100\%$ accuracy in isolating culprit features under controlled covariate shift.
> * *Self-Healing:* Successfully recovered accuracy from $68.1\%$ back to $96.2\%$ with automated version promotion ($v1.0.0 \to v1.1.0$).*
> 
> *We are now ready to demonstrate the live interactive platform at `http://127.0.0.1:8000`."*
