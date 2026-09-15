# Prior art — wirelessGeigerCounter

Pulled from [sawaiz/wirelessGeigerCounter](https://github.com/sawaiz/wirelessGeigerCounter)
(branch [`firmware/v6-ble`](https://github.com/sawaiz/wirelessGeigerCounter/tree/firmware/v6-ble))
and related [Sawaiz/geigerControl](https://github.com/Sawaiz/geigerControl).
geiger2 is **not** a port of this hardware.

Built hardware used **SBM-20**, not CTC-5. CTC-5 ≈ STS-5 ≈ SBM-20 class
([gstube STS-5](https://www.gstube.com/data/4540/);
[PocketMagic](https://www.pocketmagic.net/tube-sts-5-%D1%81tc-5-geiger-tube/)).
No CTC-5 was measured on the bench in that project.

## Lineage

| Generation | MCU | Radio | Tube | HV | Notes |
|---|---|---|---|---|---|
| V6 (2014 boards) | ATtiny2313 SOIC | nRF24L01+ | SBM-20 | MCU Timer0 PWM boost (~400 V **open-loop**) | Source of truth: `firmware/v6-ble`, `pcb/v6/` (`fbc6006:PCB/TX/`) |
| V7 CAD | ATtiny2313 QFN | nRF24 | SBM-20 | ICM7555 | `pcb/schematic.dch` — **do not mix** with V6 FW |
| Wi-Fi-era concept | ESP8266/ESP-12F | Wi-Fi | SBM-20 (README) | Schmitt boost + CW + op-amp (Maxim AN3757) | Concept / renders; not the built V6 |
| geigerControl | ESP8266 | Wi-Fi | — | — | Captive portal / OTA / websockets — **no pulse counting** |

## CTC-5 / STS-5 (public datasheet class)

| Parameter | Value |
|---|---|
| Start / counting | 280–330 V |
| Advised working | **360–440 V** (V6 aimed ~400 V on SBM-20) |
| Plateau | ≥ 80 V, slope 0.125 %/V |
| Anode load | **5–10 MΩ** |
| Stray input capacitance | ≤ 10 pF; coupling 7–10 pF |
| Background (max, gstube) | ~27 cpm |
| Size | ~110 mm × Ø12 mm |
| Pulse amplitude | **unknown** — V6 never scoped the anode pulse; do not invent |
| Dead time | ~190 µs noted for SBM-20 in V6 FW notes; **not measured** for CTC-5 |

Halogen self-quench; the anode resistor is the circuit quench.

## V6 HV (what was actually built)

- Timer0 Fast PWM → PB2/OC0A → boost: L1 SDR1005-103KL 10 mH, Q1 STN2580, D1 RS1M, C1 10 nF / 1.5 kV
- Anode load **R1 = 4.7 MΩ** (BOM; slightly under 5–10 MΩ datasheet)
- OCR0A = 127 @ 1 MHz → ~3.91 kHz, ~49.6% duty (“Set to 400V”)
- **No 555 on V6.** No HV sense net. ATtiny2313 has **no ADC** (AIN pins used by nRF SPI)
- Cannot deep-sleep: PWM must keep running or HV collapses (`SLEEP_MODE_IDLE`)

## V6 pulse path

MMBT3904 inverter: 22k / 100k / 220 pF 630 V / 10k pull-up → **Impulse / PD2 active-low**, INT0 falling edge. Idle high.

## V6 power / radio

- Schematic symbol VL621; BOM: MPD BC12AAL **2×AA**, +3 V rail, no regulator
- nRF24L01+ bit-bang SPI: CE=PD6 (net **CN**), CSN=PD5, SCK=PB0, MOSI=PD4, MISO=PB1
- `firmware/v6-ble`: Grinberg BLE **advertisement spoof** (ADV_NONCONN_IND, name GM) — not real BLE/GATT
- OSH Park 2-layer historically; geiger2 targets JLCPCB instead

## Lessons for geiger2

1. **Closed-loop HV + ADC readback** is the real upgrade (V6 was open-loop, no telemetry).
2. **Free-running HV** (or dedicated controller) so the nRF52 can sleep — don’t clock HV from the MCU if you want power-down.
3. Prefer anode load in the **5–10 MΩ** datasheet window; keep anode stray capacitance low.
4. Use **real nRF52 BLE** — do not port the nRF24 whitening stack.
5. Don’t mix V6 firmware with V7 schematic; don’t expect geigerControl to count pulses.
6. Cite `pcb/v6/bom.xlsx` for historical parts; don’t invent pulse amplitudes.

## Useful links

- https://github.com/sawaiz/wirelessGeigerCounter/tree/firmware/v6-ble
- CAD: `pcb/v6/` · Firmware: `firmware/v6-ble/`
- Last ShockBurst TX: git `bf09a87` `code/avrTx` (removed from master in `050199b`)
