# prompts/

Plain-markdown prompts with no vendor-specific syntax. They work pasted into Claude, ChatGPT or any other assistant: paste the prompt, then paste or attach `README.md`, the recent `logs/` files and anything in `from-cto-new/`. Save the answer to `logs/YYYY-MM-DD.md`.

| Prompt | When | How |
|---|---|---|
| `daily-progress-check.md` | Daily | Daily workflow (04:17 UTC / 06:17 SAST) or by hand |
| `daily-next-content.md` | Daily | Daily workflow, after the progress check, or by hand |
| `weekly-metrics-review.md` | Weekly (Mondays suggested) | By hand, or `python scripts/run_prompts.py weekly-metrics-review` |
