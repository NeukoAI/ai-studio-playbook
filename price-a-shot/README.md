# Shot cost sheet

Work out what an AI video shot, or a whole episode, costs before you generate it. You fill in your own models, prices and re-roll counts. The sheet does the math.

The formula:

```
cost of a shot = takes x price per second x seconds
episode cost   = all shots + start frames + voice + review
```

Most people underestimate takes. A take is every generation you pay for, including the ones you throw away.

## What you need

- A spreadsheet app (Google Sheets, Excel or Numbers).
- The pricing page for each model you use. Prices change often, so write down the date you read them.
- Your own log of how many takes each kept shot took. If you have no log yet, start one today. Keep a tally per shot.

## Files

| File | What it is |
|---|---|
| `shot-cost-sheet.csv` | The template. The `cost` column has formulas. Open it in a spreadsheet app and they calculate. |
| `example-60s-episode.csv` | A filled 60-second episode. Example, derived. |
| `example-model-drop-01.csv` | One 5-second G\*BOY shot run through 6 video models, priced at public list prices. Derived from our generation log. |

## Steps

1. Import `shot-cost-sheet.csv` into your spreadsheet app. In Google Sheets, use File, Import, Upload, and choose "Replace spreadsheet".
2. Add one row for each kind of shot. Insert each new row above the blank "add new shots above this row" line. The review and total formulas sum everything above `review`, so a row added below `review` or `total` is not counted. Fill in these columns:
   - `shot`: a name you will recognize, such as "video shots (12 x 5s)".
   - `model`: the model and the resolution. The price depends on the resolution.
   - `seconds`: the length of one take. For a still image, put `1`.
   - `price per second`: from the model's pricing page. For a still image, put the price of one image.
   - `takes`: the total generations for this row, including the rejected ones. For 12 shots at 3 takes each, put `36`.
3. Copy the formula into the `cost` column of each new row: `=C2*D2*E2` (change `2` to the row number). Rows inserted above the blank line are picked up by the review and total formulas on their own; the blank line stays in the range so inserting at its position grows the range.
4. Set the review row. It covers whatever you pay to check takes (an AI review tool, or a person's time). The template uses 18% of generation, which was our ratio. Replace it with your own rate.
5. Read the total. That is generation cost only. It leaves out people's time, editing, music and licensing.

### Voice

ElevenLabs bills text to speech per character, not per second. Convert it:

```
price per second = (price per 1K characters / 1000) x characters per second
```

Our G\*BOY voiceover ran 576 characters in about 45 seconds, so about 12.8 characters per second. At $0.08 per 1K characters (v4), that is about $0.001 per second. Count your own script's characters and time one take to get your number.

## The 60-second example (example, derived)

12 shots of 5 seconds each, one start frame per shot, and one voiceover.

| Row | Model | Seconds | Price per second | Takes | Cost |
|---|---|---|---|---|---|
| start frames | Nano Banana 2 (2K) | 1 | $0.12 per image | 14 | $1.68 |
| video shots | MiniMax H3 Reference (768p) | 5 | $0.06 | 36 | $10.80 |
| voiceover | ElevenLabs v4 | 60 | $0.00102 | 4 | $0.24 |
| review | checking step | | | | $2.29 |
| **total** | | | | | **$15.01** |

The same episode on Seedance 2.5 Reference at 480p ($0.2205 per second) comes to about $49 with the same takes.

Where the takes come from:

- **Stills, 14.** Our log shows 8 stills for 7 keepers (one retake to fix a prop). That is about 1.14 takes per still, so 14 takes for 12 frames.
- **Video, 36.** This number is an assumption: 3 takes per kept shot. Our logs have only one production video shot, and it was kept on the first take. That is one data point, so we do not treat it as a rate. When we tested 6 models on one shot, we paid for 6 takes to keep 1. Replace 3 with your own count.
- **Voice, 4.** We generated 4 takes of the voiceover and used 1.

## What to expect

You get a total in dollars for one episode, and a cost per row. The row with the most takes is usually the biggest. To lower the total, reduce takes before you change models: write a tighter prompt, lock the first frame, and check a cheap draft before a full render.

## Prices used (read 2026-10-20)

| Model | Price | Page |
|---|---|---|
| MiniMax H3 Reference | $0.05/s at 480p, $0.06/s at 768p | https://fal.ai/models/minimax/h3/reference-to-video |
| Seedance 2.5 Reference | about $0.2205/s at 480p, $0.4730/s at 720p | https://fal.ai/models/bytedance/seedance-2.5/reference-to-video |
| Kling O3 Standard reference | $0.084/s audio off, $0.112/s audio on | https://fal.ai/models/fal-ai/kling-video/o3/standard/reference-to-video |
| Wan 3 | $0.05/s 480p, $0.10/s 720p, $0.20/s 1080p | https://fal.ai/models/alibaba/wan-3.0/text-to-video |
| Flux 3 (video) | $0.17/s 720p, $0.29/s 1080p | https://fal.ai/models/blackforestlabs/flux-3/text-to-video |
| Grok Imagine Video | $0.05/s 480p, $0.07/s 720p | https://fal.ai/models/xai/grok-imagine-video/text-to-video |
| Nano Banana 2 | $0.08 per image, 2K at 1.5x ($0.12) | https://fal.ai/models/fal-ai/nano-banana-2 |
| Nano Banana Pro | $0.15 per image | https://fal.ai/models/fal-ai/nano-banana-pro |
| ElevenLabs v4 text to speech | $0.08 per 1K characters | https://elevenlabs.io/pricing/api |
