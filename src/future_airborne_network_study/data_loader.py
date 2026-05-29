from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_nodes() -> dict[str, Any]:
    return load_json(DATA_DIR / "architecture_nodes.json")


def load_traffic_classes() -> list[dict[str, Any]]:
    return load_json(DATA_DIR / "traffic_classes.json")["traffic_classes"]


def load_mission_services() -> list[dict[str, Any]]:
    return load_json(DATA_DIR / "mission_services.json")["mission_services"]


def load_scenarios() -> list[dict[str, Any]]:
    return load_json(DATA_DIR / "scenarios.json")["scenarios"]


def get_scenario(scenario_id: str) -> dict[str, Any]:
    for scenario in load_scenarios():
        if scenario["id"] == scenario_id:
            return scenario
    raise ValueError(f"Escenario no encontrado: {scenario_id}")
