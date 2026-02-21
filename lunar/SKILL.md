---
name: lunar
description: Get lunar phases, biodynamic calendar (Michel Gros method), and holistic environmental readings. Use when discussing moon influence, planting calendars, biodynamic agriculture, or requesting environmental/holistic context.
metadata: {"enki": {"emoji": "🌙", "requires": {"bins": ["python3", "curl"]}}}
---

# Lunar & Biodynamic Calendar

Provides lunar phase data and biodynamic calendar guidance based on Michel Gros principles for holistic environmental awareness.

## Quick Usage

```bash
# Current lunar phase + biodynamic day type
./scripts/lunar.sh today

# Weekly view (7 days)
./scripts/lunar.sh week

# Specific date
./scripts/lunar.sh 2026-02-25

# Holistic reading (moon + weather)
./scripts/lunar.sh holistic
```

## What It Provides

1. **Lunar Phases** — Current phase, illumination %, age, rise/set times
2. **Michel Gros Calendar** — Jour Racine/Fleur/Fruit/Feuille based on zodiac
3. **Montante/Descendante** — Ascending/descending moon (planting vs. harvesting)
4. **Croissante/Décroissante** — Waxing/waning (growth vs. consolidation)
5. **Recommandations** — Biodynamic guidance for farming/gardening tasks

## Moon Phases & Agriculture

### Croissante (Waxing) → Décroissante (Waning)
- **Croissante (🌒→🌕):** Sève monte, croissance aérienne, bon pour semis de plantes à fruits/feuilles
- **Décroissante (🌖→🌑):** Sève descend, enracinement, bon pour semis racines, taille, récolte conservation

### Montante → Descendante (Zodiac Position)
- **Montante:** Lune monte dans le ciel (Sagittaire→Gémeaux), sève monte, semis
- **Descendante:** Lune descend (Gémeaux→Sagittaire), sève descend, plantation/repiquage

### Les 4 Jours (Michel Gros)

Basé sur la constellation zodiacale traversée :

- **🌿 Jour Feuille** (Cancer, Scorpion, Poissons) — Salades, épinards, choux
- **🌸 Jour Fleur** (Gémeaux, Balance, Verseau) — Fleurs, brocoli, artichaut
- **🍎 Jour Fruit** (Bélier, Lion, Sagittaire) — Tomates, courges, arbres fruitiers
- **🥕 Jour Racine** (Taureau, Vierge, Capricorne) — Carottes, pommes de terre, oignons

## API Source

Uses combination of:
- **Astronomical calculation** (Python ephem library or algorithm)
- **Wttr.in** for basic moon emoji
- **Zodiac position calculation** for Michel Gros calendar

No API key required. All calculations local or free services.

## Holistic Reading

Combines lunar data + weather for complete environmental context:

```bash
./scripts/lunar.sh holistic Canton+de+Vaud
```

Returns:
- Current weather conditions
- Lunar phase & biodynamic day
- Recommendations for farming tasks

## Notes for Enki

- **Maraîcher context:** Always consider both croissante/décroissante AND montante/descendante
- **Optimal windows:** Best planting = jour approprié + lune favorable + météo correcte
- **Nœuds lunaires:** Avoid planting within 12h of lunar nodes (script warns)
- **Conservation:** Harvest root crops in lune décroissante, jour racine for best storage

---

*Gardien de la terre. Lecteur des cycles. Cultivateur du sens.* 🌙🐇
