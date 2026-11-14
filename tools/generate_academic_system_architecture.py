"""
generate_academic_system_architecture.py
Generates an authentic, publication-grade academic system architecture diagram
specifically formatted for IEEE / ACM Conference research papers:
- Pure white / crisp light-gray background (#ffffff)
- Clean vector boxes with subtle academic tints (#f8fafc, #f1f5f9, #eff6ff, #fef2f2, #ecfdf5)
- Standard dark typography (#0f172a, #1e293b, #334155)
- Mathematical notations and DSA time/space complexities in LaTeX style
- Zero text overlaps, perfect padding, beautiful aligned buses and connections
- Authentic distributed systems topology (No artificial Tier 1/2/3 column headers)
- Rendered at ultra-high 300 DPI publication resolution
"""

import os
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

def draw_academic_architecture(output_png_path, output_jpg_path):
    fig_w, fig_h = 16.5, 10.2
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=300, facecolor='#ffffff')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#ffffff')
    ax.set_xlim(0, 1650)
    ax.set_ylim(0, 1020)
    ax.axis('off')

    # Top Title / Header Banner (Clean Academic Style)
    ax.text(825, 985, "ArgusML: Distributed Closed-Loop ML Observability & Graph Diagnostic Architecture",
            fontsize=15.5, fontweight='bold', color='#0f172a', ha='center', va='center', fontfamily='sans-serif')
    ax.plot([80, 1570], [960, 960], color='#cbd5e1', lw=1.2, ls='-')

    # -------------------------------------------------------------
    # 1. INGESTION & STREAM INGRESS (Left Column)
    # -------------------------------------------------------------
    g1 = FancyBboxPatch((30, 160), 320, 770, boxstyle="round,pad=0,rounding_size=10",
                        facecolor='#f8fafc', edgecolor='#94a3b8', lw=1.4, ls='--')
    ax.add_patch(g1)
    ax.text(190, 905, "1. Ingestion & Stream Ingress", fontsize=11.5, fontweight='bold', color='#1e293b', ha='center')

    # Inference Sources Box
    c_box = FancyBboxPatch((50, 735), 280, 145, boxstyle="round,pad=0,rounding_size=8",
                           facecolor='#ffffff', edgecolor='#3b82f6', lw=1.4)
    ax.add_patch(c_box)
    ax.text(190, 855, "Production Inference Ingress", fontsize=10.0, fontweight='bold', color='#1d4ed8', ha='center')
    ax.text(190, 832, "• Client Applications & REST APIs", fontsize=8.2, color='#334155', ha='center')
    ax.text(190, 812, "• High-Throughput gRPC Streams", fontsize=8.2, color='#334155', ha='center')
    ax.text(190, 792, r"• Telemetry: $(X, \hat{y}, y, \Delta t)$ Records", fontsize=8.2, color='#0f172a', ha='center')
    ax.text(190, 768, "POST /api/models/predict | /upload-csv", fontsize=7.6, family='monospace', color='#475569', ha='center')
    ax.text(190, 748, "Non-blocking Asynchronous Stream", fontsize=7.5, color='#2563eb', fontstyle='italic', ha='center')

    # EventQueue (Circular FIFO Ring Buffer)
    q_box = FancyBboxPatch((50, 490), 280, 205, boxstyle="round,pad=0,rounding_size=8",
                           facecolor='#f0fdf4', edgecolor='#16a34a', lw=1.4)
    ax.add_patch(q_box)
    ax.text(190, 670, "EventQueue (Circular FIFO Buffer)", fontsize=10.0, fontweight='bold', color='#15803d', ha='center')
    ax.text(190, 648, r"Time Complexity: $\mathcal{O}(1)$ | Space: $\mathcal{O}(N)$", fontsize=8.2, fontweight='bold', color='#166534', ha='center')
    ax.text(190, 626, r"• Pre-allocated Buffer ($N = 5000$ slots)", fontsize=8.0, color='#334155', ha='center')
    ax.text(190, 606, "• Modulo Arithmetic: (tail + 1) % N", fontsize=8.0, family='sans-serif', color='#334155', ha='center')
    ax.text(190, 586, "• Zero Dynamic Memory Allocation", fontsize=8.0, color='#334155', ha='center')
    ax.text(190, 566, "• High-Throughput Ingestion (0.412 ms/op)", fontsize=8.0, fontweight='bold', color='#15803d', ha='center')

    # Ring buffer graphic
    ax.text(190, 548, "In-Memory FIFO Slots:", fontsize=7.5, color='#166534', ha='center', fontweight='bold')
    for i in range(7):
        col = '#bbf7d0' if i < 4 else '#ffffff'
        rect = Rectangle((82 + i*31, 520), 26, 20, facecolor=col, edgecolor='#16a34a', lw=1.2)
        ax.add_patch(rect)
        ax.text(82 + i*31 + 13, 530, f"e_{i+1}" if i < 4 else "-", fontsize=7.0, color='#15803d' if i < 4 else '#94a3b8', ha='center', va='center')
    ax.text(190, 498, "Lock-Free Ring Buffer Ingestion", fontsize=7.5, color='#15803d', fontstyle='italic', ha='center')

    # Metric Sliding Window Deque
    w_box = FancyBboxPatch((50, 185), 280, 265, boxstyle="round,pad=0,rounding_size=8",
                           facecolor='#eff6ff', edgecolor='#2563eb', lw=1.4)
    ax.add_patch(w_box)
    ax.text(190, 425, "Metric Sliding Window (Deque)", fontsize=10.0, fontweight='bold', color='#1d4ed8', ha='center')
    ax.text(190, 403, r"Amortized Complexity: $\mathcal{O}(1)$", fontsize=8.2, fontweight='bold', color='#1e40af', ha='center')
    ax.text(190, 381, r"• Double-Ended Queue ($W = 500$ observations)", fontsize=8.0, color='#334155', ha='center')
    ax.text(190, 361, "• Incremental Rolling Metrics:", fontsize=8.0, fontweight='bold', color='#334155', ha='center')
    ax.text(190, 341, r"  - Accuracy, Precision, Recall, $F_1$-Score", fontsize=7.8, color='#475569', ha='center')
    ax.text(190, 321, r"  - Continuous Regression $R^2$, RMSE, MAE", fontsize=7.8, color='#475569', ha='center')
    ax.text(190, 301, "  - Exponential Moving Average Latency", fontsize=7.8, color='#475569', ha='center')
    ax.text(190, 281, r"  - Non-parametric Percentiles ($P_{50}, P_{95}, P_{99}$)", fontsize=7.8, color='#475569', ha='center')
    ax.text(190, 258, "• Constant-Time Eviction & Counter Updates", fontsize=7.8, color='#1e40af', ha='center')
    ax.text(190, 235, r"Active Live Distribution $F_{\mathrm{live}}(x)$", fontsize=8.0, family='sans-serif', fontweight='bold', color='#1e3a8a', ha='center')
    ax.text(190, 205, "Sliding Window Telemetry Stream", fontsize=7.5, color='#2563eb', fontstyle='italic', ha='center')

    # Ingestion column arrows
    ax.annotate('', xy=(190, 695), xytext=(190, 735),
                arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.4', color='#1d4ed8', lw=1.8))
    ax.annotate('', xy=(190, 450), xytext=(190, 490),
                arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.4', color='#16a34a', lw=1.8))

    # -------------------------------------------------------------
    # 2. OBSERVABILITY KERNEL & STATE ENGINE (Mid-Left Top)
    # -------------------------------------------------------------
    g2 = FancyBboxPatch((380, 540), 410, 390, boxstyle="round,pad=0,rounding_size=10",
                        facecolor='#f8fafc', edgecolor='#64748b', lw=1.4, ls='--')
    ax.add_patch(g2)
    ax.text(585, 905, "2. Observability Kernel & State Engine", fontsize=11.5, fontweight='bold', color='#1e293b', ha='center')

    # Model Registry (Hash Map)
    reg_box = FancyBboxPatch((400, 735), 370, 145, boxstyle="round,pad=0,rounding_size=8",
                             facecolor='#fdf4ff', edgecolor='#9333ea', lw=1.4)
    ax.add_patch(reg_box)
    ax.text(585, 855, r"Model Registry ($\mathcal{O}(1)$ Hash Map)", fontsize=10.0, fontweight='bold', color='#7e22ce', ha='center')
    ax.text(585, 830, r"• Key-Value In-Memory Storage $(\mathrm{key} = \mathtt{model\_id})$", fontsize=8.0, color='#334155', ha='center')
    ax.text(585, 810, r"• Empirical Baseline Distributions $F_{\mathrm{baseline}}(x)$", fontsize=8.0, color='#334155', ha='center')
    ax.text(585, 790, "• SLA Threshold Contracts (Drift, Accuracy, Latency)", fontsize=8.0, color='#334155', ha='center')
    ax.text(585, 770, r"• Atomic Version Pointers ($\mathtt{v1.0.0} \to \mathtt{v1.1.0}$)", fontsize=8.0, fontweight='bold', color='#6b21a8', ha='center')
    ax.text(585, 748, "State: Persistent Baseline Quantile Store", fontsize=7.5, color='#7e22ce', fontstyle='italic', ha='center')

    # Statistical Drift Engine
    drift_box = FancyBboxPatch((400, 560), 370, 155, boxstyle="round,pad=0,rounding_size=8",
                               facecolor='#fefce8', edgecolor='#ca8a04', lw=1.4)
    ax.add_patch(drift_box)
    ax.text(585, 688, "Continuous Statistical Drift Engine", fontsize=10.0, fontweight='bold', color='#a16207', ha='center')
    ax.text(585, 664, "• Two-Sample Kolmogorov-Smirnov Test (Continuous):", fontsize=8.0, fontweight='bold', color='#334155', ha='center')
    ax.text(585, 644, r"$D = \sup_x |F_{\mathrm{baseline}}(x) - F_{\mathrm{live}}(x)| \quad (p < 0.05)$", fontsize=8.2, color='#854d0e', ha='center')
    ax.text(585, 620, "• Population Stability Index (PSI) (Categorical/Quantiles):", fontsize=8.0, fontweight='bold', color='#334155', ha='center')
    ax.text(585, 600, r"$\mathrm{PSI} = \sum_{b=1}^B (Q_b - P_b) \cdot \ln(Q_b / P_b) \quad (\geq 0.25)$", fontsize=8.2, color='#854d0e', ha='center')
    ax.text(585, 576, "Calculates Multi-Feature Divergence Vectors", fontsize=7.5, color='#a16207', fontstyle='italic', ha='center')

    # Bidirectional arrow between Registry & Drift Engine
    ax.annotate('', xy=(585, 715), xytext=(585, 735),
                arrowprops=dict(arrowstyle='<->,head_width=0.3,head_length=0.35', color='#9333ea', lw=1.5))

    # Connection from Sliding Window to Drift Engine
    ax.annotate('', xy=(400, 635), xytext=(330, 330),
                arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.4', color='#2563eb', lw=1.6,
                                connectionstyle="angle,angleA=0,angleB=90,rad=10"))
    ax.text(355, 500, "Rolling\nSamples\n" + r"$F_{\mathrm{live}}(x)$", fontsize=7.5, color='#1d4ed8', fontweight='bold', ha='center')

    # -------------------------------------------------------------
    # 3. TOPOLOGICAL 4-LAYER DIAGNOSTIC DAG (Center-Right Top)
    # -------------------------------------------------------------
    g3 = FancyBboxPatch((820, 440), 420, 490, boxstyle="round,pad=0,rounding_size=10",
                        facecolor='#f8fafc', edgecolor='#64748b', lw=1.4, ls='--')
    ax.add_patch(g3)
    ax.text(1030, 905, "3. Central Diagnostic Graph Mesh", fontsize=11.5, fontweight='bold', color='#1e293b', ha='center')

    dag_sub = FancyBboxPatch((840, 460), 380, 420, boxstyle="round,pad=0,rounding_size=8",
                             facecolor='#ffffff', edgecolor='#0284c7', lw=1.4)
    ax.add_patch(dag_sub)
    ax.text(1030, 855, r"Dynamic 4-Layer Dependency DAG ($\mathcal{O}(V + E)$)", fontsize=9.8, fontweight='bold', color='#0369a1', ha='center')

    # Nodes (Layer 1 to Layer 4)
    nodes = {
        'P1': (890, 790), 'P2': (975, 790), 'P3': (1060, 790), 'P4': (1150, 790),
        'F1': (900, 695), 'F2': (985, 695), 'F3': (1075, 695), 'F4': (1160, 695),
        'M':  (1030, 600),
        'S1': (920, 505), 'S2': (1030, 505), 'S3': (1140, 505)
    }

    ax.text(848, 810, "Pipelines:", fontsize=7.5, fontweight='bold', color='#64748b', ha='left')
    ax.text(848, 715, "Features:", fontsize=7.5, fontweight='bold', color='#64748b', ha='left')
    ax.text(848, 620, "Model Node:", fontsize=7.5, fontweight='bold', color='#64748b', ha='left')
    ax.text(848, 525, "Services:", fontsize=7.5, fontweight='bold', color='#64748b', ha='left')

    regular_edges = [
        ('P1', 'F1'), ('P2', 'F1'), ('P2', 'F2'), ('P3', 'F3'), ('P4', 'F4'),
        ('F1', 'M'), ('F2', 'M'), ('F3', 'M'), ('F4', 'M'),
        ('M', 'S1'), ('M', 'S2'), ('M', 'S3')
    ]
    for u, v in regular_edges:
        ax.plot([nodes[u][0], nodes[v][0]], [nodes[u][1], nodes[v][1]], color='#cbd5e1', lw=1.2, zorder=2)

    # Highlight Reverse-BFS (Red)
    ax.plot([nodes['M'][0], nodes['F2'][0]], [nodes['M'][1], nodes['F2'][1]], color='#dc2626', lw=2.8, zorder=3)
    ax.plot([nodes['F2'][0], nodes['P2'][0]], [nodes['F2'][1], nodes['P2'][1]], color='#dc2626', lw=2.8, zorder=3)
    ax.annotate('', xy=nodes['F2'], xytext=nodes['M'],
                arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.4', color='#dc2626', lw=2.5), zorder=4)
    ax.annotate('', xy=nodes['P2'], xytext=nodes['F2'],
                arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.4', color='#dc2626', lw=2.5), zorder=4)

    # Highlight Forward-BFS (Cyan / Blue)
    ax.plot([nodes['M'][0], nodes['S1'][0]], [nodes['M'][1], nodes['S1'][1]], color='#0284c7', lw=2.8, zorder=3)
    ax.plot([nodes['M'][0], nodes['S2'][0]], [nodes['M'][1], nodes['S2'][1]], color='#0284c7', lw=2.8, zorder=3)
    ax.annotate('', xy=nodes['S1'], xytext=nodes['M'],
                arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.4', color='#0284c7', lw=2.5), zorder=4)
    ax.annotate('', xy=nodes['S2'], xytext=nodes['M'],
                arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.4', color='#0284c7', lw=2.5), zorder=4)

    # Draw Nodes
    for k, (nx, ny) in nodes.items():
        if k in ['P2', 'F2']:
            c = Circle((nx, ny), 14, facecolor='#fee2e2', edgecolor='#dc2626', lw=2.0, zorder=5)
            ax.add_patch(c)
            ax.text(nx, ny, k, fontsize=8.0, fontweight='bold', color='#991b1b', ha='center', va='center', zorder=6)
        elif k == 'M':
            c = Circle((nx, ny), 17, facecolor='#fef3c7', edgecolor='#d97706', lw=2.0, zorder=5)
            ax.add_patch(c)
            ax.text(nx, ny, "ML", fontsize=8.5, fontweight='bold', color='#92400e', ha='center', va='center', zorder=6)
        elif k in ['S1', 'S2']:
            c = Circle((nx, ny), 14, facecolor='#e0f2fe', edgecolor='#0284c7', lw=2.0, zorder=5)
            ax.add_patch(c)
            ax.text(nx, ny, k, fontsize=8.0, fontweight='bold', color='#075985', ha='center', va='center', zorder=6)
        else:
            c = Circle((nx, ny), 13, facecolor='#f8fafc', edgecolor='#64748b', lw=1.2, zorder=5)
            ax.add_patch(c)
            ax.text(nx, ny, k, fontsize=7.5, color='#334155', ha='center', va='center', zorder=6)

    # Traversal badges
    ax.text(1020, 755, "Reverse-BFS Root Cause\nBacktrack to Culprit (0.184 ms)",
            fontsize=7.4, fontweight='bold', color='#dc2626', ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.25", facecolor='#fef2f2', edgecolor='#f87171', lw=0.9))

    ax.text(1130, 565, "Forward-BFS Blast Radius\nImpact (2 Services)",
            fontsize=7.4, fontweight='bold', color='#0369a1', ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.25", facecolor='#f0f9ff', edgecolor='#38bdf8', lw=0.9))

    # Connection from Drift Engine to DAG
    ax.annotate('', xy=(840, 635), xytext=(770, 635),
                arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.4', color='#ca8a04', lw=1.8))
    ax.text(805, 648, "Drift Signals", fontsize=7.2, color='#a16207', ha='center', fontweight='bold')

    # -------------------------------------------------------------
    # 4. ALERT TRIAGE & PRIORITY MAX-HEAP (Mid-Left Bottom)
    # -------------------------------------------------------------
    g4 = FancyBboxPatch((380, 160), 410, 360, boxstyle="round,pad=0,rounding_size=10",
                        facecolor='#f8fafc', edgecolor='#64748b', lw=1.4, ls='--')
    ax.add_patch(g4)
    ax.text(585, 495, "4. Alert Prioritization Subsystem", fontsize=11.5, fontweight='bold', color='#1e293b', ha='center')

    heap_box = FancyBboxPatch((400, 185), 370, 285, boxstyle="round,pad=0,rounding_size=8",
                              facecolor='#fef2f2', edgecolor='#ef4444', lw=1.4)
    ax.add_patch(heap_box)
    ax.text(585, 445, "AlertMaxHeap (Binary Priority Queue)", fontsize=10.0, fontweight='bold', color='#b91c1c', ha='center')
    ax.text(585, 423, r"Time: $\mathcal{O}(\log K)$ Push/Pop | Space: $\mathcal{O}(K)$", fontsize=8.0, fontweight='bold', color='#991b1b', ha='center')
    ax.text(585, 401, "• Pure Sift-Up (_sift_up) & Sift-Down (_sift_down)", fontsize=7.8, color='#334155', ha='center')
    ax.text(585, 381, "• Dynamic Composite Severity Scoring Function:", fontsize=8.0, fontweight='bold', color='#1e293b', ha='center')
    ax.text(585, 357, r"$\sigma = 0.40 \cdot \Delta \mathrm{Acc} + 0.35 \cdot \left(\frac{\mathrm{PSI}}{0.50}\right) + 0.25 \cdot \left(\frac{\Delta t_{99}}{\mathrm{SLA}}\right)$",
            fontsize=8.5, color='#b91c1c', ha='center')
    ax.text(585, 328, "• Deterministic Highest-Severity Incident Popping", fontsize=7.8, color='#334155', ha='center')
    ax.text(585, 308, "• Automatic Anomaly Deduplication & Suppression", fontsize=7.8, color='#334155', ha='center')
    ax.text(585, 288, "• Dispatches Critical Triggers to Auto-Remediation", fontsize=7.8, fontweight='bold', color='#b91c1c', ha='center')

    # Binary heap graphic
    ax.plot([585, 550], [250, 228], color='#ef4444', lw=1.2)
    ax.plot([585, 620], [250, 228], color='#ef4444', lw=1.2)
    ax.add_patch(Circle((585, 250), 8, facecolor='#fee2e2', edgecolor='#dc2626', lw=1.2))
    ax.add_patch(Circle((550, 228), 7, facecolor='#ffffff', edgecolor='#ef4444', lw=1.0))
    ax.add_patch(Circle((620, 228), 7, facecolor='#ffffff', edgecolor='#ef4444', lw=1.0))
    ax.text(585, 250, "Max", fontsize=6.0, color='#b91c1c', ha='center', va='center', fontweight='bold')
    ax.text(585, 200, "Heap Triage (0.045 ms Push/Pop)", fontsize=7.2, color='#b91c1c', fontstyle='italic', ha='center')

    # Arrow from DAG to Heap
    ax.annotate('', xy=(770, 370), xytext=(840, 505),
                arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.4', color='#dc2626', lw=1.8,
                                connectionstyle="angle,angleA=-90,angleB=180,rad=10"))
    ax.text(805, 410, "Incidents &\nSeverity", fontsize=7.2, color='#991b1b', ha='center', fontweight='bold')

    # -------------------------------------------------------------
    # 5. CLOSED-LOOP REMEDIATION ENGINE (Right Top)
    # -------------------------------------------------------------
    g5 = FancyBboxPatch((1265, 440), 355, 490, boxstyle="round,pad=0,rounding_size=10",
                        facecolor='#f8fafc', edgecolor='#64748b', lw=1.4, ls='--')
    ax.add_patch(g5)
    ax.text(1442, 905, "5. Closed-Loop Remediation Engine", fontsize=11.5, fontweight='bold', color='#1e293b', ha='center')

    retrain_box = FancyBboxPatch((1285, 460), 315, 420, boxstyle="round,pad=0,rounding_size=8",
                                 facecolor='#f0fdf4', edgecolor='#16a34a', lw=1.4)
    ax.add_patch(retrain_box)
    ax.text(1442, 855, "Automated Retraining Pipeline", fontsize=10.0, fontweight='bold', color='#15803d', ha='center')
    ax.text(1442, 835, "1-Click or Threshold Auto-Trigger", fontsize=7.8, color='#166534', fontstyle='italic', ha='center')

    # Steps inside Retraining Pipeline
    steps = [
        ("Step 1: In-Memory Data Fusion", r"$\mathcal{D}_{\mathrm{train}} = \mathcal{D}_{\mathrm{base}} \cup \mathcal{D}_{\mathrm{live}}$", '#dcfce7'),
        ("Step 2: Incremental Model Re-fit", "Warm-start optimization / re-estimation", '#ffffff'),
        ("Step 3: 4-Step Production Gate", r"$\mathrm{Acc} \geq 85\%, \ \mathrm{SLA} \leq 200\mathrm{ms}, \ \mathrm{No \ NaN}$", '#ffffff'),
        ("Step 4: Atomic Version Promotion", r"Promote $\mathtt{v1.0.0} \to \mathtt{v1.1.0}$ & evict alerts", '#dcfce7')
    ]
    for idx, (st_title, st_desc, bg_c) in enumerate(steps):
        s_y = 755 - idx * 68
        s_patch = FancyBboxPatch((1305, s_y), 275, 54, boxstyle="round,pad=0,rounding_size=6",
                                 facecolor=bg_c, edgecolor='#16a34a', lw=1.0)
        ax.add_patch(s_patch)
        ax.text(1442, s_y + 34, st_title, fontsize=8.0, fontweight='bold', color='#14532d', ha='center')
        ax.text(1442, s_y + 14, st_desc, fontsize=7.4, color='#334155', ha='center')
        if idx < 3:
            ax.annotate('', xy=(1442, s_y - 2), xytext=(1442, s_y + 2),
                        arrowprops=dict(arrowstyle='->,head_width=0.22,head_length=0.22', color='#16a34a', lw=1.2))

    ax.text(1442, 475, "Safe Model Version Replacement", fontsize=7.5, color='#15803d', fontstyle='italic', ha='center')

    # -------------------------------------------------------------
    # 6. SRE OBSERVABILITY & CONSOLE (Bottom-Right)
    # -------------------------------------------------------------
    g6 = FancyBboxPatch((820, 160), 800, 260, boxstyle="round,pad=0,rounding_size=10",
                        facecolor='#f8fafc', edgecolor='#64748b', lw=1.4, ls='--')
    ax.add_patch(g6)
    ax.text(1220, 395, "6. SRE Observability Console & Incident Audit Plane", fontsize=11.5, fontweight='bold', color='#1e293b', ha='center')

    # Card A: Visualizer
    ca = FancyBboxPatch((840, 185), 240, 185, boxstyle="round,pad=0,rounding_size=6",
                        facecolor='#ffffff', edgecolor='#0284c7', lw=1.2)
    ax.add_patch(ca)
    ax.text(960, 345, "Interactive DAG Visualizer", fontsize=8.8, fontweight='bold', color='#0369a1', ha='center')
    ax.text(960, 320, "• Live topology state canvas", fontsize=7.6, color='#334155', ha='center')
    ax.text(960, 298, "• Color-coded node health status", fontsize=7.6, color='#334155', ha='center')
    ax.text(960, 276, "• Dynamic path traversals", fontsize=7.6, color='#334155', ha='center')
    ax.text(960, 254, "• Real-time edge pulse updates", fontsize=7.6, color='#334155', ha='center')
    ax.text(960, 220, "Status: HEALTHY / DRIFTED", fontsize=7.2, family='sans-serif', color='#0369a1', fontweight='bold', ha='center')

    # Card B: Audit Drawer
    cb = FancyBboxPatch((1100, 185), 240, 185, boxstyle="round,pad=0,rounding_size=6",
                        facecolor='#ffffff', edgecolor='#7c3aed', lw=1.2)
    ax.add_patch(cb)
    ax.text(1220, 345, "Session Audit Drawer", fontsize=8.8, fontweight='bold', color='#6d28d9', ha='center')
    ax.text(1220, 320, "• Chronological audit log", fontsize=7.6, color='#334155', ha='center')
    ax.text(1220, 298, "• 1-Click snapshot replay", fontsize=7.6, color='#334155', ha='center')
    ax.text(1220, 276, "• Metric state tracking over time", fontsize=7.6, color='#334155', ha='center')
    ax.text(1220, 254, "• Historical DAG comparison", fontsize=7.6, color='#334155', ha='center')
    ax.text(1220, 220, "Auditable Session Traceability", fontsize=7.2, color='#6d28d9', fontweight='bold', ha='center')

    # Card C: Post-Mortem Exporter
    cc = FancyBboxPatch((1360, 185), 240, 185, boxstyle="round,pad=0,rounding_size=6",
                        facecolor='#ffffff', edgecolor='#059669', lw=1.2)
    ax.add_patch(cc)
    ax.text(1480, 345, "Markdown Incident Exporter", fontsize=8.8, fontweight='bold', color='#047857', ha='center')
    ax.text(1480, 320, "• Comprehensive post-mortems", fontsize=7.6, color='#334155', ha='center')
    ax.text(1480, 298, "• Root cause + KS/PSI divergence", fontsize=7.6, color='#334155', ha='center')
    ax.text(1480, 276, "• Blast radius impact breakdown", fontsize=7.6, color='#334155', ha='center')
    ax.text(1480, 254, "• Automated remediation logs", fontsize=7.6, color='#334155', ha='center')
    ax.text(1480, 220, "1-Click Downloadable Report", fontsize=7.2, color='#047857', fontweight='bold', ha='center')

    # -------------------------------------------------------------
    # CONTROL PLANE BUSES & CONNECTIONS
    # -------------------------------------------------------------
    # 1. Trigger from Max-Heap to Retraining Pipeline (Clean route below DAG)
    ax.annotate('', xy=(1285, 520), xytext=(770, 270),
                arrowprops=dict(arrowstyle='->,head_width=0.35,head_length=0.4', color='#15803d', lw=2.0,
                                connectionstyle="angle,angleA=0,angleB=90,rad=15"))
    ax.text(1025, 430, r"Auto-Remediation Trigger (Severity $\sigma \geq \tau$)",
            fontsize=8.0, color='#15803d', ha='center', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#f0fdf4', edgecolor='#86efac', lw=0.8))

    # 2. Alert feed from Heap to SRE Console (Clean arrow pointing to Visualizer)
    ax.annotate('', xy=(840, 270), xytext=(770, 270),
                arrowprops=dict(arrowstyle='->,head_width=0.3,head_length=0.35', color='#b91c1c', lw=1.5))
    ax.text(805, 282, "Alert Feed", fontsize=7.2, color='#b91c1c', ha='center', fontweight='bold')

    # 3. Top Closed-Loop Feedback Bus (Clean upper arch)
    ax.plot([1442, 1442, 585, 585], [880, 940, 940, 880], color='#16a34a', lw=2.5, ls='-')
    ax.annotate('', xy=(585, 880), xytext=(585, 890),
                arrowprops=dict(arrowstyle='->,head_width=0.4,head_length=0.45', color='#16a34a', lw=2.5))
    ax.text(1013, 940, r"Closed-Loop Feedback: Update Baseline Quantiles $F_{\mathrm{base}}(x)$ & Reset DAG Health to HEALTHY",
            fontsize=8.2, fontweight='bold', color='#15803d', ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#f0fdf4', edgecolor='#22c55e', lw=1.2))

    # Bottom Micro-Benchmark Summary Bar
    ax.plot([30, 1620], [130, 130], color='#cbd5e1', lw=1.0)
    perf_text = "Empirical Micro-Benchmarks:  Inference Ingestion: 0.412 ms  |  Sliding Window Amortized: O(1)  |  Reverse-BFS Traversal: 0.184 ms  |  Heap Priority Push/Pop: 0.045 ms  |  Zero DB Locks"
    ax.text(825, 105, perf_text, fontsize=8.5, color='#475569', ha='center', va='center', fontweight='bold')

    # Save outputs
    plt.savefig(output_png_path, dpi=300, facecolor='#ffffff', edgecolor='none', bbox_inches='tight')
    plt.savefig(output_jpg_path, dpi=300, facecolor='#ffffff', edgecolor='none', bbox_inches='tight')
    plt.close(fig)
    print(f"Generated Academic Architecture Diagram at:\n  {output_png_path}\n  {output_jpg_path}")

if __name__ == "__main__":
    docs_fig_dir = r"c:\DS_CP\docs\figures"
    downloads_dir = r"C:\Users\akash\Downloads"
    os.makedirs(docs_fig_dir, exist_ok=True)
    
    png_docs = os.path.join(docs_fig_dir, "fig0_system_architecture.png")
    jpg_docs = os.path.join(docs_fig_dir, "fig0_system_architecture.jpg")
    
    draw_academic_architecture(png_docs, jpg_docs)
    
    # Copy directly to Downloads for instant user access
    shutil.copy2(png_docs, os.path.join(downloads_dir, "ArgusML_System_Architecture.png"))
    shutil.copy2(jpg_docs, os.path.join(downloads_dir, "ArgusML_System_Architecture.jpg"))
    print("Copied files to Downloads folder successfully!")
