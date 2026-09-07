from openlift.models import PlantOutput
from openlift.safety import SafetyLimits, SafetySupervisor


def output(pressure=70, current=40, temperature=80):
    return PlantOutput(400, pressure, 160, current, temperature, 45, 0.7)


def test_hard_trip_overrides_command():
    supervisor = SafetySupervisor(SafetyLimits(32, 88, 125, 35, 60, 0.25))
    decision = supervisor.apply(55, output(pressure=20), 1)
    assert decision.tripped
    assert decision.frequency_hz == 0
    assert decision.first_out == "LOW_INTAKE_PRESSURE"


def test_supervisor_limits_command_rate():
    supervisor = SafetySupervisor(SafetyLimits(32, 88, 125, 35, 60, 0.25))
    decision = supervisor.apply(60, output(), 1)
    assert decision.frequency_hz == 50.25

