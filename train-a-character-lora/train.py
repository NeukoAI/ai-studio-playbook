"""Start one paid LoRA training on Replicate's fast FLUX trainer.

Usage: python train.py <your-username> <model-name> <dataset.zip> <TRIGGER>
Needs REPLICATE_API_TOKEN and `pip install replicate`.
"""
import os
import sys
import time

try:
    import replicate
except ImportError:
    sys.exit("Missing the replicate package. Run: pip install replicate")
from replicate.exceptions import ReplicateError

TRAINER = "replicate/fast-flux-trainer"
TRAINER_VERSION = "e5a5bc821112c107e6ddb8491c5b898f94d06eaca861d1dbf37b29cd69ba8988"


USAGE = "usage: python train.py <your-username> <model-name> <dataset.zip> <TRIGGER>"


def main(owner, name, zip_path, trigger):
    try:
        replicate.models.create(owner=owner, name=name, visibility="private", hardware="gpu-h100")
    except ReplicateError as e:
        print(f"model {owner}/{name} not created ({e}); using it if it already exists")

    with open(zip_path, "rb") as zip_file:
        training = replicate.trainings.create(
            model=TRAINER,
            version=TRAINER_VERSION,
            input={
                "input_images": zip_file,
                "trigger_word": trigger,
                "training_steps": 1000,
                "lora_type": "subject",
            },
            destination=f"{owner}/{name}",
        )
    print("training", training.id)

    while training.status not in ("succeeded", "failed", "canceled"):
        time.sleep(15)
        training.reload()
        print(training.status)

    print(training.status, training.output)


if __name__ == "__main__":
    if not os.environ.get("REPLICATE_API_TOKEN"):
        sys.exit("export REPLICATE_API_TOKEN first")
    if len(sys.argv) != 5:
        sys.exit(USAGE)
    if not os.path.isfile(sys.argv[3]):
        sys.exit(f"dataset zip not found: {sys.argv[3]}\n{USAGE}")
    try:
        main(*sys.argv[1:5])
    except ReplicateError as e:
        sys.exit("Replicate error: " + " ".join(str(e).split()))
