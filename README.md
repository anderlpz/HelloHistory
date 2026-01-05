# HelloHistory

A vintage rotary phone transformed into an interactive storytelling experience. When guests pick up the handset, they hear the story of Mary Lund Davis—the pioneering architect who designed the Del Monte house in 1954.

https://github.com/user-attachments/assets/7927c2d3-9882-4693-a5b6-1c07320ca314

## How It Works

1. **Pick up the handset** → Audio starts playing
2. **Listen** → 8 chapters tell Mary's story (~12 minutes)
3. **Hang up** → Audio stops, ready for the next guest

No buttons, no screens, no instructions needed. Just pick up the phone.

---

## About Mary Lund Davis

<img src="docs/images/midcentury-house-exterior-watercolor.jpg" alt="Del Monte House" width="100%">

- First licensed female architect in Washington State after WWII
- Designed the Del Monte house in 1954 as her first home and office
- Founded Monitor Cabinets with her husband George
- Designed over 200 affordable "Fantastic Homes" in the 1960s
- Featured in Architectural Record's "Record Houses of 1964"

---

## Technical Overview

<img src="docs/images/rotary-phone-disassembled-workbench.jpg" alt="HelloHistory rotary phone disassembled" width="100%">

**Hardware:**
- Raspberry Pi Zero 2 W
- USB audio adapter
- Original phone hook switch and earpiece speaker
- Lever nut wire connections (no soldering)

**Software:**
- Python 3 with gpiod for GPIO
- mpg123 for audio playback
- systemd for auto-start on boot

---

## Audio Content

| Track | Chapter | Duration |
|-------|---------|----------|
| 0 | Intro | 0:24 |
| 1 | Welcome to Del Monte | 1:41 |
| 2 | Mary's Early Life | 1:15 |
| 3 | Building the House | 1:44 |
| 4 | The Design Philosophy | 1:49 |
| 5 | Beyond Del Monte | 1:39 |
| 6 | Closing | 0:31 |
| 7 | Bonus Song | 2:32 |

**Total runtime:** ~12 minutes

---

## Project Structure

```
HelloHistory/
├── src/
│   ├── phone_player.py      # Production player (runs on Pi)
│   ├── bench_player.py      # Development player (runs on Mac)
│   └── audio/               # MP3 chapter files
├── deploy/
│   ├── deploy.sh            # Push code to Pi
│   ├── setup-pi.sh          # First-time Pi setup
│   └── setup-service.sh     # Install auto-start service
├── docs/
│   ├── CASE_STUDY.md        # How this was built with Amplifier
│   ├── PROJECT_PLAN.md      # Original project specification
│   └── ...                  # Additional documentation
├── knowledge/
│   ├── mary_biography.md    # Mary's life story
│   └── del_monte_facts.md   # House-specific details
├── scripts/
│   ├── generate_audio.py    # ElevenLabs automation
│   └── chapter_*.md         # Narration scripts
├── hardware/
│   └── SHOPPING_LIST.md     # Bill of materials
└── Makefile                 # Development commands
```

---

## Development Commands

```bash
make test           # Run bench player locally (Mac)
make deploy         # Push code to Pi
make setup-service  # Install auto-start service
make status         # Check if service is running
make logs           # View live logs
make restart        # Restart the service
make ssh            # SSH into Pi
```

---

## Development Status

- [x] Project planning & specifications
- [x] Mary's knowledge base extracted from thesis
- [x] Narration scripts written
- [x] Audio generated with ElevenLabs
- [x] Raspberry Pi setup & deployment tooling
- [x] Hook switch GPIO integration
- [x] Audio routed through original earpiece
- [x] Auto-start service on boot
- [x] Field deployment ready

### Future Enhancements

- [ ] Rotary dial input (select chapters by dialing)
- [ ] Microphone for voice interaction
- [ ] LLM-powered conversation mode

---

## The Property

The phone lives at the Del Monte house, a mid-century modern rental in Washington state. [midcenturypnw](https://linktr.ee/midcenturypnw)

---

## Built With

[Amplifier](https://github.com/microsoft/amplifier) — an open-source AI agent framework from the Research Team at Microsoft. Unlike chat-based AI tools, it can take actions: write files, run commands, deploy code, debug in real-time.

See [docs/CASE_STUDY.md](docs/CASE_STUDY.md) for the full story of how this was built.

---

## License

MIT

---

*Disclosure: I'm a member of the Amplifier team at Microsoft.*
