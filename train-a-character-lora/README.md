# Replicate LoRA kit: keep one character consistent

Train a FLUX LoRA of your character on Replicate, generate with it, or skip the LoRA and use reference images instead. Built from the pipeline NEUKO ran for G\*BOY and from Replicate's public docs as read on 2026-10-20.

Nothing in this folder runs by itself. `train.sh` and `train.py` start a paid training on your own Replicate account.

## Prerequisites

- A Replicate account with billing on, and an API token from https://replicate.com/account/api-tokens.
- `export REPLICATE_API_TOKEN=r8_...`
- For the Python scripts: Python 3.9+ and `pip install replicate`.
- For `train.sh`: your dataset zip at a public URL, put in `input_images` of `train.json` (or `train-advanced.json` for ostris) (S3, R2, a Drive direct link). `train.py` uploads a local zip for you.

## Files

| File | What it is |
|---|---|
| `dataset-checklist.md` | How many images, which angles, what to leave out |
| `caption-template.txt` | One caption pattern plus filled examples |
| `train.json` | Request body for `replicate/fast-flux-trainer` (the trainer Replicate recommends today) |
| `train-advanced.json` | Request body for `ostris/flux-dev-lora-trainer` (all the knobs: learning rate, rank, resolution) |
| `train.sh` | curl: create the destination model, then start a training. Optional third argument `ostris` uses `train-advanced.json` |
| `train.py` | Python: same, uploads your zip and polls until done |
| `generate.sh`, `generate.py` | Generate with your LoRA on `black-forest-labs/flux-dev-lora`; the Python one sweeps `lora_scale` |
| `reference_generate.py` | The no-LoRA route: new shots from a reference sheet on `google/nano-banana` |

## Steps

1. **Build the dataset.** Follow `dataset-checklist.md`. Put 10 to 20 images in a folder. Add one `.txt` caption per image using `caption-template.txt`. Zip the folder (images and `.txt` files at the zip root).
2. **Pick a trigger word.** A string that is not a real word, such as `CHRTOK`. Replace `CHRTOK` in `train.json` and in your captions.
3. **Start the training.** Either:
   - `python train.py <your-username> <character>-lora dataset.zip CHRTOK`
   - or upload the zip, put its URL in `train.json`, then `./train.sh <your-username> <character>-lora`
   Expected output: a training id, then status lines `starting`, `processing`, `succeeded`. Replicate's blog quotes under 2 minutes for this trainer.
4. **Generate.** `python generate.py <your-username>/<character>-lora "CHRTOK, three-quarter view, walking down a rainy street at night"`. Expected output: `lora-scale-0.7.png` through `lora-scale-1.2.png`. Pick the lowest scale where the character still reads as yours. Higher scales hold identity harder and fight the prompt more.
5. **If the character drifts,** check the dataset before touching settings: duplicate angles, inconsistent outfits and busy backgrounds cause most drift. Then try `training_steps` 1500, or move to `train-advanced.json` on the ostris trainer and raise `lora_rank` to 32.

To use the ostris trainer instead, edit `train-advanced.json` (dataset URL, trigger word) and run `./train.sh <your-username> <character>-lora ostris`. Its step field is `steps`, not `training_steps`. `train.sh` works from any directory, refuses to run while `YOUR-HOST` is still in the JSON, and shows HTTP errors. Both scripts create the model on `gpu-h100` hardware, which we could not check without a token; if model creation fails, create the model in the Replicate web UI and rerun.

## When to skip the LoRA

Use references (`reference_generate.py`) when any of these is true:

- You have fewer than 10 clean images of the character.
- You switch image or video models often. A FLUX.1 [dev] LoRA works on FLUX.1 [dev]. A new model means a new training.
- The character changes outfits or ages across the story.
- You are going to video. Video models take a reference frame directly. In our six-model G\*BOY test, the three models fed our frame scored 4 to 5 out of 5 on model; the three prompt-only runs scored 2 to 3.

Train a LoRA when you have 10 to 20 clean images, you will stay on one image model, and you need the same character across hundreds of images.

The reference route NEUKO moved to: make one clean seed image, generate a turnaround sheet (front, three-quarter, side, back) from it, then pass the sheet plus one or two hero frames as references for every new shot.

```
python reference_generate.py "the same character from the reference sheet, sitting on a rooftop at night, city lights behind, same outfit, same proportions" front.png three-quarter.png turnaround.png
```

Expected output: `reference-shot.png`.

## What we ran vs what Replicate runs today

Our numbers come from NEUKO's own code (read 2026-10-20). The "today" columns come from the live model pages and their input schemas on 2026-10-20.

| Setting | Ours: user LoRA pipeline | Ours: second pipeline (draft) | `replicate/fast-flux-trainer` today | `ostris/flux-dev-lora-trainer` today |
|---|---|---|---|---|
| Step field and value | `training_steps: 1000` | `steps`, default 100 | `training_steps`, default 1000 | `steps`, default 1000 (3 to 6000; README says 1000 to 3000) |
| Trigger word | random UUID per LoRA | character name, lowercase | default `TOK` | default `TOK` |
| Learning rate | not sent | 0.0001 | not exposed | default 0.0004 |
| Batch size | not sent | 1 (1 to 8) | not exposed | default 1 |
| Resolution | not sent | 512 (256 to 1024) | not exposed; ~1024 recommended | `512,768,1024` |
| LoRA rank | not sent | not sent | not exposed | default 16 (1 to 128) |
| Subject or style | not sent | not sent | `lora_type`, default `subject` | not exposed |
| Captions | none, trainer default | none | autocaption, or one `.txt` per image | Llava autocaption by default, or `.txt` |
| Max images | 200 cap | none set | 10 to 20 recommended, min 10 | min 10; README says 12 to 18 |
| Extra fields | none | `gradient_accumulation_steps`, `mixed_precision` | not in schema | not in schema |
| Generation guidance | 3.0, 28 steps, `lora_scale` 1.0 | 7.5, 28 steps | n/a | n/a |

Differences worth knowing:

1. Our user pipeline sent the same three fields the fast trainer takes today (`input_images`, `trigger_word`, `training_steps`). Today you also choose `lora_type`.
2. A random UUID trigger word works, but nobody can type it from memory. Use a short made-up token.
3. Our draft pipeline posted to `/v1/models/{owner}/{name}/versions`. Replicate's training endpoint is `/v1/models/{owner}/{name}/versions/{version_id}/trainings`. Its `gradient_accumulation_steps` and `mixed_precision` fields are not in either current trainer schema. We found no record that this pipeline ever trained a model.
4. Guidance 7.5 is an SDXL-era value. `flux-dev-lora` defaults `guidance` to 3 (range 0 to 10).
5. Our CMS stored the strength as `lora_weight`. Replicate's input is `lora_scale` (default 1, range -1 to 3).
6. The fast trainer README's curl example pins version `8b107946...`. The latest version on 2026-10-20 is `e5a5bc82...`, which this kit uses.
7. The ostris README says caption by file name (`a_photo_of_TOK.png`). The current input schema says one `.txt` per image. This kit follows the schema.
8. Replicate's 2024 blog prices ostris trainings on H100 at $0.001528/s. The live page says H200 at $0.001525/s.

## Cost

All prices from Replicate's public pages, read 2026-10-20. Check them again before you run anything.

| Item | Price | Source |
|---|---|---|
| Fast trainer | $0.0122 per second (8x H200) | https://replicate.com/replicate/fast-flux-trainer/train |
| Fast trainer, per run | "under 2 minutes", "under $2" | https://replicate.com/blog/fine-tune-flux (banner) |
| Ostris trainer | $0.001525 per second (H200) | https://replicate.com/ostris/flux-dev-lora-trainer/train |
| Ostris trainer, per run | 1000 steps "typically takes 20-30 minutes" | https://replicate.com/blog/fine-tune-flux |
| Generate with a LoRA | $0.032 per output image | https://replicate.com/black-forest-labs/flux-dev-lora |
| Reference route | $0.039 per output image | https://replicate.com/google/nano-banana |
| Hardware table | H100 and H200 both $0.001525/s | https://replicate.com/pricing |

Derived: 2 minutes on the fast trainer is about $1.46. 20 to 30 minutes on the ostris trainer is about $1.83 to $2.75. The `generate.py` sweep (4 images) is about $0.13.

Do not commit your token.

## Sources

- NEUKO's own LoRA training and generation code (not public), read 2026-10-20.
- Replicate HTTP API reference: https://replicate.com/docs/reference/http
- Replicate Python client: https://github.com/replicate/replicate-python
