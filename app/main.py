from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from future_airborne_network_study.data_loader import load_nodes, load_scenarios
from future_airborne_network_study.evaluator import evaluate_scenario
from future_airborne_network_study.reports import generate_all_reports


ROOT_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT_DIR / "app" / "static"
DEFAULT_SCENARIO = "nominal"
_runtime_scenario = DEFAULT_SCENARIO

app = FastAPI(
    title="Future Airborne Network Architecture Study",
    description="Estudio conceptual y simulador ligero de red de misión aerotransportada.",
    version="0.1.1",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/nodes")
def nodes() -> dict:
    return load_nodes()


@app.get("/api/scenarios")
def scenarios() -> dict:
    return {"scenarios": load_scenarios()}


@app.get("/api/evaluate/{scenario_id}")
def evaluate(scenario_id: str) -> dict:
    try:
        return evaluate_scenario(scenario_id).model_dump(mode="json")
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/reports")
def reports() -> dict:
    paths = generate_all_reports()
    return {"reports": [str(path.relative_to(ROOT_DIR)) for path in paths]}


@app.post("/api/playback")
def playback() -> dict:
    sequence = ["nominal", "uhf_degraded", "satcom_only", "relay_required", "coalition_gateway_limited"]
    return {"sequence": [evaluate_scenario(item).model_dump(mode="json") for item in sequence]}


# Compatibility endpoints for stale browser cache or older dashboard scripts.
@app.get("/api/status")
def status_compat() -> dict:
    return evaluate_scenario(_runtime_scenario).model_dump(mode="json")


@app.post("/api/scenario/{scenario_id}")
def scenario_compat(scenario_id: str) -> dict:
    global _runtime_scenario
    _runtime_scenario = scenario_id
    return evaluate(scenario_id)


@app.post("/api/tick")
def tick_compat() -> dict:
    return evaluate_scenario(_runtime_scenario).model_dump(mode="json")
