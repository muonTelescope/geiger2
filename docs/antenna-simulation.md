# Antenna validation with openEMS

**Planned; no antenna simulation has been run.** Start openEMS work after the
PCB layout is finalized and the enclosure is designed. The current mechanical
concept is insufficient for antenna tuning. Keep both existing HV simulation
workflows; openEMS adds electromagnetic analysis of the PCB inverted-F antenna.

## Freeze the geometry and inputs

Record revision hashes for PCB copper, board outline, stackup, antenna/feed and
matching-network reference plane, and closed-case CAD. Include batteries, battery
contacts, tube metal and other nearby conductors with their actual positions.
Specify substrate, solder-mask and shell permittivity/loss assumptions with
sources, and distinguish measured properties from estimates. Document simplified
geometry and omitted features. Preserve RF keepouts in the final assembly.

## Cases and outputs

| Case | Purpose |
|---|---|
| Bare PCB | Establish antenna/feed baseline |
| PCB with tube, batteries and contacts | Quantify nearby-metal loading |
| Complete assembly in closed shell | Evaluate enclosure detuning and radiation |
| Representative hand placement, with a documented material model | Assess sensitivity to handheld use |

Sweep across the BLE operating band with margin on both sides. Report input
impedance and S11 at the defined feed reference plane, resonant frequency,
radiation efficiency, realized gain and far-field patterns. Inspect surface
currents and local fields to locate unintended coupling. Separate mismatch loss
from radiation loss and state gain/power normalization conventions.

Use a feed-port model appropriate to the final antenna and matching network;
do not silently treat the radio's package pin as a calibrated 50 Ω plane.
Check mesh refinement, simulation decay, absorbing-boundary separation and
material/dimensional sensitivity before trusting a resonance or efficiency.
Use near-field-to-far-field transformation for radiation results. The official
[openEMS antenna tutorial](https://docs.openems.de/en/latest/python/openEMS/Tutorials/Simple_Patch_Antenna.html)
illustrates ports, S-parameters and far-field analysis; its patch geometry is not
the inverted-F geometry for this project.

## Deliverables and completion criteria

- Reproducible model scripts under `sim/antenna/`, with tool versions and frozen input revisions.
- Mesh/geometry renders, convergence tables, S11/impedance plots and radiation patterns under `docs/antenna/`.
- A report comparing the cases and recording approximations, unresolved sensitivities and proposed matching values.
- Raw field dumps in an ignored build directory; retain compact numerical results and plot sources in Git.

Create those directories with the actual simulation implementation. Confirm the
final matching network using VNA measurements of assembled hardware in its case;
follow with an over-the-air BLE check. Simulation informs tuning but does not
replace these measurements. Set quantitative acceptance targets before evaluating
the final antenna; none are claimed achieved by the current concept renders.
