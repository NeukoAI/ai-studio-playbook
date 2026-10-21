#!/usr/bin/env bash
# Starts one paid training on Replicate. Read README.md "Cost" first.
# Usage: ./train.sh <your-replicate-username> <model-name> [fast|ostris]
# Edit train.json (fast, default) or train-advanced.json (ostris) first: set input_images and trigger_word.
set -euo pipefail
usage() { echo "usage: ./train.sh <your-replicate-username> <model-name> [fast|ostris]" >&2; exit 1; }

DIR="$(cd "$(dirname "$0")" && pwd)"
[ -n "${REPLICATE_API_TOKEN:-}" ] || { echo "export REPLICATE_API_TOKEN first" >&2; exit 1; }
[ $# -ge 2 ] || usage
OWNER="$1"
NAME="$2"
case "${3:-fast}" in
  fast)  TRAINER="replicate/fast-flux-trainer";    TRAINER_VERSION="e5a5bc821112c107e6ddb8491c5b898f94d06eaca861d1dbf37b29cd69ba8988"; BODY="$DIR/train.json" ;;
  ostris) TRAINER="ostris/flux-dev-lora-trainer";  TRAINER_VERSION="26dce37af90b9d997eeb970d92e47de3064d46c300504ae376c75bef6a9022d2"; BODY="$DIR/train-advanced.json" ;;
  *) usage ;;
esac

if grep -q "YOUR-HOST" "$BODY"; then
  echo "$BODY still has the YOUR-HOST placeholder in input_images. Put your dataset zip URL there first." >&2
  exit 1
fi

curl -fsS -X POST \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"owner\": \"$OWNER\", \"name\": \"$NAME\", \"visibility\": \"private\", \"hardware\": \"gpu-h100\"}" \
  https://api.replicate.com/v1/models || echo "model create failed (above); continuing in case the model already exists" >&2
echo

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT
sed "s#YOUR_USERNAME/YOUR_CHARACTER-lora#$OWNER/$NAME#" "$BODY" > "$TMP"

curl -fsS -X POST \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d @"$TMP" \
  "https://api.replicate.com/v1/models/$TRAINER/versions/$TRAINER_VERSION/trainings"
echo
echo "Check status: curl -fsS -H \"Authorization: Bearer \$REPLICATE_API_TOKEN\" https://api.replicate.com/v1/trainings/<id>"
