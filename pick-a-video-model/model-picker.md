# Model picker by job

Which video and image model NEUKO reaches for, by job. Every pick comes from one test: the same 5-second shot of our character G\*BOY, run once through 6 video models (October 2026), no rerolls, scored on the 15-point rubric in `rubric.md`.

Cost is relative. "1x" is what one 5-second MiniMax H3 take cost us. The other numbers divide each model's spend by that. They are derived from our own spend on one platform, so your prices will differ. Look up your platform's per-second price before you commit.

## The picks

| Job | Model | Score | Relative cost | Why |
|---|---|---|---|---|
| Keep a character on-model from a reference frame | MiniMax H3 (reference mode: opening still + front view) | 13/15 (on-model 5, motion 3, set 5) | 1x, the cheapest of the six | On-model from hood to sneakers for all 5 seconds, set untouched. The catch: the turn we asked for barely happened. |
| Hold the room exactly | Kling Omni (first frame + character reference) | 12/15 (4, 3, 5) | 1.9x | Kept our basement, palette and outfit. Froze for 3 seconds, then added a jazz-hands pose we never asked for. |
| Best face, close-ups | Seedance 2.5 Reference at 480p (opening still + front view) | 12/15 (5, 3, 4) | 3.7x at 480p (7.9x quoted at 720p) | Best face of the six: eyes, horned hood, jagged grin. Pushed into a close-up that cropped out the shorts and sneakers. Soft at 480p. |
| Cheap motion off a still (previz, motion tests) | MiniMax H3, image to video | Not scored | 1x | Same pick. We used it to animate one 1996-style still into 5 seconds at 768P for the same price as the scored take. |
| Prompt only, no frame | Wan 3 | 10/15 (3, 4, 3) | 3.3x | Best of the three prompt-only runs and the cleanest turn of all six. Redrew the horns as solid devil horns, made the eyes angry and the shirt mustard. |
| Stills (the opening frame every video starts from) | Nano Banana Pro with the front view as reference; Nano Banana 2 for look development | Not scored | 0.5x (Pro, one still), 0.27x (Nano Banana 2, one 2K still) | The three top-scoring takes all started from a Nano Banana Pro still. |

## The ones we don't pick, and why

| Model | Score | Relative cost | What broke |
|---|---|---|---|
| Grok Imagine | 8/15 (2, 4, 2) | 1.2x | Bolt-on black horns, orange shirt, olive shorts. The basement became a flat red void. Added a laugh we didn't ask for. |
| Flux 3 | 7/15 (2, 3, 2) | 2.8x | Head reads as a black blob until the hood pops in at 3 seconds. Black jacket over the shirt. The room went gray. |

The honest part: Wan 3, Grok Imagine and Flux 3 never saw our opening frame. The tool we ran them through accepted the image and then dropped it without an error, so all three ran text-to-video on the prompt alone. Their scores measure "prompt only", and they lost the character partly for that reason. All three clips open on a back view that isn't our still, which is how we caught it.

Lesson: look at frame 1 of every take. If it isn't the frame you uploaded, the model never got it.

## Rules we took from it

1. Give the model a frame. Every take that got our still plus a front view scored 12 or 13. Every prompt-only take scored 10 or less.
2. Pass a single front view as the character reference, never a turnaround sheet. Turnaround sheets leak into clips.
3. Don't name text, UI or the character's name in a prompt. Models print the words they're given.
4. Quote before you run. If a model quotes too high, drop the resolution first (Seedance 2.5 Reference quoted about 2.1x more at 720p than at 480p).
5. One take per model, scored from frames. A best-of-five comparison hides how often you'd re-roll.

## Limits

- One take per model, one shot, one character. This is a sample of one, not a benchmark.
- Scores are one person's read of the frames.
- Costs are ours on one platform at one date. Use the ratios, not the numbers.
