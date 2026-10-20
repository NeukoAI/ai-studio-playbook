# model-picker

Pick a video model by the job it has to do, and test new models the same way we do. One shot of your own character goes through several models, one take each, and each take gets a score out of 15.

By NEUKO. Our results from the first run are in `model-picker.md`.

## What's here

| File | What it is |
|---|---|
| `model-picker.md` | Our picks by job (character from a frame, room, face, cheap motion, prompt only, stills), with scores, relative cost and what broke |
| `rubric.md` | The 15-point rubric: on-model, motion, set + light, 1 to 5 each |
| `test-prompt.md` | The test shot as a template, plus our G\*BOY prompts as a worked example |
| `score-sheet.csv` | Our six scored takes. Copy it and add your rows. Delete our six example rows first, or keep them to compare |

## Prerequisites

- An account on any platform that runs image and video models through one interface, such as fal.ai, Replicate, or a node editor. You need one image model that accepts a reference image and three or more video models.
- A single front-view image of your character on a plain background. Not a turnaround sheet.
- `ffmpeg` installed (`brew install ffmpeg` on macOS).
- About an hour, most of it waiting on renders.

## Steps

1. **Write your checklists (10 min).** Open `rubric.md`. List 5 or 6 visual traits that make your character on-model, and 3 or 4 set pieces plus the main light. You score against these lists, so write them before you see any output.

2. **Fill in the test prompt (10 min).** Open `test-prompt.md`. Fill the brackets in the still prompt and the video prompt with the traits from your checklists. Choose one action and one expression change. After this, don't change the text between models.

3. **Make the opening still (5 min).** Run the still prompt on an image model that takes a reference image, with your front view as Image 1, at 9:16. Every video model gets this same still.

4. **Pick the models and check prices (5 min).** Choose 3 to 6 video models. For each, look up its per-second price on the platform's model page and write it in the `your_cost` column with the page URL and the date. If one costs far more than the rest, lower its resolution before you drop it.

5. **Run one take per model (15 to 25 min).** Settings: 5 s, 9:16, audio off where the model has the setting. Give each model the still as the first frame, and the front view as a reference image if it accepts one (see section 3 of `test-prompt.md` for how to cite images). Run each model once. Don't re-roll.

6. **Pull frames (2 min).** For each clip, from the folder the clips are in:

   ```bash
   mkdir -p frames
   for f in *.mp4; do
     ffmpeg -v error -y -i "$f" -vf "fps=1,scale=360:-2,tile=5x1" -frames:v 1 "frames/${f%.mp4}-strip.jpg"
     ffmpeg -v error -y -i "$f" -vf "fps=2,scale=180:-2,tile=10x1" -frames:v 1 "frames/${f%.mp4}-dense.jpg"
   done
   ```

   The strip has one frame per second. The dense sheet has two per second.

7. **Check frame 1 (1 min).** Compare the first frame of each strip with your still. If it's a different picture, the model never got your frame and ran on the prompt alone. Some tools accept an image and then drop it without an error. Mark that take "prompt only" and say so wherever you share the result.

8. **Score from the frames (10 min).** Use `rubric.md`. Give on-model, motion and set + light 1 to 5 each. Write one line for what held and one for what broke. Add a row to `score-sheet.csv`.

9. **Pick by job.** Sort by total, then read the columns. The top total is your default for keeping a character on-model. A take that tops one column but not the total (best room, best face, best motion) is your pick for that job. Relative cost = a take's `your_cost` divided by the lowest `your_cost` among takes scoring 12 or more, so the cheapest good take is 1.0.

## What to expect

- One scored row per model in `score-sheet.csv`, with a strip and a dense sheet per clip in `frames/`.
- In our run, models that got the still plus a reference scored 12 to 13 out of 15. Prompt-only runs scored 7 to 10, and every one of them redrew the character.
- Expect the cheapest model to win on at least one job. In ours, the cheapest take was also the top score.
- Expect surprises nobody asked for: a pose, a zoom, a laugh in the audio. Score them as motion faults.

## Limits

One take per model is a snapshot. It tells you how often you'd need to re-roll, which a best-of-five hides. It is not a benchmark. Re-run when a new model ships, with the same still and the same prompt, so the new row compares cleanly with the old ones.
