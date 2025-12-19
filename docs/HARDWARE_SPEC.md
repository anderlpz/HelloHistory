# Hardware Specification

## Overview

This document specifies the hardware components needed to convert a vintage rotary phone into an AI-powered conversational experience.

**Design Goals:**
- No soldering required
- All components fit inside phone shell
- Reliable, unattended operation
- Guest-friendly (just pick up the phone)

---

## Core Computing Platform

### Raspberry Pi 5 (8GB RAM)

**Why Pi 5 over Pi 4:**
- 2-3x faster CPU performance
- Better thermal management
- PCIe support for future NVMe upgrade
- Required for reasonable LLM inference speed

**Specifications:**
- Model: Raspberry Pi 5, 8GB RAM
- Storage: 64GB+ microSD (Class A2 recommended)
- Power: USB-C, 27W (5V/5A) official power supply
- Dimensions: 85mm × 56mm × 17mm

**Where to Buy:**
- Official retailers: Adafruit, SparkFun, PiShop.us
- Approximate cost: $80

### Storage

**MicroSD Card Requirements:**
- Capacity: 64GB minimum (128GB recommended)
- Speed: Class A2 (Application Performance Class)
- Endurance: High-endurance preferred for logging

**Space Allocation:**
| Item | Size |
|------|------|
| Raspberry Pi OS | ~4GB |
| Ollama + Models | ~5-15GB |
| Vosk models | ~50MB |
| Piper voices | ~100MB |
| Knowledge base | ~100MB |
| Logs & buffer | ~5GB |
| **Total** | ~25GB used |

### Cooling

The Pi 5 runs hot under LLM inference. Options:

1. **Official Active Cooler** ($5)
   - Small fan + heatsink
   - Best cooling, slight noise

2. **Passive Aluminum Case** ($15-25)
   - Silent operation
   - Adequate for moderate use
   - Preferred for phone installation

3. **Heatsink + Thermal Pad** ($5)
   - Minimum viable cooling
   - May throttle under heavy load

**Recommendation:** Passive aluminum case that can fit in phone body.

---

## Audio System

### Option A: USB All-in-One (Simplest)

**USB Speakerphone/Conference Mic:**
- Contains microphone, speaker, and DAC
- Single USB connection
- Examples: Jabra Speak 410, generic USB speakerphone
- Cost: $30-80

**Pros:** Simple, one device
**Cons:** May not fit in handset, less authentic

### Option B: Separate Components (Recommended)

#### Microphone

**USB Lavalier/Lapel Microphone:**
- Small enough to fit in phone handset
- Good voice capture quality
- Example: BOYA BY-M1 USB, Fifine K053
- Cost: $15-30

**Placement:** Inside the handset mouthpiece area

**Alternative: I2S MEMS Microphone**
- Adafruit I2S MEMS Microphone (SPH0645)
- Requires I2S configuration but cleaner setup
- Cost: $7

#### Audio Output

**USB Audio Adapter (DAC):**
- Converts digital audio to analog
- 3.5mm output to speaker
- Example: Any USB sound card
- Cost: $8-15

**Speaker Options:**

1. **Original Phone Speaker**
   - Most authentic sound
   - May need impedance matching
   - Connect via 3.5mm → speaker wire adapter

2. **Small Replacement Speaker**
   - 2-3" diameter, 8Ω, 2-5W
   - Fits in phone body
   - Clearer audio than original
   - Cost: $5-10

3. **I2S Amplifier + Speaker**
   - Adafruit MAX98357 I2S Amp
   - Direct digital audio, cleaner signal
   - Cost: $8 + speaker

---

## Phone Integration

### Hook Switch Detection

The hook switch is a simple mechanical switch that opens/closes when the handset is lifted/replaced.

**Connection Method (No Solder):**

```
Original Hook Switch
        |
        v
   [Terminal Block] ← Screw terminals, no solder
        |
   [Jumper Wires]
        |
        v
   Raspberry Pi GPIO
```

**GPIO Wiring:**
| Wire | Pi Pin | Function |
|------|--------|----------|
| Switch Wire 1 | GPIO17 (Pin 11) | Input |
| Switch Wire 2 | GND (Pin 6) | Ground |

**Pull-up Resistor:** Use internal pull-up in software (no external resistor needed)

**Terminal Block Specs:**
- 2-position screw terminal
- Accepts 18-22 AWG wire
- Example: WAGO lever nuts or standard barrier strips

### Wiring Diagram

```
ROTARY PHONE INTERNALS
======================

                    +------------------+
                    |   HOOK SWITCH    |
                    |   (existing)     |
                    +--------+---------+
                             |
                    Wire 1   |   Wire 2
                       |     |     |
                       v     |     v
              +--------+     |     +--------+
              |Terminal|     |     |Terminal|
              | Block  |     |     | Block  |
              +---+----+     |     +----+---+
                  |          |          |
             Jumper Wire     |     Jumper Wire
                  |          |          |
                  v          |          v
              +--GPIO17------+-------GND--+
              |                          |
              |     RASPBERRY PI 5       |
              |                          |
              |  USB ← Microphone        |
              |  USB ← Audio DAC         |
              |  USB-C ← Power           |
              +--------------------------+
                           |
                      Audio Out
                           |
                           v
                    +-----------+
                    |  SPEAKER  |
                    | (in phone)|
                    +-----------+
```

### Physical Installation

**Inside Phone Body:**
1. Remove original phone internals (keep hook switch)
2. Mount Raspberry Pi (double-sided tape or standoffs)
3. Route USB cables to microphone and DAC
4. Connect speaker to DAC output
5. Route power cable out back of phone

**Handset:**
1. Open handset (usually 2 screws)
2. Position USB microphone near mouthpiece
3. Optionally replace earpiece speaker
4. Route thin USB cable through cord (or replace cord)

---

## Power System

### Power Requirements

| Component | Current Draw |
|-----------|--------------|
| Raspberry Pi 5 (idle) | ~600mA |
| Raspberry Pi 5 (load) | ~2500mA |
| USB Microphone | ~100mA |
| USB DAC | ~100mA |
| **Peak Total** | ~2700mA |

### Power Supply

**Official Raspberry Pi 5 PSU:**
- 27W USB-C (5.1V, 5A)
- Required for stable operation
- Cost: $12-15

**Alternative: Quality USB-C PD Supply**
- Must support 5V/5A or USB PD
- Cheap supplies may cause instability

**Cable Routing:**
- Power cable exits rear of phone
- Consider right-angle USB-C adapter for space

---

## Complete Bill of Materials

### Essential Components

| # | Item | Qty | Est. Cost |
|---|------|-----|-----------|
| 1 | Raspberry Pi 5 (8GB) | 1 | $80 |
| 2 | 64GB microSD (A2 class) | 1 | $12 |
| 3 | Official Pi 5 Power Supply | 1 | $12 |
| 4 | Passive heatsink/case | 1 | $15 |
| 5 | USB Lavalier Microphone | 1 | $20 |
| 6 | USB Audio Adapter | 1 | $10 |
| 7 | Small 8Ω Speaker (3") | 1 | $8 |
| 8 | Terminal blocks (2-pos) | 2 | $3 |
| 9 | Jumper wires (F-F) | 1 pack | $5 |
| 10 | 3.5mm to bare wire adapter | 1 | $5 |
| | **Subtotal** | | **$170** |

### Optional Enhancements

| # | Item | Purpose | Est. Cost |
|---|------|---------|-----------|
| 11 | I2S MEMS Microphone | Cleaner audio input | $7 |
| 12 | I2S Amplifier (MAX98357) | Better audio output | $8 |
| 13 | Real-time clock module | Keep time without network | $5 |
| 14 | Status LED + resistor | Visual feedback | $2 |
| 15 | USB extension cables | Easier routing | $5 |

### Tools Needed

- Phillips screwdriver (for phone disassembly)
- Wire strippers (if reusing phone wires)
- Double-sided mounting tape
- Electrical tape or heat shrink

---

## Assembly Notes

### No-Solder Connections

All electrical connections can be made without soldering:

1. **Terminal Blocks:** Screw terminals for hook switch wires
2. **Jumper Wires:** Pre-made female-to-female for GPIO
3. **USB Connections:** Standard USB plugs
4. **3.5mm Adapters:** Screw-terminal 3.5mm adapters available

### Fitment Considerations

**Typical Rotary Phone Internal Space:**
- Volume after removing internals: ~1000 cm³
- Raspberry Pi 5 + case: ~150 cm³
- Plenty of room for all components

**Heat Dissipation:**
- Ensure some ventilation (drill small holes if needed)
- Position Pi away from speaker magnets
- Test thermal performance before final assembly

---

## Wiring Reference

### GPIO Pinout (Relevant Pins)

```
Raspberry Pi 5 GPIO Header
==========================

        3.3V  (1) (2)  5V
      GPIO2  (3) (4)  5V
      GPIO3  (5) (6)  GND  ← Hook switch ground
             ...
     GPIO17 (11)(12) GPIO18  ← Hook switch input
             ...
```

### Hook Switch Logic

```python
# GPIO Configuration
HOOK_PIN = 17  # BCM numbering

# When handset is ON HOOK (down): Circuit OPEN → GPIO reads HIGH (pull-up)
# When handset is OFF HOOK (lifted): Circuit CLOSED → GPIO reads LOW

# Detection logic:
# if GPIO.input(HOOK_PIN) == GPIO.LOW:
#     phone_active = True  # Handset lifted
# else:
#     phone_active = False  # Handset down
```

---

## Next Steps

1. Acquire Raspberry Pi 5 and essential components
2. Set up and test Pi without phone integration
3. Disassemble target rotary phone
4. Identify hook switch wires (multimeter test)
5. Prototype audio path
6. Final integration and testing
