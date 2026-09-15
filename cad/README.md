# CAD / 3D models for geiger2 renderings

## Layout lock
Handheld: **CTC-5 along one long side**, **2×AA along the other** (parallel, similar ~110 mm length). Closed plastic shell later.

## Models in `models/`

| File | Source | Use |
|---|---|---|
| `aaCell.step` | x.drop-beacon `pcb/components/aaCell/` | AA cell body (×2) |
| `AA-LR6.FCStd` | same | FreeCAD parametric AA |
| `MY-AA-03.step` | beacon | Negative spring contact |
| `MY-ZJ-3030.step` | beacon | Positive contact |
| `NRF52832-QFAA-C77540.step` | tscircuit/EasyEDA modelcdn C77540 | SoC |
| `NRF52832-QFAA-C77540.obj` | same | SoC (mesh) |
| `QFN48.step` | beacon CC1310 QFN (fallback) | Only if C77540 model fails |
| `CTC5-approx.stl/.obj/.glb` | Generated Ø12×110 mm cylinder | Tube stand-in until better STEP |

## From wirelessGeigerCounter (`from-wirelessGeigerCounter/`)
Inventor history: `Acrylic Tube Housing.ipt`, `Back Cap.ipt` (SBM-20 era acrylic shell). **Not STEP** — needs Inventor/Fusion export for tscircuit. Useful as shell reference, not drop-in cadModel.

Better public STEP exists (GrabCAD / Marathon “SBM20-CTC5.step”, ~109.2×12 mm) — import manually if license OK; until then use `CTC5-approx.*`.

## tscircuit wiring
Prefer `cadModel={{ stepUrl, objUrl }}` like muon3 imports (EasyEDA CDN for JLC parts). For local files, use paths under `cad/models/` or host via modelcdn after `tsci` import.
