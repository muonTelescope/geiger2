# Rev A component review

Package defaults accepted 2026-09-15: 0603 general passives, 0402 RF where the
Nordic reference requires them, larger HV packages to meet voltage/derating needs.
Top-side SMT, black mask, white silk, ENIG and the beacon 0.8.6 JLC fabrication
rules remain the manufacturing baseline. `~/agent-skills` resolves to
`~/.codex/skills`; this review follows kicad-bom, kicad-schematic and kicad-pcb.

## Selection ledger

These are design candidates, **not an assembly BOM**. Exact values and MPNs must
live in the eventual authoritative circuit source; manufacturing CSVs are generated
from that source. No placement/CPL or Gerbers are released from the concept model.
Database quantities are a 2026-09-15 snapshot, not reserved or live inventory.

| Function | MPN / LCSC | Package | Review / state |
|---|---|---|---|
| BLE MCU | Nordic NRF52832-QFAA-R / C77540 | QFN48 6×6 mm | Existing locked choice; database 25,901, Extended |
| HV comparator + reference | TI TLV3012BIDBVR / C20345924 | SOT-23-6 | Recommended; 1.65 V minimum supply, 1.242 V reference, typical 8 mV hysteresis; database 3,096, Extended |
| CW capacitors | TDK C3216C0G2J103JT000N / C342714 | 1206 | Recommended 10 nF, 630 V, C0G ±5%; database 2,413, Extended. Avoid unqualified X7R DC-bias loss |
| CW diodes | Diodes Inc. BAV21W-7-F / C155214 | SOD-123 | Candidate; catalog 200 V DC reverse rating, 50 ns recovery. Generic 250 V SPICE diode is **not** this vendor model; check actual reverse stress and hot leakage before locking |
| HV inductor | TDK B82442T1105K050 / C2041861 | 5.6×5 mm | Candidate 1 mH, 9.5 Ω DCR, catalog 150 mA rated / 310 mA saturation. Simulation baseline is 8 Ω, so not a drop-in validated choice |
| Oscillator | TI LMC555CMX/NOPB / C90760 | SOIC-8 | Candidate only: supply range includes depleted 2×AA. Output drive at 1.8 V, startup timing and oscillator power require validation |
| HV switch alternative | onsemi MMBTA42LT1G / C94389 | SOT-23 | Candidate BJT alternative to a boosted-gate MOSFET; base drive, storage time and SOA unresolved |
| Positive AA contact | MY-ZJ-3030 / C964874 | Imported beacon part | Existing choice, STEP retained; mating geometry not qualified by concept render |
| Negative AA contact | MY-AA-03 / C19184098 | Imported beacon part | Existing choice, STEP retained |
| Tube contacts | TBD | Ø12 mm tube compatible | No unverified fuse clip MPN assigned |
| HV divider | 4×33 MΩ + 412 kΩ | HV legs provisionally 1206 | Exact MPNs open. Search parser returned 33 **mΩ** for 33 **MΩ**: explicitly rejected those results |

Full returned metadata and datasheet links: [parts-snapshot.json](parts-snapshot.json).
Prefer Basic/Preferred when ratings and documentation meet the need. Lower catalog
price does not justify an undocumented HV part or substituting a different manufacturer's
similarly named device. IC alternatives above are not all installed in the model.

## Electrical design checks

- Each 33 MΩ divider leg sees about 99.7 V and 0.302 mW at 400 V. Working voltage,
  voltage coefficient, leakage and contamination dominate over resistor wattage.
  Target at least 200 V working rating per leg, verify temperature derating. Thin-film
  is preferred where available; do not invent a 33 MΩ thin-film MPN.
- A 412 kΩ lower divider leg gives 1.2446 V at 400 V. Its high source impedance
  requires a separately validated ADC buffer or sampling reservoir/acquisition time.
  Adding a large capacitor directly on the comparator node changes loop response.
- Eight 10 nF C0G capacitors avoid the large DC-bias uncertainty of Class II ceramics.
  Individual ladder capacitors see stage differences, not all 400 V, but pad-to-ground
  potentials still rise along the ladder. Capacitance tolerance and leakage remain real.
- The ideal switch's 2 Ω on-resistance is not evidence that a 100–200 V MOSFET is
  fully enhanced at 1.8 V. Gate threshold is not an on-resistance guarantee. Choose a
  validated gate supply/driver or explicitly model a BJT and its base-current cost.
- RF passives must be C0G/NP0 capacitors and high-Q inductors. No final RF match is
  chosen before reference geometry, board ground, enclosure and hand effects are assessed.
- The general 0.15 mm JLC clearance is **not an HV spacing rule**. Establish separate
  HV-to-LV and per-stage constraints from the intended environment and voltage stress;
  do not route the concept as a default-netclass board.

## Primary references

- [TI TLV3012 family datasheet](https://www.ti.com/lit/ds/symlink/tlv3012.pdf)
- [TI LMC555 datasheet](https://www.ti.com/lit/ds/symlink/lmc555.pdf)
- [Analog Devices CN0536](https://www.analog.com/media/en/reference-design-documentation/reference-designs/cn0536.pdf): topology reference, not a 1.8 V drop-in design.
- Component-specific datasheets returned by JLC lookup are linked in the snapshot.
