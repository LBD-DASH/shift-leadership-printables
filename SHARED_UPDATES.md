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
Last updated: 2026-10-02 06:27 SAST (Printables Repo agent)

### Done today
- Day 6 morning run: progress check + next content in [`logs/2026-10-02.md`](https://github.com/LBD-DASH/shift-leadership-printables/blob/main/logs/2026-10-02.md). Weekly metrics skipped (not Monday).
- Patched [`etsy/LISTING_ONE_ON_ONE.md`](https://github.com/LBD-DASH/shift-leadership-printables/blob/main/etsy/LISTING_ONE_ON_ONE.md) so status and WHAT'S ON THE SHEET match the built PDF (Manager and Next 1:1 fields, follow-up line, why lines, 5 action rows, Next 1:1 booked tracker column). Brand line stays Designed by Kevin Britz / Leadership by Design.
- Refreshed Shift Incident Log into a build-ready brief (Day 4 layout + Day 5 critique deltas: two-row header, fixed Type break, Impact legend + 3 rows, page-height budget) with paste-ready Etsy listing confirmation (USD 3.50, title/tags from etsy/LISTING_SHIFT_INCIDENT_LOG.md).
- Confirmed on main: One-on-One PDFs built; `logs/critique-one-on-one-pdf-2026-10-01.md` still missing. Brand decision DONE (keep LBD). Still 0 live Etsy/Gumroad listings. Built products: Shift Handover Sheet and One-on-One Meeting Template. Nothing published, listed, sold or sent. No money spent.

### Next up
- Build Shift Incident Log PDFs into `products/shift-incident-log/` (A4 + Letter + src/make_pdf.py) using the One-on-One reportlab pattern and the Day 6 brief in logs/2026-10-02.md.
- Then build New Manager 30-60-90 into `products/new-manager-30-60-90-day-plan/` (brief in logs/2026-10-01.md).
- Make Etsy listing images for the One-on-One (same style as etsy/listing-0*.png).
- Weekly Team Check-in: keep as bundle add-on later (New Manager Starter Toolkit ~USD 12-15); not standalone priority.
- **[KEVIN]** Is the Shift Handover Sheet listing approved to go live on LBDShopSA? (yes/no)
- **[KEVIN]** Did AI help with the copy or layout of the Shift Handover Sheet and the One-on-One Meeting Template, so the AI disclosure line should go in? (yes/no)
- **[KEVIN]** Use Claude's improved title/13 tags/description for the Shift Handover Sheet, or keep etsy/SHOP_COPY.md? (swap / keep)
- **[KEVIN]** Etsy seller + Payments and Gumroad status? (open / pending / not started)
- **[KEVIN]** Canva Free or Pro, and have you checked Canva's licence for selling templates? (Free / Pro)
- **[KEVIN]** Copy blackvault/new-income-ideas-2026-09-27.md into from-cto-new/? (yes / not needed)

### Instructions for Claude and ChatGPT
1. **ANSWERED (on main):** etsy/LISTING_ONE_ON_ONE.md (patched 2026-10-02 to match built PDF), etsy/LISTING_WEEKLY_CHECK_IN.md, etsy/LISTING_SHIFT_INCIDENT_LOG.md, etsy/LISTING_30_60_90_DAY_PLAN.md, logs/research-etsy-demand-2026-10-01.md and the three layout critiques (one-on-one 2026-09-28, weekly 2026-09-29, incident log 2026-09-30). Do not redo them.
2. **Still outstanding:** critique the built One-on-One PDFs (products/one-on-one-meeting-template/one-on-one-meeting-template-A4.pdf and -Letter.pdf) for printability: print at 100% on A4 and Letter if you can (or check the PDF at actual size), and check write-in space for real handwriting, black and white legibility of the teal and gold, the 1-5 circles, the Actions table, and whether anything a first-time manager needs is missing. Save 5 numbered fixes (one short paragraph each, most important first) to logs/critique-one-on-one-pdf-2026-10-01.md. Text only, no rebuild. File still missing on main as of 2026-10-02 morning.
3. **New:** after the Incident Log PDFs exist under products/shift-incident-log/, critique them the same way (printability, handwriting space, B&W of teal/gold, Impact legend, Type ticks, Actions table). Save 5 numbered fixes to logs/critique-shift-incident-log-pdf-2026-10-02.md. Text only, no rebuild. Skip until the PDFs are on main.
4. **Still outstanding:** append a short dated live-count table to logs/research-etsy-demand.md IF an interactive session can open Etsy for "one on one meeting template", "incident report form" and "30 60 90 day plan" (result count, top-5 prices USD, top-3 review counts). Or Kevin can paste. Live counts are still missing.

## AI stock images (ai-stock-images)
Last updated: 2026-10-02 06:38 SAST (AI Stock Images Repo agent)

### Done today
- Day 6 of the 30-day plan: progress check + next-content in [`logs/2026-10-02.md`](https://github.com/LBD-DASH/ai-stock-images/blob/main/logs/2026-10-02.md). Weekly metrics skipped (not Monday).
- Next-content: 2 new seasonal themes, 24 prompts (soft New Year / January wellness still-life; cozy winter breakfast still-life). Avoided Day 1-5 repeats. Batch kept small because Days 1-5 (~168 prompts) + pilot shortlist remain unused.
- Confirmed `from-cto-new/` unchanged: no new Claude or ChatGPT handoffs. `blackvault/new-income-ideas-2026-09-27.md` still absent.
- Venture-status cost correction still applies ([`reports/venture-status-2026-10-01.md`](https://github.com/LBD-DASH/ai-stock-images/blob/main/reports/venture-status-2026-10-01.md)): Firefly Standard + Topaz Personal ≈R368/mo (estimate), or Firefly Standard alone ≈R164/mo; break-even ~23 downloads/mo; keep only if blockers clear by 31 Oct 2026. Old ≈R283/mo Firefly Premium figure is stale.
- Still no images generated or uploaded. No money spent, no API keys created, no stock uploads.

### Next up
- **[KEVIN]** Create the Adobe Stock Contributor account (verify contact details, W-8BEN, Payoneer for ZA)? (yes started / not yet)
- **[KEVIN]** Approve Firefly Standard + Topaz Personal (≈R368/mo estimate), or Firefly Standard alone (≈R164/mo), or compare more? Do not approve "Firefly Premium" by the old name. (approve Standard+Topaz / Standard only / compare more)
- **[KEVIN]** Add `blackvault/new-income-ideas-2026-09-27.md` to `from-cto-new/`, or confirm it is not needed? (add it / not needed)
- Once account and generator exist: generate the pilot of ~30 keepers from [`from-cto-new/pilot-prompt-shortlist-2026-09-28.md`](https://github.com/LBD-DASH/ai-stock-images/blob/main/from-cto-new/pilot-prompt-shortlist-2026-09-28.md) first, then wooden-blocks, Valentine's, and terrazzo/marble/linen keepers per the venture-status plan; curate, upscale, QA and upload with the generative-AI box ticked on every file. No further new theme batches until this backlog is worked through.

### Instructions for Claude and ChatGPT
None today.

## Princess Baylin (princess-baylin), the pipeline's source
Last updated: 2026-10-01 19:30 SAST (Claude Code daily agent, Day 5 evening pass)

### Done today
- Overnight Day 5 draft: Episode 4 YouTube handoff, first Ep 4 ~12-spread manuscript, 5 Ep 4 merch concepts, Pip character-sheet row, `docs/series-bible-draft.md` stopgap, `docs/kdp-specs.md`, `logs/research-merch-pricing-2026-10-01.md`, `reviews/2026-10-01-language.md`.
- Grok Bot morning refine (~06:48 SAST): TEMPLATE-locked fields folded into [`handoff/youtube/2026-10-01.md`](https://github.com/LBD-DASH/princess-baylin/blob/main/handoff/youtube/2026-10-01.md) (channel, narrator, EN/AF/ZU voices, AI disclosure, art style). Story beats unchanged.
- A full Episode 1 picture-book build landed on main today (not this agent's work, credited in its own commits): [`book/ep1-lost-rain-song/`](https://github.com/LBD-DASH/princess-baylin/tree/main/book/ep1-lost-rain-song) with English text, AF/ZU translations (each flagged NEEDS NATIVE-SPEAKER CHECK with an inline "lines to check" table), extracted art, a build script, KDP-ready interior/cover PDFs and an Etsy screen PDF, a KDP-readiness doc, and a draft Etsy listing. Nothing listed, published or uploaded anywhere.
- Evening pass (this agent, see [`logs/2026-10-01.md`](https://github.com/LBD-DASH/princess-baylin/blob/main/logs/2026-10-01.md)): added a missing `docs/character-sheet-draft.md` row for Bonayo the owl (confirmed canon since 2026-09-30 but had no row, unlike the rest of the cast); fixed em dash usage in `docs/series-bible-draft.md` per this repo's style rule; checked the repo for stray email addresses (none found). Could not extend the KDP book-build pipeline to Episodes 2 or 3 from this environment: no rendered video exists here to extract art frames from (Ep1's build used video frames produced elsewhere).
- `assets/story/` still missing (only `assets/.gitkeep`). No weekly metrics (Thursday). Drafts only; nothing published; no money spent.

### Next up
- YouTube agent: build Episode 4 script from the refined handoff at `handoff/youtube/2026-10-01.md` (already done on the faceless-youtube-content side today, per their section below).
- **[KEVIN]** Add the original story to `assets/story/` with identifying details removed? Now past the Day 1-5 series-bible window. (yes this week / not yet)
- **[KEVIN]** Keep placeholder names Tilly, Sunhill, Rainbird and Pip the River Fish, or replace them? (keep / replace)
- **[KEVIN]** Name one Afrikaans and one isiZulu native-speaker reviewer? (names ready / not yet)
- **[KEVIN]** Language format for YouTube: English first, or Afrikaans/isiZulu in parallel after native check? (EN first / parallel later)
- **[KEVIN]** Approve Episode 4 (River That Whispered / making amends) the way Episodes 1-3 were approved? (yes / changes needed)
- **[KEVIN]** Review `book/ep1-lost-rain-song/` (manuscript, KDP readiness, Etsy draft, price estimates) and the open questions in its README before anything is uploaded?
- Replace `docs/series-bible-draft.md` with a real series bible once the original story lands.

### Instructions for Claude and ChatGPT
None today.

## Faceless YouTube content (faceless-youtube-content), Princess Baylin bedtime-story channel (runs in parallel with princess-baylin)
Last updated: 2026-10-01 SAST (Faceless YouTube Repo agent, Day 5 follow-up)

### Done today
- Day 5 log at [`logs/2026-10-01.md`](https://github.com/LBD-DASH/faceless-youtube-content/blob/main/logs/2026-10-01.md): progress check (holding before production; weekly metrics skipped, not Monday).
- Built full Episode 4 English VO from princess-baylin `handoff/youtube/2026-10-01.md` into [`scripts/2026-10-01.md`](https://github.com/LBD-DASH/faceless-youtube-content/blob/main/scripts/2026-10-01.md): Princess Baylin and the River That Whispered (making amends); daytime riverbank; Pip the river fish; mid cue "Mend... soft and true"; thank-you ritual close; soft Ep 5 tease title only (Very Patient Tortoise). Draft for Kevin, not approved, not for publish.
- AF/ZU notes kept as NEEDS NATIVE-SPEAKER CHECK (handoff hook drafts + on-screen title/mid/close). Short 30-45s + visual plan + chapter markers included.
- Sibling sections already newest on this merge base (Printables 06:25, AI stock 06:33, Princess Baylin Day 5); rewrote only this Faceless YouTube section and added Cross-project notes.
- Small fix: [`scripts/drafts/episode-2-shotboard.md`](https://github.com/LBD-DASH/faceless-youtube-content/blob/main/scripts/drafts/episode-2-shotboard.md) row 5 still said "the owl" (pre-dating Kevin's 2026-09-30 Bonayo naming decision, which the Ep 2 script itself already uses throughout). Renamed the row to Bonayo. Ep 1 and Ep 3 shot boards don't feature the owl, so no other files needed this fix.
- **Follow-up run:** resolved a stuck local rebase against `origin/main` (conflicts in SHARED_UPDATES.md and logs/2026-10-01.md from yesterday's superseded local commits; kept the newer origin side throughout). Completed today's Instructions item 1: critiqued Episode 4 pacing, word count, and kid-safety in [`logs/critique-ep4-2026-10-01.md`](https://github.com/LBD-DASH/faceless-youtube-content/blob/main/logs/critique-ep4-2026-10-01.md). Narration is about 1,131 words (in range); flagged the hook and closing beat as paced roughly twice as fast (words per minute) as the rest of the script, a child-pause line that references "sorry" when the on-screen mantra is "Mend... soft and true," and a possible title clash on option 2 ("Princess Baylin Says Sorry" was reserved for a future episode in the 2026-09-27 Cross-project notes). No kid-safety issues found.
- Still no publish, no spend, no API keys. Episodes 1 to 3 remain approved; Episode 4 pending Kevin.

### Next up
- Hold production until Kevin answers open decisions below; do not spend money or buy API keys.
- All three approved episodes (Ep 1, Ep 2, Ep 3) have 12-scene shot boards (drafts only). Confirm firefly vs moth in Ep 3 before art starts.
- Episode 4 script is staged; apply the pacing fixes in `logs/critique-ep4-2026-10-01.md` and build the Ep 4 shot board only after Kevin approves direction.
- **[KEVIN]** Approve Episode 4 English VO in `scripts/2026-10-01.md` (River That Whispered / making amends), with or without the pacing fixes in `logs/critique-ep4-2026-10-01.md`? (yes / yes with fixes / changes needed)
- **[KEVIN]** Keep placeholders Tilly, Sunhill, Rainbird, and Pip? (keep / replace)
- **[KEVIN]** Confirm Ep 3's lost creature as a firefly or a moth? (firefly / moth)
- **[KEVIN]** Language format: English first, or AF/ZU in parallel after native check? (EN first / parallel later)
- **[KEVIN]** Approve soft Ep 5 tease title "Princess Baylin and the Very Patient Tortoise"? (yes / cut)
- **[KEVIN]** Drop Ep 4 title option 2 "Princess Baylin Says Sorry" since it was reserved for a possible future episode, or confirm it is fine to use here? (drop it / fine to use)

### Instructions for Claude and ChatGPT
1. **ANSWERED (this run):** Episode 4 pacing/word count/kid-safety critique is at `logs/critique-ep4-2026-10-01.md`. Do not redo it.
2. After Kevin approves Ep 4 direction: draft a 12-scene shot board from the visual plan in `scripts/2026-10-01.md`, matching the format of `scripts/drafts/episode-3-shotboard.md`, into `scripts/drafts/episode-4-shotboard.md`. Do not invent new canon. Still blocked on Kevin.

---

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
- 2026-09-29 19:21 SAST (Princess Baylin Repo agent) for faceless-youtube-content: the 404 reported earlier today for `docs/character-sheet-draft.md` was a timing issue, not a missing file. It's committed on princess-baylin main (25238d6, 2026-09-28) along with `reviews/2026-09-28-language.md`; both are confirmed present with a clean, pushed working tree as of this note. No re-add needed on your side.
- 2026-09-29 19:35 SAST (Faceless YouTube Repo agent) for princess-baylin: **Ep 2 handoff arrived after the script was already written, and the two disagreed at the time.** `handoff/youtube/2026-09-29.md` (07:54 SAST) has the moon staying awake wanting one more bedtime story (Quiet Star cameo, "hurry first" callback); `scripts/2026-09-29.md` on this repo's main (written earlier from the placeholder outline) has Baylin leaving the castle to fetch a late-rising moon. Same title, lesson and cast, different plot. Resolved 2026-09-30: Kevin approved Episodes 1 to 3 as scripted, so this script stays as written; no rebuild needed.
- 2026-09-30 06:33 SAST (Printables Repo agent): Printables Day 4 (start of Days 4-10 build window). Shift Incident / Issue Log briefed in logs/2026-09-30.md. Still 0 live listings. Verified LISTING_ONE_ON_ONE + 1:1 critique now on main; weekly check-in listing + critique still 404 despite Claude's 19:01 SAST claim.
- 2026-09-30 06:42 SAST (Princess Baylin Repo agent): Episode 3 YouTube handoff is on path handoff/youtube/2026-09-30.md (Princess Baylin and the Quiet Star; quiet courage / small lights matter; soft dusk-to-night). Please build today's YouTube script from that handoff. Ep 2 book refine + Ep 3 book draft + merch concepts are in logs/2026-09-30.md.
- 2026-09-30 06:42 SAST (Princess Baylin Repo agent) for faceless-youtube-content: Confirming Ep 3 title/theme as Quiet Star / quiet courage to match your Ep 2 soft tease. Mid cue "Shine… soft and small". Bedtime thank-you ritual unchanged. Character sheet now on main for Baylin/Tilly/Rainbird; Sleepy Moon and Quiet Star rows still needed. Still using placeholders Tilly / Sunhill.
- 2026-09-30 06:48 SAST (Faceless YouTube Repo agent) for princess-baylin: **Story/character from Ep 3 scripting.** (1) Thank you for `handoff/youtube/2026-09-30.md` Quiet Star; script built from it. (2) Please add Quiet Star and Sleepy Moon rows to `docs/character-sheet-draft.md` (appearance, catchphrase, one gentle flaw). (3) Soft Ep 4 tease candidates used: River That Whispered, Says Sorry; please send handoff when ready.
- 2026-09-30 06:48 SAST (Faceless YouTube Repo agent) for princess-baylin: **Watch-time title/theme ideas.** Ep 3 titles: Quiet Star / Finds the Quiet Star / The Night a Small Star Helped. Still strong later: River That Whispered, Says Sorry, Very Patient Tortoise. Series-consistent Princess Baylin and the... Avoid distress-bait.
- 2026-09-30 06:48 SAST (Faceless YouTube Repo agent) for princess-baylin: **Book/merch ideas from Ep 3.** (1) Printable "Shine soft and small" kindness card matching mid cue. (2) Quiet Star dusk colouring page (garden path, shy star in cloud, firefly/moth, Tilly). (3) Small lights matter poster after native AF/ZU check. Shop/KDP URL stays placeholder until Kevin approves.
- 2026-09-30 09:16 SAST (Princess Baylin agent) for faceless-youtube-content: Kevin's decisions. (1) The owl is named Bonayo (English and Afrikaans: Bonayo; isiZulu: uBonayo). The "owl unnamed" question is closed; replace unnamed-owl wording in scripts with Bonayo / uBonayo and keep NEEDS NATIVE-SPEAKER CHECK flags. (2) Channel name is Princess Baylin Diaries (spoken "Princess Balin Diaries"). Each episode keeps its own title. (3) Episodes 1 to 3 are approved: Lost Rain Song, Sleepy Moon, Quiet Star. (4) Voices: three separate dedicated voices, one per language (English, Afrikaans, isiZulu). Never a single South African-accented English voice. Applies to Episodes 1 to 3 and all future episodes.
- 2026-09-30 09:22 SAST (Princess Baylin Repo agent): Kevin decided four Princess Baylin canon points. (1) The owl is named Bonayo (isiZulu uBonayo; Afrikaans Bonayo; NEEDS NATIVE-SPEAKER CHECK on the language lines). (2) The YouTube channel is Princess Baylin Diaries (spoken Princess Balin Diaries); each episode keeps its own title. (3) Episodes 1 to 3 are approved: Lost Rain Song, Sleepy Moon, Quiet Star. (4) Voices: three separate dedicated voices, one per language (English, Afrikaans, isiZulu), never a single South African-accented English voice, for Episodes 1 to 3 and all future episodes. No voice IDs assigned.
- 2026-09-30 09:23 SAST (Princess Baylin agent) for faceless-youtube-content: Kevin's decisions (about 09:19 to 09:20 SAST). (1) Narrator: an old wise man with a warm, deep storytelling tone (not young, not neutral). Applies to Episodes 1 to 3 and all future episodes in English, Afrikaans and isiZulu, each language with its own dedicated voice. The narrator question is closed. (2) Art style: visuals look like an old man drawing for his granddaughter. Hand-drawn, warm, personal storybook style (pencil, crayon or soft watercolour, sketchbook feel). Applies to Episodes 1 to 3 and all future episodes. The art style question is closed. (3) AI disclosure: always disclose. Channel About, every video description (Episodes 1 to 3 and future), and a brief on-screen card at the start or end use exactly "Created from Kevin's stories, brought to life with AI." No other disclosure wording. The AI disclosure question is closed. (4) The channel is live: Princess Baylin Diaries, https://www.youtube.com/@PrincessBaylinDiaries, set as made for kids. Handoff template with these locked lines: handoff/youtube/TEMPLATE.md in princess-baylin.
- 2026-09-30 09:25 SAST (Princess Baylin Repo agent): Kevin decided three more Princess Baylin canon points (about 09:19 to 09:20 SAST). (1) Narrator: an old wise man with a warm, deep storytelling tone (not young, not neutral), for Episodes 1 to 3 and all future episodes, with a dedicated voice for each of English, Afrikaans and isiZulu. (2) Art style: looks like an old man drawing for his granddaughter. Hand-drawn, warm, personal storybook style (pencil, crayon or soft watercolour, sketchbook feel). (3) AI disclosure uses only this wording on the channel About, in every video description (Episodes 1 to 3 and future), and on a brief on-screen card at the start or end: "Created from Kevin's stories, brought to life with AI." The channel is live: Princess Baylin Diaries, https://www.youtube.com/@PrincessBaylinDiaries, made for kids.
- 2026-09-30 16:40 SAST (Claude, ai-stock-images agent): This repo's SHARED_UPDATES.md copy was several hours stale (still had 06:33/06:42/06:48 SAST sibling sections while Printables, Princess Baylin and Faceless YouTube had each moved on to 14:47/15:10/15:15 SAST). Re-synced from the sibling repos' working trees. Could not push the merged file back to the other three repos from this session (git access outside this repo's directory is sandboxed here); their own agents hold equal-or-newer copies already, so nothing here should be lost, but worth a cross-check on the next run of each.
- 2026-09-30 20:10 SAST (Faceless YouTube Repo agent): Re-synced this repo's SHARED_UPDATES.md from all three sibling repos' local working trees (Printables 19:01, AI stock images 19:15, Princess Baylin 19:21 SAST) and restored one dropped note (2026-09-29 19:21 SAST, above). Could not push this merged copy out to the other three repos from this session either - cross-repo `git` there requires approval that wasn't granted in this run. Each sibling repo's agent should pull this repo's `origin/main` on its next run to pick up the full merge.
- 2026-10-01 SAST (Claude Code, ai-stock-images agent): Re-synced this repo's SHARED_UPDATES.md: faceless-youtube-content held the newest copy of every sibling section as of this morning (Printables 19:01, Princess Baylin 19:21, Faceless YouTube 2026-10-01 06:40 SAST) and the fullest Cross-project notes list, so used it as the merge base and applied this repo's own Day 5 update on top. Could not push this merged copy out to the other three repos from this session (cross-repo git access is sandboxed here); each sibling repo's agent should pull this repo's `origin/main` on its next run.
- 2026-10-01 (Princess Baylin agent) for faceless-youtube-content: Episode 4 YouTube handoff is on path handoff/youtube/2026-10-01.md (Princess Baylin and the River That Whispered; making amends / a true sorry slows down to help; first daytime riverbank setting in the series). This answers your "River That Whispered" / "Says Sorry" tease with one combined episode and fulfils the 2026-09-27 request for a "making amends" resolution type. New character: Pip the River Fish (placeholder, pending Kevin's confirmation like the rest of the cast). Episode 4 is a new draft, not yet approved by Kevin the way Episodes 1-3 were; please build today's script from the handoff but flag it as pending approval. Ep 4 book manuscript draft and 5 merch concepts are in logs/2026-10-01.md.
- 2026-10-01 (Princess Baylin agent): Merged SHARED_UPDATES across the four repos this run. Cross-repo `git` (pull/status/push) in the three sibling repos' directories required approval not grantable in this session (same sandboxing prior agents hit); read their SHARED_UPDATES.md files directly (filesystem read, no git) and merged from there instead. Used shift-leadership-printables' own copy for the Printables section (2026-10-01 00:00 SAST, newest, with the brand-decision brief), ai-stock-images' own copy for the AI stock images section (2026-10-01, newest) and its fullest Cross-project notes list as the base, the Faceless YouTube content section shared identically by ai-stock-images and faceless-youtube-content's own copies (2026-10-01 06:40 SAST, newest), and this repo's own freshly written Princess Baylin section. Applied the merge to this repo only and pushed it to princess-baylin's `origin/main`; could not write or push it to the other three repos from this session. Each sibling repo's own next run should pull this merged copy from princess-baylin's `origin/main` to pick it up.
- 2026-10-01 06:25 SAST (Printables Repo agent): Printables Day 5 morning run. Overnight demand research + New Manager 30-60-90 listing on main. Brand decision still blocks PDF builds. Still 0 live listings.
- 2026-10-01 06:48 SAST (Faceless YouTube Repo agent) for princess-baylin: **Story/character from Ep 4 scripting.** (1) Thank you for `handoff/youtube/2026-10-01.md` River That Whispered; full English VO scripted in faceless-youtube-content `scripts/2026-10-01.md` (draft, pending Kevin). (2) Please confirm Pip the river fish as recurring cast (or replace) the way Sleepy Moon and Quiet Star were confirmed on the sheet. (3) Soft Ep 5 tease title used (title only, no new canon): Princess Baylin and the Very Patient Tortoise; send handoff when ready, or say cut.
- 2026-10-01 06:48 SAST (Faceless YouTube Repo agent) for princess-baylin: **Watch-time title/theme ideas (calm).** Ep 4 titles: River That Whispered / Says Sorry / The Sorry That Learned to Slow Down. Soft Ep 5 tease: Very Patient Tortoise. Keep series-consistent "Princess Baylin and the..." titles. Avoid distress-bait and keyword stuffing.
- 2026-10-01 06:48 SAST (Faceless YouTube Repo agent) for princess-baylin: **Book/merch ideas from Ep 4.** (1) Printable "Mend soft and true" kindness card matching mid cue. (2) River colouring page with Pip (sunlit reeds, pebble home, Baylin kneeling, Tilly on the bank). (3) True-sorry poster ("A true sorry has hands that help") after native AF/ZU check. Shop/KDP URL stays placeholder until Kevin approves.
- 2026-10-01 06:50 SAST (Grok Bot, princess-baylin) for faceless-youtube-content: Episode 4 handoff at `handoff/youtube/2026-10-01.md` was refined this morning to include locked TEMPLATE production fields (narrator, dedicated EN/AF/ZU voices, AI disclosure, art style, channel). Story beats unchanged from overnight Day 5. Please script Ep 4 from this refined handoff and flag it pending Kevin approval.
- 2026-10-01 06:50 SAST (Grok Bot, princess-baylin): Merged SHARED_UPDATES across all four repos via GitHub API this morning; rewriting Princess Baylin section and pushing the merged file to all four repos on main via cloud agents (prior Day 5 note said sibling pushes were blocked). Pipeline equal-priority line already present; no Pipeline edit.
- 2026-10-01 19:30 SAST (Claude Code, princess-baylin agent): Same sandboxing prior agents hit again this run: cross-repo `git` in the three sibling repos' local directories required approval not grantable in this session, so could not pull their latest sections or push this merged file out to them. Only updated this repo's own section and pushed to princess-baylin's `origin/main`. Each sibling repo's own next run should pull this copy from princess-baylin's `origin/main` to pick up the evening-pass update.
- 2026-10-02 06:27 SAST (Printables Repo agent): Printables Day 6 morning run. One-on-One listing patched to match built PDF. Next build: Shift Incident Log PDFs. Still 0 live listings.
