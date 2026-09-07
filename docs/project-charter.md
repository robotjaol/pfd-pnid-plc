# Project Charter

## Problem

Changing well conditions, sparse measurements, equipment degradation, and fragmented automation workflows make it difficult to evaluate ESP control, surveillance, and safety decisions before deployment.

## Purpose

Design and validate an open, software-first digital engineering reference for one onshore ESP well. The platform must connect process physics, virtual instrumentation, deterministic control, analytics, operator interaction, and traceable verification on a standard laptop.

## Objectives

1. Establish a transparent model from reservoir inflow to surface production.
2. Compare fixed-frequency, PID, and later constrained MPC strategies under identical scenarios.
3. Evaluate sensor and communication faults without risking physical equipment.
4. Demonstrate that analytics cannot override deterministic trips.
5. Maintain traceability across process, mechanical, electrical, PCB, embedded, PLC, HMI, MATLAB, Python, data, and validation work packages.

## Stakeholders

| Role | Interest |
|---|---|
| Researcher | Reproducible method and defensible claims |
| Control engineer | Stable control and explicit constraints |
| Production engineer | Operating envelope and production response |
| Electrical engineer | Loads, protection, interfaces and grounding |
| Instrument engineer | Tag model, ranges, alarms and diagnostics |
| Operator | Clear modes, alarms and first-out information |
| Reviewer | Traceability, evidence and limitations |

## Success condition

The project succeeds when the reference experiment can be reproduced from a clean environment, all critical interlock tests pass, assumptions remain explicit, and every reported comparison is linked to its configuration and evidence.

