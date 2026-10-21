---
name: news-post
description: Turn one news story into an Instagram or TikTok post in the news-aggregator style (a story carousel or a tweet-card reel) built on real sources, real logos, real footage and real quotes, with a slide plan, an asset list with credits, and a caption. Use when turning a news story, launch or link into a carousel or reel.
argument-hint: "[link to the story, or the story notes]"
---

# News post

Story: $ARGUMENTS

The news accounts that grow on Instagram and TikTok win on real material in a plain, fixed template: real people, real logos, real footage, real posts, one fact per slide. Designed motion-graphics and AI-generated filler read as generic, so this skill avoids them.

## Steps

1. **Read the story at its source.** Open the original article or announcement, then one or two other outlets that confirm it. Write down the facts with outlet and date. Done when every fact you will use has a source.
2. **Pick the format.** A story with strong source video (a launch film, a demo, a viral clip) becomes a tweet-card reel: a two-sentence headline with the key number in bold, over 20 to 40 seconds of the best source moments. A story with several beats (who, what happened, the twist, what's next) becomes a carousel of 5 to 8 slides. Done when the format and the beats are written down.
3. **Gather real assets**, one distinct visual per slide, each with a credit line.
   - **Logos:** Wikimedia Commons or the company's press kit. When two companies meet, put both logos side by side with a "×" between them.
   - **People:** an official portrait or press photo. Never a generated face.
   - **Product:** App Store or Play Store screenshots, press images, or charts from the source.
   - **Reactions:** posts from known accounts, quoted word for word, with name and handle.
   - **Video:** the outlet's or company's own clip, credited on screen.
   - Done when every slide has its own asset and every asset has a credit.
4. **Write the slides.** Carousel: a cover headline with the news plus the contrast that makes it interesting, then one question header per slide that the slide answers ("So what happened?", "Is it a done deal?"), then a "why this matters" slide that ends on a question. Keep each slide to one fact. Done when every fact on a slide matches step 1.
5. **Check the layout.** If you can render, look at all slides side by side. Fix text over faces, text in the bottom quarter of a 9:16 frame (the app's buttons cover it), and any slide without a visual or a credit. Done when all slides are clean.
6. **Write the caption.** The news in two lines with the outlet named, then a question that gets comments. Credit footage with the source handle.

## Output

A slide plan table `| # | Header | Text | Visual | Credit |` (or the reel's headline plus a timestamped clip list), the asset list with download links, and the caption. End with anything the user must confirm before posting, such as a figure only one outlet reported.

## Rules

- A figure reported by one outlet carries that outlet's name on the slide.
- Every slide carries a source or credit line.
- No em dashes and no stock AI phrasing in the copy.
- The agent never posts. The user reviews and posts.
