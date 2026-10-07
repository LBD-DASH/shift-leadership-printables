"""Build the Shift Handover Sheet print-and-write PDFs (A4 and US Letter), version 3.

Run from anywhere:  python3 products/shift-handover-sheet/src/make_pdf.py
Needs: reportlab, fontTools, Pillow (pip install reportlab fonttools pillow).

Self-contained: every path is relative to the repo root.
- Fonts: assets/fonts/ (Google Fonts variable fonts, SIL OFL 1.1, licence text next to each font).
  Static weights are instanced into a temporary folder at build time and only subsets are
  embedded in the PDFs. The vendored font files themselves are left unmodified.
- Logo: assets/brand/lbd-mark-reversed-cream.png (Leadership by Design L|BD mark, cream for dark bars).

Why v3: the v2 sheet (Day 1) was built before the shop's 8 mm handwriting rule. Its write-in
lines were 5.5 to 6.2 mm apart, so it failed PDF QA check C09 (rows at least 8 mm) on 2026-10-06
and 2026-10-07. v2 also read its fonts from a path outside the repo and its footer had no
"Designed by Kevin Britz" credit. v3 keeps the same one-page handover content and puts it on
the Sheet helpers used by every other product, forked from
products/weekly-team-check-in/src/make_pdf.py. Spec: logs/2026-10-07.md section 1.

Rules (asserted): 12 mm margins (every filled shape and image stays inside them, so there are
no full-bleed fills), every write-in line and table row at least 8 mm tall, every label fits
its cell, nothing runs past the footer. The script prints the row height and spare space.
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
OUT = ROOT / "products" / "shift-handover-sheet"

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
MAX_ROW = 9.5 * mm   # do not stretch rows beyond this
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


# ---------------------------------------------------------------- the sheet
def shift_line(sh, x, y, w, size=8.5):
    """'Shift:' label, Day / Night / Other ticks, then a write-in rule for 'Other'."""
    c = sh.c
    c.setFont("PM", size); c.setFillColor(NAVY)
    c.drawString(x, y + 1.0 * mm, "Shift:")
    xx = x + c.stringWidth("Shift:", "PM", size) + 2.0 * mm
    for lab in ("Day", "Night", "Other"):
        xx = sh.tick(xx, y + 0.6 * mm, lab, size=size) + 3.0 * mm
    assert x + w - xx >= 10 * mm, "no room to write the 'Other' shift"
    sh.rule(xx - 2.0 * mm, x + w, y)


def page(sh):
    c, CW = sh.c, sh.CW
    y = sh.header_bar("SHIFT HANDOVER SHEET", "Clear handovers. Safer shifts.")
    FOOT = M + 10.5 * mm            # teal note + brand line

    HDR = 6.0 * mm                  # table header rows (no sub-line)
    ROWS = OrderedDict((("header fields", 2), ("A Staffing", 2), ("B Safety", 3),
                        ("C Output", 3), ("D Equipment", 3), ("E Open tasks", 4),
                        ("F Quality", 2), ("G Key messages", 3), ("H Sign-off", 1)))
    n_rows = sum(ROWS.values())     # 23
    assert n_rows == 23
    n_gaps = len(ROWS) - 1          # 8
    n_pad = 5                       # boxes A, B, F, G, H (tables C, D, E have no pad)
    n_hdr = 3                       # tables C, D, E
    fixed = n_gaps * VGAP + n_pad * PAD + n_hdr * HDR
    avail = y - FOOT
    S = min(MAX_ROW, (avail - fixed) / n_rows)
    assert S >= MIN_ROW, f"row height {S / mm:.2f} mm < 8 mm (avail {avail / mm:.1f} mm)"

    # Header fields, two rows, columns aligned
    w = CW - 2 * GAP
    f1, f2, f3 = 0.24, 0.46, 0.30
    sh.label_line(M, y - S, w * f1, "Date")
    shift_line(sh, M + w * f1 + GAP, y - S, w * f2)
    sh.label_line(M + w * (f1 + f2) + 2 * GAP, y - S, w * f3, "Handover time")
    sh.row(S, "header row 1")
    g1, g2, g3 = 0.36, 0.36, 0.28
    sh.label_line(M, y - 2 * S, w * g1, "Outgoing leader")
    sh.label_line(M + w * g1 + GAP, y - 2 * S, w * g2, "Incoming leader")
    sh.label_line(M + w * (g1 + g2) + 2 * GAP, y - 2 * S, w * g3, "Area / line")
    sh.row(S, "header row 2")
    y -= 2 * S + VGAP

    def lines_box(y, title, prompt, labels, what, accent=None, numbered=False):
        """Box with n write-in lines. labels: list of label strings or None (plain rule)."""
        n = len(labels)
        h = n * S + PAD
        x0, x1 = sh.labelled_box(y, h, title, prompt, accent=accent)
        for k, lab in enumerate(labels):
            yy = y - (k + 1) * S
            if numbered:
                c.setFont("PB", 9); c.setFillColor(TEAL)
                c.drawString(x0 + 3 * mm, yy + 1.0 * mm, str(k + 1))
                sh.rule(x0 + 8 * mm, x1 - 3 * mm, yy)
            elif lab is None:
                sh.rule(x0 + 3 * mm, x1 - 3 * mm, yy)
            elif isinstance(lab, tuple):
                iw = x1 - x0 - 6 * mm - (len(lab) - 1) * GAP
                xa = x0 + 3 * mm
                for text, f in lab:
                    sh.label_line(xa, yy, iw * f, text); xa += iw * f + GAP
            else:
                sh.label_line(x0 + 3 * mm, yy, x1 - x0 - 6 * mm, lab)
            sh.row(S, f"{what} line {k + 1}")
        return y - h - VGAP

    def table_box(y, title, prompt, cols, fracs, n, what):
        h = HDR + n * S
        x0, x1 = sh.labelled_box(y, h, title, prompt)
        sh.table(x0, x1, y, HDR, cols, fracs, n, S, what)
        return y - h - VGAP

    # A. Staffing
    y = lines_box(y, "Staffing", "Headcount planned and actual. Who is in, who is not.",
                  [(("Planned", 0.20), ("Actual", 0.20), ("Absent / late (names):", 0.60)),
                   "Overtime or cover arranged:"], "A Staffing")
    # B. Safety
    y = lines_box(y, "Safety", "Full details go on the Shift Incident Log.",
                  ["Incidents / near misses:", "Hazards to watch:", "Open safety actions:"], "B Safety")
    # C. Output vs target
    y = table_box(y, "Output vs target", "Say why, not only what.",
                  ("Measure", "Target", "Actual", "Variance", "Reason"),
                  (0.30, 0.14, 0.14, 0.14, 0.28), ROWS["C Output"], "C Output")
    # D. Equipment and maintenance
    y = table_box(y, "Equipment", "Faults, jobs logged, what to watch.",
                  ("Equipment / asset", "Issue", "Job no.", "Status"),
                  (0.28, 0.44, 0.14, 0.14), ROWS["D Equipment"], "D Equipment")
    # E. Open tasks carried over
    y = table_box(y, "Open tasks", "Carried over to the next shift. One owner each.",
                  ("Task / action", "Owner", "Due", "Status"),
                  (0.52, 0.20, 0.13, 0.15), ROWS["E Open tasks"], "E Open tasks")
    # F. Quality or customer issues
    y = lines_box(y, "Quality and customers", "Complaints, defects, holds.",
                  [None, None], "F Quality")
    # G. Key messages (gold accent: the part the next leader must not miss)
    y = lines_box(y, "Key messages", "Top three things the next shift must know.",
                  [None, None, None], "G Key messages", accent=GOLD, numbered=True)
    # H. Sign-off
    y = lines_box(y, "Sign-off", None,
                  [(("Outgoing leader", 0.34), ("Time", 0.16), ("Incoming leader", 0.34),
                    ("Time", 0.16))], "H Sign-off")
    y += VGAP                       # no gap after the last block

    assert y >= FOOT - 0.01, f"page overflows by {(FOOT - y) / mm:.2f} mm"
    sh.footer("Walk it through face to face. Both leaders sign before the outgoing leader leaves.")
    return S, (y - FOOT)


def build(pagesize, fname):
    W, H = pagesize
    c = MarginCanvas(str(OUT / fname), pagesize=pagesize, initialFontName="P")
    c.setTitle("Shift Handover Sheet"); c.setAuthor("Kevin Britz / Leadership by Design")
    c.setSubject("Printable shift handover sheet for supervisors and team leaders")
    sh = Sheet(c, W, H)
    s, spare = page(sh); c.showPage()
    c.save()
    low = min(h for _, h in sh.rows)
    assert low >= MIN_ROW - 1e-6
    print(f"{fname}: 1 page, {len(sh.rows)} write-in rows at {s / mm:.2f} mm "
          f"(spare {abs(spare) / mm:.1f} mm), smallest {low / mm:.2f} mm, margins {M / mm:.0f} mm")


if __name__ == "__main__":
    register_fonts()
    build(A4, "shift-handover-sheet-A4.pdf")
    build(letter, "shift-handover-sheet-Letter.pdf")
