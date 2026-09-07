# Validation Protocol

## Evidence classes

1. Unit tests verify local mathematical and safety properties.
2. Integration tests verify scenario, controller, safety and file interfaces.
3. Regression tests compare versioned reference metrics within declared tolerances.
4. Fault campaigns vary onset, severity, measurement failure and communication behavior.
5. Virtual FAT maps requirements to procedures, expected results and retained evidence.

## Acceptance criteria

| ID | Criterion | Status in v0.1 |
|---|---|---|
| VAL-001 | All critical safety tests pass | Automated |
| VAL-002 | No optimizer or controller command bypasses a hard trip | Automated |
| VAL-003 | All requirement identifiers have a verification method | Inspection |
| VAL-004 | Reference experiment reproduces with a fixed seed | Automated |
| VAL-005 | Pressure tracking error and energy intensity are reported for both baselines | Automated |
| VAL-006 | Group-based splits are used for external time-series datasets | Planned |
| VAL-007 | MPC P99 solve time is below its control interval with zero deadline misses | Planned |
| VAL-008 | PCB ERC and DRC contain no critical unresolved errors | Planned |
| VAL-009 | CAD interference analysis has no unresolved collisions | Planned |
| VAL-010 | Communication loss causes deterministic degraded operation | Planned |

## Statistical protocol

Future analytics use scenario- or equipment-group splits, not random row splits. Report macro-F1, PR-AUC, false alarms per operating day, expected calibration error, lead-time distribution, and performance against fault severity. Ablations compare raw sensors, physics residuals, and combined inputs.

## Claim control

Acceptance thresholds are design targets until corresponding evidence exists. Vendor case studies motivate the research but are not used as expected project performance.

