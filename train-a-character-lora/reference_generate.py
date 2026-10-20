"""The no-LoRA route: new shots from a reference sheet with google/nano-banana.

Usage: python reference_generate.py "prompt" front.png three-quarter.png turnaround.png
Cost: about $0.039 per output image (Oct 20 2026). Up to a few refs; the turnaround does most of the work.
"""
import os
import sys

try:
    import replicate
except ImportError:
    sys.exit("Missing the replicate package. Run: pip install replicate")
from replicate.exceptions import ReplicateError


def main(prompt, *refs):
    out = replicate.run(
        "google/nano-banana",
        input={
            "prompt": prompt,
            "image_input": [open(p, "rb") for p in refs],
            "output_format": "png",
        },
    )
    with open("reference-shot.png", "wb") as f:
        f.write(out.read())
    print("reference-shot.png")


if __name__ == "__main__":
    usage = 'usage: python reference_generate.py "prompt" front.png [three-quarter.png ...]'
    if not os.environ.get("REPLICATE_API_TOKEN"):
        sys.exit("export REPLICATE_API_TOKEN first")
    if len(sys.argv) < 3:
        sys.exit(usage + "\nat least one reference image is required")
    missing = [p for p in sys.argv[2:] if not os.path.isfile(p)]
    if missing:
        sys.exit(f"reference image not found: {', '.join(missing)}\n{usage}")
    try:
        main(sys.argv[1], *sys.argv[2:])
    except ReplicateError as e:
        sys.exit("Replicate error: " + " ".join(str(e).split()))
