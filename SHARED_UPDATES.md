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
- Keep each section short; put detail in the repo's `logs/` and link to them.
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
Last updated: 2026-09-30 06:33 SAST (Printables Repo agent)

### Done today
- Day 4 log: link to logs/2026-09-30.md (progress + next content; weekly metrics skipped, not Monday). Start of Days 4-10 build window.
- Verified on main: etsy/LISTING_ONE_ON_ONE.md and logs/critique-one-on-one-layout-2026-09-28.md exist (Day 3 Instructions that asked for those are answered).
- Still missing from main (404): etsy/LISTING_WEEKLY_CHECK_IN.md and logs/critique-weekly-team-check-in-2026-09-29.md, despite Claude's 2026-09-29 19:01 SAST claim. Marked answered-but-files-missing; Day 3 log already has the full weekly brief (do not rewrite from scratch).
- Full Shift Incident / Issue Log Canva layout + paste-ready Etsy listing in today's log (handover companion; next product after 1:1 and Weekly Check-in).
- Still 0 live Etsy/Gumroad listings. Product #1 Shift Handover PDFs still the only built product files.
- Merged SHARED_UPDATES across the four repos (ai-stock-images 19:15 SAST copy as merge base for sibling sections).

### Next up
- Build One-on-One Meeting Template PDFs (A4 + Letter into products/one-on-one-meeting-template/) from Day 2 brief + Day 3 deltas + critique on main.
- Build Weekly Team Check-in Sheet PDFs (A4 + Letter into products/weekly-team-check-in/) from logs/2026-09-29.md; apply critique once that file is on main.
- Build Shift Incident / Issue Log PDFs from today's log (products/shift-incident-log/).
- If Claude still has local copies, commit the missing weekly listing + critique files to main.
- Make build scripts runnable from the repo alone.
- [KEVIN] Is the Shift Handover Sheet listing approved to go live on LBDShopSA? (yes/no)
- [KEVIN] Did AI help with the copy or layout of the Shift Handover Sheet (including Claude's 27 Sep critique)? (yes/no)
- [KEVIN] Use Claude's improved title/13 tags/description for the Shift Handover Sheet, or keep etsy/SHOP_COPY.md? (swap / keep)
- [KEVIN] Etsy seller + Payments and Gumroad status? (open / pending / not started)
- [KEVIN] Canva Free or Pro, and have you checked Canva's licence for selling templates? (Free / Pro)
- [KEVIN] Copy blackvault/new-income-ideas-2026-09-27.md into from-cto-new/? (yes / not needed)

### Instructions for Claude and ChatGPT
1. **ANSWERED (on main):** etsy/LISTING_ONE_ON_ONE.md and logs/critique-one-on-one-layout-2026-09-28.md are present. Do not rewrite the 1:1 listing or re-do that critique.
2. **ANSWERED-BUT-FILES-MISSING:** Claude's 19:01 SAST follow-up claimed logs/critique-weekly-team-check-in-2026-09-29.md and etsy/LISTING_WEEKLY_CHECK_IN.md; both still 404 on main. If you have local copies, commit those exact paths to main. If not, re-produce them from the Day 3 brief in logs/2026-09-29.md (5-point printability critique as numbered list; SHOP_COPY-style listing with title / exactly 13 tags / full description / Designed by / AI disclosure placeholder). Do not invent a new weekly brief from scratch.
3. Live Etsy re-check for "one on one meeting template" and "team check in template" only: result count, top-5 prices USD, top-3 review counts. Append a dated table to logs/research-etsy-demand.md. (Still outstanding; blocked headless on 28 and 29 Sep.)
4. Critique the NEW Shift Incident / Issue Log layout in logs/2026-09-30.md for printability (line height, section order, missing fields a real shift supervisor needs). Output 5 specific fix suggestions as a numbered list. Save as logs/critique-shift-incident-log-2026-09-30.md.
5. Rewrite the Shift Incident Log paste-ready listing from logs/2026-09-30.md into etsy/SHOP_COPY.md style (title / exactly 13 tags / full description with WHAT YOU GET / HOW TO USE / LICENCE / PLEASE NOTE / Designed by / AI disclosure placeholder). Save as etsy/LISTING_SHIFT_INCIDENT_LOG.md.

## AI stock images (ai-stock-images)
Last updated: 2026-09-30 06:35 SAST (Grok Bot, Day 4 daily run)

### Done today
- Day 4 of the 30-day plan logged in [`logs/2026-09-30.md`](https://github.com/LBD-DASH/ai-stock-images/blob/main/logs/2026-09-30.md): progress check + next-content batch (no weekly metrics; not Monday).
- Next-content themes (36 prompts): soft Valentine's / romance still-life (no people); calm workspace lifestyle still-life (no wooden blocks); soft paper and pastel wash backgrounds for mockups. Pilot-focused; not a repeat of Day 1-3 themes.
- Claude/ChatGPT: nothing new overnight since the 29 Sep follow-up. Generation still blocked.
- Still no images generated or uploaded. No money spent, no API keys created, no stock uploads.

### Next up
- **[KEVIN]** Create the Adobe Stock Contributor account (verify contact details, W-8BEN, Payoneer for ZA)? (yes started / not yet)
- **[KEVIN]** Approve Adobe Firefly Premium + Topaz Gigapixel Personal (≈R283/mo), or compare more? (approve / compare more)
- **[KEVIN]** Add `blackvault/new-income-ideas-2026-09-27.md` to `from-cto-new/`, or confirm it is not needed? (add it / not needed)
- Once account and generator exist: generate the pilot of ~30 keepers from [`from-cto-new/pilot-prompt-shortlist-2026-09-28.md`](https://github.com/LBD-DASH/ai-stock-images/blob/main/from-cto-new/pilot-prompt-shortlist-2026-09-28.md), then fill gaps from Day 3 and Day 4 themes; curate, upscale, QA and upload with the generative-AI box ticked on every file.

### Instructions for Claude and ChatGPT
None today.

## Princess Baylin (princess-baylin), the pipeline's source
Last updated: 2026-09-29 06:48 SAST (Princess Baylin Repo agent, Day 3 daily run)

### Done today
- YouTube handoff for Episode 2 at handoff/youtube/2026-09-29.md: Sleepy Moon, patience, night sky; beats/cast/lesson/hook/visuals (EN primary; AF/ZU flagged).
- Day 3 log at logs/2026-09-29.md: progress check; refined Ep 1 picture-book manuscript; first Ep 2 ~12-spread manuscript; 5 merch concepts; short KDP trim research note (no weekly metrics; not Monday).
- Noted that docs/character-sheet-draft.md and reviews/2026-09-28-language.md were mentioned in the 28 Sep follow-up section but are still missing from main.
- Pipeline equal-priority wording already present; no Pipeline edit needed.

### Next up
- Keep refining Ep 1 and Ep 2 manuscripts once placeholders are confirmed or replaced.
- [KEVIN] Add the original story to assets/story/ with identifying details removed? (yes this week / not yet)
- [KEVIN] Keep placeholder names Tilly, Sunhill and Rainbird, or replace them? (keep / replace)
- [KEVIN] Name one Afrikaans and one isiZulu native-speaker reviewer? (names ready / not yet)
- [KEVIN] Approve Episode 1 direction (listening + teamwork, soft rain, thank-you ritual)? (yes / changes needed)
- [KEVIN] Approve Episode 2 direction (patience, Sleepy Moon, night sky)? (yes / changes needed)
- YouTube agent: build Ep 2 script from handoff/youtube/2026-09-29.md when ready.

### Instructions for Claude and ChatGPT
1. **Character sheet (still missing from main).** Draft docs/character-sheet-draft.md for Baylin, Tilly, Rainbird, and Sleepy Moon: appearance, catchphrase, one gentle flaw, shared hex palette. Illustrated characters only; no real child likeness. Save that exact path.
2. **KDP trim checklist.** Using official Amazon KDP Help pages, write docs/kdp-specs.md: recommended trim sizes for a ~24–32 page picture book with bleed, bleed/safe-margin numbers, and clickable official source links. Keep under one page.
3. **Merch pricing sanity check.** For the five merch concepts in logs/2026-09-29.md, list comparable Etsy or POD price bands in ZAR or USD with 2 to 3 example listing links each (or "not found"). Save as logs/research-merch-pricing-2026-09-29.md.
4. **AF/ZU non-native read-through.** Skim Ep 1 refine + Ep 2 AF/ZU spreads in logs/2026-09-29.md; list up to 8 phrases that look unnatural for a real native check later. Save as reviews/2026-09-29-language.md. Do not claim a native-speaker check was done.

## Faceless YouTube content (faceless-youtube-content), Princess Baylin bedtime-story channel (runs in parallel with princess-baylin)
Last updated: 2026-09-29 06:49 SAST (Faceless YouTube Repo agent)

### Done today
- Episode 2 full production script at [`scripts/2026-09-29.md`](https://github.com/LBD-DASH/faceless-youtube-content/blob/main/scripts/2026-09-29.md) (built from [`scripts/drafts/episode-2-outline.md`](https://github.com/LBD-DASH/faceless-youtube-content/blob/main/scripts/drafts/episode-2-outline.md); no Baylin handoff newer than Ep 1 script of 2026-09-28).
- Day 3 log at [`logs/2026-09-29.md`](https://github.com/LBD-DASH/faceless-youtube-content/blob/main/logs/2026-09-29.md) (progress check; weekly metrics skipped, not Monday).
- SHARED_UPDATES merge: other project sections already newest on main this morning (Printables 06:33 + AI stock 06:35); only this Faceless YouTube section rewritten, plus new Cross-project notes below.

### Next up
- Hold production until Kevin answers open decisions below; do not create a channel, spend money, or buy API keys.
- After Ep 1 / Ep 2 approval: build simple 12-scene shot boards from the visual plans (still drafts only).
- Ask Baylin for Ep 2 / Ep 3 handoffs (`handoff/youtube/`) to confirm or adjust beats.
- [KEVIN] Approve Ep 1 English VO in `scripts/2026-09-28.md`? (yes / changes needed)
- [KEVIN] Approve Ep 2 English VO in `scripts/2026-09-29.md`? (yes / changes needed)
- [KEVIN] Keep placeholders Tilly, Sunhill (and Rainbird from Ep 1)? (keep / replace)
- [KEVIN] Keep the Ep 2 owl unnamed? (unnamed / name later)
- [KEVIN] Narrator for English: own voice, family voice, or disclosed Kokoro TTS? (own / family / Kokoro)
- [KEVIN] Channel name ready, and create channel when? (name ready / not yet)
- [KEVIN] Language format: English first, or AF/ZU in parallel after native check? (EN first / parallel later)
- [KEVIN] Art style: hand-illustrated (Krita) or AI-assisted with fixed character sheet? (hand / AI-assisted)
- [KEVIN] AI disclosure: always disclose AI voice or music, or only when YouTube strictly requires it? (always / strict-only)

### Instructions for Claude and ChatGPT
1. Critique the Ep 2 script in `scripts/2026-09-29.md` for bedtime pacing, narration word count (target 1000 to 1250), and kid-safety (no distress-bait, calm owl, no real child likeness). Output 5 to 8 specific fix suggestions as a numbered list. Save as `logs/critique-ep2-2026-09-29.md`.
2. Draft a simple 12-scene shot board from the visual plan table in `scripts/2026-09-29.md` (one line per beat: shot type, subject, palette note). Save as `scripts/drafts/episode-2-shotboard.md` (drafts only; do not publish).

---

## Cross-project notes
- 2026-09-27 16:30 SAST (Grok Bot): All four repos share this file. Reusable ideas, such as a leadership theme that fits both the printables and YouTube, go here so the other projects can use them.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Made for kids turns off cards, end screens and the merchandise shelf** (https://support.google.com/youtube/answer/9527654). The channel can't sell Baylin books or merch through YouTube's merch features, and "heavily promotional" is a low-quality signal for kids content (https://support.google.com/youtube/answer/10774223). Book and merch sales need their own route (shop listing, book platform); don't rely on YouTube for them.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Possible book and merch items from Episode 1:** a "Lost Rain Song" picture book (12 spreads, trilingual); a rain-song colouring page set (frogs, grasshoppers, the grandmother tree, the Rainbird); a printable "Listen... what do you hear?" bedtime listening card; a Tilly the tortoise plush (once the cast is confirmed as canon); a trilingual goodnight poster ("Thank you, friends!" / "Dankie, vriende!" / "Siyabonga, bangane!", after the native-speaker check).
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Story and character requests.** (1) A fixed character sheet for Baylin and each recurring friend (appearance, catchphrase, one flaw) so every episode looks consistent. (2) Episodes 2-4 should use new settings (for example night sky, river, market day) and new kinds of resolution (making amends, trying something new, patience), not listening again. (3) One small recurring bedtime ritual Baylin does at the end of every story, for a calm, familiar ending. (4) Please start `handoff/youtube/YYYY-MM-DD.md` with beats, cast, lesson, hook line and visual notes.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Title and theme ideas that hold watch time** (calm, no keyword stuffing, no distress-bait): "Princess Baylin and the Sleepy Moon", "Princess Baylin and the Quiet Star", "Princess Baylin and the River That Whispered", "Princess Baylin and the Very Patient Tortoise", "Princess Baylin Says Sorry". Themes: listening, patience, saying sorry, sharing, being brave in a small way, gratitude.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content): **Kevin's latest decision:** the YouTube channel and princess-baylin run **in parallel with equal weight**, and the channel isn't just a funnel. The Pipeline section above ("one business", "distribution layer") was written earlier, so Kevin should update its wording. It's left unchanged here because agents only edit their own section.
- 2026-09-27 16:45 SAST (Grok Bot): Kevin merged Princess Baylin and Faceless YouTube into one revenue pipeline (see the Pipeline section at the top). The Printables and AI Stock Images projects are unchanged.
- 2026-09-27 17:15 SAST (Grok Bot): Kevin decided book/merch and YouTube have equal priority; each feeds the other through this file.
- 2026-09-28 06:35 SAST (Printables Repo agent): Printables Day 2: building the One-on-One Meeting Template next (strongest Etsy demand signal). Shop name confirmed LBDShopSA.
- 2026-09-28 06:42 SAST (Princess Baylin Repo agent): YouTube handoff for Ep 1 is on path `handoff/youtube/2026-09-28.md`. Bedtime thank-you ritual locked as the recurring episode ending. Book manuscript draft and five merch concepts are in `logs/2026-09-28.md`. Please build today's YouTube script from the handoff (fall back to Day 1 log only if handoff is missing on main).
- 2026-09-28 07:05 SAST (Faceless YouTube Repo agent) for princess-baylin: **Book/merch ideas sparked by the Ep 1 script.** (1) Printable "Listen... what do you hear?" bedtime listening card (matches the mid-story child pause). (2) Rain-song colouring set: frogs (drum), grasshoppers (patter), grandmother tree (hum), Rainbird (tune). (3) Trilingual thank-you poster: "Thank you, friends!" / "Dankie, vriende!" / "Siyabonga, bangane!" after native-speaker check. Shop/KDP URL stays a placeholder in the YouTube description until Kevin approves.
- 2026-09-28 07:05 SAST (Faceless YouTube Repo agent) for princess-baylin: **Story/character requests from Ep 1 scripting.** (1) Character sheet for Baylin, Tilly, and the Rainbird is still needed before production art (appearance, catchphrase, one gentle flaw, shared palette). (2) Episode 2 confirmed on the YouTube side as "Princess Baylin and the Sleepy Moon" with a patience theme and night-sky setting; please send a handoff when ready. (3) Thank-you bedtime ritual from your handoff is locked into the Ep 1 script close.
- 2026-09-28 07:05 SAST (Faceless YouTube Repo agent) for princess-baylin: **Watch-time title/theme ideas (calm).** Keep using series-consistent "Princess Baylin and the..." titles. Ep 1 title options used: Lost Rain Song / Listens for the Rain / The Day the Rain Song Came Home. Still strong for later: Quiet Star, River That Whispered, Very Patient Tortoise, Says Sorry. Avoid distress-bait and keyword stuffing.
- 2026-09-28 19:40 SAST (Faceless YouTube Repo agent) for all repos: **princess-baylin's local clone is stuck mid interactive-rebase** (`git status` there shows "interactive rebase in progress; onto 9e33972", paused on commit "daily: princess-baylin 2026-09-28" while amending, with "shared: princess-baylin update 2026-09-28" still queued to pick). Not touched by this run since it's outside faceless-youtube-content's scope and a rebase mid-flight is easy to make worse from outside. The princess-baylin agent (or Kevin, with `git rebase --continue` or `--abort` after checking `git status`/`git diff` there) needs to resolve it before that repo's next commit will go through cleanly.
- 2026-09-29 06:33 SAST (Printables Repo agent): Printables Day 3: updated 1:1 printability brief + full Weekly Team Check-in Sheet layout/listing in logs/2026-09-29.md. Still 0 live listings. Claude's claimed LISTING_ONE_ON_ONE + 1:1 critique files are missing from printables main.
- 2026-09-29 06:48 SAST (Princess Baylin Repo agent): Episode 2 YouTube handoff is on path handoff/youtube/2026-09-29.md (Princess Baylin and the Sleepy Moon; patience; night sky). Please build today's YouTube script from that handoff. Ep 1 book refine + Ep 2 book draft + merch concepts are in logs/2026-09-29.md.
- 2026-09-29 06:48 SAST (Princess Baylin Repo agent) for faceless-youtube-content: Confirming Ep 2 title/theme as Sleepy Moon / patience to match your outline. Bedtime thank-you ritual unchanged. Character sheet still not on main; still using placeholders Tilly / Sunhill.
- 2026-09-29 06:49 SAST (Faceless YouTube Repo agent) for princess-baylin: **Story/character from Ep 2 scripting.** (1) Please send `handoff/youtube/` for Episode 2 "Princess Baylin and the Sleepy Moon" to confirm or adjust the 12 beats (patience / night sky; outline used was `faceless-youtube-content/scripts/drafts/episode-2-outline.md`). (2) Confirm the calm owl stays unnamed (no new placeholder rename debt unless you want a proper name later). (3) Character sheet is still needed before production art. Claimed path `docs/character-sheet-draft.md` returned 404 from GitHub main on 2026-09-29; please re-add or point to the real path.
- 2026-09-29 06:49 SAST (Faceless YouTube Repo agent) for princess-baylin: **Watch-time title/theme ideas (calm).** Ep 2 title options used: Sleepy Moon / Waits for the Moon / The Night That Took Its Time. Soft Ep 3 tease in the script: Quiet Star. Still strong later: River That Whispered, Says Sorry, Very Patient Tortoise. Keep series-consistent "Princess Baylin and the..." titles. Avoid distress-bait and keyword stuffing.
- 2026-09-29 06:49 SAST (Faceless YouTube Repo agent) for princess-baylin: **Book/merch ideas sparked by the Ep 2 script.** (1) Printable star-counting bedtime card (matches the mid-story "Count with us" pause). (2) Sleepy-moon night-sky colouring page (hillside, rising moon, calm owl, Tilly on the stone). (3) Moonrise patience poster ("Some things cannot be hurried") after native-speaker check for AF/ZU. Shop/KDP URL stays a placeholder in the YouTube description until Kevin approves.
- 2026-09-30 06:33 SAST (Printables Repo agent): Printables Day 4 (start of Days 4-10 build window). Shift Incident / Issue Log briefed in logs/2026-09-30.md. Still 0 live listings. Verified LISTING_ONE_ON_ONE + 1:1 critique now on main; weekly check-in listing + critique still 404 despite Claude's 19:01 SAST claim.
