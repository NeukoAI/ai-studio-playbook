"""Sweep lora_scale on one prompt so you can see where the character holds.

Usage: python generate.py <owner/model> "CHRTOK, three-quarter view, ..."
Cost: 4 images at about $0.032 each on black-forest-labs/flux-dev-lora (Oct 20 2026).
"""
import os
import sys

try:
    import replicate
except ImportError:
    sys.exit("Missing the replicate package. Run: pip install replicate")
from replicate.exceptions import ReplicateError

SCALES = [0.7, 0.9, 1.0, 1.2]


def main(lora, prompt):
    for scale in SCALES:
        out = replicate.run(
            "black-forest-labs/flux-dev-lora",
            input={
                "prompt": prompt,
                "lora_weights": lora,
                "lora_scale": scale,
                "guidance": 3,
                "num_inference_steps": 28,
                "aspect_ratio": "4:5",
                "output_format": "png",
                "seed": 7,
            },
        )
        image = out[0] if isinstance(out, list) else out
        path = f"lora-scale-{scale}.png"
        with open(path, "wb") as f:
            f.write(image.read())
        print(scale, path)


if __name__ == "__main__":
    usage = 'usage: python generate.py <owner/model> "CHRTOK, three-quarter view, ..."'
    if not os.environ.get("REPLICATE_API_TOKEN"):
        sys.exit("export REPLICATE_API_TOKEN first")
    if len(sys.argv) != 3:
        sys.exit(usage)
    try:
        main(sys.argv[1], sys.argv[2])
    except ReplicateError as e:
        sys.exit("Replicate error: " + " ".join(str(e).split()))
