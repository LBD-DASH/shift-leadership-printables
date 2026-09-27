# Weekly metrics review: Shift & Leadership Printables (Canva templates)

_Run once a week (Mondays suggested). It isn't part of the daily schedule: paste it into a chat assistant, or run `python scripts/run_prompts.py weekly-metrics-review`._

## Inputs
Use the repo's `README.md` (the plan, money model, 30-day plan and success/kill criteria), the most recent files in `logs/` (newest first) and anything in `from-cto-new/`. If you're pasting this prompt into a chat assistant, paste or attach those files below it. If no logs are supplied, treat today as Day 1 of the 30-day plan.

## Task
1. Pull these metrics from the logs for the last 7 days and the 7 days before that: listings live (Etsy, Gumroad), new listings, Etsy views, favourites, orders, revenue (ZAR), conversion rate, Gumroad sales, Pinterest clicks, ad spend.
2. Show them as a small table with week-on-week change. Write "unknown" where a number is missing.
3. Rank the top 5 listings by views and by sales. Name the product types (handover, check-in, 1:1, planner, bundle) that convert best and the search terms that bring the most views, if logged.
4. Say what worked, what didn't, and one experiment for next week.
5. Measure progress against the success/kill criteria in the README. Recommend **continue**, **adjust** or **kill**, with a one-line reason.
6. List the metrics Kevin should paste into next week's logs so the next review has real numbers.

## Output
Reply with a single markdown section that starts with the heading `## Weekly metrics review`. It gets appended to `logs/YYYY-MM-DD.md` (today's date), either by the daily workflow or by Kevin pasting it in.

Rules:
- Don't make up numbers. If a metric isn't in the logs, write "unknown" and say who needs to supply it.
- Keep it short and specific. Kevin should be able to act on it in under 5 minutes.
- Mark anything that needs Kevin personally (accounts, KYC, payments, approvals, reviews) with **[KEVIN]**.
