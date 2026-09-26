"""
Generate high-resolution architecture_diagram.png with Maroon & Gold styling.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    fig.patch.set_facecolor('#0A0A0C')
    ax.set_facecolor('#0A0A0C')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Color tokens
    BG_CARD = '#161118'
    BORDER_MAROON = '#881337'
    BORDER_GOLD = '#F59E0B'
    TEXT_WHITE = '#FFFFFF'
    TEXT_GOLD = '#FCD34D'
    TEXT_MUTED = '#9CA3AF'
    TEXT_CYAN = '#38BDF8'
    ACCENT_GREEN = '#10B981'

    # Title
    ax.text(7, 7.55, "ArgusML: Master 5-Layer System Architecture & Telemetry Pipeline", 
            ha='center', va='center', color=TEXT_WHITE, fontsize=15, fontweight='bold')
    ax.text(7, 7.2, "Decoupled Asynchronous Streaming & In-Memory DSA Engine", 
            ha='center', va='center', color=TEXT_GOLD, fontsize=9.5, fontweight='semibold')

    # Layer Cards
    layers = [
        ("Layer 1: Ingestion Buffer", "Circular FIFO EventQueue (O(1))\n• Modulo Pointer Wrapping\n• Zero Backpressure Drop\n• Capacity: 5,000 events", 0.6, 2.2, BORDER_GOLD),
        ("Layer 2: Rolling Telemetry", "MetricSlidingWindow Deque (O(1))\n• Rolling Accuracy, Precision, F1\n• P50, P95, P99 Latency (ms)\n• Size: W = 400 predictions", 3.2, 2.2, BORDER_MAROON),
        ("Layer 3: Statistical Drift", "DriftEngine & ModelRegistry\n• In-Memory HashMap Baselines\n• 2-Sample KS-Test (D stat, p-val)\n• PSI (Quantile Binning >= 0.25)", 5.8, 2.2, BORDER_GOLD),
        ("Layer 4: Topological RCA", "Dynamic DependencyGraph (O(V+E))\n• 4-Layer Dynamic DAG Modeling\n• Reverse-BFS: Upstream Culprit\n• Forward-BFS: Downstream Blast", 8.4, 2.2, BORDER_MAROON),
        ("Layer 5: Priority Heap", "AlertMaxHeap Priority Queue (O(log N))\n• Pure _sift_up / _sift_down\n• Composite Severity Scoring\n• Root Cause Confidence (RCS)", 11.0, 2.2, BORDER_GOLD),
    ]

    for title, desc, x, w, border_col in layers:
        # Card Box
        rect = patches.FancyBboxPatch((x, 3.2), w, 3.5,
                                      boxstyle="round,pad=0.15,rounding_size=0.15",
                                      facecolor=BG_CARD, edgecolor=border_col, linewidth=2.0)
        ax.add_patch(rect)

        # Header bar
        header_rect = patches.FancyBboxPatch((x, 6.2), w, 0.5,
                                             boxstyle="round,pad=0.08,rounding_size=0.1",
                                             facecolor='#27131F', edgecolor=border_col, linewidth=1.0)
        ax.add_patch(header_rect)
        ax.text(x + w/2, 6.45, title, ha='center', va='center', color=TEXT_GOLD, fontsize=8.5, fontweight='bold')

        # Content
        ax.text(x + 0.12, 4.65, desc, ha='left', va='center', color=TEXT_WHITE, fontsize=7.5, linespacing=1.6)

    # Connecting Arrows
    arrow_props = dict(arrowstyle="->,head_width=0.4,head_length=0.6", color='#F59E0B', lw=2.0)
    for i in range(4):
        x_start = 0.6 + i * 2.6 + 2.2 + 0.05
        x_end = 0.6 + (i + 1) * 2.6 - 0.05
        ax.annotate("", xy=(x_end, 4.95), xytext=(x_start, 4.95), arrowprops=arrow_props)
        ax.text((x_start + x_end)/2, 5.25, f"Step {i+1}", ha='center', va='center', color='#FDE68A', fontsize=7, fontweight='bold')

    # Bottom Closed-Loop Retraining & History Section
    bot_rect = patches.FancyBboxPatch((0.6, 0.5), 12.6, 2.2,
                                      boxstyle="round,pad=0.15,rounding_size=0.15",
                                      facecolor='#1C121A', edgecolor='#DC2626', linewidth=2.0)
    ax.add_patch(bot_rect)

    ax.text(6.9, 2.35, "Closed-Loop Self-Healing & Observability Engine (Phases 7, 8 & 9)", 
            ha='center', va='center', color='#FCA5A5', fontsize=10.5, fontweight='bold')

    sub_boxes = [
        ("Phase 7: 1-Click Retraining Gate", "• Fit candidate on drifted window\n• 4-Step Validation Criteria\n• Version Promotion (v1.0 -> v1.1)\n• Max-Heap Alert Auto-Resolution", 0.9, 3.8),
        ("Phase 8: Post-Mortem Exporter", "• Automated Markdown Generation\n• Root Cause Confidence (RCS)\n• KS / PSI Statistical Evidence\n• Impacted Blast Radius Summary", 5.0, 3.8),
        ("Phase 9: Session History Drawer", "• Chronological Test Session Audit\n• In-Place 4s Telemetry Deduplication\n• 1-Click Interactive DAG Replay\n• Filter by Drift / Retrain / Model", 9.1, 3.8)
    ]

    for s_title, s_desc, sx, sw in sub_boxes:
        s_rect = patches.FancyBboxPatch((sx, 0.75), sw, 1.35,
                                        boxstyle="round,pad=0.08,rounding_size=0.08",
                                        facecolor='#0D090E', edgecolor='#881337', linewidth=1.2)
        ax.add_patch(s_rect)
        ax.text(sx + sw/2, 1.85, s_title, ha='center', va='center', color='#FDE047', fontsize=8, fontweight='bold')
        ax.text(sx + 0.12, 1.25, s_desc, ha='left', va='center', color=TEXT_WHITE, fontsize=6.8, linespacing=1.4)

    plt.tight_layout()
    output_png = "docs/architecture_diagram.png"
    plt.savefig(output_png, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[SUCCESS] Generated architecture diagram at {output_png}")

if __name__ == "__main__":
    create_architecture_diagram()
