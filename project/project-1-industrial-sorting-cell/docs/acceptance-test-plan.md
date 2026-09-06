# Acceptance Test Plan

| Test | Scenario | Expected Result | Evidence |
|---|---|---|---|
| AT01 | Healthy startup in Auto | Run latches after Start | Online Ladder screenshot |
| AT02 | Press Stop during Idle | Run drops and outputs de energize | Screenshot |
| AT03 | Activate E Stop | Fault latches and Run drops | Screenshot |
| AT04 | High box cycle | High class captured and box exits right | Video or GIF |
| AT05 | Low box cycle | Low class captured and box exits left | Video or GIF |
| AT06 | Ten mixed boxes | No incorrect routing | Counter screenshot |
| AT07 | Block entry conveyor | Entry jam timeout faults | Fault screenshot |
| AT08 | Prevent load completion | Loading timeout faults | Fault screenshot |
| AT09 | Prevent unload position | Rotation timeout faults | Fault screenshot |
| AT10 | Block right exit | Right exit jam faults | Fault screenshot |
| AT11 | Block left exit | Left exit jam faults | Fault screenshot |
| AT12 | Remove classification signal | Invalid classification faults | Screenshot |
| AT13 | Fault Reset with E Stop active | Reset rejected | Ladder screenshot |
| AT14 | Manual feeder jog | Feeder moves only in Manual | Screenshot |
| AT15 | Command Load and Unload jog together | Mutual exclusion prevents both commands | Ladder screenshot |
| AT16 | Resume after normal Stop | Sequence resumes without state corruption | Video |
| AT17 | 50 cycle endurance run | No deadlock or incorrect state overlap | Counter screenshot |

## Pass Criteria

All safety simulation permissives, routing behavior, timeout faults, and reset conditions must behave as documented. No two mutually exclusive sequence states may remain active simultaneously during normal operation.
