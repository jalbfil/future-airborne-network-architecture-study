from future_airborne_network_study.evaluator import evaluate_scenario
from future_airborne_network_study.models import MissionState


def test_nominal_ready():
    result = evaluate_scenario("nominal")
    assert result.mission_state == MissionState.MISSION_READY
    assert "VIDEO_STREAM" in result.allowed_flows


def test_satcom_only_constrained():
    result = evaluate_scenario("satcom_only")
    assert result.mission_state in {MissionState.MISSION_CONSTRAINED, MissionState.MISSION_DEGRADED}
    assert "VIDEO_STREAM" in result.dropped_flows


def test_relay_required_not_critical():
    result = evaluate_scenario("relay_required")
    assert result.mission_state != MissionState.MISSION_CRITICAL
