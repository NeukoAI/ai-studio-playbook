# Models as memes: a brand playbook

Fine-tune an image model on your character or brand. Put it on your website. Give your community credits to remix it. Pick the best every week, post them with the maker's name, and put them on GIPHY.

We ran this for our character G\*BOY. Fans made every GIF on [giphy.com/gboy](https://giphy.com/gboy), which showed 398 uploads and 53.3M GIF views when we read it on 2026-10-20. On the generator site, 3,354 people made 156,251 generations (NEUKO's internal G\*BOY stats sheet, Feb 26 2026).

**Who this is for.** A brand, studio or IP owner with a recognizable character, mascot or visual style and an audience that already talks about it.

**What you need before you start.**

- Rights to the character and the assets you train on.
- Someone who can ship a small web app, or a no-code builder that can call an image API.
- An account with an inference provider that hosts LoRA models (we used Replicate, then moved to fal).
- A budget you can treat as marketing spend (step 4).
- One person who can review submissions for about an hour a week (step 5).

---

## Step 1. Collect the assets

The model only learns what you show it. Gather:

| Asset | How many | Notes |
|---|---|---|
| Character turnaround (front, 3/4, side, back) | 1 sheet, split into single views | Clean background. This anchors the silhouette |
| Expressions | 6 to 10 | Happy, angry, scared, smug. Memes run on faces |
| Poses and actions | 10 to 20 | Running, pointing, sitting, holding things |
| Scenes and lighting | 5 to 10 | Different backgrounds so the model learns the character, not the room |
| Brand marks you want kept | as needed | Colors, the outfit, props that make the character "yours" |
| Do-not-make list | 1 page | What the character never does. You'll need it for step 7 |

Rules of thumb:

- Vary everything except the character. If every image has the same background, the model will think the background is part of the character.
- Remove watermarks, text and logos you don't want generated.
- Keep only images you own or have cleared.
- The rows above add up to about 25 to 45 sourced images. Train on the best 10 to 20 of them, the number the LoRA kit asks for. More near-duplicates make the character drift.

## Step 2. Fine-tune the model

Train a LoRA, a small add-on file that teaches a base image model what your character looks like. You don't retrain the whole model.

Follow the kit in [`../train-a-character-lora/`](../train-a-character-lora/). It covers the dataset checklist, the trainer inputs we used, and the reference-based alternative if you can't train.

Done when 8 out of 10 test prompts in new settings ("[character] at a bus stop in the rain", "[character] as a 1980s action figure") look like your character without hand-fixing.

## Step 3. Build the remix site

Four features are the minimum. Here is what G\*BOY fans actually used, from the internal stats sheet of Feb 26 2026:

| Mode | What it does | Generations | Share (derived) |
|---|---|---|---|
| Create | Type a prompt, get your character in that scene | 63,120 | 40.4% |
| Random | One tap, no prompt needed | 60,222 | 38.5% |
| Edit | Change an existing image ("make it night", "give him a hat") | 15,859 | 10.1% |
| PFP | The sheet's label. Most likely profile-picture mode; the live site now shows a "Hood Up" tab instead | 7,919 | 5.1% |
| Animate | Turn a still into a short clip | 5,864 | 3.8% |
| Upscale | Make an image bigger and sharper | 3,143 | 2.0% |
| **Total** | | **156,251** | |

Source: NEUKO internal G\*BOY stats sheet, Feb 26 2026, tab "Daily Data", row 2026-02-26. The six modes add up to 156,127, which is 124 under the total column. Shares use the total.

What the split tells you:

- **About 79% of everything came from two buttons**, Create and Random (derived). Most people want one tap to a funny picture. Put those two first.
- **Random was almost as popular as Create.** A lot of people don't want to type. Build a good random-prompt list (your character plus a stock of situations, moods and styles).
- **Animate was under 4%** but it makes the GIFs. Keep it, and count on your best picks being animated by you or by your most active fans.

So build these, in this order:

1. **Generate.** Prompt box plus a Random button. Prepend your trigger word and a style line to every prompt so people can't drift off-model.
2. **Edit.** Upload or pick a past image and change one thing.
3. **Animate.** Image to a 3 to 6 second clip. Export as GIF and MP4.
4. **Share.** One tap to download, post to X or Instagram, or copy a link. Watermark lightly with your handle, and put the maker's username in the file name so you can credit them later.

Also needed:

- **Accounts.** Email or social login, so you know who made what and can reward them.
- **A gallery.** Each user's history, plus a public feed you can browse when picking.
- **A submit button.** "Submit to this week's picks." This is how the weekly loop starts (step 5).
- **Terms.** A short line at sign-up saying makers grant you the right to repost and upload their submissions with credit. GIPHY only gives upgraded channels to content owners uploading their own content ([GIPHY help, "Your GIPHY Account Has Been Flagged"](https://support.giphy.com/hc/en-us/articles/360019670992-Your-GIPHY-Account-Has-Been-Flagged)), so you need this grant before fan work goes on your channel.

## Step 4. Set the credit budget as marketing spend

Treat credits like a media budget. You know the most you can spend before you launch, and every credit you pay for becomes something a fan made with your character.

**Price one credit at or above one generation's cost.** Price the expensive modes in whole credits.

**Worked example (derived, all prices read 2026-10-20).**

| Input | Value | Source |
|---|---|---|
| Image cost | $0.035 per megapixel, so about $0.035 for a 1024×768 image | [fal.ai/models/fal-ai/flux-lora](https://fal.ai/models/fal-ai/flux-lora) |
| Animate cost | $0.27 for a 6 s 768p clip | [fal.ai/models/fal-ai/minimax/hailuo-02/standard/image-to-video](https://fal.ai/models/fal-ai/minimax/hailuo-02/standard/image-to-video) |
| 1 credit | $0.035 | our choice |
| Credits per mode | Create, Random, Edit, Upscale = 1 · Animate = 8 | 8 × $0.035 = $0.28, which covers $0.27. Assumes Edit and Upscale cost about one image; check your provider |
| Fans | 1,000 | your choice |
| Credits per fan | 50 | your choice |

- Total credits: 1,000 × 50 = **50,000**.
- Maximum model spend: 50,000 × $0.035 = **$1,750**, even if every fan uses every credit.
- If fans use credits the way G\*BOY fans did (96% stills, 4% animate), 50,000 credits buys about 45,000 generations (derived).
- G\*BOY averaged about 47 generations per user (156,251 ÷ 3,354, derived), so 50 credits each is close to what a real fan uses.

What the example leaves out: LoRA training (see step 2), hosting, moderation API calls, and your team's time. Prices change, so re-read the provider pages before you set your budget.

**Options:**

- **Free credits only.** Cleanest for a brand. Spend is capped.
- **Free starter credits, then paid packs.** G\*BOY sold credit packs. Its credits page said credits "cover the electricity plus a little extra". The sheet logged 1,446 transactions by 2026-02-26.
- **Top-ups as rewards.** Give weekly winners more credits (step 5). It costs you cents and keeps your best makers making.

## Step 5. Run the weekly pick and reward loop

This is how the G\*BOY GIPHY channel got filled. In Austin's words, "we picked the best submissions every week."

Every week:

1. **Collect.** Pull everything submitted that week, plus anything people posted with your tag.
2. **Shortlist.** One person picks 10 to 20. Look for a clear joke or feeling, a recognizable character, and something people would send to a friend.
3. **Review** each pick against your guardrails (step 7).
4. **Post the winners** on your socials with the maker's handle in the caption.
5. **Reward.** The picks that get shared most get more credits, a repost, a feature, merch, or a shout-out on stream. Reward shares, since shares are what spread the character.
6. **Upload** the winners to GIPHY (step 6).
7. **Tell everyone** what won and why, so next week's submissions get better.

Keep the cadence fixed. Same day, same time.

## Step 6. Amplify on GIPHY and your socials

GIPHY puts your GIFs inside the GIF search people already use. For G\*BOY it is where most of the views came from: 53.3M GIF views across 398 uploads (read 2026-10-20).

1. **Apply for a brand channel.** [Apply For A Brand Channel](https://support.giphy.com/hc/en-us/articles/360019977992-Apply-For-A-Brand-Channel). Brands need a company-domain email, a username that matches the business, a working website, a public social profile and at least 5 uploads ([Tips For Submitting An Application](https://support.giphy.com/hc/en-us/articles/360020433711-Tips-For-Submitting-An-Application)).
2. **Upload in batches** each week. Tag with your character name, the emotion or reaction ("happy", "help", "evil smile"), and the action. GIPHY allows up to 20 tags per upload, no "#" needed ([How to Upload](https://support.giphy.com/hc/en-us/articles/360019977552-How-to-Upload)).
3. **Think reactions.** The GIFs that travel are ones people send as replies: yes, no, help, success, mood. Tags on the first page of our channel include "mood", "success", "help" and "evil smile".
4. **Keep it PG.** GIPHY says most of its large API partners only accept PG content and below ([GIPHY Clips Best Practices](https://support.giphy.com/hc/en-us/articles/360045679212-GIPHY-Clips-Best-Practices)). A higher rating means fewer places your GIFs can show up.
5. **Credit the makers** in the GIF description and in your social post.
6. **On socials**, post the weekly winners as a carousel or a short reel, and repost fans' own posts. Label the work clearly, for example "fan-made, curated by [brand]".

## Step 7. Brand-safety guardrails and moderation

Set these up before launch.

- **Prompt filter.** Block words and topics from your do-not-make list, plus the usual (sexual content, violence against real people, hate, other brands' trademarks, real public figures). The live G\*BOY generator has a built-in "spicy content detected" warning (in the page on 2026-10-20).
- **Output check.** Run an image-safety classifier on every output before showing it. Blur or block anything flagged.
- **Locked style.** Prepend the trigger word and a style line server-side so people can't remove them.
- **Nothing goes out under your name without a human review.** The site output is the fan's. Your channel output is yours. The weekly pick is your quality gate.
- **Report and takedown.** A report button on every public image, and a named person who answers within a day.
- **Rate limits.** Credits cap spend. Also cap generations per minute per account to stop scripts.
- **Disclosure.** Label AI-made, fan-made work as such wherever you post it.
- **Rights.** Your terms grant you repost rights (step 3). Keep a record of who made each pick.

## Step 8. What to measure

Track weekly, in one sheet. G\*BOY's sheet tracked users, transactions, total generations, generations by mode and error rate per day.

| Metric | Why |
|---|---|
| New users, active users | Is the community showing up? |
| Generations, by mode | What people actually use. Cut what nobody touches |
| Generations per user | Depth. G\*BOY averaged about 47 (derived) |
| Credits spent vs budget | Your marketing spend, live |
| Error rate | G\*BOY's ranged from 0 to 14.52% between Jan 13 and Feb 26. Failed generations cost you goodwill and credits |
| Submissions per week | Health of the weekly loop |
| GIPHY views and uploads | Reach that compounds |
| Shares and saves of weekly-pick posts | Which picks travel. Feed this back into rewards |
| Cost per 1,000 GIF views | Total spend ÷ GIPHY views × 1,000. Compare it with your paid media CPM |

---

## Sources

| Claim | Source |
|---|---|
| 398 uploads, 53.3M GIF views | https://giphy.com/gboy, read 2026-10-20 |
| 3,354 users, 156,251 generations, 1,446 transactions, per-mode split, error % range | NEUKO's internal G\*BOY stats sheet, Feb 26 2026 (not public), daily data from 2026-01-13 to 2026-02-26 |
| Generator modes, credits copy, "spicy content detected" warning | https://www.gboyspecial.com/create and /credits, read 2026-10-20 |
| Weekly picks | NEUKO, G\*BOY team, 2026-10-20 |
| Image and animate prices | fal.ai model pages linked in step 4, read 2026-10-20 |
| GIPHY channel, upload and rating rules | support.giphy.com pages linked in steps 3 and 6, read 2026-10-20. If a link is blocked, search the page title: "Your GIPHY Account Has Been Flagged", "Apply For A Brand Channel", "Tips For Submitting An Application", "How to Upload", "GIPHY Clips Best Practices" |

Shares, averages, the 79% figure and the budget example are derived from these numbers.
