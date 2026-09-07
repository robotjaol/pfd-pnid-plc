# Physics Model

## Validity envelope

The baseline is a low-order dynamic model designed for transparent software integration and fault testing. It preserves expected directions and constraints but is not a substitute for calibrated nodal-analysis or vendor ESP design software.

## Reservoir inflow

The liquid rate is limited by a linear productivity relationship:

\[
q = J(P_r-P_{intake}),
\]

where \(J\) is the productivity index. This approximation is acceptable only within the declared single-phase equivalent envelope.

## Pump and system intersection

Pump head follows the affinity-law speed scaling and a quadratic approximation around a nominal curve. System resistance combines hydrostatic pressure, wellhead pressure, tubing loss, choke loss, and an injected blockage multiplier. The equilibrium flow is obtained from the available differential pressure and quadratic resistance.

\[
H(N,Q) = H_{shutoff}\left(\frac{N}{N_0}\right)^2
\left[1-k_Q\left(\frac{Q}{Q_{BEP}N/N_0}\right)^2\right].
\]

## Electrical and thermal model

Hydraulic power is \(P_h=Q\Delta P\). Electrical power divides hydraulic power by pump and motor efficiency. Current uses a simplified three-phase apparent-power relationship. Motor temperature is a first-order state driven by electrical load and ambient temperature.

## Known omissions

Gas-liquid slip, detailed PVT behavior, emulsion viscosity, pump-stage geometry, cable voltage drop, harmonics, transformer losses, annular transients, separator performance, thermal exchange along the wellbore, and mechanical thrust are deferred. Each must be added before claims are extended beyond the initial research questions.

