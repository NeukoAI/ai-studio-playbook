# NeukoAI Agent Skills

AI entertainment stack — give your agent superpowers to create and sustain attention.

A public skill library for AI agents. Skills provide self-contained instructions that enable agents to interact with onchain protocols and APIs.

## Available Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [blowfish-launch-token](./blowfish-launch-token/) | Launch Solana tokens via the Blowfish Agent API | Active |
| [character-image-studio](./character-image-studio/) | Manage character visual identities and generate consistent images via the NeukoAI Image Studio API | Active |
| [lunar](./lunar/) | Get lunar phases, biodynamic calendar (Michel Gros method), and holistic environmental readings for agriculture | Active |
| [weather](./weather/) | Get current weather and forecasts via free APIs (wttr.in, Open-Meteo) — no API key required | Active |

## Usage Examples

### 🌾 Smart Farming Assistant

Combine **lunar** + **weather** skills for biodynamic agriculture guidance:

```
User: "Should I plant lettuce today?"

Agent uses lunar skill:
- Checks current moon phase (waxing/waning)
- Identifies biodynamic day type (Leaf/Root/Flower/Fruit)
- Determines if moon is ascending/descending

Agent uses weather skill:
- Checks current conditions and 3-day forecast
- Evaluates soil moisture and temperature

Agent responds:
"Today is a Leaf Day (🌿) with descending moon — perfect for 
transplanting lettuce. Weather: 12°C, light rain tomorrow will 
help establishment. Ideal timing."
```

**Why it matters:** Traditional biodynamic farmers track lunar calendars manually. These skills give any agent instant access to centuries-old agricultural wisdom + modern weather data.

### 🪙 Token Launch with Character Identity

Combine **blowfish-launch-token** + **character-image-studio**:

```
User: "Launch a token for my rabbit character."

Agent:
1. Uses character-image-studio to generate consistent avatar
2. Uploads image to IPFS via blowfish API
3. Launches token with image metadata
4. Returns CA + verified visual identity
```

### 🌙 Holistic Context Awareness

The **lunar** skill provides "holistic readings" that merge:
- Moon phase + zodiac position
- Biodynamic calendar recommendations
- Current weather conditions
- Seasonal context

Perfect for agents assisting with:
- Regenerative agriculture
- Permaculture planning
- Natural rhythms and cycles
- Outdoor event scheduling

## Quick Start

Point your agent at this repository to browse and install skills.

## Skill Structure

Each skill is a directory containing:

```
skill-name/
├── SKILL.md              # Core skill instructions (required)
├── references/           # Supplementary documentation (optional)
│   ├── topic-a.md
│   └── topic-b.md
└── scripts/              # Executable helper scripts (optional)
    └── helper.sh
```

### SKILL.md Format

Every `SKILL.md` includes YAML frontmatter and a markdown body:

```yaml
---
name: skill-name
description: What this skill does and when to use it.
metadata: {"neuko": {"emoji": "🎯", "homepage": "https://..."}}
---
```

The markdown body contains everything an AI agent needs to execute the skill: endpoints, authentication flows, code examples, error handling, and step-by-step workflows.

## Contributing

1. Fork this repository
2. Create a directory for your skill (lowercase, hyphenated)
3. Add a `SKILL.md` with frontmatter and complete instructions
4. Optionally add `references/` and `scripts/` directories
5. Submit a pull request

## License

MIT
