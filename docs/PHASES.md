# HelloHistory: Phased Implementation

## Philosophy: Start Simple, Add Complexity

```
PHASE 4          PHASE 3              PHASE 2           PHASE 1
─────────────────────────────────────────────────────────────────►
Simplest                                                 Most Complex

Voice Tracks  →  Choose Your    →   AI Chat with   →  Full Assistant
(Loop)           Own Adventure      Mary's History     + Web Search
                 (Rotary Dial)
```

**Each phase is a complete, deployable experience.** You can stop at any phase and have something guests will love.

---

## Phase 4: Voice Tracks (Simplest MVP)

### Experience
Guest picks up phone → Hears Mary telling stories → Stories loop

### What It Is
Pre-recorded audio chapters about Mary Lund Davis, the Del Monte house, and her work. When guests pick up the phone, they hear Mary's voice sharing stories. Simple, elegant, magical.

### Technical Requirements

| Component | Solution | Complexity |
|-----------|----------|------------|
| Voice Generation | ElevenLabs | You generate audio files |
| Hardware | Raspberry Pi Zero 2W | $15, tiny, enough for audio |
| Hook Detection | GPIO | Simple on/off |
| Audio Output | USB DAC + Speaker | Standard |
| Software | Python + pygame | Play audio files |

### Content Needed

**Chapter Structure (Example):**
```
Chapter 1: Welcome to Del Monte (2-3 min)
  - Mary introduces herself
  - "You're standing in my finest building..."
  - Brief overview of the house

Chapter 2: My Story (3-4 min)
  - Danish immigrant parents
  - Father teaching her to build
  - "He always told me I could do anything a man could do"

Chapter 3: Building Del Monte (3-4 min)
  - 1954, designing her first home
  - "Skin and bones" architecture
  - The clerestory windows, the light

Chapter 4: The Fantastic Homes (2-3 min)
  - Affordable housing mission
  - "All low-cost housing doesn't have to be cheap"
  - 200+ homes built

Chapter 5: Pacific Northwest Modernism (2-3 min)
  - Her contemporaries
  - Indoor/outdoor living philosophy
  - Connection to nature

Chapter 6: Personal Stories (2-3 min)
  - The purple horse
  - Sailing victories
  - Japanese maple collection

Chapter 7: Closing (1 min)
  - "Enjoy my house. Treat it well."
  - Invitation to explore
```

### Behavior
```
Hook Lifted → Play Chapter 1
Chapter 1 ends → Play Chapter 2
...
Chapter 7 ends → Loop back to Chapter 1
Hook Replaced → Stop playback, reset to Chapter 1
```

### Hardware (Phase 4)

| Item | Cost | Notes |
|------|------|-------|
| Raspberry Pi Zero 2W | $15 | Tiny, sufficient for audio |
| 32GB microSD | $8 | Holds OS + audio files |
| USB Audio Adapter | $10 | For speaker output |
| Small Speaker | $8 | Fits in phone |
| Hook switch wiring | $5 | Terminal blocks, jumpers |
| Power supply | $10 | USB-C |
| **Total** | **~$56** | Much cheaper than full AI |

### Scripts to Generate

You'll need to write/refine scripts for each chapter, then generate audio with ElevenLabs.

**Script Format:**
```markdown
# Chapter 1: Welcome to Del Monte

[Warm, inviting tone]

Hello! I'm Mary Lund Davis, and you're calling from my Del Monte 
house. I built this place back in 1954 as my very first home and 
architecture office.

[Slight pause, reflective]

You know, I always considered it my finest building. Some architects 
chase grand commissions, but there's something special about designing 
the place where you'll live and work...

[Continue for 2-3 minutes]
```

### Estimated Timeline
- Script writing: 2-3 hours
- ElevenLabs generation: 1-2 hours
- Hardware setup: 2-3 hours
- Software: 1-2 hours
- **Total: 1 weekend project**

---

## Phase 3: Choose Your Own Adventure

### Experience
Guest picks up phone → Hears Mary's greeting → Uses rotary dial to select topics → Hears selected content

### What It Is
Interactive menu system using the rotary phone's dial. "Dial 1 to hear about this house. Dial 2 to learn about my life. Dial 3 for things to do nearby..."

### Technical Requirements

| Component | Solution | Complexity |
|-----------|----------|------------|
| Everything from Phase 4 | Same | - |
| Rotary Dial Detection | GPIO pulse counting | Medium |
| Menu Logic | State machine | Low |
| More Audio Content | ElevenLabs | More scripts |

### Rotary Dial Detection

Rotary phones generate pulses when dialed:
- Dial "1" = 1 pulse
- Dial "5" = 5 pulses
- Dial "0" = 10 pulses

```
Dial rotates → Opens/closes circuit → GPIO counts pulses
```

**Hardware Addition:**
- Connect dial pulse wire to GPIO
- Software counts pulses, debounces, determines digit

### Menu Structure

```
MAIN MENU (plays on pickup):
"Hello! I'm Mary Lund Davis. Welcome to my Del Monte house.
 Dial 1 to hear about this house.
 Dial 2 to learn about my life.
 Dial 3 to hear about my other buildings.
 Dial 4 for things to do in the area.
 Dial 0 to hear everything from the beginning."

[1] THIS HOUSE
    → "Del Monte was built in 1954..."
    → "Dial 1 for the architecture, 2 for the story behind it, 
       0 to return to main menu"

[2] MY LIFE
    → "I was born in Sacramento in 1922..."
    → Sub-menus for childhood, education, career, family

[3] MY OTHER BUILDINGS
    → "The Fantastic Homes were my proudest achievement..."
    → Sub-menus for Fantastic Homes, Alameda, Pampas Point

[4] THINGS TO DO
    → Pre-recorded recommendations
    → "There's a wonderful restaurant called..."
    → Local attractions, beaches, hikes
```

### Hardware Additions (Phase 3)

| Item | Cost | Notes |
|------|------|-------|
| Phase 4 hardware | $56 | Base |
| Additional GPIO wiring for dial | $5 | May already have access |
| **Total** | **~$61** | Minimal additional cost |

### Estimated Timeline
- Additional script writing: 3-4 hours
- Rotary dial reverse-engineering: 2-3 hours
- Menu software: 3-4 hours
- Testing: 2-3 hours
- **Total: 1-2 weekends**

---

## Phase 2: AI Chat with Mary's History

### Experience
Guest picks up phone → Mary greets them → Guest asks any question → Mary responds conversationally

### What It Is
The original vision: a conversational AI that embodies Mary, trained on her history, able to answer questions naturally.

### Technical Requirements

| Component | Solution | Complexity |
|-----------|----------|------------|
| Hardware | Raspberry Pi 5 (8GB) | More powerful |
| STT | Vosk | Offline speech recognition |
| LLM | Ollama + gemma2:2b | Local inference |
| TTS | Piper | Offline, natural voice |
| Knowledge | System prompt + RAG | Mary's history |

### What Changes from Phase 3
- Replace pre-recorded audio with generated speech
- Add microphone for guest input
- Add STT → LLM → TTS pipeline
- Replace menu logic with conversation loop

### Hardware (Phase 2)

| Item | Cost | Notes |
|------|------|-------|
| Raspberry Pi 5 (8GB) | $80 | Required for LLM |
| 64GB microSD | $12 | Holds models |
| Power supply (27W) | $12 | Pi 5 needs more power |
| Cooling | $15 | Passive case |
| USB Microphone | $20 | For guest speech |
| USB Audio Adapter | $10 | For speaker |
| Speaker | $8 | Same as before |
| Hook switch wiring | $5 | Same as before |
| **Total** | **~$162** | Significant upgrade |

### Estimated Timeline
- Port Phase 3 code: 1-2 hours
- Set up STT/LLM/TTS on Pi: 4-6 hours
- Optimize latency: 4-6 hours
- Test and refine: 4-6 hours
- **Total: 2-3 weekends**

---

## Phase 1: Full Assistant + Web Search

### Experience
Guest picks up phone → Can ask Mary anything → Mary can search for local info, recommendations, etc.

### What It Is
Full-featured AI assistant that knows Mary's history AND can provide live information about the area.

### Technical Requirements

| Component | Solution | Complexity |
|-----------|----------|------------|
| Everything from Phase 2 | Same | - |
| Internet Connection | WiFi | Required |
| Web Search | API (Tavily, SerpAPI, etc.) | Tool calling |
| Function Calling | LLM with tools | More complex prompts |

### What Changes from Phase 2
- Requires reliable internet
- LLM needs function/tool calling capability
- Additional APIs for search, places, weather
- More complex system prompt

### Additional Capabilities
- "What's the weather tomorrow?"
- "Where should we eat dinner?"
- "What's there to do nearby?"
- "Tell me about [local attraction]"

### Hardware (Phase 1)

| Item | Cost | Notes |
|------|------|-------|
| Phase 2 hardware | $162 | Base |
| Reliable WiFi | $0 | Existing |
| API costs | ~$5-10/month | Search APIs |
| **Total** | **~$170 + ongoing** | Similar hardware, adds API costs |

### Estimated Timeline
- Add tool calling: 2-4 hours
- Integrate search APIs: 2-3 hours
- Test and refine: 4-6 hours
- **Total: 1-2 weekends** (after Phase 2)

---

## Summary Comparison

| Phase | Experience | Hardware Cost | Complexity | Timeline |
|-------|------------|---------------|------------|----------|
| **4** | Voice tracks (loop) | ~$56 | Low | 1 weekend |
| **3** | Choose your own adventure | ~$61 | Medium | 1-2 weekends |
| **2** | AI chat (Mary's history) | ~$162 | High | 2-3 weekends |
| **1** | Full assistant + web | ~$170 + API | Very High | 1-2 more weekends |

---

## Recommended Path

### Start Here: Phase 4
1. Write scripts for 5-7 chapters
2. Generate audio with ElevenLabs
3. Order Pi Zero 2W and components (~$56)
4. Build and deploy

**Why Phase 4 first:**
- Lowest cost to validate
- Fastest to deploy
- Guests get magical experience immediately
- You learn the hardware integration
- Audio content is reusable in later phases

### Then Decide
After Phase 4 is live, you'll know:
- Do guests engage with it?
- Do they want interactivity?
- Is the audio quality right?
- Is the content compelling?

That feedback informs whether to invest in Phase 3, 2, or 1.

---

## Phase 4 Next Steps

1. **Write chapter scripts** (I can help draft these)
2. **Generate audio** with ElevenLabs
3. **Order hardware:**
   - Raspberry Pi Zero 2W
   - 32GB microSD card
   - USB audio adapter
   - Small speaker
   - Terminal blocks & jumper wires
   - USB-C power supply
4. **Build software** (simple Python audio player)
5. **Integrate with phone**
6. **Deploy!**

---

## Voice Selection for ElevenLabs

For Mary Lund Davis, consider:
- **Rachel** - Warm, mature, American
- **Charlotte** - Refined, articulate
- **Custom clone** - If you find reference audio of a similar voice/era

You can test voices at elevenlabs.io before committing to generation.
