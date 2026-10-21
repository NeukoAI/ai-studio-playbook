# models-as-memes

A playbook for brands. Fine-tune an image model on your character, let your community remix it on your site, pay for it as marketing spend, and pick the best every week for your socials and GIPHY.

NEUKO ran this for G\*BOY. Fans made every GIF on giphy.com/gboy (398 uploads, 53.3M GIF views, read 2026-10-20), and 3,354 people made 156,251 generations on the generator (NEUKO's internal G\*BOY stats sheet, Feb 26 2026).

## Prerequisites

- Rights to a character, mascot or visual style.
- 10 to 20 clean images of it to train on, the same number the LoRA kit uses (playbook step 1 lists which).
- An inference provider account that can train and serve a LoRA (Replicate or fal).
- A small web app, or someone who can build one.
- A marketing budget you're willing to cap in credits.
- One person with an hour a week to pick winners.

## Steps

Open [`models-as-memes-playbook.md`](models-as-memes-playbook.md) and work through it in order:

1. Collect the assets.
2. Fine-tune the model. Training steps live in the LoRA kit, [`../train-a-character-lora/`](../train-a-character-lora/). If you copy this folder somewhere else, copy that kit too or fix the link.
3. Build the remix site (generate, edit, animate, share).
4. Set the credit budget.
5. Run the weekly pick and reward loop.
6. Upload winners to GIPHY and post them on your socials.
7. Set guardrails before launch.
8. Measure weekly.

## Copy-paste inputs

**Prompt prefix**, added server-side to every generation. Replace the brackets.

```
[TRIGGER_WORD], [character name], [one-line style, e.g. "2D cartoon, thick outlines, flat colors"], 
```

**Random-prompt template.** The site picks one item from each list.

```
{character} {action} {place}, {mood}, {style}

action: eating ramen, waiting for a bus, falling off a skateboard, holding a tiny umbrella, sending an email
place: in the rain, on a rooftop at night, in a grocery store, underwater, at a 1980s mall
mood: smug, panicked, sleepy, proud, heartbroken
style: claymation, 1990s anime, pixel art, oil painting, vintage toy ad
```

**Terms line** for sign-up. Have your lawyer check the wording.

```
By submitting an image, you let [Brand] repost it, upload it to GIPHY and use it in our social posts, with credit to your username.
```

**Weekly pick checklist.**

```
[ ] Character is on-model
[ ] Clear joke or feeling in one look
[ ] Something you'd send a friend as a reply
[ ] Passes the do-not-make list
[ ] PG
[ ] Maker's username recorded
```

## What you should end up with

- A LoRA that puts your character into new scenes without hand-fixing (8 of 10 test prompts).
- A live site with Generate, Random, Edit, Animate and Share, behind a login, with credits.
- A capped spend. In the playbook's worked example, 1,000 fans × 50 credits caps model spend at $1,750 (derived from fal prices read 2026-10-20).
- A weekly post of fan-made winners on your socials, and a GIPHY brand channel that grows every week.
- One sheet with users, generations by mode, spend, submissions and GIPHY views.

## Credit

Written by NEUKO. Numbers are from NEUKO's own G\*BOY stats and public pages, with sources at the end of the playbook.
