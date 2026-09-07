# System Requirements Specification

| ID | Requirement | Priority | Verification |
|---|---|---|---|
| SYS-001 | The reference system shall represent one onshore ESP-lifted well from reservoir inflow to surface choke. | Must | Inspection and model test |
| SYS-002 | The simulator shall expose reservoir pressure, flow, intake pressure, discharge pressure, motor current, motor temperature, power and frequency. | Must | Integration test |
| SYS-003 | The system shall support fixed-speed and closed-loop PID modes under an identical scenario configuration. | Must | Benchmark run |
| SYS-004 | The safety supervisor shall limit frequency to 35 through 60 Hz and rate of change to 0.25 Hz/s in the reference configuration. | Must | Unit test |
| SYS-005 | Low intake pressure, high motor current, or high motor temperature shall override any advisory command; numerical values are configuration-controlled. | Must | Fault-injection test |
| SYS-006 | The first detected trip cause shall be retained as the first-out record. | Must | Unit test |
| SYS-007 | Scenario output shall be machine-readable CSV with a deterministic seed. | Must | Reproduction test |
| SYS-008 | Benchmark output shall identify simulation-only status and shall not present field claims. | Must | Inspection |
| SYS-009 | PLC, MCU, HMI, MATLAB and Python work packages shall use the shared tag register. | Should | Interface audit |
| SYS-010 | Public datasets shall be obtained through source links and shall not be redistributed without permission. | Must | Repository audit |
| SYS-011 | The proposal shall state research questions, method, metrics, acceptance criteria and limitations. | Must | Document review |
| SYS-012 | The repository shall distinguish model-in-the-loop, software-in-the-loop, controller-in-the-loop and true HIL evidence. | Must | Document review |
| SYS-013 | The architecture shall permit a future physical PLC or MCU without replacing the plant interface. | Should | Design review |
| SYS-014 | Critical requirements shall have stable identifiers and a planned verification method. | Must | Traceability audit |
| SYS-015 | Analytics shall operate in advisory mode unless a validated safety path authorizes the command. | Must | Architecture and integration test |

## Assumptions

The initial model is single-well, lumped-parameter, single-fluid-equivalent, and intended for control studies. It is not a multiphase flow assurance model. Equipment curves and protection settings are illustrative. The controller interval is one second and the first release does not claim real-time operating-system behavior.
