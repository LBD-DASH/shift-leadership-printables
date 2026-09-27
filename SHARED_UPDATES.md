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

## Sync rule (for the repo agents)
On every run, the agent:
1. Reads `SHARED_UPDATES.md` from all four repos.
2. Builds a merged copy. For each project section, it keeps the version with the newest `Last updated`. It keeps every Cross-project note that appears in any copy, removes duplicates and sorts them by date.
3. Applies its own update.
4. Writes the merged file to all four repos on `main`.

Nothing is deleted without a note explaining why. The file stays plain markdown so any model can read and write it.

---

## Pipeline: Princess Baylin and Faceless YouTube are one business (decided by Kevin, 2026-09-27)
These two repos are **one money-making pipeline**, not two brands. The repo names stay the same for now.
- **princess-baylin is the source.** It owns the stories, characters, book manuscripts and merch concepts.
- **faceless-youtube-content is the distribution and ad-revenue layer.** Its niche is locked to narrated Princess Baylin bedtime stories for children. Every script, title, description and thumbnail is built from Baylin material.
- **Handoff:** each Baylin run writes `handoff/youtube/YYYY-MM-DD.md` in princess-baylin, containing the story beats, the characters in the episode, the lesson, a hook line and visual notes. The YouTube agent reads the newest handoff. If none is newer than its last script, it uses the latest Baylin outline or manuscript.
- **Income first.** Baylin's priorities are children's book drafts (for Amazon KDP or print on demand) and merch concepts. YouTube's priorities are scripts built for watch time and ad revenue.
- **Honest limit:** YouTube treats children's content as "made for kids", which means no personalised ads (so lower ad rates), no comments and no mini-player. Books and merch are expected to earn more than ads, so the YouTube channel also drives viewers to them.
- **Rules that still apply:** English, Afrikaans and isiZulu, with a native-speaker check before anything is published. No identifying details about the child. AI use is disclosed where platforms require it. Everything is a draft for Kevin, and nothing is published or listed without his approval. No paid API key.

---

## Shift and leadership printables (shift-leadership-printables)
Last updated: 2026-09-27 16:30 SAST (Grok Bot, setup)
- **Done:** repo created with README, prompts, daily Action (06:17 SAST, skips without an API key) and a from-cto-new folder.
- **In progress:** first daily run by the Printables Repo agent.
- **Next:** pick the first printable (for example a shift handover sheet) and draft its layout, copy and Etsy listing.
- **Needs:** nothing yet.

## AI stock images (ai-stock-images)
Last updated: 2026-09-27 16:30 SAST (Grok Bot, setup)
- **Done:** repo created with README, prompts, daily Action and a from-cto-new folder.
- **In progress:** first daily run by the AI Stock Images Repo agent.
- **Next:** first themed batch of image prompts, keywords and titles, disclosed as AI-generated.
- **Needs:** a decision on the image generator to use (a free option first).

## Princess Baylin (princess-baylin), the pipeline's source
Last updated: 2026-09-27 16:45 SAST (Grok Bot, pipeline restructure)
- **Done:** repo set up. First daily log is on main with the episode outline "Princess Baylin and the Lost Rain Song" in English, Afrikaans and isiZulu (commit 2cf1a6e).
- **In progress:** being restructured as the source for the YouTube channel.
- **Next (daily run at 06:37 SAST):** a first draft of a picture-book manuscript (about 12 spreads, English first, Afrikaans and isiZulu marked for a native-speaker check); 3 to 5 merch concepts, such as prints, colouring pages, plush toys and bedtime cards; and `handoff/youtube/YYYY-MM-DD.md` for the YouTube agent.
- **Needs:** Kevin to add the original story to `assets/story/`; native-speaker reviewers for Afrikaans and isiZulu; Kevin's choice of book platform (for example Amazon KDP).

## Faceless YouTube content (faceless-youtube-content), Princess Baylin bedtime-story channel (runs in parallel with princess-baylin)
Last updated: 2026-09-27 16:32 SAST (Grok Bot, first daily run). Note: the earlier "16:45" stamps in this file were ahead of the clock; the commit that wrote them landed at 16:29 SAST.
- **Done:** niche locked to narrated Princess Baylin bedtime stories (Kevin). First daily log [`logs/2026-09-27.md`](https://github.com/LBD-DASH/faceless-youtube-content/blob/main/logs/2026-09-27.md): YouTube rules checked against official pages (made for kids, AI disclosure, YPP thresholds including the 8,000-hour bar for new applicants from 1 Feb 2027, and the inauthentic-content policy); free tool shortlist with licence notes; Episode 1 video plan for "Princess Baylin and the Lost Rain Song". README and prompts updated for the locked niche and the parallel projects.
- **In progress:** Episode 1 script. princess-baylin has no `handoff/youtube/` file yet, so it's built from the princess-baylin log of 27 Sep 2026.
- **Next (Mon 28 Sep):** the full 8–10 minute English voiceover script (about 1,000–1,250 words, an estimate), a shot list for the 12 scenes, the Short script, and notes for the Afrikaans and isiZulu adaptations.
- **Needs:** [KEVIN] original story in princess-baylin `assets/story/` (the current cast is placeholders); a narrator choice (own or family voice recommended, or Kokoro TTS for English, which is Apache 2.0); native-speaker narrators or reviewers for Afrikaans and isiZulu (no free commercial-use TTS found for those languages); a channel name; whether to always disclose an AI voice or AI music.

---

## Cross-project notes
- 2026-09-27 16:30 SAST (Grok Bot): All four repos share this file. Reusable ideas, such as a leadership theme that fits both the printables and YouTube, go here so the other projects can use them.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content): **Kevin's latest decision:** the YouTube channel and princess-baylin run **in parallel with equal weight**, and the channel isn't just a funnel. The Pipeline section above ("one business", "distribution layer") was written earlier, so Kevin should update its wording. It's left unchanged here because agents only edit their own section.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Made for kids turns off cards, end screens and the merchandise shelf** (https://support.google.com/youtube/answer/9527654). The channel can't sell Baylin books or merch through YouTube's merch features, and "heavily promotional" is a low-quality signal for kids content (https://support.google.com/youtube/answer/10774223). Book and merch sales need their own route (shop listing, book platform); don't rely on YouTube for them.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Story and character requests.** (1) A fixed character sheet for Baylin and each recurring friend (appearance, catchphrase, one flaw) so every episode looks consistent. (2) Episodes 2–4 should use new settings (for example night sky, river, market day) and new kinds of resolution (making amends, trying something new, patience), not listening again. (3) One small recurring bedtime ritual Baylin does at the end of every story, for a calm, familiar ending. (4) Please start `handoff/youtube/YYYY-MM-DD.md` with beats, cast, lesson, hook line and visual notes.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Title and theme ideas that hold watch time** (calm, no keyword stuffing, no distress-bait): "Princess Baylin and the Sleepy Moon", "Princess Baylin and the Quiet Star", "Princess Baylin and the River That Whispered", "Princess Baylin and the Very Patient Tortoise", "Princess Baylin Says Sorry". Themes: listening, patience, saying sorry, sharing, being brave in a small way, gratitude.
- 2026-09-27 16:32 SAST (Grok Bot, faceless-youtube-content) for princess-baylin: **Possible book and merch items from Episode 1:** a "Lost Rain Song" picture book (12 spreads, trilingual); a rain-song colouring page set (frogs, grasshoppers, the grandmother tree, the Rainbird); a printable "Listen… what do you hear?" bedtime listening card; a Tilly the tortoise plush (once the cast is confirmed as canon); a trilingual goodnight poster ("Thank you, friends!" / "Dankie, vriende!" / "Siyabonga, bangane!", after the native-speaker check).
- 2026-09-27 16:45 SAST (Grok Bot): Kevin merged Princess Baylin and Faceless YouTube into one revenue pipeline (see the Pipeline section at the top). The Printables and AI Stock Images projects are unchanged.
