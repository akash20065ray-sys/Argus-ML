"""
ArgusML FastAPI Application Server: Universal AI Observability Platform.
Supports monitoring, drift analysis, DAG topologies, and RCA for ANY ML Model.
"""

from contextlib import asynccontextmanager
import io
import os
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
from pydantic import BaseModel

from .core.orchestrator import ArgusSystem

# Instantiate the singleton universal ArgusSystem
system = ArgusSystem(window_size=400)


@asynccontextmanager
async def lifespan(app: FastAPI):
    system.start()
    yield
    system.stop()


app = FastAPI(
    title="ArgusML Universal AI Observability Platform",
    version="2.0.0",
    description="Universal Real-time ML Model Watchdog & Graph-Powered Root Cause Diagnostic Engine",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SelectModelRequest(BaseModel):
    model_id: str


class FeatureDriftRequest(BaseModel):
    feature_name: Optional[str] = None
    multiplier: float = 3.5


class IngestEventRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_id: str
    features: Dict[str, float]
    prediction: Any
    confidence: Optional[float] = 0.95
    ground_truth: Optional[Any] = None
    latency_ms: Optional[float] = 45.0


class RegisterModelJsonRequest(BaseModel):
    model_id: str
    name: str
    model_type: str = "CLASSIFICATION"  # 'CLASSIFICATION' or 'REGRESSION'
    data: Dict[str, List[float]]  # Feature name -> array of numbers
    target_name: str
    target_values: List[float]
    downstream_services: Optional[List[str]] = None
    upstream_pipelines: Optional[List[str]] = None
    sla_min_accuracy: Optional[float] = 0.85
    sla_max_p99_latency_ms: Optional[float] = 200.0


@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "platform": "ArgusML Universal",
        "active_model": system.active_model_id,
        "version": "2.0.0",
    }


@app.get("/api/dashboard")
def get_dashboard():
    """Returns real-time aggregated metrics, drift telemetry, graph, and priority alerts."""
    return system.get_dashboard_summary()


@app.get("/api/models")
def list_models():
    """Returns all models currently registered in the HashMap store."""
    return {
        "active_model_id": system.active_model_id,
        "models": system.registry.list_models(),
    }


@app.post("/api/models/select")
def select_model(req: SelectModelRequest):
    """Switches the actively monitored model and rebuilds DAG topology."""
    success = system.switch_active_model(req.model_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Model '{req.model_id}' not found.")
    return {
        "status": "SUCCESS",
        "active_model_id": req.model_id,
        "message": f"Switched active telemetry to {req.model_id}",
    }


@app.post("/api/models/load-samples")
def load_sample_models():
    """Optional endpoint to load showcase demo models if requested."""
    system.load_sample_models()
    return {
        "status": "SUCCESS",
        "message": "Sample models loaded successfully",
        "active_model_id": system.active_model_id,
    }



@app.post("/api/models/register")
def register_custom_model_json(req: RegisterModelJsonRequest):
    """Registers ANY new ML model with custom JSON baseline dataset."""
    meta = system.register_custom_model(
        model_id=req.model_id,
        name=req.name,
        model_type=req.model_type,
        data_dict=req.data,
        target_name=req.target_name,
        target_values=req.target_values,
        downstream_services=req.downstream_services,
        upstream_pipelines=req.upstream_pipelines,
        sla_min_accuracy=req.sla_min_accuracy or 0.85,
        sla_max_p99_latency_ms=req.sla_max_p99_latency_ms or 200.0,
    )
    return {"status": "SUCCESS", "model": meta.to_dict()}


@app.post("/api/models/upload-csv")
async def register_model_csv(
    file: UploadFile = File(...),
    model_id: str = Form(...),
    name: str = Form(...),
    target_column: str = Form(...),
    model_type: str = Form("CLASSIFICATION"),
    downstream_services_str: str = Form("API Gateway, Dashboard"),
    upstream_pipelines_str: str = Form("Primary ETL Pipeline"),
):
    """
    Accepts ANY user CSV dataset, computes baselines, trains reference model,
    builds dynamic DAG topology, and initiates real-time monitoring!
    """
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        if target_column not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"Target column '{target_column}' not found in CSV. Available columns: {list(df.columns)}",
            )

        # Separate features and target
        features_df = df.drop(columns=[target_column])
        numeric_cols = features_df.select_dtypes(include=["number"]).columns.tolist()

        if len(numeric_cols) < 1:
            raise HTTPException(status_code=400, detail="CSV must contain at least 1 numerical feature column.")

        data_dict = {col: df[col].astype(float).tolist() for col in numeric_cols}
        target_vals = df[target_column].astype(float).tolist()

        downstream = [s.strip() for s in downstream_services_str.split(",") if s.strip()]
        upstream = [s.strip() for s in upstream_pipelines_str.split(",") if s.strip()]

        meta = system.register_custom_model(
            model_id=model_id,
            name=name,
            model_type=model_type.upper(),
            data_dict=data_dict,
            target_name=target_column,
            target_values=target_vals,
            downstream_services=downstream,
            upstream_pipelines=upstream,
        )

        return {
            "status": "SUCCESS",
            "model_id": model_id,
            "features_inferred": numeric_cols,
            "rows_processed": len(df),
            "model": meta.to_dict(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process CSV: {str(e)}")


@app.post("/api/simulate/drift-feature")
def inject_feature_drift(req: FeatureDriftRequest):
    """Injects covariate shift into ANY chosen feature of the active model."""
    system.simulator.set_feature_drift(req.feature_name, req.multiplier)
    return {
        "status": "SUCCESS",
        "drift_feature": req.feature_name,
        "multiplier": req.multiplier,
    }


@app.post("/api/simulate/latency-spike")
def toggle_latency_spike(spike: bool = True):
    system.simulator.set_latency_spike(spike)
    return {"status": "SUCCESS", "latency_spiked": spike}


@app.post("/api/simulate/reset")
def reset_simulation():
    """Clears sliding window, alerts, and resets feature drift to healthy baseline."""
    system.reset_metrics()
    return {"status": "SUCCESS", "message": "Telemetry and drift reset to baseline"}


@app.post("/api/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: str):
    success = system.alert_heap.resolve(alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"success": True, "alert_id": alert_id}


@app.post("/api/models/{model_id}/retrain")
def retrain_model_endpoint(model_id: str):
    """
    Phase 7: 1-Click Automated Model Retraining Trigger.
    Retrains the active model on recent distribution data, updates baselines, and resolves alerts.
    """
    try:
        result = system.retrain_active_model()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Retraining failed: {str(e)}")


@app.get("/api/alerts/{alert_id}/report")
def get_incident_report(alert_id: str):
    """
    Phase 8: Downloadable Markdown Incident Post-Mortem Report.
    """
    report_md = system.generate_incident_report(alert_id)
    return {"alert_id": alert_id, "report_markdown": report_md}



# Serve static frontend files
frontend_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
)
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    def serve_index():
        index_file = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "ArgusML API is running. Frontend directory found."}
