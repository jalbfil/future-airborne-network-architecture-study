# Brief para LinkedIn — Future Airborne Network Architecture Study

## Proyecto

`future-airborne-network-architecture-study`

Repositorio:

`https://github.com/jalbfil/future-airborne-network-architecture-study`

## Objetivo del post

Redactar una publicación profesional sobre un estudio conceptual y simulador ligero de arquitectura futura de red de misión aerotransportada.

El post debe transmitir que el proyecto no es solo una app ni solo un dashboard, sino un ejercicio de criterio técnico sobre comunicaciones, continuidad de misión, priorización de tráfico y arquitectura de sistemas de sistemas.

Idea central:

> En una red aérea futura, la pregunta no es solo si hay conectividad, sino qué información de misión puede seguir fluyendo cuando la red se degrada.

## Contexto dentro de la línea de proyectos

Este proyecto continúa una línea de portfolio centrada en comunicaciones críticas, redes tácticas, automatización, visualización y arquitectura:

1. `tactical-ospf-resilience-lab`  
   Diseño y validación manual de una topología IP resiliente con OSPF.

2. `tactical-netdevops-validator`  
   Automatización de la validación del estado de red mediante Python y reportes JSON/HTML.

3. `tactical-c2-network-dashboard`  
   Visualización tipo C2 del estado operativo de la red.

4. `tactical-radio-cognitive-gateway`  
   Clasificación sintética de estado de radioenlace y decisión UHF/SATCOM mediante ML local.

5. `future-airborne-network-architecture-study`  
   Estudio conceptual y simulador de arquitectura futura de red de misión aerotransportada.

Este quinto proyecto sube un nivel: pasa de validar enlaces concretos a razonar sobre continuidad de misión, arquitectura de servicios y priorización de flujos.

## Advertencia de alcance

No presentar como arquitectura real, sistema operacional ni referencia a ningún programa concreto.

Usar siempre lenguaje seguro:

- estudio conceptual;
- arquitectura genérica;
- laboratorio de portfolio;
- simulador ligero;
- red de misión aerotransportada;
- enfoque público y no sensible;
- sistema de sistemas como concepto general;
- continuidad de misión.

Evitar:

- nombres de programas reales;
- detalles clasificados;
- afirmar que es una arquitectura oficial;
- hablar de armas, efectos o capacidades operacionales;
- decir que simula un sistema real.

## Escenario conceptual

La arquitectura modela una red de misión con:

- `BASE`: puesto de mando o nodo terrestre.
- `GROUND-GW`: pasarela terrestre.
- `UAV-01`: nodo no tripulado de apoyo/relay.
- `RELAY-01`: nodo relay aerotransportado.
- `AIR-01`: plataforma aérea principal.
- `AIR-02`: plataforma aérea secundaria.
- `MISSION-EDGE`: nodo edge/nube de misión.
- `SATCOM-GW`: pasarela SATCOM.

La topología conceptual estudia enlaces UHF/LOS/relay/SATCOM y una pasarela federada limitada.

## Problema técnico

En muchas aproximaciones, una red se evalúa como `up/down`. Este proyecto intenta ir más allá:

> Una red puede estar parcialmente disponible y aun así no ser capaz de sostener todos los servicios de misión.

La pregunta pasa de ser:

```text
¿Hay conectividad?
```

a:

```text
¿Qué flujos críticos sobreviven bajo degradación?
```

## Estados de misión

El simulador clasifica la arquitectura en cuatro estados:

- `MISSION_READY`: todos los flujos principales pueden sostenerse.
- `MISSION_DEGRADED`: la misión continúa, pero con compresión/reducción.
- `MISSION_CONSTRAINED`: solo sobreviven flujos esenciales.
- `MISSION_CRITICAL`: no se sostiene el mínimo crítico.

## Clases de tráfico

El proyecto modela flujos de misión con prioridades:

- `C2_ORDER`: orden C2, siempre prioritaria.
- `TRACK_UPDATE`: actualización de tracks.
- `POSITION_UPDATE`: posición propia.
- `SENSOR_METADATA`: metadatos ISR, comprimibles.
- `TELEMETRY`: telemetría, reducible.
- `VIDEO_STREAM`: vídeo, bloqueable si la red está restringida.
- `BULK_LOGS`: logs/datos no críticos, diferibles.

Idea importante:

> No todos los datos tienen el mismo valor cuando el ancho de banda se degrada.

## Escenarios evaluados

El simulador incluye cinco escenarios:

1. `nominal`  
   Todos los enlaces principales están disponibles. Estado esperado: `MISSION_READY`.

2. `uhf_degraded`  
   El enlace UHF pierde capacidad y aumenta pérdida. Estado esperado: `MISSION_DEGRADED`.

3. `satcom_only`  
   Solo queda SATCOM. Se preservan C2, tracks y posición; se bloquea vídeo pesado. Estado esperado: `MISSION_CONSTRAINED`.

4. `relay_required`  
   El enlace directo no es viable y la arquitectura usa relay. Estado esperado: `MISSION_DEGRADED`.

5. `coalition_gateway_limited`  
   La pasarela federada limita el intercambio. Estado esperado: `MISSION_CONSTRAINED`.

## Parte práctica construida

El repo incluye:

- datos JSON de nodos, enlaces, servicios, tráfico y escenarios;
- simulador Python;
- evaluador de continuidad de misión;
- política de priorización de flujos;
- reportes JSON;
- API FastAPI;
- dashboard web;
- capturas de los cinco escenarios;
- tests con pytest;
- documentación técnica en castellano.

Arquitectura del proyecto:

```text
Datos JSON
   ↓
Simulador Python
   ↓
Evaluador de misión
   ↓
Política de tráfico
   ↓
Reportes JSON
   ↓
FastAPI + Dashboard
```

## Validación local

Validación realizada:

```text
pytest -q
6 passed, 1 warning
```

El dashboard arrancó correctamente con:

```text
python -m uvicorn app.main:app --reload
```

Se validaron los cinco escenarios por API con respuestas `200 OK`:

- `/api/evaluate/nominal`
- `/api/evaluate/uhf_degraded`
- `/api/evaluate/satcom_only`
- `/api/evaluate/relay_required`
- `/api/evaluate/coalition_gateway_limited`

También se generaron reportes JSON para los cinco escenarios.

## Imagen recomendada

Usar como imagen principal:

`assets/dashboard-satcom-only.png`

Motivo:

Es la captura que mejor transmite la idea de continuidad de misión bajo restricción: cuando solo queda SATCOM, no todo el tráfico puede sobrevivir; se priorizan flujos críticos y se bloquea tráfico pesado.

## Mensaje central del post

Mensaje principal:

> Una arquitectura de comunicaciones futura no debe diseñarse solo para transportar paquetes, sino para preservar los flujos de información que sostienen la decisión.

Otra formulación:

> En redes de misión, conectividad no equivale automáticamente a continuidad operativa. Hay que saber qué servicios sobreviven cuando la red se degrada.

## Tono deseado

Tono:

- profesional;
- técnico-aplicado;
- sobrio;
- reflexivo;
- orientado a arquitectura;
- conectado con CIS/Defensa;
- sin hype;
- sin afirmar capacidades reales.

## Estructura recomendada del post

### Apertura

Opción 1:

> Después de trabajar en resiliencia de red, validación NetDevOps, visualización tipo C2 y gateways radio/SATCOM, he querido subir un nivel: estudiar cómo podría evaluarse la continuidad de misión en una red aérea futura genérica.

Opción 2:

> En una red de misión no basta con preguntar si hay conectividad. La pregunta realmente útil es qué información crítica puede seguir fluyendo cuando la arquitectura se degrada.

### Desarrollo

Explicar brevemente:

- arquitectura aérea genérica;
- nodos tripulados/no tripulados/relay/SATCOM/edge;
- clases de tráfico;
- escenarios degradados;
- política de priorización;
- dashboard y reportes.

### Resultado

Mencionar:

- simulador Python;
- dashboard FastAPI;
- reportes JSON;
- cinco escenarios;
- tests pasando;
- documentación técnica en castellano.

### Aprendizaje

Idea clave:

> La continuidad de misión depende tanto de la arquitectura de red como de la priorización de datos.

### Cierre

Opción:

> Para mí, este proyecto representa un cambio de enfoque: de validar enlaces a razonar sobre servicios, flujos críticos y continuidad de misión.

## Hashtags recomendados

Usar 5-6 como máximo:

`#Telecomunicaciones #CIS #Defensa #NetworkArchitecture #SATCOM #Python`

Alternativa:

`#MissionNetworks #Telecomunicaciones #FastAPI #Python #Defensa #CIS`

## Cosas que no debe decir

No decir:

- arquitectura real;
- simulación de programa concreto;
- sistema operacional;
- C2 real;
- solución lista para producción;
- capacidades clasificadas.

Sí decir:

- estudio conceptual;
- simulador ligero;
- arquitectura genérica;
- red de misión;
- continuidad bajo degradación;
- priorización de flujos;
- enfoque seguro y público.

## Idea final que debe quedar

> El proyecto explora cómo pasar de una visión de red basada en conectividad a una visión de arquitectura basada en continuidad de misión: qué información crítica sobrevive, qué se degrada y qué debe esperar cuando los enlaces se restringen.
