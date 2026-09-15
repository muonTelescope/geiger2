# Prior art — wirelessGeigerCounter

Pulled from [sawaiz/wirelessGeigerCounter](https://github.com/sawaiz/wirelessGeigerCounter)
(and related [Sawaiz/geigerControl](https://github.com/Sawaiz/geigerControl)) for the
geiger2 clean-sheet. geiger2 is **not** a port of this hardware.

## Lineage

| Generation | MCU | Radio | Tube | HV | Notes |
|---|---|---|---|---|---|
| V6 (2014 boards) | ATtiny2313 SOIC | nRF24L01+ | SBM-20 | MCU Timer0 PWM boost (~400 V open-loop) | Source of truth: `firmware/v6-ble`, `pcb/v6/` |
| V7 CAD | ATtiny2313 QFN | nRF24 | SBM-20 | ICM7555 oscillator | `pcb/schematic.dch` — do not mix with V6 FW |
| Wi-Fi prototype docs | ESP8266/ESP-12F | Wi-Fi | SBM-20 (README) | Schmitt oscillator + Cockcroft–Walton + op-amp vs reference | Maxim AN3757-inspired; never mixed into V6 |
| geigerControl | ESP8266 | Wi-Fi | — | — | Captive portal / OTA / websockets only — **no pulse counting** |

## Lessons to carry into geiger2

1. **Closed-loop HV + readback is a hard requirement.** V6 had no ADC / no tube-voltage telemetry; PWM was open-loop (`OCR0A = 127` ≈ 400 V). geiger2 must regulate and measure HV.
2. **Don’t burn the MCU as the HV clock if you want deep sleep.** Early MCU-PWM HV prevented power-down (PWM stops → HV collapses). Separate HV converter (or a converter that free-runs) so the nRF52 can sleep between counts/ads.
3. **Pulse path.** V6: NPN impulse stage → INT0 falling edge. Count in ISR; report CPM as pulses/60 s. Dead-time correction was never done.
4. **Wireless intent.** Product description for geiger2 is Bluetooth advertising (repo blurb). V6 faked BLE ADV_NONCONN_IND via nRF24; nRF52 does real BLE natively — use SoftDevice/Zephyr BLE, not the nRF24 hack.
5. **Tube change.** Prior art used **SBM-20**. geiger2 uses **CTC-5 / STS-5** (Cyrillic СТС-5) NOS Russian tubes — similar form factor/sensitivity class to SBM-20, verify HV plateau on the bench.

## V6 pin map (reference only)

| Function | ATtiny2313 |
|---|---|
| GM impulse | PD2 / INT0 |
| HV PWM | PB2 / OC0A (~3.91 kHz, ~50% duty) |
| nRF CE/CSN/SCK/MOSI/MISO | PD6 / PD5 / PB0 / PD4 / PB1 |

## Useful links

- Repo: https://github.com/sawaiz/wirelessGeigerCounter
- V6 BLE firmware branch: `firmware/v6-ble`
- V6 CAD: `pcb/v6/` (DipTrace)
- Maxim AN3757 (HV / CW multiplier style used in Wi-Fi-era notes)
