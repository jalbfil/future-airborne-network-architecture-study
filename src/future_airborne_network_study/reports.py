from __future__ import annotations

import json
from pathlib import Path

from future_airborne_network_study.data_loader import load_scenarios
from future_airborne_network_study.evaluator import evaluate_scenario


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"


def generate_all_reports() -> list[Path]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    for scenario in load_scenarios():
        evaluation = evaluate_scenario(scenario["id"])
        path = REPORTS_DIR / f"{scenario['id']}-report.json"
        path.write_text(json.dumps(evaluation.model_dump(mode="json"), indent=2, ensure_ascii=False), encoding="utf-8")
        paths.append(path)

    return paths
