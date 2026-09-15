# JLCPCB 2-layer design rules (from x.drop beacon)

Source of truth copied from `~/enzo/x.drop-beacon/pcb/beacon.kicad_pro` and
`beacon.kicad_dru` (rev ~0.8.8). Apply these in the geiger2 KiCad project;
custom rules live in [`hardware/pcb/geiger2.kicad_dru`](../hardware/pcb/geiger2.kicad_dru).

## Order form (beacon convention)

- JLCPCB FR4, **2 copper layers**
- 1.6 mm, **1 oz** copper
- White solder mask both sides, black silkscreen, ENIG
- KiCad stackup metadata alone does **not** configure the order — set these in the JLCPCB form

## Board design rules (mm)

| Parameter | Value | Notes |
|---|---|---|
| min clearance | 0.1524 (6 mil) | Default netclass |
| min track width | 0.1524 | Custom rule floor |
| min connection | 0.1524 | |
| min copper–edge clearance | 0.3 | |
| min hole clearance | 0.127 | |
| min hole-to-hole | 0.127 | |
| min through-hole diameter | 0.2 | |
| min via diameter | 0.5 | |
| min via annular width | 0.1 | |
| min text height / thickness | 0.5 / 0.1 | |
| blind/buried / microvias | off | |

## Preferred track widths

`0.1524, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 1.0` mm

## Preferred vias

| Diameter | Drill | Use |
|---|---|---|
| 0.6 | 0.3 | Signal (default) |
| 0.35 | 0.2 | Tight escape (use sparingly) |
| 1.0 | 0.6 | Power / mechanical |
| 0.45 pad / 0.2 drill | — | Thermal vias when avoiding JLC Kelvin surcharge (beacon TMP117 lesson) |

Default netclass: track 0.1524, via 0.6/0.3, clearance 0.1524.

## Beacon-specific rules not carried over

Antenna keepout / DN024 radiator rules and J1 guide-hole 5 mil escape are beacon-only.
Re-add RF keepout rules once the nRF52 antenna geometry is chosen.
