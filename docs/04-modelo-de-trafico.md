# 04. Modelo de tráfico

El modelo distingue entre flujos críticos y no críticos.

| Prioridad | Tráfico | Tratamiento |
|---:|---|---|
| P1 | Orden C2 | Siempre transmitir |
| P2 | Tracks | Siempre transmitir |
| P2 | Posición propia | Siempre transmitir |
| P3 | Metadatos ISR | Comprimir si hay degradación |
| P4 | Telemetría | Reducir frecuencia |
| P6 | Vídeo | Bloquear si la red está restringida |
| P7 | Logs | Retrasar |

La idea principal es que la red no debe tratar todos los flujos igual. Cuando aparece una restricción, el objetivo no es mantener todo, sino preservar lo que sostiene la decisión.
