(* IEC 61131-3 reference logic. Map variables to the target runtime explicitly. *)
TYPE ESP_STATE : (IDLE, PERMISSIVE_CHECK, STARTING, RAMPING, RUNNING, DERATED, CONTROLLED_STOP, TRIPPED, LOCKOUT); END_TYPE

VAR
    State : ESP_STATE := IDLE;
    StartCmd, StopCmd, EStop, CommHealthy, SensorHealthy : BOOL;
    IntakePressureBar, MotorCurrentA, MotorTemperatureC : REAL;
    RequestedFrequencyHz, SafeFrequencyHz : REAL;
    FirstOutCode : UINT := 0;
END_VAR

IF EStop OR IntakePressureBar < 32.0 OR MotorCurrentA > 180.0 OR MotorTemperatureC > 125.0 THEN
    IF FirstOutCode = 0 THEN
        IF EStop THEN FirstOutCode := 1;
        ELSIF IntakePressureBar < 32.0 THEN FirstOutCode := 2;
        ELSIF MotorCurrentA > 180.0 THEN FirstOutCode := 3;
        ELSE FirstOutCode := 4;
        END_IF;
    END_IF;
    State := TRIPPED;
END_IF;

CASE State OF
    IDLE:
        SafeFrequencyHz := 0.0;
        IF StartCmd THEN State := PERMISSIVE_CHECK; END_IF;
    PERMISSIVE_CHECK:
        IF CommHealthy AND SensorHealthy AND NOT EStop THEN State := STARTING;
        ELSE State := IDLE;
        END_IF;
    STARTING:
        SafeFrequencyHz := 35.0;
        State := RAMPING;
    RAMPING:
        SafeFrequencyHz := MIN(SafeFrequencyHz + 0.25, LIMIT(35.0, RequestedFrequencyHz, 60.0));
        IF SafeFrequencyHz >= LIMIT(35.0, RequestedFrequencyHz, 60.0) THEN State := RUNNING; END_IF;
    RUNNING:
        SafeFrequencyHz := LIMIT(35.0, RequestedFrequencyHz, 60.0);
        IF NOT CommHealthy OR NOT SensorHealthy THEN State := DERATED; END_IF;
        IF StopCmd THEN State := CONTROLLED_STOP; END_IF;
    DERATED:
        SafeFrequencyHz := 40.0;
        IF CommHealthy AND SensorHealthy THEN State := RUNNING; END_IF;
        IF StopCmd THEN State := CONTROLLED_STOP; END_IF;
    CONTROLLED_STOP:
        SafeFrequencyHz := MAX(0.0, SafeFrequencyHz - 0.5);
        IF SafeFrequencyHz = 0.0 THEN State := IDLE; END_IF;
    TRIPPED:
        SafeFrequencyHz := 0.0;
        State := LOCKOUT;
    LOCKOUT:
        SafeFrequencyHz := 0.0;
END_CASE;
