# V1 Hardware Shopping List

Last updated: 2025-12-20

## Overview

Complete parts list for the HelloHistory V1 audio player - converting an ITT 500 rotary phone into a standalone audio player that tells the story of Mary Lund Davis.

---

## Components

### Core Electronics

| Item | Purpose | Price | Link | Notes |
|------|---------|-------|------|-------|
| Raspberry Pi Zero 2 WH | Main compute unit | $19.80 | [Adafruit #6008](https://www.adafruit.com/product/6008) | Must have pre-soldered headers (WH version) |
| CanaKit 5V 2.5A Power Supply | Power for Pi | $9.95 | [Amazon B00MARDJZ4](https://www.amazon.com/dp/B00MARDJZ4) | Micro-USB, UL listed, 5ft cable |
| SanDisk 32GB MicroSD (A1) | OS and audio storage | $8.49 | [Amazon B08GY9NYRM](https://www.amazon.com/dp/B08GY9NYRM) | A1 rated for app performance |

### Audio

| Item | Purpose | Price | Link | Notes |
|------|---------|-------|------|-------|
| UGREEN USB Audio Adapter | Audio output from Pi | $13.99 | [Amazon B01N905VOY](https://www.amazon.com/dp/B01N905VOY) | Dual 3.5mm jacks, works with Raspberry Pi |
| MakerHawk Speaker 3W 8Ohm (2-pack) | Handset earpiece speaker | $10.99 | [Amazon B07FTB281F](https://www.amazon.com/dp/B07FTB281F) | 31x28x15mm - trim mounting tabs to fit in earpiece |

### Wiring & Connections

| Item | Purpose | Price | Link | Notes |
|------|---------|-------|------|-------|
| EDGELEC Jumper Wires 120pcs (30cm) | GPIO connections | $6.98 | [Amazon B07GD2BWPY](https://www.amazon.com/dp/B07GD2BWPY) | Select "11.8 inch (30cm)" size. Includes M-M, M-F, F-F |
| Amazon Basics 3.5mm Audio Cable 4ft | Connect DAC to phone wires | $6.70 | [Amazon B00NO73MUQ](https://www.amazon.com/dp/B00NO73MUQ) | Will be cut and spliced to phone cord wires |
| Wago 221 Lever Nuts (assorted) | No-solder wire connections | ~$12 | Search "Wago 221 lever nuts" on Amazon | For splicing audio and phone wires without soldering |

---

## Cost Summary

| Category | Subtotal |
|----------|----------|
| Core Electronics | $38.24 |
| Audio | $24.98 |
| Wiring & Connections | ~$25.68 |
| **Total** | **~$89** |

---

## Speaker Installation Notes

The MakerHawk speaker (31x28x15mm body) fits inside the ITT 500 handset earpiece cavity (~40-45mm diameter, 20-25mm deep):

1. **Trim the mounting tabs** - The speaker has tabs extending ~14mm on each side. Snip them off with wire cutters.
2. **Secure with foam/putty** - Use foam padding or mounting putty to hold the speaker in place.
3. **Route wires** - Thread speaker wires down through the handset handle to the coiled cord.

---

## Wiring Diagram

```
BASE UNIT (Pi location)                    HANDSET
============================              ==========
                                          
Pi Zero 2 W                               MakerHawk
    |                                     Speaker
    | USB                                    ^
    v                                        |
USB Audio ──> 3.5mm ──> Wago ──> Phone Cord ─┘
Adapter              splice   (reuse earpiece wires)

GPIO 17 ◄──── Wago ◄──── Hook Switch
GPIO 27 ◄──── Wago ◄──── Rotary Dial Pulse
```

The existing phone cord has 4 wires:
- 2 wires for earpiece (reuse for new speaker)
- 2 wires for microphone (unused in V1)

---

## Ordering Checklist

- [ ] Raspberry Pi Zero 2 WH (Adafruit)
- [ ] CanaKit Power Supply (Amazon)
- [ ] SanDisk 32GB MicroSD (Amazon)
- [ ] UGREEN USB Audio Adapter (Amazon)
- [ ] MakerHawk Speaker 2-pack (Amazon)
- [ ] EDGELEC Jumper Wires 30cm (Amazon)
- [ ] Amazon Basics 3.5mm Cable (Amazon)
- [ ] Wago 221 Lever Nuts (Amazon)

---

## Tools Needed (not included)

- Wire cutters/strippers
- Small Phillips screwdriver (for opening phone)
- Multimeter (optional, for testing connections)
