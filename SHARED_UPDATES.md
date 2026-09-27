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

## Faceless YouTube content (faceless-youtube-content), the pipeline's distribution
Last updated: 2026-09-27 16:45 SAST (Grok Bot, pipeline restructure)
- **Done:** repo set up. The niche is now locked to narrated Princess Baylin bedtime stories for children, so niche shortlisting has stopped.
- **In progress:** being restructured as the distribution and ad-revenue layer for Princess Baylin.
- **Next (daily run at 06:43 SAST):** one script of about 8 to 10 minutes built from the newest Baylin handoff, written for watch time with a strong opening hook, a calm pace and an ending that leads into the next episode. It also includes 3 title options, a description with keywords and a link to the book or merch, a thumbnail concept, and chapter markers.
- **Needs:** Kevin to approve a channel name and set up the channel when ready; a free voice and animation tool (to be recommended); a "made for kids" setting on every upload.

---

## Cross-project notes
- 2026-09-27 16:30 SAST (Grok Bot): All four repos share this file. Reusable ideas, such as a leadership theme that fits both the printables and YouTube, go here so the other projects can use them.
- 2026-09-27 16:45 SAST (Grok Bot): Kevin merged Princess Baylin and Faceless YouTube into one revenue pipeline (see the Pipeline section at the top). The Printables and AI Stock Images projects are unchanged.
