#!/usr/bin/env python3
"""
Lunar phase and biodynamic calendar calculator.
No external dependencies except standard library.
"""

import sys
import math
from datetime import datetime, timedelta

def julian_date(dt):
    """Convert datetime to Julian Date."""
    a = (14 - dt.month) // 12
    y = dt.year + 4800 - a
    m = dt.month + 12 * a - 3
    jdn = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    jd = jdn + (dt.hour - 12) / 24 + dt.minute / 1440 + dt.second / 86400
    return jd

def moon_phase(dt):
    """
    Calculate moon phase for given datetime.
    Returns: (phase_name, illumination_percent, age_days, emoji)
    """
    # Known new moon: 2000-01-06 18:14 UTC
    known_new_moon = datetime(2000, 1, 6, 18, 14)
    synodic_month = 29.530588861  # days
    
    diff = (dt - known_new_moon).total_seconds() / 86400
    phase_cycle = diff % synodic_month
    age = phase_cycle
    
    # Calculate illumination
    illumination = (1 - math.cos(2 * math.pi * phase_cycle / synodic_month)) / 2 * 100
    
    # Determine phase name
    if age < 1.84566:
        phase_name = "Nouvelle Lune"
        emoji = "🌑"
    elif age < 5.53699:
        phase_name = "Premier Croissant"
        emoji = "🌒"
    elif age < 9.22831:
        phase_name = "Premier Quartier"
        emoji = "🌓"
    elif age < 12.91963:
        phase_name = "Gibbeuse Croissante"
        emoji = "🌔"
    elif age < 16.61096:
        phase_name = "Pleine Lune"
        emoji = "🌕"
    elif age < 20.30228:
        phase_name = "Gibbeuse Décroissante"
        emoji = "🌖"
    elif age < 23.99361:
        phase_name = "Dernier Quartier"
        emoji = "🌗"
    elif age < 27.68493:
        phase_name = "Dernier Croissant"
        emoji = "🌘"
    else:
        phase_name = "Nouvelle Lune"
        emoji = "🌑"
    
    waxing = age < synodic_month / 2
    
    return {
        "phase": phase_name,
        "emoji": emoji,
        "illumination": round(illumination, 1),
        "age": round(age, 1),
        "waxing": waxing,
        "cycle_name": "Croissante" if waxing else "Décroissante"
    }

def zodiac_sign(dt):
    """
    Calculate zodiac sign for moon position (simplified tropical calculation).
    Returns constellation for Michel Gros calendar.
    """
    # Simplified: moon traverses zodiac ~monthly
    # This is approximate - real calculation needs ephemeris
    day_of_year = dt.timetuple().tm_yday
    lunar_month_offset = (dt.day / 29.53) * 360
    
    # Approximate zodiac position (simplified)
    signs = [
        ("Bélier", "Fruit", "🍎"),
        ("Taureau", "Racine", "🥕"),
        ("Gémeaux", "Fleur", "🌸"),
        ("Cancer", "Feuille", "🌿"),
        ("Lion", "Fruit", "🍎"),
        ("Vierge", "Racine", "🥕"),
        ("Balance", "Fleur", "🌸"),
        ("Scorpion", "Feuille", "🌿"),
        ("Sagittaire", "Fruit", "🍎"),
        ("Capricorne", "Racine", "🥕"),
        ("Verseau", "Fleur", "🌸"),
        ("Poissons", "Feuille", "🌿")
    ]
    
    # Rough approximation based on date (2.5 days per sign average)
    days_since_new_year = (dt - datetime(dt.year, 1, 1)).days
    # Moon takes ~27.3 days for zodiac cycle
    zodiac_cycle_days = 27.3
    position = (days_since_new_year % zodiac_cycle_days) / zodiac_cycle_days * 12
    sign_index = int(position) % 12
    
    return {
        "sign": signs[sign_index][0],
        "element": signs[sign_index][1],
        "emoji": signs[sign_index][2]
    }

def ascending_descending(dt):
    """
    Calculate if moon is ascending or descending.
    Simplified: based on zodiac position.
    Ascending: Sagittarius → Gemini
    Descending: Gemini → Sagittarius
    """
    zodiac = zodiac_sign(dt)
    ascending_signs = ["Sagittaire", "Capricorne", "Verseau", "Poissons", "Bélier", "Taureau", "Gémeaux"]
    
    is_ascending = zodiac["sign"] in ascending_signs
    
    return {
        "ascending": is_ascending,
        "name": "Montante" if is_ascending else "Descendante",
        "symbol": "↗️" if is_ascending else "↘️"
    }

def recommendations(phase_data, zodiac_data, asc_desc):
    """Generate biodynamic recommendations."""
    tips = []
    
    element = zodiac_data["element"]
    waxing = phase_data["waxing"]
    ascending = asc_desc["ascending"]
    
    # Day type recommendation
    if element == "Racine":
        tips.append(f"Jour Racine 🥕 : carottes, pommes de terre, oignons, radis")
    elif element == "Feuille":
        tips.append(f"Jour Feuille 🌿 : salades, épinards, choux, herbes")
    elif element == "Fruit":
        tips.append(f"Jour Fruit 🍎 : tomates, courges, haricots, arbres fruitiers")
    elif element == "Fleur":
        tips.append(f"Jour Fleur 🌸 : fleurs, brocoli, chou-fleur, artichaut")
    
    # Moon cycle recommendation
    if waxing and ascending:
        tips.append("🌱 Excellent pour SEMIS (sève monte, croissance active)")
    elif waxing and not ascending:
        tips.append("🌿 Bon pour PLANTATION/REPIQUAGE (croissance + enracinement)")
    elif not waxing and ascending:
        tips.append("✂️ Bon pour RÉCOLTE feuilles/fruits (sève haute, moins d'enracinement)")
    elif not waxing and not ascending:
        tips.append("🥕 Excellent pour RÉCOLTE conservation, TAILLE, TRAVAIL DU SOL")
    
    return tips

def main():
    if len(sys.argv) > 1:
        try:
            target_date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
        except:
            print(f"Invalid date format. Use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
    else:
        target_date = datetime.now()
    
    phase = moon_phase(target_date)
    zodiac = zodiac_sign(target_date)
    asc_desc = ascending_descending(target_date)
    tips = recommendations(phase, zodiac, asc_desc)
    
    # Output as simple parseable format
    print(f"DATE:{target_date.strftime('%Y-%m-%d')}")
    print(f"PHASE:{phase['phase']}")
    print(f"EMOJI:{phase['emoji']}")
    print(f"ILLUMINATION:{phase['illumination']}")
    print(f"AGE:{phase['age']}")
    print(f"CYCLE:{phase['cycle_name']}")
    print(f"ZODIAC:{zodiac['sign']}")
    print(f"ELEMENT:{zodiac['element']}")
    print(f"ELEMENT_EMOJI:{zodiac['emoji']}")
    print(f"MOVEMENT:{asc_desc['name']}")
    print(f"MOVEMENT_SYMBOL:{asc_desc['symbol']}")
    print("TIPS:")
    for tip in tips:
        print(f"  {tip}")

if __name__ == "__main__":
    main()
