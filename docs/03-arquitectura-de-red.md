# 03. Arquitectura de red

La arquitectura se organiza en capas:

```text
Capa física / enlace
Capa IP / transporte
Capa de servicios de misión
Capa de priorización de datos
Capa edge / nube de misión
Capa de visualización C2
Capa de interoperabilidad
```

## Idea principal

Una red de misión futura no debe diseñarse solo pensando en enlaces disponibles, sino en servicios que deben mantenerse bajo degradación.

La capa de priorización decide qué flujos sobreviven. La capa edge reduce presión sobre los enlaces. La visualización muestra la continuidad de misión, no solo si un enlace está activo o caído.
