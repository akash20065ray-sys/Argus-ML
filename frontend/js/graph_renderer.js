/**
 * Interactive DAG Topology Renderer for ArgusML.
 * Renders Data Pipeline -> Feature -> Model -> Downstream Services on Canvas.
 */

class GraphRenderer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.nodes = [];
    this.edges = [];
    this.hoveredNode = null;
    this.pulsePhase = 0;

    this.initCanvas();
    this.bindEvents();
    this.startAnimationLoop();
  }

  initCanvas() {
    // Handle retina display scaling
    const rect = this.canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    this.width = rect.width;
    this.height = rect.height;
    this.canvas.width = this.width * dpr;
    this.canvas.height = this.height * dpr;
    this.ctx.scale(dpr, dpr);
  }

  bindEvents() {
    window.addEventListener('resize', () => this.initCanvas());

    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      let found = null;
      for (const node of this.nodes) {
        const dist = Math.hypot(node.x - mouseX, node.y - mouseY);
        if (dist <= node.radius + 8) {
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

    // Assign coordinates
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
        const radius = node.type === 'MODEL' ? 24 : 16;

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
      this.pulsePhase = (this.pulsePhase + 0.05) % (Math.PI * 2);
      this.render();
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  render() {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.width, this.height);

    // Draw grid lines
    this.drawBackgroundGrid(ctx);

    // Draw edges
    this.edges.forEach((edge) => {
      if (edge.sourceNode && edge.targetNode) {
        this.drawEdge(ctx, edge);
      }
    });

    // Draw nodes
    this.nodes.forEach((node) => {
      this.drawNode(ctx, node);
    });

    // Tooltip for hovered node
    if (this.hoveredNode) {
      this.drawTooltip(ctx, this.hoveredNode);
    }
  }

  drawBackgroundGrid(ctx) {
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
    ctx.lineWidth = 1;
    const step = 30;
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
  }

  drawEdge(ctx, edge) {
    const { sourceNode, targetNode } = edge;
    const isDegraded =
      sourceNode.health === 'CRITICAL' || targetNode.health === 'CRITICAL';

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
      ctx.strokeStyle = 'rgba(255, 51, 102, 0.6)';
      ctx.lineWidth = 2.5;
      ctx.shadowColor = '#ff3366';
      ctx.shadowBlur = 8;
    } else {
      ctx.strokeStyle = 'rgba(79, 172, 254, 0.25)';
      ctx.lineWidth = 1.5;
    }
    ctx.stroke();

    // Animated signal packet along edge
    const t = (Math.sin(this.pulsePhase) + 1) / 2;
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
    ctx.fillStyle = isDegraded ? '#ff3366' : '#00f2fe';
    ctx.fill();

    ctx.restore();
  }

  drawNode(ctx, node) {
    const { x, y, radius, health, type, name } = node;

    ctx.save();

    let color = '#00f2a9'; // Healthy green
    let glow = 'rgba(0, 242, 169, 0.4)';

    if (health === 'CRITICAL') {
      color = '#ff3366'; // Critical crimson
      glow = 'rgba(255, 51, 102, 0.8)';
    } else if (health === 'WARNING') {
      color = '#ffb703'; // Warning amber
      glow = 'rgba(255, 183, 3, 0.6)';
    }

    // Glowing aura for critical nodes
    if (health === 'CRITICAL') {
      const pulseSize = radius + 6 + Math.sin(this.pulsePhase * 2) * 4;
      ctx.beginPath();
      ctx.arc(x, y, pulseSize, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255, 51, 102, 0.18)';
      ctx.fill();
    }

    // Outer ring
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = '#0f1422';
    ctx.fill();
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = color;
    ctx.shadowColor = glow;
    ctx.shadowBlur = 12;
    ctx.stroke();

    // Inner core
    ctx.beginPath();
    ctx.arc(x, y, radius * 0.4, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();

    // Node label
    ctx.shadowBlur = 0;
    ctx.font = '500 11px Inter, sans-serif';
    ctx.fillStyle = '#cbd5e1';
    ctx.textAlign = 'center';
    ctx.fillText(name, x, y + radius + 15);

    // Layer type sub-badge
    ctx.font = '600 8px JetBrains Mono, monospace';
    ctx.fillStyle = '#64748b';
    ctx.fillText(type, x, y - radius - 6);

    ctx.restore();
  }

  drawTooltip(ctx, node) {
    const pad = 12;
    const title = node.name;
    const sub = `Type: ${node.type} | Status: ${node.health}`;

    ctx.save();
    ctx.font = '600 12px Outfit, sans-serif';
    const titleWidth = ctx.measureText(title).width;
    ctx.font = '400 10px JetBrains Mono, monospace';
    const subWidth = ctx.measureText(sub).width;
    const boxW = Math.max(titleWidth, subWidth) + pad * 2;
    const boxH = 50;

    let bx = node.x - boxW / 2;
    let by = node.y - node.radius - boxH - 12;
    if (by < 10) by = node.y + node.radius + 20;

    ctx.fillStyle = 'rgba(15, 20, 34, 0.95)';
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.lineWidth = 1;
    ctx.roundRect(bx, by, boxW, boxH, 8);
    ctx.fill();
    ctx.stroke();

    ctx.font = '600 12px Outfit, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'left';
    ctx.fillText(title, bx + pad, by + 20);

    ctx.font = '400 10px JetBrains Mono, monospace';
    ctx.fillStyle = node.health === 'CRITICAL' ? '#ff3366' : '#00f2fe';
    ctx.fillText(sub, bx + pad, by + 38);

    ctx.restore();
  }
}

window.GraphRenderer = GraphRenderer;
