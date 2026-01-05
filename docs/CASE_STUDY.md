# HelloHistory Case Study: Building a Hardware Project with Amplifier

## From Idea to Finished Product in Days, Not Months

**Project:** HelloHistory - A vintage rotary phone that plays narrated stories about architect Mary Lund Davis when guests lift the handset.

**Built with:** Amplifier by Microsoft

**Timeline:** ~2 weeks from concept to working prototype

---

## The Vision

Transform a 1960s rotary phone into an interactive storytelling experience for guests at a short-term rental property. When visitors pick up the phone, they hear the story of Mary Lund Davis—the pioneering architect who designed the house in 1954.

**The challenge:** Build a complete hardware-software product with no prior Raspberry Pi experience, integrating:
- GPIO hardware detection
- Audio playback through original phone components
- Auto-start services
- Remote deployment and management

---

## What Amplifier Enabled

### 1. Rapid Research & Planning

Amplifier helped research and document:
- Hardware requirements (why Raspberry Pi, not Arduino)
- Complete bill of materials with verified links
- Software architecture decisions
- Mary Lund Davis biography extracted from academic thesis

**Artifacts produced:**
- `docs/PROJECT_PLAN.md` - Comprehensive project specification
- `docs/HARDWARE_SPEC.md` - Hardware components and wiring
- `docs/SOFTWARE_SPEC.md` - Software architecture
- `knowledge/mary_biography.md` - Extracted biography
- `hardware/SHOPPING_LIST.md` - Verified purchase links

### 2. Content Creation Pipeline

Amplifier helped create the narrative content:
- Wrote 7 chapter scripts in a warm narrator style
- Created voice prompts for ElevenLabs
- Built audio generation tooling
- Split full recordings into chapter files

**Artifacts produced:**
- `scripts/chapter_*.md` - Narration scripts
- `scripts/generate_audio.py` - ElevenLabs automation
- `scripts/audio_config.yaml` - Voice and chapter configuration
- `src/audio/*.mp3` - 8 audio tracks (intro + 6 chapters + song)

### 3. Development Workflow

Amplifier created a complete development environment:
- Bench testing player for Mac development
- Makefile with 15+ commands for common tasks
- Deployment scripts for Raspberry Pi
- Service management tooling

**Key commands:**
```bash
make test          # Run local bench player
make deploy        # Push to Pi
make setup-service # Install auto-start
make logs          # View Pi logs
make ssh           # Connect to Pi
```

### 4. Real-Time Hardware Debugging

The most impressive use of Amplifier was live hardware integration:

**Hook Switch Wiring:**
- Guided through identifying 7 wires from the hook switch
- Created GPIO test scripts on the fly
- Debugged wiring issues in real-time
- Found correct wire pair through systematic testing

**Audio Routing:**
- Connected USB audio adapter
- Wired audio to original earpiece speaker
- Troubleshot ALSA configuration issues
- Set up persistent volume control

**The AI wrote and deployed code to the Pi in real-time during hardware testing.**

### 5. Production Deployment

Amplifier created production-ready infrastructure:
- `phone_player.py` - Production player with logging
- `setup-service.sh` - Systemd service installer
- Auto-start on boot
- Configurable volume control
- Error recovery and restart logic

---

## Project Timeline

| Phase | Duration | What Happened |
|-------|----------|---------------|
| Research & Planning | Day 1-2 | Project specs, hardware decisions, knowledge extraction |
| Content Creation | Day 3-5 | Scripts, voice prompts, audio generation |
| Dev Tooling | Day 6-7 | Bench player, Makefile, deployment scripts |
| Pi Setup | Day 8 | OS flash, network config, initial deployment |
| Hardware Integration | Day 9-10 | GPIO wiring, audio routing, hook switch debugging |
| Production | Day 10 | Auto-start service, final testing |

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ROTARY PHONE                         │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ Hook Switch │    │  Earpiece   │    │   (Future)  │ │
│  │ Gray+Yellow │    │   Speaker   │    │ Rotary Dial │ │
│  └──────┬──────┘    └──────┬──────┘    └─────────────┘ │
│         │                  │                            │
└─────────┼──────────────────┼────────────────────────────┘
          │                  │
          ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│              RASPBERRY PI ZERO 2 W                      │
│                                                         │
│  GPIO 17 ◄─── Hook detect      USB Audio ───► 3.5mm    │
│  GND     ◄─── Ground           Adapter   ───► Speaker  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ phone_player.py (systemd service)               │   │
│  │                                                  │   │
│  │ • Monitors GPIO for handset lift/hangup         │   │
│  │ • Plays chapter audio via mpg123                │   │
│  │ • Auto-advances through playlist                │   │
│  │ • Logs to /home/pi/delmonte/logs/phone.log     │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Files Created

```
HelloHistory/
├── .amplifier/AGENTS.md          # Project-specific AI instructions
├── Makefile                       # 15+ development commands
├── README.md                      # Project overview
│
├── docs/
│   ├── PROJECT_PLAN.md           # Comprehensive spec
│   ├── HARDWARE_SPEC.md          # Hardware guide
│   ├── SOFTWARE_SPEC.md          # Software architecture
│   ├── BENCH_TESTING_GUIDE.md    # Local testing guide
│   ├── PI_DEVELOPMENT_WORKFLOW.md # Pi deployment guide
│   ├── AUDIO_WORKFLOW.md         # Audio generation guide
│   └── PHASES.md                 # Phased implementation
│
├── deploy/
│   ├── deploy.sh                 # Deployment script
│   ├── setup-pi.sh               # First-time Pi setup
│   └── setup-service.sh          # Systemd service installer
│
├── hardware/
│   └── SHOPPING_LIST.md          # BOM with links
│
├── knowledge/
│   ├── mary_biography.md         # Extracted biography
│   ├── del_monte_facts.md        # House details
│   └── system_prompt.md          # AI character prompt
│
├── scripts/
│   ├── chapter_*.md              # Narration scripts
│   ├── generate_audio.py         # ElevenLabs automation
│   └── audio_config.yaml         # Voice configuration
│
└── src/
    ├── bench_player.py           # Mac testing player
    ├── phone_player.py           # Production Pi player
    └── audio/
        ├── 00_intro.mp3
        ├── 01_welcome.mp3
        ├── 02_marys_story.mp3
        ├── 03_building.mp3
        ├── 04_design.mp3
        ├── 05_other_work.mp3
        ├── 06_closing.mp3
        └── 07_song.mp3
```

---

## Key Learnings

### What Worked Well

1. **Real-time hardware debugging** - Having AI write and deploy test scripts while physically probing wires was incredibly powerful.

2. **Incremental development** - Starting with Mac bench testing before Pi deployment caught issues early.

3. **Documentation as you go** - Amplifier created docs alongside code, not as an afterthought.

4. **Systematic troubleshooting** - When hook switch wiring was wrong, Amplifier guided systematic testing of all 7 wires to find the correct pair.

### Challenges Overcome

1. **ALSA audio configuration** - Required debugging card numbering and config files
2. **gpiod API changes** - Python library had breaking changes between versions
3. **Heredoc paste issues** - SSH terminal mangled multi-line pastes
4. **Hook switch polarity** - Logic was inverted, fixed with one-line code change

---

## The Result

A standalone, production-ready device that:
- ✅ Starts automatically when powered on
- ✅ Plays audio when handset is lifted
- ✅ Stops when handset is replaced
- ✅ Uses original phone speaker
- ✅ Requires no network to operate
- ✅ Can be updated remotely when on Wi-Fi

**Total development time with Amplifier: ~2 weeks**
**Estimated time without AI assistance: 2-3 months**

---

## Conclusion

This project demonstrates Amplifier's strength in:

1. **Cross-domain work** - Research, writing, coding, hardware, deployment
2. **Real-time collaboration** - Debugging hardware while AI writes code
3. **Complete solutions** - Not just code, but docs, tooling, and deployment
4. **Learning acceleration** - First-time Pi user to working product

The vintage phone now tells Mary's story to every guest who picks it up—a fitting tribute built with modern AI assistance.
