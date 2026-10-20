#!/usr/bin/env bash
# One image from your trained LoRA via black-forest-labs/flux-dev-lora (about $0.032 per image, Oct 20 2026).
set -euo pipefail
[ -n "${REPLICATE_API_TOKEN:-}" ] || { echo "export REPLICATE_API_TOKEN first" >&2; exit 1; }
LORA="${1:?usage: ./generate.sh <owner/model> \"CHRTOK prompt...\"}"
PROMPT="${2:?usage: ./generate.sh <owner/model> \"CHRTOK prompt...\"}"

curl -fsS -X POST \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: wait" \
  -d "{\"input\": {
        \"prompt\": \"$PROMPT\",
        \"lora_weights\": \"$LORA\",
        \"lora_scale\": 1,
        \"guidance\": 3,
        \"num_inference_steps\": 28,
        \"aspect_ratio\": \"4:5\",
        \"output_format\": \"png\",
        \"seed\": 7
      }}" \
  https://api.replicate.com/v1/models/black-forest-labs/flux-dev-lora/predictions
echo
