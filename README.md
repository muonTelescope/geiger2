# geiger2

Clean-sheet **Bluetooth-advertising Geiger counter**: nRF52-class MCU, CTC-5
(STS-5 / СТС-5) NOS Russian GM tube, regulated HV with voltage readback,
JLCPCB 2-layer PCB.

This is a new design. Prior wireless Geiger work
([wirelessGeigerCounter](https://github.com/sawaiz/wirelessGeigerCounter))
informs requirements; it is not a port. See [docs/prior-art.md](docs/prior-art.md).

## Goals

| Area | Decision |
|---|---|
| MCU / radio | nRF52 (or similar Nordic BLE SoC) — real BLE advertising, not nRF24 fakery |
| Detector | CTC-5 / STS-5 halogen-quenched GM tube (NOS Russian), same marking as stock on hand |
| HV | Regulated bias + **ADC readback** of tube voltage (fix the open-loop V6 gap) |
| Fab | JLCPCB **2-layer** FR4; DRC/settings copied from [x.drop beacon](../enzo/x.drop-beacon) — [docs/jlcpcb-drc.md](docs/jlcpcb-drc.md) |
| Firmware | BLE advertise CPM (and HV telemetry when useful); count pulses in hardware interrupt / PPI |

## Tube (CTC-5 / STS-5)

Typical datasheet window (verify each tube on the bench — NOS parts vary):

| Parameter | Typical |
|---|---|
| Operating voltage | **360–440 V** (often ~390–400 V nominal) |
| Starting / counting voltage | ~280–330 V |
| Plateau | ≥ 80 V, slope ≤ ~0.125 %/V |
| Anode load | 5–10 MΩ |
| Size | ~110 mm × Ø12 mm |
| Sensitive to | β / γ (hard beta + gamma); precursor class to SBM-20 |

Design HV setpoint near mid-plateau (~400 V) with regulation and continuous
readback so aging, temperature, and battery sag don’t walk off the plateau.

## Architecture (draft)

```
battery → 3.3 V regulator → nRF52
                └──────────→ HV boost / CW (or dedicated HV IC)
                                ├─ regulated ~400 V → CTC-5 anode (via 5–10 MΩ)
                                ├─ divider → MCU ADC (readback)
                                └─ quench / pulse → GPIO / PPI count

nRF52 → BLE ADV (device id, CPM, optional HV mV)
```

Open questions for schematic rev A: exact nRF52 module vs bare chip + antenna,
HV topology (free-running boost vs dedicated controller), battery chemistry,
and mechanical tube mount.

## Repo layout

```
hardware/pcb/     KiCad project (DRC seed: geiger2.kicad_dru)
firmware/         nRF52 firmware (Zephyr or nRF Connect SDK — TBD)
manufacturing/    JLCPCB BOM/CPL mappings when ready
docs/             prior art, fab rules, design notes
```

## Manufacturing

Match x.drop beacon order defaults unless we document a change:

- JLCPCB FR4, 2 layers, 1.6 mm, 1 oz, white mask, black silk, ENIG
- Design rules: [docs/jlcpcb-drc.md](docs/jlcpcb-drc.md)

## Status

Bootstrap: README, prior-art extract, JLCPCB DRC seed. Schematic / layout /
firmware not started yet.
