"""Build the Weekly Team Check-in print-and-write PDFs (A4 and US Letter).

Run from anywhere:  python3 products/weekly-team-check-in/src/make_pdf.py
Needs: reportlab, fontTools, Pillow (pip install reportlab fonttools pillow).

Self-contained: every path is relative to the repo root.
- Fonts: assets/fonts/ (Google Fonts variable fonts, SIL OFL 1.1, licence text next to each font).
  Static weights are instanced into a temporary folder at build time and only subsets are
  embedded in the PDFs. The vendored font files themselves are left unmodified.
- Logo: assets/brand/lbd-mark-reversed-cream.png (Leadership by Design L|BD mark, cream for dark bars).

Forked from products/feedback-conversation-log/src/make_pdf.py (same Sheet helpers, colours and
spacing) and laid out to the build-ready spec in logs/2026-10-06.md section 1, which applies the
five fixes in logs/critique-weekly-team-check-in-2026-09-29.md to the Day 3 brief in
logs/2026-09-29.md.

Page 1 is the 15-minute huddle sheet (header fields, Last week, Wins, Round-robin, Decisions,
Actions, Stop doing, Next check-in). Page 2 is the monthly team pulse (5 statements tallied 1 to 5,
check-ins this month, one change).

Rules (asserted): 12 mm margins (every filled shape and image stays inside them, so there are
no full-bleed fills), every write-in line and table row at least 8 mm tall, every label fits
its cell, nothing runs past the footer. The script prints the row heights per page.
"""
import tempfile
from collections import OrderedDict
from pathlib import Path

from fontTools.ttLib import TTFont as FTFont
from fontTools.varLib import instancer
from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[3]
FONTS = ROOT / "assets" / "fonts"
MARK = ROOT / "assets" / "brand" / "lbd-mark-reversed-cream.png"
OUT = ROOT / "products" / "weekly-team-check-in"

PLAYFAIR = FONTS / "playfair-display" / "PlayfairDisplay[wght].ttf"
SOURCE = FONTS / "source-sans-3" / "SourceSans3[wght].ttf"

# alias -> (variable font, weight)
WEIGHTS = {
    "P": (SOURCE, 400),     # body
    "PM": (SOURCE, 600),    # field labels
    "PB": (SOURCE, 700),    # numbers
    "SH": (PLAYFAIR, 600),  # section headings
    "ST": (PLAYFAIR, 700),  # title
}


def register_fonts():
    tmp = Path(tempfile.mkdtemp(prefix="lbd-fonts-"))
    for alias, (src, wght) in WEIGHTS.items():
        vf = FTFont(str(src))
        try:
            inst = instancer.instantiateVariableFont(vf, {"wght": wght}, updateFontNames=True)
        except Exception:
            inst = instancer.instantiateVariableFont(vf, {"wght": wght})
        path = tmp / f"{alias}.ttf"
        inst.save(str(path))
        pdfmetrics.registerFont(TTFont(alias, str(path)))


NAVY = HexColor("#0F1F2E")
TEAL = HexColor("#2A7B88")
GOLD = HexColor("#C8A864")
CREAM = HexColor("#F8F6F1")
GREY = HexColor("#5F6A73")   # navy at 65% on white
LINE = HexColor("#B7BEC4")   # navy-tinted rule, visible when printed

M = 12 * mm          # margins, all sides
GAP = 4 * mm         # gutter between side-by-side fields
VGAP = 2.2 * mm      # gap between stacked boxes
PAD = 1.0 * mm       # space under the last write-in line inside a box
LBL = 38 * mm        # left label column on page 1
MIN_ROW = 8 * mm     # handwriting rule
MAX_ROW = 9.5 * mm   # do not stretch rows beyond this on page 1
BAR = 13 * mm        # navy header bar
FOOTER = "Designed by Kevin Britz / Leadership by Design  \u00b7  leadershipbydesign.co  \u00b7  For use within one workplace"


class MarginCanvas(canvas.Canvas):
    """Canvas that asserts every filled or stroked rectangle and every image sits inside the
    12 mm margins. That is the no-full-bleed-fills rule, checked on every shape drawn."""

    def _inside(self, x, y, w, h, what):
        W, H = self._pagesize
        x0, x1 = min(x, x + w), max(x, x + w)
        y0, y1 = min(y, y + h), max(y, y + h)
        e = 0.01
        assert x0 >= M - e and x1 <= W - M + e and y0 >= M - e and y1 <= H - M + e, (
            f"{what} at ({x0 / mm:.1f}, {y0 / mm:.1f})-({x1 / mm:.1f}, {y1 / mm:.1f}) mm "
            f"crosses the 12 mm margin")

    def rect(self, x, y, width, height, stroke=1, fill=0):
        self._inside(x, y, width, height, "rect")
        return super().rect(x, y, width, height, stroke=stroke, fill=fill)

    def roundRect(self, x, y, width, height, radius, stroke=1, fill=0):
        self._inside(x, y, width, height, "roundRect")
        return super().roundRect(x, y, width, height, radius, stroke=stroke, fill=fill)

    def drawImage(self, image, x, y, width=None, height=None, **kw):
        self._inside(x, y, width, height, "image")
        return super().drawImage(image, x, y, width, height, **kw)


class Sheet:
    def __init__(self, c, W, H):
        self.c, self.W, self.H = c, W, H
        self.CW = W - 2 * M
        self.rows = []          # every write-in row / table row height drawn, for the report

    # ---------- checks ----------
    def fits(self, text, font, size, maxw, what=""):
        w = self.c.stringWidth(text, font, size)
        assert w <= maxw + 0.01, f"'{text}' {what} is {w / mm:.1f} mm wide, room {maxw / mm:.1f} mm"

    def row(self, h, what):
        assert h >= MIN_ROW - 1e-6, f"{what}: row {h / mm:.2f} mm < 8 mm"
        self.rows.append((what, h))

    # ---------- primitives ----------
    def header_bar(self, title, tagline):
        c, CW = self.c, self.CW
        bh = BAR
        top = self.H - M
        c.setFillColor(NAVY); c.roundRect(M, top - bh, CW, bh, 2 * mm, stroke=0, fill=1)
        c.setFillColor(GOLD); c.rect(M, top - bh, 3 * mm, bh, stroke=0, fill=1)
        c.setFillColor(CREAM); c.setFont("ST", 16.5)
        c.drawString(M + 8 * mm, top - bh + 4.4 * mm, title)
        mh = 8 * mm
        im = Image.open(MARK); mw = mh * im.width / im.height
        mx = M + CW - 5 * mm - mw
        c.drawImage(str(MARK), mx, top - bh + (bh - mh) / 2, mw, mh, mask="auto")
        dx = mx - 3.5 * mm
        c.setStrokeColor(GOLD); c.setLineWidth(0.6)
        c.line(dx, top - bh + 3.0 * mm, dx, top - 3.0 * mm)
        c.setFont("PM", 9); c.setFillColor(GOLD)
        c.drawRightString(dx - 3.5 * mm, top - bh + 7.3 * mm, "Leadership by Design")
        c.setFont("P", 7.5); c.setFillColor(CREAM)
        c.drawRightString(dx - 3.5 * mm, top - bh + 3.5 * mm, tagline)
        tw = c.stringWidth(title, "ST", 16.5)
        right_w = max(c.stringWidth("Leadership by Design", "PM", 9), c.stringWidth(tagline, "P", 7.5))
        assert M + 8 * mm + tw + 6 * mm < dx - 3.5 * mm - right_w, "header bar text collides"
        # thin gold underline
        c.setFillColor(GOLD); c.rect(M, top - bh - 1.2 * mm, CW, 0.5 * mm, stroke=0, fill=1)
        return top - bh - 1.2 * mm

    def rule(self, x0, x1, y, width=0.6):
        self.c.setStrokeColor(LINE); self.c.setLineWidth(width)
        self.c.line(x0, y, x1, y)

    def label_line(self, x, y, w, label, size=8.5):
        """Label sitting on a write-in rule at baseline y; rule runs to x + w."""
        c = self.c
        lw = c.stringWidth(label, "PM", size) + 1.8 * mm
        assert w - lw >= 12 * mm, f"no write-in room after '{label}'"
        c.setFont("PM", size); c.setFillColor(NAVY)
        c.drawString(x, y + 1.0 * mm, label)
        self.rule(x + lw, x + w, y)

    def tick(self, x, y, label=None, size=8.5, s=3.4 * mm):
        """Tick box with its bottom at y, optional label after it. Returns x after the label."""
        c = self.c
        c.setStrokeColor(TEAL); c.setLineWidth(0.9); c.setFillColor(white)
        c.rect(x, y, s, s, stroke=1, fill=1)
        x += s + 1.3 * mm
        if label:
            c.setFont("P", size); c.setFillColor(NAVY)
            c.drawString(x, y + 0.6 * mm, label)
            x += c.stringWidth(label, "P", size)
        return x

    def labelled_box(self, ytop, h, title, prompt=None, accent=None):
        """Full-width outlined box with a left label column. Returns (x0, x1) of the writing area."""
        c, CW = self.c, self.CW
        c.setStrokeColor(LINE); c.setLineWidth(0.7)
        c.roundRect(M, ytop - h, CW, h, 1.5 * mm, stroke=1, fill=0)
        xs = M + LBL
        c.line(xs, ytop - h, xs, ytop)
        if accent is not None:   # accent left rule, clipped to the rounded box
            c.saveState()
            p = c.beginPath(); p.roundRect(M, ytop - h, CW, h, 1.5 * mm)
            c.clipPath(p, stroke=0, fill=0)
            c.setFillColor(accent); c.rect(M, ytop - h, 1.6 * mm, h, stroke=0, fill=1)
            c.restoreState()
            c.setStrokeColor(LINE); c.setLineWidth(0.7)
            c.roundRect(M, ytop - h, CW, h, 1.5 * mm, stroke=1, fill=0)
        tx = M + 3.4 * mm
        tw = LBL - 3.4 * mm - 2.2 * mm
        y = ytop - 4.6 * mm
        last = y
        c.setFillColor(TEAL); c.setFont("SH", 10)
        for line in simpleSplit(title, "SH", 10, tw):
            c.drawString(tx, y, line); last = y; y -= 4.2 * mm
        if prompt:
            y += 0.9 * mm
            c.setFillColor(GREY); c.setFont("P", 7)
            for line in simpleSplit(prompt, "P", 7, tw):
                c.drawString(tx, y, line); last = y; y -= 2.9 * mm
        # last baseline plus descenders must stay 1.2 mm clear of the box bottom
        assert last - 2.4 * mm >= ytop - h, f"label column for '{title}' overflows its box"
        return xs, M + CW

    def table(self, x0, x1, ytop, hdr, cols, fracs, n, S, what, sub=None):
        """Grid table in [x0, x1]: cream header row (column name, optional sub-line), n rows of S.
        The outer border is the enclosing box. Returns the column x positions."""
        c = self.c
        w = x1 - x0
        xs = [x0]
        for f in fracs:
            xs.append(xs[-1] + w * f)
        assert abs(xs[-1] - x1) < 0.01, "column fractions must sum to 1"
        # cream header, clipped to the box so it never pokes past the rounded corner
        c.saveState()
        p = c.beginPath(); p.roundRect(M, ytop - hdr - n * S, self.CW, hdr + n * S, 1.5 * mm)
        c.clipPath(p, stroke=0, fill=0)
        c.setFillColor(CREAM); c.rect(x0, ytop - hdr, w, hdr, stroke=0, fill=1)
        c.restoreState()
        for i, col in enumerate(cols):
            cw = xs[i + 1] - xs[i] - 3.0 * mm
            self.fits(col, "PM", 8.5, cw, f"header in {what}")
            c.setFont("PM", 8.5); c.setFillColor(NAVY)
            base = ytop - hdr + (4.6 * mm if sub else 1.9 * mm)
            c.drawString(xs[i] + 1.6 * mm, base, col)
            if sub and sub[i]:
                if callable(sub[i]):
                    sub[i](xs[i] + 1.6 * mm, ytop - hdr + 1.5 * mm, cw)
                else:
                    self.fits(sub[i], "P", 7, cw, f"sub-header in {what}")
                    c.setFont("P", 7); c.setFillColor(GREY)
                    c.drawString(xs[i] + 1.6 * mm, ytop - hdr + 1.5 * mm, sub[i])
        c.setStrokeColor(LINE); c.setLineWidth(0.5)
        for r in range(n):
            yy = ytop - hdr - r * S
            c.line(x0, yy, x1, yy)
            self.row(S, f"{what} row {r + 1}")
        for xx in xs[1:-1]:
            c.line(xx, ytop - hdr - n * S, xx, ytop)
        return xs

    def footer(self, note=None):
        c = self.c
        if note:
            c.setFont("PM", 8); c.setFillColor(TEAL)
            self.fits(note, "PM", 8, self.CW, "footer note")
            c.drawCentredString(self.W / 2, M + 6.4 * mm, note)
        c.setFillColor(GOLD); c.rect(self.W / 2 - 10 * mm, M + 4.0 * mm, 20 * mm, 0.6 * mm, stroke=0, fill=1)
        c.setFont("P", 7.2); c.setFillColor(GREY)
        self.fits("\u00a9 " + FOOTER, "P", 7.2, self.CW, "brand line")
        c.drawCentredString(self.W / 2, M + 0.8 * mm, "\u00a9 " + FOOTER)


def grid(sh, top, cols, fracs, subs, n, S, what, hdr=8.6 * mm):
    """Full-width grid (page-2-index style): cream header with optional grey sub-line, n rows of S,
    outer border and column rules. Returns (column x positions, bottom y)."""
    c, CW = sh.c, sh.CW
    xs = [M]
    for f in fracs:
        xs.append(xs[-1] + CW * f)
    assert abs(xs[-1] - (M + CW)) < 0.01, f"{what}: column fractions must sum to 1"
    c.setFillColor(CREAM); c.rect(M, top - hdr, CW, hdr, stroke=0, fill=1)
    for i, col in enumerate(cols):
        cw = xs[i + 1] - xs[i] - 2.4 * mm
        sh.fits(col, "PM", 8.5, cw, f"header in {what}")
        c.setFont("PM", 8.5); c.setFillColor(NAVY)
        c.drawString(xs[i] + 1.4 * mm, top - hdr + (4.6 * mm if subs[i] else 3.0 * mm), col)
        if subs[i]:
            sh.fits(subs[i], "P", 7, cw, f"sub-header in {what}")
            c.setFont("P", 7); c.setFillColor(GREY)
            c.drawString(xs[i] + 1.4 * mm, top - hdr + 1.5 * mm, subs[i])
    bot = top - hdr - n * S
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.rect(M, bot, CW, top - bot, stroke=1, fill=0)
    for r in range(n):
        c.line(M, top - hdr - r * S, M + CW, top - hdr - r * S)
        sh.row(S, f"{what} row {r + 1}")
    for xx in xs[1:-1]:
        c.line(xx, bot, xx, top)
    return xs, bot


# ---------------------------------------------------------------- page 1
def page_one(sh):
    c, CW = sh.c, sh.CW
    y = sh.header_bar("WEEKLY TEAM CHECK-IN", "15 minutes, every week.")
    FOOT = M + 10.5 * mm            # teal note + brand line

    # Page-height budget (logs/2026-10-06.md section 1). Rows are the only thing that flexes.
    HEAD_C = 7.0 * mm               # Round-robin heading line
    HDR_C = 8.6 * mm                # Round-robin grid header (with sub-line)
    HDR_E = 6.0 * mm                # Actions table header
    ROWS = OrderedDict((("header fields", 1), ("A Last week", 1), ("B Wins", 3),
                        ("C Round-robin", 8), ("D Decisions", 2), ("E Actions", 5),
                        ("F Stop doing", 1), ("G Next check-in", 1)))
    n_rows = sum(ROWS.values())     # 22
    assert n_rows == 22
    n_gaps = len(ROWS) - 1          # 7
    n_pad = 5                       # boxes A, B, D, F, G
    fixed = n_gaps * VGAP + n_pad * PAD + HEAD_C + HDR_C + HDR_E
    avail = y - FOOT
    S = min(MAX_ROW, (avail - fixed) / n_rows)
    assert S >= MIN_ROW, f"page 1 row height {S / mm:.2f} mm < 8 mm (avail {avail / mm:.1f} mm)"

    # Header fields: one row of four
    w = CW - 3 * GAP
    x = M
    for lab, f in (("Team", 0.28), ("Site / area", 0.26), ("Facilitator", 0.26), ("Week of", 0.20)):
        sh.label_line(x, y - S, w * f, lab); x += w * f + GAP
    sh.row(S, "header row")
    y -= S + VGAP

    def one_line_box(y, title, fields, what, accent=None):
        h = S + PAD
        x0, x1 = sh.labelled_box(y, h, title, None, accent=accent)
        iw = x1 - x0 - 6 * mm
        xa = x0 + 3 * mm
        ww = iw - (len(fields) - 1) * GAP
        for lab, f in fields:
            sh.label_line(xa, y - S, ww * f, lab); xa += ww * f + GAP
        sh.row(S, f"{what} line 1")
        return y - h - VGAP

    # Box A: Last week (critique fix 4: link back to last week's actions)
    y = one_line_box(y, "Last week", (("Actions closed:", 0.28), ("Carried over:", 0.28),
                                       ("Needs escalating:", 0.44)), "A Last week")

    # Box B: Wins this week, numbered 1 to 3
    n = ROWS["B Wins"]
    h = n * S + PAD
    x0, x1 = sh.labelled_box(y, h, "Wins this week", "2 min. Name three things that went well.")
    for k in range(n):
        yy = y - (k + 1) * S
        c.setFont("PB", 9); c.setFillColor(TEAL); c.drawString(x0 + 3 * mm, yy + 1.0 * mm, str(k + 1))
        sh.rule(x0 + 8 * mm, x1 - 3 * mm, yy)
        sh.row(S, f"B Wins line {k + 1}")
    y -= h + VGAP

    # Block C: Round-robin grid, full width (critique fixes 1 and 3)
    c.setFont("SH", 10); c.setFillColor(TEAL)
    c.drawString(M, y - 4.6 * mm, "Round-robin")
    xp = M + c.stringWidth("Round-robin", "SH", 10) + 3 * mm
    prompt = "6 min. One turn each, under a minute."
    c.setFont("P", 7.5); c.setFillColor(GREY); c.drawString(xp, y - 4.6 * mm, prompt)
    legend = "Energy: 1 = running on empty, 5 = fully energised"
    lw = c.stringWidth(legend, "PM", 8)
    gap_c = (M + CW - lw) - (xp + c.stringWidth(prompt, "P", 7.5))
    assert gap_c >= 6 * mm, f"round-robin heading collides (gap {gap_c / mm:.1f} mm)"
    c.setFont("PM", 8); c.setFillColor(NAVY); c.drawRightString(M + CW, y - 4.6 * mm, legend)
    y -= HEAD_C
    n = ROWS["C Round-robin"]
    xs, bot = grid(sh, y, ("Name", "Energy", "Top priority this week", "Blocker"),
                   (0.20, 0.17, 0.33, 0.30), ("", "circle one", "", "and help needed from"),
                   n, S, "C Round-robin", hdr=HDR_C)
    colw = xs[2] - xs[1]
    pitch = min(6 * mm, (colw - 6 * mm) / 4)
    assert pitch >= 5 * mm, "energy digits too close to circle"
    cx0 = (xs[1] + xs[2]) / 2 - 2 * pitch
    for r in range(n):
        mid = y - HDR_C - r * S - S / 2
        c.setFont("PM", 9); c.setFillColor(GREY)
        for k in range(5):
            c.drawCentredString(cx0 + k * pitch, mid - 1.1 * mm, str(k + 1))
    y = bot - VGAP

    # Box D: Decisions made (2 lines; page budget, see log)
    n = ROWS["D Decisions"]
    h = n * S + PAD
    x0, x1 = sh.labelled_box(y, h, "Decisions made", "2 min. What we decided, and who needs to know.")
    for k in range(n):
        sh.rule(x0 + 3 * mm, x1 - 3 * mm, y - (k + 1) * S)
        sh.row(S, f"D Decisions line {k + 1}")
    y -= h + VGAP

    # Box E: Actions (critique fix 4: Done column)
    n = ROWS["E Actions"]
    h = HDR_E + n * S
    x0, x1 = sh.labelled_box(y, h, "Actions", "3 min. One owner each. Read them back. Not done? Carry it to next week.")
    xs = sh.table(x0, x1, y, HDR_E, ("Owner", "Action", "Due", "Done"),
                  (0.24, 0.46, 0.16, 0.14), n, S, "E Actions")
    tb = 3.4 * mm
    assert xs[4] - xs[3] >= tb + 2 * mm, "Done column too narrow for its tick box"
    for r in range(n):
        yb = y - HDR_E - (r + 1) * S + (S - tb) / 2
        sh.tick((xs[3] + xs[4]) / 2 - tb / 2, yb)
    y -= h + VGAP

    # Box F: Stop doing (gold accent)
    y = one_line_box(y, "Stop doing", (("One habit or task we will drop this week:", 1.0),),
                     "F Stop doing", accent=GOLD)
    # Box G: Next check-in (critique fix 5)
    y = one_line_box(y, "Next check-in", (("Date", 0.32), ("Time", 0.24), ("Where", 0.44)),
                     "G Next check-in")
    y += VGAP                       # no gap after the last block

    assert y >= FOOT - 0.01, f"page 1 overflows by {(FOOT - y) / mm:.2f} mm"
    sh.footer("15 minutes. Stand if you can. Everyone speaks once.")
    return S, (y - FOOT)


# ---------------------------------------------------------------- page 2
def page_two(sh):
    c, CW = sh.c, sh.CW
    y = sh.header_bar("MONTHLY TEAM PULSE", "Last check-in of the month.")
    FOOT = M + 10.5 * mm
    c.setFont("ST", 15); c.setFillColor(NAVY)
    c.drawString(M, y - 8.0 * mm, "How is the team doing?")
    sub = "Run it at the end of the last check-in of the month. Everyone scores each line from 1 to 5."
    sh.fits(sub, "P", 9, CW, "page 2 intro")
    c.setFont("P", 9); c.setFillColor(GREY)
    c.drawString(M, y - 12.6 * mm, sub)
    y -= 14.5 * mm
    S0 = 9 * mm
    w = CW - 2 * GAP
    x = M
    for lab, f in (("Team", 0.38), ("Month", 0.30), ("Facilitator", 0.32)):
        sh.label_line(x, y - S0, w * f, lab); x += w * f + GAP
    sh.row(S0, "p2 header fields")
    y -= S0 + 4 * mm

    legend = "1 = strongly disagree, 5 = strongly agree. One tally mark per person, then write the average."
    sh.fits(legend, "P", 8, CW, "pulse legend")
    c.setFont("P", 8); c.setFillColor(NAVY)
    c.drawString(M, y - 4.4 * mm, legend)
    y -= 6.5 * mm

    statements = ("I know what is expected of me this week.",
                  "I can get help when I am stuck.",
                  "We deal with problems early.",
                  "Wins are noticed, not only mistakes.",
                  "I would recommend this team as a place to work.")
    HDR = 8.6 * mm
    S2 = 9.0 * mm                   # rows in the two boxes below the pulse
    HDR_M = 6.0 * mm
    box_m = HDR_M + 5 * S2          # Check-ins this month
    box_c = 3 * S2 + PAD            # One change
    box_h = 2 * S2 + PAD            # What we heard
    R = (y - FOOT - HDR - 4 * mm - box_h - VGAP - box_m - VGAP - box_c) / len(statements)
    assert R >= 12 * mm, f"pulse row {R / mm:.2f} mm < 12 mm"
    cols = ("#", "Statement", "1", "2", "3", "4", "5", "Average", "Last month")
    subs = ("", "", "tally", "tally", "tally", "tally", "tally", "this month", "average")
    fr = (0.05, 0.40, 0.07, 0.07, 0.07, 0.07, 0.07, 0.10, 0.10)
    top = y
    xs, bot = grid(sh, top, cols, fr, subs, len(statements), R, "p2 pulse", hdr=HDR)
    for r, st in enumerate(statements):
        mid = top - HDR - r * R - R / 2
        c.setFont("PB", 9); c.setFillColor(TEAL)
        c.drawCentredString((xs[0] + xs[1]) / 2, mid - 1.2 * mm, str(r + 1))
        lines = simpleSplit(st, "P", 9.5, xs[2] - xs[1] - 3 * mm)
        assert len(lines) <= 2, f"statement {r + 1} wraps to {len(lines)} lines"
        c.setFont("P", 9.5); c.setFillColor(NAVY)
        y0 = mid - 1.2 * mm + (len(lines) - 1) * 2.0 * mm
        for k, ln in enumerate(lines):
            c.drawString(xs[1] + 1.6 * mm, y0 - k * 4.0 * mm, ln)
    y = bot - 4 * mm

    # What we heard
    x0, x1 = sh.labelled_box(y, box_h, "What we heard", "Two or three comments. No names.")
    for k in range(2):
        sh.rule(x0 + 3 * mm, x1 - 3 * mm, y - (k + 1) * S2)
        sh.row(S2, f"p2 what we heard line {k + 1}")
    y -= box_h + VGAP

    # Check-ins this month
    x0, x1 = sh.labelled_box(y, box_m, "Check-ins this month", "One line per weekly sheet.")
    sh.table(x0, x1, y, HDR_M, ("Week of", "Present", "Closed", "Carried", "We stopped doing"),
             (0.20, 0.15, 0.15, 0.15, 0.35), 5, S2, "p2 check-ins")
    y -= box_m + VGAP

    # One change
    x0, x1 = sh.labelled_box(y, box_c, "One change", "Pick the lowest line. Agree one change.")
    iw = x1 - x0 - 6 * mm
    xa = x0 + 3 * mm
    sh.label_line(xa, y - S2, iw * 0.30, "Lowest line #")
    sh.label_line(xa + iw * 0.30 + GAP, y - S2, iw * 0.70 - GAP, "What gets in the way:")
    sh.row(S2, "p2 one change line 1")
    sh.label_line(xa, y - 2 * S2, iw, "One thing we will change next month:")
    sh.row(S2, "p2 one change line 2")
    sh.label_line(xa, y - 3 * S2, iw * 0.45, "Owner")
    sh.label_line(xa + iw * 0.45 + GAP, y - 3 * S2, iw * 0.55 - GAP, "Check it on")
    sh.row(S2, "p2 one change line 3")
    y -= box_c

    assert y >= FOOT - 0.01, f"page 2 overflows by {(FOOT - y) / mm:.2f} mm"
    sh.footer("A team conversation tool, not an employee rating form. Talk about the line, not the person.")
    return R, (y - FOOT)


def build(pagesize, fname):
    W, H = pagesize
    c = MarginCanvas(str(OUT / fname), pagesize=pagesize, initialFontName="P")
    c.setTitle("Weekly Team Check-in"); c.setAuthor("Kevin Britz / Leadership by Design")
    c.setSubject("Printable weekly team huddle sheet and monthly team pulse for managers")
    sh = Sheet(c, W, H)
    s1, spare1 = page_one(sh); n1 = len(sh.rows); c.showPage()
    s2, spare2 = page_two(sh); c.showPage()
    c.save()
    low = min(h for _, h in sh.rows)
    assert low >= MIN_ROW - 1e-6
    p1 = [h for _, h in sh.rows[:n1]]
    print(f"{fname}: page 1 {len(p1)} write-in rows at {s1 / mm:.2f} mm (spare {abs(spare1) / mm:.1f} mm); "
          f"page 2 pulse rows {s2 / mm:.2f} mm (spare {abs(spare2) / mm:.1f} mm); "
          f"{len(sh.rows)} rows checked, smallest {low / mm:.2f} mm, margins {M / mm:.0f} mm")


if __name__ == "__main__":
    register_fonts()
    build(A4, "weekly-team-check-in-A4.pdf")
    build(letter, "weekly-team-check-in-Letter.pdf")
