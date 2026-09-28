"""
Generate updated official ArgusML Presentation matching CrimsonOrbit style:
Slide 1: College Header (VIT Pune), Title (ArgusML), Group 9, Guide: Prof. Sheela, Platform Meta
Slide 2: College Header, TEAM MEMBERS Table (Roll No, Name, PRN)
Slide 3: Complete Problem Statement (The Silent Failure of ML in Production)
Slide 4: Literature Review in Table Format (Comparative Taxonomy of Observability Tools)
Slide 5: Proposed Solution & System Novelty
Slide 6: System Architecture & 5-Layer Master Telemetry Pipeline
Slide 7: DSA Foundation & Complexity Matrix Table
Slide 8: Module Lead - Krishna (Queue, Deque, Drift Engine)
Slide 9: Module Lead - Aakash (Dynamic DAG, Reverse-BFS Attribution)
Slide 10: Module Lead - Sanskar (Binary Max-Heap, 4-Step Retraining Gate)
Slide 11: Module Lead - Ghanshyam (Baseline Registry HashMap, Traffic Simulator)
Slide 12: Module Lead - Hari (Session History Drawer, Post-Mortems, UI)
Slide 13: Team Division & Module Contribution Breakdown
Slide 14: Experimental Validation, Conclusion & Live Demo

Outputs:
- C:/Users/akash/Downloads/ArgusML_Presentation.pptx
- C:/Users/akash/Desktop/ArgusML_Presentation.pptx
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 Widescreen
    prs.slide_height = Inches(7.5)

    # CrimsonOrbit High-Contrast Color Palette
    BG_DARK = RGBColor(15, 18, 25)          # #0F1219 Dark Slate
    BG_CARD = RGBColor(25, 30, 42)          # #191E2A Card Navy
    BG_CARD_ALT = RGBColor(32, 38, 54)      # #202636 Secondary Card
    BORDER_CRIMSON = RGBColor(235, 60, 60)  # #EB3C3C Crimson Red
    BORDER_GOLD = RGBColor(245, 158, 11)    # #F59E0B Warm Amber Gold
    BORDER_CYAN = RGBColor(56, 189, 248)    # #38BDF8 Sky Blue
    BORDER_GREEN = RGBColor(16, 185, 129)   # #10B981 Emerald Green
    BORDER_MUTED = RGBColor(51, 65, 85)     # #334155 Slate
    
    TEXT_WHITE = RGBColor(255, 255, 255)    # #FFFFFF
    TEXT_OFFWHITE = RGBColor(241, 245, 249) # #F1F5F9
    TEXT_MUTED = RGBColor(203, 213, 225)    # #CBD5E1
    TEXT_DIM = RGBColor(148, 163, 184)      # #94A3B8
    TEXT_GOLD = RGBColor(252, 211, 77)      # #FCD34D
    TEXT_CYAN = RGBColor(125, 211, 252)     # #7DD3FC
    TEXT_GREEN = RGBColor(110, 231, 183)    # #6EE7B7
    TEXT_CRIMSON = RGBColor(252, 165, 165)  # #FCA5A5

    blank_layout = prs.slide_layouts[6]

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="VISHWAKARMA INSTITUTE OF TECHNOLOGY, PUNE • GROUP - 9"):
        # Header text
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.73), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = category_text.upper()
        p1.font.name = "Arial"
        p1.font.size = Pt(10.5)
        p1.font.bold = True
        p1.font.color.rgb = BORDER_CRIMSON

        p2 = tf.add_paragraph()
        p2.text = title_text
        p2.font.name = "Arial"
        p2.font.size = Pt(21)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(3)

        # Underline bar
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.48), Inches(11.73), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_CRIMSON
        line.line.fill.background()

    # =============================================================
    # SLIDE 1: Title Slide (Simple Plain Language)
    # =============================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)

    # Top College Badge Pill
    college_pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(0.7), Inches(10.33), Inches(0.65))
    college_pill.fill.solid()
    college_pill.fill.fore_color.rgb = BG_CARD
    college_pill.line.color.rgb = BORDER_CRIMSON
    college_pill.line.width = Pt(1.5)
    tf_c = college_pill.text_frame
    tf_c.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_c = tf_c.paragraphs[0]
    p_c.text = "VISHWAKARMA INSTITUTE OF TECHNOLOGY, PUNE"
    p_c.alignment = PP_ALIGN.CENTER
    p_c.font.name = "Arial"
    p_c.font.size = Pt(14)
    p_c.font.bold = True
    p_c.font.color.rgb = TEXT_GOLD

    # Main Project Title Box
    tb_t = s1.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.33), Inches(2.7))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p_t1 = tf_t.paragraphs[0]
    p_t1.text = "ARGUSML"
    p_t1.alignment = PP_ALIGN.CENTER
    p_t1.font.name = "Arial Black"
    p_t1.font.size = Pt(40)
    p_t1.font.bold = True
    p_t1.font.color.rgb = BORDER_CRIMSON

    p_t2 = tf_t.add_paragraph()
    p_t2.text = "Real-Time Health Watchdog & Root-Cause Tracker for AI Models"
    p_t2.alignment = PP_ALIGN.CENTER
    p_t2.font.name = "Arial"
    p_t2.font.size = Pt(18)
    p_t2.font.bold = True
    p_t2.font.color.rgb = TEXT_WHITE
    p_t2.space_before = Pt(4)

    p_t3 = tf_t.add_paragraph()
    p_t3.text = "A fast in-memory system that monitors live machine learning models, catches silent data changes, finds the exact broken feature using graphs, and fixes accuracy automatically with zero downtime."
    p_t3.alignment = PP_ALIGN.CENTER
    p_t3.font.name = "Calibri"
    p_t3.font.size = Pt(13.5)
    p_t3.font.color.rgb = TEXT_MUTED
    p_t3.space_before = Pt(8)

    # Pill 1: Presented By Group 9
    pill1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(4.7), Inches(4.2), Inches(0.85))
    pill1.fill.solid()
    pill1.fill.fore_color.rgb = BG_CARD
    pill1.line.color.rgb = BORDER_CYAN
    pill1.line.width = Pt(1.5)
    tf_p1 = pill1.text_frame
    tf_p1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_p1 = tf_p1.paragraphs[0]
    p_p1.text = "Presented By: GROUP - 9"
    p_p1.alignment = PP_ALIGN.CENTER
    p_p1.font.name = "Arial"
    p_p1.font.size = Pt(14)
    p_p1.font.bold = True
    p_p1.font.color.rgb = TEXT_CYAN

    # Pill 2: Guide: Prof. Sheela
    pill2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(4.7), Inches(4.2), Inches(0.85))
    pill2.fill.solid()
    pill2.fill.fore_color.rgb = BG_CARD
    pill2.line.color.rgb = BORDER_GOLD
    pill2.line.width = Pt(1.5)
    tf_p2 = pill2.text_frame
    tf_p2.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_p2 = tf_p2.paragraphs[0]
    p_p2.text = "Guide: Prof. Sheela"
    p_p2.alignment = PP_ALIGN.CENTER
    p_p2.font.name = "Arial"
    p_p2.font.size = Pt(14)
    p_p2.font.bold = True
    p_p2.font.color.rgb = TEXT_GOLD

    # Bottom Metadata Box
    tb_bot = s1.shapes.add_textbox(Inches(1.0), Inches(6.1), Inches(11.33), Inches(0.8))
    tf_b = tb_bot.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "28/09/2026   •   Built with 5 Core Data Structures   •   Platform: Python & FastAPI"
    p_b.alignment = PP_ALIGN.CENTER
    p_b.font.name = "Calibri"
    p_b.font.size = Pt(12)
    p_b.font.color.rgb = TEXT_DIM

    # =============================================================
    # SLIDE 2: Team Members Table
    # =============================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "TEAM MEMBERS", "VISHWAKARMA INSTITUTE OF TECHNOLOGY, PUNE • GROUP - 9")

    table_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.8), Inches(10.93), Inches(4.8))
    table_card.fill.solid()
    table_card.fill.fore_color.rgb = BG_CARD
    table_card.line.color.rgb = BORDER_CRIMSON
    table_card.line.width = Pt(1.5)

    rows = 6
    cols = 3
    tbl_shape = s2.shapes.add_table(rows, cols, Inches(1.5), Inches(2.1), Inches(10.33), Inches(4.0))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(2.0)
    tbl.columns[1].width = Inches(5.33)
    tbl.columns[2].width = Inches(3.0)

    headers = ["ROLL NO.", "NAME", "PRN"]
    team_data = [
        ["4", "Agaldare Ghansham Dilip", "1251010321"],
        ["7", "Aher Krishna Gorakh", "1251010727"],
        ["9", "Akash Kumar", "1251010761"],
        ["38", "Bhargude Sanskar Sandip", "1251010716"],
        ["49", "Hari Ratnakar Birare", "1251010693"],
    ]

    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BORDER_CRIMSON
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    for row_idx, row in enumerate(team_data):
        row_bg = BG_CARD if row_idx % 2 == 0 else BG_CARD_ALT
        for col_idx, val in enumerate(row):
            cell = tbl.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.CENTER if col_idx != 1 else PP_ALIGN.LEFT
            p.font.name = "Arial"
            p.font.size = Pt(12.5)
            p.font.color.rgb = TEXT_OFFWHITE if col_idx != 1 else TEXT_GOLD
            if col_idx == 1:
                p.font.bold = True

    # =============================================================
    # SLIDE 3: Problem Statement (Simple Plain Language)
    # =============================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "THE PROBLEM: WHY AI MODELS BREAK SILENTLY", "REAL-WORLD MLOPS CHALLENGE")

    card_coords = [
        (Inches(0.8), Inches(1.7), Inches(5.6), Inches(2.4), "1. AI Models Fail Silently", BORDER_CRIMSON, [
            ("• Normal Code vs AI Models:", True, TEXT_CRIMSON),
            ("  Normal software crashes with a red error screen (HTTP 500). But broken AI models keep saying 'Everything is OK' (HTTP 200) while giving completely wrong predictions!", False, TEXT_MUTED),
            ("• Silent Business Loss:", True, TEXT_OFFWHITE),
            ("  Real-world changes (changing user habits, currency errors, sensor glitches) secretly drop model accuracy from 95% down to 65% without anyone noticing.", False, TEXT_MUTED)
        ]),
        (Inches(6.93), Inches(1.7), Inches(5.6), Inches(2.4), "2. Standard Server Tools Are Blind", BORDER_GOLD, [
            ("• Datadog & Prometheus Limitations:", True, TEXT_GOLD),
            ("  Traditional tools only check if the computer CPU and RAM are running. They are completely blind to whether the data itself has changed.", False, TEXT_MUTED),
            ("• Invisible Data Changes:", True, TEXT_OFFWHITE),
            ("  A model can have 100% server uptime and zero crashes, but still make 100% wrong decisions because input data drifted.", False, TEXT_MUTED)
        ]),
        (Inches(0.8), Inches(4.35), Inches(5.6), Inches(2.55), "3. Finding the Bad Feature Takes Days", BORDER_CYAN, [
            ("• Complex Multi-Step Pipelines:", True, TEXT_CYAN),
            ("  Data flows through many steps: Data Sources -> Features -> AI Model -> Apps. When an app fails, nobody knows which specific feature caused it.", False, TEXT_MUTED),
            ("• Manual Searching Wastes Time:", True, TEXT_OFFWHITE),
            ("  Engineers spend days manually checking database tables to guess which feature broke.", False, TEXT_MUTED)
        ]),
        (Inches(6.93), Inches(4.35), Inches(5.6), Inches(2.55), "4. Fixing Models Is Slow & Manual", BORDER_GREEN, [
            ("• Alerts Without Solutions:", True, TEXT_GREEN),
            ("  Existing tools only send alert emails, but don't help engineers fix the issue or retrain the model.", False, TEXT_MUTED),
            ("• Expensive Downtime:", True, TEXT_OFFWHITE),
            ("  Fixing models requires manual coding, manual testing, and manual redeployment, leaving broken models running for days.", False, TEXT_MUTED)
        ]),
    ]

    for left, top, width, height, title, b_color, lines in card_coords:
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = b_color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.18)

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = b_color

        for text, is_bold, col in lines:
            p = tf.add_paragraph()
            p.text = text
            p.font.name = "Calibri"
            p.font.size = Pt(10.5)
            p.font.bold = is_bold
            p.font.color.rgb = col
            p.space_before = Pt(2)

    # =============================================================
    # SLIDE 4: Literature Review (Simple Plain Language Table)
    # =============================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "LITERATURE REVIEW: EXISTING TOOLS VS ARGUSML", "EASY COMPARISON TABLE")

    tbl_shape4 = s4.shapes.add_table(9, 5, Inches(0.8), Inches(1.7), Inches(11.73), Inches(5.2))
    tbl4 = tbl_shape4.table
    tbl4.columns[0].width = Inches(2.2)
    tbl4.columns[1].width = Inches(2.3)
    tbl4.columns[2].width = Inches(2.4)
    tbl4.columns[3].width = Inches(2.1)
    tbl4.columns[4].width = Inches(2.73)

    lit_headers = ["What It Does", "Server Tools (Datadog)", "Offline Tools (Evidently)", "Data Loggers (WhyLogs)", "ArgusML (Our Project)"]
    lit_rows = [
        ["What It Monitors", "Server CPU & RAM only", "Saved CSV files on disk", "Summary numbers only", "Live Predictions + Data Drift + Graph"],
        ["Processing Speed", "Slow background lag", "Slow batch delay (>100ms)", "Fast summaries (<2ms)", "Super Fast In-Memory (<0.45 ms)"],
        ["Catches Data Drift?", "No (Blind to data changes)", "Only offline on saved files", "Approximate guesses", "Yes, in Real-Time on Live Data"],
        ["Finds Bad Feature?", "No (Manual guessing)", "No (No pipeline map)", "No", "Yes, Auto-traces connections O(V+E)"],
        ["Alert Prioritization", "Floods user with all alerts", "None", "None", "Smart Priority Queue (Most urgent first)"],
        ["Auto-Fix & Retrain?", "No, manual coding only", "No", "No", "1-Click Auto-Retrain with Zero Downtime"],
        ["Extra Setup Needed", "Heavy paid cloud software", "Heavy disk & file storage", "Java / Cloud SDKs", "Zero Extra Tools (Pure Python & DSA)"],
        ["Runs In Real-Time?", "Only server uptime", "No (Runs after hours)", "Streaming summaries", "Yes (Real-time live watchdog)"]
    ]

    for c_idx, h in enumerate(lit_headers):
        cell = tbl4.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BORDER_CRIMSON if c_idx == 4 else BG_CARD_ALT
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_GOLD if c_idx == 4 else TEXT_WHITE

    for r_idx, row in enumerate(lit_rows):
        r_bg = BG_CARD if r_idx % 2 == 0 else BG_CARD_ALT
        for c_idx, val in enumerate(row):
            cell = tbl4.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = r_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.CENTER if c_idx != 0 else PP_ALIGN.LEFT
            p.font.name = "Calibri"
            p.font.size = Pt(10.2)
            if c_idx == 4:
                p.font.bold = True
                p.font.color.rgb = TEXT_GREEN
            elif c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_GOLD
            else:
                p.font.color.rgb = TEXT_OFFWHITE

    # =============================================================
    # SLIDE 5: Proposed Solution (Simple Plain Language)
    # =============================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "OUR SOLUTION: 6 WAYS ARGUSML FIXES THIS", "HOW ARGUSML SOLVES THE PROBLEM")

    sol_cards = [
        (Inches(0.8), Inches(1.7), Inches(3.64), Inches(2.4), "1. Ultra-Fast In-Memory Engine", BORDER_CRIMSON, [
            "• Runs 100% inside computer memory without databases.",
            "• Processes incoming predictions in under 0.45 ms.",
            "• Uses lightweight memory footprint (<12 MB RAM).",
            "• Zero third-party vendor bloat or subscriptions."
        ]),
        (Inches(4.84), Inches(1.7), Inches(3.64), Inches(2.4), "2. Live Drift Watchdog", BORDER_GOLD, [
            "• Compares live data against baseline training numbers.",
            "• Uses statistical tests (KS-Test & PSI) automatically.",
            "• Checks for data drift every 25 predictions.",
            "• Catches silent accuracy decay immediately."
        ]),
        (Inches(8.88), Inches(1.7), Inches(3.64), Inches(2.4), "3. Automatic Root-Cause Finder", BORDER_CYAN, [
            "• Maps connections: Pipelines -> Features -> Model -> Apps.",
            "• Climbs backwards along the graph in O(V+E) time.",
            "• Pinpoints the exact corrupted feature automatically.",
            "• Calculates a clear Root Cause Confidence Score."
        ]),
        (Inches(0.8), Inches(4.35), Inches(3.64), Inches(2.55), "4. Smart Priority Alerts", BORDER_GREEN, [
            "• Uses a Binary Max-Heap priority queue in O(log N).",
            "• Sorts alerts by real severity so biggest issues come first.",
            "• Combines accuracy drop, drift size, and affected apps.",
            "• Stops engineers from getting overwhelmed by alerts."
        ]),
        (Inches(4.84), Inches(4.35), Inches(3.64), Inches(2.55), "5. 1-Click Auto-Retraining", BORDER_GOLD, [
            "• Retrains the model on recent data with 1 simple click.",
            "• 4-Step Safety Gate ensures the new model is accurate.",
            "• Promotes the new version (v1.0 -> v1.1) with zero downtime.",
            "• Clears alerts and restores model health to HEALTHY."
        ]),
        (Inches(8.88), Inches(4.35), Inches(3.64), Inches(2.55), "6. History & Replay Drawer", BORDER_CRIMSON, [
            "• Clean ChatGPT-style audit drawer tracks every test run.",
            "• 1-Click Snapshot Replay shows past graph states.",
            "• Generates downloadable Markdown incident reports.",
            "• Interactive animated 2D Canvas dashboard."
        ]),
    ]

    for left, top, width, height, title, b_color, lines in sol_cards:
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = b_color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.16)

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = b_color

        for line in lines:
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Calibri"
            p.font.size = Pt(10.2)
            p.font.color.rgb = TEXT_OFFWHITE
            p.space_before = Pt(2)

    # =============================================================
    # SLIDE 6: System Architecture (Simple Step-by-Step Flow)
    # =============================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "SYSTEM ARCHITECTURE: HOW DATA FLOWS", "ARGUSML 5-LAYER MASTER PIPELINE")

    layers = [
        ("Step 1: Incoming Predictions Queue", "Circular FIFO Queue (queue.py)", "Catches fast incoming predictions in a circular line buffer in O(1) time without running out of memory.", BORDER_CYAN),
        ("Step 2: Recent Predictions Window", "Sliding Window Deque (deque.py)", "Holds the recent 400 predictions to calculate live accuracy, precision, and latency instantly in O(1) time.", BORDER_GOLD),
        ("Step 3: Statistical Drift Checker", "DriftEngine & Baseline HashMap", "Compares live incoming numbers with original training baselines (KS-Test & PSI) every 25 predictions.", BORDER_CRIMSON),
        ("Step 4: Connection Graph (RCA)", "Dynamic Dependency Graph (graph.py)", "Traces connections backwards in O(V+E) to find the bad feature, and forwards to see affected user apps.", BORDER_GREEN),
        ("Step 5: Priority Alerts & Auto-Fix", "Binary Max-Heap & Retraining Gate", "Puts biggest problems at the top in O(log N) time and provides 1-Click Retraining to restore model health.", BORDER_GOLD)
    ]

    for idx, (l_title, l_comp, l_desc, b_col) in enumerate(layers):
        top_pos = Inches(1.7 + (idx * 1.05))
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.73), Inches(0.92))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = b_col
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.1)

        p1 = tf.paragraphs[0]
        p1.text = f"{l_title.upper()}  ➔  {l_comp}"
        p1.font.name = "Arial"
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = b_col

        p2 = tf.add_paragraph()
        p2.text = l_desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_OFFWHITE
        p2.space_before = Pt(2)

    # =============================================================
    # SLIDE 7: DSA Foundation & Complexity Analysis Matrix
    # =============================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "DATA STRUCTURES & ALGORITHMS FOUNDATION", "5 CORE DATA STRUCTURES & COMPLEXITY MATRIX")

    tbl_shape7 = s7.shapes.add_table(6, 5, Inches(0.8), Inches(1.7), Inches(11.73), Inches(5.2))
    tbl7 = tbl_shape7.table
    tbl7.columns[0].width = Inches(2.1)
    tbl7.columns[1].width = Inches(2.2)
    tbl7.columns[2].width = Inches(3.63)
    tbl7.columns[3].width = Inches(2.0)
    tbl7.columns[4].width = Inches(1.8)

    dsa_headers = ["Data Structure", "ArgusML Component", "What It Does In Simple Terms", "Time Complexity", "Space Complexity"]
    dsa_rows = [
        ["Circular FIFO Queue", "EventQueue (queue.py)", "Line buffer for incoming predictions; safely drops oldest items during bursts without memory leaks.", "Enqueue: O(1)\nDequeue: O(1)", "O(C)\nFixed Capacity"],
        ["Double-Ended Queue", "MetricSlidingWindow (deque.py)", "Sliding window of 400 recent predictions to calculate accuracy and speed instantly without recalculating past data.", "Append / Evict:\nO(1) Amortized", "O(W)\nWindow Size"],
        ["In-Memory Hash Map", "ModelRegistry (registry.py)", "Instant dictionary lookup for model info and baseline reference numbers.", "Average Lookup: O(1)\nInsert: O(1)", "O(M * F)\nModels & Features"],
        ["Binary Max-Heap", "AlertMaxHeap (heap.py)", "Smart priority queue that sorts alerts so the biggest problem is always at the top.", "Push: O(log N)\nPop Max: O(log N)", "O(N)\nActive Incidents"],
        ["Directed Acyclic Graph", "DependencyGraph (graph.py)", "Map of connections (Pipelines -> Features -> Model -> Apps) to trace causes backwards and impacts forwards.", "Reverse-BFS: O(V+E)\nForward-BFS: O(V+E)", "O(V + E)\nNodes & Edges"]
    ]


    for c_idx, h in enumerate(dsa_headers):
        cell = tbl7.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BORDER_CRIMSON
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    for r_idx, row in enumerate(dsa_rows):
        r_bg = BG_CARD if r_idx % 2 == 0 else BG_CARD_ALT
        for c_idx, val in enumerate(row):
            cell = tbl7.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = r_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.CENTER if c_idx in [0, 3, 4] else PP_ALIGN.LEFT
            p.font.name = "Calibri"
            p.font.size = Pt(10.5)
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_GOLD
            elif c_idx == 1:
                p.font.bold = True
                p.font.color.rgb = TEXT_CYAN
            elif c_idx == 3:
                p.font.bold = True
                p.font.color.rgb = TEXT_GREEN
            else:
                p.font.color.rgb = TEXT_OFFWHITE

    # =============================================================
    # SLIDE 8: Krishna (Queue, Deque, Drift)
    # =============================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Data Ingestion Buffer & Statistical Drift Engine", "MODULE LEAD: KRISHNA")

    card_k1 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    card_k1.fill.solid()
    card_k1.fill.fore_color.rgb = BG_CARD
    card_k1.line.color.rgb = BORDER_CYAN
    card_k1.line.width = Pt(1.5)
    tf_k1 = card_k1.text_frame
    tf_k1.word_wrap = True
    tf_k1.margin_left = tf_k1.margin_right = tf_k1.margin_top = Inches(0.2)
    p = tf_k1.paragraphs[0]
    p.text = "⚡ Ingestion Queue & Metric Window"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_CYAN

    k1_bullets = [
        ("• Circular FIFO Queue (queue.py):", True, TEXT_GOLD),
        ("  Asynchronous prediction buffer (Capacity: 5000 events). Enqueue and dequeue operate in strict O(1) time using modulo pointer wrapping: tail = (tail + 1) % capacity.", False, TEXT_MUTED),
        ("• Zero-Allocation Overflow Protection:", True, TEXT_GOLD),
        ("  When the queue reaches capacity, oldest unconsumed records are dropped gracefully, eliminating memory leaks during sudden traffic surges.", False, TEXT_MUTED),
        ("• Metric Sliding Window (deque.py):", True, TEXT_GOLD),
        ("  Double-ended queue holding recent W = 400 predictions. Supports O(1) append and oldest-record eviction.", False, TEXT_MUTED),
        ("• Amortized O(1) Telemetry:", True, TEXT_GOLD),
        ("  Computes rolling accuracy, precision, recall, and P99 latency continuously over the sliding window.", False, TEXT_MUTED)
    ]
    for text, is_bold, col in k1_bullets:
        p = tf_k1.add_paragraph()
        p.text = text
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = is_bold
        p.font.color.rgb = col
        p.space_before = Pt(3)

    card_k2 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.83), Inches(1.7), Inches(5.7), Inches(5.2))
    card_k2.fill.solid()
    card_k2.fill.fore_color.rgb = BG_CARD
    card_k2.line.color.rgb = BORDER_GOLD
    card_k2.line.width = Pt(1.5)
    tf_k2 = card_k2.text_frame
    tf_k2.word_wrap = True
    tf_k2.margin_left = tf_k2.margin_right = tf_k2.margin_top = Inches(0.2)
    p = tf_k2.paragraphs[0]
    p.text = "📊 Statistical Drift Engine (detector.py)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

    k2_bullets = [
        ("• Two-Sample Kolmogorov-Smirnov Test:", True, TEXT_CYAN),
        ("  Compares empirical cumulative distributions (eCDF) in O(N log N) time: D = sup |F_base(x) - F_prod(x)|. Rejects null hypothesis if p-value < 0.05.", False, TEXT_MUTED),
        ("• Population Stability Index (PSI):", True, TEXT_CYAN),
        ("  Measures shift across 10 quantile bins in O(N + B) time: PSI = SUM((Actual% - Expected%) * ln(Actual% / Expected%)).", False, TEXT_MUTED),
        ("• Quantile Binning Calibration:", True, TEXT_CYAN),
        ("  PSI < 0.10: Stable | 0.10 <= PSI < 0.25: Moderate Drift | PSI >= 0.25: Critical Covariate Drift.", False, TEXT_MUTED),
        ("• Batched Analytical Cadence:", True, TEXT_CYAN),
        ("  Evaluates statistical drift every 25 processed events to balance statistical sample power with microsecond compute overhead.", False, TEXT_MUTED)
    ]
    for text, is_bold, col in k2_bullets:
        p = tf_k2.add_paragraph()
        p.text = text
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = is_bold
        p.font.color.rgb = col
        p.space_before = Pt(3)

    # =============================================================
    # SLIDE 9: Aakash (DAG, Reverse-BFS, RCS)
    # =============================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Dynamic Dependency DAG & Reverse-BFS Attribution", "MODULE LEAD: AAKASH (PROJECT LEAD)")

    card_a1 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    card_a1.fill.solid()
    card_a1.fill.fore_color.rgb = BG_CARD
    card_a1.line.color.rgb = BORDER_CRIMSON
    card_a1.line.width = Pt(1.5)
    tf_a1 = card_a1.text_frame
    tf_a1.word_wrap = True
    tf_a1.margin_left = tf_a1.margin_right = tf_a1.margin_top = Inches(0.2)
    p = tf_a1.paragraphs[0]
    p.text = "🌲 4-Layer Dynamic DAG (graph.py)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_CRIMSON

    a1_bullets = [
        ("• Layer 1 (Pipelines):", True, TEXT_GOLD),
        ("  Upstream ingestion sources (e.g. Kafka Stream ETL, Stripe Webhook API).", False, TEXT_MUTED),
        ("• Layer 2 (Features):", True, TEXT_GOLD),
        ("  Numerical feature inputs inferred directly from baseline dataset.", False, TEXT_MUTED),
        ("• Layer 3 (Model):", True, TEXT_GOLD),
        ("  Active machine learning model node with health states (HEALTHY/WARNING/CRITICAL).", False, TEXT_MUTED),
        ("• Layer 4 (Services):", True, TEXT_GOLD),
        ("  Downstream consumer microservices (e.g. Checkout Gateway, Reporting API).", False, TEXT_MUTED),
        ("• Reverse-BFS (O(V+E)):", True, TEXT_GOLD),
        ("  Starting from degraded Model node, traverses reverse adjacency list upstream to isolate culprit drifting feature and originating pipeline.", False, TEXT_MUTED),
        ("• Forward-BFS (O(V+E)):", True, TEXT_GOLD),
        ("  Traverses forward adjacency list downstream to quantify total impacted Blast Radius.", False, TEXT_MUTED)
    ]
    for text, is_bold, col in a1_bullets:
        p = tf_a1.add_paragraph()
        p.text = text
        p.font.name = "Calibri"
        p.font.size = Pt(10.2)
        p.font.bold = is_bold
        p.font.color.rgb = col
        p.space_before = Pt(2)

    card_a2 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.83), Inches(1.7), Inches(5.7), Inches(5.2))
    card_a2.fill.solid()
    card_a2.fill.fore_color.rgb = BG_CARD
    card_a2.line.color.rgb = BORDER_CYAN
    card_a2.line.width = Pt(1.5)
    tf_a2 = card_a2.text_frame
    tf_a2.word_wrap = True
    tf_a2.margin_left = tf_a2.margin_right = tf_a2.margin_top = Inches(0.2)
    p = tf_a2.paragraphs[0]
    p.text = "🎯 Multi-Factor Root Cause Score (RCS)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_CYAN

    a2_bullets = [
        ("• Mathematical Formulation:", True, TEXT_GOLD),
        ("  RCS = (0.45 * DriftEvidence) + (0.30 * PerfDrop) + (0.15 * TopologyProximity) + (0.10 * BlastImpact)", False, TEXT_CYAN),
        ("• Drift Evidence (45%):", True, TEXT_GOLD),
        ("  Composite of Kolmogorov-Smirnov statistic (D) and Population Stability Index (PSI).", False, TEXT_MUTED),
        ("• Performance Drop (30%):", True, TEXT_GOLD),
        ("  Degree of rolling accuracy degradation below the model's SLA threshold.", False, TEXT_MUTED),
        ("• Topology Proximity (15%):", True, TEXT_GOLD),
        ("  Shortest graph distance from candidate feature node to the active Model node in DAG.", False, TEXT_MUTED),
        ("• Blast Impact (10%):", True, TEXT_GOLD),
        ("  Ratio of affected downstream production microservices.", False, TEXT_MUTED),
        ("• Automated RCA Verdict:", True, TEXT_GOLD),
        ("  Isolates the single primary culprit feature with >85% confidence score, eliminating guesswork.", False, TEXT_MUTED)
    ]
    for text, is_bold, col in a2_bullets:
        p = tf_a2.add_paragraph()
        p.text = text
        p.font.name = "Calibri"
        p.font.size = Pt(10.2)
        p.font.bold = is_bold
        p.font.color.rgb = col
        p.space_before = Pt(2)

    # =============================================================
    # SLIDE 10: Sanskar (Max-Heap & Retraining Gate)
    # =============================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Incident Priority Max-Heap & Automated Retraining", "MODULE LEAD: SANSKAR")

    card_s1 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    card_s1.fill.solid()
    card_s1.fill.fore_color.rgb = BG_CARD
    card_s1.line.color.rgb = BORDER_GOLD
    card_s1.line.width = Pt(1.5)
    tf_s1 = card_s1.text_frame
    tf_s1.word_wrap = True
    tf_s1.margin_left = tf_s1.margin_right = tf_s1.margin_top = Inches(0.2)
    p = tf_s1.paragraphs[0]
    p.text = "⛰️ Binary Max-Heap Priority Queue (heap.py)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

    s1_bullets = [
        ("• Pure Array-Backed Implementation:", True, TEXT_CYAN),
        ("  Complete binary tree implemented with pure _sift_up and _sift_down pointer methods without external heap libraries.", False, TEXT_MUTED),
        ("• Logarithmic Asymptotic Bounds:", True, TEXT_CYAN),
        ("  Push new alert: O(log N) | Extract maximum severity incident: O(log N) | Peek top incident: O(1).", False, TEXT_MUTED),
        ("• Composite Severity Scoring:", True, TEXT_CYAN),
        ("  Severity = (AccuracyDrop * 40) + (DriftMagnitude * 40) + (BlastRadiusCount * 20).", False, TEXT_MUTED),
        ("• Thread-Safe Resolution:", True, TEXT_CYAN),
        ("  Resolves and clears alerts safely in concurrent multi-threaded streaming environments.", False, TEXT_MUTED)
    ]
    for text, is_bold, col in s1_bullets:
        p = tf_s1.add_paragraph()
        p.text = text
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = is_bold
        p.font.color.rgb = col
        p.space_before = Pt(3)

    card_s2 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.83), Inches(1.7), Inches(5.7), Inches(5.2))
    card_s2.fill.solid()
    card_s2.fill.fore_color.rgb = BG_CARD
    card_s2.line.color.rgb = BORDER_GREEN
    card_s2.line.width = Pt(1.5)
    tf_s2 = card_s2.text_frame
    tf_s2.word_wrap = True
    tf_s2.margin_left = tf_s2.margin_right = tf_s2.margin_top = Inches(0.2)
    p = tf_s2.paragraphs[0]
    p.text = "🔄 Closed-Loop 4-Step Validation Gate (Phase 7)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GREEN

    s2_bullets = [
        ("• Step 1: Data Sufficiency:", True, TEXT_GOLD),
        ("  Ensures sliding window has >= 20 labeled records (or synthesizes recent adaptive distribution batch).", False, TEXT_MUTED),
        ("• Step 2: Candidate Re-Fitting:", True, TEXT_GOLD),
        ("  Re-fits model parameters to the drifted distribution window, adapting decision boundaries.", False, TEXT_MUTED),
        ("• Step 3: 4-Step Validation Gate:", True, TEXT_GOLD),
        ("  1) Accuracy >= SLA target | 2) P99 Latency <= SLA threshold | 3) Candidate outperforms degraded active model | 4) Non-negative R2 score.", False, TEXT_MUTED),
        ("• Step 4: Zero-Downtime Promotion:", True, TEXT_GOLD),
        ("  Promotes candidate, bumps version (v1.0.0 -> v1.1.0), updates HashMap baselines, resolves Max-Heap alerts, and resets DAG health to HEALTHY.", False, TEXT_MUTED)
    ]
    for text, is_bold, col in s2_bullets:
        p = tf_s2.add_paragraph()
        p.text = text
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = is_bold
        p.font.color.rgb = col
        p.space_before = Pt(3)

    # =============================================================
    # SLIDE 11: Ghanshyam (Registry & Simulator)
    # =============================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "In-Memory Baseline Registry & Traffic Simulator", "MODULE LEAD: GHANSHYAM")

    card_g1 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    card_g1.fill.solid()
    card_g1.fill.fore_color.rgb = BG_CARD
    card_g1.line.color.rgb = BORDER_CYAN
    card_g1.line.width = Pt(1.5)
    tf_g1 = card_g1.text_frame
    tf_g1.word_wrap = True
    tf_g1.margin_left = tf_g1.margin_right = tf_g1.margin_top = Inches(0.2)
    p = tf_g1.paragraphs[0]
    p.text = "🗂️ In-Memory Model Registry (registry.py)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_CYAN

    g1_bullets = [
        ("• Hash Map Baseline Store:", True, TEXT_GOLD),
        ("  O(1) average-time model metadata and empirical distribution lookup indexed by model_id and feature_name.", False, TEXT_MUTED),
        ("• Empirical Distribution Moments:", True, TEXT_GOLD),
        ("  Stores baseline sample vectors, mean, standard deviation, min, max, and quantiles for every registered feature.", False, TEXT_MUTED),
        ("• Multi-Task Model Support:", True, TEXT_GOLD),
        ("  Handles both CLASSIFICATION (Accuracy, F1-Score) and REGRESSION (MAE, RMSE, R2 Score) model metadata.", False, TEXT_MUTED),
        ("• Clean Standby State:", True, TEXT_GOLD),
        ("  Enables clean system boots, dynamic model switching, and full workspace resets.", False, TEXT_MUTED)
    ]
    for text, is_bold, col in g1_bullets:
        p = tf_g1.add_paragraph()
        p.text = text
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = is_bold
        p.font.color.rgb = col
        p.space_before = Pt(3)

    card_g2 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.83), Inches(1.7), Inches(5.7), Inches(5.2))
    card_g2.fill.solid()
    card_g2.fill.fore_color.rgb = BG_CARD
    card_g2.line.color.rgb = BORDER_CRIMSON
    card_g2.line.width = Pt(1.5)
    tf_g2 = card_g2.text_frame
    tf_g2.word_wrap = True
    tf_g2.margin_left = tf_g2.margin_right = tf_g2.margin_top = Inches(0.2)
    p = tf_g2.paragraphs[0]
    p.text = "🚦 Universal Traffic Simulator (traffic_simulator.py)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_CRIMSON

    g2_bullets = [
        ("• Multi-Threaded Production Streamer:", True, TEXT_CYAN),
        ("  Streams synthetic inferences into EventQueue at 15-25 events/sec with realistic Gaussian feature distributions and latency noise.", False, TEXT_MUTED),
        ("• Controlled Covariate Shift Injector:", True, TEXT_CYAN),
        ("  Allows interactive scaling of any chosen feature distribution (e.g. 3.5x mean shift) to trigger real-time KS/PSI drift.", False, TEXT_MUTED),
        ("• Latency Spike Simulation:", True, TEXT_CYAN),
        ("  Simulates downstream database or network degradation by adding +250ms latency spikes.", False, TEXT_MUTED),
        ("• Universal CSV Ingestion:", True, TEXT_CYAN),
        ("  Parses user CSV files, infers numeric features, trains reference models, and initializes baseline distributions on the fly.", False, TEXT_MUTED)
    ]
    for text, is_bold, col in g2_bullets:
        p = tf_g2.add_paragraph()
        p.text = text
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = is_bold
        p.font.color.rgb = col
        p.space_before = Pt(3)

    # =============================================================
    # SLIDE 12: Hari (History Drawer, Post-Mortems, UI)
    # =============================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12)
    add_header(s12, "History Drawer, Post-Mortems & Canvas Dashboard", "MODULE LEAD: HARI")

    card_h1 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2))
    card_h1.fill.solid()
    card_h1.fill.fore_color.rgb = BG_CARD
    card_h1.line.color.rgb = BORDER_GOLD
    card_h1.line.width = Pt(1.5)
    tf_h1 = card_h1.text_frame
    tf_h1.word_wrap = True
    tf_h1.margin_left = tf_h1.margin_right = tf_h1.margin_top = Inches(0.2)
    p = tf_h1.paragraphs[0]
    p.text = "📜 Observability History Drawer (history.py)"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GOLD

    h1_bullets = [
        ("• Chronological Audit Trail:", True, TEXT_CYAN),
        ("  Thread-safe ModelTestingHistory captures timestamps, event badges, accuracy, latency, and culprit features with O(1) prepend.", False, TEXT_MUTED),
        ("• In-Place Deduplication:", True, TEXT_CYAN),
        ("  Deduplicates rapid telemetry checks within 4s window to maintain clean, non-spammy session histories.", False, TEXT_MUTED),
        ("• 1-Click DAG Snapshot Replay:", True, TEXT_CYAN),
        ("  Clicking any history entry opens a snapshot modal rendering the exact historical DAG topology and culprit highlighting.", False, TEXT_MUTED),
        ("• Session Filtering:", True, TEXT_CYAN),
        ("  Filter tabs categorize sessions by All, Drift Incidents, Retrained Runs, and Registered Models.", False, TEXT_MUTED)
    ]
    for text, is_bold, col in h1_bullets:
        p = tf_h1.add_paragraph()
        p.text = text
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = is_bold
        p.font.color.rgb = col
        p.space_before = Pt(3)

    card_h2 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.83), Inches(1.7), Inches(5.7), Inches(5.2))
    card_h2.fill.solid()
    card_h2.fill.fore_color.rgb = BG_CARD
    card_h2.line.color.rgb = BORDER_GREEN
    card_h2.line.width = Pt(1.5)
    tf_h2 = card_h2.text_frame
    tf_h2.word_wrap = True
    tf_h2.margin_left = tf_h2.margin_right = tf_h2.margin_top = Inches(0.2)
    p = tf_h2.paragraphs[0]
    p.text = "📑 Post-Mortems & Interactive Web Dashboard"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BORDER_GREEN

    h2_bullets = [
        ("• Downloadable Markdown Post-Mortems:", True, TEXT_GOLD),
        ("  Phase 8 engine exports complete incident post-mortems documenting root cause, KS/PSI stats, blast radius, and remediation logs.", False, TEXT_MUTED),
        ("• Canvas 2D Topological DAG Visualization:", True, TEXT_GOLD),
        ("  Custom High-DPI graph engine with animated data signal pulses, node hover inspection, and pulsating degradation halos.", False, TEXT_MUTED),
        ("• FastAPI REST Endpoints:", True, TEXT_GOLD),
        ("  Clean REST API powering /api/dashboard, /api/ingest, /api/history, /api/models/upload-csv, and /api/models/retrain.", False, TEXT_MUTED),
        ("• Sleek Dark-Mode Aesthetics:", True, TEXT_GOLD),
        ("  Custom glassmorphic styling, responsive cards, KPI pills, and real-time live telemetry polling.", False, TEXT_MUTED)
    ]
    for text, is_bold, col in h2_bullets:
        p = tf_h2.add_paragraph()
        p.text = text
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = is_bold
        p.font.color.rgb = col
        p.space_before = Pt(3)

    # =============================================================
    # SLIDE 13: Team Division & Module Contribution Breakdown
    # =============================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_bg(s13)
    add_header(s13, "TEAM RESPONSIBILITIES & MODULE OWNERSHIP", "WORK DIVISION & INDIVIDUAL MEMBER CONTRIBUTIONS")

    members = [
        ("Aakash (Lead)", "DAG & RCA Engine", [
            "• Dynamic 4-Layer Dependency DAG",
            "• Reverse-BFS Upstream Attribution (O(V+E))",
            "• Forward-BFS Downstream Blast Radius",
            "• Multi-Factor Root Cause Score (RCS Engine)",
            "• ArgusSystem Central Orchestrator Loop"
        ], BORDER_CRIMSON),
        ("Krishna", "Queue, Deque & Drift", [
            "• Circular FIFO Buffer (EventQueue, O(1))",
            "• Metric Sliding Window (Deque, O(1))",
            "• Two-Sample KS-Test Engine (O(N log N))",
            "• Population Stability Index (PSI) Binning",
            "• Rolling Accuracy & P99 Latency Engine"
        ], BORDER_CYAN),
        ("Sanskar", "Max-Heap & Retrain", [
            "• Binary Max-Heap with _sift_up / _sift_down",
            "• Logarithmic Severity Ranking (O(log N))",
            "• Automated 1-Click Model Retraining",
            "• 4-Step Model Validation Gate (v1.1.0)",
            "• Max-Heap Incident Resolution & Reset"
        ], BORDER_GOLD),
        ("Ghanshyam", "Registry & Simulator", [
            "• In-Memory Baseline Store (HashMap, O(1))",
            "• Multi-Task Baselines (Class. & Reg.)",
            "• Real-Time Traffic Streamer Simulator",
            "• Synthetic Covariate Shift Injector",
            "• Multipart CSV Parsing & Ingestion"
        ], BORDER_GREEN),
        ("Hari", "History, Reports & UI", [
            "• Session Audit Drawer (ModelTestingHistory)",
            "• 1-Click Interactive Historical DAG Replay",
            "• Automated Markdown Post-Mortem Exporter",
            "• Glassmorphic Dashboard & REST APIs",
            "• HTML5 Canvas 2D Animated Topological Graph"
        ], BORDER_GOLD),
    ]

    for idx, (name, role, tasks, b_col) in enumerate(members):
        left_pos = Inches(0.8 + (idx * 2.38))
        card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.7), Inches(2.26), Inches(5.2))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = b_col
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.14)

        p1 = tf.paragraphs[0]
        p1.text = name
        p1.alignment = PP_ALIGN.CENTER
        p1.font.name = "Arial"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = b_col

        p2 = tf.add_paragraph()
        p2.text = role
        p2.alignment = PP_ALIGN.CENTER
        p2.font.name = "Arial"
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_GOLD
        p2.space_before = Pt(2)

        for task in tasks:
            p = tf.add_paragraph()
            p.text = task
            p.font.name = "Calibri"
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_OFFWHITE
            p.space_before = Pt(3)

    # =============================================================
    # SLIDE 14: Experimental Validation & Live Demo Guide
    # =============================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_bg(s14)
    add_header(s14, "EXPERIMENTAL VALIDATION & LIVE DEMONSTRATION", "EMPIRICAL BENCHMARKS, CONCLUSION & VIVA DEMO")

    # 4 Stat Cards on Top
    stat_coords = [
        (Inches(0.8), Inches(1.7), Inches(2.78), Inches(1.5), "17 / 17 Tests Passed", "100% Pass Rate across Queue, Deque, Heap, Graph, Drift & Retrain suites.", BORDER_GREEN),
        (Inches(3.78), Inches(1.7), Inches(2.78), Inches(1.5), "< 0.45 ms Overhead", "Ultra-low telemetry compute latency; zero impact on inference throughput.", BORDER_CYAN),
        (Inches(6.76), Inches(1.7), Inches(2.78), Inches(1.5), "100% RCA Accuracy", "Reverse-BFS consistently isolated culprit features with >86% confidence.", BORDER_GOLD),
        (Inches(9.74), Inches(1.7), Inches(2.78), Inches(1.5), "v1.0.0 ➔ v1.1.0 Promoted", "Automated validation gate recovered accuracy from 68% to 96% with zero downtime.", BORDER_CRIMSON),
    ]

    for left, top, width, height, num_txt, desc_txt, b_col in stat_coords:
        card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = b_col
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.14)
        tf.margin_top = Inches(0.12)

        p1 = tf.paragraphs[0]
        p1.text = num_txt
        p1.alignment = PP_ALIGN.CENTER
        p1.font.name = "Arial"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = b_col

        p2 = tf.add_paragraph()
        p2.text = desc_txt
        p2.alignment = PP_ALIGN.CENTER
        p2.font.name = "Calibri"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_OFFWHITE
        p2.space_before = Pt(2)

    # Bottom Big Card for Live Demo
    demo_card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.45), Inches(11.73), Inches(3.45))
    demo_card.fill.solid()
    demo_card.fill.fore_color.rgb = BG_CARD
    demo_card.line.color.rgb = BORDER_CRIMSON
    demo_card.line.width = Pt(1.5)

    tf_d = demo_card.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = Inches(0.2)

    p_dt = tf_d.paragraphs[0]
    p_dt.text = "🎯 Core Capstone Achievements & Live Demonstration Guide"
    p_dt.font.name = "Arial"
    p_dt.font.size = Pt(14)
    p_dt.font.bold = True
    p_dt.font.color.rgb = BORDER_GOLD

    demo_bullets = [
        ("• Pure In-Memory DSA Engine:", True, TEXT_CYAN),
        ("  Replaced heavy distributed monitoring agents with 5 core data structures operating in microsecond bounds (<0.45 ms).", False, TEXT_MUTED),
        ("• Automated Root Cause Attribution:", True, TEXT_CYAN),
        ("  Eliminated manual ETL debugging by traversing dependency graphs in O(V+E) time to pinpoint exact culprit features.", False, TEXT_MUTED),
        ("• Closed-Loop Self-Healing:", True, TEXT_CYAN),
        ("  Automated 4-step validation gate that re-fits, validates, and promotes models (v1.0.0 -> v1.1.0) with zero human downtime.", False, TEXT_MUTED),
        ("• Live Interactive Demonstration Steps:", True, TEXT_GREEN),
        ("  1) Load Model (Customer Churn / Fraud Shield) ➔ 2) Stream Live Traffic ➔ 3) Inject Drift into `monthly_charges` ➔ 4) Observe Reverse-BFS Isolation & Max-Heap Alert ➔ 5) Click 1-Click Retrain & Download Incident Post-Mortem Report at http://127.0.0.1:8000.", False, TEXT_GOLD)
    ]

    for text, is_bold, col in demo_bullets:
        p = tf_d.add_paragraph()
        p.text = text
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = is_bold
        p.font.color.rgb = col
        p.space_before = Pt(3)

    # Save Presentation to multiple locations
    downloads_path = os.path.expanduser("~/Downloads")
    desktop_path = os.path.expanduser("~/Desktop")
    docs_path = os.path.abspath("docs")

    save_targets = [
        os.path.join(downloads_path, "ArgusML_Simple_Presentation.pptx"),
        os.path.join(downloads_path, "ArgusML_Final_Presentation.pptx"),
        os.path.join(desktop_path, "ArgusML_Final_Presentation.pptx"),
        os.path.join(docs_path, "ArgusML_Presentation.pptx"),
        os.path.join(downloads_path, "ArgusML_Presentation.pptx"),
        os.path.join(desktop_path, "ArgusML_Presentation.pptx"),
    ]

    for target in save_targets:
        try:
            prs.save(target)
            print(f"[SUCCESS] Presentation saved to: {target}")
        except PermissionError:
            print(f"[NOTE] Could not overwrite locked file: {target} (currently open in PowerPoint). Saved to alternatives.")
        except Exception as e:
            print(f"[WARNING] Error saving to {target}: {e}")

if __name__ == "__main__":
    create_presentation()

