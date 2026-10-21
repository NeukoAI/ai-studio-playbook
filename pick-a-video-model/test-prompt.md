# The test prompt

One 5-second shot, 9:16, the same text for every model. The template comes first, then our G\*BOY version as a worked example. Fill in the brackets once and don't change the text between models.

## The shot

5 s, 9:16. The character stands in their set, turns head and shoulders to camera, and one expression change happens. One action only, so motion is easy to score.

## 1. Opening still (image model, front view as Image 1)

Template:

> Vertical 9:16 [style] film still. The character from Image 1, exactly as drawn: [every visual trait from your on-model checklist]. Same [style] and proportions as Image 1. [Pose and framing: full body, three-quarter view, facing what]. Setting: [the room, with each set piece from your set checklist]. [The main light and where it falls]. [What fills the bottom of the frame]. [Mood words].

G\*BOY version (we ran this on Nano Banana Pro with a single front view as Image 1):

> Vertical 9:16 animated film still. The character from Image 1, exactly as drawn: a slim figure whose body is a glossy void-black silhouette, a red hood with two small horn points and a red cape knotted at the neck, glowing white oval eyes, a yellow short-sleeve shirt, sage green cargo shorts, white socks and lilac high-top sneakers. Same 2D cel-shaded cartoon style and proportions as Image 1. He stands full body in the center of the frame, three-quarter view, facing a wall of old CRT television monitors on the left that glow with blue-green static and scanlines. Setting: a cramped late-1990s hideout basement with bare concrete walls, exposed pipes, tangled cables, and a wall of pinned photos joined by red string behind him. One red emergency light in a wire cage on the ceiling bathes the room in red, with cool CRT glow on his left side. His feet rest on a plain concrete floor that fills the lower quarter of the frame. Moody, cinematic, high contrast.

## 2. Video prompt, first-frame models (the still as the first frame)

Template:

> The [character] in the first frame stands in the [set], [view], facing the [thing]. [The one action], [one secondary motion], and [the expression change]. Their design stays the same throughout: [the checklist, short]. The camera holds at [height] with a slow, slight push-in. [One light motion]. [Style].

G\*BOY version:

> The hooded character in the first frame stands in the red-lit basement, three-quarter view, facing the wall of CRT monitors. He turns his head and shoulders toward the camera, his red cape swinging with the turn, and a wide white jagged grin opens under his glowing white oval eyes. His design stays the same throughout: glossy black silhouette body, red horned hood, yellow shirt, sage green cargo shorts, lilac sneakers. The camera holds at chest height with a slow, slight push-in. The red emergency light pulses gently and the CRT screens flicker with static. 2D cel-shaded cartoon style.

## 3. Reference models (still + front view)

Same text, with the images cited the way each model expects:

- **Seedance-style `@Image` syntax.** Images: [still, front view]. Open with "Open on the exact frame of @Image1: the hooded character stands..." and say "His design matches @Image2 throughout".
- **MiniMax-style.** Same as above, cite them as `Image 1` and `Image 2`.
- **Kling Omni-style (first frame plus references).** First frame: the still. Reference images: [front view], cited as `@Image1`. Open with "The hooded character from @Image1 stands in the red-lit basement of the first frame...".

Check each model's own docs for how it cites images. The syntax changes between models and versions.

## Rules

- Never name text, UI or the character's name in the prompt. Models print the words they're given.
- Use a single front view as the character reference, never a turnaround. Turnarounds leak into the clip.
- Turn audio off where the model has the setting. Mute every clip when you compare.
