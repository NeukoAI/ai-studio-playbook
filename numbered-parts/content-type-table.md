# Content types on @neuko.ai (Instagram), May 26 to Sep 20, 2026

Built 2026-10-20 from our IG analytics (latest snapshot per post, captured 2026-10-15). 82 IG posts: 64 reels and image posts, 18 stories.

## Result

| Type | n | Views total | Views median | Views min | Views max | Saves total | Saves median | Shares total | Shares median |
|---|---|---|---|---|---|---|---|---|---|
| Numbered part 1 to 3, first upload | 3 | 7,263,203 | 2,269,406 | 2,224,768 | 2,769,029 | 124,594 | 41,829 | 203,943 | 52,189 |
| Numbered part 4, first upload (**disputed**, see below) | 1 | 215,982 | 215,982 | 215,982 | 215,982 | 3,806 | 3,806 | 4,825 | 4,825 |
| Series teaser or extra clip | 4 | 1,094,563 | 235,429 | 2,302 | 621,403 | 8,417 | 1,857 | 5,135 | 1,323 |
| Re-upload of a piece already posted | 25 | 758,359 | 790 | 0 | 457,277 | 10,305 | 4 | 11,253 | 5 |
| One-off reel | 23 | 4,538,225 | 39,128 | 7,700 | 2,256,440 | 20,123 | 50 | 200,203 | 45 |
| Image or carousel post | 7 | 352,240 | 18,927 | 1,402 | 217,135 | 2,391 | 38 | 31,551 | 14 |
| Story | 18 | 61,399 | 3,402 | 326 | 7,529 | n/a | n/a | n/a | n/a |

Re-uploads by view band (`reupload-thresholds.sql`): 17 of 25 under 3,300 views, 4 between 3,300 and 49,999, 4 at 50,000 or more. The 4 over 50k were zombie re-uploads posted 3 to 5 days after the original, while the series was still running: Part 1 on Aug 5 (457,277), Part 2 twice on Aug 15 (93,594 and 82,156), Part 4 on Sep 7 (77,258). Of the 19 re-uploads from Aug 20 on, 17 stayed under 3,300.

What the table says:

- The three numbered parts carry 7.26M of the account's 14.3M IG views in this window (derived: 7,263,203 / 14,283,971 summed from the table).
- Median saves: 41,829 per numbered part, 50 per one-off reel, 4 per re-upload.
- One-off reels can spike (Shabang 2.26M, "beauty machine" 1.43M), but their median is 39k.

## Part 4 is disputed

Two IG posts carry Part 4. The first upload (Sep 4) shows 215,982 views. A re-upload three days later (Sep 7) shows 77,258. Each has one snapshot, from 2026-10-15. The table counts the first upload and keeps Part 4 in its own row, so it doesn't move the Parts 1 to 3 numbers.

## How posts are typed

1. **Piece.** Each post maps to a piece by caption text: zombie Part 1 to 4, a zombie teaser per part ("drops next week", "drops soon", "trailer"), the "another piece" extra clip, and four named one-offs that were posted twice (Shabang, "beauty machine", "Eleven used PSYCHIC", "Peter and MJ"). Everything else is its own piece.
2. **Re-upload.** Any post that is not the earliest post of its piece.
3. **Type.** Stories, then re-uploads, then first uploads by piece (numbered part, teaser or extra, image post, one-off reel).

Limits:
- Caption text decides the piece. Whether a re-upload was the identical file was not checked: only the Part 2 video is on disk. Two Aug 15 Part 2 re-uploads carry different hashtags (#ariel, #thelittlemermaid), so they may be trims.
- "Don't Get Bit" (Jul 7) carries the `series:zombie` tag but is a different zombie series. The caption match on "zombie movie" keeps it out of the zombie pieces.
- One Sep 8 Part 4 re-upload shows 0 views. It may have failed or been deleted.

## Run it on your own posts

The queries are in this folder. Point them at a SQLite file of your own posts (see `README.md` for the table shape):

```sh
sqlite3 -header -column your.db < content-types.sql
sqlite3 -header -column your.db < content-types-by-post.sql
sqlite3 -header -column your.db < reupload-thresholds.sql
```
