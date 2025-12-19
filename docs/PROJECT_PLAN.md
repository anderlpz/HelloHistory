# HelloHistory: Talk to Mary Lund Davis

## Project Vision

Transform a vintage rotary phone into an interactive experience where guests at the Del Monte rental property can "speak with" Mary Lund Davis, the pioneering architect who designed and built the home in 1954.

When a guest picks up the phone, they hear Mary's voice and can ask questions about:
- Her life and career as the first licensed female architect in Washington State after WWII
- The design philosophy behind Del Monte (her "finest building")
- Pacific Northwest modernism and her contributions
- Her Danish heritage and family history
- Her other works (Fantastic Homes, Monitor Cabinets, etc.)

---

## Critical Hardware Decision: Why NOT Arduino

**Arduino cannot work for this project.** Here's why:

| Requirement | Arduino | Raspberry Pi 5 |
|-------------|---------|----------------|
| Run LLM inference | No | Yes (Ollama + small models) |
| Speech-to-Text | No | Yes (Vosk) |
| Text-to-Speech | No (only basic tones) | Yes (Piper TTS) |
| Audio I/O | Limited (no native support) | Full support (USB/I2S) |
| RAM | 2KB-256KB | 4-8GB |
| Storage | KB-MB | 32GB+ microSD |
| WiFi/Ethernet | Add-on shields | Built-in |
| Python support | No | Yes |

**The Raspberry Pi 5 (8GB) is the only viable option** for running local LLMs, speech recognition, and natural voice synthesis.

---

## System Architecture

```
                    ROTARY PHONE SHELL
                          |
            +-------------+-------------+
            |                           |
     [Hook Switch]              [Original Speaker]
     (GPIO trigger)              (or replacement)
            |                           |
            v                           ^
    +-------+-------+           +-------+-------+
    |  Raspberry Pi |           | Audio Output  |
    |      5        |---------->| (USB DAC or   |
    |   (8GB RAM)   |           |  I2S amp)     |
    +-------+-------+           +---------------+
            |
            v
    +-------+-------+
    | USB Microphone|
    | (in handset)  |
    +---------------+

SOFTWARE PIPELINE:
==================

1. WAKE: Hook switch lifted → GPIO triggers start
2. GREETING: Play Mary's greeting audio
3. LISTEN: Vosk STT captures guest speech
4. THINK: Ollama + LLM generates Mary's response
5. SPEAK: Piper TTS synthesizes Mary's voice
6. PLAY: Audio plays through phone speaker
7. LOOP: Back to LISTEN until hook replaced
8. SLEEP: Hook replaced → system returns to idle
```

---

## Software Components

### 1. Speech-to-Text: Vosk
- Offline speech recognition
- Fast, lightweight
- Works on Raspberry Pi
- Free, open source

### 2. LLM: Ollama with Small Model
- **Recommended models:**
  - `gemma2:2b` - Good balance of quality/speed
  - `qwen2.5:3b` - Slightly larger, better responses
  - `phi3:mini` - Microsoft's small model
- System prompt will contain Mary's personality, history, and knowledge
- RAG (Retrieval Augmented Generation) for detailed historical facts

### 3. Text-to-Speech: Piper TTS
- Offline, fast synthesis
- Multiple voice options
- Can potentially fine-tune a custom "Mary" voice
- Natural sounding output

### 4. Hook Detection: GPIO
- Simple circuit: hook switch connects to GPIO pin
- When lifted: pin goes HIGH (or LOW depending on wiring)
- Python monitors GPIO state

### 5. Audio I/O
- **Input:** USB lavalier/miniature microphone (fits in handset)
- **Output:** USB audio adapter + small speaker (or original phone speaker)

---

## Hardware Bill of Materials (No-Solder Options)

### Core Computing
| Item | Purpose | Est. Cost | Link Type |
|------|---------|-----------|-----------|
| Raspberry Pi 5 (8GB) | Main computer | $80 | Official retailer |
| 64GB microSD card | OS + models | $15 | Any Class 10+ |
| USB-C Power Supply (27W) | Power | $15 | Official RPi PSU |
| Passive cooler or case | Thermal | $10-20 | Fits inside phone |

### Audio (No Solder)
| Item | Purpose | Est. Cost |
|------|---------|-----------|
| USB lavalier microphone | Voice capture | $15-30 |
| USB audio adapter (DAC) | Audio output | $10-20 |
| Small 8Ω speaker (2-3") | Audio playback | $5-10 |
| OR: USB speakerphone | All-in-one audio | $30-50 |

### Phone Integration (No Solder)
| Item | Purpose | Est. Cost |
|------|---------|-----------|
| Jumper wires (F-F) | GPIO connections | $5 |
| Hook switch (if original broken) | Wake detection | $5-10 |
| Terminal blocks | Wire connections | $5 |

### Optional Enhancements
| Item | Purpose | Est. Cost |
|------|---------|-----------|
| I2S audio amplifier (Adafruit MAX98357) | Better audio | $8 |
| Real-time clock module | Time keeping | $5 |
| Status LED | Visual feedback | $2 |

**Estimated Total: $150-200** (excluding the rotary phone)

---

## No-Solder Wiring Approach

### Hook Switch Connection
The rotary phone's hook switch can be connected using:
1. **Terminal blocks** - Screw-in connections
2. **Lever nuts (Wago)** - Push-in connectors
3. **Alligator clips** (for prototyping)

```
Hook Switch Wires → Terminal Block → Jumper Wires → GPIO Header

GPIO Setup:
- Pin 17 (GPIO17): Hook switch input
- Pin 1 (3.3V): Power for pull-up
- Pin 6 (GND): Ground reference
```

### Audio Connections
- USB microphone → USB port on Pi
- USB DAC → USB port on Pi → 3.5mm to speaker

---

## Mary Lund Davis: Character Profile

Based on the thesis by her grandson Nevis Charles Granum, here's Mary's character:

### Biographical Facts
- Born: February 13, 1922, Sacramento (lucky number: 13)
- Parents: Anders and Freida Lund (Danish immigrants from Bredebro)
- Education: UC architecture, University of Washington 1941-1945
- Married: George Davis, May 26, 1950
- Children: Kit (1956), Gail
- Passed: 2008

### Personality Traits
- **Confident pioneer:** "My father always told me I could do anything a man could do"
- **Practical visionary:** "All low-cost housing does not have to be cheap"
- **Wit and charm:** Smoked from long cigarette holders, drank Grey Goose from Marimekko teacups
- **Action-oriented:** "We were going to set the world on fire in architecture"
- **Nature lover:** Collected 180 Japanese maples, designed gardens

### Voice & Speaking Style
- Direct, confident
- References her Danish heritage
- Uses architectural terms naturally
- Warm but not overly sentimental
- Occasionally quotes or paraphrases Frank Lloyd Wright
- Pride in craftsmanship and affordability

### Key Topics She'd Discuss
1. **Del Monte (this house)**
   - Built 1954, her first home and office
   - "Skin and bones" architecture
   - Light timber frame wrapped in plywood skin
   - Indoor/outdoor living, clerestory windows
   - Monitor Cabinets throughout
   - "My finest building"

2. **Design Philosophy**
   - Pacific Northwest modernism
   - Affordable doesn't mean cheap
   - Connection to nature
   - "The human spirit is best when not boxed in"
   - Practical, livable spaces

3. **Career**
   - First licensed female architect in WA after WWII
   - Monitor Cabinets with George
   - Fantastic Homes (200+ affordable homes)
   - Featured in Architectural Record 1964
   - AIA awards

4. **Family & Heritage**
   - Danish roots, grew up speaking Danish
   - Father taught her to build, sail, shoot
   - Sailing champion (Adam's Cup)
   - The purple horse story

---

## Development Phases

### Phase 1: Proof of Concept (Desktop)
- [ ] Set up voice assistant pipeline on Mac/Linux
- [ ] Create Mary's system prompt and test responses
- [ ] Test STT → LLM → TTS flow
- [ ] Refine character voice and knowledge

### Phase 2: Raspberry Pi Port
- [ ] Install Raspberry Pi OS
- [ ] Install Ollama, Vosk, Piper
- [ ] Port and test voice pipeline
- [ ] Optimize for latency

### Phase 3: Phone Integration
- [ ] Disassemble rotary phone
- [ ] Identify hook switch mechanism
- [ ] Connect GPIO for hook detection
- [ ] Install microphone in handset
- [ ] Install speaker (original or replacement)
- [ ] Test full integration

### Phase 4: Knowledge Enhancement
- [ ] Extract key facts from thesis PDF
- [ ] Create structured knowledge base
- [ ] Implement RAG for detailed questions
- [ ] Test historical accuracy

### Phase 5: Polish & Deploy
- [ ] Optimize boot time (auto-start)
- [ ] Add error recovery
- [ ] Create setup documentation
- [ ] Install at Del Monte property

---

## Files & Directory Structure

```
HelloHistory/
├── .amplifier/
│   └── AGENTS.md
├── docs/
│   ├── PROJECT_PLAN.md          # This file
│   ├── HARDWARE_SPEC.md         # Detailed hardware guide
│   └── SOFTWARE_SPEC.md         # Software architecture
├── src/
│   ├── mary_assistant.py        # Main voice assistant
│   ├── hook_detector.py         # GPIO hook switch handler
│   ├── audio_manager.py         # Audio I/O management
│   └── config.json              # Configuration
├── knowledge/
│   ├── mary_biography.md        # Extracted biography
│   ├── del_monte_facts.md       # House-specific knowledge
│   └── system_prompt.md         # LLM system prompt
├── hardware/
│   └── wiring_diagram.md        # Connection guide
└── README.md
```

---

## Next Steps

1. **Create detailed specifications** (hardware & software docs)
2. **Extract Mary's knowledge** from thesis into structured format
3. **Prototype voice pipeline** on development machine
4. **Order hardware** once specs are finalized
5. **Begin integration** once hardware arrives

---

## Contribution Opportunities for Amplifier

As we build this, we may create reusable components:

- **tool-gpio**: GPIO control tool for Raspberry Pi projects
- **tool-audio**: Audio capture/playback tool
- **agent-character**: Character-based conversational agent template
- **profile-embedded**: Profile optimized for embedded/Pi deployments
- **hook-voice-activity**: Hook for voice activity detection

These could be contributed back to the Amplifier ecosystem.
