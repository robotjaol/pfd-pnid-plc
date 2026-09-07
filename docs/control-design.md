# Control Design

## Hierarchy

1. The plant model computes the virtual well response.
2. The controller requests VFD frequency.
3. The safety supervisor validates magnitude, rate, and hard-trip conditions.
4. The plant receives only the validated command.

## PID baseline

The PID loop regulates intake pressure. Error sign is selected so that pressure above setpoint raises speed and increases drawdown. Integral action includes conditional anti-windup, and the output passes through magnitude and ramp-rate limits.

## Future constrained MPC

The planned manipulated variables are VFD frequency and choke position. The objective combines intake-pressure tracking, production tracking, electrical energy, control movement, and slack penalties. Constraints include intake pressure, motor current, temperature, pump operating envelope, frequency, frequency ramp, choke position, and solver deadline.

## Safe autonomy rule

The optimizer never owns trips. Its output is a recommendation that passes through constraint validation and deterministic logic. Invalid, stale, uncertain, or late recommendations force advisory or degraded operation.

