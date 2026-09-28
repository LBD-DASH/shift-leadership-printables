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
Last updated: 2026-09-28 06:35 SAST (Printables Repo agent)

### Done today
- Day 2 log: link to logs/2026-09-28.md (progress + next content + first weekly metrics).
- Prioritised One-on-One Meeting Template as next build (per Claude's Etsy demand research).
- Full Canva layout + paste-ready Etsy listing draft for the 1:1 in today's log.
- Merged SHARED_UPDATES across the four repos.

### Next up
- Layout the One-on-One Meeting Template in Canva from today's log (A4 + Letter PDFs into products/one-on-one-meeting-template/).
- Draft Weekly Team Check-in Sheet next.
- Make build scripts runnable from the repo alone.
- [KEVIN] Is the Shift Handover Sheet listing approved to go live on LBDShopSA? (yes/no)
- [KEVIN] Did AI help with the copy or layout of the Shift Handover Sheet (including Claude's 27 Sep critique)? (yes/no)
- [KEVIN] Use Claude's improved title/13 tags/description for the Shift Handover Sheet, or keep etsy/SHOP_COPY.md? (swap / keep)
- [KEVIN] Etsy seller + Payments and Gumroad status? (open / pending / not started)
- [KEVIN] Canva Free or Pro, and have you checked Canva's licence for selling templates? (Free / Pro)

### Instructions for Claude and ChatGPT
1. Turn the One-on-One Meeting Template draft in logs/2026-09-28.md into a paste-ready listing block matching etsy/SHOP_COPY.md style (title/13 tags/full description). Save as etsy/LISTING_ONE_ON_ONE.md or append to the log.
2. Live Etsy re-check for "one on one meeting template" and "team check in template" only: result count, top-5 prices USD, top-3 review counts. Append a dated table to logs/research-etsy-demand.md.
3. Critique the 1:1 page layout in today's log for printability (line height, section order, missing fields a real first-time manager needs). Output 5 specific fix suggestions as a numbered list in the log or a short file under logs/.

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
Last updated: 2026-09-28 06:42 SAST (Princess Baylin Repo agent)

### Done today
- YouTube handoff for Episode 1 at [`handoff/youtube/2026-09-28.md`](https://github.com/LBD-DASH/princess-baylin/blob/main/handoff/youtube/2026-09-28.md): beats, cast, lesson, hook, visual notes (EN primary; AF/ZU flagged).
- Day 2 log at [`logs/2026-09-28.md`](https://github.com/LBD-DASH/princess-baylin/blob/main/logs/2026-09-28.md): progress check, first ~12-spread picture-book manuscript (EN + AF/ZU flagged), 5 merch concepts, Monday weekly metrics baseline (recommend adjust).
- Recurring bedtime thank-you ritual noted for every episode ending.
- Pipeline equal-priority line already present; no further Pipeline edit needed.

### Next up
- Refine the picture-book manuscript (do not restart) once placeholders are confirmed or replaced.
- YouTube agent should build Ep 1 script from today's handoff at 06:43 SAST.
- Sketch a one-page character sheet for Baylin, Tilly and the Rainbird after Kevin's call on names.
- [KEVIN] Add the original story to `assets/story/` with identifying details removed? (yes this week / not yet)
- [KEVIN] Keep placeholder names Tilly, Sunhill and Rainbird, or replace them? (keep / replace)
- [KEVIN] Name one Afrikaans and one isiZulu native-speaker reviewer? (names ready / not yet)
- [KEVIN] Approve Episode 1 direction (listening + teamwork, soft rain, thank-you bedtime ritual) for book and YouTube? (yes / changes needed)

### Instructions for Claude and ChatGPT
1. **Language review of the book draft.** Read the Afrikaans and isiZulu manuscript sections in `logs/2026-09-28.md`. Output a markdown table with columns `language`, `spread`, `original`, `suggested`, `reason`. Save as `reviews/2026-09-28-language.md`. State that a human native speaker must still confirm.
2. **Character sheet draft.** From Day 1 and Day 2 logs, draft a one-page character sheet for Baylin, Tilly and the Rainbird: appearance bullets, catchphrase, one gentle flaw each, and a shared colour palette (hex codes). Save as `docs/character-sheet-draft.md`. No real child likeness.
3. **KDP trim checklist.** Research current Amazon KDP picture-book trim sizes suitable for ~24–32 pages with bleed. Output a short checklist with official source links at `docs/kdp-specs.md` (create or overwrite).
4. **Merch pricing sanity check.** For the five merch concepts in `logs/2026-09-28.md`, list comparable Etsy or POD price bands in ZAR or USD with 2 to 3 example listing links each (or "not found"). Save as `logs/research-merch-pricing-2026-09-28.md`.

## Faceless YouTube content (faceless-youtube-content), Princess Baylin bedtime-story channel (runs in parallel with princess-baylin)
Last updated: 2026-09-28 07:05 SAST (Faceless YouTube Repo agent)

### Done today
- Ep 1 full script at [`scripts/2026-09-28.md`](https://github.com/LBD-DASH/faceless-youtube-content/blob/main/scripts/2026-09-28.md) (from Baylin handoff/youtube/2026-09-28.md)
- Day 2 log + first Monday weekly metrics at [`logs/2026-09-28.md`](https://github.com/LBD-DASH/faceless-youtube-content/blob/main/logs/2026-09-28.md)
- Merged SHARED_UPDATES; Pipeline already equal-priority (no edit needed)

### Next up
- Hold production until Kevin answers open decisions below; do not create a channel, spend money, or buy API keys.
- After script approval: build a simple 12-scene shot board from the visual plan in `scripts/2026-09-28.md` (still drafts only).
- Keep Episode 2 as "Princess Baylin and the Sleepy Moon" (patience / night sky) once Baylin confirms beats.
- [KEVIN] Approve Ep 1 English VO in `scripts/2026-09-28.md`? (yes / changes needed)
- [KEVIN] Keep placeholders Tilly, Sunhill, Rainbird? (keep / replace)
- [KEVIN] Narrator for English: own voice, family voice, or disclosed Kokoro TTS? (own / family / Kokoro)
- [KEVIN] Channel name ready, and create channel when? (name ready / not yet)
- [KEVIN] Language format: English first, or AF/ZU in parallel after native check? (EN first / parallel later)
- [KEVIN] Art style: hand-illustrated (Krita) or AI-assisted with fixed character sheet? (hand / AI-assisted)
- [KEVIN] AI disclosure: always disclose AI voice or music, or only when YouTube strictly requires it? (always / strict-only)

### Instructions for Claude and ChatGPT
1. **Episode 2 outline.** Read princess-baylin `handoff/youtube/2026-09-28.md` and faceless-youtube-content `scripts/2026-09-28.md` (Ep 1 close teases Sleepy Moon). Write an outline for "Princess Baylin and the Sleepy Moon": 12 numbered scene beats (one or two sentences each), the lesson in one line (patience), a hook line for the first 15 seconds, and one visual note per scene. Night-sky setting. Save as `scripts/drafts/episode-2-outline.md` in faceless-youtube-content, or paste into chat for Kevin.
2. **Channel name shortlist.** Propose 10 channel names for a calm children's bedtime-story channel starring Princess Baylin. For each: name, one-line reason, and whether the matching @handle looks free (say "not checked" if you can't check). Plain markdown table. Paste in chat or save under `logs/channel-name-shortlist.md`.
3. **Narrator decision brief for Kevin.** In under 200 words, compare three options: Kevin's own voice, a family member's voice, and Kokoro-82M TTS (free, Apache 2.0, English only). Cover cost, time per episode, trust with parents, and YouTube's inauthentic-content risk. End with one recommendation. Paste in chat or save as `logs/narrator-brief.md`.
4. **Afrikaans and isiZulu TTS question.** Is there any text-to-speech voice for Afrikaans or isiZulu that is free and licensed for commercial use? List each candidate with licence and source link. If none, write "None found". Paste in chat or save as `logs/af-zu-tts-check.md`.
5. **Thumbnail style guide.** One-page guide for a hand-drawn or flat-illustration thumbnail style safe for made-for-kids: palette (hex codes), free fonts only, one layout rule, and 3 do/don't pairs. No real child's likeness. Save as `docs/thumbnail-style-guide.md` or paste in chat.

---

## Cross-project notes
- 2026-09-27 16:30 SAST (Grok Bot): All four repos share this file. Reusable ideas, such as a leadership theme that fits both the printables and YouTube, go here so the other projects can use them.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content): **Kevin's latest decision:** the YouTube channel and princess-baylin run **in parallel with equal weight**, and the channel isn't just a funnel. The Pipeline section above ("one business", "distribution layer") was written earlier, so Kevin should update its wording. It's left unchanged here because agents only edit their own section.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Made for kids turns off cards, end screens and the merchandise shelf** (https://support.google.com/youtube/answer/9527654). The channel can't sell Baylin books or merch through YouTube's merch features, and "heavily promotional" is a low-quality signal for kids content (https://support.google.com/youtube/answer/10774223). Book and merch sales need their own route (shop listing, book platform); don't rely on YouTube for them.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Story and character requests.** (1) A fixed character sheet for Baylin and each recurring friend (appearance, catchphrase, one flaw) so every episode looks consistent. (2) Episodes 2-4 should use new settings (for example night sky, river, market day) and new kinds of resolution (making amends, trying something new, patience), not listening again. (3) One small recurring bedtime ritual Baylin does at the end of every story, for a calm, familiar ending. (4) Please start `handoff/youtube/YYYY-MM-DD.md` with beats, cast, lesson, hook line and visual notes.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Title and theme ideas that hold watch time** (calm, no keyword stuffing, no distress-bait): "Princess Baylin and the Sleepy Moon", "Princess Baylin and the Quiet Star", "Princess Baylin and the River That Whispered", "Princess Baylin and the Very Patient Tortoise", "Princess Baylin Says Sorry". Themes: listening, patience, saying sorry, sharing, being brave in a small way, gratitude.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Possible book and merch items from Episode 1:** a "Lost Rain Song" picture book (12 spreads, trilingual); a rain-song colouring page set (frogs, grasshoppers, the grandmother tree, the Rainbird); a printable "Listen... what do you hear?" bedtime listening card; a Tilly the tortoise plush (once the cast is confirmed as canon); a trilingual goodnight poster ("Thank you, friends!" / "Dankie, vriende!" / "Siyabonga, bangane!", after the native-speaker check).
- 2026-09-27 16:45 SAST (Grok Bot): Kevin merged Princess Baylin and Faceless YouTube into one revenue pipeline (see the Pipeline section at the top). The Printables and AI Stock Images projects are unchanged.
- 2026-09-27 17:15 SAST (Grok Bot): Kevin decided book/merch and YouTube have equal priority; each feeds the other through this file.
- 2026-09-28 06:35 SAST (Printables Repo agent): Printables Day 2: building the One-on-One Meeting Template next (strongest Etsy demand signal). Shop name confirmed LBDShopSA.
- 2026-09-28 06:42 SAST (Princess Baylin Repo agent): YouTube handoff for Ep 1 is on path `handoff/youtube/2026-09-28.md`. Bedtime thank-you ritual locked as the recurring episode ending. Book manuscript draft and five merch concepts are in `logs/2026-09-28.md`. Please build today's YouTube script from the handoff (fall back to Day 1 log only if handoff is missing on main).
- 2026-09-28 07:05 SAST (Faceless YouTube Repo agent) for princess-baylin: **Story/character requests from Ep 1 scripting.** (1) Character sheet for Baylin, Tilly, and the Rainbird is still needed before production art (appearance, catchphrase, one gentle flaw, shared palette). (2) Episode 2 confirmed on the YouTube side as "Princess Baylin and the Sleepy Moon" with a patience theme and night-sky setting; please send a handoff when ready. (3) Thank-you bedtime ritual from your handoff is locked into the Ep 1 script close.
- 2026-09-28 07:05 SAST (Faceless YouTube Repo agent) for princess-baylin: **Watch-time title/theme ideas (calm).** Keep using series-consistent "Princess Baylin and the..." titles. Ep 1 title options used: Lost Rain Song / Listens for the Rain / The Day the Rain Song Came Home. Still strong for later: Quiet Star, River That Whispered, Very Patient Tortoise, Says Sorry. Avoid distress-bait and keyword stuffing.
- 2026-09-28 07:05 SAST (Faceless YouTube Repo agent) for princess-baylin: **Book/merch ideas sparked by the Ep 1 script.** (1) Printable "Listen... what do you hear?" bedtime listening card (matches the mid-story child pause). (2) Rain-song colouring set: frogs (drum), grasshoppers (patter), grandmother tree (hum), Rainbird (tune). (3) Trilingual thank-you poster: "Thank you, friends!" / "Dankie, vriende!" / "Siyabonga, bangane!" after native-speaker check. Shop/KDP URL stays a placeholder in the YouTube description until Kevin approves.
