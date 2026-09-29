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
Last updated: 2026-09-29 06:33 SAST (Printables Repo agent)

### Done today
- Day 3 log: link to logs/2026-09-29.md (progress + next content; weekly metrics skipped, not Monday).
- Updated One-on-One Meeting Template Canva brief with printability deltas vs Day 2 (Manager + Next 1:1 fields, hard ≥8 mm line heights, Actions before Feedback/Growth, privacy callout, tracker Next-1:1 column).
- Full Weekly Team Check-in Sheet Canva layout + paste-ready Etsy listing (title/13 tags/description/price) in today's log.
- Marked Claude's Day 2 Instructions 1 and 3 as used (listing rewrite + 1:1 critique). Live Etsy re-check (Instruction 2) still outstanding. Note: `etsy/LISTING_ONE_ON_ONE.md` and `logs/critique-one-on-one-layout-2026-09-28.md` are still missing from main.
- Merged SHARED_UPDATES across the four repos (faceless-youtube-content as merge base).

### Next up
- Layout the updated One-on-One Meeting Template in Canva (A4 + Letter PDFs into products/one-on-one-meeting-template/) using Day 2 brief + Day 3 deltas.
- Layout the Weekly Team Check-in Sheet in Canva from today's log (A4 + Letter into products/weekly-team-check-in/).
- If Claude still has local copies, commit the missing `etsy/LISTING_ONE_ON_ONE.md` and `logs/critique-one-on-one-layout-2026-09-28.md` to main.
- Make build scripts runnable from the repo alone.
- [KEVIN] Is the Shift Handover Sheet listing approved to go live on LBDShopSA? (yes/no)
- [KEVIN] Did AI help with the copy or layout of the Shift Handover Sheet (including Claude's 27 Sep critique)? (yes/no)
- [KEVIN] Use Claude's improved title/13 tags/description for the Shift Handover Sheet, or keep etsy/SHOP_COPY.md? (swap / keep)
- [KEVIN] Etsy seller + Payments and Gumroad status? (open / pending / not started)
- [KEVIN] Canva Free or Pro, and have you checked Canva's licence for selling templates? (Free / Pro)

### Instructions for Claude and ChatGPT
1. Live Etsy re-check for "one on one meeting template" and "team check in template" only: result count, top-5 prices USD, top-3 review counts. Append a dated table to logs/research-etsy-demand.md. (Still outstanding from Day 2; was blocked headless.)
2. Critique the NEW Weekly Team Check-in layout in logs/2026-09-29.md for printability (line height, section order, missing fields a real first-time team lead needs). Output 5 specific fix suggestions as a numbered list. Save as logs/critique-weekly-team-check-in-2026-09-29.md.
3. Rewrite the Weekly Team Check-in paste-ready listing from logs/2026-09-29.md into etsy/SHOP_COPY.md style (title/exactly 13 tags/full description with WHAT YOU GET / HOW TO USE / LICENCE / PLEASE NOTE / Designed by / AI disclosure placeholder). Save as etsy/LISTING_WEEKLY_CHECK_IN.md.
4. If you still have local copies of etsy/LISTING_ONE_ON_ONE.md and logs/critique-one-on-one-layout-2026-09-28.md from the 28 Sep follow-up, commit them to main (they are missing from the repo). Do not rewrite the 1:1 listing or re-do the same 1:1 critique.

## AI stock images (ai-stock-images)
Last updated: 2026-09-28 19:11 SAST (Claude Code, Instructions follow-up)

### Done today
- Day 2 of the 30-day plan logged in [`logs/2026-09-28.md`](https://github.com/LBD-DASH/ai-stock-images/blob/main/logs/2026-09-28.md): progress check, next-content batch, and first weekly metrics review (Monday), by the earlier daily run.
- Pilot prompt shortlist done: 10 best niche prompts (wooden-blocks growth, Diwali, terrazzo/marble/linen) with title templates and keywords, saved to [`from-cto-new/pilot-prompt-shortlist-2026-09-28.md`](https://github.com/LBD-DASH/ai-stock-images/blob/main/from-cto-new/pilot-prompt-shortlist-2026-09-28.md).
- Firefly stock-resale confirmation and Contributor setup checklist **not done**: this session had no web search/fetch permission, so both were left undone rather than fabricating quotes or guessing Adobe help URLs. Carried over below. See `logs/2026-09-28.md` results section for detail.
- Still no images generated or uploaded. No money spent, no API keys created, no stock uploads.

### Next up
- **[KEVIN]** Create the Adobe Stock Contributor account (ID check, W-8BEN, PayPal)? (yes started / not yet)
- **[KEVIN]** Approve Adobe Firefly Premium + Topaz Gigapixel Personal (≈R283/mo), or compare more? (approve / compare more)
- **[KEVIN]** Add `blackvault/new-income-ideas-2026-09-27.md` to `from-cto-new/`, or confirm it is not needed? (add it / not needed)
- **[KEVIN]** Can web search/fetch be enabled for the daily headless run (or granted once interactively), so the two blocked research items below can be completed with real sources? (enable / grant once / skip these items)
- Once account and generator exist: generate the pilot of 30 keepers using `from-cto-new/pilot-prompt-shortlist-2026-09-28.md`, then curate, upscale, QA and upload with the generative-AI box ticked on every file.

### Instructions for Claude and ChatGPT
1. **Firefly stock-resale confirmation (carried over, blocked 28 Sep for lack of web access).** Check Adobe Firefly's current terms of use for whether outputs may be submitted to Adobe Stock for commercial licensing/resale. Return a short answer (yes / no / unclear) plus 3 to 5 quoted bullets with source URLs. Save as `from-cto-new/firefly-stock-resale-YYYY-MM-DD.md`. Do not sign up or buy anything.
2. **Contributor setup checklist (carried over, blocked 28 Sep for lack of web access).** Write a one-page Adobe Stock Contributor setup checklist for a South African individual (account, ID verify, W-8BEN, PayPal, first-upload AI disclosure). Bullet list with official Adobe help links. Save as `docs/adobe-contributor-setup.md`.

## Princess Baylin (princess-baylin), the pipeline's source
Last updated: 2026-09-28 19:23 SAST (Princess Baylin Repo agent, follow-up run)

### Done today
- YouTube handoff for Episode 1 at [`handoff/youtube/2026-09-28.md`](https://github.com/LBD-DASH/princess-baylin/blob/main/handoff/youtube/2026-09-28.md): beats, cast, lesson, hook, visual notes (EN primary; AF/ZU flagged).
- Day 2 log at [`logs/2026-09-28.md`](https://github.com/LBD-DASH/princess-baylin/blob/main/logs/2026-09-28.md): progress check, first ~12-spread picture-book manuscript (EN + AF/ZU flagged), 5 merch concepts, Monday weekly metrics baseline (recommend adjust).
- Recurring bedtime thank-you ritual noted for every episode ending.
- Pipeline equal-priority line already present; no further Pipeline edit needed.
- Follow-up (instructions 1 and 2 below): [`docs/character-sheet-draft.md`](https://github.com/LBD-DASH/princess-baylin/blob/main/docs/character-sheet-draft.md) (Baylin, Tilly, Rainbird, placeholder hex palette) and [`reviews/2026-09-28-language.md`](https://github.com/LBD-DASH/princess-baylin/blob/main/reviews/2026-09-28-language.md) (non-native read-through of the manuscript's AF/ZU spreads, 4 items flagged for a real native-speaker check).

### Next up
- Refine the picture-book manuscript (do not restart) once placeholders are confirmed or replaced.
- [KEVIN] Add the original story to `assets/story/` with identifying details removed? (yes this week / not yet)
- [KEVIN] Keep placeholder names Tilly, Sunhill and Rainbird, or replace them (see `docs/character-sheet-draft.md`)? (keep / replace)
- [KEVIN] Name one Afrikaans and one isiZulu native-speaker reviewer? (names ready / not yet)
- [KEVIN] Approve Episode 1 direction (listening + teamwork, soft rain, thank-you bedtime ritual) for book and YouTube? (yes / changes needed)
- Once WebSearch/browsing is available in a headless run: the KDP trim checklist and merch pricing sanity check below (both blocked today for lack of web access, not attempted rather than guessed).

### Instructions for Claude and ChatGPT
1. **KDP trim checklist (carried over, blocked 28 Sep for lack of web access).** Research current Amazon KDP picture-book trim sizes suitable for ~24-32 pages with bleed. Output a short checklist with official source links at `docs/kdp-specs.md`.
2. **Merch pricing sanity check (carried over, blocked 28 Sep for lack of web access).** For the five merch concepts in `logs/2026-09-28.md`, list comparable Etsy or POD price bands in ZAR or USD with 2 to 3 example listing links each (or "not found"). Save as `logs/research-merch-pricing-YYYY-MM-DD.md`.
3. None else today.

## Faceless YouTube content (faceless-youtube-content), Princess Baylin bedtime-story channel (runs in parallel with princess-baylin)
Last updated: 2026-09-28 19:40 SAST (Faceless YouTube Repo agent, follow-up run)

### Done today
- Ep 1 full script at [`scripts/2026-09-28.md`](https://github.com/LBD-DASH/faceless-youtube-content/blob/main/scripts/2026-09-28.md) (from Baylin handoff/youtube/2026-09-28.md)
- Day 2 log + first Monday weekly metrics at [`logs/2026-09-28.md`](https://github.com/LBD-DASH/faceless-youtube-content/blob/main/logs/2026-09-28.md)
- Follow-up: checked [`scripts/drafts/episode-2-outline.md`](scripts/drafts/episode-2-outline.md) against the real `princess-baylin/handoff/youtube/2026-09-28.md` (only Ep 1 handoff exists so far). Cast (Tilly, Kingdom of Sunhill), tone, and the callback to Baylin's "shout first" instinct all match Ep 1 canon. No changes needed; still a draft pending Kevin's canon calls and Baylin's own Ep 2 handoff when it lands.
- Confirmed the 27 Sep instructions (channel name shortlist, narrator brief, AF/ZU TTS check, thumbnail style guide) are already answered in [`logs/2026-09-27.md`](logs/2026-09-27.md) ("Response to Instructions for Claude and ChatGPT"); not duplicated into separate files since the original instructions allowed pasting into the log.
- Committed a leftover unstaged `SHARED_UPDATES.md` edit from an earlier session, then merged in princess-baylin's newer 19:23 SAST section (character sheet + language review follow-up) which hadn't reached this repo yet.

### Next up
- Hold production until Kevin answers open decisions below; do not create a channel, spend money, or buy API keys.
- After script approval: build a simple 12-scene shot board from the visual plan in `scripts/2026-09-28.md` (still drafts only).
- Keep Episode 2 as "Princess Baylin and the Sleepy Moon" (patience / night sky) once Baylin sends its own handoff to confirm beats.
- [KEVIN] Approve Ep 1 English VO in `scripts/2026-09-28.md`? (yes / changes needed)
- [KEVIN] Keep placeholders Tilly, Sunhill, Rainbird? (keep / replace)
- [KEVIN] Narrator for English: own voice, family voice, or disclosed Kokoro TTS? (own / family / Kokoro)
- [KEVIN] Channel name ready, and create channel when? (name ready / not yet)
- [KEVIN] Language format: English first, or AF/ZU in parallel after native check? (EN first / parallel later)
- [KEVIN] Art style: hand-illustrated (Krita) or AI-assisted with fixed character sheet? (hand / AI-assisted)
- [KEVIN] AI disclosure: always disclose AI voice or music, or only when YouTube strictly requires it? (always / strict-only)

### Instructions for Claude and ChatGPT
None today.

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
- 2026-09-28 19:40 SAST (Faceless YouTube Repo agent) for all repos: **princess-baylin's local clone is stuck mid interactive-rebase** (`git status` there shows "interactive rebase in progress; onto 9e33972", paused on commit "daily: princess-baylin 2026-09-28" while amending, with "shared: princess-baylin update 2026-09-28" still queued to pick). Not touched by this run since it's outside faceless-youtube-content's scope and a rebase mid-flight is easy to make worse from outside. The princess-baylin agent (or Kevin, with `git rebase --continue` or `--abort` after checking `git status`/`git diff` there) needs to resolve it before that repo's next commit will go through cleanly.
- 2026-09-29 06:33 SAST (Printables Repo agent): Printables Day 3: updated 1:1 printability brief + full Weekly Team Check-in Sheet layout/listing in logs/2026-09-29.md. Still 0 live listings. Claude's claimed LISTING_ONE_ON_ONE + 1:1 critique files are missing from printables main.
