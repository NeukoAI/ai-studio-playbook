# Numbered part template

How we cut and post a story as numbered parts on IG and TikTok. Each rule comes from our fake 1996 zombie movie, which ran as numbered parts on @neuko.ai and @neukoai in Jul and Aug 2026. On IG, Parts 1 to 3 did 2,769,029, 2,269,406 and 2,224,768 views. Re-uploads of pieces we had already posted did a median of 790 (`content-type-table.md`).

## The template

| Beat | Rule | What Part 2 did (measured from the file) |
|---|---|---|
| Cold open | The most striking shot of the part fills 0 to 2 s. A monster, a reveal, a face in the lens. No title card or logo first. | A zombie sea witch charges the lens from 0 to 2.77 s. Black from 2.77 to 3.3 s. The story starts at 3.3 s. |
| Part card | The part number appears in the first frame as on-screen text (`PART 2`) and in the first words of the caption. | The caption opened with it: "part 2 of the lost 90s princess zombie movie (1996)". The video had no on-screen card in its first 4 s. Add one next time. |
| Story | One location or one goal per part. Cut every 2 to 6 s. | 44 scene changes in 120 s (ffmpeg scene detect at 0.3, end card and fades included), so about one every 2.7 s (derived). |
| Cliffhanger | The last shot before the end card introduces the next threat or character. The next part pays it off. | Last shot from 1:50.5 to 1:53.1: a captain at a ship's wheel. Part 3's caption tags him (#captainhook). |
| End card | Under 5 s. Then stop. | "The End, a NEUKO production" from 1:53.1 to 1:57.3, then black to 2:00. |
| Length | Our parts ran long. Part 2 is 120 s. Viewers watched an average of 45 to 48 s on IG and 26 to 34 s on TikTok. Put the cold open and the hook inside the first 30 s. | See the timing table below. |
| Posting gap | About a week between parts. Post a teaser 1 to 4 days before the next part. | 10.3 days to Part 2, then 7.9 days to Part 3. The Part 3 teaser went up 4.1 days early and did 621,403 views on IG. |
| Same day on both | IG and TikTok on the same day, within an hour. | Every part went up on both the same day: 32 min, 2 h 9 min and 5 min after IG. |
| Nothing goes back up unchanged | A piece that already ran comes back only as a new cut, a new hook or a fork (a new branch of the story). Never the same file. | 25 re-uploads on IG: median 790 views, 17 of 25 under 3,300. |

## Real timing, Parts 1 to 3

Dates and views from our IG and TikTok analytics (latest snapshot, captured 2026-10-15). Duration from `ffprobe`.

| Part | IG posted (UTC) | IG views | IG avg watch | TikTok posted (UTC) | TikTok views | TikTok avg watch | Gap since last part | File duration |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-07-31 14:14 | 2,769,029 | 48.01 s | 2026-07-31 14:46 | 1,580,721 | 28.12 s | n/a | not measured |
| 2 | 2026-08-10 20:50 | 2,269,406 | 46.92 s | 2026-08-10 22:59 | 389,639 | 33.9 s | 10.3 days | 120.05 s |
| 3 | 2026-08-18 19:31 | 2,224,768 | 44.6 s | 2026-08-18 19:36 | 1,175,312 | 28.9 s | 7.9 days | not measured |

Notes:
- **Durations.** We could measure only the Part 2 file. We matched it to Part 2 by its characters, but we have not confirmed it is the exact posted cut. Parts 1 and 3 were not available to measure.
- **IG avg watch** is the average watch time IG reports per post. For Part 2 it is 46.92 s of 120.05 s, about 39% (derived, and only if the file is the posted cut).
- **TikTok Part 2** was 2 h 9 min behind IG. Parts 1 and 3 went up 32 and 5 min after IG.
- **Teasers and extras between parts:** "another piece" clip Aug 7 (318,339 IG), Part 3 teaser Aug 14 (621,403 IG), Part 4 teaser Sep 3 (152,519 IG).
- **Part 4** posted Sep 4, 17.1 days after Part 3. Its IG views are disputed (215,982 on the first upload, 77,258 on a Sep 7 re-upload). See `content-type-table.md`.

## Checklist for the next part

1. The first 2 s show the strongest shot. Scrub the export to 0:02 and check.
2. `PART N` is on screen in frame one and first in the caption.
3. The last shot before the end card sets up Part N+1.
4. The end card runs under 5 s.
5. The next part's date is set, about a week out. The teaser is cut and scheduled 1 to 4 days before it.
6. IG and TikTok go up within the same hour.
7. Before posting anything from the library, name what is new: the cut, the hook, or the fork. If you can't, don't post it.

## Measure your own

Run the three `.sql` queries in this folder against your own post export, or rebuild the table by hand: one row per post, columns `type, views, saves, shares`, median per type. Use `ffprobe -v error -show_entries format=duration -of csv=p=0 part.mp4` for duration and `ffmpeg -i part.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep -c pts_time` to count cuts.
