# numbered-parts

A template for telling one story as numbered parts on IG and TikTok, plus the queries we used to check that parts beat re-uploads on our own account.

Our receipt: a fake 1996 zombie movie, posted as numbered parts on @neuko.ai. On IG, Parts 1 to 3 did 2.77M, 2.27M and 2.22M views. The 25 times we re-uploaded a piece we had already posted, the median was 790 views.

## Files

- `part-template.md` is the template: cold open, part card, cliffhanger, end card, length, posting gap, and the rule that nothing goes back up unchanged. Each rule shows what our Part 2 did, measured from the file.
- `content-type-table.md` is our table of views, saves and shares per content type, with the method and its limits.
- `content-types.sql`, `content-types-by-post.sql` and `reupload-thresholds.sql` are the queries behind that table.

## Use the template

Prerequisites: a story you can split into 3 or more parts, and an editor that exports 1080x1920 video. `ffmpeg` and `ffprobe` are optional, for checking your cut.

1. Split the story so each part ends on a new threat or a new character. Write the last shot of each part first.
2. For each part, put the strongest shot in the first 2 seconds. Put `PART N` on screen in frame one.
3. Keep the end card under 5 seconds.
4. Check the export:
   ```sh
   ffprobe -v error -show_entries format=duration -of csv=p=0 part-2.mp4
   ffmpeg -v error -ss 2 -i part-2.mp4 -frames:v 1 check-2s.jpg   # is this the shot you want people to stop on?
   ```
5. Post Part 1 on IG and TikTok within the same hour. Caption line 1: `part 1 of <title>`.
6. Post a teaser 1 to 4 days before each next part. Post the next part about a week after the last one.
7. Before posting anything you already ran, write down what is new: the cut, the hook, or a fork. If nothing is new, skip it.

Expected result: a filled-in checklist (bottom of `part-template.md`) per part, and a posting calendar with a part about every 7 to 10 days and a teaser between them.

## Check it on your own account

Prerequisites: `sqlite3`, and your posts in a SQLite file with the same shape as ours (`posts` with `platform, post_id, posted_at, kind, text`; `metric_snapshots` with `platform, post_id, captured_at, views, saves, shares`). Any export with one row per post works if you rebuild the table by hand.

1. Edit the `pieced` CASE in `content-types.sql` so your series captions map to pieces (`'my series p1'`, `'my series p2'`, and so on).
2. Run:
   ```sh
   sqlite3 -header -column your.db < content-types.sql
   sqlite3 -header -column your.db < content-types-by-post.sql
   ```
3. Expected output: one row per type with n, total and median views, saves and shares. Read the per-post listing to check every post landed in the right type.

Our numbers are in `content-type-table.md` for comparison.
