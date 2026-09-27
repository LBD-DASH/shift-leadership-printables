# Shift & Leadership Printables (Canva templates)

> **Start here:** read [SHARED_UPDATES.md](SHARED_UPDATES.md) for the status of all four sister projects, and write your update back into it.

_Repo: `shift-leadership-printables`. Side venture, separate from YardOps, 6HN and LBD. Background research: `blackvault/new-income-ideas-2026-09-27.md` (27 Sep 2026)._

## The idea
We design practical, downloadable printables for shift work and leadership exercises: team check-in sheets, shift handover sheets, manager one-on-one templates, shift planners, toolbox-talk and stand-up sheets, and manager starter toolkits. Each product is built as an editable Canva template (shared via a Canva template link) plus a print-ready PDF, and sold as a digital download on Etsy or Gumroad. Buyers find them through marketplace search, so we don't need an audience first.

## Target platform
Etsy (main channel, pays out in ZAR through Etsy Payments) and Gumroad (mirror listings, ZAR bank payouts). Pinterest is used as free traffic.

## How money is made
- One-off digital download sales: single templates at $6–18 and bundles or toolkits at $20–30.
- Fees (research estimates, check current rates): Etsy is about 12–13% all-in (listing $0.20, transaction 6.5%, processing 4.5% + R8, plus Offsite Ads 12–15% on attributed sales). Gumroad is about 10% + $0.50.
- Research estimate for the category (not a promise): month 1 R0–800, month 3 R500–5,000, month 6 R2,000–15,000. The top of that range needs 50+ good listings and bundles.

## First 30 days
- **Days 1–3:** Research niches using Etsy autocomplete, bestsellers, review counts and prices for searches like shift handover, team check-in, one-on-one template and shift planner. Score 20 product ideas on demand, competition and whether the product needs real design. Shortlist 10.
- **Days 4–10:** Build the first 10 products: real layouts in Canva, editable template link plus PDF, mock-ups, SEO titles, 13 tags each, AI disclosure (if AI was used) and 'Designed by'. Build 1 bundle (for example a new-manager toolkit: 1:1 template + team check-in + handover sheet).
- **Days 11–14:** List 10 products on Etsy **[KEVIN approves]** and mirror them on Gumroad. Set up 3 Pinterest boards.
- **Days 15–30:** Add 5–10 new listings a week (target 25–30 live by day 30). Run a weekly SEO review of views, favourites and conversion. Optionally test R300 of Etsy Ads on the 3 best listings, and stop if it doesn't pay back within 2 weeks.

## Success and kill criteria
**Success (keep going and scale):**
- Day 30: 25+ live listings, at least 1 sale, and 500+ Etsy views in total.
- Week 8: 3+ sales and a view-to-sale conversion around 1% or better on the best listings. Then scale toward 50–60 listings and bundles.

**Kill (stop or change direction):**
- Fewer than 3 sales after 30 listings and 8 weeks: change niche (the research rule).
- Any Etsy originality/IP warning that repeats after a fix: pause and review with Kevin.
- Etsy Ads spend that doesn't pay back within 2 weeks: stop ads.

## What only Kevin can do
- Open the Etsy seller account and Etsy Payments (ID, address, SA bank account, card, 2FA on his own authenticator).
- Open Gumroad and add ZAR payouts. Canva Pro, if used (check Canva's licence terms for selling templates).
- Approve the niche shortlist and the first listings.

## Risks and policy rules
- Etsy Creativity Standards (since 10 Jun 2025): products must be original designs, AI use must be disclosed, and listings must say 'Designed by'. Generic templates and PLR get shops suspended.
- Canva licensing: sell editable template links and your own PDFs, not raw Canva elements; follow Canva's content licence for template sellers.
- Pace uploads so the shop doesn't look like a spam farm. Enforcement is automated and does flag compliant shops too.
- One Etsy shop per person unless Etsy approves more.

## Repo layout
- `README.md`: this plan
- `assets/`: source files and exports (keep large binaries out of git where you can)
- `prompts/`: plain-markdown prompts that work pasted into Claude, ChatGPT or any other assistant
  - `daily-progress-check.md` and `daily-next-content.md` run every day
  - `weekly-metrics-review.md` is run by hand once a week
- `from-cto-new/`: material carried over from cto.new (the prompt runner includes any text files here as context)
- `scripts/run_prompts.py`: runs prompts through OpenAI or Anthropic and appends the output to `logs/YYYY-MM-DD.md`
- `logs/`: one file per day (`YYYY-MM-DD.md`). Agents append output; Kevin pastes real metrics in by hand.
- `.github/workflows/daily-prompts.yml`: runs the two daily prompts at 04:17 UTC (06:17 SAST) every day, or by hand from the Actions tab

## Automation
The daily workflow only calls an LLM if a repo secret `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` exists. Without one it prints `skipped: no API key` and finishes cleanly without committing anything. To switch it on, add one of the secrets under Settings → Secrets and variables → Actions. Optional repo variables: `OPENAI_MODEL` or `ANTHROPIC_MODEL` to pick the model, and `LLM_PROVIDER=anthropic` to prefer Anthropic when both keys are set.

Run locally: `python scripts/run_prompts.py` (daily prompts), `python scripts/run_prompts.py weekly-metrics-review`, or `python scripts/run_prompts.py --all`.

The prompts can only reason over the README, logs and `from-cto-new/`. They can't see platform dashboards, so paste real numbers into the day's log, or the reviews will say "unknown".
