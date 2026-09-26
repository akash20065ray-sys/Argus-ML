"""
ArgusML Presentation Generator (CrimsonOrbit High-Contrast Professional Theme).
Features:
- CrimsonOrbit Color Palette (Background: #0F1219, Cards: #191E2A, Accents: #EB3C3C Crimson & #F59E0B Gold, Text: #FFFFFF & #CBD5E1)
- Highly visible typography (large font sizes 11-26pt, high contrast)
- Slide 3: Literature Review & Theoretical Positioning (as requested!)
- Native High-Impact System Architecture Slide Layout with crisp layer cards and data flow
- Slide 12: Team Roles & Contribution Breakdown
- Slide 13: Experimental Results & Live Demo
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_crimson_orbit_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 Widescreen
    prs.slide_height = Inches(7.5)

    # CrimsonOrbit Exact Palette
    BG_DARK = RGBColor(15, 18, 25)          # #0F1219 Clean Dark Slate
    BG_CARD = RGBColor(25, 30, 42)          # #191E2A High-Contrast Card Navy
    BG_CARD_ALT = RGBColor(30, 36, 50)      # #1E2432 Lighter Card
    BORDER_CRIMSON = RGBColor(235, 60, 60)  # #EB3C3C Vibrant Crimson Red
    BORDER_GOLD = RGBColor(245, 158, 11)    # #F59E0B Warm Amber Gold
    BORDER_CYAN = RGBColor(56, 189, 248)    # #38BDF8 Sky Blue
    BORDER_GREEN = RGBColor(16, 185, 129)   # #10B981 Emerald Green
    TEXT_WHITE = RGBColor(255, 255, 255)    # #FFFFFF Pure Crisp White
    TEXT_OFFWHITE = RGBColor(241, 245, 249) # #F1F5F9 Off White
    TEXT_MUTED = RGBColor(203, 213, 225)    # #CBD5E1 Light Slate Gray
    TEXT_GOLD = RGBColor(252, 211, 77)      # #FCD34D Bright Pale Gold
    TEXT_CRIMSON = RGBColor(252, 165, 165)  # #FCA5A5 Light Crimson

    blank_layout = prs.slide_layouts[6]

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="ARGUSML • PRODUCTION AI OBSERVABILITY"):
        # Category Badge Box
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.73), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = category_text.upper()
        p1.font.name = "Arial"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = BORDER_CRIMSON

        p2 = tf.add_paragraph()
        p2.text = title_text
        p2.font.name = "Arial"
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(3)

        # Underline accent bar
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.48), Inches(11.73), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_CRIMSON
        line.line.fill.background()

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Crimson Orbit Style)
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)

    # Accent side bar
    side_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.3), Inches(0.12), Inches(3.2))
    side_bar.fill.solid()
    side_bar.fill.fore_color.rgb = BORDER_CRIMSON
    side_bar.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.1), Inches(1.2), Inches(11.2), Inches(3.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "DATA STRUCTURES & ALGORITHMS CAPSTONE PROJECT • VIT PUNE"
    p_badge.font.name = "Arial"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = BORDER_GOLD

    p_t = tf1.add_paragraph()
    p_t.text = "ArgusML: Universal Production AI Observability &\nGraph-Powered Root Cause Diagnostics"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(28)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE
    p_t.space_before = Pt(8)

    p_sub = tf1.add_paragraph()
    p_sub.text = "An in-memory observability platform built upon 5 foundational data structures for continuous drift detection, reverse DAG attribution, max-heap incident prioritization, and automated model retraining."
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_before = Pt(10)

    # Team Card
    card_t = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.8), Inches(11.73), Inches(2.1))
    card_t.fill.solid()
    card_t.fill.fore_color.rgb = BG_CARD
    card_t.line.color.rgb = BORDER_CRIMSON
    card_t.line.width = Pt(2.0)

    tf_t = card_t.text_frame
    tf_t.margin_left = Inches(0.3)
    tf_t.margin_top = Inches(0.2)
    pt1 = tf_t.paragraphs[0]
    pt1.text = "PROJECT TEAM MEMBERS & MODULE OWNERSHIP:"
    pt1.font.name = "Arial"
    pt1.font.size = Pt(11)
    pt1.font.bold = True
    pt1.font.color.rgb = BORDER_GOLD

    pt2 = tf_t.add_paragraph()
    pt2.text = "• Aakash (Lead): System Orchestrator, 4-Layer Dynamic DAG Topology & Reverse-BFS Root Cause Attribution\n" \
               "• Krishna: High-Throughput Circular FIFO Ingestion Queue, Deque Sliding Window & KS/PSI Statistical Drift Engine\n" \
               "• Sanskar: Binary Max-Heap Priority Alert Queue & Automated 1-Click Retraining Validation Gate\n" \
               "• Ghanshyam: Hash Map Baseline Model Registry & Universal Multi-Model Traffic Simulation Engine\n" \
               "• Hari: Session History Audit Drawer, 1-Click Snapshot Replay & Markdown Incident Post-Mortem Exporter"
    pt2.font.name = "Calibri"
    pt2.font.size = Pt(11)
    pt2.font.color.rgb = TEXT_OFFWHITE
    pt2.space_before = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 2: Problem Statement & Industry Context
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "The Silent Decay of Machine Learning in Production", "PROBLEM STATEMENT & INDUSTRY MOTIVATION")

    col_w = Inches(5.65)
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), col_w, Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = BG_CARD
    c1.line.color.rgb = BORDER_CRIMSON
    c1.line.width = Pt(2.0)
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.25)
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "🚨 Critical Failure Modes in Production ML"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BORDER_CRIMSON

    probs = [
        ("Silent Model Failure", "Unlike web servers that return HTTP 500 errors, ML models fail silently — confidently producing wrong predictions as input distributions drift over time."),
        ("No Upstream Root-Cause Pinpointing", "When accuracy degrades, data teams take days manually inspecting multi-table ETL pipelines to isolate which specific input feature became corrupted."),
        ("SRE Alert Fatigue", "Generic monitoring tools flood engineers with hundreds of uncorrelated metrics without mathematical severity ranking."),
        ("Manual Retraining Hazards", "Data scientists retrain models manually without automated validation gates, often accidentally deploying regressed models.")
    ]
    for h, desc in probs:
        ph = tf1.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(11)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(8)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10)
        pd.font.color.rgb = TEXT_MUTED

    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), col_w, Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = BG_CARD
    c2.line.color.rgb = BORDER_GOLD
    c2.line.width = Pt(2.0)
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.25)
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "🎯 Engineering Objectives of ArgusML"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

    objs = [
        ("Sub-Millisecond Ingestion & Telemetry", "Process streaming production inferences in O(1) time without adding latency to live inference APIs (<0.45 ms)."),
        ("Statistical Drift Detection", "Continuously measure divergence using 2-sample Kolmogorov-Smirnov test and Population Stability Index (PSI)."),
        ("Automated Graph-Based Attribution", "Model relationships as a 4-layer dynamic DAG to isolate culprit features via Reverse-BFS in O(V+E) time."),
        ("Closed-Loop Self-Healing Gate", "Automate 1-click candidate retraining with a 4-step validation gate before zero-downtime production promotion.")
    ]
    for h, desc in objs:
        ph = tf2.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(11)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(8)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10)
        pd.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 3: Literature Review & Academic Background (Requested!)
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "Literature Review & Theoretical Positioning", "ACADEMIC SURVEY & PRIOR ART")

    c_lit1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.65), Inches(5.2))
    c_lit1.fill.solid()
    c_lit1.fill.fore_color.rgb = BG_CARD
    c_lit1.line.color.rgb = BORDER_CYAN
    c_lit1.line.width = Pt(2.0)
    tf_l1 = c_lit1.text_frame
    tf_l1.margin_left = tf_l1.margin_right = tf_l1.margin_top = Inches(0.25)
    tf_l1.word_wrap = True

    p = tf_l1.paragraphs[0]
    p.text = "📚 Literature Survey on Distribution Shift"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_CYAN

    lit_points = [
        ("Covariate Shift (Shimodaira, 2000)", "P(X) shifts while P(Y|X) remains constant. Common in upstream ETL sensor calibration or demographic shifts."),
        ("Concept Drift (Widmer & Kubat, 1996)", "P(Y|X) changes over time (e.g. macro-economic shocks altering loan default probability)."),
        ("Statistical Distance Benchmarks", "Surveyed Kolmogorov-Smirnov, Population Stability Index (PSI), Wasserstein Distance, and Kullback-Leibler (KL) Divergence."),
        ("Why KS & PSI in ArgusML?", "2-sample KS test provides non-parametric shape divergence with exact p-values (O(N log N)); PSI provides quantile-calibrated stability thresholds (O(N+B)).")
    ]
    for h, desc in lit_points:
        ph = tf_l1.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10.5)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf_l1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = TEXT_MUTED

    c_lit2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.65), Inches(5.2))
    c_lit2.fill.solid()
    c_lit2.fill.fore_color.rgb = BG_CARD
    c_lit2.line.color.rgb = BORDER_GOLD
    c_lit2.line.width = Pt(2.0)
    tf_l2 = c_lit2.text_frame
    tf_l2.margin_left = tf_l2.margin_right = tf_l2.margin_top = Inches(0.25)
    tf_l2.word_wrap = True

    p = tf_l2.paragraphs[0]
    p.text = "⚖️ Comparative Analysis: ArgusML vs Industry"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

    comp_points = [
        ("Evidently AI / Great Expectations", "Primarily offline batch statistical profile generators. Lack real-time dependency DAG modeling and upstream root-cause traversal."),
        ("Prometheus / Datadog APM", "Heavy infrastructure focus (CPU/RAM). Blind to statistical feature distribution shifts and algorithmic failure modes."),
        ("ArgusML Novelty 1 (In-Memory DSA)", "Replaces heavy distributed broker stacks with 5 pure in-memory data structures executing in <0.45 ms."),
        ("ArgusML Novelty 2 (Reverse-BFS Attribution)", "First platform to combine statistical KS/PSI tests with 4-layer DAG Reverse-BFS for automated upstream attribution.")
    ]
    for h, desc in comp_points:
        ph = tf_l2.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10.5)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf_l2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 4: Proposed Solution & Core Innovation
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "ArgusML: In-Memory 5-DSA Observability Platform", "PROPOSED SOLUTION & NOVELTY")

    sol_boxes = [
        ("1. Pure In-Memory DSA Core", "Zero third-party vendor bloat. Built entirely from foundational data structures for microsecond execution (<0.45 ms).", BORDER_CRIMSON),
        ("2. Real-Time Drift Watchdog", "Continuous 2-sample KS-test and PSI quantile binning against HashMap empirical baselines every 25 streaming predictions.", BORDER_GOLD),
        ("3. Topological RCA (Reverse-BFS)", "Traverses reverse graph adjacency lists in O(V+E) to isolate culprit features and calculate multi-factor Root Cause Confidence (RCS).", BORDER_CYAN),
        ("4. Priority Max-Heap Queue", "Maintains active incidents ranked by composite severity score (accuracy drop, drift intensity, blast radius) in O(log N) time.", BORDER_CRIMSON),
        ("5. 4-Step Closed-Loop Gate", "Automated candidate retraining with 4-step validation criteria before promoting to production (v1.0.0 -> v1.1.0).", BORDER_GOLD),
        ("6. Session History & Snapshot Replay", "ChatGPT-style chronological session audit drawer with 1-click interactive DAG topology replays and markdown post-mortems.", BORDER_GREEN),
    ]

    for idx, (title, desc, col) in enumerate(sol_boxes):
        row = idx // 3
        col_pos = idx % 3
        bx = Inches(0.8 + col_pos * 4.0)
        by = Inches(1.7 + row * 2.7)

        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, Inches(3.75), Inches(2.4))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = col
        card.line.width = Pt(2.0)

        tf = card.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Arial"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_OFFWHITE
        p2.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 5: System Architecture & Data Flow (Clean Visual Native Layout)
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "System Architecture & Master Telemetry Pipeline", "SYSTEM ARCHITECTURE & DESIGN")

    # 5 Horizontal Architecture Layer Cards
    layers = [
        ("Layer 1: Ingestion Buffer", "Circular FIFO EventQueue", "O(1) Enqueue / Dequeue • Modulo pointer arithmetic • 5,000 capacity • Zero-allocation overflow drop", BORDER_GOLD),
        ("Layer 2: Rolling Telemetry", "MetricSlidingWindow (Deque)", "O(1) Amortized compute • Rolling Accuracy, Precision, F1 • Rolling P50, P95, P99 Latency (ms)", BORDER_CRIMSON),
        ("Layer 3: Statistical Drift", "DriftEngine & ModelRegistry", "O(1) HashMap baseline lookup • Two-Sample KS-Test (D stat, p-val) • PSI (Quantile Binning >= 0.25)", BORDER_CYAN),
        ("Layer 4: Topological RCA", "Dynamic DependencyGraph", "O(V+E) Dynamic 4-layer DAG • Reverse-BFS Upstream Attribution • Forward-BFS Downstream Blast Radius", BORDER_GOLD),
        ("Layer 5: Priority Alert Heap", "AlertMaxHeap Priority Queue", "O(log N) Push / Pop • Pure _sift_up / _sift_down • Composite severity scoring • 1-Click Retraining Gate", BORDER_GREEN),
    ]

    card_h = Inches(0.92)
    gap_h = Inches(0.12)
    top_start = Inches(1.7)

    for idx, (l_title, dsa_name, desc, col) in enumerate(layers):
        cy = top_start + idx * (card_h + gap_h)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), cy, Inches(11.73), card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = col
        card.line.width = Pt(1.8)

        tf = card.text_frame
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.12)
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"{l_title}  ➔  {dsa_name}"
        p1.font.name = "Arial"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_OFFWHITE
        p2.space_before = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 6: Core DSA Foundations & Theoretical Complexity Table
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Core DSA Mapping & Theoretical Complexity Analysis", "DATA STRUCTURES & ALGORITHMS FOUNDATION")

    rows, cols = 6, 5
    table_shape = s6.shapes.add_table(rows, cols, Inches(0.8), Inches(1.7), Inches(11.73), Inches(5.1))
    tbl = table_shape.table

    col_widths = [Inches(2.2), Inches(2.3), Inches(3.0), Inches(2.2), Inches(2.03)]
    for idx, w in enumerate(col_widths):
        tbl.columns[idx].width = w

    headers = ["Data Structure", "ArgusML Component", "System Purpose & Implementation", "Time Complexity", "Space Complexity"]
    for idx, text in enumerate(headers):
        cell = tbl.cell(0, idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(40, 20, 30)
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = BORDER_GOLD
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
            cell.fill.fore_color.rgb = BG_CARD if row_idx % 2 == 1 else BG_CARD_ALT
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Calibri"
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_OFFWHITE
            if col_idx in [0, 3]:
                p.font.bold = True
                if col_idx == 0:
                    p.font.color.rgb = BORDER_GOLD
                elif col_idx == 3:
                    p.font.color.rgb = TEXT_GOLD

    # -------------------------------------------------------------
    # SLIDE 7: Deep-Dive: Ingestion & Statistical Drift (Krishna)
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Data Ingestion Buffer & Statistical Drift Engine", "MODULE LEAD: KRISHNA")

    c1 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = BG_CARD
    c1.line.color.rgb = BORDER_CRIMSON
    c1.line.width = Pt(2.0)
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.2)
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "⚡ Ingestion Queue & Metric Window"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

    q_items = [
        ("Circular FIFO Queue (queue.py)", "Asynchronous prediction buffer (Capacity: 5000 events). Enqueue and dequeue operate in strict O(1) time using modulo pointer wrapping: tail = (tail + 1) % capacity."),
        ("Zero-Allocation Overflow Protection", "When the queue reaches capacity, oldest unconsumed records are dropped gracefully, eliminating memory leaks during sudden traffic surges."),
        ("Metric Sliding Window (deque.py)", "Double-ended queue holding recent W = 400 predictions. Supports O(1) append and oldest-record eviction."),
        ("Amortized O(1) Telemetry", "Computes rolling accuracy, precision, recall, and P99 latency continuously over the sliding window.")
    ]
    for h, desc in q_items:
        ph = tf1.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10.5)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = TEXT_MUTED

    c2 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = BG_CARD
    c2.line.color.rgb = BORDER_GOLD
    c2.line.width = Pt(2.0)
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.2)
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "📊 Statistical Drift Engine (detector.py)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

    d_items = [
        ("Two-Sample Kolmogorov-Smirnov Test", "Compares empirical cumulative distributions (eCDF) in O(N log N) time: D = sup |F_base(x) - F_prod(x)|. Rejects null hypothesis if p-value < 0.05."),
        ("Population Stability Index (PSI)", "Measures shift across 10 quantile bins in O(N + B) time: PSI = SUM((Actual% - Expected%) * ln(Actual% / Expected%))."),
        ("Quantile Binning Calibration", "PSI < 0.10: Stable | 0.10 <= PSI < 0.25: Moderate Drift | PSI >= 0.25: Critical Covariate Drift."),
        ("Batched Analytical Cadence", "Evaluates statistical drift every 25 processed events to balance statistical sample power with microsecond compute overhead.")
    ]
    for h, desc in d_items:
        ph = tf2.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10.5)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 8: Deep-Dive: Dynamic DAG & Reverse-BFS RCA (Aakash - Lead)
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Dynamic Dependency DAG & Reverse-BFS Attribution", "MODULE LEAD: AAKASH (PROJECT LEAD)")

    c_left = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = BG_CARD
    c_left.line.color.rgb = BORDER_GOLD
    c_left.line.width = Pt(2.0)
    tf_l = c_left.text_frame
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = Inches(0.2)
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "🌲 4-Layer Dynamic DAG (graph.py)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

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
        ph.font.size = Pt(9.5)
        ph.font.color.rgb = TEXT_OFFWHITE
        ph.space_before = Pt(5)

    c_right = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = BG_CARD
    c_right.line.color.rgb = BORDER_CRIMSON
    c_right.line.width = Pt(2.0)
    tf_r = c_right.text_frame
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = Inches(0.2)
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "🎯 Multi-Factor Root Cause Confidence Score (RCS)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

    r_items = [
        ("Mathematical Formulation", "RCS = (0.45 * DriftEvidence) + (0.30 * PerfDrop) + (0.15 * TopologyProximity) + (0.10 * BlastImpact)"),
        ("Drift Evidence (45%)", "Composite of Kolmogorov-Smirnov statistic (D) and Population Stability Index (PSI)."),
        ("Performance Drop (30%)", "Degree of rolling accuracy degradation below the model's SLA threshold."),
        ("Topology Proximity (15%)", "Shortest graph distance from candidate feature node to the active Model node in DAG."),
        ("Blast Impact (10%)", "Ratio of affected downstream production microservices."),
        ("Automated RCA Verdict", "Isolates the single primary culprit feature with >85% confidence score, eliminating guesswork.")
    ]
    for h, desc in r_items:
        ph = tf_r.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10.5)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf_r.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 9: Deep-Dive: Priority Max-Heap & Retraining Gate (Sanskar)
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Incident Priority Max-Heap & Automated Retraining", "MODULE LEAD: SANSKAR")

    c1 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = BG_CARD
    c1.line.color.rgb = BORDER_CRIMSON
    c1.line.width = Pt(2.0)
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.2)
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "⛰️ Binary Max-Heap Priority Queue (heap.py)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

    h_items = [
        ("Pure Array-Backed Implementation", "Complete binary tree implemented with pure _sift_up and _sift_down pointer methods without external heap libraries."),
        ("Logarithmic Asymptotic Bounds", "Push new alert: O(log N) | Extract maximum severity incident: O(log N) | Peek top incident: O(1)."),
        ("Composite Severity Scoring", "Severity = (AccuracyDrop * 40) + (DriftMagnitude * 40) + (BlastRadiusCount * 20)."),
        ("Thread-Safe Resolution", "Resolves and clears alerts safely in concurrent multi-threaded streaming environments.")
    ]
    for h, desc in h_items:
        ph = tf1.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10.5)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = TEXT_MUTED

    c2 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = BG_CARD
    c2.line.color.rgb = BORDER_GOLD
    c2.line.width = Pt(2.0)
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.2)
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "🔄 Closed-Loop 4-Step Validation Gate (Phase 7)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

    r_items = [
        ("Step 1: Data Sufficiency", "Ensures sliding window has >= 20 labeled records (or synthesizes recent adaptive distribution batch)."),
        ("Step 2: Candidate Re-Fitting", "Re-fits model parameters to the drifted distribution window, adapting decision boundaries."),
        ("Step 3: 4-Step Validation Gate", "1) Accuracy >= SLA target | 2) P99 Latency <= SLA threshold | 3) Candidate outperforms degraded active model | 4) Non-negative R2 score."),
        ("Step 4: Zero-Downtime Promotion", "Promotes candidate, bumps version (v1.0.0 -> v1.1.0), updates HashMap baselines, resolves Max-Heap alerts, and resets DAG health to HEALTHY.")
    ]
    for h, desc in r_items:
        ph = tf2.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10.5)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 10: Deep-Dive: Model Registry & Simulator (Ghanshyam)
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "In-Memory Baseline Registry & Traffic Simulator", "MODULE LEAD: GHANSHYAM")

    c1 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = BG_CARD
    c1.line.color.rgb = BORDER_GOLD
    c1.line.width = Pt(2.0)
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.2)
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "🗂️ In-Memory Model Registry (registry.py)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

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
        ph.font.size = Pt(10.5)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = TEXT_MUTED

    c2 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = BG_CARD
    c2.line.color.rgb = BORDER_CRIMSON
    c2.line.width = Pt(2.0)
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.2)
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "🚦 Universal Traffic Simulator (traffic_simulator.py)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

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
        ph.font.size = Pt(10.5)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 11: Deep-Dive: History, Reports & UI (Hari)
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "History Drawer, Post-Mortems & Canvas Dashboard", "MODULE LEAD: HARI")

    c1 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = BG_CARD
    c1.line.color.rgb = BORDER_CRIMSON
    c1.line.width = Pt(2.0)
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.2)
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "📜 Observability History Drawer (history.py)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

    hist_items = [
        ("Chronological Audit Trail", "Thread-safe ModelTestingHistory captures timestamps, event badges, accuracy, latency, and culprit features with O(1) prepend."),
        ("In-Place Deduplication", "Deduplicates rapid telemetry checks within 4s window to maintain clean, non-spammy session histories."),
        ("1-Click DAG Snapshot Replay", "Clicking any history entry opens a snapshot modal rendering the exact historical DAG topology and culprit highlighting."),
        ("Session Filtering", "Filter tabs categorize sessions by All, Drift Incidents, Retrained Runs, and Registered Models.")
    ]
    for h, desc in hist_items:
        ph = tf1.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10.5)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = TEXT_MUTED

    c2 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = BG_CARD
    c2.line.color.rgb = BORDER_GOLD
    c2.line.width = Pt(2.0)
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.2)
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "📑 Post-Mortems & Interactive Web Dashboard"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

    ui_items = [
        ("Downloadable Markdown Post-Mortems", "Phase 8 engine exports complete incident post-mortems documenting root cause, KS/PSI stats, blast radius, and remediation logs."),
        ("Canvas 2D Topological DAG Visualization", "Custom High-DPI graph engine with animated data signal pulses, node hover inspection, and pulsating degradation halos."),
        ("FastAPI REST Endpoints", "Clean REST API powering /api/dashboard, /api/ingest, /api/history, /api/models/upload-csv, and /api/models/retrain."),
        ("Sleek Dark-Mode Aesthetics", "Custom glassmorphic styling, responsive cards, KPI pills, and real-time live telemetry polling.")
    ]
    for h, desc in ui_items:
        ph = tf2.add_paragraph()
        ph.text = f"• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(10.5)
        ph.font.color.rgb = TEXT_WHITE
        ph.space_before = Pt(6)
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 12: Team Division & Individual Contribution Breakdown
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12)
    add_header(s12, "Team Division & Module Contribution Breakdown", "TEAM RESPONSIBILITIES & MODULE OWNERSHIP")

    members = [
        ("Aakash (Lead)", "DAG & RCA Engine", BORDER_GOLD, [
            "Dynamic 4-Layer Dependency DAG (Pipelines -> Features -> Model -> Services)",
            "Reverse-BFS Upstream Root Cause Attribution (O(V+E))",
            "Forward-BFS Downstream Blast Radius Traversal (O(V+E))",
            "Multi-factor Root Cause Confidence Scoring (RCS Engine)",
            "ArgusSystem Central Orchestrator & Telemetry Loop"
        ]),
        ("Krishna", "Queue, Deque & Drift", BORDER_CRIMSON, [
            "Circular FIFO Ingestion Buffer (EventQueue, O(1) Push/Pop)",
            "Metric Sliding Window (Double-Ended Queue, O(1) Amortized)",
            "Two-Sample Kolmogorov-Smirnov (KS) Drift Test (O(N log N))",
            "Population Stability Index (PSI) Distribution Analyzer (O(N+B))",
            "Rolling P99 Latency & Accuracy Telemetry Engine"
        ]),
        ("Sanskar", "Max-Heap & Retraining", BORDER_GOLD, [
            "Incident Priority Max-Heap with custom _sift_up / _sift_down",
            "Multi-factor Incident Severity Ranking & O(log N) Extraction",
            "Automated 1-Click Retraining on Rolling Distribution Windows",
            "4-Step Closed-Loop Model Validation Gate & Version Promotion",
            "Automated Max-Heap Incident Resolution & Node Health Recovery"
        ]),
        ("Ghanshyam", "Registry & Simulation", BORDER_CRIMSON, [
            "In-Memory Baseline Distribution Store (ModelRegistry HashMap, O(1))",
            "Multi-Task Model Support (Classification & Regression Baselines)",
            "Universal Real-Time Traffic Simulator & Background Workers",
            "Synthetic Covariate Shift Injector & Latency Spike Trigger",
            "Multipart CSV Parsing & Feature Ingestion Utilities"
        ]),
        ("Hari", "History, Reports & UI", BORDER_GOLD, [
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
        c_shape = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.7), card_w, Inches(5.2))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = BG_CARD
        c_shape.line.color.rgb = col
        c_shape.line.width = Pt(2.0)

        tf = c_shape.text_frame
        tf.margin_left = tf.margin_right = Inches(0.14)
        tf.margin_top = Inches(0.15)
        tf.word_wrap = True

        p_name = tf.paragraphs[0]
        p_name.text = name
        p_name.font.name = "Arial"
        p_name.font.size = Pt(11.5)
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
            pt.font.size = Pt(8.3)
            pt.font.color.rgb = TEXT_MUTED
            pt.space_before = Pt(5)

    # -------------------------------------------------------------
    # SLIDE 13: Experimental Results, Conclusion & Live Demo
    # -------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    add_bg(s13)
    add_header(s13, "Experimental Evaluation, Conclusion & Live Demo", "VALIDATION & VIVA DEMONSTRATION")

    metrics = [
        ("17 / 17 Tests Passed", "100% Pass Rate across Queue, Deque, Heap, Graph, Drift & Retraining suites.", BORDER_GREEN),
        ("< 0.45 ms Overhead", "Ultra-low telemetry compute latency; zero throughput impact on production models.", BORDER_GOLD),
        ("100% RCA Accuracy", "Reverse-BFS consistently isolated culprit drifting features with >90% RCS confidence.", BORDER_CRIMSON),
        ("v1.0.0 -> v1.1.0 Promotion", "Automated validation gate recovered accuracy from 68% back to 96% with zero downtime.", TEXT_GOLD)
    ]

    for idx, (val, label, col) in enumerate(metrics):
        cx = Inches(0.8 + idx * 2.95)
        card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.7), Inches(2.8), Inches(1.8))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = col
        card.line.width = Pt(2.0)

        tf = card.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.15)
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.name = "Arial"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.name = "Calibri"
        p2.font.size = Pt(8.8)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(4)

    # Bottom summary box
    c_bot = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.8), Inches(11.73), Inches(3.1))
    c_bot.fill.solid()
    c_bot.fill.fore_color.rgb = BG_CARD
    c_bot.line.color.rgb = BORDER_GOLD
    c_bot.line.width = Pt(2.0)
    tf_b = c_bot.text_frame
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = Inches(0.2)
    tf_b.word_wrap = True

    p = tf_b.paragraphs[0]
    p.text = "🎯 Core Capstone Achievements & Live Demonstration"
    p.font.name = "Arial"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

    concl_points = [
        "• Pure In-Memory DSA Engine: Replaced heavy third-party monitoring agents with 5 core data structures operating in microsecond bounds.",
        "• Automated Root Cause Attribution: Eliminated manual ETL debugging by traversing dependency graphs in O(V+E) time.",
        "• Closed-Loop Self-Healing: Automated 4-step validation gate that re-fits, validates, and promotes models with zero human downtime.",
        "• Live Interactive Demonstration: We are now ready to demonstrate live traffic simulation, drift injection, Reverse-BFS attribution, and session history replay at http://127.0.0.1:8000."
    ]
    for pt in concl_points:
        p = tf_b.add_paragraph()
        p.text = pt
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(5)

    downloads_path = os.path.expanduser("~/Downloads")
    output_pptx = os.path.join(downloads_path, "ArgusML_Presentation.pptx")
    prs.save(output_pptx)
    print(f"[SUCCESS] Saved CrimsonOrbit Presentation to {output_pptx}")

if __name__ == "__main__":
    create_crimson_orbit_presentation()
