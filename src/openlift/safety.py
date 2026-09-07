from dataclasses import dataclass

from .models import PlantOutput


@dataclass
class SafetyLimits:
    minimum_intake_pressure_bar: float
    maximum_current_a: float
    maximum_temperature_c: float
    output_min_hz: float
    output_max_hz: float
    ramp_limit_hz_s: float


@dataclass
class SafetyDecision:
    frequency_hz: float
    tripped: bool
    first_out: str


class SafetySupervisor:
    def __init__(self, limits: SafetyLimits, initial_frequency_hz: float = 50.0):
        self.limits = limits
        self.previous_frequency_hz = initial_frequency_hz
        self.first_out = "NONE"

    def apply(self, requested_hz: float, output: PlantOutput | None, dt_s: float) -> SafetyDecision:
        reasons = []
        if output is not None:
            if output.intake_pressure_bar < self.limits.minimum_intake_pressure_bar:
                reasons.append("LOW_INTAKE_PRESSURE")
            if output.motor_current_a > self.limits.maximum_current_a:
                reasons.append("HIGH_MOTOR_CURRENT")
            if output.motor_temperature_c > self.limits.maximum_temperature_c:
                reasons.append("HIGH_MOTOR_TEMPERATURE")
        if reasons:
            if self.first_out == "NONE":
                self.first_out = reasons[0]
            self.previous_frequency_hz = 0.0
            return SafetyDecision(0.0, True, self.first_out)

        bounded = max(self.limits.output_min_hz, min(self.limits.output_max_hz, requested_hz))
        max_change = self.limits.ramp_limit_hz_s * dt_s
        safe = self.previous_frequency_hz + max(-max_change, min(max_change, bounded - self.previous_frequency_hz))
        self.previous_frequency_hz = safe
        return SafetyDecision(safe, False, self.first_out)

