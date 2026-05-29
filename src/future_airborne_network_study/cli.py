from __future__ import annotations

import argparse
import json

from future_airborne_network_study.evaluator import evaluate_scenario
from future_airborne_network_study.reports import generate_all_reports


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluador de arquitectura futura de red aerotransportada.")
    parser.add_argument("scenario", nargs="?", default="nominal", help="Escenario a evaluar.")
    parser.add_argument("--generate-reports", action="store_true", help="Generar reportes JSON para todos los escenarios.")
    args = parser.parse_args()

    if args.generate_reports:
        paths = generate_all_reports()
        for path in paths:
            print(path)
        return

    result = evaluate_scenario(args.scenario)
    print(json.dumps(result.model_dump(mode="json"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
