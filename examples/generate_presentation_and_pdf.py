"""
Script to generate ArgusML_Presentation.pptx and ArgusML_Team_Presentation_Script.pdf.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.pdfgen import canvas


def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 widescreen
    prs.slide_height = Inches(7.5)

    # Color Palette
    BG_COLOR = RGBColor(11, 16, 29)       # Deep Navy #0B101D
    CARD_BG = RGBColor(19, 27, 46)        # Card Navy #131B2E
    CYAN_ACCENT = RGBColor(0, 242, 254)   # Cyan #00F2FE
    BLUE_ACCENT = RGBColor(56, 189, 248)  # Sky Blue #38BDF8
    EMERALD_ACCENT = RGBColor(16, 185, 129) # Green #10B981
    CRIMSON_ACCENT = RGBColor(239, 68, 68) # Red #EF4444
    TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC
    TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8
    TEXT_DIM = RGBColor(100, 116, 139)    # #64748B

    blank_layout = prs.slide_layouts[6]

    def add_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="ARGUSML OBSERVABILITY PLATFORM"):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = category_text.upper()
        p1.font.name = "Arial"
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = CYAN_ACCENT

        p2 = tf.add_paragraph()
        p2.text = title_text
        p2.font.name = "Arial"
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    add_slide_bg(slide1)

    # Title box
    tb = slide1.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.3), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p_badge = tf.paragraphs[0]
    p_badge.text = "DATA STRUCTURES & ALGORITHMS CAPSTONE PROJECT"
    p_badge.font.name = "Arial"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = CYAN_ACCENT

    p_title = tf.add_paragraph()
    p_title.text = "ArgusML: Universal Production AI Observability & Graph-Powered Root Cause Diagnostics"
    p_title.font.name = "Arial"
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE
    p_title.space_before = Pt(10)

    p_sub = tf.add_paragraph()
    p_sub.text = "A real-time watchdog system built with 5 foundational data structures for continuous drift detection, reverse DAG attribution, max-heap incident prioritization, and automated model retraining."
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_before = Pt(12)

    # Team Card
    card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.0), Inches(11.33), Inches(1.8))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = RGBColor(30, 41, 69)

    tf_team = card.text_frame
    tf_team.margin_left = Inches(0.3)
    tf_team.margin_top = Inches(0.2)
    p_t = tf_team.paragraphs[0]
    p_t.text = "PROJECT TEAM & CONTRIBUTION ROLES:"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(10)
    p_t.font.bold = True
    p_t.font.color.rgb = BLUE_ACCENT

    p_m = tf_team.add_paragraph()
    p_m.text = "• Aakash (Lead): System Orchestration, 4-Layer Dynamic DAG Topology & Reverse-BFS RCA Engine\n" \
               "• Krishna: High-Throughput Circular FIFO Ingestion Queue, Deque Sliding Window & Drift Analytics (KS/PSI)\n" \
               "• Sanskar: Binary Max-Heap Priority Alert Queue & Automated 1-Click Retraining Validation Gate\n" \
               "• Ghanshyam: Hash Map Baseline Model Registry & Universal Multi-Model Traffic Simulation Engine\n" \
               "• Hari: Session History Audit Drawer, Snapshot Replay & Markdown Incident Post-Mortem Exporter"
    p_m.font.name = "Calibri"
    p_m.font.size = Pt(11)
    p_m.font.color.rgb = TEXT_WHITE
    p_m.space_before = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 2: Team Roles & Individual Contributions (Requested Slide 2!)
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_slide_bg(slide2)
    add_header(slide2, "Team Roles & Individual Module Distribution", "MODULE OWNERSHIP & DSA ASSIGNMENT")

    # 5 Person Cards
    members = [
        ("Aakash (Lead)", "DAG & RCA Engine", CYAN_ACCENT, [
            "Dynamic 4-Layer Dependency DAG (Pipelines -> Features -> Model -> Services)",
            "Reverse-BFS Upstream Root Cause Attribution (O(V+E))",
            "Forward-BFS Downstream Blast Radius Traversal (O(V+E))",
            "Multi-factor Root Cause Confidence Scoring (RCS Engine)",
            "ArgusSystem Central Orchestrator & Telemetry Loop"
        ]),
        ("Krishna", "Queue, Deque & Drift", BLUE_ACCENT, [
            "Circular FIFO Ingestion Buffer (EventQueue, O(1) Push/Pop)",
            "Metric Sliding Window (Double-Ended Queue, O(1) Amortized)",
            "Two-Sample Kolmogorov-Smirnov (KS) Drift Test (O(N log N))",
            "Population Stability Index (PSI) Distribution Analyzer (O(N+B))",
            "Rolling P99 Latency & Accuracy Telemetry Engine"
        ]),
        ("Sanskar", "Max-Heap & Retraining", EMERALD_ACCENT, [
            "Incident Priority Max-Heap with custom _sift_up / _sift_down",
            "Multi-factor Incident Severity Ranking & O(log N) Extraction",
            "Automated 1-Click Retraining on Rolling Distribution Windows",
            "4-Step Closed-Loop Model Validation Gate & Version Promotion",
            "Automated Max-Heap Incident Resolution & Node Health Recovery"
        ]),
        ("Ghanshyam", "Registry & Simulation", RGBColor(168, 85, 247), [
            "In-Memory Baseline Distribution Store (ModelRegistry HashMap, O(1))",
            "Multi-Task Model Support (Classification & Regression Baselines)",
            "Universal Real-Time Traffic Simulator & Background Workers",
            "Synthetic Covariate Shift Injector & Latency Spike Trigger",
            "Multipart CSV Parsing & Feature Ingestion Utilities"
        ]),
        ("Hari", "History, Reports & UI", RGBColor(245, 158, 11), [
            "Chronological Session Audit Drawer (ModelTestingHistory)",
            "1-Click Interactive Historical DAG Topology Snapshot Replay",
            "Automated Markdown Post-Mortem Incident Report Generator",
            "Full-Stack Glassmorphic Dashboard & Real-Time REST APIs",
            "HTML5 Canvas 2D Animated Topological Graph Visualization"
        ]),
    ]

    card_w = Inches(2.22)
    card_gap = Inches(0.18)
    left_start = Inches(0.8)

    for i, (name, role, col, tasks) in enumerate(members):
        c_left = left_start + i * (card_w + card_gap)
        c_shape = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.7), card_w, Inches(5.2))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = CARD_BG
        c_shape.line.color.rgb = col
        c_shape.line.width = Pt(1.5)

        tf = c_shape.text_frame
        tf.margin_left = tf.margin_right = Inches(0.14)
        tf.margin_top = Inches(0.15)
        tf.word_wrap = True

        p_name = tf.paragraphs[0]
        p_name.text = name
        p_name.font.name = "Arial"
        p_name.font.size = Pt(12)
        p_name.font.bold = True
        p_name.font.color.rgb = col

        p_role = tf.add_paragraph()
        p_role.text = role
        p_role.font.name = "Calibri"
        p_role.font.size = Pt(9.5)
        p_role.font.bold = True
        p_role.font.color.rgb = TEXT_WHITE
        p_role.space_before = Pt(2)

        for task in tasks:
            pt = tf.add_paragraph()
            pt.text = f"• {task}"
            pt.font.name = "Calibri"
            pt.font.size = Pt(8.5)
            pt.font.color.rgb = TEXT_MUTED
            pt.space_before = Pt(5)

    # -------------------------------------------------------------
    # SLIDE 3: Problem Statement & Motivation
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_slide_bg(slide3)
    add_header(slide3, "The Silent Failure of AI Systems in Production", "INDUSTRY PROBLEM & MOTIVATION")

    col_w = Inches(5.6)
    c1 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), col_w, Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = CRIMSON_ACCENT
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.25)
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "🚨 Critical Industry Challenges"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CRIMSON_ACCENT

    points1 = [
        ("Silent Model Degradation", "ML models don't crash with 500 errors; they silently predict incorrect outcomes as real-world input distributions drift over time."),
        ("No Upstream Root-Cause Pinpointing", "When accuracy drops, data engineering teams take days debugging complex multi-table ETL pipelines to find which specific feature broke."),
        ("Alert Fatigue & Unprioritized Incidents", "Standard APM tools trigger hundreds of disconnected metrics, drowning SREs in noise without severity prioritization."),
        ("Manual & Risky Retraining Loops", "Data scientists manually retrain models and redeploy without standardized automated validation gates, causing regressions.")
    ]
    for h, desc in points1:
        ph = tf1.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(11)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(8)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = TEXT_MUTED

    c2 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), col_w, Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = EMERALD_ACCENT
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.25)
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "💡 The ArgusML Solution"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = EMERALD_ACCENT

    points2 = [
        ("Pure In-Memory DSA Engine", "Zero heavy third-party vendor bloat; built entirely using 5 foundational data structures for blazing fast O(1) & O(V+E) execution."),
        ("Reverse-BFS Root Cause Attribution", "Automated upstream topological graph traversal isolates exact culprit features and corrupted ETL pipelines in milliseconds."),
        ("Max-Heap Composite Prioritization", "Prioritizes incidents by composite severity score (accuracy drop, drift intensity, and blast radius) in O(log N) time."),
        ("Closed-Loop Retraining Gate", "1-click automated retraining on recent sliding windows with 4-step validation criteria before zero-downtime production promotion.")
    ]
    for h, desc in points2:
        ph = tf2.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(11)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(8)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 4: Core DSA Mapping & Algorithmic Complexity Table (Requested Slide!)
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_slide_bg(slide4)
    add_header(slide4, "Core DSA Mapping & Theoretical Complexity Analysis", "DATA STRUCTURES & ALGORITHMS FOUNDATION")

    # Table of 5 DSAs
    rows, cols = 6, 5
    left, top, width, height = Inches(0.8), Inches(1.7), Inches(11.73), Inches(5.1)
    table_shape = slide4.shapes.add_table(rows, cols, left, top, width, height)
    tbl = table_shape.table

    col_widths = [Inches(2.2), Inches(2.3), Inches(3.0), Inches(2.2), Inches(2.03)]
    for idx, w in enumerate(col_widths):
        tbl.columns[idx].width = w

    headers = ["Data Structure", "ArgusML Component", "System Purpose & Implementation", "Time Complexity", "Space Complexity"]
    for idx, text in enumerate(headers):
        cell = tbl.cell(0, idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(26, 38, 66)
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.alignment = PP_ALIGN.CENTER

    dsa_data = [
        ("Circular FIFO Queue", "EventQueue\n(queue.py)", "Asynchronous prediction ingestion buffer with modulo pointer wrapping to prevent memory leaks.", "Enqueue: O(1)\nDequeue: O(1)", "O(C)\nFixed Capacity"),
        ("Double-Ended Queue", "MetricSlidingWindow\n(deque.py)", "Rolling window over recent W predictions for rolling accuracy, precision, recall, and P99 latency.", "Append / Evict: O(1)\nAmortized Compute", "O(W)\nWindow Size"),
        ("In-Memory Hash Map", "ModelRegistry\n(registry.py)", "Constant-time model lookup, baseline empirical distribution storage, and SLA threshold indexing.", "Average Lookup: O(1)\nInsert: O(1)", "O(M * F)\nModels & Features"),
        ("Binary Max-Heap", "AlertMaxHeap\n(heap.py)", "Priority queue with custom _sift_up / _sift_down ranking incidents by composite severity score.", "Push: O(log N)\nPop Max: O(log N)", "O(N)\nActive Incidents"),
        ("Directed Acyclic Graph", "DependencyGraph\n(graph.py)", "4-layer topology (Pipelines -> Features -> Model -> Services) for upstream RCA and downstream blast.", "Reverse-BFS: O(V+E)\nForward-BFS: O(V+E)", "O(V + E)\nNodes & Edges"),
    ]

    for row_idx, data in enumerate(dsa_data, start=1):
        for col_idx, val in enumerate(data):
            cell = tbl.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 1 else RGBColor(15, 22, 38)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Calibri"
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_WHITE
            if col_idx in [0, 3]:
                p.font.bold = True
                if col_idx == 0:
                    p.font.color.rgb = BLUE_ACCENT
                elif col_idx == 3:
                    p.font.color.rgb = EMERALD_ACCENT

    # -------------------------------------------------------------
    # SLIDE 5: System Architecture & Data Flow
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_slide_bg(slide5)
    add_header(slide5, "End-to-End System Architecture & Telemetry Pipeline", "ARCHITECTURAL BLUEPRINT")

    flow_boxes = [
        ("1. Ingestion Stream", "Circular FIFO EventQueue", "High-throughput O(1) buffer absorbs async model prediction traffic without blocking production services.", CYAN_ACCENT),
        ("2. Sliding Telemetry", "Deque MetricSlidingWindow", "Computes rolling accuracy and P99 latency across recent 400 inferences in amortized O(1) time.", BLUE_ACCENT),
        ("3. Statistical Drift", "DriftEngine (KS & PSI)", "Continuously compares sliding window distribution against Hash Map baselines using 2-sample KS & PSI.", RGBColor(168, 85, 247)),
        ("4. Root Cause Traversal", "DAG Reverse-BFS Engine", "Traverses dependency graph upstream in O(V+E) to isolate culprit features and corrupted ETL origins.", CRIMSON_ACCENT),
        ("5. Priority Alert Queue", "AlertMaxHeap", "Ranks incidents by composite severity score in O(log N) for prioritized SRE action and incident triage.", RGBColor(245, 158, 11)),
        ("6. Automated Retraining", "Validation Gate & History", "Retrains candidate model, checks 4 validation criteria, bumps version, resolves heap alerts, and logs history.", EMERALD_ACCENT),
    ]

    for idx, (step_title, dsa_name, desc, col) in enumerate(flow_boxes):
        row = idx // 3
        col_pos = idx % 3
        bx = Inches(0.8 + col_pos * 4.0)
        by = Inches(1.7 + row * 2.7)

        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, Inches(3.75), Inches(2.4))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.18)
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = step_title
        p1.font.name = "Arial"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = dsa_name
        p2.font.name = "Calibri"
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = "Calibri"
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = TEXT_MUTED
        p3.space_before = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 6: Deep-Dive: Aakash (DAG & Reverse-BFS RCA)
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_slide_bg(slide6)
    add_header(slide6, "Deep-Dive: Dynamic Dependency DAG & Reverse-BFS RCA", "MODULE LEAD: AAKASH")

    # Left Column: Graph modeling & Traversal
    c_left = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = CYAN_ACCENT
    tf_l = c_left.text_frame
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = Inches(0.2)
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "🌲 4-Layer Dynamic DAG Architecture (graph.py)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    l_items = [
        ("Layer 1 (Pipelines)", "Upstream ingestion sources (e.g. Kafka Stream ETL, Credit Bureau API)."),
        ("Layer 2 (Features)", "Numerical/categorical feature inputs inferred directly from baseline dataset."),
        ("Layer 3 (Model)", "Active machine learning model node with health states (HEALTHY/WARNING/CRITICAL)."),
        ("Layer 4 (Services)", "Downstream consumer microservices (e.g. Checkout Gateway, Reporting API)."),
        ("Reverse-BFS (O(V+E))", "Starting from degraded Model node, traverses reverse adjacency list upstream to isolate culprit drifting feature and originating pipeline."),
        ("Forward-BFS (O(V+E))", "Traverses forward adjacency list downstream to quantify total impacted Blast Radius.")
    ]
    for h, desc in l_items:
        ph = tf_l.add_paragraph()
        ph.text = f"• {h}: {desc}"
        ph.font.size = Pt(9)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(4)

    # Right Column: RCS Formula
    c_right = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = CARD_BG
    c_right.line.color.rgb = BLUE_ACCENT
    tf_r = c_right.text_frame
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = Inches(0.2)
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "🎯 Multi-Factor Root Cause Confidence Score (RCS)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    r_items = [
        ("Mathematical Formulation", "RCS = (0.45 * DriftEvidence) + (0.30 * PerfDrop) + (0.15 * TopologyProximity) + (0.10 * BlastImpact)"),
        ("Drift Evidence (45%)", "Composite of Kolmogorov-Smirnov statistic (D) and Population Stability Index (PSI)."),
        ("Performance Drop (30%)", "Degree of rolling accuracy degradation below the model's SLA threshold."),
        ("Topology Proximity (15%)", "Shortest graph distance from candidate feature node to the active Model node in DAG."),
        ("Blast Impact (10%)", "Ratio of affected downstream production microservices."),
        ("Candidate Ranking", "Ranks all upstream features by RCS; isolates the top candidate with >85% confidence.")
    ]
    for h, desc in r_items:
        ph = tf_r.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(5)
        pd = tf_r.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 7: Deep-Dive: Krishna (Queue, Deque & Drift Analytics)
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_slide_bg(slide7)
    add_header(slide7, "Deep-Dive: Ingestion Buffer, Deque Window & Drift Engine", "MODULE LEAD: KRISHNA")

    c1 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = BLUE_ACCENT
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.2)
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "⚡ Ingestion Queue & Metric Window"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    q_items = [
        ("Circular FIFO Queue (queue.py)", "High-throughput asynchronous inference buffer (Capacity: 5000 events). Enqueue and dequeue operate in strict O(1) time using modulo pointer arithmetic."),
        ("Zero-Allocation Buffer Overflow", "When buffer fills, oldest unconsumed telemetry is dropped gracefully, preventing memory leaks during high traffic spikes."),
        ("Double-Ended Queue Window (deque.py)", "Maintains recent W = 400 prediction records. O(1) rolling append and oldest-record eviction."),
        ("Amortized O(1) Metrics", "Calculates rolling accuracy, precision, recall, and P99 latency continuously over the sliding window.")
    ]
    for h, desc in q_items:
        ph = tf1.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = TEXT_MUTED

    c2 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = RGBColor(168, 85, 247)
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.2)
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "📊 Statistical Drift Engine (detector.py)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(168, 85, 247)

    d_items = [
        ("Two-Sample Kolmogorov-Smirnov Test", "Non-parametric empirical cumulative distribution function (eCDF) test. Computes maximum vertical divergence D in O(N log N) time."),
        ("P-Value Significance Threshold", "If p-value < 0.05 (alpha = 0.05), the null hypothesis that baseline and sliding window come from the same distribution is rejected."),
        ("Population Stability Index (PSI)", "Quantifies population shift across quantile bins in O(N + B) time: PSI = SUM((Actual% - Expected%) * ln(Actual% / Expected%))."),
        ("Drift Classification", "PSI < 0.10: Stable | 0.10 <= PSI < 0.25: Moderate Warning | PSI >= 0.25: Critical Covariate Drift.")
    ]
    for h, desc in d_items:
        ph = tf2.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 8: Deep-Dive: Sanskar (Max-Heap & Retraining Gate)
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_slide_bg(slide8)
    add_header(slide8, "Deep-Dive: Incident Max-Heap & Closed-Loop Retraining", "MODULE LEAD: SANSKAR")

    c1 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = EMERALD_ACCENT
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.2)
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "⛰️ Binary Max-Heap Priority Queue (heap.py)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = EMERALD_ACCENT

    h_items = [
        ("Pure DSA Heap Implementation", "Array-backed complete binary tree built with pure _sift_up and _sift_down pointer methods (no external libraries)."),
        ("Logarithmic Complexity", "Push new incident: O(log N) | Extract maximum severity incident: O(log N) | Peek top alert: O(1)."),
        ("Composite Severity Scoring", "Severity = (AccuracyDrop * 40) + (DriftMagnitude * 40) + (BlastRadiusCount * 20)."),
        ("Thread-Safe Resolution", "Resolves and de-duplicates alerts safely in concurrent multi-threaded streaming environments.")
    ]
    for h, desc in h_items:
        ph = tf1.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = TEXT_MUTED

    c2 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = CYAN_ACCENT
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.2)
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "🔄 Closed-Loop 4-Step Validation Gate (Phase 7)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    r_items = [
        ("Step 1: Data Sufficiency Check", "Ensures sliding window has >= 20 ground-truth samples (or synthesizes recent adaptive distribution batch)."),
        ("Step 2: Candidate Model Re-Fitting", "Re-fits model parameters to the drifted distribution window, adapting decision boundaries."),
        ("Step 3: 4-Step Validation Criteria", "1) Accuracy >= SLA target | 2) P99 Latency <= SLA threshold | 3) Candidate outperforms degraded active model | 4) Non-negative R2 score."),
        ("Step 4: Zero-Downtime Promotion", "Promotes candidate, bumps version (v1.0.0 -> v1.1.0), updates HashMap baselines, resolves Max-Heap alerts, and resets DAG node health.")
    ]
    for h, desc in r_items:
        ph = tf2.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 9: Deep-Dive: Ghanshyam (Registry & Simulation)
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    add_slide_bg(slide9)
    add_header(slide9, "Deep-Dive: In-Memory Model Registry & Traffic Simulator", "MODULE LEAD: GHANSHYAM")

    c1 = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = RGBColor(168, 85, 247)
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.2)
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "🗂️ In-Memory Model Registry (registry.py)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(168, 85, 247)

    reg_items = [
        ("Hash Map Baseline Store", "O(1) average-time model metadata and empirical distribution lookup indexed by model_id and feature_name."),
        ("Empirical Distribution Moments", "Stores baseline sample vectors, mean, standard deviation, min, max, and quantiles for every registered feature."),
        ("Multi-Task Model Support", "Handles both CLASSIFICATION (Accuracy, F1-Score) and REGRESSION (MAE, RMSE, R2 Score) model metadata."),
        ("Clean Standby State", "Enables clean system boots, dynamic model switching, and full workspace resets.")
    ]
    for h, desc in reg_items:
        ph = tf1.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = TEXT_MUTED

    c2 = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = BLUE_ACCENT
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.2)
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "🚦 Universal Traffic Simulator (traffic_simulator.py)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    sim_items = [
        ("Multi-Threaded Production Streamer", "Streams synthetic inferences into EventQueue at 15-25 events/sec with realistic Gaussian feature distributions and latency noise."),
        ("Controlled Covariate Shift Injector", "Allows interactive scaling of any chosen feature distribution (e.g. 3.5x mean shift) to trigger real-time KS/PSI drift."),
        ("Latency Spike Simulation", "Simulates downstream database or network degradation by adding +250ms latency spikes."),
        ("Universal CSV Ingestion", "Parses user CSV files, infers numeric features, trains reference models, and initializes baseline distributions on the fly.")
    ]
    for h, desc in sim_items:
        ph = tf2.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 10: Deep-Dive: Hari (History, Reports & UI)
    # -------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    add_slide_bg(slide10)
    add_header(slide10, "Deep-Dive: History Drawer, Post-Mortems & Dashboard", "MODULE LEAD: HARI")

    c1 = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = RGBColor(245, 158, 11)
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.2)
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "📜 Observability Session History Drawer (history.py)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(245, 158, 11)

    hist_items = [
        ("Chronological Audit Trail", "Thread-safe ModelTestingHistory captures timestamps, event badges, rolling accuracy, P99 latency, and culprit features with O(1) prepend."),
        ("In-Place Deduplication", "Deduplicates rapid telemetry checks within 4s window to maintain clean, non-spammy session histories."),
        ("1-Click DAG Snapshot Replay", "Clicking any history entry opens a snapshot modal rendering the exact historical DAG topology and culprit highlighting."),
        ("Session Filtering", "Filter tabs categorize sessions by All, Drift Incidents, Retrained Runs, and Registered Models.")
    ]
    for h, desc in hist_items:
        ph = tf1.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = TEXT_MUTED

    c2 = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = CYAN_ACCENT
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.2)
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "📑 Post-Mortems & Interactive Web Dashboard"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    ui_items = [
        ("Downloadable Markdown Post-Mortems", "Phase 8 engine automatically exports complete incident post-mortems documenting root cause, KS/PSI stats, blast radius, and remediation logs."),
        ("Canvas 2D Topological DAG Visualization", "Custom High-DPI graph engine with animated data signal pulses, node hover inspection, and pulsating degradation halos."),
        ("FastAPI REST Endpoints", "Clean REST API powering /api/dashboard, /api/ingest, /api/history, /api/models/upload-csv, and /api/models/retrain."),
        ("Sleek Dark-Mode Aesthetics", "Custom glassmorphic styling, responsive cards, KPI pills, and real-time live telemetry polling.")
    ]
    for h, desc in ui_items:
        ph = tf2.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 11: Experimental Results & Performance Benchmarks
    # -------------------------------------------------------------
    slide11 = prs.slides.add_slide(blank_layout)
    add_slide_bg(slide11)
    add_header(slide11, "Experimental Evaluation & Unit Test Verification", "VALIDATION & BENCHMARKS")

    # 4 Stat Metric Cards
    metrics = [
        ("17 / 17 Tests Passed", "100% Pass Rate across Queue, Deque, Heap, Graph, Drift & Retraining suites.", EMERALD_ACCENT),
        ("< 0.45 ms Overhead", "Ultra-low telemetry compute latency; zero throughput impact on production models.", CYAN_ACCENT),
        ("100% Root Cause Accuracy", "Reverse-BFS consistently isolated culprit drifting features with >90% RCS confidence.", BLUE_ACCENT),
        ("v1.0.0 -> v1.1.0 Retraining", "Automated validation gate recovered accuracy from 68% back to 96% with zero downtime.", RGBColor(168, 85, 247))
    ]

    for idx, (val, label, col) in enumerate(metrics):
        cx = Inches(0.8 + idx * 2.95)
        card = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.7), Inches(2.8), Inches(1.8))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.15)
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.name = "Arial"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.name = "Calibri"
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(4)

    # Bottom summary box
    c_bot = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.8), Inches(11.73), Inches(3.1))
    c_bot.fill.solid()
    c_bot.fill.fore_color.rgb = CARD_BG
    c_bot.line.color.rgb = RGBColor(30, 41, 69)
    tf_b = c_bot.text_frame
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = Inches(0.2)
    tf_b.word_wrap = True

    p = tf_b.paragraphs[0]
    p.text = "🧪 Comprehensive Pytest Test Suite Summary (17 Unit Tests Verified)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    tests_list = [
        "• test_dsa.py (4 tests): FIFO queue order & circular overflow; rolling deque accuracy & P99 latency; max-heap priority order; DAG forward/reverse traversal.",
        "• test_drift_rca.py (3 tests): 2-sample KS test & PSI statistical drift; Reverse-BFS culprit attribution; multi-candidate RCS ranking.",
        "• test_history.py (3 tests): Chronological audit session logging; capacity overflow eviction; end-to-end orchestrator history lifecycle.",
        "• test_retraining.py (2 tests): Automated 1-click model retraining with 4-step validation gate; markdown incident post-mortem generation.",
        "• test_universal_models.py (5 tests): Clean default startup; on-demand demo showcase; dynamic DAG rebuilding; custom CSV ingestion; standby unloader."
    ]
    for t in tests_list:
        pt = tf_b.add_paragraph()
        pt.text = t
        pt.font.name = "Calibri"
        pt.font.size = Pt(9.5)
        pt.font.color.rgb = TEXT_MUTED
        pt.space_before = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 12: Conclusion & Viva Takeaways
    # -------------------------------------------------------------
    slide12 = prs.slides.add_slide(blank_layout)
    add_slide_bg(slide12)
    add_header(slide12, "Summary, Architectural Impact & Future Scope", "CONCLUSION & VIVA TAKEAWAYS")

    col_w = Inches(5.6)
    c1 = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), col_w, Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = CYAN_ACCENT
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.25)
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "🎯 Core Capstone Achievements"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    achieve = [
        ("Pure In-Memory DSA Design", "Proved that 5 core data structures (Queue, Deque, HashMap, Max-Heap, DAG) can replace heavyweight APM platforms with microsecond latency."),
        ("Automated Graph Diagnostics", "Eliminated manual RCA debugging by automatically traversing reverse DAG dependencies to pinpoint culprit features and upstream ETL origins."),
        ("Closed-Loop Self-Healing", "Built a safe, 4-step validation gate that automatically retrains candidate models and promotes them without human intervention."),
        ("Universal Compatibility", "Seamlessly supports any custom classification or regression model via CSV uploads, REST APIs, or Python client scripts.")
    ]
    for h, desc in achieve:
        ph = tf1.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(7)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = TEXT_MUTED

    c2 = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), col_w, Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = BLUE_ACCENT
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.25)
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "🔮 Future Extensions & Live Demo"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT

    future = [
        ("Phase 10: Multi-Channel Webhooks", "Automated webhook dispatching to Slack, Discord, Microsoft Teams, PagerDuty, and Email on critical alert triggers."),
        ("Deep Learning & Unstructured Data", "Extending Kolmogorov-Smirnov and PSI embedding drift checks to LLM token embeddings and computer vision models."),
        ("Multi-Cluster Distributed Graphs", "Scaling the DAG topology across distributed microservice meshes via Redis and gRPC event streaming."),
        ("Live Interactive Demonstration", "Now demonstrating live traffic simulation, drift injection, Reverse-BFS attribution, and history snapshot replay at http://127.0.0.1:8000.")
    ]
    for h, desc in future:
        ph = tf2.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(7)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = TEXT_MUTED

    # Save presentation
    output_pptx = "ArgusML_Presentation.pptx"
    prs.save(output_pptx)
    print(f"[SUCCESS] Saved presentation to {output_pptx}")


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header
        self.drawString(54, 750, "ArgusML — DSA Capstone Project Presentation Script & Defense Guide")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "Confidential — For Academic Viva & Presentation Defense")
        self.line(54, 48, 558, 48)
        self.restoreState()


def create_script_pdf():
    output_pdf = "ArgusML_Team_Presentation_Script.pdf"
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=64,
        bottomMargin=64
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=14
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0369A1"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=5
    )
    speech_style = ParagraphStyle(
        'Speech_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0F172A"),
        leftIndent=12,
        spaceAfter=6
    )
    badge_style = ParagraphStyle(
        'Badge',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0284C7")
    )
    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1E293B")
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A")
    )

    elements = []

    # Title Banner
    elements.append(Paragraph("ArgusML: Complete Team Presentation Script & Viva Defense Guide", title_style))
    elements.append(Paragraph("<b>5-Member Project Distribution:</b> Aakash (Lead), Krishna, Sanskar, Ghanshyam, Hari | <b>Total Unit Tests:</b> 17/17 Passed", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=0, spaceAfter=12))

    # SECTION 1: Team Distribution Summary Table
    elements.append(Paragraph("1. Team Distribution & Module Ownership Matrix", h1_style))
    elements.append(Paragraph("This matrix outlines the exact technical ownership, data structures, algorithms, and source files for each of the 5 team members:", body_style))

    team_table_data = [
        [
            Paragraph("Team Member", table_cell_bold),
            Paragraph("Module & Role", table_cell_bold),
            Paragraph("DSA Concepts Implemented", table_cell_bold),
            Paragraph("Time / Space Complexity", table_cell_bold),
            Paragraph("Code Files Executed", table_cell_bold),
        ],
        [
            Paragraph("<b>Aakash</b><br/>(Project Lead)", table_cell),
            Paragraph("Dynamic 4-Layer DAG & Reverse-BFS Root Cause Engine", table_cell),
            Paragraph("• Directed Acyclic Graph (DAG)<br/>• Reverse-BFS Upstream Attribution<br/>• Forward-BFS Blast Radius<br/>• Multi-Factor RCS Scoring", table_cell),
            Paragraph("• Reverse-BFS: <b>O(V + E)</b><br/>• Forward-BFS: <b>O(V + E)</b><br/>• Space: <b>O(V + E)</b>", table_cell),
            Paragraph("<code>dsa/graph.py</code><br/><code>rca/engine.py</code><br/><code>orchestrator.py</code>", table_cell),
        ],
        [
            Paragraph("<b>Krishna</b><br/>(Co-Lead)", table_cell),
            Paragraph("Ingestion Queue, Sliding Window & Statistical Drift", table_cell),
            Paragraph("• Circular FIFO EventQueue<br/>• Double-Ended Queue (Deque)<br/>• 2-Sample Kolmogorov-Smirnov<br/>• Population Stability Index", table_cell),
            Paragraph("• Queue Enqueue: <b>O(1)</b><br/>• Deque Evict: <b>O(1)</b><br/>• KS Test: <b>O(N log N)</b><br/>• PSI: <b>O(N + B)</b>", table_cell),
            Paragraph("<code>dsa/queue.py</code><br/><code>dsa/deque.py</code><br/><code>drift/detector.py</code>", table_cell),
        ],
        [
            Paragraph("<b>Sanskar</b><br/>(Analytical Lead)", table_cell),
            Paragraph("Incident Max-Heap & 1-Click Retraining Validation Gate", table_cell),
            Paragraph("• Array-backed Binary Max-Heap<br/>• Custom _sift_up / _sift_down<br/>• Closed-Loop Validation Gate<br/>• Automated Version Promotion", table_cell),
            Paragraph("• Push Incident: <b>O(log N)</b><br/>• Pop Max: <b>O(log N)</b><br/>• Peek Top Alert: <b>O(1)</b><br/>• Retrain Check: <b>O(S)</b>", table_cell),
            Paragraph("<code>dsa/heap.py</code><br/><code>simulator/universal_runner.py</code><br/><code>orchestrator.py</code>", table_cell),
        ],
        [
            Paragraph("<b>Ghanshyam</b><br/>(Core Systems)", table_cell),
            Paragraph("In-Memory Model Registry & Multi-Model Traffic Simulator", table_cell),
            Paragraph("• In-Memory Hash Map Store<br/>• Empirical Moments Baseline<br/>• Background Traffic Synthesizer<br/>• Controlled Covariate Drift", table_cell),
            Paragraph("• Baseline Lookup: <b>O(1)</b><br/>• Model Switch: <b>O(1)</b><br/>• Traffic Stream: <b>O(K)</b>", table_cell),
            Paragraph("<code>dsa/registry.py</code><br/><code>simulator/traffic_simulator.py</code><br/><code>simulator/universal_runner.py</code>", table_cell),
        ],
        [
            Paragraph("<b>Hari</b><br/>(Observability & UI)", table_cell),
            Paragraph("Session History Drawer, Post-Mortems & Interactive UI", table_cell),
            Paragraph("• Chronological Audit History<br/>• 1-Click DAG Snapshot Replay<br/>• Markdown Report Synthesizer<br/>• Canvas 2D Graph Engine", table_cell),
            Paragraph("• Fast Prepend: <b>O(1)</b><br/>• Snapshot Lookup: <b>O(1)</b><br/>• Report Export: <b>O(R)</b>", table_cell),
            Paragraph("<code>dsa/history.py</code><br/><code>app/main.py</code><br/><code>frontend/js/app.js</code><br/><code>frontend/js/graph_renderer.js</code>", table_cell),
        ],
    ]

    t_team = Table(team_table_data, colWidths=[68, 105, 125, 95, 111])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_team)
    elements.append(Spacer(1, 14))

    # SECTION 2: Complete Word-for-Word Slide Presentation Script
    elements.append(Paragraph("2. Slide-by-Slide Word-for-Word Presentation Script", h1_style))
    elements.append(Paragraph("Follow this chronological speaking sequence during the group presentation. Each speaker covers their specific slides and hands over cleanly to the next speaker:", body_style))
    elements.append(Spacer(1, 6))

    # Slide 1 & 2 (Aakash)
    elements.append(Paragraph("🎤 Slide 1 & 2: Introduction & Team Division (Speaker: AAKASH)", h2_style))
    elements.append(Paragraph("<b>Exact Words to Speak:</b>", body_style))
    elements.append(Paragraph(
        '"Respected professors and panel members, good morning. Today, our team is presenting <b>ArgusML</b> — a Universal Production AI Observability and Graph-Powered Root Cause Diagnostic Platform built upon 5 foundational Data Structures and Algorithms.<br/><br/>'
        'In today’s presentation, we have divided the technical modules cleanly among 5 team members:<br/>'
        '• <b>I (Aakash)</b> am leading the system architecture, dynamic 4-layer DAG topology modeling, and Reverse-BFS root cause attribution.<br/>'
        '• <b>Krishna</b> will present the high-throughput circular FIFO ingestion queue, sliding window deque, and Kolmogorov-Smirnov statistical drift engine.<br/>'
        '• <b>Sanskar</b> will explain the binary max-heap priority queue and the closed-loop automated model retraining validation gate.<br/>'
        '• <b>Ghanshyam</b> will detail the in-memory hash map model registry and universal multi-model traffic simulation engine.<br/>'
        '• <b>Hari</b> will showcase our session history audit drawer, 1-click historical snapshot replay, and downloadable markdown post-mortem generator.<br/><br/>'
        'Let us begin with the core problem that motivated this project."',
        speech_style
    ))

    # Slide 3 & 4 (Aakash)
    elements.append(Paragraph("🎤 Slide 3 & 4: Problem Statement, Novelty & DSA Mapping (Speaker: AAKASH)", h2_style))
    elements.append(Paragraph(
        '"Unlike traditional web servers that throw 500 internal errors when they break, machine learning models fail silently. Real-world consumer behavior shifts, causing data distributions to drift, while the model continues making confident, incorrect predictions. When a model’s accuracy drops from 95% to 65%, data engineering teams waste days manually tracing through dozens of multi-table ETL pipelines to isolate which specific feature was corrupted.<br/><br/>'
        'ArgusML solves this by implementing an entirely in-memory, pure DSA architecture with zero third-party vendor bloat. As shown in our DSA Mapping table on Slide 4, every system component maps directly to optimal theoretical complexity:<br/>'
        '1. Circular FIFO Buffer for O(1) ingestion without memory overflow.<br/>'
        '2. Double-Ended Queue for amortized O(1) rolling performance metrics.<br/>'
        '3. In-Memory Hash Map for O(1) model and baseline empirical distribution lookups.<br/>'
        '4. Binary Max-Heap for O(log N) composite severity prioritization.<br/>'
        '5. Dynamic Directed Acyclic Graph (DAG) for O(V+E) reverse and forward BFS traversals.<br/><br/>'
        'I will now hand over to Krishna to explain how live predictions enter the system and how statistical drift is detected."',
        speech_style
    ))

    # Slide 5 & 7 (Krishna)
    elements.append(Paragraph("🎤 Slide 5 & 7: Ingestion Queue, Deque Window & Drift Analytics (Speaker: KRISHNA)", h2_style))
    elements.append(Paragraph(
        '"Thank you, Aakash. I will now explain how ArgusML continuously watches streaming inferences and detects distribution shifts.<br/><br/>'
        'When client applications send inference payloads to <code>POST /api/ingest</code>, they enter our <b>Circular FIFO EventQueue</b> (<code>queue.py</code>). We implemented modulo pointer arithmetic so that enqueuing and dequeuing operate strictly in O(1) time with a fixed capacity of 5,000 events. If an extreme traffic spike occurs, oldest unconsumed records are evicted gracefully, completely preventing memory leaks.<br/><br/>'
        'Next, a background stream processor dequeues batches into our <b>MetricSlidingWindow</b> (<code>deque.py</code>), which is an in-memory double-ended queue holding recent W = 400 predictions. This allows us to calculate rolling accuracy, precision, recall, and P99 latency in amortized O(1) time.<br/><br/>'
        'Every 25 processed events, our <b>DriftEngine</b> (<code>detector.py</code>) executes two statistical tests against the baseline distributions stored in our Hash Map:<br/>'
        '1. <b>Two-Sample Kolmogorov-Smirnov (KS) Test:</b> We compute the maximum vertical divergence D between the baseline empirical cumulative distribution function (eCDF) and the sliding window in O(N log N) time. If p < 0.05, we flag significant covariate drift.<br/>'
        '2. <b>Population Stability Index (PSI):</b> We bucket feature values across quantile bins in O(N + B) time. A PSI >= 0.25 indicates critical distribution shift.<br/><br/>'
        'Once drift is detected, Aakash’s DAG engine is triggered to isolate the root cause."',
        speech_style
    ))

    # Slide 6 (Aakash - DAG Deep Dive)
    elements.append(Paragraph("🎤 Slide 6: Dynamic DAG & Root Cause Confidence Scoring (Speaker: AAKASH)", h2_style))
    elements.append(Paragraph(
        '"Once statistical drift is flagged, our <b>DependencyGraph</b> (<code>graph.py</code>) performs automated root cause attribution.<br/><br/>'
        'The DAG dynamically builds a 4-layer topology:<br/>'
        '<code>Upstream Pipelines → Inferred Features → Active Model → Downstream Services</code>.<br/><br/>'
        'We execute two Breadth-First Search traversals, both operating in O(V + E) linear time:<br/>'
        '1. <b>Reverse-BFS Upstream Attribution:</b> Starting at the degraded Model node, we traverse reverse adjacency lists upstream to find which specific feature node and upstream ingestion pipeline originated the corruption.<br/>'
        '2. <b>Forward-BFS Downstream Blast Radius:</b> We traverse forward adjacency lists downstream from the model node to identify every production consumer API and reporting service impacted.<br/><br/>'
        'To rank candidate causes with mathematical rigor, I designed the <b>Root Cause Confidence Score (RCS)</b> formula:<br/>'
        '<code>RCS = (0.45 * DriftEvidence) + (0.30 * AccuracyDrop) + (0.15 * TopologyProximity) + (0.10 * BlastImpact)</code>.<br/>'
        'This pinpoints the true culprit feature with over 85% to 95% confidence.<br/><br/>'
        'I will now hand over to Sanskar to explain how incidents are prioritized in the Max-Heap and how automated retraining cures the model."',
        speech_style
    ))

    # Slide 8 (Sanskar)
    elements.append(Paragraph("🎤 Slide 8: Priority Max-Heap & 1-Click Retraining Validation Gate (Speaker: SANSKAR)", h2_style))
    elements.append(Paragraph(
        '"Thank you, Aakash. I will now explain our <b>AlertMaxHeap</b> and the <b>Closed-Loop Automated Model Retraining Pipeline</b>.<br/><br/>'
        'In production environments monitoring multiple models, alerts must be prioritized so SREs tackle the most dangerous failures first. We implemented a pure, array-backed <b>Binary Max-Heap</b> (<code>heap.py</code>) using pure <code>_sift_up</code> and <code>_sift_down</code> pointer swaps. Pushing a new incident and extracting the maximum severity incident both run in strict O(log N) time, while peeking the top incident is O(1). Incidents are ranked by composite severity taking into account accuracy drop, drift magnitude, and blast radius.<br/><br/>'
        'When an incident occurs, our <b>Automated Retraining Engine</b> (<code>orchestrator.py</code>) allows 1-click remediation with a strict <b>4-Step Validation Gate</b>:<br/>'
        '1. It collects recent sliding window observations and fits a candidate model to the drifted distribution.<br/>'
        '2. It evaluates 4 validation criteria: Data sufficiency, Accuracy >= SLA target, Latency <= SLA threshold, and positive R² score.<br/>'
        '3. If validation passes, the candidate is promoted to production, the version is bumped (e.g. v1.0.0 → v1.1.0), Hash Map baselines are refreshed, active Max-Heap alerts are resolved, and DAG node health resets to HEALTHY.<br/><br/>'
        'I will now pass to Ghanshyam to explain our Model Registry and Traffic Simulator."',
        speech_style
    ))

    # Slide 9 (Ghanshyam)
    elements.append(Paragraph("🎤 Slide 9: Model Registry & Universal Traffic Simulator (Speaker: GHANSHYAM)", h2_style))
    elements.append(Paragraph(
        '"Thank you, Sanskar. I will cover the <b>ModelRegistry</b> and our <b>Universal Traffic Simulation Engine</b>.<br/><br/>'
        'The <b>ModelRegistry</b> (<code>registry.py</code>) serves as our central in-memory Hash Map baseline store. It provides O(1) constant-time lookup for model metadata, SLA thresholds, and empirical baseline distribution moments (mean, variance, min, max, and quantiles). It universally supports both <b>Classification models</b> (tracking Accuracy and F1) and <b>Regression models</b> (tracking MAE, RMSE, and R²).<br/><br/>'
        'To enable comprehensive testing without external hardware, I built the <b>UniversalTrafficSimulator</b> (<code>traffic_simulator.py</code>). It runs a background streaming thread pushing realistic predictions with Gaussian noise into the EventQueue at 20 events per second. It features controlled covariate shift injection — allowing users to dynamically multiply any feature’s distribution by 3.5x or spike latency by +250ms with a single click.<br/><br/>'
        'Furthermore, our CSV upload parser automatically extracts numerical columns, fits reference models, registers baselines in HashMap, and builds dynamic DAG topologies on the fly.<br/><br/>'
        'I now hand over to Hari to present our session audit history, post-mortem generator, and user interface."',
        speech_style
    ))

    # Slide 10, 11 & 12 (Hari)
    elements.append(Paragraph("🎤 Slide 10, 11 & 12: Session History, Post-Mortems & Live Demo (Speaker: HARI)", h2_style))
    elements.append(Paragraph(
        '"Thank you, Ghanshyam. I will present our <b>Testing & Observability Session History Drawer</b>, <b>Incident Post-Mortem Exporter</b>, and the front-end dashboard.<br/><br/>'
        'In production, auditability is essential. We implemented <b>ModelTestingHistory</b> (<code>history.py</code>), which maintains a thread-safe chronological record of all model registrations, live drift detections, retraining runs, and switches. New session snapshots are prepended in O(1) time. With our <b>1-Click Historical Snapshot Replay</b>, clicking any card in the drawer immediately loads the exact DAG topology canvas, statistical indicators (KS/PSI), and blast radius captured during that test run.<br/><br/>'
        'Our <b>Incident Post-Mortem Generator</b> automatically exports a comprehensive Markdown report documenting the executive summary, primary culprit feature, candidate RCS confidence rankings, impacted downstream services, and remediation logs.<br/><br/>'
        'Finally, our web dashboard is built with clean Vanilla HTML5, CSS3, and an interactive Canvas 2D DAG renderer with pulsating node halos. All 17 unit tests in our Pytest suite pass with 100% success.<br/><br/>'
        'We are now ready for the live demonstration and panel questions."',
        speech_style
    ))
    elements.append(Spacer(1, 14))

    # SECTION 3: Individual Code Breakdown & File Execution
    elements.append(Paragraph("3. Individual Code Breakdown & Files Executed", h1_style))
    elements.append(Paragraph("Use this section during technical viva when professors ask: <i>'Which specific files and code functions did you write and execute?'</i>", body_style))

    code_breakdown = [
        ("Aakash (Lead)", [
            ("backend/app/core/dsa/graph.py", "Implemented DependencyGraph class with forward_adj and reverse_adj adjacency lists. Built build_topology_for_model(), get_upstream_nodes(model_id) via Reverse-BFS, and get_downstream_nodes(model_id) via Forward-BFS."),
            ("backend/app/core/rca/engine.py", "Built RootCauseAnalysisEngine and diagnose_model(). Formulated the 4-factor Root Cause Confidence Score (RCS) weighting drift evidence, accuracy drop, graph proximity, and blast radius."),
            ("backend/app/core/orchestrator.py", "Architected ArgusSystem singleton orchestrator coordinating EventQueue, MetricSlidingWindow, DriftEngine, AlertMaxHeap, and ModelRegistry.")
        ]),
        ("Krishna", [
            ("backend/app/core/dsa/queue.py", "Built EventQueue circular buffer with head/tail pointers, modulo wrapping self.tail = (self.tail + 1) % self.capacity, and enqueue()/dequeue() O(1) operations."),
            ("backend/app/core/dsa/deque.py", "Built MetricSlidingWindow using collections.deque with fixed maxlen. Built get_performance_metrics() and get_latency_metrics() for rolling P99 latency."),
            ("backend/app/core/drift/detector.py", "Built DriftEngine implementing compute_ks_test() using scipy.stats.ks_2samp and compute_psi() with quantile binning.")
        ]),
        ("Sanskar", [
            ("backend/app/core/dsa/heap.py", "Built AlertMaxHeap with pure _sift_up and _sift_down array methods. Built push(), pop_max(), peek(), and resolve(alert_id) for O(log N) incident ranking."),
            ("backend/app/core/simulator/universal_runner.py", "Built evaluate_validation_gate() implementing the 4-step validation criteria (data sufficiency, accuracy recovery, latency check, non-negative R2)."),
            ("backend/app/core/orchestrator.py", "Built retrain_active_model() executing candidate fitting, version bumping (v1.0.0 -> v1.1.0), Max-Heap alert clearing, and node health resets.")
        ]),
        ("Ghanshyam", [
            ("backend/app/core/dsa/registry.py", "Built ModelRegistry and ModelMetadata classes. Implemented register_model(), get_model(), register_feature_baseline(), and moments calculation in O(1) HashMap."),
            ("backend/app/core/simulator/traffic_simulator.py", "Built UniversalTrafficSimulator running background thread _stream_loop() generating synthetic inferences with Gaussian noise and latency spikes."),
            ("backend/app/core/simulator/universal_runner.py", "Built UniversalModel wrapper supporting both Classification and Regression scikit-learn models.")
        ]),
        ("Hari", [
            ("backend/app/core/dsa/history.py", "Built ModelTestingHistory and TestSessionRecord dataclass. Implemented record_session() with in-place deduplication and get_history()."),
            ("backend/app/main.py", "Built FastAPI REST API exposing /api/dashboard, /api/history, /api/history/{id}, /api/models/upload-csv, and /api/alerts/{id}/report."),
            ("frontend/js/app.js & graph_renderer.js", "Built Canvas 2D interactive DAG topology renderer, session history drawer renderer, snapshot inspection modal, and toast notification engine.")
        ])
    ]

    for name, files in code_breakdown:
        elements.append(Paragraph(f"<b>{name}:</b>", h2_style))
        for fpath, fdesc in files:
            elements.append(Paragraph(f"• <b><code>{fpath}</code></b>: {fdesc}", body_style))
        elements.append(Spacer(1, 4))

    elements.append(Spacer(1, 10))

    # SECTION 4: Expected Viva Questions & High-Scoring Answers
    elements.append(Paragraph("4. Expected Professor Viva Q&A Guide (High-Scoring Answers)", h1_style))

    viva_qa = [
        ("Q1 (For Aakash): Why did you choose Reverse-BFS over Dijkstra or DFS for Root Cause Analysis?",
         "Answer: In a dependency DAG where all dependency relationships are discrete unweighted links between upstream ETL pipelines, features, and model nodes, Breadth-First Search (BFS) explores dependencies layer by layer in strictly optimal O(V + E) time. Dijkstra would add unnecessary O(E log V) heap overhead for unweighted edges, while DFS can explore deep non-critical paths first. Reverse-BFS guarantees finding the nearest upstream corrupted feature with shortest topological proximity first."),

        ("Q2 (For Krishna): How does the Circular FIFO Queue prevent memory overflow during traffic spikes?",
         "Answer: Our EventQueue allocates a fixed circular buffer of capacity C = 5000 using modulo pointer wrapping: self.tail = (self.tail + 1) % self.capacity. When the queue is full (size == capacity), new events overwrite the oldest unconsumed entry and increment a dropped_events counter. This ensures O(1) constant-time ingestion while guaranteeing memory usage never exceeds the pre-allocated buffer size."),

        ("Q3 (For Sanskar): Why is a Binary Max-Heap superior to an array or sorted list for incident management?",
         "Answer: An unsorted array requires O(N) linear time to search for the highest-severity alert, which is too slow in high-throughput systems. A sorted array requires O(N) time on every new alert insertion. A Binary Max-Heap provides the optimal theoretical balance: O(log N) insertion via _sift_up and O(log N) extraction of the critical alert via _sift_down, while peeking the active top alert is instantaneous O(1)."),

        ("Q4 (For Ghanshyam): How does ModelRegistry achieve O(1) baseline retrieval, and how does it support multiple models?",
         "Answer: ModelRegistry is backed by Python's in-memory Hash Map (dictionary) indexed by unique model_id strings. Each ModelMetadata record maintains an inner hash map feature_baselines mapping feature names to EmpiricalBaseline objects containing baseline sample arrays and statistical moments. Hash map bucket indexing provides O(1) average-time retrieval regardless of how many models are registered in the platform."),

        ("Q5 (For Hari): How does the Session History Drawer capture and replay historical DAG snapshots?",
         "Answer: When a drift incident, model switch, or retraining occurs, ModelTestingHistory captures a deep-copy snapshot of the graph adjacency list and node health states inside TestSessionRecord.graph_snapshot. When a user clicks a historical record in the UI, our frontend GraphRenderer reads that snapshot and replays the exact canvas topology and red-highlighted culprit nodes without needing to roll back active live production telemetry.")
    ]

    for q, a in viva_qa:
        elements.append(Paragraph(f"<b>{q}</b>", h2_style))
        elements.append(Paragraph(a, body_style))
        elements.append(Spacer(1, 4))

    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Saved script PDF to {output_pdf}")


if __name__ == "__main__":
    create_presentation()
    create_script_pdf()
