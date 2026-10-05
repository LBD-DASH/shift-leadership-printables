"""Build the Feedback Conversation Log print-and-write PDFs (A4 and US Letter).

Run from anywhere:  python3 products/feedback-conversation-log/src/make_pdf.py
Needs: reportlab, fontTools, Pillow (pip install reportlab fonttools pillow).

Self-contained: every path is relative to the repo root.
- Fonts: assets/fonts/ (Google Fonts variable fonts, SIL OFL 1.1, licence text next to each font).
  Static weights are instanced into a temporary folder at build time and only subsets are
  embedded in the PDFs. The vendored font files themselves are left unmodified.
- Logo: assets/brand/lbd-mark-reversed-cream.png (Leadership by Design L|BD mark, cream for dark bars).

Forked from products/shift-incident-log/src/make_pdf.py (same Sheet helpers, colours and
spacing) and laid out to the build-ready spec in logs/2026-10-05.md section 1, which supersedes
the outline in logs/2026-10-04.md section 2.

Page 1 is one conversation (header fields, Before you talk, Situation, Behaviour, Impact,
Their view, What we agreed, Follow-up). Page 2 is a monthly index with 15 rows, a type key and
a month-end count callout.

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
OUT = ROOT / "products" / "feedback-conversation-log"

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


# ---------------------------------------------------------------- page 1
def page_one(sh):
    c, CW = sh.c, sh.CW
    y = sh.header_bar("FEEDBACK CONVERSATION LOG", "One conversation per sheet. Facts first.")
    FOOT = M + 10.5 * mm            # teal note + brand line

    # Page-height budget (logs/2026-10-05.md section 1). Rows are the only thing that flexes.
    HDR_G = 6.0 * mm                # What we agreed table header
    ROWS = OrderedDict((("header fields", 2), ("A Before you talk", 2), ("C Situation", 3),
                        ("D Behaviour", 3), ("E Impact", 2), ("F Their view", 3),
                        ("G What we agreed", 4), ("H Follow-up", 2)))
    n_rows = sum(ROWS.values())     # 21
    assert n_rows == 21
    n_gaps = len(ROWS) - 1          # gap after every block except the last: 7
    n_pad = 6                       # boxes A, C, D, E, F, H
    fixed = n_gaps * VGAP + n_pad * PAD + HDR_G
    avail = y - FOOT
    S = min(MAX_ROW, (avail - fixed) / n_rows)
    assert S >= MIN_ROW, f"page 1 row height {S / mm:.2f} mm < 8 mm (avail {avail / mm:.1f} mm)"

    # Header fields: two rows, columns aligned 0.45 | 0.32 | 0.23
    w = CW - 2 * GAP
    for r, fields in enumerate(((("Team member", 0.45), ("Role", 0.32), ("Date", 0.23)),
                                (("Manager", 0.45), ("Team / shift", 0.32), ("Time", 0.23)))):
        x = M
        for lab, f in fields:
            sh.label_line(x, y - (r + 1) * S, w * f, lab); x += w * f + GAP
        sh.row(S, f"header row {r + 1}")
    y -= 2 * S + VGAP

    # Box A: Before you talk (one point + Type ticks)
    h = ROWS["A Before you talk"] * S + PAD
    x0, x1 = sh.labelled_box(y, h, "Before you talk",
                             "Pick the type and the one point before you start.")
    xa = x0 + 3 * mm
    sh.label_line(xa, y - S, x1 - x0 - 6 * mm, "The one thing I want them to keep doing or change:")
    sh.row(S, "A Before you talk line 1")
    yy = y - 2 * S
    c.setFont("PM", 8.5); c.setFillColor(NAVY); c.drawString(xa, yy + 1.0 * mm, "Type:")
    xx = xa + c.stringWidth("Type:", "PM", 8.5) + 2.5 * mm
    labels = ("Praise: keep doing it", "Corrective: change it", "Coaching: grow it")
    for k, lab in enumerate(labels):
        xx = sh.tick(xx, yy + 0.8 * mm, lab)
        if k < len(labels) - 1:
            xx += 5 * mm
    assert xx <= x1 - 3 * mm, f"Type ticks run {(xx - (x1 - 3 * mm)) / mm:.1f} mm past the box"
    type_spare = x1 - 3 * mm - xx
    sh.row(S, "A Before you talk line 2")
    y -= h + VGAP

    def lined_box(y, n, title, prompt, what):
        h = n * S + PAD
        x0, x1 = sh.labelled_box(y, h, title, prompt)
        for k in range(n):
            sh.rule(x0 + 3 * mm, x1 - 3 * mm, y - (k + 1) * S)
            sh.row(S, f"{what} line {k + 1}")
        return y - h - VGAP

    y = lined_box(y, ROWS["C Situation"], "Situation",
                  "When and where. Facts only, no judgement words.", "C Situation")
    y = lined_box(y, ROWS["D Behaviour"], "Behaviour",
                  "What they did or said that you saw or heard yourself.", "D Behaviour")
    y = lined_box(y, ROWS["E Impact"], "Impact",
                  "On the team, the customer, the work or safety.", "E Impact")
    y = lined_box(y, ROWS["F Their view"], "Their view",
                  "Ask: How do you see it? Note their words, briefly.", "F Their view")

    # Box G: What we agreed
    n = ROWS["G What we agreed"]
    h = HDR_G + n * S
    x0, x1 = sh.labelled_box(y, h, "What we agreed",
                             "Small, specific steps. Both of you know who does what.")
    xs = sh.table(x0, x1, y, HDR_G, ("Action", "Who", "By when", "Done"),
                  (0.55, 0.19, 0.16, 0.10), n, S, "G What we agreed")
    tb = 3.4 * mm
    assert xs[4] - xs[3] >= tb + 2 * mm, "Done column too narrow for its tick box"
    for r in range(n):
        yb = y - HDR_G - (r + 1) * S + (S - tb) / 2
        sh.tick((xs[3] + xs[4]) / 2 - tb / 2, yb)
    y -= h + VGAP

    # Box H: Follow-up
    h = ROWS["H Follow-up"] * S + PAD
    x0, x1 = sh.labelled_box(y, h, "Follow-up", "Check back. Say thank you if it changed.")
    iw = x1 - x0 - 6 * mm
    xa = x0 + 3 * mm
    yy = y - S
    sh.label_line(xa, yy, iw * 0.36, "Follow-up date")
    xr = xa + iw * 0.36 + GAP
    c.setFont("PM", 8.5); c.setFillColor(NAVY); c.drawString(xr, yy + 1.0 * mm, "Result:")
    xx = xr + c.stringWidth("Result:", "PM", 8.5) + 2.0 * mm
    res = ("Better", "Same", "Needs another talk")
    for k, lab in enumerate(res):
        xx = sh.tick(xx, yy + 0.8 * mm, lab)
        if k < len(res) - 1:
            xx += 3 * mm
    assert xx <= x1 - 3 * mm, "Result ticks run past the box"
    sh.row(S, "H Follow-up line 1")
    yy = y - 2 * S
    sh.label_line(xa, yy, iw * 0.36, "Manager initials")
    xt = xa + iw * 0.36 + GAP
    sh.label_line(xt, yy, xa + iw - xt, "Team member initials (optional)")
    sh.row(S, "H Follow-up line 2")
    y -= h

    assert y >= FOOT - 0.01, f"page 1 overflows by {(FOOT - y) / mm:.2f} mm"
    sh.footer("Log it the same day. Record what was seen and agreed, not opinions about the person.")
    return S, (y - FOOT), type_spare


# ---------------------------------------------------------------- page 2
def page_two(sh):
    c, CW = sh.c, sh.CW
    y = sh.header_bar("FEEDBACK LOG INDEX", "One line per conversation.")
    FOOT = M + 10.5 * mm
    c.setFont("ST", 15); c.setFillColor(NAVY)
    c.drawString(M, y - 8.0 * mm, "Conversations this month")
    sub = "Add a line after every conversation. Bring this page to your next 1:1 with your own manager."
    sh.fits(sub, "P", 9, CW, "page 2 intro")
    c.setFont("P", 9); c.setFillColor(GREY)
    c.drawString(M, y - 12.6 * mm, sub)
    y -= 14.5 * mm
    S0 = 9 * mm
    w = CW - 2 * GAP
    x = M
    for lab, f in (("Manager", 0.38), ("Team / shift", 0.36), ("Month", 0.26)):
        sh.label_line(x, y - S0, w * f, lab); x += w * f + GAP
    sh.row(S0, "p2 header fields")
    y -= S0 + 4 * mm

    HDR = 8.6 * mm
    KEY = 6.5 * mm
    CALL = 13 * mm
    rows = 15
    S = (y - FOOT - HDR - KEY - 3 * mm - CALL) / rows
    assert S >= MIN_ROW, f"page 2 row {S / mm:.2f} mm < 8 mm"
    cols = ("#", "Date", "Team member", "Type", "Topic (one line)", "Follow-up", "Done")
    subs = ("", "", "", "circle one", "", "date", "tick")
    fr = (0.05, 0.10, 0.20, 0.13, 0.32, 0.12, 0.08)
    xs = [M]
    for f in fr:
        xs.append(xs[-1] + CW * f)
    assert abs(xs[-1] - (M + CW)) < 0.01
    top = y
    c.setFillColor(CREAM); c.rect(M, top - HDR, CW, HDR, stroke=0, fill=1)
    for i, col in enumerate(cols):
        cw = xs[i + 1] - xs[i] - 2.4 * mm
        sh.fits(col, "PM", 8.5, cw, "index header")
        c.setFont("PM", 8.5); c.setFillColor(NAVY)
        c.drawString(xs[i] + 1.4 * mm, top - HDR + (4.6 * mm if subs[i] else 3.0 * mm), col)
        if subs[i]:
            sh.fits(subs[i], "P", 7, cw, "index sub-header")
            c.setFont("P", 7); c.setFillColor(GREY)
            c.drawString(xs[i] + 1.4 * mm, top - HDR + 1.5 * mm, subs[i])
    bot = top - HDR - rows * S
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.rect(M, bot, CW, top - bot, stroke=1, fill=0)
    opts = "P    C    CH"
    sh.fits(opts, "PM", 8.5, xs[4] - xs[3] - 2.8 * mm, "type options")
    tb = 3.4 * mm
    assert xs[7] - xs[6] >= tb + 2 * mm, "Done column too narrow for its tick box"
    for r in range(rows):
        yy = top - HDR - r * S
        c.setStrokeColor(LINE); c.setLineWidth(0.6)
        c.line(M, yy, M + CW, yy)
        sh.row(S, f"p2 index row {r + 1}")
        mid = yy - S / 2
        c.setFont("PB", 9); c.setFillColor(TEAL)
        c.drawCentredString((xs[0] + xs[1]) / 2, mid - 1.2 * mm, str(r + 1))
        c.setFont("PM", 8.5); c.setFillColor(GREY)
        c.drawCentredString((xs[3] + xs[4]) / 2, mid - 1.1 * mm, opts)
        sh.tick((xs[6] + xs[7]) / 2 - tb / 2, mid - tb / 2)
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    for xx in xs[1:-1]:
        c.line(xx, bot, xx, top)
    y = bot

    key = "Type key:  P = Praise  \u00b7  C = Corrective  \u00b7  CH = Coaching"
    sh.fits(key, "P", 8, CW, "type key")
    c.setFont("P", 8); c.setFillColor(NAVY)
    c.drawString(M, y - 4.4 * mm, key)
    y -= KEY + 3 * mm

    # teal callout: month-end count on the left, tip right-aligned
    c.setStrokeColor(TEAL); c.setLineWidth(0.9)
    c.roundRect(M, y - CALL, CW, CALL, 1.5 * mm, stroke=1, fill=0)
    c.setFillColor(TEAL); c.rect(M, y - CALL, 1.6 * mm, CALL, stroke=0, fill=1)
    base = y - CALL / 2 - 1.2 * mm
    xx = M + 5 * mm
    c.setFont("PM", 9.5); c.setFillColor(TEAL)
    lab = "Month-end count:"
    c.drawString(xx, base, lab)
    xx += c.stringWidth(lab, "PM", 9.5) + 3 * mm
    for k, code in enumerate(("P", "C", "CH")):
        c.setFont("PM", 9.5); c.setFillColor(TEAL)
        c.drawString(xx, base, code)
        xx += c.stringWidth(code, "PM", 9.5) + 1.2 * mm
        sh.rule(xx, xx + 12 * mm, base - 0.4 * mm, width=0.8)
        xx += 12 * mm + (3.5 * mm if k < 2 else 0)
    tip = "Aim for more P than C. No P this month? Look for one this week."
    tip_right = M + CW - 4 * mm
    tip_w = c.stringWidth(tip, "P", 8.5)
    tip_gap = tip_right - tip_w - xx
    assert tip_gap >= 3 * mm, f"callout tip collides with the count rules (gap {tip_gap / mm:.1f} mm)"
    c.setFont("P", 8.5); c.setFillColor(NAVY)
    c.drawRightString(tip_right, base, tip)
    y -= CALL
    assert y >= FOOT - 0.01, f"page 2 overflows by {(FOOT - y) / mm:.2f} mm"
    sh.footer("A conversation record for good management, not an HR, disciplinary or legal file.")
    return S, (y - FOOT), tip_gap


def build(pagesize, fname):
    W, H = pagesize
    c = MarginCanvas(str(OUT / fname), pagesize=pagesize, initialFontName="P")
    c.setTitle("Feedback Conversation Log"); c.setAuthor("Kevin Britz / Leadership by Design")
    c.setSubject("Printable feedback conversation record and monthly feedback index for managers")
    sh = Sheet(c, W, H)
    s1, spare1, type_spare = page_one(sh); n1 = len(sh.rows); c.showPage()
    s2, spare2, tip_gap = page_two(sh); c.showPage()
    c.save()
    low = min(h for _, h in sh.rows)
    assert low >= MIN_ROW - 1e-6
    p1 = [h for _, h in sh.rows[:n1]]
    p2 = [(w, h) for w, h in sh.rows[n1:]]
    p2_idx = [h for w, h in p2 if w.startswith("p2 index")]
    print(f"{fname}: page 1 row {s1 / mm:.2f} mm (spare {spare1 / mm:.1f} mm), "
          f"page 2 row {s2 / mm:.2f} mm (spare {spare2 / mm:.1f} mm), "
          f"{len(sh.rows)} rows checked, smallest {low / mm:.2f} mm, margins {M / mm:.0f} mm")
    print(f"  page 1: {len(p1)} write-in rows at {s1 / mm:.2f} mm; Type ticks spare {type_spare / mm:.1f} mm")
    print(f"  page 2: header fields 1 row at 9.00 mm; index {len(p2_idx)} rows at {s2 / mm:.2f} mm; "
          f"callout tip gap {tip_gap / mm:.1f} mm")


if __name__ == "__main__":
    register_fonts()
    build(A4, "feedback-conversation-log-A4.pdf")
    build(letter, "feedback-conversation-log-Letter.pdf")
