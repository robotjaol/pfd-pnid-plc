# Fault Matrix

| ID | Fault | Detection | Initial PT | Control Response | Recovery |
|---|---|---|---:|---|---|
| F01 | Entry jam | `M_EntryOccupied` remains TRUE | 8 s | Latch Fault, stop Auto | Inspect queue, Manual recovery, Reset |
| F02 | Turntable loading timeout | `M_Loading` remains TRUE | 4 s | Latch Fault | Remove obstruction, recover, Reset |
| F03 | Rotation timeout | `M_RotateToUnload` remains TRUE | 4 s | Latch Fault | Check position sensors and turn actuator |
| F04 | Discharge timeout | `M_Discharge` remains TRUE | 5 s | Latch Fault | Inspect discharge path |
| F05 | Return home timeout | `M_ReturnHome` remains TRUE | 4 s | Latch Fault | Check load position sensor |
| F06 | Left exit jam | `M_LeftRun` remains TRUE | 8 s | Latch Fault | Clear left line |
| F07 | Right exit jam | `M_RightRun` remains TRUE | 8 s | Latch Fault | Clear right line |
| F08 | Invalid classification | Box reaches turn entry with no class memory | Immediate | Latch Fault | Check height sensors |
| F09 | Emergency stop | `iEStopNC = FALSE` | Immediate | Latch Fault, remove Run | Restore E Stop, inspect machine, Reset |

## Commissioning Note

The initial timeout values are engineering defaults for simulation. Record actual maximum normal transition times, then set each timeout with adequate process margin.
