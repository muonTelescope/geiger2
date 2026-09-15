# JLCPCB 2-layer design rules (from x.drop beacon)

**Source:** Downloads fab pack
`/Users/sawaiz/Downloads/x.drop-beacon-0.8.6/pcb/beacon.kicad_pro`
(JLC-preferred mins). Do **not** copy git `master` `.kicad_pro` on
`~/enzo/x.drop-beacon` for a new board — that tree still has the older
0.1524 mm track / 0.127 mm hole / 0.5 mm silk set.

Custom rules seed: [`hardware/pcb/geiger2.kicad_dru`](../hardware/pcb/geiger2.kicad_dru).

GitHub reference: `teamsafehome/x.drop-beacon`.

## Order / cart (beacon convention)

| Option | Value |
|---|---|
| Layers | 2 |
| Thickness | 1.6 mm |
| Outer copper | 1 oz |
| Finish | ENIG |
| Solder mask | black (both sides) |
| Silkscreen | white |
| E-test | yes |
| Impedance control | none |
| PCBA | SMT **top only**, **Standard** |

KiCad stackup metadata alone does **not** configure the order — set these in the JLCPCB form.

### Stackup (from beacon.kicad_pcb)

F.Cu 0.035 mm (1 oz) / FR4 core 1.51 mm εr 4.5 / B.Cu 0.035 mm. Mask thickness 0.01. Copper finish ENIG.

## Board design rules (mm) — JLC preferred

| Parameter | Value |
|---|---|
| min_track_width / min_connection / min_clearance | **0.15** |
| zone min_clearance | **0.20** |
| min_copper_edge_clearance | **0.20** |
| min_hole_clearance / min_hole_to_hole | **0.20** |
| min_through_hole_diameter | 0.2 |
| min_via_diameter | **0.60** |
| min_via_annular_width | **0.15** |
| silk_line_width | **0.15** |
| silk text size / thickness | **1.0 / 0.15** |
| min_silk_clearance | **0.15** |
| min_text_height / min_text_thickness | **1.0 / 0.15** |
| fab text | 1.0 / 0.15 |
| solder_mask_min_width | **0.13** |
| pad_to_mask_clearance | 0 |
| tenting | front + back |
| blind/buried / microvias | off |
| drc_exclusions | empty (fix root causes; don’t waiver-farm) |

## Default netclass

- track **0.15**, clearance **0.15**, via **0.60 / 0.30**

## Vias

| Diameter | Drill | Use |
|---|---|---|
| **0.6** | **0.3** | Signal (default) |
| ≥ **0.45** pad | **0.2** | Thermal (avoid JLC Kelvin surcharge) |
| 1.0 | 0.6 | Power / mechanical |

**Do not** use 0.35/0.2 vias — JLC charges 4-wire Kelvin.

## Fab / export conventions we follow

- Gerbers.zip files at **archive root** (no nested folder)
- Separate PTH / NPTH Excellon, mm; shared drill/place origin
- Exclude non-SMT from BOM/PnP (headers, fiducials, tooling, cells)
- Tooling holes `1.152mm-ToolingHole`: **NPTH only, no paste**, keep mask openings (not tented)
- Silk: hide tiny 0402/LED refs; keep F.Fab 1.0/0.15; eyeball CPL for polarized parts

## Beacon-only rules (not copied)

Antenna keepout / DN024 radiator rules and J1 guide-hole 5 mil escape stay on the beacon. Re-add RF keepout once the nRF52 antenna geometry is chosen.
