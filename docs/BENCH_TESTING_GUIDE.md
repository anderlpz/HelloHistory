# Bench Testing Guide: HelloHistory V1

**Goal:** Get the audio player working on a desk/bench before integrating into the ITT 500 phone.

---

## Overview

This guide covers setting up and testing all hardware externally:
- Raspberry Pi Zero 2 WH setup
- USB audio adapter configuration
- Speaker output testing
- Software testing with keyboard/button controls (simulating hook switch)

**What we're skipping for now:**
- Hook switch detection (no phone)
- Rotary dial pulse counting (no phone)
- Phone housing integration

---

## Hardware for Bench Testing

| Item | Purpose | Status |
|------|---------|--------|
| Raspberry Pi Zero 2 WH kit | Compute | ✅ Received |
| CanaKit 5V 2.5A Power Supply | Power | ✅ Received |
| 32GB MicroSD (from kit) | Storage | ✅ Received (needs reflash) |
| UGREEN USB Audio Adapter | Audio out | ✅ Received |
| MakerHawk Speaker 3W 8Ω | Audio playback | ✅ Received |
| 3.5mm audio cable | Connect DAC to speaker | ✅ Received |

**Optional for bench testing:**
- Momentary push button + jumper wires (to simulate hook switch)
- Or just use keyboard input over SSH

---

## Phase 1: Pi Setup

### Step 1: Flash the SD Card

1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Insert the 32GB MicroSD card from the kit
3. In Imager:
   - **Device:** Raspberry Pi Zero 2 W
   - **OS:** Raspberry Pi OS Lite (32-bit) — under "Raspberry Pi OS (other)"
   - **Storage:** Your SD card

4. Click the **gear icon** (⚙️) or "Edit Settings" for advanced options:

   **General tab:**
   - ✅ Set hostname: `delmonte`
   - ✅ Set username and password: `pi` / (choose a password)
   - ✅ Configure wireless LAN:
     - SSID: (your WiFi network name)
     - Password: (your WiFi password)
     - Country: US
   - ✅ Set locale settings: America/Los_Angeles, us keyboard

   **Services tab:**
   - ✅ Enable SSH (Use password authentication)

5. Click **Save**, then **Write**
6. Wait for write + verification to complete

### Step 2: First Boot

1. Insert SD card into Pi Zero 2 WH
2. Connect power supply (micro-USB port labeled "PWR")
3. Wait 1-2 minutes for first boot and WiFi connection

4. Find the Pi on your network:
   ```bash
   # Try mDNS first
   ping delmonte.local
   
   # If that doesn't work, scan your network
   # (replace 192.168.1 with your network prefix)
   nmap -sn 192.168.1.0/24 | grep -i raspberry
   ```

5. SSH into the Pi:
   ```bash
   ssh pi@delmonte.local
   # Enter the password you set
   ```

### Step 3: Initial Configuration

```bash
# Update the system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-pygame git alsa-utils

# Verify Python version (should be 3.11+)
python3 --version

# Create project directory
mkdir -p ~/delmonte/audio ~/delmonte/logs
```

---

## Phase 2: Audio Setup

### Step 1: Connect USB Audio Adapter

1. Plug the UGREEN USB Audio Adapter into the Pi's USB port (labeled "USB", not "PWR")
   - **Note:** Pi Zero 2 WH has micro-USB, the kit should include a micro-USB to USB-A adapter
2. Connect the 3.5mm audio cable to the adapter's **green (output)** jack
3. Connect the speaker to the other end of the audio cable
   - For bench testing, you can use any speaker/headphones with a 3.5mm jack
   - Or wire the MakerHawk speaker directly (it has bare wire leads)

### Step 2: Configure Audio Output

```bash
# List audio devices
aplay -l

# You should see something like:
# card 1: Device [USB Audio Device], device 0: USB Audio [USB Audio]

# Set USB audio as default
# Find the card number from aplay -l (usually card 1)
sudo nano /etc/asound.conf
```

Add this content:
```
defaults.pcm.card 1
defaults.ctl.card 1
```

Save and exit (Ctrl+X, Y, Enter).

```bash
# Test with a system sound
speaker-test -t wav -c 1

# You should hear "Front Left" spoken
# Press Ctrl+C to stop
```

### Step 3: Test MP3 Playback

```bash
# Install mpg123 for quick MP3 testing
sudo apt install -y mpg123

# Test with a sample (we'll copy real files later)
# For now, generate a test tone
speaker-test -t sine -f 440 -c 1 -l 1
```

---

## Phase 3: Copy Audio Files

From your Mac (in a new terminal):

```bash
cd /Users/alexlopez/Sites/DelMonte/HelloHistory

# Copy all audio files to the Pi
scp src/audio/*.mp3 pi@delmonte.local:~/delmonte/audio/

# Verify they arrived
ssh pi@delmonte.local "ls -la ~/delmonte/audio/"
```

Test playback on the Pi:
```bash
# SSH into Pi
ssh pi@delmonte.local

# Play the intro
mpg123 ~/delmonte/audio/00_intro.mp3
```

---

## Phase 4: Bench Player Software

The bench player is a simplified version of the phone player that works without GPIO:
- **Spacebar** = Toggle play/pause (simulates hook switch)
- **Number keys 0-7** = Jump to chapter (simulates rotary dial)
- **Q** = Quit

### Step 1: Copy the Player Script

From your Mac:
```bash
scp src/bench_player.py pi@delmonte.local:~/delmonte/
```

### Step 2: Run the Bench Player

```bash
ssh pi@delmonte.local
cd ~/delmonte
python3 bench_player.py
```

**Controls:**
- Press **Space** to start playback (like picking up phone)
- Press **Space** again to stop (like hanging up)
- Press **1-6** to jump to that chapter
- Press **0** to restart from intro
- Press **7** to play the song
- Press **Q** to quit

---

## Phase 5: Testing Checklist

### Audio Quality
- [ ] Audio plays clearly through speaker
- [ ] Volume is adequate (adjust with `alsamixer` if needed)
- [ ] No pops/clicks at track transitions
- [ ] All 8 tracks play correctly

### Playback Logic
- [ ] Spacebar starts playback from intro
- [ ] Spacebar stops playback
- [ ] Number keys jump to correct chapters
- [ ] Tracks advance automatically when finished
- [ ] After track 7 (song), loops back to intro

### System Stability
- [ ] Can run for 30+ minutes without issues
- [ ] Responds correctly after multiple start/stop cycles
- [ ] Memory usage stays stable (`htop`)

---

## Troubleshooting

### No Audio Output

1. Check USB adapter is recognized:
   ```bash
   lsusb
   # Should show "C-Media Electronics" or similar
   ```

2. Check audio device:
   ```bash
   aplay -l
   # Should list USB Audio Device
   ```

3. Check volume:
   ```bash
   alsamixer
   # Press F6 to select USB device
   # Use arrow keys to adjust volume
   # Press M to unmute if muted
   ```

4. Check cable connections

### pygame.mixer Errors

If you see `pygame.error: No available audio device`:
```bash
# Make sure asound.conf is correct
cat /etc/asound.conf

# Try reinitializing with specific device
# Edit bench_player.py to use:
# pygame.mixer.init(devicename='hw:1,0')
```

### SSH Connection Issues

```bash
# If delmonte.local doesn't resolve
# Find Pi's IP address from your router, or:
arp -a | grep -i raspberry

# Connect by IP instead
ssh pi@192.168.x.x
```

---

## Next Steps (After Bench Testing Works)

1. **Add physical button** (optional)
   - Connect a momentary push button to GPIO 17 + GND
   - Modify player to use button instead of keyboard

2. **Set up auto-start service**
   - Create systemd service so player runs on boot

3. **Phone integration** (when you have the phone)
   - Wire hook switch to GPIO 17
   - Wire rotary dial pulses to GPIO 27
   - Install speaker in handset
   - Mount Pi in phone base

---

## Files Reference

| File | Location | Purpose |
|------|----------|---------|
| `bench_player.py` | `src/bench_player.py` (dev) → `~/delmonte/` (Pi) | Keyboard-controlled test player |
| Audio files | `src/audio/*.mp3` (dev) → `~/delmonte/audio/` (Pi) | Chapter audio |
| ALSA config | `/etc/asound.conf` (Pi) | USB audio default |
