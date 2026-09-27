#!/usr/bin/env python3
"""Run prompts from prompts/ against an LLM and append the output to logs/YYYY-MM-DD.md.

Usage:
    python scripts/run_prompts.py                      # the two daily prompts (default)
    python scripts/run_prompts.py weekly-metrics-review
    python scripts/run_prompts.py --all                # every prompt in prompts/

Providers (standard library only, no pip installs needed):
- OPENAI_API_KEY    -> OpenAI Chat Completions API (model: OPENAI_MODEL, default gpt-5-mini)
- ANTHROPIC_API_KEY -> Anthropic Messages API       (model: ANTHROPIC_MODEL, default claude-sonnet-4-5)
- If both are set, OpenAI is used unless LLM_PROVIDER=anthropic.
- If neither is set it prints 'skipped: no API key' and exits 0 without writing anything.

Context sent with each prompt: README.md, any text files in from-cto-new/, and the most
recent files in logs/ (including output already written earlier in the same run).
"""
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
LOGS_DIR = ROOT / "logs"
CTO_DIR = ROOT / "from-cto-new"
DAILY = ["daily-progress-check", "daily-next-content"]
ALL_ORDER = ["daily-progress-check", "weekly-metrics-review", "daily-next-content"]
SKIP_NAMES = {"README.md", ".gitkeep"}
TEXT_SUFFIXES = {".md", ".txt", ".csv", ".json", ".yml", ".yaml"}
MAX_LOG_FILES = 7           # recent logs sent as context
MAX_CTO_CHARS = 15000       # cap for carried-over cto.new material
MAX_CONTEXT_CHARS = 60000   # keep requests small and cheap
TIMEOUT = 180

SYSTEM = ("You are an operator agent for a small side business. You cannot browse or take "
          "actions; you can only reason over the README, logs and notes supplied and write the "
          "requested markdown. Be concrete, honest about uncertainty, and never invent metrics: "
          "if a number is not in the logs, say it is unknown.")


def build_context() -> str:
    parts = []
    readme = ROOT / "README.md"
    if readme.exists():
        parts.append("=== README.md ===\n" + readme.read_text(encoding="utf-8"))
    if CTO_DIR.is_dir():
        cto_text = ""
        for p in sorted(CTO_DIR.rglob("*")):
            if p.is_file() and p.name not in SKIP_NAMES and p.suffix.lower() in TEXT_SUFFIXES:
                rel = p.relative_to(ROOT).as_posix()
                cto_text += f"=== {rel} ===\n" + p.read_text(encoding="utf-8", errors="replace") + "\n\n"
        if cto_text:
            parts.append(cto_text[:MAX_CTO_CHARS])
    logs = sorted(p for p in LOGS_DIR.glob("*.md") if p.name not in SKIP_NAMES)[-MAX_LOG_FILES:]
    if not logs:
        parts.append("=== logs/ ===\n(no logs yet: this is the first run, treat today as Day 1)")
    for p in reversed(logs):  # newest first
        parts.append(f"=== logs/{p.name} ===\n" + p.read_text(encoding="utf-8"))
    ctx = "\n\n".join(parts)
    return ctx[:MAX_CONTEXT_CHARS]


def _post(url: str, body: dict, headers: dict) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers={**headers, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"HTTP {e.code}: {detail}") from e


def call_openai(key: str, system: str, user: str) -> str:
    model = os.environ.get("OPENAI_MODEL") or "gpt-5-mini"
    data = _post("https://api.openai.com/v1/chat/completions",
                 {"model": model, "messages": [{"role": "system", "content": system},
                                               {"role": "user", "content": user}]},
                 {"Authorization": f"Bearer {key}"})
    return (data["choices"][0]["message"]["content"] or "").strip()


def call_anthropic(key: str, system: str, user: str) -> str:
    model = os.environ.get("ANTHROPIC_MODEL") or "claude-sonnet-4-5"
    data = _post("https://api.anthropic.com/v1/messages",
                 {"model": model, "max_tokens": 8000, "system": system,
                  "messages": [{"role": "user", "content": user}]},
                 {"x-api-key": key, "anthropic-version": "2023-06-01"})
    return "".join(b.get("text", "") for b in data.get("content", [])).strip()


def pick_provider():
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    pref = os.environ.get("LLM_PROVIDER", "").strip().lower()
    if pref == "anthropic" and anthropic_key:
        return "anthropic", lambda s, u: call_anthropic(anthropic_key, s, u)
    if openai_key:
        return "openai", lambda s, u: call_openai(openai_key, s, u)
    if anthropic_key:
        return "anthropic", lambda s, u: call_anthropic(anthropic_key, s, u)
    return None, None


def select_prompts(args):
    if "--all" in args:
        names = ALL_ORDER + sorted(p.stem for p in PROMPTS_DIR.glob("*.md")
                                   if p.name not in SKIP_NAMES and p.stem not in ALL_ORDER)
    elif args:
        names = [pathlib.Path(a).stem for a in args]
    else:
        names = DAILY
    files = []
    for n in names:
        p = PROMPTS_DIR / f"{n}.md"
        if not p.exists():
            raise SystemExit(f"Prompt not found: prompts/{n}.md")
        files.append(p)
    return files


def main(argv) -> int:
    files = select_prompts(argv)
    provider, call = pick_provider()
    if provider is None:
        print("skipped: no API key (set an OPENAI_API_KEY or ANTHROPIC_API_KEY secret to enable)")
        return 0

    now = dt.datetime.now(dt.timezone.utc)
    today = now.strftime("%Y-%m-%d")
    weekday = now.strftime("%A")
    LOGS_DIR.mkdir(exist_ok=True)
    log_path = LOGS_DIR / f"{today}.md"
    for pf in files:
        ctx = build_context()  # rebuilt so later prompts see earlier output from today
        user = (f"Today is {weekday} {today} (UTC). Repository files follow.\n\n{ctx}\n\n"
                f"=== TASK: prompts/{pf.name} ===\n{pf.read_text(encoding='utf-8')}\n\n"
                "Return only the markdown section to append to today's log.")
        try:
            out = call(SYSTEM, user) or "_empty response_"
        except (urllib.error.URLError, RuntimeError, KeyError, IndexError, ValueError,
                TimeoutError) as e:
            out = f"_error calling {provider}: {type(e).__name__}: {e}_"
            print(f"{pf.name}: error {e}", file=sys.stderr)
        with log_path.open("a", encoding="utf-8") as f:
            if f.tell() == 0:
                f.write(f"# Log {today}\n")
            f.write(f"\n<!-- {pf.stem} | {provider} | {now.strftime('%H:%M')} UTC -->\n\n{out}\n")
        print(f"{pf.name}: written to logs/{log_path.name}")
    # Exit 0 even on API errors so the error text is still committed and visible.
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
