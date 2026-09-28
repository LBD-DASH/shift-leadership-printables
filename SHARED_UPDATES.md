# Shared updates across the four side-venture projects

This file lives in all four repos and is kept in sync:
- https://github.com/LBD-DASH/shift-leadership-printables
- https://github.com/LBD-DASH/ai-stock-images
- https://github.com/LBD-DASH/princess-baylin
- https://github.com/LBD-DASH/faceless-youtube-content

It gives anyone working on any one project (the repo agents, Claude, ChatGPT or Kevin) the full picture of all four: what's done, what's in progress, what's next, and what the others need.

## How to use this file (any AI or person)
1. **Read this whole file first**, then do your work in the repo you're in.
2. **Write your update back here**, only in the section for the project you worked on. Change its `Last updated` line (date, time in SAST, who) and edit Done, In progress, Next and Needs.
3. If you want to tell another project something, add a dated line under **Cross-project notes** at the bottom. Don't edit another project's section.
4. Keep each section short. Put details in that repo's `logs/` and link to them.
5. If you can only edit one repo (for example Claude or ChatGPT working in one chat), that's fine. The repo agents sync this file across all four repos on every daily run.

## Daily entry format (every project section, every day)
Each project section is a brief for the next AI. Rewrite your own section each run using exactly this structure, in this order:

```
## <Project name> (<repo-name>)
Last updated: YYYY-MM-DD HH:MM SAST (<who>)

### Done today
- What was finished today, with links to files or logs.

### Next up
- The next concrete steps for this project. Tag anything only Kevin can do with [KEVIN] and phrase it as a yes/no question.

### Instructions for Claude and ChatGPT
- One item per task, question or decision an outside AI should take on (work the repo agent can't do itself).
- Each item says exactly what to produce and what the output should look like (format, length, file path to save it to).
- If there is nothing, write: None today
```

Rules:
- The "### Instructions for Claude and ChatGPT" heading is always present. Never leave it out.
- Keep each section short; put detail in the repo's `logs/` and link to it.
- Only edit your own project's section. Notes for other projects go under Cross-project notes.
- A section still in the older Done / In progress / Next / Needs style is converted to this format the next time its owner updates it.

## Sync rule (for the repo agents)
On every run, the agent:
1. Reads `SHARED_UPDATES.md` from all four repos.
2. Builds a merged copy. For each project section, it keeps the version with the newest `Last updated`. It keeps every Cross-project note that appears in any copy, removes duplicates and sorts them by date.
3. Applies its own update.
4. Writes the merged file to all four repos on `main`.

Nothing is deleted without a note explaining why. The file stays plain markdown so any model can read and write it.

---

## Pipeline: Princess Baylin and Faceless YouTube (decided by Kevin, 2026-09-27; wording updated to equal priority)
These two repos run **in parallel with equal weight**. Neither exists only to feed the other. The repo names stay the same for now.
- **princess-baylin** owns the stories, characters, book manuscripts and merch concepts.
- **faceless-youtube-content** is a narrated Princess Baylin bedtime-story channel for children, with equal priority to the books and merch. Its scripts, titles, descriptions and thumbnails are built from Baylin material, and it sends story, title and product ideas back.
- **Handoff:** each Baylin run writes `handoff/youtube/YYYY-MM-DD.md` in princess-baylin, containing the story beats, the characters in the episode, the lesson, a hook line and visual notes. The YouTube agent reads the newest handoff. If none is newer than its last script, it uses the latest Baylin outline or manuscript.
- **Priorities:** Baylin works on children's book drafts (for Amazon KDP or print on demand) and merch concepts. YouTube works on scripts built for watch time and ad revenue. Both count equally.
- **Honest limit:** YouTube treats children's content as "made for kids", which means no personalised ads (so lower ad rates), no comments, no mini-player, and no cards, end screens or merch shelf. Book and merch sales therefore need their own routes rather than relying on YouTube features.
Book/merch and YouTube run in parallel with equal priority; each feeds the other through this file.
- **Rules that still apply:** English, Afrikaans and isiZulu, with a native-speaker check before anything is published. No identifying details about the child. AI use is disclosed where platforms require it. Everything is a draft for Kevin, and nothing is published or listed without his approval. No paid API key.

---

## Shift and leadership printables (shift-leadership-printables)
Last updated: 2026-09-27 18:05 SAST (Claude, same-day follow-up run)

### Done today
- First daily log: [`logs/2026-09-27.md`](https://github.com/LBD-DASH/shift-leadership-printables/blob/main/logs/2026-09-27.md). Day 1 of the 30-day plan, with a full spec for product #1 (Shift Handover Sheet) and outlines for the Weekly Team Check-in Sheet and One-on-One Meeting Template.
- Shift Handover Sheet built and rebranded to leadershipbydesign.co (navy #0F1F2E, teal #2A7B88, gold #C8A864, cream #F8F6F1; Playfair Display and Source Sans 3). A4 and US Letter PDFs are in `products/shift-handover-sheet/`. The shop icon, banner, 4 listing images and shop copy are in `etsy/`.
- Etsy shop name set: LBDShopSA (Leadership by Design account). `docs/ETSY_SETUP_CHECKLIST.md` and `docs/CLAUDE_DAILY_PROMPT.md` are in the repo.
- Claude did today's 3 "Instructions for Claude and ChatGPT" tasks (below), all logged in [`logs/2026-09-27.md`](https://github.com/LBD-DASH/shift-leadership-printables/blob/main/logs/2026-09-27.md) (new sections at the bottom) and [`logs/research-etsy-demand.md`](https://github.com/LBD-DASH/shift-leadership-printables/blob/main/logs/research-etsy-demand.md): (1) live Etsy demand check across the 5 target search terms, (2) an improved title/tags/description for the Shift Handover Sheet listing, (3) full page-by-page copy for the One-on-One Meeting Template.
- Headline finding: the One-on-One Meeting Template search term is the only one of the five with a proven, reviewed top-3 seller (11 reviews) — best next product to finish. "Shift planner printable" pulls the wrong audience (personal night-shift planners, not team-leader tools) and should be dropped as a tag.

### Next up
- Build the One-on-One Meeting Template in Canva from the copy in `logs/2026-09-27.md` (highest-demand product per today's research).
- Draft the Weekly Team Check-in Sheet as a paste-ready Etsy listing in the `docs/ETSY_SETUP_CHECKLIST.md` format, in the new brand.
- Make the build scripts runnable from the repo alone (they currently depend on fonts and brand images kept outside the repo).
- [KEVIN] Is the Shift Handover Sheet listing approved to go live on LBDShopSA? (yes/no)
- [KEVIN] Did AI help with the copy or layout? (yes/no; this sets the AI disclosure line — note Claude drafted the improved title/tags/description critique in `logs/2026-09-27.md` today, so if that critique is used, the answer is yes)
- [KEVIN] Use the improved title/13 tags/description opening Claude drafted today for the Shift Handover Sheet listing, or keep the current `etsy/SHOP_COPY.md` version? (yes to swap / no to keep)

### Instructions for Claude and ChatGPT
None today. Tomorrow: once Kevin answers the [KEVIN] questions above, the next useful task is turning the One-on-One Meeting Template copy into a paste-ready Etsy listing (title/tags/description, same format as `etsy/SHOP_COPY.md`), the same way item 2 above was done for the Shift Handover Sheet.

## AI stock images (ai-stock-images)
Last updated: 2026-09-28 06:35 SAST (Grok Bot, Day 2 daily run + Monday weekly metrics)

### Done today
- Day 2 of the 30-day plan logged in [`logs/2026-09-28.md`](https://github.com/LBD-DASH/ai-stock-images/blob/main/logs/2026-09-28.md): progress check, next-content batch, and first weekly metrics review (Monday).
- New niche-themed batch of 36 image prompts (titles + keywords + AI disclosure notes): Diwali/late-autumn festive still-life; soft wedding/engagement still-life (no people); material-specific textures (terrazzo, marble, linen). Chosen from Day 1 theme validation niches, not repeats of Day 1's broad holiday/Q1/abstract lists.
- Weekly metrics review: all upload/acceptance/download/earnings figures are unknown (none in the repo yet). Recommendation: **adjust**. Keep the project, stop inventing more theme batches until Kevin creates the Adobe account and approves a generator.
- Still no images generated or uploaded. No money spent, no API keys created, no stock uploads.

### Next up
- **[KEVIN]** Create the Adobe Stock Contributor account (ID check, W-8BEN, PayPal)? (yes started / not yet)
- **[KEVIN]** Approve Adobe Firefly Premium + Topaz Gigapixel Personal (≈R283/mo), or compare more? (approve / compare more)
- **[KEVIN]** Add `blackvault/new-income-ideas-2026-09-27.md` to `from-cto-new/`, or confirm it is not needed? (add it / not needed)
- Once both account and generator exist: generate a pilot of ~30 keepers from the lowest-saturation niches (Diwali, wooden-blocks growth, terrazzo/marble/linen), then curate, upscale, QA and upload with the generative-AI box ticked on every file.

### Instructions for Claude and ChatGPT
1. **Firefly stock-resale confirmation.** Check Adobe Firefly's current terms of use for whether outputs may be submitted to Adobe Stock for commercial licensing/resale. Return a short answer (yes / no / unclear) plus 3 to 5 quoted bullets with source URLs. Save as `from-cto-new/firefly-stock-resale-2026-09-28.md`. Do not sign up or buy anything.
2. **Pilot prompt shortlist.** From `logs/2026-09-27.md` and `logs/2026-09-28.md`, pick the 10 best niche prompts for a first generation pilot (prefer Diwali, wooden-blocks growth, terrazzo/marble/linen). Output a numbered list with prompt text, title template and the first 10 keywords each. Save as `from-cto-new/pilot-prompt-shortlist-2026-09-28.md`.
3. **Contributor setup checklist.** Write a one-page Adobe Stock Contributor setup checklist for a South African individual (account, ID verify, W-8BEN, PayPal, first-upload AI disclosure). Bullet list with official Adobe help links. Save as `docs/adobe-contributor-setup.md`.

## Princess Baylin (princess-baylin), the pipeline's source
Last updated: 2026-09-27 17:15 SAST (Grok Bot)

### Done today
- The first daily log was committed at `logs/2026-09-27.md` in commit `2cf1a6e`.
- Progress check: Day 1 of the 30-day plan, at the series bible stage.
- The episode outline is **Princess Baylin and the Lost Rain Song**, **Prinses Baylin en die Verlore Reënlied**, and **Inkosazana uBaylin neNgoma Yemvula Elahlekile**. The Rainbird has forgotten the song that brings rain. Baylin must listen and collect one piece of the song from each creature. The lesson is listening and teamwork.
- The log includes 10-step outlines, on-screen text and a 12-scene illustration list.
- Placeholder characters and setting are Tilly the tortoise, the Kingdom of Sunhill and the Rainbird.
- The daily routine is set to 06:37 SAST. The book, merch and YouTube pipeline restructure starts on 28 Sep.

### Next up
For the 28 Sep run:
- Push `handoff/youtube/2026-09-28.md` early for the YouTube handoff.
- Draft a picture-book manuscript of about 12 spreads, English first, with Afrikaans and isiZulu flagged for review, for KDP or print on demand.
- Propose 3 to 5 merch concepts, each with a platform and rough price.
- Run the progress check.

### Instructions for Claude and ChatGPT
1. Review the Afrikaans and isiZulu title and outline sections in `logs/2026-09-27.md` in a native-speaker style. Output a corrected version as a markdown table with columns `original`, `suggested` and `reason` in a new file at `reviews/2026-09-27-language.md`. State that a human native speaker must still confirm it.
2. Research current Amazon KDP picture-book specifications for trim size, page count and bleed. Output a short checklist with source links at `docs/kdp-specs.md`.
3. Propose 3 alternative names for Tilly, Sunhill and the Rainbird that work in English, Afrikaans and isiZulu. Output them as a table for Kevin to choose from.

Decisions for Kevin: add the original story to `assets/story/` with identifying details removed, and name the Afrikaans and isiZulu native-speaker reviewers.

Safety: Never include the child's face, real name details, school, location or other identifying details.

## Faceless YouTube content (faceless-youtube-content), Princess Baylin bedtime-story channel (runs in parallel with princess-baylin)
Last updated: 2026-09-27 17:15 SAST (Faceless YouTube Repo agent, new brief format)

### Done today
- Niche locked by Kevin: narrated Princess Baylin bedtime stories, made for kids, equal weight with princess-baylin.
- First daily log on main: [`logs/2026-09-27.md`](https://github.com/LBD-DASH/faceless-youtube-content/blob/main/logs/2026-09-27.md). It covers YouTube rules checked against official pages (made for kids, AI disclosure, Partner Program thresholds including the 8,000-hour bar for new applicants from 1 Feb 2027, inauthentic-content policy), a free tool shortlist with licence notes, and the Episode 1 video plan for "Princess Baylin and the Lost Rain Song".
- README and prompts rewritten for the locked niche so any model can pick up the work.
- Daily run scheduled for 06:43 SAST. No paid API keys are used.

### Next up
- Mon 28 Sep, 06:43 SAST: full 8 to 10 minute English script for Episode 1 in `scripts/2026-09-28.md` (hook in the first 15 seconds, calm pace, ending that leads into Episode 2), with 3 titles, description, thumbnail concept, chapter markers and AI disclosure notes. Built from the princess-baylin log of 27 Sep, because princess-baylin has no `handoff/youtube/` file yet.
- Mon 28 Sep: first weekly metrics review (no channel exists yet, so it will record a baseline of zero).

### Instructions for Claude and ChatGPT
1. **Episode 2 outline.** Read princess-baylin `logs/2026-09-27.md` for the cast and tone. Write an outline for "Princess Baylin and the Sleepy Moon": 12 numbered scene beats (one or two sentences each), the lesson in one line, a hook line for the first 15 seconds, and one visual note per scene. Use a night-sky setting and a patience-based resolution. Save it as `scripts/drafts/episode-2-outline.md` in faceless-youtube-content, or paste it into chat for Kevin.
2. **Channel name shortlist.** Propose 10 channel names for a calm children's bedtime-story channel starring Princess Baylin. For each, give the name, a one-line reason, and whether the matching @handle looks free (say "not checked" if you can't check). Plain markdown table.
3. **Narrator decision brief for Kevin.** In under 200 words, compare three options: Kevin's own voice, a family member's voice, and Kokoro-82M TTS (free, Apache 2.0, English only). Cover cost, the time per episode, trust with parents, and YouTube's inauthentic-content risk. End with one recommendation.
4. **Afrikaans and isiZulu question.** Answer: is there any text-to-speech voice for Afrikaans or isiZulu that is free and licensed for commercial use? List each candidate with its licence and a source link. If you find none, say "None found".
5. **Thumbnail style guide.** Write a one-page guide for a hand-drawn or flat-illustration thumbnail style that is safe for made-for-kids content: palette (hex codes), font suggestions (free fonts only), a layout rule and 3 do/don't pairs. No real child's likeness.

---

## Cross-project notes
- 2026-09-27 16:30 SAST (Grok Bot): All four repos share this file. Reusable ideas, such as a leadership theme that fits both the printables and YouTube, go here so the other projects can use them.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content): **Kevin's latest decision:** the YouTube channel and princess-baylin run **in parallel with equal weight**, and the channel isn't just a funnel. The Pipeline section above ("one business", "distribution layer") was written earlier, so Kevin should update its wording. It's left unchanged here because agents only edit their own section.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Made for kids turns off cards, end screens and the merchandise shelf** (https://support.google.com/youtube/answer/9527654). The channel can't sell Baylin books or merch through YouTube's merch features, and "heavily promotional" is a low-quality signal for kids content (https://support.google.com/youtube/answer/10774223). Book and merch sales need their own route (shop listing, book platform); don't rely on YouTube for them.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Story and character requests.** (1) A fixed character sheet for Baylin and each recurring friend (appearance, catchphrase, one flaw) so every episode looks consistent. (2) Episodes 2–4 should use new settings (for example night sky, river, market day) and new kinds of resolution (making amends, trying something new, patience), not listening again. (3) One small recurring bedtime ritual Baylin does at the end of every story, for a calm, familiar ending. (4) Please start `handoff/youtube/YYYY-MM-DD.md` with beats, cast, lesson, hook line and visual notes.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Title and theme ideas that hold watch time** (calm, no keyword stuffing, no distress-bait): "Princess Baylin and the Sleepy Moon", "Princess Baylin and the Quiet Star", "Princess Baylin and the River That Whispered", "Princess Baylin and the Very Patient Tortoise", "Princess Baylin Says Sorry". Themes: listening, patience, saying sorry, sharing, being brave in a small way, gratitude.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Possible book and merch items from Episode 1:** a "Lost Rain Song" picture book (12 spreads, trilingual); a rain-song colouring page set (frogs, grasshoppers, the grandmother tree, the Rainbird); a printable "Listen… what do you hear?" bedtime listening card; a Tilly the tortoise plush (once the cast is confirmed as canon); a trilingual goodnight poster ("Thank you, friends!" / "Dankie, vriende!" / "Siyabonga, bangane!", after the native-speaker check).
- 2026-09-27 16:45 SAST (Grok Bot): Kevin merged Princess Baylin and Faceless YouTube into one revenue pipeline (see the Pipeline section at the top). The Printables and AI Stock Images projects are unchanged.
- 2026-09-27 17:15 SAST (Grok Bot): Kevin decided book/merch and YouTube have equal priority; each feeds the other through this file.
