# CODESYS Ladder Networks

This file is the implementation specification for `PLC_PRG`.

Notation:

`--| |--` normally open contact

`--|/|--` normally closed contact

`--( )--` standard coil

`--(S)--` Set coil

`--(R)--` Reset coil

Use CODESYS Ladder blocks for `TON`, `R_TRIG`, `F_TRIG`, and `CTU`.

## Network 001: Edge Detection Blocks

Instantiate the following blocks in separate Ladder networks or one ordered network:

```text
R_AtEntry      CLK := FIO.iAtEntry
R_AtTurnEntry  CLK := FIO.iAtTurnEntry
R_AtRightEntry CLK := FIO.iAtRightEntry
R_AtLeftEntry  CLK := FIO.iAtLeftEntry
F_AtRightExit  CLK := FIO.iAtRightExit
F_AtLeftExit   CLK := FIO.iAtLeftExit
R_Fault        CLK := M_Fault
```

## Network 002: Auto Permissive

```text
 FIO.iAutoMode     FIO.iStopNC      FIO.iEStopNC      M_Fault
----| |---------------| |---------------| |-------------|/|--------( M_AutoPermissive )
```

## Network 003: Manual Permissive

```text
 FIO.iAutoMode     FIO.iStopNC      FIO.iEStopNC      M_Fault
----|/|---------------| |---------------| |-------------|/|--------( M_ManualPermissive )
```

## Network 004: Run Latch Set

```text
 M_AutoPermissive      FIO.iStartPB
----| |--------------------| |--------------------------------------(S M_Run)
```

## Network 005: Run Latch Reset

Create parallel reset branches for Stop, E Stop, and Fault.

```text
 FIO.iStopNC
----|/|-------------------------------------------------------------(R M_Run)

 FIO.iEStopNC
----|/|-------------------------------------------------------------(R M_Run)

 M_Fault
----| |-------------------------------------------------------------(R M_Run)
```

## Network 006: Simulated Emergency Stop Fault

```text
 FIO.iEStopNC
----|/|-------------------------------------------------------------(S M_Fault)
```

## Network 007: Reset Fault and Sequence

Reset is accepted only when E Stop and Stop circuits are healthy.

```text
 FIO.iResetPB      FIO.iEStopNC      FIO.iStopNC
----| |----------------| |---------------| |------------------------(R M_Fault)
```

Use the same condition to reset:

`M_Loading`, `M_RotateToUnload`, `M_Discharge`, `M_ReturnHome`, `M_EntryOccupied`, `M_LowSeen`, `M_HighSeen`, `M_BoxLow`, `M_BoxHigh`, `M_LeftRun`, `M_RightRun`.

Set `M_Idle` when Reset is accepted **and** `FIO.iAtLoadPos` is TRUE.

```text
 FIO.iResetPB  FIO.iEStopNC  FIO.iStopNC  FIO.iAtLoadPos
----| |------------| |-----------| |------------| |-----------------(S M_Idle)
```

If the turntable is not at load position after a fault, use Manual mode to recover it before resetting the automatic sequence.

## Network 008: Entry Occupancy

```text
 R_AtEntry.Q
----| |-------------------------------------------------------------(S M_EntryOccupied)

 R_AtTurnEntry.Q
----| |-------------------------------------------------------------(R M_EntryOccupied)
```

## Network 009: Classification Memory

```text
 FIO.iLowBox
----| |-------------------------------------------------------------(S M_LowSeen)

 FIO.iHighBox
----| |-------------------------------------------------------------(S M_HighSeen)
```

At the turntable entry, classify the box.

```text
 R_AtTurnEntry.Q      M_HighSeen
----| |-------------------| |---------------------------------------(S M_BoxHigh)

 R_AtTurnEntry.Q      M_HighSeen      M_LowSeen
----| |-------------------|/|------------| |------------------------(S M_BoxLow)
```

Mutual exclusion:

```text
 M_BoxHigh
----| |-------------------------------------------------------------(R M_BoxLow)

 M_BoxLow
----| |-------------------------------------------------------------(R M_BoxHigh)
```

## Network 010: Invalid Classification Fault

```text
 R_AtTurnEntry.Q      M_HighSeen      M_LowSeen
----| |-------------------|/|------------|/|------------------------(S M_Fault)
```

## Network 011: Idle to Loading Transition

```text
 M_Run  M_AutoPermissive  M_Idle  FIO.iAtTurnEntry       ClassValid
--| |--------| |------------| |---------| |-----------------| |-----(S M_Loading)
```

Implement `ClassValid` as a parallel branch of `M_BoxHigh OR M_BoxLow`.

Use the same transition condition to Reset `M_Idle`.

## Network 012: Loading to Rotate Transition

```text
 M_Loading      FIO.iAtFront
----| |-------------| |---------------------------------------------(S M_RotateToUnload)
----| |-------------| |---------------------------------------------(R M_Loading)
```

## Network 013: Rotate to Discharge Transition

```text
 M_RotateToUnload      FIO.iAtUnloadPos
----| |---------------------| |-------------------------------------(S M_Discharge)
----| |---------------------| |-------------------------------------(R M_RotateToUnload)
```

## Network 014: High Box Discharge Complete

```text
 M_Discharge      M_BoxHigh      R_AtRightEntry.Q
----| |--------------| |---------------| |--------------------------(S M_ReturnHome)
----| |--------------| |---------------| |--------------------------(R M_Discharge)
```

## Network 015: Low Box Discharge Complete

```text
 M_Discharge      M_BoxLow       R_AtLeftEntry.Q
----| |--------------| |---------------| |--------------------------(S M_ReturnHome)
----| |--------------| |---------------| |--------------------------(R M_Discharge)
```

## Network 016: Return Home to Idle

```text
 M_ReturnHome      FIO.iAtLoadPos
----| |----------------| |------------------------------------------(S M_Idle)
----| |----------------| |------------------------------------------(R M_ReturnHome)
```

Use the same condition to reset classification memory:

`M_LowSeen`, `M_HighSeen`, `M_BoxLow`, `M_BoxHigh`.

## Network 017: Left Exit Conveyor Latch

```text
 R_AtLeftEntry.Q
----| |-------------------------------------------------------------(S M_LeftRun)

 F_AtLeftExit.Q
----| |-------------------------------------------------------------(R M_LeftRun)
```

## Network 018: Right Exit Conveyor Latch

```text
 R_AtRightEntry.Q
----| |-------------------------------------------------------------(S M_RightRun)

 F_AtRightExit.Q
----| |-------------------------------------------------------------(R M_RightRun)
```

## Network 019: Entry Jam Timer

```text
TON T_EntryJam
IN := M_Run AND M_AutoPermissive AND M_EntryOccupied AND M_Idle
PT := T#8s
```

## Network 020: Loading Timeout

```text
TON T_LoadTimeout
IN := M_Run AND M_Loading
PT := T#4s
```

## Network 021: Rotate Timeout

```text
TON T_RotateTimeout
IN := M_Run AND M_RotateToUnload
PT := T#4s
```

## Network 022: Discharge Timeout

```text
TON T_DischargeTimeout
IN := M_Run AND M_Discharge
PT := T#5s
```

## Network 023: Return Home Timeout

```text
TON T_ReturnTimeout
IN := M_Run AND M_ReturnHome
PT := T#4s
```

## Network 024: Exit Conveyor Timeouts

```text
TON T_LeftExitTimeout
IN := M_Run AND M_LeftRun
PT := T#8s

TON T_RightExitTimeout
IN := M_Run AND M_RightRun
PT := T#8s
```

## Network 025: Timeout Fault Latch

Create parallel branches to one Set coil `M_Fault`:

```text
T_EntryJam.Q
T_LoadTimeout.Q
T_RotateTimeout.Q
T_DischargeTimeout.Q
T_ReturnTimeout.Q
T_LeftExitTimeout.Q
T_RightExitTimeout.Q
```

If any branch is TRUE:

```text
---------------------------------------------------------------(S M_Fault)
```

## Network 026: Automatic Feeder Command

```text
 M_Run  M_AutoPermissive  M_Idle  M_EntryOccupied  M_LeftRun  M_RightRun
--| |--------| |------------| |--------|/|-------------|/|---------|/|----( Auto_Feeder )
```

Create `Auto_Feeder` as a BOOL local variable if you prefer explicit intermediate commands.

## Network 027: Automatic Entry Conveyor Command

The entry conveyor runs only while the cell is in Idle and the entry section contains one box. When the box reaches the turntable, the sequence changes to Loading and the entry conveyor stops while the turntable Load command takes over.

```text
 M_Run  M_AutoPermissive  M_Idle  M_EntryOccupied
--| |--------| |------------| |--------| |------------------------( Auto_Entry )
```

Equivalent Boolean intent:

`Auto_Entry = M_Run AND M_AutoPermissive AND M_Idle AND M_EntryOccupied`

This first release intentionally uses single piece flow. A later performance revision can add a buffered queue with separate class memory for the next product.

## Network 028: Automatic Turntable Outputs

### Load Direction

```text
 M_Run  M_AutoPermissive       M_Loading
--| |--------| |-------------------| |-----------------------------+
                                                                  +--( Auto_Load )
 M_Discharge  M_BoxHigh
----------------| |--------| |------------------------------------+
```

### Unload Direction

```text
 M_Run  M_AutoPermissive  M_Discharge  M_BoxLow
--| |--------| |-------------| |----------| |---------------------( Auto_Unload )
```

### Turn Command

```text
 M_Run  M_AutoPermissive       M_RotateToUnload
--| |--------| |-------------------| |-----------------------------+
                                                                  +--( Auto_Turn )
 M_Discharge
----------------| |------------------------------------------------+
```

`Auto_Turn` is intentionally FALSE during `M_ReturnHome`, allowing the Factory I/O turntable to return to its load position.

## Network 029: Automatic Exit Commands

```text
 M_Run  M_AutoPermissive  M_LeftRun
--| |--------| |-------------| |----------------------------------( Auto_Left )

 M_Run  M_AutoPermissive  M_RightRun
--| |--------| |-------------| |----------------------------------( Auto_Right )
```

## Network 030: Manual Commands

Create Manual command branches using `M_ManualPermissive`.

```text
M_ManualPermissive  HMI.xJogFeeder ----------------------------( Manual_Feeder )
M_ManualPermissive  HMI.xJogEntry  ----------------------------( Manual_Entry )
M_ManualPermissive  HMI.xJogTurn   ----------------------------( Manual_Turn )
M_ManualPermissive  HMI.xJogLeftExit --------------------------( Manual_Left )
M_ManualPermissive  HMI.xJogRightExit -------------------------( Manual_Right )
```

Load and Unload must be mutually exclusive:

```text
 M_ManualPermissive  HMI.xJogLoad  HMI.xJogUnload
----| |----------------| |-------------|/|------------------------( Manual_Load )

 M_ManualPermissive  HMI.xJogUnload  HMI.xJogLoad
----| |----------------| |---------------|/|----------------------( Manual_Unload )
```

## Network 031: Final Physical Outputs

Each final actuator is the OR of its Auto and Manual command, followed by a final hard gating layer. The direct `iEStopNC`, `iStopNC`, and `NOT M_Fault` contacts ensure outputs drop in the same PLC scan even if a permissive intermediate variable was calculated earlier in the scan.

General pattern:

```text
     Auto_Command
--------| |---------+
                    +--- FIO.iEStopNC --- FIO.iStopNC --- M_Fault --- Physical Output
 Manual_Command     |         | |              | |          |/|
--------| |---------+
```

Apply the pattern as follows:

```text
(Auto_Feeder OR Manual_Feeder) AND FIO.iEStopNC AND FIO.iStopNC AND NOT M_Fault -> FIO.oFeederConveyor
(Auto_Entry OR Manual_Entry) AND FIO.iEStopNC AND FIO.iStopNC AND NOT M_Fault -> FIO.oEntryConveyor
(Auto_Load OR Manual_Load) AND FIO.iEStopNC AND FIO.iStopNC AND NOT M_Fault -> FIO.oLoad
(Auto_Unload OR Manual_Unload) AND FIO.iEStopNC AND FIO.iStopNC AND NOT M_Fault -> FIO.oUnload
(Auto_Turn OR Manual_Turn) AND FIO.iEStopNC AND FIO.iStopNC AND NOT M_Fault -> FIO.oTurn
(Auto_Left OR Manual_Left) AND FIO.iEStopNC AND FIO.iStopNC AND NOT M_Fault -> FIO.oLeftConveyor
(Auto_Right OR Manual_Right) AND FIO.iEStopNC AND FIO.iStopNC AND NOT M_Fault -> FIO.oRightConveyor
```

## Network 032: Indicator Outputs

```text
M_Run AND M_AutoPermissive AND NOT M_Fault -> FIO.oRunLamp
M_Fault                                    -> FIO.oFaultLamp
FIO.iAutoMode                              -> FIO.oAutoLamp
```

## Network 033: Production Counters

Use `CTU` blocks with a large PV such as 32767.

High product count pulse:

`R_AtRightEntry.Q AND M_BoxHigh`

Low product count pulse:

`R_AtLeftEntry.Q AND M_BoxLow`

Total product count pulse:

`(R_AtRightEntry.Q AND M_BoxHigh) OR (R_AtLeftEntry.Q AND M_BoxLow)`

Fault count pulse:

`R_Fault.Q`

Configure:

```text
C_High.CU  := High product count pulse
C_Low.CU   := Low product count pulse
C_Total.CU := Total product count pulse
C_Fault.CU := R_Fault.Q
PV         := 32767
R          := FALSE or a dedicated maintenance reset command
```

## Network 034: State Integrity Diagnostic

During commissioning, monitor all state bits. Under normal automatic operation, exactly one of the following should be TRUE:

`M_Idle`, `M_Loading`, `M_RotateToUnload`, `M_Discharge`, `M_ReturnHome`.

For the first implementation, verify this in the Watch window. A later revision can add explicit state conflict diagnostics.

## Commissioning Assumption

The exact active logic of `iLowBox` and `iHighBox` depends on the Factory I/O sensor arrangement. This design assumes a tall box can activate the high beam and a low box does not. Confirm the two inputs online before running Auto mode. If the scene presents inverted or different behavior, change only the classification networks, not the sequence architecture.
