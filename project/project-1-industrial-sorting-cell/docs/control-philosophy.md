# Control Philosophy

## 1. Purpose

The controller operates an automated sorting cell that classifies boxes by height and routes them to separate discharge conveyors through a turntable.

## 2. Operating Modes

### Auto Mode

Automatic sequencing is permitted when:

`AutoMode AND StopNC AND EStopNC AND NOT Fault`

A Start command latches the machine Run request. Stop, emergency stop activation, or a latched fault removes the Run request.

### Manual Mode

Manual mode is intended for commissioning and maintenance. Individual actuator jog commands are provided through `GVL_HMI`. Manual outputs are only allowed when Auto mode is OFF, Stop and E Stop circuits are healthy, and no fault is latched.

Manual mode does not bypass mechanical limits or mutual exclusion between Load and Unload commands.

## 3. Sequence Philosophy

The automatic sequence uses one hot state bits:

1. `M_Idle`
2. `M_Loading`
3. `M_RotateToUnload`
4. `M_Discharge`
5. `M_ReturnHome`

Only one state should be active during normal operation.

## 4. Classification Philosophy

`M_HighSeen` and `M_LowSeen` remember classification sensor activation while the box travels toward the turntable.

At `iAtTurnEntry`:

1. If `M_HighSeen = TRUE`, the box is classified High.
2. Else if `M_LowSeen = TRUE`, the box is classified Low.
3. If neither is TRUE, an Invalid Classification fault is latched.

This method tolerates the common physical arrangement where a tall box may activate both low and high beams.

## 5. Routing Philosophy

High box: right discharge conveyor.

Low box: left discharge conveyor.

The routing convention can be reversed during commissioning without changing the state machine.

## 6. Fault Philosophy

Every major motion has timeout supervision. A timer expiration sets `M_Fault`, de energizes automatic outputs, resets the Run latch, and requires operator intervention.

Timeouts are diagnostic assumptions and must be tuned against measured Factory I/O cycle times.

## 7. Safety Boundary

`iEStopNC` is a simulation of a hardwired emergency stop input. This project is not a safety rated control system and does not implement a safety PLC, safety relay, PL, SIL, or validated risk reduction function.
