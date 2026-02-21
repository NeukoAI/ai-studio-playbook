#!/bin/bash
# Lunar & Biodynamic Calendar Tool
# Usage: lunar.sh [today|week|holistic|YYYY-MM-DD] [location]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

show_lunar() {
    local date="$1"
    if [ -z "$date" ]; then
        python3 "$SCRIPT_DIR/lunar_calc.py"
    else
        python3 "$SCRIPT_DIR/lunar_calc.py" "$date"
    fi
}

format_output() {
    local data date phase emoji illum age cycle zodiac element elem_emoji movement move_sym
    local in_tips=false
    local tips=""
    
    data=$(cat)
    
    # Parse all data first
    while IFS= read -r line; do
        if [[ "$line" == TIPS:* ]]; then
            in_tips=true
            continue
        fi
        
        if [ "$in_tips" = true ]; then
            # This is a tip line
            tips+="$line"$'\n'
        else
            # Parse key:value pairs
            key="${line%%:*}"
            value="${line#*:}"
            case "$key" in
                DATE) date="$value" ;;
                PHASE) phase="$value" ;;
                EMOJI) emoji="$value" ;;
                ILLUMINATION) illum="$value" ;;
                AGE) age="$value" ;;
                CYCLE) cycle="$value" ;;
                ZODIAC) zodiac="$value" ;;
                ELEMENT) element="$value" ;;
                ELEMENT_EMOJI) elem_emoji="$value" ;;
                MOVEMENT) movement="$value" ;;
                MOVEMENT_SYMBOL) move_sym="$value" ;;
            esac
        fi
    done <<< "$data"
    
    # Display formatted output
    echo "🌙 Lecture Lunaire — $date"
    echo ""
    echo "$emoji  $phase ($cycle)"
    echo "   Illumination: ${illum}%"
    echo "   Âge lunaire: ${age} jours"
    echo ""
    echo "$elem_emoji  Jour $element (constellation: $zodiac)"
    echo "$move_sym  Lune $movement"
    
    # Display tips
    if [ -n "$tips" ]; then
        echo ""
        echo "📋 Recommandations Biodynamiques:"
        echo "$tips"
    fi
}

case "${1:-today}" in
    today)
        show_lunar "" | format_output
        ;;
    
    week)
        for i in {0..6}; do
            date=$(date -d "+$i days" +%Y-%m-%d 2>/dev/null || date -v+${i}d +%Y-%m-%d)
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            show_lunar "$date" | format_output
            echo ""
        done
        ;;
    
    holistic)
        location="${2:-Canton+de+Vaud}"
        echo "🌍 Lecture Holistique — Environnement Complet"
        echo ""
        echo "━━━ MÉTÉO ━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        curl -s "wttr.in/${location}?format=%l:+%c+%t+%h+%w+%m" 2>/dev/null || echo "Météo indisponible"
        echo ""
        echo ""
        echo "━━━ LUNE & BIODYNAMIE ━━━━━━━━━━━━━━"
        show_lunar "" | format_output
        ;;
    
    *)
        # Assume it's a date in YYYY-MM-DD format
        show_lunar "$1" | format_output
        ;;
esac
