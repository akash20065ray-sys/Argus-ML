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
> *"Respected guide Prof. Sheela and honorable panel members, good morning. Today, our team — Group 9 — is presenting **ArgusML**: A Real-Time Health Watchdog and Root-Cause Diagnostic Platform for Machine Learning Models, built from scratch using 5 foundational Data Structures and Algorithms.*
> 
> *Our team members are Ghansham (Roll No. 4), Krishna (Roll No. 7), myself Akash (Roll No. 9), Sanskar (Roll No. 38), and Hari (Roll No. 49).*
> 
> *Let us explain the real-world problem that motivated our project in simple terms."*

---

### 🎤 Slide 3: Problem Statement (Why AI Models Break Silently)
**Speaker: AKASH (Lead)**
> *"In regular software development, when a bug happens, the server crashes loudly with an error code like HTTP 500.*
> 
> *However, **AI models break silently**:*
> 1. *When customer habits or incoming data change, the model keeps running and returns `HTTP 200 OK`. But its predictions become completely wrong, dropping real-world accuracy from 95% down to 65% without anyone noticing.*
> 2. *Existing tools like Datadog or Prometheus only check CPU and RAM — they cannot see if incoming data has drifted.*
> 3. *Because data flows through huge multi-step pipelines, when an app fails, engineers take days manually querying databases to guess which feature broke.*
> 4. *Existing tools only send alert emails; they don't fix the model, leading to costly downtime.*
> 
> *ArgusML was built to catch these data changes instantly and fix the model automatically."*

---

### 🎤 Slide 4: Literature Survey & Research Gap Analysis
**Speaker: AKASH (Lead)**
> *"On Slide 4, we conducted a systematic Literature Survey of foundational research papers in ML monitoring:*
> 1. *Sculley et al. (NeurIPS 2015) proved that 95% of production ML is technical debt and monitoring glue code, but did not provide an in-memory automated solution.*
> 2. *Shimodaira (2000) and Gama et al. (2014) formalized covariate shift and concept drift equations, but their models remained theoretical without live microservice integration.*
> 3. *Breck et al. (SysML 2019) introduced data validation, but it relies on slow offline batch jobs with multi-hour delays.*
> 4. *Rabanser & Lipton (NeurIPS 2019) evaluated statistical tests (KS-Test/PSI), but tested them in isolation on static datasets without upstream graph root-cause isolation.*
> 5. *Existing tools like EvidentlyAI and WhyLogs operate as offline batch profilers lacking dynamic graph lineage, priority alert heaps, and closed-loop retraining.*
> 
> *ArgusML addresses these gaps by combining real-time in-memory statistical drift testing with 4-layer dependency graph Reverse-BFS and automated retraining."*

---

### 🎤 Slide 5 & 6: Our Solution & System Architecture
**Speaker: AKASH (Lead)**
> *"ArgusML solves this using 6 simple, powerful capabilities:*
> 1. *An Ultra-Fast In-Memory Engine that runs in under 0.45 ms using less than 12 MB of RAM.*
> 2. *A Live Drift Watchdog that checks incoming data against baseline numbers every 25 predictions.*
> 3. *An Automatic Root-Cause Finder that climbs backward up the pipeline graph to pinpoint the exact corrupted feature.*
> 4. *Smart Priority Alerts that sort issues by real urgency so engineers see the most critical problems first.*
> 5. *1-Click Auto-Retraining that updates the model to version 1.1 with zero downtime.*
> 6. *A Timeline History Drawer with 1-click historical replay and downloadable post-mortems.*
> 
> *On Slide 6, you can see how data flows step-by-step: from the Ingestion Queue into the Recent Predictions Window, through the Drift Checker, across the Connection Graph, and into the Priority Alert Heap.*
> 
> *I will now hand over to Krishna to explain the Ingestion Queue and Drift Checker."*


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
