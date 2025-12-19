# Software Specification

## Overview

The HelloHistory software transforms a Raspberry Pi into a conversational AI that embodies Mary Lund Davis, allowing guests to have natural voice conversations through the rotary phone.

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| OS | Raspberry Pi OS (64-bit) | Base operating system |
| Runtime | Python 3.11+ | Application runtime |
| STT | Vosk | Offline speech-to-text |
| LLM | Ollama + gemma2:2b | Local language model |
| TTS | Piper | Offline text-to-speech |
| GPIO | gpiozero/RPi.GPIO | Hook switch detection |
| Audio | PyAudio | Microphone/speaker I/O |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        MAIN CONTROLLER                          │
│                      (mary_assistant.py)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        v                     v                     v
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Hook Detector │    │ Audio Manager │    │ Conversation  │
│   (GPIO)      │    │  (PyAudio)    │    │    Engine     │
└───────────────┘    └───────────────┘    └───────────────┘
                              │                     │
                     ┌────────┴────────┐           │
                     │                 │           │
                     v                 v           v
              ┌───────────┐    ┌───────────┐ ┌───────────┐
              │   Vosk    │    │   Piper   │ │  Ollama   │
              │   (STT)   │    │   (TTS)   │ │   (LLM)   │
              └───────────┘    └───────────┘ └───────────┘
```

---

## State Machine

```
                    ┌──────────────┐
                    │    IDLE      │◄─────────────────────┐
                    │  (waiting)   │                      │
                    └──────┬───────┘                      │
                           │                              │
                    Hook lifted                    Hook replaced
                           │                              │
                           v                              │
                    ┌──────────────┐                      │
                    │   GREETING   │                      │
                    │ (play intro) │                      │
                    └──────┬───────┘                      │
                           │                              │
                    Greeting done                         │
                           │                              │
                           v                              │
               ┌──────────────────────┐                   │
               │      LISTENING       │◄──────┐           │
               │  (capture speech)    │       │           │
               └──────────┬───────────┘       │           │
                          │                   │           │
                   Speech detected            │           │
                          │                   │           │
                          v                   │           │
               ┌──────────────────────┐       │           │
               │     PROCESSING       │       │           │
               │   (STT → LLM → TTS)  │       │           │
               └──────────┬───────────┘       │           │
                          │                   │           │
                   Response ready             │           │
                          │                   │           │
                          v                   │           │
               ┌──────────────────────┐       │           │
               │      SPEAKING        │───────┘           │
               │   (play response)    │                   │
               └──────────┬───────────┘                   │
                          │                               │
                          └───────────────────────────────┘
```

---

## Module Specifications

### 1. Main Controller (`mary_assistant.py`)

**Responsibilities:**
- Initialize all subsystems
- Manage state machine
- Coordinate between modules
- Handle graceful shutdown

**Key Functions:**
```python
class MaryAssistant:
    def __init__(self, config_path: str)
    async def run(self)  # Main event loop
    async def on_hook_lifted(self)
    async def on_hook_replaced(self)
    async def conversation_turn(self, user_speech: str) -> str
    def shutdown(self)
```

### 2. Hook Detector (`hook_detector.py`)

**Responsibilities:**
- Monitor GPIO pin for hook switch state
- Debounce switch signal
- Emit events on state change

**Configuration:**
```python
HOOK_PIN = 17           # GPIO pin (BCM numbering)
DEBOUNCE_MS = 50        # Debounce time
POLL_INTERVAL = 0.1     # Seconds between checks
```

**Key Functions:**
```python
class HookDetector:
    def __init__(self, pin: int, callback_lifted, callback_replaced)
    def start(self)
    def stop(self)
    @property
    def is_off_hook(self) -> bool
```

### 3. Audio Manager (`audio_manager.py`)

**Responsibilities:**
- Configure audio devices
- Capture microphone input
- Play audio output
- Manage audio streams

**Key Functions:**
```python
class AudioManager:
    def __init__(self, mic_device: str, speaker_device: str)
    def start_recording(self) -> AudioStream
    def stop_recording(self) -> bytes
    def play_audio(self, audio_data: bytes)
    def play_file(self, path: str)
    def set_volume(self, level: int)
```

### 4. Speech-to-Text (`stt_engine.py`)

**Technology:** Vosk

**Model:** `vosk-model-small-en-us-0.15` (40MB)
- Larger model available: `vosk-model-en-us-0.22` (1.8GB)

**Key Functions:**
```python
class STTEngine:
    def __init__(self, model_path: str)
    def transcribe(self, audio_data: bytes) -> str
    def transcribe_stream(self, stream) -> Generator[str]
```

**Performance Target:** <500ms latency for typical utterance

### 5. Language Model (`llm_engine.py`)

**Technology:** Ollama

**Recommended Models:**
| Model | Size | Quality | Speed |
|-------|------|---------|-------|
| gemma2:2b | 1.6GB | Good | Fast |
| qwen2.5:3b | 2GB | Better | Medium |
| phi3:mini | 2.3GB | Good | Medium |

**System Prompt Structure:**
```
You are Mary Lund Davis, a pioneering architect...

[Character background]
[Personality traits]
[Knowledge about Del Monte house]
[Conversation guidelines]

Always respond as Mary would - confident, warm, knowledgeable.
Keep responses conversational (2-3 sentences typical).
If asked something you don't know, respond naturally as Mary would.
```

**Key Functions:**
```python
class LLMEngine:
    def __init__(self, model: str, system_prompt: str)
    async def generate(self, user_message: str, history: list) -> str
    def clear_history(self)
```

**Conversation History:**
- Maintain last 4-6 exchanges for context
- Clear on hook replaced (new conversation)

### 6. Text-to-Speech (`tts_engine.py`)

**Technology:** Piper

**Voice Selection:**
- Default: `en_US-lessac-medium` (natural female voice)
- Alternative: `en_GB-alba-medium` (British accent, period feel)
- Future: Custom fine-tuned voice

**Key Functions:**
```python
class TTSEngine:
    def __init__(self, voice_model: str)
    def synthesize(self, text: str) -> bytes
    def synthesize_to_file(self, text: str, path: str)
```

**Audio Post-Processing (Optional):**
- Add slight telephone filter effect
- Subtle vinyl crackle for period authenticity
- Can be disabled for clarity

---

## Configuration

### Main Configuration (`config.json`)

```json
{
  "hardware": {
    "hook_pin": 17,
    "mic_device": "USB Audio",
    "speaker_device": "USB Audio"
  },
  "audio": {
    "sample_rate": 16000,
    "channels": 1,
    "volume": 80
  },
  "stt": {
    "model_path": "models/vosk-model-small-en-us",
    "silence_threshold": 0.5,
    "max_recording_seconds": 30
  },
  "llm": {
    "model": "gemma2:2b",
    "temperature": 0.7,
    "max_tokens": 150,
    "history_length": 6
  },
  "tts": {
    "voice": "en_US-lessac-medium",
    "speed": 1.0,
    "apply_phone_filter": true
  },
  "behavior": {
    "greeting_audio": "audio/greeting.wav",
    "goodbye_audio": "audio/goodbye.wav",
    "thinking_audio": "audio/thinking.wav",
    "error_audio": "audio/error.wav"
  }
}
```

---

## Conversation Flow

### Greeting
When handset is lifted, Mary greets the caller:

> "Hello! This is Mary Lund Davis. You're calling from my Del Monte house - 
> my first home and office, which I designed back in 1954. 
> What would you like to know?"

### Sample Interactions

**Q: "Who are you?"**
> "I'm Mary Lund Davis. I was the first licensed female architect in 
> Washington State after the war. I designed this very house you're 
> standing in - we called it Del Monte. It was my finest building, 
> if I do say so myself."

**Q: "Tell me about this house."**
> "Del Monte was built in 1954 as our first home and my architecture 
> office. I designed it as a 'skin and bones' structure - light timber 
> frame wrapped in plywood, with clerestory windows to bring in the 
> light. The whole idea was indoor-outdoor living, connecting you 
> to the landscape."

**Q: "What's your background?"**
> "I grew up in Sacramento, born to Danish immigrants. My father Anders 
> taught me to build houses when I was just eight years old. He always 
> told me I could do anything a man could do - and I believed him. 
> I studied architecture at the University of Washington, graduated 
> in 1945, and never looked back."

### Goodbye
When handset is replaced, Mary says goodbye:

> "It was lovely chatting with you. Enjoy my house - 
> treat it well. Goodbye!"

---

## Error Handling

| Error | User Experience | Technical Response |
|-------|-----------------|-------------------|
| STT fails | "I'm sorry, I didn't catch that. Could you say that again?" | Retry STT, log error |
| LLM timeout | "Let me think about that... [pause] I seem to have lost my train of thought." | Retry with shorter prompt |
| TTS fails | [Silence, then retry] | Fall back to cached audio or retry |
| System crash | [Automatic restart] | Systemd auto-restart |

---

## Performance Targets

| Metric | Target | Acceptable |
|--------|--------|------------|
| Hook detection | <100ms | <200ms |
| STT latency | <500ms | <1000ms |
| LLM response | <3s | <5s |
| TTS synthesis | <1s | <2s |
| End-to-end | <5s | <8s |

---

## Installation & Dependencies

### System Dependencies
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv portaudio19-dev sox alsa-utils
```

### Python Dependencies (`requirements.txt`)
```
pyaudio>=0.2.13
vosk>=0.3.45
numpy>=1.24.0
requests>=2.28.0
gpiozero>=2.0
RPi.GPIO>=0.7.1
pydub>=0.25.1
soundfile>=0.12.1
```

### Ollama Installation
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gemma2:2b
```

### Piper Installation
```bash
# Download Piper binary
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
tar -xzf piper_arm64.tar.gz
mv piper /opt/piper

# Download voice model
mkdir -p /opt/piper/voices
wget -O /opt/piper/voices/en_US-lessac-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget -O /opt/piper/voices/en_US-lessac-medium.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
```

### Vosk Model
```bash
mkdir -p models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip -d models/
```

---

## Auto-Start Configuration

### Systemd Service (`/etc/systemd/system/hellohistory.service`)

```ini
[Unit]
Description=HelloHistory Voice Assistant
After=network.target ollama.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/HelloHistory
ExecStart=/home/pi/HelloHistory/venv/bin/python mary_assistant.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Enable Service
```bash
sudo systemctl enable hellohistory
sudo systemctl start hellohistory
```

---

## Directory Structure

```
/home/pi/HelloHistory/
├── mary_assistant.py      # Main entry point
├── hook_detector.py       # GPIO handling
├── audio_manager.py       # Audio I/O
├── stt_engine.py          # Vosk wrapper
├── llm_engine.py          # Ollama wrapper
├── tts_engine.py          # Piper wrapper
├── config.json            # Configuration
├── requirements.txt       # Python dependencies
├── models/
│   └── vosk-model-small-en-us/
├── voices/
│   ├── en_US-lessac-medium.onnx
│   └── en_US-lessac-medium.onnx.json
├── audio/
│   ├── greeting.wav
│   ├── goodbye.wav
│   └── thinking.wav
├── knowledge/
│   ├── mary_biography.md
│   ├── del_monte_facts.md
│   └── system_prompt.txt
└── logs/
    └── assistant.log
```

---

## Testing Strategy

### Unit Tests
- Hook detection: Simulate GPIO state changes
- Audio: Record/playback test files
- STT: Test with known audio samples
- TTS: Verify output audio files generated

### Integration Tests
- Full conversation flow (mock GPIO)
- Response quality verification
- Latency measurement

### Field Testing
- Real phone hardware
- Multiple conversation scenarios
- Long-running stability test (24+ hours)

---

## Future Enhancements

1. **Custom Voice Model**
   - Fine-tune Piper voice to sound like Mary
   - Requires audio samples of similar voice

2. **RAG Integration**
   - Index thesis PDF for detailed facts
   - More accurate historical responses

3. **Multi-language**
   - Danish greetings (her heritage)
   - Period-appropriate expressions

4. **Analytics**
   - Track popular questions
   - Improve responses over time

5. **Remote Management**
   - Web interface for monitoring
   - Remote configuration updates
