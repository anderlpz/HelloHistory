# ElevenLabs AI Concierge Integration Plan

**Goal:** Add conversational AI agent accessible via rotary dial to answer questions about the Del Monte area using the Airbnb guide as a knowledge base.

## Overview

Users can dial different numbers for different experiences:
- **Dial 0** → Talk to AI concierge (ElevenLabs agent with Airbnb guide knowledge)
- **Dial 1** → Listen to house history (existing audio tour)

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  Rotary Phone (Hardware)                            │
│  - Handset lift detection (existing)                │
│  - Rotary dial pulse detection (NEW)                │
│  - Speaker (existing)                               │
│  - Microphone (NEW - for AI conversation)           │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  Raspberry Pi (DelMonte)                            │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  phone_player.py (UPDATED)                  │   │
│  │  - Handset lift → Play greeting             │   │
│  │  - Wait for dial input                      │   │
│  │  - Route based on digit                     │   │
│  └──────────────┬──────────────────────────────┘   │
│                 │                                   │
│  ┌──────────────▼──────────────┐  ┌──────────────┐ │
│  │  History Tour Module (1)    │  │  AI Module   │ │
│  │  - Play audio files         │  │  (0)         │ │
│  │  - Existing functionality   │  │  - Dial det  │ │
│  └─────────────────────────────┘  │  - WebSocket │ │
│                                    │  - Audio I/O │ │
│                                    └──────┬───────┘ │
└───────────────────────────────────────────┼─────────┘
                                            │ WebSocket
                                            │ (Internet)
                                            ▼
                              ┌──────────────────────────┐
                              │  ElevenLabs Cloud        │
                              │  - Conversational AI     │
                              │  - Knowledge Base        │
                              │    (Airbnb Guide PDF)    │
                              └──────────────────────────┘
```

---

## Phase 1: Knowledge Base Setup (No Code Required)

### Step 1.1: Get ElevenLabs Account
1. Sign up at https://elevenlabs.io
2. Choose plan:
   - **Creator ($22/month)** recommended: 250 minutes = ~4 hours conversation
   - Start with **Free (15 minutes)** for testing

### Step 1.2: Create AI Agent
1. Go to https://elevenlabs.io/app/agents/agents
2. Click "Create New Agent"
3. Configure:
   - **Name:** "Del Monte Concierge"
   - **Voice:** Choose a friendly, helpful voice
   - **System Prompt:** 
     ```
     You are a friendly local concierge for Del Monte, a beautiful historic home 
     rental. Your role is to help guests discover local restaurants, attractions, 
     activities, and answer questions about the area. You have access to a 
     comprehensive local guide. Be warm, conversational, and helpful. Keep 
     responses concise since users are on the phone.
     ```

### Step 1.3: Upload Knowledge Base
1. In agent settings, go to "Knowledge Base"
2. Click "Upload Document"
3. Upload: `/Users/alexlopez/Downloads/Minimalist Home Rental Welcome Guide A4 Document.pdf`
   - **Good news:** ElevenLabs accepts PDF directly, even image-based PDFs
   - Their system will OCR it automatically
4. Save agent settings
5. **Note the Agent ID** - you'll need this for integration

---

## Phase 2: Audio Updates

### Step 2.1: Update Greeting Recording
**Current greeting:** "Welcome to Del Monte..."

**New greeting needed:** 
```
Welcome to Del Monte. 

For the story of this historic home, dial 1.

To speak with your AI concierge and learn about local restaurants, 
attractions, and things to do, dial 0.
```

**Record and save as:** `audio/00_greeting_with_menu.mp3`

### Step 2.2: Optional Additional Recordings
- `audio/0X_ai_connecting.mp3` - "Connecting you to your AI concierge..."
- `audio/0X_ai_error.mp3` - "Sorry, the concierge is unavailable. Please try again later."

---

## Phase 3: Dial Detection Hardware/Software

### Option A: GPIO Pulse Detection (Recommended)
Rotary dials work by sending pulses when you dial a number.
- Dial 1 = 1 pulse
- Dial 0 = 10 pulses
- Each pulse is a brief circuit close/open

**Implementation:**
```python
import RPi.GPIO as GPIO
import time

DIAL_PIN = 23  # GPIO pin connected to dial mechanism

def detect_dial():
    """
    Wait for dial input and return the digit dialed (0-9).
    Returns None if timeout.
    """
    GPIO.setup(DIAL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    pulses = 0
    timeout = 5.0  # 5 second timeout
    start_time = time.time()
    
    # Wait for first pulse to start
    while GPIO.input(DIAL_PIN) == GPIO.HIGH:
        if time.time() - start_time > timeout:
            return None
        time.sleep(0.01)
    
    # Count pulses
    in_pulse = False
    while time.time() - start_time < timeout:
        pin_state = GPIO.input(DIAL_PIN)
        
        if pin_state == GPIO.LOW and not in_pulse:
            # Pulse started
            pulses += 1
            in_pulse = True
            time.sleep(0.05)  # Debounce
            
        elif pin_state == GPIO.HIGH and in_pulse:
            # Pulse ended
            in_pulse = False
            
        # If no activity for 1 second after pulses, done
        if pulses > 0 and time.time() - start_time > 1.0:
            break
            
        time.sleep(0.01)
    
    # Convert pulse count to digit (0 = 10 pulses)
    if pulses == 10:
        return 0
    elif 1 <= pulses <= 9:
        return pulses
    else:
        return None
```

### Option B: DTMF Tone Detection (If you add DTMF converter)
Some people add DTMF converters to rotary phones for easier detection.

**Library:** `python-dtmf-detector`

---

## Phase 4: ElevenLabs Integration

### Step 4.1: Install Dependencies
```bash
# On Raspberry Pi
cd ~/delmonte
source venv/bin/activate
pip install elevenlabs pyaudio
```

### Step 4.2: Create AI Module
**File:** `src/ai_concierge.py`

```python
import os
import signal
import subprocess
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.conversation import AudioInterface

class PhoneAudioInterface(AudioInterface):
    """Audio interface for rotary phone using ALSA"""
    
    def __init__(self):
        self.recording_process = None
        self.playback_process = None
        
    def start(self):
        """Initialize audio capture and playback"""
        # Start recording from USB audio (microphone on phone)
        self.recording_process = subprocess.Popen(
            [
                "arecord",
                "-D", "plughw:0,0",  # USB Audio device
                "-f", "S16_LE",       # 16-bit PCM
                "-r", "16000",        # 16kHz sample rate
                "-c", "1",            # Mono
                "-t", "raw",          # Raw PCM output
                "-"                   # Output to stdout
            ],
            stdout=subprocess.PIPE
        )
        
    def stop(self):
        """Cleanup audio resources"""
        if self.recording_process:
            self.recording_process.terminate()
        if self.playback_process:
            self.playback_process.terminate()
    
    def output(self, audio_chunk: bytes):
        """Play audio to phone speaker"""
        # Play audio using aplay
        if not self.playback_process or self.playback_process.poll() is not None:
            self.playback_process = subprocess.Popen(
                [
                    "aplay",
                    "-D", "plughw:0,0",  # USB Audio device
                    "-f", "S16_LE",
                    "-r", "16000",
                    "-c", "1",
                    "-t", "raw",
                    "-"
                ],
                stdin=subprocess.PIPE
            )
        
        try:
            self.playback_process.stdin.write(audio_chunk)
            self.playback_process.stdin.flush()
        except BrokenPipeError:
            pass
    
    def input(self) -> bytes:
        """Capture audio from phone microphone"""
        if self.recording_process:
            # Read 0.1 seconds of audio (1600 bytes at 16kHz, 16-bit, mono)
            audio_data = self.recording_process.stdout.read(1600)
            return audio_data
        return b""


def start_ai_conversation(agent_id: str, api_key: str):
    """
    Start ElevenLabs AI conversation via rotary phone.
    
    Args:
        agent_id: ElevenLabs agent ID
        api_key: ElevenLabs API key
    """
    client = ElevenLabs(api_key=api_key)
    
    conversation = Conversation(
        client,
        agent_id=agent_id,
        requires_auth=True,
        audio_interface=PhoneAudioInterface(),
        
        # Logging callbacks
        callback_agent_response=lambda response: print(f"AI: {response}"),
        callback_user_transcript=lambda transcript: print(f"User: {transcript}"),
    )
    
    # Start conversation
    print("Starting AI conversation...")
    conversation.start_session(user_id="rotary_phone_guest")
    
    # Handle graceful shutdown on Ctrl+C
    signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())
    
    # Wait for conversation to end (user hangs up or timeout)
    conversation_id = conversation.wait_for_session_end()
    print(f"Conversation ended: {conversation_id}")
    
    return conversation_id


if __name__ == "__main__":
    # Test the AI conversation
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python ai_concierge.py <agent_id> <api_key>")
        sys.exit(1)
    
    agent_id = sys.argv[1]
    api_key = sys.argv[2]
    
    start_ai_conversation(agent_id, api_key)
```

### Step 4.3: Update phone_player.py

Add to `src/phone_player.py`:

```python
from ai_concierge import start_ai_conversation
from dial_detection import detect_dial

# After handset lift and 1.5s delay:
def handle_phone_pickup():
    time.sleep(1.5)  # Existing delay
    
    # Play greeting with menu
    play_audio("audio/00_greeting_with_menu.mp3")
    
    # Wait for dial input
    digit = detect_dial()
    
    if digit == 1:
        # Existing history tour
        play_playlist(PLAYLIST)
        
    elif digit == 0:
        # AI concierge
        play_audio("audio/0X_ai_connecting.mp3")  # Optional
        
        try:
            agent_id = os.getenv("ELEVENLABS_AGENT_ID")
            api_key = os.getenv("ELEVENLABS_API_KEY")
            
            start_ai_conversation(agent_id, api_key)
            
        except Exception as e:
            print(f"AI conversation error: {e}")
            play_audio("audio/0X_ai_error.mp3")  # Optional
    
    else:
        # Invalid input - replay greeting
        play_audio("audio/00_greeting_with_menu.mp3")
```

---

## Phase 5: Configuration & Deployment

### Step 5.1: Environment Variables
Add to Raspberry Pi environment (or `/etc/systemd/system/phone-player.service`):

```bash
# Get these from your ElevenLabs dashboard
export ELEVENLABS_API_KEY="your_api_key_here"
export ELEVENLABS_AGENT_ID="your_agent_id_here"
```

### Step 5.2: Update Systemd Service
Edit `/etc/systemd/system/phone-player.service`:

```ini
[Service]
Environment="ELEVENLABS_API_KEY=your_key"
Environment="ELEVENLABS_AGENT_ID=your_agent_id"
```

### Step 5.3: Test Incrementally
```bash
# Test 1: Dial detection only
python src/dial_detection.py

# Test 2: AI conversation (without phone)
python src/ai_concierge.py <agent_id> <api_key>

# Test 3: Full integration
sudo systemctl restart phone-player
# Pick up phone and test both options
```

---

## Cost Estimation

**ElevenLabs Creator Plan ($22/month):**
- 250 minutes of conversation
- Average call: 3-5 minutes
- **~50-80 calls per month**
- Additional minutes: $0.10/min

**For typical Airbnb usage:**
- Assume 10 guests/month × 2 calls each × 4 minutes = 80 minutes/month
- **Creator plan is sufficient**

---

## Troubleshooting

### Issue: No audio from microphone
**Check:**
```bash
arecord -l  # List recording devices
arecord -D plughw:0,0 -d 5 test.wav  # Test recording
aplay test.wav  # Play back
```

### Issue: WebSocket connection fails
**Check:**
- Internet connectivity: `ping api.elevenlabs.io`
- API key validity
- Agent ID correctness

### Issue: AI doesn't have guide knowledge
**Check:**
- Knowledge base uploaded in ElevenLabs dashboard
- Document processing completed (may take a few minutes)

---

## Future Enhancements

1. **Multi-lingual support** - Detect language, switch agent
2. **Call logging** - Track most common questions
3. **Fallback to SMS** - If internet down, text guest info
4. **Voice feedback** - "I heard you dial [digit]"
5. **Emergency info** - Dial 9 for emergency contacts

---

## Next Steps

1. ✅ Sign up for ElevenLabs account
2. ✅ Create AI agent with Airbnb guide
3. ☐ Record new greeting with menu options
4. ☐ Implement dial detection
5. ☐ Integrate ElevenLabs SDK
6. ☐ Test on Raspberry Pi
7. ☐ Deploy and monitor usage

---

## Questions for User

Before starting implementation:

1. **Hardware:** Does your rotary phone have a microphone? Or will guests need to speak into the handset earpiece?
2. **Dial mechanism:** Can you confirm your rotary dial is connected to a GPIO pin? Which pin?
3. **Internet:** Confirm Raspberry Pi has stable internet (required for ElevenLabs WebSocket)
4. **Voice recording:** Do you want to record the new greeting yourself, or should we generate it with AI?

---

## References

- ElevenLabs Conversational AI: https://elevenlabs.io/docs/conversational-ai/overview
- ElevenLabs Python SDK: https://github.com/elevenlabs/elevenlabs-python
- Rotary Dial Detection: https://github.com/hhromic/python-rpi-gpio-rotary-encoder
