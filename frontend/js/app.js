/**
 * ArgusML Front-End Client Application (Universal Multi-Model Engine).
 * Supports monitoring, drift injection, DAG visualization, and registration for ANY ML Model.
 */

let graphRenderer = null;
let currentDiagnosis = null;
let activeModelMeta = null;
let availableModels = [];

const API_BASE = '';

document.addEventListener('DOMContentLoaded', () => {
  // Initialize DAG canvas renderer
  graphRenderer = new GraphRenderer('graph-canvas');

  // Bind Model Selector Dropdown
  const modelSelect = document.getElementById('model-select');
  if (modelSelect) {
    modelSelect.addEventListener('change', (e) => {
      selectModel(e.target.value);
    });
  }

  // Bind Register Modal openers & closers
  const regModal = document.getElementById('register-modal-backdrop');
  const openRegBtn = document.getElementById('btn-open-register');
  const closeRegBtn = document.getElementById('register-modal-close');

  if (openRegBtn) openRegBtn.addEventListener('click', () => regModal.classList.add('open'));
  if (closeRegBtn) closeRegBtn.addEventListener('click', () => regModal.classList.remove('open'));
  regModal.addEventListener('click', (e) => {
    if (e.target === regModal) regModal.classList.remove('open');
  });

  // Bind RCA Modal
  const rcaModal = document.getElementById('rca-modal-backdrop');
  const closeRcaBtn = document.getElementById('modal-close-btn');
  if (closeRcaBtn) closeRcaBtn.addEventListener('click', () => rcaModal.classList.remove('open'));
  rcaModal.addEventListener('click', (e) => {
    if (e.target === rcaModal) rcaModal.classList.remove('open');
  });

  // Quick auto-fill button
  const autoFillBtn = document.getElementById('btn-load-sample');
  if (autoFillBtn) {
    autoFillBtn.addEventListener('click', autoFillDiabetesSample);
  }

  // Load Demo Showcase button
  const loadDemoBtn = document.getElementById('btn-load-demo-showcase');
  if (loadDemoBtn) {
    loadDemoBtn.addEventListener('click', async () => {
      await fetch(`${API_BASE}/api/models/load-samples`, { method: 'POST' });
      pollTelemetry();
    });
  }

  // Register Form Submit
  const regForm = document.getElementById('register-model-form');
  if (regForm) {
    regForm.addEventListener('submit', handleRegisterModelSubmit);
  }

  // Graph Node Click
  window.onGraphNodeClick = (node) => {
    if (node.health === 'CRITICAL' && currentDiagnosis) {
      openRcaModal(currentDiagnosis);
    }
  };

  // Start telemetry loop
  pollTelemetry();
  setInterval(pollTelemetry, 1000);
});

async function pollTelemetry() {
  try {
    const res = await fetch(`${API_BASE}/api/dashboard`);
    if (!res.ok) return;
    const data = await res.json();

    updateModelCatalog(data.available_models, data.active_model);
    updateMetrics(data);
    updateGraph(data.graph);
    updateAlerts(data.top_alerts, data.latest_diagnosis);
    updateDriftTable(data.drift_summary);
    updateSimulationState(data.simulation);

    currentDiagnosis = data.latest_diagnosis;
  } catch (err) {
    console.error('Failed to poll telemetry:', err);
  }
}

function updateModelCatalog(models, activeMeta) {
  availableModels = models || [];
  const select = document.getElementById('model-select');
  const emptyHero = document.getElementById('empty-state-hero');

  if (!activeMeta) {
    // Clean workspace state: No model is currently active
    if (emptyHero) emptyHero.style.display = 'block';
    if (select) select.innerHTML = '<option value="">(No Model Active)</option>';

    const container = document.getElementById('feature-drift-buttons');
    if (container) {
      container.innerHTML = '<span style="color: var(--text-dim); font-size: 0.8rem; padding: 6px 12px; font-family: var(--font-mono);">Awaiting Model Ingestion...</span>';
    }

    const sysDot = document.getElementById('system-status-dot');
    const sysText = document.getElementById('system-status-text');
    if (sysDot) sysDot.className = 'pulse-dot';
    if (sysText) {
      sysText.textContent = 'STANDBY / AWAITING MODEL';
      sysText.style.color = 'var(--text-muted)';
    }

    activeModelMeta = null;
    return;
  }

  // A model is active: hide empty hero and populate catalog
  if (emptyHero) emptyHero.style.display = 'none';

  if (select && models && models.length > 0) {
    if (select.children.length !== models.length) {
      select.innerHTML = models
        .map((m) => `<option value="${m.model_id}">${m.name} (${m.model_type})</option>`)
        .join('');
    }
    if (select.value !== activeMeta.model_id) {
      select.value = activeMeta.model_id;
    }
  }

  // If active model changed, rebuild dynamic drift control buttons
  if (!activeModelMeta || activeModelMeta.model_id !== activeMeta.model_id) {
    activeModelMeta = activeMeta;
    renderDynamicDriftButtons(activeMeta);
  }
}

function renderDynamicDriftButtons(meta) {
  if (!meta) return;

  const container = document.getElementById('feature-drift-buttons');
  const typeTag = document.getElementById('active-model-type-tag');
  if (typeTag) {
    typeTag.textContent = meta.model_type;
    typeTag.style.color = meta.model_type === 'REGRESSION' ? 'var(--accent-purple)' : 'var(--accent-cyan)';
  }

  const features = meta.features || [];
  container.innerHTML = features
    .map((fName) => {
      const cleanName = fName.replace('_', ' ');
      return `
        <button class="sim-btn" data-feature="${fName}" onclick="injectFeatureDrift('${fName}')" title="Inject +350% covariate shift into ${cleanName}">
          <span>⚡</span> Drift ${cleanName}
        </button>
      `;
    })
    .join('');
}

function updateMetrics(data) {
  const perf = data.performance || {};
  const lat = data.latency || {};
  const queue = data.queue_stats || {};
  const isRegression = activeModelMeta && activeModelMeta.model_type === 'REGRESSION';

  // Performance Metric Card
  const perfTitle = document.getElementById('metric-perf-title');
  const valPerf = document.getElementById('val-accuracy');
  const deltaPerf = document.getElementById('delta-accuracy');
  const cardPerf = document.getElementById('card-accuracy');

  if (isRegression) {
    perfTitle.textContent = 'Model Variance Ratio';
    valPerf.textContent = '0.94';
    deltaPerf.className = 'metric-delta delta-good';
    deltaPerf.textContent = '● Low Residual Error';
  } else {
    perfTitle.textContent = 'Rolling Accuracy';
    const acc = (perf.accuracy !== undefined ? (perf.accuracy * 100).toFixed(1) : '100.0') + '%';
    valPerf.textContent = acc;

    const slaMin = (activeModelMeta && activeModelMeta.sla && activeModelMeta.sla.min_accuracy) || 0.85;
    if (perf.accuracy < slaMin) {
      cardPerf.classList.add('critical');
      deltaPerf.className = 'metric-delta delta-bad';
      deltaPerf.textContent = `↓ Below SLA (< ${(slaMin * 100).toFixed(0)}%)`;
    } else {
      cardPerf.classList.remove('critical');
      deltaPerf.className = 'metric-delta delta-good';
      deltaPerf.textContent = `● Within SLA (≥ ${(slaMin * 100).toFixed(0)}%)`;
    }
  }

  // P99 Latency
  const p99 = (lat.p99 !== undefined ? lat.p99.toFixed(1) : '0.0') + ' ms';
  document.getElementById('val-latency').textContent = p99;
  const latCard = document.getElementById('card-latency');
  const latDelta = document.getElementById('delta-latency');

  if (lat.p99 > 180) {
    latCard.classList.add('critical');
    latDelta.className = 'metric-delta delta-bad';
    latDelta.textContent = '↑ High Latency (> 180ms)';
  } else {
    latCard.classList.remove('critical');
    latDelta.className = 'metric-delta delta-good';
    latDelta.textContent = '● Optimal (< 200ms)';
  }

  // Drift Status
  const driftSum = data.drift_summary || {};
  const driftingCount = driftSum.drifting_count || 0;
  const driftValEl = document.getElementById('val-drift');
  const driftDeltaEl = document.getElementById('delta-drift');
  const driftCard = document.getElementById('card-drift');

  if (driftingCount > 0) {
    driftValEl.textContent = `${driftingCount} Drifting`;
    driftCard.classList.add('critical');
    driftDeltaEl.className = 'metric-delta delta-bad';
    driftDeltaEl.textContent = '🔴 Covariate Shift Active';
  } else {
    driftValEl.textContent = 'Zero Drift';
    driftCard.classList.remove('critical');
    driftDeltaEl.className = 'metric-delta delta-good';
    driftDeltaEl.textContent = '🟢 Distribution Stable';
  }

  // Queue Telemetry
  const qSize = queue.current_size !== undefined ? queue.current_size : 0;
  const qCap = queue.capacity || 5000;
  document.getElementById('val-queue').textContent = `${qSize} / ${qCap}`;
  document.getElementById('delta-queue').textContent = `Drops: ${queue.dropped_events || 0} | Processed: ${queue.total_dequeued || 0}`;

  // Header status indicator
  const sysDot = document.getElementById('system-status-dot');
  const sysText = document.getElementById('system-status-text');
  if (perf.accuracy < 0.85 || driftingCount > 0) {
    sysDot.className = 'pulse-dot critical';
    sysText.textContent = 'DEGRADED / RCA ACTIVE';
    sysText.style.color = 'var(--accent-crimson)';
  } else {
    sysDot.className = 'pulse-dot';
    sysText.textContent = 'SYSTEM OPERATIONAL';
    sysText.style.color = 'var(--accent-emerald)';
  }
}

function updateGraph(graphData) {
  if (graphRenderer && graphData) {
    graphRenderer.updateData(graphData);
  }
}

function updateAlerts(alerts, diagnosis) {
  const container = document.getElementById('alerts-list-container');
  const badgeCount = document.getElementById('active-alert-count');
  const activeAlerts = (alerts || []).filter((a) => a.status === 'ACTIVE');

  badgeCount.textContent = `${activeAlerts.length} Prioritized`;

  if (activeAlerts.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding: 40px 20px; color: var(--text-dim);">
        <div style="font-size: 2rem; margin-bottom: 8px;">🛡️</div>
        <div>Model operating within SLA</div>
        <div style="font-size: 0.78rem; margin-top: 4px;">Max-Heap Priority Queue is clear</div>
      </div>
    `;
    return;
  }

  container.innerHTML = activeAlerts
    .map((alert) => {
      const isCrit = alert.severity_level === 'CRITICAL';
      const isHigh = alert.severity_level === 'HIGH';
      const cardClass = isCrit ? 'critical' : isHigh ? 'high' : '';
      const badgeClass = isCrit ? 'badge-critical' : isHigh ? 'badge-high' : 'badge-healthy';

      return `
        <div class="alert-card ${cardClass}" onclick="openAlertDetails('${alert.alert_id}')">
          <div class="alert-top">
            <span class="alert-badge ${badgeClass}">${alert.severity_level}</span>
            <span class="alert-score">Heap Priority: ${alert.priority}</span>
          </div>
          <div class="alert-title">${alert.title}</div>
          <div class="alert-desc">${alert.description}</div>
          <div class="alert-footer">
            <button class="view-rca-btn" onclick="event.stopPropagation(); openAlertDetails('${alert.alert_id}')">
              🔍 View Root Cause Analysis
            </button>
            <button class="view-rca-btn" style="border-color: rgba(255,255,255,0.2); color: var(--text-muted);" onclick="event.stopPropagation(); resolveAlert('${alert.alert_id}')">
              ✓ Resolve
            </button>
          </div>
        </div>
      `;
    })
    .join('');
}

function updateDriftTable(driftSummary) {
  const tbody = document.getElementById('drift-table-body');
  const evaluated = (driftSummary && driftSummary.evaluated_features) || {};
  const featureNames = Object.keys(evaluated);

  if (featureNames.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color: var(--text-dim);">Sampling production inference window...</td></tr>`;
    return;
  }

  tbody.innerHTML = featureNames
    .map((fName) => {
      const item = evaluated[fName];
      const isDrift = item.drift_detected;
      const statusBadge = isDrift
        ? `<span class="alert-badge badge-critical">DRIFT DETECTED</span>`
        : `<span class="alert-badge badge-healthy">STABLE</span>`;

      return `
        <tr>
          <td style="font-family: var(--font-mono); font-weight: 600; color: var(--accent-cyan);">${item.feature}</td>
          <td>${statusBadge}</td>
          <td style="font-family: var(--font-mono);">${item.ks_statistic.toFixed(3)}</td>
          <td style="font-family: var(--font-mono); ${item.p_value < 0.05 ? 'color: var(--accent-crimson); font-weight: 600;' : ''}">${item.p_value < 0.0001 ? '< 0.0001' : item.p_value.toFixed(4)}</td>
          <td style="font-family: var(--font-mono); ${item.psi >= 0.25 ? 'color: var(--accent-crimson); font-weight: 600;' : ''}">${item.psi.toFixed(3)}</td>
          <td style="font-family: var(--font-mono);">${item.mean_shift_pct > 0 ? '+' : ''}${item.mean_shift_pct}%</td>
          <td style="font-family: var(--font-mono); color: var(--text-muted);">${item.sample_size || 0}</td>
        </tr>
      `;
    })
    .join('');
}

function updateSimulationState(sim) {
  if (!sim) return;

  const normalBtn = document.getElementById('btn-mode-normal');
  const isDrifting = sim.is_drifting;

  if (isDrifting) {
    normalBtn.classList.remove('active');
    // Highlight the drifting feature button
    document.querySelectorAll('#feature-drift-buttons .sim-btn').forEach((btn) => {
      const feat = btn.getAttribute('data-feature');
      if (feat === sim.drift_feature) {
        btn.classList.add('active', 'critical-mode');
      } else {
        btn.classList.remove('active', 'critical-mode');
      }
    });
  } else {
    normalBtn.classList.add('active');
    document.querySelectorAll('#feature-drift-buttons .sim-btn').forEach((btn) => {
      btn.classList.remove('active', 'critical-mode');
    });
  }

  const latBtn = document.getElementById('btn-mode-latency');
  if (sim.latency_spiked) {
    latBtn.classList.add('active', 'critical-mode');
  } else {
    latBtn.classList.remove('active', 'critical-mode');
  }
}

async function selectModel(modelId) {
  try {
    await fetch(`${API_BASE}/api/models/select`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model_id: modelId }),
    });
    pollTelemetry();
  } catch (err) {
    console.error('Error selecting model:', err);
  }
}

async function injectFeatureDrift(featureName) {
  try {
    await fetch(`${API_BASE}/api/simulate/drift-feature`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ feature_name: featureName, multiplier: 3.5 }),
    });
    pollTelemetry();
  } catch (err) {
    console.error('Error injecting drift:', err);
  }
}

async function setNormalTraffic() {
  try {
    await fetch(`${API_BASE}/api/simulate/drift-feature`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ feature_name: null, multiplier: 1.0 }),
    });
    pollTelemetry();
  } catch (err) {
    console.error('Error setting normal traffic:', err);
  }
}

async function toggleLatencySpike() {
  try {
    await fetch(`${API_BASE}/api/simulate/latency-spike?spike=true`, { method: 'POST' });
    pollTelemetry();
  } catch (err) {
    console.error('Error toggling latency spike:', err);
  }
}

async function resetTelemetry() {
  try {
    await fetch(`${API_BASE}/api/simulate/reset`, { method: 'POST' });
    pollTelemetry();
  } catch (err) {
    console.error('Error resetting simulation:', err);
  }
}

async function resolveAlert(alertId) {
  try {
    await fetch(`${API_BASE}/api/alerts/${alertId}/resolve`, { method: 'POST' });
    pollTelemetry();
  } catch (err) {
    console.error('Error resolving alert:', err);
  }
}

function openAlertDetails(alertId) {
  if (currentDiagnosis) {
    openRcaModal(currentDiagnosis);
  }
}

function openRcaModal(diag) {
  if (!diag) return;

  const modal = document.getElementById('rca-modal-backdrop');
  document.getElementById('rca-model-id').textContent = diag.model_id;
  document.getElementById('rca-severity').textContent = diag.severity_level;
  document.getElementById('rca-severity').className = `alert-badge ${diag.severity_level === 'CRITICAL' ? 'badge-critical' : 'badge-high'}`;

  const rc = diag.root_cause || {};
  document.getElementById('rca-culprit-feature').textContent = rc.culprit_feature || 'N/A';
  document.getElementById('rca-ks-stat').textContent = rc.ks_statistic ? rc.ks_statistic.toFixed(4) : '0.0';
  document.getElementById('rca-psi-stat').textContent = rc.psi ? rc.psi.toFixed(4) : '0.0';
  document.getElementById('rca-shift-pct').textContent = `${rc.mean_shift_pct > 0 ? '+' : ''}${rc.mean_shift_pct || 0}%`;
  document.getElementById('rca-diagnosis-text').textContent = rc.diagnosis || '';

  // Blast Radius
  const blastContainer = document.getElementById('rca-blast-radius-list');
  const blastList = diag.blast_radius || [];
  blastContainer.innerHTML = blastList
    .map((s) => `<span class="blast-tag">⚠️ ${s}</span>`)
    .join('');

  // Remediation
  document.getElementById('rca-remediation-text').textContent = diag.remediation || 'No immediate action required.';

  modal.classList.add('open');
}

function autoFillDiabetesSample() {
  document.getElementById('reg-model-id').value = 'diabetes_risk_v1';
  document.getElementById('reg-model-name').value = 'Clinical Diabetes Risk Predictor';
  document.getElementById('reg-model-type').value = 'CLASSIFICATION';
  document.getElementById('reg-target-col').value = 'has_diabetes';
  document.getElementById('reg-downstream').value = 'Hospital Emergency Alert System, Patient Portal API, EHR Telemetry';

  // Generate a sample CSV file on the fly and put into file input
  let csv = 'glucose_level,bmi_index,serum_insulin,patient_age,has_diabetes\n';
  for (let i = 0; i < 300; i++) {
    const glucose = (90 + Math.random() * 70).toFixed(1);
    const bmi = (22 + Math.random() * 12).toFixed(1);
    const insulin = (10 + Math.random() * 50).toFixed(1);
    const age = (25 + Math.random() * 45).toFixed(0);
    const hasDiabetes = glucose > 130 ? 1 : 0;
    csv += `${glucose},${bmi},${insulin},${age},${hasDiabetes}\n`;
  }

  const blob = new Blob([csv], { type: 'text/csv' });
  const file = new File([blob], 'diabetes_sample.csv', { type: 'text/csv' });
  const dataTransfer = new DataTransfer();
  dataTransfer.items.add(file);
  document.getElementById('reg-csv-file').files = dataTransfer.files;
}

async function handleRegisterModelSubmit(e) {
  e.preventDefault();
  const fileInput = document.getElementById('reg-csv-file');
  if (!fileInput.files || fileInput.files.length === 0) {
    alert('Please select a CSV file.');
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  formData.append('model_id', document.getElementById('reg-model-id').value);
  formData.append('name', document.getElementById('reg-model-name').value);
  formData.append('model_type', document.getElementById('reg-model-type').value);
  formData.append('target_column', document.getElementById('reg-target-col').value);
  formData.append('downstream_services_str', document.getElementById('reg-downstream').value);

  try {
    const res = await fetch(`${API_BASE}/api/models/upload-csv`, {
      method: 'POST',
      body: formData,
    });
    const result = await res.json();
    if (!res.ok) {
      alert('Failed: ' + (result.detail || 'Error registering model'));
      return;
    }

    document.getElementById('register-modal-backdrop').classList.remove('open');
    pollTelemetry();
  } catch (err) {
    console.error('Error uploading CSV model:', err);
    alert('Failed to register model.');
  }
}
