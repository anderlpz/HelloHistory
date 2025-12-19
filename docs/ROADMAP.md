# HelloHistory Roadmap

## Version Strategy

```
┌─────────────────────────────────────────────────────────────────────┐
│  MVP (Mac Prototype)     →    V1 (Phone Deploy)    →    Future     │
│  ────────────────────         ─────────────────         ──────     │
│  • Validate experience        • Hardware build          • Custom   │
│  • Test voice quality         • Self-contained            voice    │
│  • Refine Mary's character    • Offline operation       • RAG      │
│  • Zero hardware cost         • Guest-ready             • Multi-   │
│                                                           lang     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Voice Model Options

### The Trade-off Triangle

```
        QUALITY
           ▲
          /│\
         / │ \
        /  │  \     Fish Speech, XTTS, OpenVoice
       /   │   \    (GPU required, slower)
      /    │    \
     /     │     \
    /──────┼──────\
   /       │       \
  /        │        \
 ▼─────────┴─────────▼
SPEED              SIMPLICITY
(Piper)            (Cloud APIs)
```

### Option Comparison

| Model | Quality | Speed | Voice Clone | Runs on Pi? | Offline? | License |
|-------|---------|-------|-------------|-------------|----------|---------|
| **Piper** | Good | Very Fast | No (preset voices) | Yes | Yes | MIT |
| **Fish Speech** | Excellent | Slow | Yes (10-30s sample) | Difficult | Yes | Apache/CC-NC |
| **OpenVoice** | Very Good | Medium | Yes (instant) | Difficult | Yes | MIT |
| **XTTS** | Very Good | Slow | Yes (6s sample) | No (needs GPU) | Yes | CPML (NC) |
| **ElevenLabs** | Excellent | Fast | Yes | N/A (cloud) | No | Commercial |
| **Fish.audio API** | Excellent | Fast | Yes | N/A (cloud) | No | Commercial |

### Recommendation by Version

| Version | Recommended | Rationale |
|---------|-------------|-----------|
| **MVP** | Fish.audio API or ElevenLabs | Best quality for testing experience, no setup |
| **V1** | Piper | Proven on Pi, fast, reliable, offline |
| **Future** | Fish Speech local or custom Piper voice | Best of both worlds |

### Voice Model Deep Dive

#### Piper (MVP fallback, V1 primary)
- **Pros:** Blazing fast (<100ms), runs on Pi, many voices, battle-tested
- **Cons:** No voice cloning, preset voices only
- **Best voice for Mary:** `en_US-lessac-medium` (natural female) or `en_GB-alba-medium` (refined British)
- **Why it works:** For V1, reliability > perfect voice match

#### Fish Speech / Fish.audio
- **Local (fish-speech):** 4B parameter model, needs GPU, very slow on CPU
- **API (fish.audio):** Cloud service, excellent quality, voice cloning from 10-30s sample
- **Voice cloning:** Could potentially clone a voice similar to Mary's era
- **Cost:** API has free tier, then usage-based pricing

#### OpenVoice (MIT, by MyShell)
- **Pros:** MIT license (free commercial use), instant voice cloning, good quality
- **Cons:** Needs GPU for reasonable speed, complex setup
- **Use case:** If we find a reference voice we want to clone

#### ElevenLabs
- **Pros:** Industry-leading quality, easy API, voice cloning
- **Cons:** Cloud-only, ongoing costs, requires internet
- **Use case:** MVP testing for best possible voice quality

---

## Conversation Flow Architecture

### How "Scripting" Works

This isn't traditional scripting (pre-written dialogues). Instead, it's **guided improvisation**:

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONVERSATION ENGINE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   SYSTEM    │    │   CONTEXT   │    │   USER      │        │
│  │   PROMPT    │ +  │   MEMORY    │ +  │   INPUT     │ → LLM  │
│  │             │    │             │    │             │        │
│  │ "You are    │    │ Previous    │    │ "Tell me    │        │
│  │  Mary..."   │    │ exchanges   │    │  about..."  │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│                                                                 │
│                              ↓                                  │
│                                                                 │
│                     ┌─────────────┐                            │
│                     │   MARY'S    │                            │
│                     │  RESPONSE   │                            │
│                     │             │                            │
│                     │ Generated   │                            │
│                     │ in-character│                            │
│                     └─────────────┘                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### The Three Layers of "Scripting"

#### Layer 1: System Prompt (Character Definition)
This is the "script" - but it defines WHO Mary is, not WHAT she says:

```
You are Mary Lund Davis, a pioneering architect...
- Your personality: confident, warm, practical
- Your knowledge: Del Monte, Fantastic Homes, Pacific NW modernism
- Your speaking style: direct, 2-3 sentences, occasional wit
- Your boundaries: you lived until 2008, you don't know modern tech
```

#### Layer 2: Knowledge Base (Facts She Can Reference)
Structured information Mary can draw from:

```
knowledge/
├── mary_biography.md      # Her life story
├── del_monte_facts.md     # This specific house
├── fantastic_homes.md     # Her affordable housing work
├── design_philosophy.md   # Her architectural principles
└── personal_stories.md    # Anecdotes, the purple horse, etc.
```

#### Layer 3: Conversation Memory (Dynamic Context)
The LLM remembers recent exchanges:

```
Turn 1: Guest asks about the house
Turn 2: Mary explains Del Monte's design
Turn 3: Guest asks follow-up about windows
Turn 4: Mary elaborates on clerestory windows (remembers context)
```

### Pre-Scripted Elements

Some things ARE scripted (audio files, not generated):

| Element | Type | Purpose |
|---------|------|---------|
| Greeting | Pre-recorded or generated once | Consistent, polished first impression |
| Goodbye | Pre-recorded or generated once | Warm send-off |
| "Thinking" sound | Audio file | Fill silence during LLM processing |
| Error recovery | Pre-recorded | "I'm sorry, could you say that again?" |

### Conversation Flow State Machine

```
                        ┌──────────────┐
           ┌───────────→│    IDLE      │←──────────────┐
           │            └──────┬───────┘               │
           │                   │ Hook lifted           │
           │                   ▼                       │
           │            ┌──────────────┐               │
           │            │   GREETING   │               │
           │            │ (pre-scripted)│              │
           │            └──────┬───────┘               │
           │                   │                       │
           │                   ▼                       │
           │    ┌──────────────────────────┐          │
           │    │        LISTENING          │          │
      Hook │    │   (Vosk captures audio)   │←───┐     │ Hook
   replaced│    └──────────┬───────────────┘    │     │ replaced
           │               │ Speech detected    │     │
           │               ▼                    │     │
           │    ┌──────────────────────────┐    │     │
           │    │       PROCESSING          │    │     │
           │    │  ┌─────┐ ┌─────┐ ┌─────┐ │    │     │
           │    │  │ STT │→│ LLM │→│ TTS │ │    │     │
           │    │  └─────┘ └─────┘ └─────┘ │    │     │
           │    └──────────┬───────────────┘    │     │
           │               │ Response ready     │     │
           │               ▼                    │     │
           │    ┌──────────────────────────┐    │     │
           │    │        SPEAKING           │────┘     │
           │    │   (Piper audio plays)     │          │
           │    └──────────────────────────┘          │
           │                                          │
           └──────────────────────────────────────────┘
```

### Handling Edge Cases

| Situation | Response |
|-----------|----------|
| Silence (no speech detected) | After 5s: "Are you still there? Don't be shy!" |
| Very long input | Truncate, respond to first part |
| Unintelligible speech | "I'm sorry, my hearing isn't what it used to be. Could you say that again?" |
| Off-topic question | Stay in character: "I'm not sure about that, but let me tell you about..." |
| Inappropriate content | Deflect gracefully, redirect to architecture |
| "Are you AI?" | "I'm Mary Lund Davis. This is my house. What would you like to know about it?" |

---

## MVP: Mac Prototype

### Scope

**Goal:** Validate the experience before buying hardware

**What it includes:**
- Voice input via Mac microphone
- LLM generating Mary's responses
- Voice output via Mac speakers
- Basic conversation loop
- Mary's character and knowledge

**What it excludes:**
- GPIO/hook detection (simulated with keyboard)
- Raspberry Pi optimization
- Phone hardware integration
- Production reliability features

### Technology Stack (MVP)

| Component | Choice | Rationale |
|-----------|--------|-----------|
| STT | Whisper (local) or Deepgram API | Best accuracy for testing |
| LLM | Ollama + llama3.2:3b or Claude API | Fast iteration |
| TTS | Fish.audio API or ElevenLabs | Best voice quality for validation |
| Runtime | Python | Simple, fast development |
| Interface | Terminal + keyboard triggers | Simulate phone behavior |

### MVP Success Criteria

1. **Response Quality:** Mary's responses feel authentic and knowledgeable
2. **Conversation Flow:** Natural back-and-forth, maintains context
3. **Latency:** <8 seconds end-to-end is acceptable for testing
4. **Voice:** Sounds appropriate for the character (period, warmth)
5. **Knowledge:** Can answer questions about Del Monte, her life, architecture

### MVP File Structure

```
src/
├── mvp/
│   ├── mary_mvp.py          # Main conversation loop
│   ├── stt_whisper.py       # Speech-to-text (Whisper)
│   ├── llm_client.py        # LLM interface (Ollama/API)
│   ├── tts_client.py        # TTS interface (Fish.audio/ElevenLabs)
│   └── config_mvp.yaml      # MVP configuration
```

---

## V1: Phone Deployment

### Scope

**Goal:** Working phone installation at Del Monte property

**What it includes:**
- Everything in MVP
- Raspberry Pi 5 hardware
- GPIO hook switch detection
- Offline STT (Vosk)
- Offline TTS (Piper)
- Local LLM (Ollama + small model)
- Auto-start on boot
- Error recovery
- Phone hardware integration

**Constraints:**
- Must run fully offline (WiFi optional for updates)
- Must fit inside rotary phone shell
- Must be reliable for unattended operation
- Response time <8 seconds

### V1 Technology Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Platform | Raspberry Pi 5 (8GB) | Only option for local LLM |
| STT | Vosk | Fast, offline, proven on Pi |
| LLM | Ollama + gemma2:2b | Good balance quality/speed |
| TTS | Piper | Fast, offline, natural voices |
| Hook Detection | gpiozero | Simple, reliable |
| Service | systemd | Auto-start, recovery |

---

## Future Enhancements (Backlog)

### Voice Improvements

| Enhancement | Description | Complexity |
|-------------|-------------|------------|
| Custom Piper voice | Train Piper on similar voice samples | High |
| Fish Speech on Pi | When hardware improves or model shrinks | Medium |
| Period audio effects | Subtle vinyl crackle, phone filter | Low |
| Multiple voice styles | Mary at different ages/moods | High |

### Intelligence Improvements

| Enhancement | Description | Complexity |
|-------------|-------------|------------|
| RAG integration | Index full thesis for detailed questions | Medium |
| Better context | Remember conversations across sessions | Medium |
| Proactive stories | Mary volunteers stories based on time of day | Low |
| Question suggestions | "Would you like to hear about the purple horse?" | Low |

### Experience Improvements

| Enhancement | Description | Complexity |
|-------------|-------------|------------|
| Dial detection | Different responses based on dialed "number" | High |
| Ring simulation | Phone "rings" at certain times, Mary calls guest | Medium |
| Multi-language | Danish greetings, Spanish for diverse guests | Medium |
| Guest analytics | Track popular questions for improvement | Low |

### Hardware Improvements

| Enhancement | Description | Complexity |
|-------------|-------------|------------|
| Better mic | Noise-canceling USB mic | Low |
| Audio amp | Louder, clearer speaker output | Low |
| Status LED | Visual feedback hidden inside phone | Low |
| Remote management | Web interface for monitoring | Medium |

### Wild Ideas (Someday/Maybe)

- **Photo album integration:** "If you open the album on the coffee table..."
- **Sensor triggers:** Motion sensor activates ambient Mary comments
- **Multi-room:** Different "characters" on different phones
- **AR companion:** Mary appears via phone camera overlay
- **Guest book integration:** Mary references previous guests' questions

---

## Development Phases

### Phase 0: Planning (Current)
- [x] Project setup and git repo
- [x] Hardware/software specifications
- [x] Mary's knowledge base
- [x] Voice model research
- [ ] Roadmap finalization ← **You are here**
- [ ] Mac prototype requirements

### Phase 1: MVP Development (Next)
- [ ] Set up Python environment
- [ ] Implement STT (Whisper)
- [ ] Implement LLM client (Ollama)
- [ ] Implement TTS client (Fish.audio API)
- [ ] Build conversation loop
- [ ] Test and refine Mary's character
- [ ] Validate experience with real conversations

### Phase 2: V1 Preparation
- [ ] Order Raspberry Pi and components
- [ ] Set up Pi OS and dependencies
- [ ] Port MVP code to Pi
- [ ] Replace cloud TTS with Piper
- [ ] Replace Whisper with Vosk
- [ ] Optimize for latency
- [ ] Test reliability

### Phase 3: Hardware Integration
- [ ] Acquire/prepare rotary phone
- [ ] Identify and wire hook switch
- [ ] Install microphone in handset
- [ ] Install speaker
- [ ] Mount Pi inside phone
- [ ] Test full integration

### Phase 4: Deployment
- [ ] Configure auto-start
- [ ] Test error recovery
- [ ] Create maintenance documentation
- [ ] Install at Del Monte property
- [ ] Test with real guests
- [ ] Iterate based on feedback

---

## Decision Log

| Decision | Choice | Date | Rationale |
|----------|--------|------|-----------|
| Platform | Raspberry Pi 5 | 2024-12-19 | Only viable option for local LLM |
| MVP TTS | Cloud API (Fish/Eleven) | 2024-12-19 | Best quality for validation |
| V1 TTS | Piper | 2024-12-19 | Proven offline performance on Pi |
| MVP STT | Whisper | 2024-12-19 | Best accuracy |
| V1 STT | Vosk | 2024-12-19 | Fast offline on Pi |
| Assembly | No-solder | 2024-12-19 | Accessibility, reversibility |

---

## Open Questions

1. **Voice selection:** Should we test multiple Piper voices before committing?
2. **Greeting style:** Pre-recorded audio or generate once and cache?
3. **Conversation length:** Should there be a time limit per call?
4. **Error handling:** How verbose should error messages be?
5. **Updates:** How will we update the system remotely if needed?
6. **Backup:** Should there be a fallback if LLM fails (pre-recorded responses)?
