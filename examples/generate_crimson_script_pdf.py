"""
Generate ArgusML_Team_Presentation_Script.pdf matching the 13-slide CrimsonOrbit flow.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable

def generate_script_pdf():
    downloads_path = os.path.expanduser("~/Downloads")
    output_pdf = os.path.join(downloads_path, "ArgusML_Team_Presentation_Script.pdf")

    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Colors
    c_dark_navy = colors.HexColor("#0F1219")
    c_card_bg = colors.HexColor("#191E2A")
    c_crimson = colors.HexColor("#EB3C3C")
    c_gold = colors.HexColor("#F59E0B")
    c_text_dark = colors.HexColor("#1E293B")
    c_text_muted = colors.HexColor("#64748B")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_crimson,
        alignment=1, # Center
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_text_muted,
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=c_crimson,
        spaceBefore=12,
        spaceAfter=6
    )

    speaker_badge_style = ParagraphStyle(
        'SpeakerBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_gold,
        spaceBefore=8,
        spaceAfter=2
    )

    script_body_style = ParagraphStyle(
        'ScriptBody',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.2,
        leading=13.5,
        textColor=c_text_dark,
        leftIndent=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_text_dark,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'THeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=c_text_dark
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("ARGUSML: CAPSTONE PRESENTATION SCRIPT", title_style))
    story.append(Paragraph("13-Slide Speaking Script • 5-Member Module Ownership • Viva Defense Q&A", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_crimson, spaceAfter=10))

    # Team Ownership Table
    story.append(Paragraph("1. Team Division & Module Ownership", h1_style))
    
    table_data = [
        [
            Paragraph("Member", table_header_style),
            Paragraph("Module & Role", table_header_style),
            Paragraph("DSA Concepts", table_header_style),
            Paragraph("Complexity", table_header_style),
            Paragraph("Source Files", table_header_style),
        ],
        [
            Paragraph("<b>Aakash</b><br/>(Lead)", table_cell_style),
            Paragraph("DAG & RCA Engine", table_cell_style),
            Paragraph("Dynamic 4-Layer DAG<br/>Reverse-BFS Attribution<br/>Forward-BFS Blast<br/>RCS Confidence Formula", table_cell_style),
            Paragraph("Reverse-BFS: O(V+E)<br/>Forward-BFS: O(V+E)", table_cell_style),
            Paragraph("dsa/graph.py<br/>rca/engine.py<br/>orchestrator.py", table_cell_style),
        ],
        [
            Paragraph("<b>Krishna</b>", table_cell_style),
            Paragraph("Queue, Deque & Drift", table_cell_style),
            Paragraph("Circular FIFO Buffer<br/>Deque Sliding Window<br/>2-Sample KS-Test<br/>PSI Analyzer", table_cell_style),
            Paragraph("Enqueue: O(1)<br/>Deque: O(1)<br/>KS: O(N log N)<br/>PSI: O(N + B)", table_cell_style),
            Paragraph("dsa/queue.py<br/>dsa/deque.py<br/>drift/detector.py", table_cell_style),
        ],
        [
            Paragraph("<b>Sanskar</b>", table_cell_style),
            Paragraph("Heap & Retraining Gate", table_cell_style),
            Paragraph("Binary Max-Heap<br/>_sift_up / _sift_down<br/>4-Step Validation Gate<br/>Version Promotion", table_cell_style),
            Paragraph("Push: O(log N)<br/>Pop: O(log N)<br/>Retrain Gate: O(S)", table_cell_style),
            Paragraph("dsa/heap.py<br/>universal_runner.py<br/>orchestrator.py", table_cell_style),
        ],
        [
            Paragraph("<b>Ghanshyam</b>", table_cell_style),
            Paragraph("Registry & Traffic Sim", table_cell_style),
            Paragraph("In-Memory Baseline Store<br/>Multi-Task Moments<br/>Shift/Spike Injector<br/>CSV Ingestion", table_cell_style),
            Paragraph("Model: O(1)<br/>Baseline: O(1)<br/>Stream: O(K)", table_cell_style),
            Paragraph("dsa/registry.py<br/>traffic_simulator.py<br/>universal_runner.py", table_cell_style),
        ],
        [
            Paragraph("<b>Hari</b>", table_cell_style),
            Paragraph("History, Reports & UI", table_cell_style),
            Paragraph("Chronological History<br/>DAG Snapshot Replay<br/>Markdown Post-Mortem<br/>Canvas 2D Dashboard", table_cell_style),
            Paragraph("Prepend: O(1)<br/>Snapshot: O(1)<br/>Report: O(R)", table_cell_style),
            Paragraph("dsa/history.py<br/>main.py<br/>app.js / renderer.js", table_cell_style),
        ],
    ]

    t = Table(table_data, colWidths=[65, 110, 150, 105, 110])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark_navy),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # Speaking Script Section
    story.append(Paragraph("2. Word-for-Word Speaking Script (13 Slides)", h1_style))

    scripts = [
        ("Slide 1: Title & Project Overview", "AAKASH (Lead)",
         "Respected professors and panel members, good morning. Today, our team is presenting ArgusML — a Universal Production AI Observability and Graph-Powered Root Cause Diagnostic Platform built entirely upon 5 foundational Data Structures and Algorithms. Modern enterprises deploy hundreds of machine learning models to production, but managing their reliability remains an unsolved challenge. Our goal with ArgusML was to build a pure, in-memory watchdog engine capable of sub-millisecond telemetry, automated statistical drift detection, topological root cause attribution, and closed-loop self-healing without relying on heavy third-party vendor stacks."),
        
        ("Slide 2: Problem Statement & Industry Motivation", "AAKASH (Lead)",
         "Unlike traditional software services that crash with HTTP 500 errors when a bug occurs, machine learning models fail silently. As real-world customer behavior evolves, input distributions drift away from the baseline. The model continues to output confident predictions, but its real-world accuracy silently collapses from 95% down to 65%. When an accuracy drop is discovered, data engineering teams face three bottlenecks: manual root-cause isolation across multi-table ETL pipelines, SRE alert fatigue from hundreds of uncorrelated alerts, and manual retraining hazards where unvalidated models are accidentally deployed."),
        
        ("Slide 3: Literature Review & Theoretical Positioning", "AAKASH (Lead)",
         "In our literature survey, we analyzed classical distribution shift paradigms: Covariate Shift (Shimodaira, 2000), where P(X) shifts while P(Y|X) remains fixed; and Concept Drift (Widmer and Kubat, 1996), where relationships P(Y|X) change over time. We evaluated several statistical distance metrics, including Wasserstein Distance, KL Divergence, the 2-Sample Kolmogorov-Smirnov test, and PSI. We selected KS-test and PSI because KS-test provides a non-parametric empirical CDF distance with rigorous p-value thresholds in O(N log N) time, while PSI delivers robust quantile-binned stability measurements in O(N+B) time. Unlike Evidently AI or Datadog, ArgusML is the first system to integrate statistical drift detection with 4-layer dependency DAG Reverse-BFS for automated upstream attribution."),
        
        ("Slide 4 & 5: Proposed Solution & System Architecture", "AAKASH (Lead)",
         "ArgusML introduces a 5-pillar in-memory architecture: 1) A Pure In-Memory DSA Core executing in under 0.45 ms overhead; 2) A Real-Time Drift Watchdog running KS-test and PSI evaluations every 25 streaming events; 3) Topological Root Cause Attribution isolating corrupted features via Reverse-BFS; 4) A Priority Max-Heap Queue ranking incidents by composite mathematical severity; 5) A 4-Step Closed-Loop Retraining Validation Gate promoting recovered models with zero downtime. Live predictions flow seamlessly across the 5 distinct topological layers shown on Slide 5. I will now hand over to Krishna."),
        
        ("Slide 6 & 7: DSA Foundations, Ingestion Buffer & Drift Engine", "KRISHNA",
         "Thank you, Aakash. Every ArgusML module maps directly to optimal theoretical complexity: EventQueue operates in strict O(1) time; MetricSlidingWindow provides amortized O(1) compute; ModelRegistry provides O(1) average-time lookups; AlertMaxHeap guarantees O(log N) push and extraction; and DependencyGraph traverses topology in O(V+E) linear time. When live predictions arrive at POST /api/ingest, our Circular FIFO EventQueue buffers events using modulo pointer wrapping with 5,000 capacity. Our MetricSlidingWindow maintains recent W = 400 inferences for rolling accuracy and P99 latency. Every 25 events, our DriftEngine executes the 2-Sample KS test and PSI quantile binning against HashMap baselines."),
        
        ("Slide 8: Dynamic DAG & Root Cause Confidence Scoring (RCS)", "AAKASH (Lead)",
         "Thank you, Krishna. Our DependencyGraph dynamically builds a 4-layer topology: Upstream Pipelines -> Inferred Features -> Active Model -> Downstream Services. When performance degrades, we execute Reverse-BFS in O(V+E) time starting from the degraded Model node upstream to pinpoint the culprit feature and its originating ETL ingestion source. We also execute Forward-BFS downstream to compute the impacted Blast Radius. To provide mathematical certainty, I formulated the Root Cause Confidence Score (RCS) = (0.45 * DriftEvidence) + (0.30 * AccuracyDrop) + (0.15 * TopologyProximity) + (0.10 * BlastImpact), isolating the primary culprit with over 85% to 95% confidence."),
        
        ("Slide 9: Incident Priority Max-Heap & Retraining Gate", "SANSKAR",
         "Thank you, Aakash. To prevent SRE alert fatigue in multi-model environments, we implemented a pure, array-backed Binary Max-Heap using custom _sift_up and _sift_down methods. Pushing new incidents and extracting the critical top incident both execute in strict O(log N) time. When an incident requires remediation, our 1-Click Retraining Engine executes a 4-Step Validation Gate: Data sufficiency check, Candidate re-fitting, 4-step validation (Accuracy >= SLA, Latency <= SLA, positive R2), and Zero-downtime promotion with version bumping (v1.0.0 -> v1.1.0), Max-Heap alert clearance, and DAG health recovery."),
        
        ("Slide 10: In-Memory Baseline Registry & Traffic Simulator", "GHANSHYAM",
         "Thank you, Sanskar. The ModelRegistry is our in-memory Hash Map baseline store, providing O(1) constant-time lookup for model metadata, SLA thresholds, and empirical baseline distribution moments across both Classification and Regression models. To thoroughly validate the system, I built the UniversalTrafficSimulator, which streams synthetic predictions at 20 events per second with Gaussian noise. It features an interactive Covariate Shift Injector allowing users to scale any feature's distribution by 3.5x or spike latency by +250ms with a single click to trigger live drift. Our CSV parser also extracts columns and registers baselines automatically."),
        
        ("Slide 11: History Drawer, Post-Mortems & Canvas Dashboard", "HARI",
         "Thank you, Ghanshyam. We built ModelTestingHistory, maintaining a thread-safe chronological record of all model registrations, live drift detections, and retraining runs with O(1) prepend operations. With our 1-Click DAG Snapshot Replay, clicking any card in the drawer immediately loads the exact historical DAG topology and culprit highlighting captured during that run. Our Post-Mortem Engine automatically compiles and downloads a comprehensive Markdown post-mortem report documenting executive summaries, culprit feature rankings, and remediation logs. Our dashboard is built with Vanilla HTML5/CSS3 and an interactive Canvas 2D DAG renderer with pulsating node halos."),
        
        ("Slide 12 & 13: Team Contribution Breakdown, Evaluation & Live Demo", "AAKASH (Lead)",
         "On Slide 12, we summarize our team's module ownership across the 5 core DSA components. On Slide 13, we present our experimental evaluation results: All 17 unit tests in our Pytest suite pass with 100% success; Telemetry compute overhead averages under 0.45 ms per prediction; Reverse-BFS RCA achieved 100% accuracy in isolating culprit features; and automated retraining recovered model accuracy from 68% back to 96% with zero downtime. We are now excited to demonstrate the live ArgusML platform running at http://127.0.0.1:8000 and look forward to your questions.")
    ]

    for title, speaker, text in scripts:
        story.append(Paragraph(f"<b>{title}</b>", ParagraphStyle('SlideT', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=c_dark_navy, spaceBefore=4)))
        story.append(Paragraph(f"Speaker: <b>{speaker}</b>", speaker_badge_style))
        story.append(Paragraph(f'"{text}"', script_body_style))
        story.append(Spacer(1, 3))

    # Viva Defense Q&A
    story.append(PageBreak())
    story.append(Paragraph("3. Expected Viva Questions & High-Scoring Defense Answers", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_gold, spaceAfter=8))

    qas = [
        ("Q1 (For Aakash): Why Reverse-BFS over Dijkstra or DFS for Root Cause Analysis?",
         "Answer: In our dependency DAG, all dependency links between pipelines, features, and model nodes are discrete unweighted edges. BFS explores dependencies layer by layer in strictly optimal O(V+E) time. Dijkstra introduces unnecessary O(E log V) heap overhead for unweighted graphs, while DFS can explore deep non-critical branches. Reverse-BFS guarantees that we discover the closest upstream culprit feature and originating ingestion pipeline with shortest topological distance first."),
        
        ("Q2 (For Krishna): How does the Circular FIFO Queue prevent memory overflow during spikes?",
         "Answer: Our EventQueue allocates a fixed circular buffer of capacity C = 5000 using modulo pointer wrapping: self.tail = (self.tail + 1) % self.capacity. When the queue reaches capacity, new events overwrite the oldest unconsumed entry and increment a dropped_events counter. This ensures O(1) constant-time ingestion while guaranteeing that memory usage never exceeds the pre-allocated buffer size."),
        
        ("Q3 (For Sanskar): Why is a Binary Max-Heap superior to an array or sorted list for incidents?",
         "Answer: An unsorted array requires O(N) linear time to search for the highest-severity alert, which is too slow in high-throughput systems. A sorted array requires O(N) time on every new alert insertion. A Binary Max-Heap provides the optimal theoretical balance: O(log N) insertion via _sift_up and O(log N) extraction of the critical alert via _sift_down, while peeking the active top alert is instantaneous O(1)."),
        
        ("Q4 (For Ghanshyam): How does ModelRegistry achieve O(1) baseline retrieval across multiple models?",
         "Answer: ModelRegistry is backed by Python's in-memory Hash Map indexed by unique model_id strings. Each ModelMetadata record maintains an inner hash map feature_baselines mapping feature names to EmpiricalBaseline objects containing baseline sample arrays and statistical moments. Hash map bucket indexing provides O(1) average-time retrieval regardless of how many models are registered in the platform."),
        
        ("Q5 (For Hari): How does the Session History Drawer capture and replay historical DAG snapshots?",
         "Answer: When a drift incident, model switch, or retraining occurs, ModelTestingHistory captures a deep-copy snapshot of the graph adjacency list and node health states inside TestSessionRecord.graph_snapshot. When a user clicks a historical record in the UI, our frontend GraphRenderer reads that snapshot and replays the exact canvas topology and red-highlighted culprit nodes without needing to roll back active live production telemetry.")
    ]

    for q, a in qas:
        story.append(Paragraph(f"<b>{q}</b>", ParagraphStyle('QStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, textColor=c_crimson, spaceBefore=6)))
        story.append(Paragraph(a, ParagraphStyle('AStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=8.8, leading=12.5, textColor=c_text_dark, leftIndent=8, spaceAfter=4)))

    doc.build(story)
    print(f"[SUCCESS] Saved Crimson Script PDF to {output_pdf}")

if __name__ == "__main__":
    generate_script_pdf()
