# HelloHistory Project

## Project Overview

HelloHistory is a hardware-software project being developed with Amplifier.

**Goals:**
- Develop the core hardware-software application
- Explore Amplifier extension opportunities (modules, tools, profiles, bundles)
- Contribute reusable components back to the Amplifier ecosystem

## Development Environment

- **Amplifier Profile:** `dev` (recommended for full development capabilities)

## Project Structure

```
HelloHistory/
├── .amplifier/           # Amplifier project configuration
│   └── AGENTS.md         # This file - project instructions
├── src/                  # Source code (to be created)
├── hardware/             # Hardware designs/schematics (to be created)
├── docs/                 # Documentation (to be created)
└── README.md             # Project readme (to be created)
```

## Amplifier Contribution Opportunities

As we develop this project, we may identify reusable components to contribute:

### Module Types
- **Providers** - LLM backend integrations
- **Tools** - Agent capabilities (filesystem, web, custom hardware tools)
- **Hooks** - Observability and control (logging, metrics, hardware events)
- **Orchestrators** - Conversation flow management
- **Context Managers** - Context handling strategies

### Other Contributions
- **Profiles** - Pre-configured capability sets for hardware development
- **Bundles** - Composable configuration units (markdown + YAML frontmatter)
- **Agents** - Specialized AI personas (e.g., hardware-debugger, pcb-reviewer)
- **Collections** - Groups of related modules/profiles/agents

## Development Guidelines

Follow the core philosophies:
- **Ruthless Simplicity** - Start minimal, grow as needed
- **Modular Design** - Self-contained, regeneratable components
- **Text-First** - Human-readable markdown and YAML formats

## Git Workflow

- Main branch: `main`
- Feature branches: `feature/<feature-name>`
- Always commit with descriptive messages
