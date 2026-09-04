# ArgusML Workspace Instructions & State
- Workspace: c:\DS_CP
- Project: ArgusML (Universal AI Observability & Root-Cause Platform)
- Architecture: 5 Core Data Structures (EventQueue, MetricSlidingWindow, ModelRegistry, AlertMaxHeap, DependencyGraph).
- Universal: Works for ANY model, classification or regression.
- Running: Backend runs via `uvicorn backend.app.main:app --port 8000`, Dashboard on `http://127.0.0.1:8000`.
- All tests passing (9/9).
- Next potential phase: Phase 7 (1-Click Auto-Retraining Trigger).
