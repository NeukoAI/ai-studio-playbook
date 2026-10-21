# The 15-point rubric

Three scores, 1 to 5 each, 15 max. Score from extracted frames, never from memory of watching the clip once.

## Before you score

Pull frames from every take (see `README.md` step 6, and check frame 1 per step 7). Look at frame 1 first. If frame 1 isn't the still you uploaded, the model ran on the prompt alone. Score it anyway and label it "prompt only".

## 1. On-model (1 to 5)

Does the character match the reference in every frame? Write your character's checklist before you run anything. Ours, for G\*BOY:

- red hood with two small horn points
- glowing white oval eyes
- jagged white grin
- yellow short-sleeve shirt
- sage green cargo shorts
- lilac high-top sneakers

## 2. Motion (1 to 5)

Did the one action you asked for happen, and nothing extra? Ours: he turns his head and shoulders to camera and a grin opens. Mark down for actions that didn't happen (a barely-there turn) and for actions nobody asked for (a pose, a zoom, an added laugh).

## 3. Set + light (1 to 5)

Did the room and the light survive? List the set pieces. Ours:

- wall of CRT monitors
- red emergency light in a wire cage
- pinned photos joined by red string
- bare concrete walls and floor

## How we read the scale

Our drop 01 scores were judgment calls against the checklists above. We wrote these anchors afterwards so the next run is easier to repeat:

| Score | On-model | Motion | Set + light |
|---|---|---|---|
| 5 | Every checklist item holds in every frame | The action happens fully, nothing extra | Every set piece and the light hold |
| 4 | One item drifts | The action happens, with one small extra or a weak beat | One set piece lost or changed |
| 3 | Two or three items wrong or drifting | The action is partial, or a large unasked action | Several set pieces lost, look still right |
| 2 | Recognizable as the character, most items wrong | The action barely happens and extras take over | The room is a different room |
| 1 | A different character | No usable motion | No set |

## Write down per take

- the three scores and the total
- `held`: what it got right, one line
- `broke`: what went wrong, one line
- input: "prompt + frame" or "prompt only"
- what it cost you (`your_cost`). Relative cost = your_cost divided by the lowest your_cost among takes that scored 12 or more; the cheapest good take is 1.0.

Use `score-sheet.csv` for this.
