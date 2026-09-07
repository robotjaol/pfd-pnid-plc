from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import yaml

from .control import PIDConfig, PIDController
from .models import ESPWellModel, PlantParameters
from .safety import SafetyLimits, SafetySupervisor


def load_config(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def run(config: dict, mode: str = "pid") -> list[dict]:
    sim = config["simulation"]
    plant_config = config["plant"]
    control_config = config["control"]
    safety_config = config["safety"]
    scenario = config["scenario"]
    dt_s = float(sim["dt_s"])
    rng = np.random.default_rng(int(sim["seed"]))
    plant = ESPWellModel(PlantParameters(**plant_config))
    pid = PIDController(PIDConfig(
        kp=control_config["kp"],
        ki=control_config["ki"],
        kd=control_config["kd"],
        output_min_hz=control_config["output_min_hz"],
        output_max_hz=control_config["output_max_hz"],
        ramp_limit_hz_s=control_config["ramp_limit_hz_s"],
    ), plant_config["nominal_frequency_hz"])
    supervisor = SafetySupervisor(SafetyLimits(
        minimum_intake_pressure_bar=safety_config["minimum_intake_pressure_bar"],
        maximum_current_a=safety_config["maximum_current_a"],
        maximum_temperature_c=safety_config["maximum_temperature_c"],
        output_min_hz=control_config["output_min_hz"],
        output_max_hz=control_config["output_max_hz"],
        ramp_limit_hz_s=control_config["ramp_limit_hz_s"],
    ), plant_config["nominal_frequency_hz"])

    rows = []
    previous = None
    frequency = plant_config["nominal_frequency_hz"]
    steps = int(float(sim["duration_s"]) / dt_s)
    for index in range(steps + 1):
        time_s = index * dt_s
        reservoir = plant_config["reservoir_pressure_bar"]
        if time_s >= scenario["reservoir_decline_start_s"]:
            reservoir -= scenario["reservoir_decline_bar"]
        blockage = 0.0
        if time_s >= scenario["blockage_start_s"]:
            progress = (time_s - scenario["blockage_start_s"]) / max(float(sim["duration_s"]) - scenario["blockage_start_s"], 1.0)
            blockage = min(scenario["final_blockage_fraction"], scenario["final_blockage_fraction"] * progress)

        measured_pressure = (previous.intake_pressure_bar if previous else 80.0) + rng.normal(0.0, 0.15)
        requested = plant_config["nominal_frequency_hz"] if mode == "fixed" else pid.step(
            control_config["pressure_setpoint_bar"], measured_pressure, dt_s
        )
        decision = supervisor.apply(requested, previous, dt_s)
        frequency = decision.frequency_hz
        previous = plant.step(frequency, reservoir, blockage, dt_s)
        rows.append({
            "time_s": round(time_s, 3),
            "mode": mode,
            "reservoir_pressure_bar": round(reservoir, 4),
            "blockage_fraction": round(blockage, 6),
            "frequency_hz": round(frequency, 4),
            "flow_m3d": round(previous.flow_m3d, 4),
            "intake_pressure_bar": round(previous.intake_pressure_bar, 4),
            "discharge_pressure_bar": round(previous.discharge_pressure_bar, 4),
            "motor_current_a": round(previous.motor_current_a, 4),
            "motor_temperature_c": round(previous.motor_temperature_c, 4),
            "electrical_power_kw": round(previous.electrical_power_kw, 4),
            "pump_efficiency": round(previous.pump_efficiency, 6),
            "tripped": decision.tripped,
            "first_out": decision.first_out,
        })
        if decision.tripped:
            break
    return rows


def write_csv(rows: list[dict], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def benchmark(config: dict) -> dict:
    results = {}
    setpoint = config["control"]["pressure_setpoint_bar"]
    dt_s = config["simulation"]["dt_s"]
    for mode in ("fixed", "pid"):
        rows = run(config, mode)
        pressure = np.asarray([row["intake_pressure_bar"] for row in rows])
        power = np.asarray([row["electrical_power_kw"] for row in rows])
        flow = np.asarray([row["flow_m3d"] for row in rows])
        rmse = float(np.sqrt(np.mean((pressure - setpoint) ** 2)))
        energy_kwh = float(np.sum(power) * dt_s / 3600.0)
        volume_m3 = float(np.sum(flow) * dt_s / 86400.0)
        results[mode] = {
            "samples": len(rows),
            "pressure_rmse_bar": round(rmse, 5),
            "energy_kwh": round(energy_kwh, 5),
            "produced_volume_m3": round(volume_m3, 5),
            "energy_intensity_kwh_m3": round(energy_kwh / max(volume_m3, 1e-9), 5),
            "tripped": bool(rows[-1]["tripped"]),
            "first_out": rows[-1]["first_out"],
        }
    results["metadata"] = {
        "status": "simulation-only",
        "interpretation": "Reference-model outputs; not validated field-performance claims.",
    }
    return results


def write_json(data: dict, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8") as stream:
        json.dump(data, stream, indent=2)
        stream.write("\n")
