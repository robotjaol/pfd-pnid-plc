# Data Dictionary

The authoritative tag import is [`../hmi/tags.csv`](../hmi/tags.csv). All timestamps use elapsed simulation seconds in the baseline. Engineering units are encoded in column names in generated CSV files.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `time_s` | float | s | Elapsed experiment time |
| `reservoir_pressure_bar` | float | bar | Scenario reservoir pressure |
| `blockage_fraction` | float | 1 | Injected obstruction severity |
| `frequency_hz` | float | Hz | Safety-approved VFD command |
| `flow_m3d` | float | m3/d | Simulated liquid rate |
| `intake_pressure_bar` | float | bar | Simulated pump intake pressure |
| `discharge_pressure_bar` | float | bar | Simulated pump discharge pressure |
| `motor_current_a` | float | A | Simplified motor line current |
| `motor_temperature_c` | float | degC | Lumped motor temperature state |
| `electrical_power_kw` | float | kW | Estimated input power |
| `pump_efficiency` | float | 1 | Simplified pump efficiency |
| `tripped` | bool | 1 | Safety-trip state |
| `first_out` | string | 1 | First retained trip cause |

