# Rev A — MCU selection and pin budget

## Decision

| Item | Choice | Why |
|---|---|---|
| SoC | **Nordic nRF52832-QFAA-R** | BLE advertising + SAADC + GPIOTE is enough; no USB/Thread need |
| Package | QFN-48-EP 6×6 mm | Escape on **2-layer** (matches JLCPCB plan) |
| LCSC / JLC | **C77540** | Extended; SMT Economic + Standard assembly |
| Form | **Bare SoC** (not a module) | Same fab style as x.drop beacon; PCB antenna on-board |
| Antenna | **PCB inverted-F** (Nordic nRF52832 reference geometry) | User requirement; not DN024 (that’s TI sub-GHz) |
| HFCLK | 32 MHz crystal + load caps (NP0, Nordic values) | Required for radio |
| LFCLK | 32.768 kHz crystal on P0.00/P0.01 | AA life / RTC for CPM windows |
| DCDC | Enable internal DC/DC (inductor on DCC) | Lower radio current on 2×AA |
| Debug | SWDIO / SWDCLK + RESET; Tag-Connect TC2030 style like beacon | |

Rejected for rev A: nRF52840 (extra cost/memory unused), pre-certified modules (harder JLC BOM, fights “PCB antenna + JLC parts”), WLCSP (painful on 2-layer).

Certification note: bare SoC + PCB antenna means **we own** FCC/CE/Bluetooth qualification later. Acceptable for prototype rev A.

## Power (2×AA, beacon clips)

Copy beacon battery contacts (JLC assembly parts):

| Ref (beacon) | MPN | LCSC | Role |
|---|---|---|---|
| BT+ | **MY-ZJ-3030** | **C964874** | AA positive contact |
| BT− | **MY-AA-03** | **C19184098** | AA negative spring |

Two cells in series → VBAT ≈ 1.8–3.2 V into nRF52832 (1.7–3.6 V). No 3.3 V LDO required if the SoC runs direct from VBAT (beacon pattern). Reverse insertion via clip geometry only.

Mechanical cell outlines: copy `aaCell` from `~/enzo/x.drop-beacon/pcb/components/aaCell/`.

## Pin budget (QFN-48 GPIO map)

Fixed / non-GPIO (schematic only): `VDD`, `VSS`, `DEC1`–`DEC4`, `DCC`, `ANT`, `XC1`, `XC2`, `SWDCLK`, `SWDIO`.

| Net | Pin | Mode | Notes |
|---|---|---|---|
| XL1 | **P0.00** | LF crystal | 32.768 kHz |
| XL2 | **P0.01** | LF crystal | |
| **HV_SENSE** | **P0.02 / AIN0** | SAADC | Divided tube HV (~400 V → ≤1.8 V AIN). Filter near pin. |
| **VBAT_SENSE** | **P0.03 / AIN1** | SAADC | Optional VBAT divider for advertising battery state |
| NFC1 | P0.09 | **NC** | Leave unconnected; do not route under antenna |
| NFC2 | P0.10 | **NC** | |
| **GM_PULSE** | **P0.11** | GPIOTE IN | Active-low impulse from front-end (V6-style). Sense low, IRQ / PPI count. |
| **HV_EN** | **P0.12** | GPIO OUT | Enables free-running HV converter (not MCU PWM — so System OFF / deep sleep stays possible) |
| **LED_STATUS** | **P0.13** | GPIO OUT | Optional activity LED; series R for 2×AA |
| UART_TX | P0.14 | UART | Debug bring-up only; test pads OK |
| UART_RX | P0.15 | UART | |
| SPARE0 | P0.16 | GPIO | Test pad |
| SPARE1 | P0.17 | GPIO | Test pad |
| **RESET** | **P0.21** | RESET | External pull-up; SWD header |
| Remaining P0.04–P0.08, P0.18–P0.20, P0.22–P0.31 | — | **Unused / test pads** | Prefer leave as unconnected GPIOs with DNF test pads rather than tying |

### Layout constraints

- Keep **HV_EN** and HV magnetics away from `ANT` / match network and from `HV_SENSE` analog.
- Route `GM_PULSE` short; no long antenna-adjacent stubs.
- Follow Nordic nRF52832 QFN reference for RF match + PCB antenna clearance (metal-free keepout; no unrelated pads — beacon-style custom rule later).
- Prefer JLC **Basic** passives for decoupling; RF match = C0G/NP0 + high-Q L (per `kicad-bom` skill).

## Still open (next, not blocking this lock)

- Exact HV IC / boost topology (free-running, closed-loop, ADC readback) — separate doc
- CTC-5 tube spring/fuse clips (Ø12 mm) — JLC part pick
- Final RF match BOM after antenna geometry is drawn

## Skills path

User asked for `~/agent-skills`. That path did not exist; linked to `~/.codex/skills` (KiCad BOM / schematic / PCB / gerbers / footprint skills). Prefer LCSC field name **`LCSC`** on symbols for JLC BOM export (`kicad-bom` skill).


## Product locks (rev A)

- **BLE:** advertising **plus** connectable GATT (config/telemetry), not ads-only.
- **Mechanics:** closed plastic **handheld shell** — antenna keepout must account for hand and enclosure; shell CAD later.
- **Defaults:** status LED only; raw CPM in ads/GATT (µSv/h later); alkaline 2×AA floor; TC2030-style SWD.
