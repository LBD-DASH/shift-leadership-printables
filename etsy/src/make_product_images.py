"""Etsy listing-image packs for the built products (fork of etsy/src/make_images.py).

Same visual system as the Shift Handover set (etsy/listing-0*.png): navy gradient hero,
cream close-up, cream what-you-get, navy how-it-works, 2000x1500 RGB PNG.

Run from anywhere:  python3 etsy/src/make_product_images.py [one-on-one|incident-log|30-60-90|feedback-log|weekly-check-in|handover|starter-toolkit ...]
All paths below are repo-relative (the script changes into the repo root first).

Render step (done by this script, one command per PDF size):
  pdftoppm -r 300 -png products/<folder>/<file>-A4.pdf     etsy/src/renders/<key>/sheet-A4-p
  pdftoppm -r 300 -png products/<folder>/<file>-Letter.pdf etsy/src/renders/<key>/sheet-Letter-p
  then sheet-<size>-p-<n>.png is renamed to sheet-<size>-p<n>.png

On-image text is taken from the matching etsy/LISTING_*.md file (product name, title
phrases, WHAT YOU GET, HOW TO USE IT). No prices, stars, sales, reviews or favourites.
"""
import os, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

os.chdir(Path(__file__).resolve().parents[2])   # repo root; every path below is repo-relative

PLAYFAIR = "assets/fonts/playfair-display/PlayfairDisplay[wght].ttf"
SOURCE = "assets/fonts/source-sans-3/SourceSans3[wght].ttf"
MARK_FILE = "assets/brand/lbd-mark-reversed-cream.png"

def hx(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
NAVY = hx("#0F1F2E"); TEAL = hx("#2A7B88"); GOLD = hx("#C8A864"); CREAM = hx("#F8F6F1")
NAVY2 = hx("#142838")
MUTED_ON_NAVY = (205, 210, 214)
INK_MUTED = (96, 106, 115)
HAIR = (221, 223, 222)
BRAND = "Leadership by Design"
LW, LH = 2000, 1500

# ---------------- products (copy from etsy/LISTING_*.md only) ----------------
PRODUCTS = {
    "one-on-one": dict(
        pdf="products/one-on-one-meeting-template/one-on-one-meeting-template",
        pages=2,
        label="PRINTABLE PDF \u00b7 2 PAGES",
        name=("One-on-One", "Meeting Template"),
        sub="Manager 1:1 Agenda + 12 Month Tracker",
        hero_front=("A4", 1), hero_back=[("Letter", 2)],
        closeup_page=1,
        closeup_head="Stop guessing what to cover in a 1:1.",
        ticks=[("2 print-ready PDFs", "A4 and US Letter, 2 pages each"),
               ("Page 1: the meeting sheet", "Page 2: the 12-month tracker"),
               ("Instant download", "Nothing is shipped"),
               ("Print at home or at work", "In colour or black and white")],
        step4="Work through the sheet together",
    ),
    "incident-log": dict(
        pdf="products/shift-incident-log/shift-incident-log",
        pages=2,
        label="PRINTABLE PDF \u00b7 2 PAGES",
        name=("Shift Incident", "Report Form"),
        sub="Workplace Incident Log + Weekly Tracker",
        hero_front=("A4", 1), hero_back=[("Letter", 2)],
        closeup_page=1,
        closeup_head="Stop losing mid-shift problems between people.",
        ticks=[("2 print-ready PDFs", "A4 and US Letter, 2 pages each"),
               ("Page 1: the incident sheet", "Page 2: the weekly tracker"),
               ("Instant download", "Nothing is shipped"),
               ("Print at home or at work", "In colour or black and white")],
        step4="Update Page 2 at every handover",
    ),
    "30-60-90": dict(
        pdf="products/new-manager-30-60-90-day-plan/new-manager-30-60-90-day-plan",
        pages=3,
        label="PRINTABLE PDF \u00b7 3 PAGES",
        name=("New Manager", "30-60-90 Day Plan"),
        sub="First 90 Days Planner for Team Leaders",
        hero_front=("A4", 2), hero_back=[("A4", 1), ("Letter", 3)],
        closeup_page=2,
        closeup_head="Your first 90 days as a manager, on three pages.",
        ticks=[("2 print-ready PDFs", "A4 and US Letter, 3 pages each"),
               ("The three phases", "Days 1 to 30, 31 to 60 and 61 to 90"),
               ("13-week check-in", "One row per week"),
               ("Instant download", "Nothing is shipped")],
        step4="Work through one phase at a time",
    ),
    "feedback-log": dict(
        pdf="products/feedback-conversation-log/feedback-conversation-log",
        pages=2,
        label="PRINTABLE PDF \u00b7 2 PAGES",
        name=("Feedback", "Conversation Log"),
        sub="Manager Feedback Form + Monthly Index",
        hero_front=("A4", 1), hero_back=[("Letter", 2)],
        closeup_page=1,
        closeup_head="Feedback that is fair, short and written down.",
        ticks=[("2 print-ready PDFs", "A4 and US Letter, 2 pages each"),
               ("Page 1: one conversation", "Page 2: the monthly index"),
               ("Instant download", "Nothing is shipped"),
               ("Print at home or at work", "In colour or black and white")],
        step4="Add one line to Page 2",
    ),
    "weekly-check-in": dict(
        pdf="products/weekly-team-check-in/weekly-team-check-in",
        pages=2,
        label="PRINTABLE PDF \u00b7 2 PAGES",
        name=("Weekly Team", "Check-in"),
        sub="15 Minute Huddle Sheet + Monthly Team Pulse",
        hero_front=("A4", 1), hero_back=[("Letter", 2)],
        closeup_page=1,
        closeup_head="A team check-in that ends with owners and dates.",
        ticks=[("2 print-ready PDFs", "A4 and US Letter, 2 pages each"),
               ("Page 1: the huddle sheet", "Page 2: the monthly pulse"),
               ("Instant download", "Nothing is shipped"),
               ("Print at home or at work", "In colour or black and white")],
        step4="Go round the team once",
    ),
    "handover": dict(
        pdf="products/shift-handover-sheet/shift-handover-sheet",
        pages=1,
        label="PRINTABLE PDF \u00b7 1 PAGE",
        name=("Shift Handover", "Sheet"),
        sub="Supervisor Shift Change Report",
        hero_front=("A4", 1), hero_back=[("Letter", 1)],
        closeup_page=1,
        closeup_head="Stop losing information between shifts.",
        ticks=[("2 print-ready PDFs", "A4 and US Letter, 1 page each"),
               ("Eight handover blocks", "Staffing, safety, output, equipment, tasks and more"),
               ("Instant download", "Nothing is shipped"),
               ("Print at home or at work", "In colour or black and white")],
        step4="Walk it through, then both sign",
    ),
    "starter-toolkit": dict(
        pdf="products/new-manager-starter-toolkit/new-manager-starter-toolkit",
        pages=9,
        label="PRINTABLE PDF \u00b7 9 PAGES",
        name=("New Manager", "Starter Toolkit"),
        sub="30-60-90 Plan, One-on-One, Team Check-in, Feedback Log",
        hero_front=("A4", 2), hero_back=[("A4", 4), ("A4", 6)],
        closeup_page=6,
        closeup_head="Four routines for your first 90 days as a manager.",
        ticks=[("2 print-ready PDFs", "A4 and US Letter, 9 pages each"),
               ("Four tools in one file", "Plan, 1:1, huddle and feedback"),
               ("Instant download", "Nothing is shipped"),
               ("Print at home or at work", "In colour or black and white")],
        step4="Start with the 90-day plan",
    ),
}

# ---------------- type helpers (as make_images.py) ----------------
_cache = {}
def font(kind, size, wght):
    key = (kind, size, wght)
    if key not in _cache:
        f = ImageFont.truetype({"serif": PLAYFAIR, "sans": SOURCE}[kind], size)
        f.set_variation_by_axes([wght]); _cache[key] = f
    return _cache[key]
def serif(s, w=600): return font("serif", s, w)
def sans(s, w=400): return font("sans", s, w)

def tw(d, t, f, sp=0):
    b = d.textbbox((0, 0), t, font=f); return b[2] - b[0] + sp * max(0, len(t) - 1)
def fit(d, t, maker, maxw, start, sp=0):
    s = start
    while tw(d, t, maker(s), sp) > maxw: s -= 2
    return maker(s)
def tracked(d, xy, t, f, fill, sp, anchor="l"):
    x, y = xy
    total = tw(d, t, f, sp)
    if anchor == "m": x -= total / 2
    elif anchor == "r": x -= total
    for ch in t:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + sp
    return total
def wrap(d, t, f, maxw):
    lines, cur = [], ""
    for w in t.split():
        nxt = (cur + " " + w).strip()
        if tw(d, nxt, f) <= maxw or not cur: cur = nxt
        else: lines.append(cur); cur = w
    lines.append(cur)
    if len(lines) == 2:   # balance two-line labels so no single orphan word
        ws = t.split()
        best = min(range(1, len(ws)), key=lambda i: max(tw(d, " ".join(ws[:i]), f), tw(d, " ".join(ws[i:]), f)))
        lines = [" ".join(ws[:best]), " ".join(ws[best:])]
    return lines

# ---------------- brand mark ----------------
MARK_REV = Image.open(MARK_FILE).convert("RGBA")
def navy_mark(src):
    """Recolour the cream letters to navy (gold bar kept) for cream backgrounds."""
    out = src.copy(); px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a and b > 180: px[x, y] = NAVY + (a,)
    return out
MARK_NAVY = navy_mark(MARK_REV)
def mark(img, h): return img.resize((int(img.width * h / img.height), h), Image.LANCZOS)

def brand_lockup(canvas, x, y, h, dark=True, anchor="l"):
    d = ImageDraw.Draw(canvas)
    m = mark(MARK_REV if dark else MARK_NAVY, h)
    f = sans(int(h * 0.36), 500); sp = int(h * 0.075); gap = int(h * 0.45)
    total = m.width + gap * 2 + 2 + tw(d, BRAND.upper(), f, sp)
    if anchor == "r": x -= total
    if anchor == "m": x -= total // 2
    canvas.alpha_composite(m, (int(x), int(y)))
    lx = x + m.width + gap
    d.line((lx, y + h * 0.1, lx, y + h * 0.9), fill=(GOLD if dark else HAIR), width=2)
    bb = d.textbbox((0, 0), "L", font=f)
    tracked(d, (lx + gap, y + h / 2 - (bb[1] + bb[3]) / 2), BRAND.upper(), f, CREAM if dark else NAVY, sp)
    return total

def paste_shadow(bg, img, xy, angle=0, blur=18, off=(14, 20), alpha=90):
    im = img.convert("RGBA")
    if angle: im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", (im.width + blur * 4, im.height + blur * 4), (0, 0, 0, 0))
    m = im.split()[3].point(lambda a: alpha if a > 0 else 0)
    blk = Image.new("RGBA", im.size, (5, 12, 20, 255)); blk.putalpha(m)
    sh.paste(blk, (blur * 2, blur * 2), blk)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    bg.alpha_composite(sh, (xy[0] - blur * 2 + off[0], xy[1] - blur * 2 + off[1]))
    bg.alpha_composite(im, xy)
    return im.size

def vgrad(w, h, c1, c2):
    g = Image.new("RGB", (w, h)); gd = ImageDraw.Draw(g)
    for i in range(h):
        t = i / (h - 1); gd.line((0, i, w, i), fill=tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3)))
    return g

def by_h(img, h): return img.resize((int(img.width * h / img.height), h), Image.LANCZOS)

# ---------------- render ----------------
def render(key, p):
    rd = Path("etsy/src/renders") / key
    rd.mkdir(parents=True, exist_ok=True)
    for size in ("A4", "Letter"):
        subprocess.run(["pdftoppm", "-r", "300", "-png", f"{p['pdf']}-{size}.pdf",
                        str(rd / f"sheet-{size}-p")], check=True)
        for n in range(1, p["pages"] + 1):
            src = rd / f"sheet-{size}-p-{n}.png"
            if src.exists(): src.replace(rd / f"sheet-{size}-p{n}.png")
    return {(s, n): Image.open(rd / f"sheet-{s}-p{n}.png").convert("RGB")
            for s in ("A4", "Letter") for n in range(1, p["pages"] + 1)}

# ---------------- the four listing images ----------------
def hero(p, S, out):
    im = vgrad(LW, LH, NAVY, NAVY2).convert("RGBA"); d = ImageDraw.Draw(im)
    d.rectangle((1000, 0, LW, LH), fill=hx("#1A3347"))
    th = 1100
    backs = p["hero_back"]
    if len(backs) == 1:
        paste_shadow(im, by_h(S[backs[0]], th), (1070, 140), 3, blur=24, off=(16, 26), alpha=170)
    else:
        paste_shadow(im, by_h(S[backs[0]], th - 40), (1150, 110), 7, blur=24, off=(16, 26), alpha=150)
        paste_shadow(im, by_h(S[backs[1]], th - 20), (1090, 150), 2, blur=24, off=(16, 26), alpha=170)
    paste_shadow(im, by_h(S[p["hero_front"]], th), (1030, 190), -4, blur=26, off=(18, 30), alpha=190)
    tx = 110
    tracked(d, (tx, 300), p["label"], sans(36, 600), GOLD, 11)
    l1, l2 = p["name"]
    fh = fit(d, max(l1, l2, key=lambda s: tw(d, s, serif(140))), lambda s: serif(s, 600), 820, 140)
    d.text((tx, 390), l1, font=fh, fill=CREAM)
    y2 = 390 + int(fh.size * 1.18)
    d.text((tx, y2), l2, font=fh, fill=CREAM)
    # Playfair old-style figures (3, 9) drop below the baseline, so keep the rule clear of them
    yl = max(390 + int(fh.size * 2.55), d.textbbox((tx, y2), l2, font=fh)[3] + 45)
    d.line((tx, yl, tx + 150, yl), fill=GOLD, width=5)
    d.text((tx, yl + 50), "A4 & US Letter", font=sans(62, 600), fill=CREAM)
    d.text((tx, yl + 135), p["sub"], font=fit(d, p["sub"], lambda s: sans(s, 400), 820, 44), fill=MUTED_ON_NAVY)
    brand_lockup(im, tx, 1300, 90, dark=True)
    im.convert("RGB").save(out, optimize=True)

def closeup(p, S, out):
    im = Image.new("RGBA", (LW, LH), CREAM + (255,)); d = ImageDraw.Draw(im)
    sheet = S[("A4", p["closeup_page"])]
    crop = sheet.crop((0, 0, sheet.width, int(sheet.width * 0.62)))
    cw = 1760; ch = int(crop.height * cw / crop.width)
    crop = crop.resize((cw, ch), Image.LANCZOS)
    top = LH - ch - 60; bar_h = top - 50
    d.rectangle((0, 0, LW, bar_h), fill=NAVY)
    paste_shadow(im, crop, (120, top), blur=22, off=(0, 18), alpha=80)
    tracked(d, (120, 70), "CLOSE-UP", sans(30, 600), GOLD, 10)
    head = p["closeup_head"]
    d.text((120, 125), head, font=fit(d, head, lambda s: serif(s, 600), 1760, 72), fill=CREAM)
    im.convert("RGB").save(out, optimize=True)

def what_you_get(p, S, out):
    im = Image.new("RGBA", (LW, LH), CREAM + (255,)); d = ImageDraw.Draw(im)
    tracked(d, (LW / 2, 95), "INCLUDED IN YOUR DOWNLOAD", sans(30, 600), TEAL, 10, anchor="m")
    d.text((LW / 2, 215), "What you get", font=serif(104, 600), fill=NAVY, anchor="mm")
    d.line((LW / 2 - 80, 300, LW / 2 + 80, 300), fill=GOLD, width=5)
    th = 680; n = min(p["pages"], 3); step = 22
    for size, x, lab in [("A4", 90, "A4 PDF"), ("Letter", 630, "US Letter PDF")]:
        first = by_h(S[(size, 1)], th)
        # later pages peek out behind page 1, offset up and right
        for k in range(n, 1, -1):
            paste_shadow(im, by_h(S[(size, k)], th), (x + step * (k - 1), 395 - step * (k - 1)),
                         blur=14, off=(6, 12), alpha=55)
        paste_shadow(im, first, (x, 395), blur=18, off=(10, 18), alpha=70)
        c = x + first.width // 2 + step * (n - 1) // 2
        d.rounded_rectangle((c - 180, 1140, c + 180, 1220), 8, fill=NAVY)
        d.text((c, 1180), lab, font=sans(40, 600), fill=CREAM, anchor="mm")
    ix, iy = 1220, 400
    for t, s in p["ticks"]:
        d.ellipse((ix, iy, ix + 80, iy + 80), fill=TEAL)
        d.line((ix + 21, iy + 42, ix + 35, iy + 57, ix + 60, iy + 27), fill=CREAM, width=9, joint="curve")
        ft = fit(d, t, lambda z: serif(z, 600), 580, 52)
        d.text((ix + 112, iy - 4), t, font=ft, fill=NAVY)
        fs = sans(36, 400); lines = wrap(d, s, fs, 580)
        for i, ln in enumerate(lines):
            d.text((ix + 112, iy + 70 + i * 44), ln, font=fs, fill=INK_MUTED)
        iy += 205
    d.line((90, 1340, LW - 90, 1340), fill=HAIR, width=2)
    brand_lockup(im, LW - 90, 1375, 64, dark=False, anchor="r")
    im.convert("RGB").save(out, optimize=True)

def how_it_works(p, out):
    im = vgrad(LW, LH, NAVY, NAVY2).convert("RGBA"); d = ImageDraw.Draw(im)
    tracked(d, (LW / 2, 140), "FOUR SIMPLE STEPS", sans(30, 600), GOLD, 10, anchor="m")
    d.text((LW / 2, 265), "How it works", font=serif(110, 600), fill=CREAM, anchor="mm")
    d.line((LW / 2 - 80, 360, LW / 2 + 80, 360), fill=GOLD, width=5)
    steps = [("Buy", "Check out on Etsy"), ("Download", "A4 & Letter PDFs"),
             ("Print", "At home or at work"), ("Use", p["step4"])]
    colw = 440; x0 = (LW - colw * 4) // 2; cy = 730
    d.line((x0 + colw / 2, cy, x0 + colw * 3.5, cy), fill=hx("#2E4457"), width=4)
    for i, (t, s) in enumerate(steps):
        c = x0 + colw * i + colw / 2
        d.ellipse((c - 125, cy - 125, c + 125, cy + 125), fill=NAVY, outline=GOLD, width=6)
        d.text((c, cy - 8), str(i + 1), font=serif(150, 600), fill=GOLD, anchor="mm")
        d.text((c, cy + 235), t, font=fit(d, t, lambda z: serif(z, 600), colw - 40, 68), fill=CREAM, anchor="mm")
        fs = sans(40, 400)
        for j, ln in enumerate(wrap(d, s, fs, colw - 50)):
            d.text((c, cy + 320 + j * 52), ln, font=fs, fill=MUTED_ON_NAVY, anchor="mm")
    d.text((LW / 2, 1250), "Instant download after purchase. Nothing is shipped.", font=sans(38, 400),
           fill=MUTED_ON_NAVY, anchor="mm")
    brand_lockup(im, LW / 2, 1340, 70, dark=True, anchor="m")
    im.convert("RGB").save(out, optimize=True)

def build(key):
    p = PRODUCTS[key]; S = render(key, p)
    od = Path("etsy") / key; od.mkdir(parents=True, exist_ok=True)
    hero(p, S, od / "listing-01-hero.png")
    closeup(p, S, od / "listing-02-closeup.png")
    what_you_get(p, S, od / "listing-03-what-you-get.png")
    how_it_works(p, od / "listing-04-how-it-works.png")
    print("built", od)

if __name__ == "__main__":
    for k in (sys.argv[1:] or list(PRODUCTS)): build(k)
