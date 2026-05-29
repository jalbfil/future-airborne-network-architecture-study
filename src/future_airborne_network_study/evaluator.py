from __future__ import annotations

from future_airborne_network_study.data_loader import get_scenario, load_traffic_classes
from future_airborne_network_study.models import FlowAction, FlowDecision, MissionEvaluation, MissionState, TrafficClass


def _usable_links(scenario: dict) -> list[dict]:
    return [link for link in scenario["links"] if link.get("available", True) and not link.get("standby", False)]


def _available_bandwidth(scenario: dict) -> float:
    links = _usable_links(scenario)
    if not links:
        return 0.0
    return min(link["bandwidth_kbps"] for link in links)


def _bottleneck_latency(scenario: dict) -> float:
    links = _usable_links(scenario)
    if not links:
        return 0.0
    return max(link["latency_ms"] for link in links)


def _estimated_loss(scenario: dict) -> float:
    links = _usable_links(scenario)
    if not links:
        return 100.0
    return max(link["loss_pct"] for link in links)


def _critical_minimum(traffic: list[TrafficClass]) -> float:
    return sum(item.required_kbps for item in traffic if item.critical)


def _decision(
    item: TrafficClass,
    effective_kbps: float,
    action: FlowAction,
    reason: str,
) -> FlowDecision:
    return FlowDecision(
        traffic_id=item.id,
        label=item.label,
        priority=item.priority,
        requested_kbps=item.required_kbps,
        effective_kbps=effective_kbps,
        action=action,
        reason=reason,
    )


def _make_decision(item: TrafficClass, remaining: float, constrained: bool, degraded: bool) -> tuple[FlowDecision, float]:
    requested = item.required_kbps

    if item.critical:
        if remaining >= requested:
            return _decision(item, requested, FlowAction.ALLOW, "Flujo crítico permitido."), remaining - requested
        return _decision(item, 0, FlowAction.DROP, "No hay capacidad suficiente ni para el mínimo crítico."), remaining

    if constrained:
        if item.policy == "delay_if_constrained":
            return _decision(item, 0, FlowAction.DELAY, "Tráfico no crítico diferido en modo restringido."), remaining
        return _decision(item, 0, FlowAction.DROP, "Tráfico no crítico bloqueado para preservar flujos esenciales."), remaining

    if degraded and item.policy == "compress_if_degraded":
        effective = requested * (item.compression_ratio or 0.5)
        if remaining >= effective:
            return _decision(item, effective, FlowAction.COMPRESS, "Flujo comprimido por degradación de red."), remaining - effective

    if degraded and item.policy == "reduce_if_degraded":
        effective = requested * (item.reduction_ratio or 0.5)
        if remaining >= effective:
            return _decision(item, effective, FlowAction.REDUCE, "Flujo reducido en frecuencia por degradación de red."), remaining - effective

    if remaining >= requested:
        return _decision(item, requested, FlowAction.ALLOW, "Capacidad suficiente para el flujo."), remaining - requested

    if item.policy == "delay_if_constrained":
        return _decision(item, 0, FlowAction.DELAY, "No cabe en la ventana actual; queda diferido."), remaining

    return _decision(item, 0, FlowAction.DROP, "Capacidad insuficiente para flujo no crítico."), remaining


def evaluate_scenario(scenario_id: str) -> MissionEvaluation:
    scenario = get_scenario(scenario_id)
    traffic = [TrafficClass(**item) for item in load_traffic_classes()]
    traffic = sorted(traffic, key=lambda item: item.priority)

    available = _available_bandwidth(scenario)
    latency = _bottleneck_latency(scenario)
    loss = _estimated_loss(scenario)
    critical_minimum = _critical_minimum(traffic)

    if available < critical_minimum:
        initial_state = MissionState.MISSION_CRITICAL
        constrained = True
        degraded = True
    elif available < 350:
        initial_state = MissionState.MISSION_CONSTRAINED
        constrained = True
        degraded = True
    elif available < 900 or loss >= 6 or latency >= 180:
        initial_state = MissionState.MISSION_DEGRADED
        constrained = False
        degraded = True
    else:
        initial_state = MissionState.MISSION_READY
        constrained = False
        degraded = False

    remaining = available
    decisions: list[FlowDecision] = []
    for item in traffic:
        decision, remaining = _make_decision(item, remaining, constrained=constrained, degraded=degraded)
        decisions.append(decision)

    dropped_critical = any(
        decision.action == FlowAction.DROP and next(t for t in traffic if t.id == decision.traffic_id).critical
        for decision in decisions
    )
    if dropped_critical:
        mission_state = MissionState.MISSION_CRITICAL
    elif any(decision.action in {FlowAction.DROP, FlowAction.DELAY} for decision in decisions):
        mission_state = MissionState.MISSION_CONSTRAINED if constrained else MissionState.MISSION_DEGRADED
    elif any(decision.action in {FlowAction.COMPRESS, FlowAction.REDUCE} for decision in decisions):
        mission_state = MissionState.MISSION_DEGRADED
    else:
        mission_state = initial_state

    return MissionEvaluation(
        scenario=scenario_id,
        label=scenario["label"],
        mission_state=mission_state,
        available_bandwidth_kbps=available,
        bottleneck_latency_ms=latency,
        estimated_loss_pct=loss,
        allowed_flows=[d.traffic_id for d in decisions if d.action == FlowAction.ALLOW],
        compressed_flows=[d.traffic_id for d in decisions if d.action == FlowAction.COMPRESS],
        reduced_flows=[d.traffic_id for d in decisions if d.action == FlowAction.REDUCE],
        delayed_flows=[d.traffic_id for d in decisions if d.action == FlowAction.DELAY],
        dropped_flows=[d.traffic_id for d in decisions if d.action == FlowAction.DROP],
        decisions=decisions,
        recommendation=_recommendation(mission_state),
    )


def _recommendation(state: MissionState) -> str:
    if state == MissionState.MISSION_READY:
        return "La arquitectura soporta los flujos principales. Mantener supervisión y redundancia activa."
    if state == MissionState.MISSION_DEGRADED:
        return "La misión continúa con degradación. Mantener C2/tracks, comprimir metadatos y reducir telemetría."
    if state == MissionState.MISSION_CONSTRAINED:
        return "Modo restringido. Preservar C2, posición y tracks. Bloquear vídeo y diferir datos no críticos."
    return "Estado crítico. El mínimo de misión no está garantizado. Requiere restaurar enlace, relay o capacidad adicional."
