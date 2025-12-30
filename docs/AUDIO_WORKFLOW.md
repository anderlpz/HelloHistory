# Audio Workflow

How to create, edit, and regenerate audio chapters for HelloHistory.

---

## Overview

```
scripts/
├── chapter_*.md              # Annotated scripts (human-readable, with notes)
├── voice_prompt.md           # ElevenLabs voice configuration
└── voice-tracks/
    └── *.txt                 # Clean text with SSML (sent to ElevenLabs)

src/audio/
└── *.mp3                     # Generated audio files (played by phone)
```

**Flow:**
```
Edit script → Update voice-track → Generate with ElevenLabs → Save MP3 → Test
```

---

## File Types

### 1. Chapter Scripts (`scripts/chapter_*.md`)

Human-readable scripts with annotations and notes for voice generation.

**Example:** `scripts/chapter_01_welcome.md`
```markdown
# Chapter 1: Welcome to Del Monte

**Duration:** ~2.5 minutes
**Style:** Warm documentary narrator

---

## Script

Welcome to Del Monte. [warmly] You've just picked up a piece of history.

In 1954, a young architect named Mary Lund Davis built this house...

[slight pause]

Now, Mary wasn't just any architect...

---

## Notes for Voice Generation

- Opening should feel like an invitation
- "Piece of history" - slight emphasis, intriguing
- Wonder at the $6,350 figure
```

### 2. Voice Tracks (`scripts/voice-tracks/*.txt`)

Clean text with SSML markup for ElevenLabs. These files are what you paste into ElevenLabs.

**Example:** `scripts/voice-tracks/01_welcome.txt`
```
[Chapter 1: Welcome to Del Monte]

You're staying in a piece of mid-century architectural history.

In 1954, a young architect named Mary Lund Davis built this house with her husband George. It was her first home, her office, and what she always called <break time="0.5s" /> her finest building.

<break time="1s" />

Now, Mary wasn't just any architect...
```

**SSML Tags Supported by ElevenLabs:**
- `<break time="0.5s" />` - Pause for specified duration
- `<break strength="medium" />` - Relative pause (weak, medium, strong)
- `<emphasis>word</emphasis>` - Emphasize a word
- `<prosody rate="slow">text</prosody>` - Adjust speaking rate

### 3. Voice Prompt (`scripts/voice_prompt.md`)

The voice configuration for ElevenLabs. Use this when creating/selecting a voice.

```
A 1960s documentary narrator. A woman in her 40s with a warm, refined 
voice - like a narrator from a mid-century educational film or the 
Wonderful World of Disney. She has that classic optimistic, earnest 
quality of postwar America. Articulate with clear enunciation, unhurried 
pacing, and genuine warmth. Neutral American accent with a slightly 
transatlantic quality.
```

### 4. Audio Files (`src/audio/*.mp3`)

Final MP3 files played by the phone. Named with numeric prefixes for ordering:

| File | Content |
|------|---------|
| `00_intro.mp3` | Brief intro/greeting |
| `01_welcome.mp3` | Chapter 1: Welcome to Del Monte |
| `02_marys_story.mp3` | Chapter 2: Mary's Story |
| `03_building.mp3` | Chapter 3: Building Del Monte |
| `04_design.mp3` | Chapter 4: The Design Philosophy |
| `05_other_work.mp3` | Chapter 5: Her Other Work |
| `06_closing.mp3` | Chapter 6: Closing |
| `07_song.mp3` | Bonus: Song |

---

## Editing a Chapter

### Step 1: Edit the Script

```bash
# Open the annotated script
code scripts/chapter_01_welcome.md
```

Make your changes. Keep the notes section updated for future reference.

### Step 2: Update the Voice Track

```bash
# Open the voice track (what ElevenLabs sees)
code scripts/voice-tracks/01_welcome.txt
```

Convert your script edits to clean text with SSML breaks:
- Replace `[pause]` notes with `<break time="0.5s" />`
- Remove annotation brackets like `[warmly]`
- Keep the text natural and readable

### Step 3: Generate Audio

**Option A: Manual (ElevenLabs Web)**

1. Go to [ElevenLabs](https://elevenlabs.io/app/speech-synthesis)
2. Select your saved voice (or create one using `voice_prompt.md`)
3. Paste the contents of your `.txt` file
4. Adjust settings:
   - Stability: ~50%
   - Clarity + Similarity: ~75%
   - Style: ~40-45%
5. Click Generate
6. Download the MP3

**Option B: Automated (see below)**

```bash
# Generate a single chapter
python3 scripts/generate_audio.py 01_welcome

# Generate all chapters
python3 scripts/generate_audio.py --all
```

### Step 4: Save the Audio

```bash
# Move/rename the downloaded file
mv ~/Downloads/ElevenLabs_*.mp3 src/audio/01_welcome.mp3
```

### Step 5: Test

```bash
make test
# Press 1 to hear Chapter 1
```

---

## Adding a New Chapter

### 1. Create the Script

```bash
# Create annotated script
cat > scripts/chapter_08_new_topic.md << 'EOF'
# Chapter 8: New Topic

**Duration:** ~X minutes
**Style:** Warm documentary narrator

---

## Script

Your script here...

---

## Notes for Voice Generation

- Note 1
- Note 2
EOF
```

### 2. Create the Voice Track

```bash
# Create clean text for ElevenLabs
cat > scripts/voice-tracks/08_new_topic.txt << 'EOF'
[Chapter 8: New Topic]

Your clean script text here with <break time="0.5s" /> SSML breaks.
EOF
```

### 3. Generate and Save Audio

Generate via ElevenLabs (manual or automated), save as `src/audio/08_new_topic.mp3`.

### 4. Update the Player

Edit `src/bench_player.py` to add the new track:

```python
self.tracks = [
    ("00_intro.mp3", "Intro"),
    ("01_welcome.mp3", "Chapter 1: Welcome to Del Monte"),
    # ... existing chapters ...
    ("08_new_topic.mp3", "Chapter 8: New Topic"),  # Add this line
]
```

Also update `src/phone_player.py` when it exists.

### 5. Test

```bash
make test
# Press 8 to hear Chapter 8
```

---

## Automated Generation (ElevenLabs API)

### Setup

1. Get your API key from [ElevenLabs](https://elevenlabs.io/app/settings/api-keys)

2. Save it to your environment:
   ```bash
   echo 'export ELEVENLABS_API_KEY="your-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. Install the SDK:
   ```bash
   pip install elevenlabs
   ```

### Usage

```bash
# Generate a single chapter
python3 scripts/generate_audio.py 01_welcome

# Generate all chapters
python3 scripts/generate_audio.py --all

# List available voices
python3 scripts/generate_audio.py --list-voices

# Preview without generating (dry run)
python3 scripts/generate_audio.py 01_welcome --dry-run
```

### Configuration

The script reads settings from `scripts/audio_config.yaml`:

```yaml
voice_id: "your-voice-id"      # From ElevenLabs
model_id: "eleven_monolingual_v1"
stability: 0.5
similarity_boost: 0.75
style: 0.45

chapters:
  - id: "00_intro"
    source: null  # No source file, uses inline text
    text: "Welcome to Del Monte. Pick up the receiver to begin."
  - id: "01_welcome"
    source: "voice-tracks/01_welcome.txt"
  - id: "02_marys_story"
    source: "voice-tracks/02_marys_story.txt"
  # ... etc
```

---

## Tips

### SSML Pacing

Use breaks to create natural pacing:

```
Short pause (half second):
<break time="0.5s" />

Medium pause (one second):
<break time="1s" />

Paragraph break (two seconds):
<break time="2s" />
```

### Voice Consistency

- Always use the same voice ID for all chapters
- Keep stability/similarity settings consistent
- Generate full chapters rather than stitching clips

### File Sizes

Target ~1MB per minute of audio. A 3-minute chapter should be ~3MB.
If files are too large, use a lower bitrate (128kbps is fine for speech).

### Version Control

- **Do commit:** Scripts (`.md`, `.txt`), config files
- **Do commit:** Final audio files (they're not huge)
- **Don't commit:** Temporary/test audio files

---

## Troubleshooting

### Audio sounds robotic
- Increase "Clarity + Similarity Enhancement" 
- Try a different voice
- Add more SSML breaks for natural pacing

### Pronunciation issues
- Use phonetic spelling: "Del Mon-tay" instead of "Del Monte"
- Add hyphens to break up words: "arch-i-tect"
- Use `<phoneme>` SSML tag for precise control

### Audio too fast/slow
- Use `<prosody rate="slow">` or `<prosody rate="fast">`
- Add more `<break>` tags
- Adjust the Style slider in ElevenLabs

### Generation fails
- Check API key is valid
- Check you have credits remaining
- Try shorter text (split into multiple generations)
