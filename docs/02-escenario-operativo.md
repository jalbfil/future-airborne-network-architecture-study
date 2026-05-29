# 02. Escenario operativo genérico

El escenario modela una red aérea de misión compuesta por nodos terrestres, plataformas aéreas, nodos relay, un enlace SATCOM de respaldo y una capa de servicios edge.

La topología base es:

```text
BASE → GROUND-GW → UAV-01 → AIR-01 → AIR-02
                  \\       /
                   RELAY-01
```

Además, existe una capacidad SATCOM de respaldo y una conexión hacia servicios de misión federados o edge.

## Hipótesis

El modelo no busca simular un sistema real. Usa hipótesis simplificadas para razonar sobre continuidad de misión:

- los enlaces tienen capacidad, latencia y pérdida;
- los flujos tienen prioridad y ancho de banda requerido;
- los flujos críticos se preservan antes que los no críticos;
- en degradación se comprime, reduce, retrasa o bloquea tráfico.
