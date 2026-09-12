/**
 * Interactive DAG Topology Renderer for ArgusML.
 * Dynamically visualizes: Upstream Ingestion -> Features -> Model -> Downstream Services.
 * Features: High-DPI crisp rendering, animated data signals, pulsating degradation halos, and hover tooltips.
 */

class GraphRenderer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.nodes = [];
    this.edges = [];
    this.hoveredNode = null;
    this.pulsePhase = 0;
    this.width = 800;
    this.height = 460;

    this.initCanvas();
    this.bindEvents();
    this.startAnimationLoop();
  }

  initCanvas() {
    if (!this.canvas) return;
    const parent = this.canvas.parentElement;
    const rect = parent ? parent.getBoundingClientRect() : this.canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;

    this.width = Math.max(rect.width || 800, 600);
    this.height = Math.max(rect.height || 460, 400);

    this.canvas.width = this.width * dpr;
    this.canvas.height = this.height * dpr;
    this.ctx.resetTransform ? this.ctx.resetTransform() : this.ctx.setTransform(1, 0, 0, 1, 0, 0);
    this.ctx.scale(dpr, dpr);
  }

  bindEvents() {
    // Automatically handle container resize
    if (window.ResizeObserver && this.canvas.parentElement) {
      const ro = new ResizeObserver(() => {
        this.initCanvas();
        if (this.lastGraphData) {
          this.updateData(this.lastGraphData);
        }
      });
      ro.observe(this.canvas.parentElement);
    } else {
      window.addEventListener('resize', () => {
        this.initCanvas();
        if (this.lastGraphData) this.updateData(this.lastGraphData);
      });
    }

    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      let found = null;
      for (const node of this.nodes) {
        const dist = Math.hypot(node.x - mouseX, node.y - mouseY);
        if (dist <= node.radius + 12) {
          found = node;
          break;
        }
      }
      this.hoveredNode = found;
      this.canvas.style.cursor = found ? 'pointer' : 'default';
    });

    this.canvas.addEventListener('click', () => {
      if (this.hoveredNode && window.onGraphNodeClick) {
        window.onGraphNodeClick(this.hoveredNode);
      }
    });
  }

  updateData(graphData) {
    if (!graphData || !graphData.nodes) return;
    this.lastGraphData = graphData;

    // Categorize nodes into 4 topological layers
    const layers = {
      PIPELINE: [],
      FEATURE: [],
      MODEL: [],
      SERVICE: [],
    };

    graphData.nodes.forEach((n) => {
      if (layers[n.type]) {
        layers[n.type].push(n);
      }
    });

    const w = this.width;
    const h = this.height;

    // Assign dynamic column positions across full width
    const layerX = {
      PIPELINE: w * 0.12,
      FEATURE: w * 0.38,
      MODEL: w * 0.65,
      SERVICE: w * 0.88,
    };

    const positionedNodes = [];
    const nodeMap = {};

    Object.keys(layers).forEach((layerKey) => {
      const group = layers[layerKey];
      const count = group.length;
      const spacing = h / (count + 1);

      group.forEach((node, idx) => {
        const x = layerX[layerKey];
        const y = spacing * (idx + 1);
        const radius = node.type === 'MODEL' ? 22 : node.type === 'PIPELINE' ? 16 : 14;

        const pNode = {
          ...node,
          x,
          y,
          radius,
        };
        positionedNodes.push(pNode);
        nodeMap[node.id] = pNode;
      });
    });

    this.nodes = positionedNodes;
    this.edges = (graphData.edges || []).map((e) => ({
      ...e,
      sourceNode: nodeMap[e.source],
      targetNode: nodeMap[e.target],
    }));
  }

  startAnimationLoop() {
    const loop = () => {
      this.pulsePhase = (this.pulsePhase + 0.04) % (Math.PI * 2);
      this.render();
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  render() {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.width, this.height);

    // 1. Subtle background grid
    this.drawBackgroundGrid(ctx);

    // 2. Draw DAG connection edges & animated signal packets
    this.edges.forEach((edge) => {
      if (edge.sourceNode && edge.targetNode) {
        this.drawEdge(ctx, edge);
      }
    });

    // 3. Draw nodes
    this.nodes.forEach((node) => {
      this.drawNode(ctx, node);
    });

    // 4. Draw interactive hover tooltip
    if (this.hoveredNode) {
      this.drawTooltip(ctx, this.hoveredNode);
    }
  }

  drawBackgroundGrid(ctx) {
    ctx.save();
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.025)';
    ctx.lineWidth = 1;
    const step = 35;
    for (let x = 0; x < this.width; x += step) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, this.height);
      ctx.stroke();
    }
    for (let y = 0; y < this.height; y += step) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(this.width, y);
      ctx.stroke();
    }
    ctx.restore();
  }

  drawEdge(ctx, edge) {
    const { sourceNode, targetNode } = edge;
    const isDegraded = sourceNode.health === 'CRITICAL' || targetNode.health === 'CRITICAL';

    ctx.save();
    ctx.beginPath();
    ctx.moveTo(sourceNode.x, sourceNode.y);

    // Smooth Bezier Curve
    const cpX1 = (sourceNode.x + targetNode.x) / 2;
    const cpY1 = sourceNode.y;
    const cpX2 = cpX1;
    const cpY2 = targetNode.y;

    ctx.bezierCurveTo(cpX1, cpY1, cpX2, cpY2, targetNode.x, targetNode.y);

    if (isDegraded) {
      ctx.strokeStyle = 'rgba(239, 68, 68, 0.7)';
      ctx.lineWidth = 2.5;
      ctx.shadowColor = '#ef4444';
      ctx.shadowBlur = 8;
    } else {
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.25)';
      ctx.lineWidth = 1.5;
    }
    ctx.stroke();

    // Animated signal packet along edge
    const t = (Math.sin(this.pulsePhase + (sourceNode.y % 5)) + 1) / 2;
    const packetX =
      Math.pow(1 - t, 3) * sourceNode.x +
      3 * Math.pow(1 - t, 2) * t * cpX1 +
      3 * (1 - t) * Math.pow(t, 2) * cpX2 +
      Math.pow(t, 3) * targetNode.x;
    const packetY =
      Math.pow(1 - t, 3) * sourceNode.y +
      3 * Math.pow(1 - t, 2) * t * cpY1 +
      3 * (1 - t) * Math.pow(t, 2) * cpY2 +
      Math.pow(t, 3) * targetNode.y;

    ctx.beginPath();
    ctx.arc(packetX, packetY, 2.5, 0, Math.PI * 2);
    ctx.fillStyle = isDegraded ? '#ef4444' : '#00f2fe';
    ctx.shadowColor = isDegraded ? '#ef4444' : '#00f2fe';
    ctx.shadowBlur = 6;
    ctx.fill();

    ctx.restore();
  }

  drawNode(ctx, node) {
    const { x, y, radius, health, type, name } = node;

    ctx.save();

    let color = '#10b981'; // Healthy Emerald
    let glow = 'rgba(16, 185, 129, 0.5)';

    if (health === 'CRITICAL') {
      color = '#ef4444'; // Crimson
      glow = 'rgba(239, 68, 68, 0.9)';
    } else if (health === 'WARNING') {
      color = '#f59e0b'; // Amber
      glow = 'rgba(245, 158, 11, 0.7)';
    }

    // Glowing pulsating aura for degraded nodes
    if (health === 'CRITICAL') {
      const pulseSize = radius + 8 + Math.sin(this.pulsePhase * 3) * 5;
      ctx.beginPath();
      ctx.arc(x, y, pulseSize, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(239, 68, 68, 0.2)';
      ctx.fill();
    }

    // Outer node circle
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = '#0d1322';
    ctx.fill();
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = color;
    ctx.shadowColor = glow;
    ctx.shadowBlur = 10;
    ctx.stroke();

    // Inner core
    ctx.beginPath();
    ctx.arc(x, y, radius * 0.45, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();

    // Layer type label above node
    ctx.shadowBlur = 0;
    ctx.font = '700 8px JetBrains Mono, monospace';
    ctx.fillStyle = '#64748b';
    ctx.textAlign = 'center';
    ctx.fillText(type, x, y - radius - 5);

    // Formatted node name label below node
    const displayName = this.formatLabel(name);
    ctx.font = '600 10.5px Inter, sans-serif';
    ctx.fillStyle = health === 'CRITICAL' ? '#fca5a5' : '#e2e8f0';
    ctx.textAlign = 'center';

    if (Array.isArray(displayName)) {
      ctx.fillText(displayName[0], x, y + radius + 13);
      ctx.fillText(displayName[1], x, y + radius + 24);
    } else {
      ctx.fillText(displayName, x, y + radius + 14);
    }

    ctx.restore();
  }

  formatLabel(text) {
    if (!text) return '';
    // Format feature or service names for clean rendering
    let clean = text.replace(/_/g, ' ');
    if (clean.length > 18) {
      const words = clean.split(' ');
      if (words.length >= 2) {
        const mid = Math.ceil(words.length / 2);
        return [words.slice(0, mid).join(' '), words.slice(mid).join(' ')];
      }
      return clean.slice(0, 16) + '...';
    }
    return clean;
  }

  drawTooltip(ctx, node) {
    const pad = 12;
    const title = node.name;
    const sub = `Type: ${node.type} | Status: ${node.health}`;

    ctx.save();
    ctx.font = '700 12px Outfit, sans-serif';
    const titleWidth = ctx.measureText(title).width;
    ctx.font = '500 10px JetBrains Mono, monospace';
    const subWidth = ctx.measureText(sub).width;
    const boxW = Math.max(titleWidth, subWidth) + pad * 2;
    const boxH = 52;

    let bx = node.x - boxW / 2;
    let by = node.y - node.radius - boxH - 12;
    if (by < 10) by = node.y + node.radius + 24;

    ctx.fillStyle = 'rgba(13, 19, 34, 0.98)';
    ctx.strokeStyle = 'rgba(0, 242, 254, 0.4)';
    ctx.lineWidth = 1;
    ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
    ctx.shadowBlur = 12;
    ctx.roundRect(bx, by, boxW, boxH, 8);
    ctx.fill();
    ctx.stroke();

    ctx.shadowBlur = 0;
    ctx.font = '700 12px Outfit, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'left';
    ctx.fillText(title, bx + pad, by + 20);

    ctx.font = '600 10px JetBrains Mono, monospace';
    ctx.fillStyle = node.health === 'CRITICAL' ? '#ef4444' : '#00f2fe';
    ctx.fillText(sub, bx + pad, by + 38);

    ctx.restore();
  }
}

window.GraphRenderer = GraphRenderer;
