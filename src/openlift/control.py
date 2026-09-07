from dataclasses import dataclass


@dataclass
class PIDConfig:
    kp: float
    ki: float
    kd: float
    output_min_hz: float
    output_max_hz: float
    ramp_limit_hz_s: float


class PIDController:
    def __init__(self, config: PIDConfig, initial_output_hz: float = 50.0):
        self.c = config
        self.integral = 0.0
        self.previous_error = 0.0
        self.output = initial_output_hz

    def step(self, setpoint: float, measurement: float, dt_s: float) -> float:
        error = measurement - setpoint
        derivative = (error - self.previous_error) / max(dt_s, 1e-9)
        candidate_integral = self.integral + error * dt_s
        raw = self.output + self.c.kp * error + self.c.ki * candidate_integral + self.c.kd * derivative
        limited = max(self.c.output_min_hz, min(self.c.output_max_hz, raw))
        if limited == raw or (limited == self.c.output_max_hz and error < 0) or (limited == self.c.output_min_hz and error > 0):
            self.integral = candidate_integral
        max_change = self.c.ramp_limit_hz_s * dt_s
        self.output += max(-max_change, min(max_change, limited - self.output))
        self.previous_error = error
        return self.output

