from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass
class PlantParameters:
    reservoir_pressure_bar: float
    productivity_index_m3d_bar: float
    wellhead_pressure_bar: float
    hydrostatic_bar: float
    tubing_loss_bar_per_flow2: float
    choke_loss_bar_per_flow2: float
    nominal_frequency_hz: float
    nominal_head_bar: float
    shutoff_head_bar: float
    best_efficiency_flow_m3d: float
    nominal_efficiency: float
    motor_efficiency: float
    thermal_time_constant_s: float
    ambient_temperature_c: float


@dataclass
class PlantState:
    flow_m3d: float = 400.0
    intake_pressure_bar: float = 80.0
    discharge_pressure_bar: float = 170.0
    motor_temperature_c: float = 65.0


@dataclass
class PlantOutput:
    flow_m3d: float
    intake_pressure_bar: float
    discharge_pressure_bar: float
    motor_current_a: float
    motor_temperature_c: float
    electrical_power_kw: float
    pump_efficiency: float


class ESPWellModel:
    """Low-order engineering model for control and fault-injection studies.

    The model is dimensionally simplified and explicitly not a design tool.
    It preserves the expected direction of the IPR, hydraulic loss, affinity,
    efficiency, electrical power and thermal relationships.
    """

    def __init__(self, parameters: PlantParameters):
        self.p = parameters
        self.state = PlantState()

    def _steady_flow(self, frequency_hz: float, reservoir_pressure_bar: float,
                     blockage_fraction: float) -> float:
        speed_ratio = max(frequency_hz, 0.0) / self.p.nominal_frequency_hz
        pump_head = self.p.nominal_head_bar * speed_ratio**2
        available = reservoir_pressure_bar + pump_head - self.p.hydrostatic_bar - self.p.wellhead_pressure_bar
        resistance = self.p.tubing_loss_bar_per_flow2 + self.p.choke_loss_bar_per_flow2
        resistance *= 1.0 + 4.0 * max(0.0, min(blockage_fraction, 0.95))
        return max(0.0, min(self.p.productivity_index_m3d_bar * 80.0, sqrt(max(available, 0.0) / resistance)))

    def step(self, frequency_hz: float, reservoir_pressure_bar: float,
             blockage_fraction: float, dt_s: float) -> PlantOutput:
        target_flow = self._steady_flow(frequency_hz, reservoir_pressure_bar, blockage_fraction)
        alpha = min(1.0, dt_s / 35.0)
        self.state.flow_m3d += alpha * (target_flow - self.state.flow_m3d)

        drawdown = self.state.flow_m3d / self.p.productivity_index_m3d_bar
        target_intake = max(1.0, reservoir_pressure_bar - drawdown)
        self.state.intake_pressure_bar += alpha * (target_intake - self.state.intake_pressure_bar)

        speed_ratio = frequency_hz / self.p.nominal_frequency_hz
        normalized_flow = self.state.flow_m3d / max(self.p.best_efficiency_flow_m3d * speed_ratio, 1.0)
        efficiency = max(0.25, self.p.nominal_efficiency * (1.0 - 0.55 * (normalized_flow - 1.0) ** 2))
        pump_head = max(0.0, self.p.shutoff_head_bar * speed_ratio**2 * (1.0 - 0.35 * normalized_flow**2))
        self.state.discharge_pressure_bar = self.state.intake_pressure_bar + pump_head

        hydraulic_kw = self.state.flow_m3d / 86400.0 * pump_head * 1e5 / 1000.0
        electrical_kw = hydraulic_kw / max(efficiency * self.p.motor_efficiency, 0.1)
        current_a = electrical_kw * 1000.0 / (sqrt(3.0) * 1000.0 * 0.82)
        target_temperature = self.p.ambient_temperature_c + 0.25 * electrical_kw
        thermal_alpha = min(1.0, dt_s / self.p.thermal_time_constant_s)
        self.state.motor_temperature_c += thermal_alpha * (target_temperature - self.state.motor_temperature_c)

        return PlantOutput(
            flow_m3d=self.state.flow_m3d,
            intake_pressure_bar=self.state.intake_pressure_bar,
            discharge_pressure_bar=self.state.discharge_pressure_bar,
            motor_current_a=current_a,
            motor_temperature_c=self.state.motor_temperature_c,
            electrical_power_kw=electrical_kw,
            pump_efficiency=efficiency,
        )
