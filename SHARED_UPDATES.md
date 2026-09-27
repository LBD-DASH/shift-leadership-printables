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

## Princess Baylin (princess-baylin)
Last updated: 2026-09-27 16:30 SAST (Grok Bot, setup)
- **Done:** repo created. Every prompt requires English, Afrikaans and isiZulu, with a native-speaker check, and no identifying details about the child.
- **In progress:** first daily run by the Princess Baylin Repo agent.
- **Next:** episode 1 outline in all three languages.
- **Needs:** Kevin to add his daughter's original story to `assets/story/`, and native-speaker reviewers for Afrikaans and isiZulu.

## Faceless YouTube content (faceless-youtube-content)
Last updated: 2026-09-27 16:30 SAST (Grok Bot, setup)
- **Done:** repo created with README, prompts, daily Action and a from-cto-new folder.
- **In progress:** first daily run by the Faceless YouTube Repo agent.
- **Next:** shortlist and score niches, and check YouTube's current AI-content and monetisation rules.
- **Needs:** Kevin to choose a niche from the shortlist.

---

## Cross-project notes
- 2026-09-27 16:30 SAST (Grok Bot): All four repos share this file. Reusable ideas, such as a leadership theme that fits both the printables and YouTube, go here so the other projects can use them.
