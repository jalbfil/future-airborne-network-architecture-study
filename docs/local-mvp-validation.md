# Validación local del MVP

Este documento recoge la validación local del proyecto `Future Airborne Network Architecture Study`.

## 1. Ejecución del dashboard

Comando ejecutado:

```powershell
python -m uvicorn app.main:app --reload
```

Resultado observado:

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete.
```

El dashboard cargó correctamente en el navegador y sirvió los recursos estáticos:

```text
GET / HTTP/1.1 200 OK
GET /static/styles.css HTTP/1.1 200 OK
GET /static/dashboard.js HTTP/1.1 200 OK
```

## 2. Escenarios validados

Se validaron correctamente los cinco escenarios del simulador mediante la API:

```text
GET /api/evaluate/nominal HTTP/1.1 200 OK
GET /api/evaluate/uhf_degraded HTTP/1.1 200 OK
GET /api/evaluate/satcom_only HTTP/1.1 200 OK
GET /api/evaluate/relay_required HTTP/1.1 200 OK
GET /api/evaluate/coalition_gateway_limited HTTP/1.1 200 OK
```

Interpretación:

- `nominal`: arquitectura en estado nominal.
- `uhf_degraded`: continuidad con degradación controlada.
- `satcom_only`: modo restringido con flujos esenciales.
- `relay_required`: continuidad mediante nodo relay.
- `coalition_gateway_limited`: intercambio restringido por pasarela federada.

## 3. Tests

Comando ejecutado:

```powershell
pytest -q
```

Resultado observado:

```text
...... [100%]
6 passed, 1 warning in 0.34s
```

El warning observado corresponde a la pila de test `FastAPI/Starlette/httpx` y no afecta al funcionamiento del MVP.

## 4. Reportes generados

Comando ejecutado:

```powershell
python scripts/generate_reports.py
```

Reportes generados:

```text
reports/nominal-report.json
reports/uhf_degraded-report.json
reports/satcom_only-report.json
reports/relay_required-report.json
reports/coalition_gateway_limited-report.json
```

## 5. Capturas añadidas

Se añadieron capturas del dashboard para los cinco escenarios:

```text
assets/dashboard-nominal.png
assets/dashboard-uhf-degraded.png
assets/dashboard-satcom-only.png
assets/dashboard-relay-required.png
assets/dashboard-coalition-gateway-limited.png
```

## 6. Resultado

El MVP queda validado como estudio técnico y demostrador ligero de continuidad de misión:

```text
datos JSON → simulador Python → evaluación de misión → dashboard FastAPI → reportes JSON
```

El resultado no representa una arquitectura real ni un sistema operacional. Es un laboratorio conceptual y seguro para estudiar cómo una red de misión podría priorizar flujos críticos bajo degradación.
