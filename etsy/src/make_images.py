"""Etsy shop images, v2 - rebranded to leadershipbydesign.co.

Brand source (see SHOP_COPY.md / brand/BRAND_NOTES.md):
  --lbd-navy #0F1F2E, --lbd-teal #2A7B88, --lbd-gold #C8A864, --lbd-cream #F8F6F1
  Headings: Playfair Display (600), body: Source Sans 3
  Logo: https://www.leadershipbydesign.co/favicon.png  (L|BD mark)
Product sheets are rendered from the unchanged PDFs (src/renders/*.png).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/workspace/side-ventures/printables/etsy/"
OUT = BASE
R = BASE + "src/renders/"
BR = BASE + "brand/"
G = "/usr/share/fonts/truetype/sand-box/google/"
PLAYFAIR = G + "Playfair Display/PlayfairDisplay-VariableFont_wght.ttf"
PLAYFAIR_I = G + "Playfair Display/PlayfairDisplay-Italic-VariableFont_wght.ttf"
SOURCE = G + "Source Sans 3/SourceSans3-VariableFont_wght.ttf"

def hx(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
NAVY = hx("#0F1F2E"); TEAL = hx("#2A7B88"); GOLD = hx("#C8A864"); CREAM = hx("#F8F6F1")
NAVY2 = hx("#142838")            # hsl(207 42% 15%) = site --card (dark theme)
MUTED_ON_NAVY = (205, 210, 214)   # cream-muted look (rgba(248,246,241,.7) on navy)
INK_MUTED = (96, 106, 115)        # rgba(15,31,46,.65) on cream
HAIR = (221, 223, 222)            # rgba(15,31,46,.1) on cream
BRAND = "Leadership by Design"
TAGLINE = "Built by design. Not by default."

_cache = {}
def font(kind, size, wght):
    key = (kind, size, wght)
    if key not in _cache:
        path = {"serif": PLAYFAIR, "serif-i": PLAYFAIR_I, "sans": SOURCE}[kind]
        f = ImageFont.truetype(path, size); f.set_variation_by_axes([wght]); _cache[key] = f
    return _cache[key]
def serif(s, w=600): return font("serif", s, w)
def serif_i(s, w=500): return font("serif-i", s, w)
def sans(s, w=400): return font("sans", s, w)

def tw(d, t, f, sp=0):
    b = d.textbbox((0, 0), t, font=f); return b[2] - b[0] + sp * max(0, len(t) - 1)
def fit(d, t, maker, maxw, start, sp=0):
    s = start
    while tw(d, t, maker(s), sp) > maxw: s -= 2
    return maker(s)

def tracked(d, xy, t, f, fill, sp, anchor="l"):
    """Letter-spaced caps (site uses tracking-[0.3em] uppercase labels)."""
    x, y = xy
    total = tw(d, t, f, sp)
    if anchor == "m": x -= total / 2
    elif anchor == "r": x -= total
    for ch in t:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + sp
    return total

# ---- logo assets (real mark from leadershipbydesign.co/favicon.png) ----
LOGO = Image.open(BR + "lbd-favicon-512.png").convert("RGB")

def logo_rgba(letter_col):
    """Knock the white background out of the real mark; recolour the navy letters
    (gold bar kept). Used only for dark backgrounds."""
    src = LOGO; out = Image.new("RGBA", src.size); sp = src.load(); op = out.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b = sp[x, y]
            dr, db = 255 - r, 255 - b
            if dr < 3 and db < 3: op[x, y] = (0, 0, 0, 0); continue
            if db > 0 and dr / db < 0.6:   # gold pixel (mix of white and #C8A864)
                a = min(255, int(db / 155 * 255)); op[x, y] = GOLD + (a,)
            else:                           # navy pixel (mix of white and #0F1F2E)
                a = min(255, int(dr / 240 * 255)); op[x, y] = letter_col + (a,)
    return out.crop(out.getbbox())

MARK_REV = logo_rgba(CREAM)
MARK_REV.save(BR + "lbd-mark-reversed-cream.png")
MARK_NAVY = logo_rgba(NAVY)
MARK_NAVY.save(BR + "lbd-mark-transparent.png")

def mark(img, h):
    return img.resize((int(img.width * h / img.height), h), Image.LANCZOS)

sheetA4 = Image.open(R + "sheet300-A4.png").convert("RGB")
sheetL = Image.open(R + "sheet300-Letter.png").convert("RGB")

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

def brand_lockup(canvas, x, y, h, dark=True, anchor="l"):
    """Mark + tracked 'LEADERSHIP BY DESIGN' (mirrors lbd-logo-horizontal.png)."""
    d = ImageDraw.Draw(canvas)
    m = mark(MARK_REV if dark else MARK_NAVY, h)
    f = sans(int(h * 0.36), 500); sp = int(h * 0.075)
    gap = int(h * 0.45)
    total = m.width + gap * 2 + 2 + tw(d, BRAND.upper(), f, sp)
    if anchor == "r": x -= total
    if anchor == "m": x -= total // 2
    canvas.alpha_composite(m, (int(x), int(y)))
    lx = x + m.width + gap
    d.line((lx, y + h * 0.1, lx, y + h * 0.9), fill=(GOLD if dark else HAIR) , width=2)
    bb = d.textbbox((0, 0), "L", font=f)
    tracked(d, (lx + gap, y + h / 2 - (bb[1] + bb[3]) / 2), BRAND.upper(), f,
            CREAM if dark else NAVY, sp)
    return total

# ---------- 1. shop icon: the real logo, cropped tighter so it reads at small sizes ----------
cx, cy = 262, 255; half = 196
ic = LOGO.crop((cx - half, cy - half, cx + half, cy + half)).resize((500, 500), Image.LANCZOS)
ic.save(OUT + "shop-icon.png")

# ---------- 2. banner 3360x840 ----------
W, H = 3360, 840
bn = Image.new("RGBA", (W, H), NAVY + (255,))
sky = Image.open(BR + "site-city-skyline-faded.jpg").convert("RGB")
sw = 1700; sky = sky.resize((sw, int(sky.height * sw / sky.width)), Image.LANCZOS)
sky = sky.crop((0, (sky.height - H) // 2 + 80, sw, (sky.height - H) // 2 + 80 + H))
# navy wash over the photo (site overlays dark navy on its skyline imagery)
wash = Image.new("RGB", sky.size, NAVY)
sky = Image.blend(sky, wash, 0.72).convert("RGBA")
fade = Image.new("L", sky.size, 0); fd = ImageDraw.Draw(fade)
for i in range(sw):
    t = min(1, i / 700); fd.line((i, 0, i, H), fill=int(255 * t * t * (3 - 2 * t)))
bn.paste(sky, (W - sw, 0), fade)
d = ImageDraw.Draw(bn)
x0 = 700
mk = mark(MARK_REV, 150)
bn.alpha_composite(mk, (x0, 150))
tracked(d, (x0 + mk.width + 50, 196), "PRINTABLE TEAM LEADER TOOLS", sans(34, 600), GOLD, 10)
tracked(d, (x0 + mk.width + 50, 250), "SHIFT HANDOVER · HUDDLES · CHECK-INS", sans(28, 500), MUTED_ON_NAVY, 7)
ft = fit(d, BRAND, lambda s: serif(s, 600), 2250 - x0, 150)
d.text((x0, 360), BRAND, font=ft, fill=CREAM)
d.line((x0, 580, x0 + 160, 580), fill=GOLD, width=4)
d.text((x0, 615), TAGLINE, font=serif_i(58, 500), fill=GOLD)
th = 580
for img, ang, x, y in [(sheetL, 6, 2560, 120), (sheetA4, -5, 2320, 110)]:
    s = img.resize((int(img.width * th / img.height), th), Image.LANCZOS)
    paste_shadow(bn, s, (x, y), ang, blur=16, off=(12, 18), alpha=150)
bn.convert("RGB").save(OUT + "shop-banner.png")

# ---------- listing helpers ----------
LW, LH = 2000, 1500
def vgrad(w, h, c1, c2):
    g = Image.new("RGB", (w, h)); gd = ImageDraw.Draw(g)
    for i in range(h):
        t = i / (h - 1); gd.line((0, i, w, i), fill=tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3)))
    return g

# ---------- 3a. hero ----------
hero = vgrad(LW, LH, NAVY, NAVY2).convert("RGBA"); d = ImageDraw.Draw(hero)
# slightly lighter navy panel on the right to lift the sheets
d.rounded_rectangle((1000, 0, LW, LH), 0, fill=hx("#1A3347"))
th = 1100
sL = sheetL.resize((int(sheetL.width * th / sheetL.height), th), Image.LANCZOS)
sA = sheetA4.resize((int(sheetA4.width * th / sheetA4.height), th), Image.LANCZOS)
paste_shadow(hero, sL, (1070, 140), 3, blur=24, off=(16, 26), alpha=170)
paste_shadow(hero, sA, (1030, 190), -4, blur=26, off=(18, 30), alpha=190)
tx = 110
tracked(d, (tx, 300), "PRINTABLE PDF", sans(36, 600), GOLD, 11)
fh = fit(d, "Handover Sheet", lambda s: serif(s, 600), 840, 140)
d.text((tx, 390), "Shift", font=fh, fill=CREAM)
d.text((tx, 390 + int(fh.size * 1.18)), "Handover Sheet", font=fh, fill=CREAM)
yl = 390 + int(fh.size * 2.55)
d.line((tx, yl, tx + 150, yl), fill=GOLD, width=5)
d.text((tx, yl + 50), "A4 & US Letter", font=sans(62, 600), fill=CREAM)
d.text((tx, yl + 135), "Instant download. Print every shift.", font=sans(44, 400), fill=MUTED_ON_NAVY)
brand_lockup(hero, tx, 1300, 90, dark=True)
hero.convert("RGB").save(OUT + "listing-01-hero.png")

# ---------- 3b. close-up ----------
cu = Image.new("RGBA", (LW, LH), CREAM + (255,)); d = ImageDraw.Draw(cu)
crop = sheetA4.crop((0, 0, sheetA4.width, int(sheetA4.width * 0.62)))
cw = 1760; ch = int(crop.height * cw / crop.width)
crop = crop.resize((cw, ch), Image.LANCZOS)
top = LH - ch - 60
bar_h = top - 50
d.rectangle((0, 0, LW, bar_h), fill=NAVY)
paste_shadow(cu, crop, (120, top), blur=22, off=(0, 18), alpha=80)
tracked(d, (120, 70), "CLOSE-UP", sans(30, 600), GOLD, 10)
head = "Every handover detail, captured in minutes."
fh = fit(d, head, lambda s: serif(s, 600), 1760, 72)
d.text((120, 125), head, font=fh, fill=CREAM)
cu.convert("RGB").save(OUT + "listing-02-closeup.png")

# ---------- 3c. what you get ----------
wg = Image.new("RGBA", (LW, LH), CREAM + (255,)); d = ImageDraw.Draw(wg)
tracked(d, (LW / 2, 95), "INCLUDED IN YOUR DOWNLOAD", sans(30, 600), TEAL, 10, anchor="m")
d.text((LW / 2, 215), "What you get", font=serif(104, 600), fill=NAVY, anchor="mm")
d.line((LW / 2 - 80, 300, LW / 2 + 80, 300), fill=GOLD, width=5)
th = 700
for img, x, lab in [(sheetA4, 90, "A4 PDF"), (sheetL, 630, "US Letter PDF")]:
    s = img.resize((int(img.width * th / img.height), th), Image.LANCZOS)
    paste_shadow(wg, s, (x, 380), blur=18, off=(10, 18), alpha=70)
    c = x + s.width // 2
    d.rounded_rectangle((c - 180, 1140, c + 180, 1220), 8, fill=NAVY)
    d.text((c, 1180), lab, font=sans(40, 600), fill=CREAM, anchor="mm")
items = [("2 print-ready PDFs", "A4 and US Letter, 1 page each"),
         ("Instant download", "Available right after purchase"),
         ("Print at home or work", "Any standard printer, colour or B&W"),
         ("Reusable every shift", "Print as many as your team needs")]
ix, iy = 1220, 400
for t, s in items:
    d.ellipse((ix, iy, ix + 80, iy + 80), fill=TEAL)
    d.line((ix + 21, iy + 42, ix + 35, iy + 57, ix + 60, iy + 27), fill=CREAM, width=9, joint="curve")
    ft = fit(d, t, lambda z: serif(z, 600), 660, 52); fs = fit(d, s, lambda z: sans(z, 400), 660, 36)
    d.text((ix + 112, iy - 4), t, font=ft, fill=NAVY)
    d.text((ix + 112, iy + 70), s, font=fs, fill=INK_MUTED)
    iy += 205
d.line((90, 1340, LW - 90, 1340), fill=HAIR, width=2)
brand_lockup(wg, LW - 90, 1375, 64, dark=False, anchor="r")
wg.convert("RGB").save(OUT + "listing-03-what-you-get.png")

# ---------- 3d. how it works ----------
hw = vgrad(LW, LH, NAVY, NAVY2).convert("RGBA"); d = ImageDraw.Draw(hw)
tracked(d, (LW / 2, 140), "FOUR SIMPLE STEPS", sans(30, 600), GOLD, 10, anchor="m")
d.text((LW / 2, 265), "How it works", font=serif(110, 600), fill=CREAM, anchor="mm")
d.line((LW / 2 - 80, 360, LW / 2 + 80, 360), fill=GOLD, width=5)
steps = [("Buy", "Check out on Etsy"), ("Download", "A4 & Letter PDFs"),
         ("Print", "At home or at work"), ("Use", "Every shift change")]
colw = 440; x0 = (LW - colw * 4) // 2; cy = 730
d.line((x0 + colw / 2, cy, x0 + colw * 3.5, cy), fill=hx("#2E4457"), width=4)
for i, (t, s) in enumerate(steps):
    c = x0 + colw * i + colw / 2
    d.ellipse((c - 125, cy - 125, c + 125, cy + 125), fill=NAVY, outline=GOLD, width=6)
    d.text((c, cy - 8), str(i + 1), font=serif(150, 600), fill=GOLD, anchor="mm")
    ft = fit(d, t, lambda z: serif(z, 600), colw - 40, 68)
    d.text((c, cy + 235), t, font=ft, fill=CREAM, anchor="mm")
    fs = fit(d, s, lambda z: sans(z, 400), colw - 40, 40)
    d.text((c, cy + 320), s, font=fs, fill=MUTED_ON_NAVY, anchor="mm")
d.text((LW / 2, 1250), "Instant digital download · No physical item shipped", font=sans(38, 400), fill=MUTED_ON_NAVY, anchor="mm")
brand_lockup(hw, LW / 2, 1340, 70, dark=True, anchor="m")
hw.convert("RGB").save(OUT + "listing-04-how-it-works.png")
print("done")
