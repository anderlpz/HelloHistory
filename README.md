# HelloHistory

An AI-powered vintage rotary phone that lets guests "talk to" Mary Lund Davis, the pioneering architect who designed the Del Monte house in 1954.

## The Vision

When guests at the Del Monte short-term rental pick up the vintage rotary phone, they can have a conversation with Mary Lund Davis herself - asking about her life, the house she designed, Pacific Northwest modernism, and more.

This project honors Mary's legacy by bringing her voice back to her "finest building."

## About Mary Lund Davis

- First licensed female architect in Washington State after WWII
- Designed the Del Monte house in 1954 as her first home and office
- Founded Monitor Cabinets with her husband George
- Designed over 200 affordable "Fantastic Homes" in the 1960s
- Featured in Architectural Record's "Record Houses of 1964"

## Project Structure

```
HelloHistory/
├── .amplifier/           # Amplifier project configuration
├── docs/
│   ├── PROJECT_PLAN.md   # Overall project plan
│   ├── HARDWARE_SPEC.md  # Hardware components & wiring
│   └── SOFTWARE_SPEC.md  # Software architecture
├── knowledge/
│   ├── mary_biography.md # Mary's life story
│   ├── del_monte_facts.md# House-specific details
│   └── system_prompt.md  # AI character prompt
├── src/                  # Source code (coming soon)
└── hardware/             # Wiring diagrams (coming soon)
```

## Technology Stack

- **Hardware:** Raspberry Pi 5 (8GB) inside rotary phone shell
- **STT:** Vosk (offline speech recognition)
- **LLM:** Ollama + gemma2:2b (local inference)
- **TTS:** Piper (offline voice synthesis)
- **Trigger:** GPIO hook switch detection

## Development Status

- [x] Project planning & specifications
- [x] Mary's knowledge base extracted from thesis
- [ ] Voice pipeline prototype
- [ ] Raspberry Pi setup
- [ ] Phone hardware integration
- [ ] Field deployment

## Developed With

This project is developed with [Amplifier](https://github.com/microsoft/amplifier), an AI-powered modular development assistant.

## License

TBD
