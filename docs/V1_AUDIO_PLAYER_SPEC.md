# V1 Specification: Rotary Phone Audio Player

## Overview

V1 transforms the ITT 500 rotary phone into a standalone audio player that tells the story of Mary Lund Davis and Del Monte. Guests pick up the handset to hear the narration, and use the rotary dial to skip to specific chapters.

**This is NOT the AI conversation version** - that's a future enhancement. V1 is a pre-recorded audio experience with chapter navigation.

---

## User Experience

### Basic Flow

```
Guest picks up phone
        │
        ▼
┌───────────────────┐
│ Intro plays       │ "Vagabond Hospitality presents..."
│ (~20 seconds)     │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Chapter 1 starts  │ Welcome to Del Monte
│ automatically     │
└────────┬──────────┘
         │
    Continues through all chapters...
         │
         ▼
┌───────────────────┐
│ Chapter 6: Closing│ "Goodbye for now"
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Song plays        │ (optional, if guest stays on line)
└────────┬──────────┘
         │
    Guest hangs up (or loop back to intro?)
```

### Rotary Dial Navigation

| Dial | Action |
|------|--------|
| **1** | Jump to Chapter 1: Welcome to Del Monte |
| **2** | Jump to Chapter 2: Mary's Story |
| **3** | Jump to Chapter 3: Building Del Monte |
| **4** | Jump to Chapter 4: The Design Philosophy |
| **5** | Jump to Chapter 5: Her Other Work |
| **6** | Jump to Chapter 6: Closing |
| **0** | Restart from beginning (Intro) |
| **7-9** | Reserved / No action |

### Behavior Details

- **Picking up phone:** Starts playback from intro (or resumes if within timeout?)
- **Dialing during playback:** Immediately stops current audio, jumps to selected chapter
- **Hanging up:** Stops playback, resets state
- **Picking up again:** Starts fresh from intro

---

## Hardware Requirements

### Components (Minimal V1 Build)

| Component | Purpose | Est. Cost |
|-----------|---------|-----------|
| Raspberry Pi Zero 2 W | Compute (Pi 5 overkill for audio playback) | $15 |
| 32GB microSD (A1) | Storage | $8 |
| USB Audio Adapter | Audio output | $10 |
| Small speaker (8Ω 2W) | Handset audio | $5 |
| Jumper wires | GPIO connections | $3 |
| USB power supply | Power | $10 |
| **Total** | | **~$51** |

**Note:** Pi Zero 2 W is sufficient for V1 (audio playback only). Upgrade to Pi 5 for V2 (AI conversation).

### GPIO Connections

```
ITT 500 Phone                    Raspberry Pi
─────────────                    ─────────────
Hook Switch ──────────────────── GPIO 17 + GND
Rotary Dial Pulse ────────────── GPIO 27 + GND
(Optional) Dial "in motion" ──── GPIO 22 + GND
```

### Audio Path

```
Pi USB ──► USB DAC ──► 3.5mm ──► Amplifier (optional) ──► Handset Speaker
```

**Handset Speaker Options:**
1. **Reuse original earpiece** - Most authentic, may need small amp
2. **Replace with modern speaker** - Clearer audio, easier wiring
3. **Bone conduction transducer** - Unique feel, premium option

---

## Audio Files

### Structure

```
audio/
├── 00_intro.mp3          # Vagabond Hospitality presents... (~20s)
├── 01_welcome.mp3        # Chapter 1: Welcome to Del Monte (~2 min)
├── 02_marys_story.mp3    # Chapter 2: Mary's Story (~2.5 min)
├── 03_building.mp3       # Chapter 3: Building Del Monte (~2.5 min)
├── 04_design.mp3         # Chapter 4: The Design Philosophy (~2 min)
├── 05_other_work.mp3     # Chapter 5: Her Other Work (~2 min)
├── 06_closing.mp3        # Chapter 6: Closing (~1.5 min)
└── 07_song.mp3           # Bonus: Suno-composed song (~3 min?)
```

### Audio Preparation

The existing full MP3 (`src/DelMonte-121925-2304.mp3`, ~14 min) needs to be split.

**Option A: Manual split with Audacity**
- Import MP3
- Mark chapter boundaries
- Export each section

**Option B: FFmpeg with timestamps**
```bash
# Example (timestamps TBD from actual audio)
ffmpeg -i DelMonte-121925-2304.mp3 -ss 00:00:00 -to 00:00:20 -c copy audio/00_intro.mp3
ffmpeg -i DelMonte-121925-2304.mp3 -ss 00:00:20 -to 00:02:15 -c copy audio/01_welcome.mp3
# ... etc
```

**Audio Format:**
- Format: MP3 (or WAV for lower latency)
- Sample rate: 44.1kHz or 22.05kHz
- Bit depth: 16-bit
- Channels: Mono (handset is single speaker)

---

## Software Architecture

### Technology Stack

| Component | Technology | Why |
|-----------|------------|-----|
| OS | Raspberry Pi OS Lite (32-bit) | Minimal, fast boot |
| Runtime | Python 3.11 | Simple, well-supported |
| Audio | pygame.mixer or simpleaudio | Reliable MP3 playback |
| GPIO | gpiozero | Clean, simple API |

### State Machine

```
                    ┌──────────────┐
          ┌────────►│    IDLE      │◄─────────────┐
          │         │  (on-hook)   │              │
          │         └──────┬───────┘              │
          │                │                      │
          │         Hook lifted                   │
          │                │                 Hook replaced
          │                ▼                      │
          │         ┌──────────────┐              │
          │         │   PLAYING    │──────────────┤
          │         │  (off-hook)  │              │
          │         └──────┬───────┘              │
          │                │                      │
          │         Dial detected                 │
          │                │                      │
          │                ▼                      │
          │         ┌──────────────┐              │
          └─────────│   JUMPING    │──────────────┘
                    │ (switching)  │
                    └──────────────┘
```

### Core Module: `phone_player.py`

```python
"""
Del Monte Rotary Phone Audio Player - V1
"""
import time
from pathlib import Path
from enum import Enum, auto
from gpiozero import Button
import pygame

class State(Enum):
    IDLE = auto()      # Phone on hook, waiting
    PLAYING = auto()   # Phone off hook, audio playing
    JUMPING = auto()   # Switching chapters

class PhonePlayer:
    def __init__(self, audio_dir: Path):
        self.audio_dir = audio_dir
        self.state = State.IDLE
        self.current_track = 0
        
        # Track list in playback order
        self.tracks = [
            "00_intro.mp3",
            "01_welcome.mp3",
            "02_marys_story.mp3",
            "03_building.mp3",
            "04_design.mp3",
            "05_other_work.mp3",
            "06_closing.mp3",
            "07_song.mp3",
        ]
        
        # GPIO setup
        self.hook = Button(17, pull_up=True, bounce_time=0.1)
        self.dial_pulse = Button(27, pull_up=True, bounce_time=0.05)
        
        # Dial state
        self.pulse_count = 0
        self.last_pulse_time = 0
        self.dial_timeout = 0.2  # seconds between pulses
        
        # Audio setup
        pygame.mixer.init()
        
        # Wire up events
        self.hook.when_pressed = self.on_hang_up
        self.hook.when_released = self.on_pick_up
        self.dial_pulse.when_pressed = self.on_dial_pulse
    
    def on_pick_up(self):
        """Handset lifted - start playing"""
        if self.state == State.IDLE:
            self.state = State.PLAYING
            self.current_track = 0
            self.play_current()
    
    def on_hang_up(self):
        """Handset replaced - stop everything"""
        pygame.mixer.music.stop()
        self.state = State.IDLE
        self.current_track = 0
        self.pulse_count = 0
    
    def on_dial_pulse(self):
        """Rotary dial pulse detected"""
        if self.state != State.PLAYING:
            return
        
        self.pulse_count += 1
        self.last_pulse_time = time.time()
    
    def check_dial_complete(self):
        """Check if dial has finished rotating (no pulses for timeout)"""
        if self.pulse_count == 0:
            return
        
        if time.time() - self.last_pulse_time > self.dial_timeout:
            # Dial complete - interpret number
            dialed = self.pulse_count if self.pulse_count < 10 else 0
            self.pulse_count = 0
            self.jump_to_chapter(dialed)
    
    def jump_to_chapter(self, number: int):
        """Jump to chapter by dialed number"""
        # Map dial number to track index
        # 0 = restart (track 0), 1-6 = chapters (tracks 1-6)
        if number == 0:
            target = 0  # Intro
        elif 1 <= number <= 6:
            target = number  # Direct mapping
        else:
            return  # Invalid, ignore
        
        pygame.mixer.music.stop()
        self.current_track = target
        self.play_current()
    
    def play_current(self):
        """Play the current track"""
        if self.current_track >= len(self.tracks):
            # End of playlist - could loop or stop
            self.current_track = 0  # Loop back
        
        track_path = self.audio_dir / self.tracks[self.current_track]
        if track_path.exists():
            pygame.mixer.music.load(str(track_path))
            pygame.mixer.music.play()
    
    def check_track_ended(self):
        """Check if current track finished, advance to next"""
        if self.state == State.PLAYING and not pygame.mixer.music.get_busy():
            self.current_track += 1
            self.play_current()
    
    def run(self):
        """Main loop"""
        print("Del Monte Phone Player started. Waiting for pickup...")
        try:
            while True:
                self.check_dial_complete()
                self.check_track_ended()
                time.sleep(0.05)  # 50ms poll interval
        except KeyboardInterrupt:
            print("\nShutting down...")
            pygame.mixer.quit()

if __name__ == "__main__":
    player = PhonePlayer(Path("audio"))
    player.run()
```

### Directory Structure

```
/home/pi/delmonte/
├── phone_player.py       # Main application
├── config.py             # Configuration (GPIO pins, paths)
├── audio/
│   ├── 00_intro.mp3
│   ├── 01_welcome.mp3
│   ├── 02_marys_story.mp3
│   ├── 03_building.mp3
│   ├── 04_design.mp3
│   ├── 05_other_work.mp3
│   ├── 06_closing.mp3
│   └── 07_song.mp3
└── logs/
    └── player.log
```

---

## Installation

### 1. Flash Raspberry Pi OS

```bash
# Use Raspberry Pi Imager
# Select: Raspberry Pi OS Lite (32-bit)
# Configure: WiFi, SSH, hostname=delmonte
```

### 2. Initial Setup

```bash
ssh pi@delmonte.local

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-pygame git

# Create project directory
mkdir -p ~/delmonte/audio ~/delmonte/logs
```

### 3. Copy Files

```bash
# From your development machine
scp phone_player.py pi@delmonte.local:~/delmonte/
scp audio/*.mp3 pi@delmonte.local:~/delmonte/audio/
```

### 4. Test

```bash
# SSH in and run
cd ~/delmonte
python3 phone_player.py
```

### 5. Auto-Start Service

Create `/etc/systemd/system/delmonte.service`:

```ini
[Unit]
Description=Del Monte Phone Player
After=sound.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/delmonte
ExecStart=/usr/bin/python3 phone_player.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable delmonte
sudo systemctl start delmonte
```

---

## Testing Plan

### Phase 1: Desktop Testing (No Phone)

1. Test audio playback with pygame
2. Simulate GPIO inputs with keyboard
3. Verify state machine logic

### Phase 2: Breadboard Testing

1. Wire momentary buttons to GPIO
2. Button 1 = hook switch
3. Button 2 = dial pulses (tap rapidly)
4. Test with headphones on 3.5mm

### Phase 3: Phone Integration

1. Open ITT 500, identify hook switch wires
2. Connect to GPIO via terminal blocks
3. Test hook detection
4. Identify dial pulse wires
5. Test dial detection
6. Connect speaker, test audio

### Phase 4: Field Testing

1. Full run-through of all chapters
2. Rapid dial switching
3. Hang up mid-chapter
4. Multiple pickup/hangup cycles
5. 24-hour stability test

---

## Open Questions

1. **Song file:** Is there a separate song MP3, or should it be generated?
2. **Loop behavior:** After closing, should it loop back to intro or stop?
3. **Volume control:** Fixed volume or adjustable? (Original phones had ringer volume)
4. **Timeout:** If left off-hook for 30+ min with no interaction, hang up tone?
5. **Visual indicator:** Add LED to show system is ready? (Subtle, maybe inside phone)

---

## Future Enhancements (V2+)

- **AI Conversation Mode:** Switch to Vosk + Ollama + Piper for interactive Q&A
- **Visitor Analytics:** Log which chapters are most popular
- **Remote Updates:** Pull new audio files via WiFi
- **Multiple Languages:** Danish greeting option (honoring Mary's heritage)
- **Ringer Activation:** Ring the bell on special occasions

---

## Timeline Estimate

| Phase | Tasks | Duration |
|-------|-------|----------|
| Audio prep | Split MP3, normalize levels | 1-2 hours |
| Software dev | Write & test phone_player.py | 2-3 hours |
| Hardware setup | Wire Pi, test GPIO | 2-3 hours |
| Phone integration | Open phone, connect, test | 3-4 hours |
| Polish & deploy | Service setup, final testing | 2-3 hours |
| **Total** | | **~12-15 hours** |

---

## References

- [gpiozero documentation](https://gpiozero.readthedocs.io/)
- [pygame.mixer documentation](https://www.pygame.org/docs/ref/mixer.html)
- [Rotary dial pulse detection](https://hackaday.io/project/165208/logs)
- ITT 500 hook switch research (see earlier conversation)
