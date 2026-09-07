# Safety and Limitations

OpenLift DED is educational research software. It is not approved, certified, calibrated, or validated for an operating oil well, hazardous area, high-voltage installation, safety instrumented function, or production decision.

## Non-negotiable rules

- Do not connect this baseline directly to field equipment.
- Do not reuse illustrative trip values or equipment ratings.
- Do not claim IEC, API, ATEX, SIL, functional-safety, or cybersecurity compliance.
- Keep hardwired and deterministic protection independent from analytics.
- Treat model predictions as hypotheses until calibrated and independently validated.
- Require operator authorization and management of change before any physical trial.

## Principal risks

Model-form error, unrepresented multiphase behavior, sensor bias, domain shift, stale timestamps, communication loss, unsafe optimizer recommendations, and incorrect configuration can produce plausible but wrong outputs. The design therefore records uncertainty, first-out trips, fallback behavior, and the source configuration for every experiment.

