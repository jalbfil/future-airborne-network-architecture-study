from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


class MissionState(str, Enum):
    MISSION_READY = "MISSION_READY"
    MISSION_DEGRADED = "MISSION_DEGRADED"
    MISSION_CONSTRAINED = "MISSION_CONSTRAINED"
    MISSION_CRITICAL = "MISSION_CRITICAL"


class FlowAction(str, Enum):
    ALLOW = "ALLOW"
    COMPRESS = "COMPRESS"
    REDUCE = "REDUCE"
    DELAY = "DELAY"
    DROP = "DROP"


class TrafficClass(BaseModel):
    id: str
    label: str
    priority: int
    required_kbps: float
    critical: bool
    policy: str
    compression_ratio: float | None = None
    reduction_ratio: float | None = None


class FlowDecision(BaseModel):
    traffic_id: str
    label: str
    priority: int
    requested_kbps: float
    effective_kbps: float
    action: FlowAction
    reason: str


class MissionEvaluation(BaseModel):
    scenario: str
    label: str
    mission_state: MissionState
    available_bandwidth_kbps: float = Field(description="Capacidad útil aproximada del cuello de botella")
    bottleneck_latency_ms: float
    estimated_loss_pct: float
    allowed_flows: list[str]
    compressed_flows: list[str]
    reduced_flows: list[str]
    delayed_flows: list[str]
    dropped_flows: list[str]
    decisions: list[FlowDecision]
    recommendation: str
