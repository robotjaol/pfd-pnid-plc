# Sequence of Operation

## Preconditions

1. Factory I/O and CODESYS are connected.
2. Stop NC and E Stop NC inputs are TRUE.
3. Auto mode is selected.
4. No fault is latched.
5. Turntable is at the load position.

## Sequence

### S0 IDLE

The feeder releases one box only when the cell is Idle and both exit conveyor occupancy latches are clear. Classification sensor states are captured while the box advances. This release uses single piece flow to keep classification and recovery deterministic.

Transition to S1 occurs when the box reaches `iAtTurnEntry` and a valid class has been captured.

### S1 LOADING

`oLoad` is energized to transfer the box from the entry conveyor onto the turntable.

Transition to S2 occurs when `iAtFront` is TRUE.

### S2 ROTATE TO UNLOAD

`oTurn` is energized. The turntable moves from load position to unload position.

Transition to S3 occurs when `iAtUnloadPos` is TRUE.

### S3 DISCHARGE

For a High box, `oLoad` remains active to discharge toward the right side.

For a Low box, `oUnload` is active to discharge toward the left side.

`oTurn` remains active to hold the turntable at the unload orientation.

Transition to S4 occurs when the corresponding right or left entry sensor confirms that the box has entered the discharge conveyor.

### S4 RETURN HOME

`oTurn` is removed, allowing the turntable to return to its load position.

Transition to S0 occurs when `iAtLoadPos` is TRUE.

Classification memory is cleared after the completed cycle.

## Exit Conveyor Control

A discharge conveyor starts when its entry sensor detects a box. It remains on until the box clears its exit sensor. A timeout supervises each exit conveyor.

## Stop Behavior

A normal Stop removes the Run latch and pauses automatic outputs. Sequence state is retained. A new Start may resume the sequence if no fault exists.

## Fault Behavior

A timeout or invalid classification latches `M_Fault` and removes the Run latch. Automatic outputs are disabled. Recovery is performed in Manual mode if the mechanism is not in a safe reset position.
