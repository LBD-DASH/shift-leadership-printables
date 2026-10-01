"""Build the One-on-One Meeting Template print-and-write PDFs (A4 and US Letter).

Run from anywhere:  python3 products/one-on-one-meeting-template/src/make_pdf.py
Needs: reportlab, fontTools, Pillow (pip install reportlab fonttools pillow).

Self-contained: every path is relative to the repo root.
- Fonts: assets/fonts/ (Google Fonts variable fonts, SIL OFL 1.1, licence text next to each font).
  Static weights are instanced into a temporary folder at build time and only subsets are
  embedded in the PDFs. The vendored font files themselves are left unmodified.
- Logo: assets/brand/lbd-mark-reversed-cream.png (Leadership by Design L|BD mark, cream for dark bars).

Layout follows the Day 2 brief (logs/2026-09-28.md), the Day 3 deltas (logs/2026-09-29.md) and the
critique (logs/critique-one-on-one-layout-2026-09-28.md). Approach and styling match
products/shift-handover-sheet/src/make_pdf.py. Rules: 12 mm margins, every write-in line and table
row at least 8 mm tall, scale circles at least 7 mm with 3 mm gaps, no full-bleed fills.
"""
import os
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont as FTFont
from fontTools.varLib import instancer
from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[3]
FONTS = ROOT / "assets" / "fonts"
MARK = ROOT / "assets" / "brand" / "lbd-mark-reversed-cream.png"
OUT = ROOT / "products" / "one-on-one-meeting-template"

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
GAP = 4 * mm         # gutter between side-by-side boxes
VGAP = 2.5 * mm      # gap between stacked boxes
T = 6 * mm           # section title band above each box
PAD = 1.2 * mm       # space under the last line inside a box
MIN_ROW = 8 * mm     # handwriting rule
FOOTER = "Designed by Kevin Britz / Leadership by Design  \u00b7  leadershipbydesign.co  \u00b7  For use within one workplace"


class Sheet:
    def __init__(self, c, W, H):
        self.c, self.W, self.H = c, W, H
        self.CW = W - 2 * M

    # ---------- primitives ----------
    def header_bar(self, title, tagline):
        c, CW = self.c, self.CW
        bh = 14 * mm
        top = self.H - M
        c.setFillColor(NAVY); c.roundRect(M, top - bh, CW, bh, 2 * mm, stroke=0, fill=1)
        c.setFillColor(GOLD); c.rect(M, top - bh, 3 * mm, bh, stroke=0, fill=1)
        c.setFillColor(CREAM); c.setFont("ST", 17)
        c.drawString(M + 8 * mm, top - bh + 4.8 * mm, title)
        mh = 8.5 * mm
        im = Image.open(MARK); mw = mh * im.width / im.height
        mx = M + CW - 5 * mm - mw
        c.drawImage(str(MARK), mx, top - bh + (bh - mh) / 2, mw, mh, mask="auto")
        dx = mx - 3.5 * mm
        c.setStrokeColor(GOLD); c.setLineWidth(0.6)
        c.line(dx, top - bh + 3.2 * mm, dx, top - 3.2 * mm)
        c.setFont("PM", 9); c.setFillColor(GOLD)
        c.drawRightString(dx - 3.5 * mm, top - bh + 7.8 * mm, "Leadership by Design")
        c.setFont("P", 7.5); c.setFillColor(CREAM)
        c.drawRightString(dx - 3.5 * mm, top - bh + 3.9 * mm, tagline)
        # thin gold underline
        c.setFillColor(GOLD); c.rect(M, top - bh - 1.4 * mm, CW, 0.5 * mm, stroke=0, fill=1)
        return top - bh - 1.4 * mm

    def rule(self, x0, x1, y, width=0.6):
        self.c.setStrokeColor(LINE); self.c.setLineWidth(width)
        self.c.line(x0, y, x1, y)

    def label_line(self, x, y, w, label, size=8.5):
        """Label sitting on a write-in rule at baseline y; rule runs to x + w."""
        c = self.c
        c.setFont("PM", size); c.setFillColor(NAVY)
        c.drawString(x, y + 1.0 * mm, label)
        lw = c.stringWidth(label, "PM", size) + 1.8 * mm
        self.rule(x + lw, x + w, y)

    def section(self, x, ytop, w, h, title, hint=None):
        """Title band with gold marker, then an outlined box. Returns inner x, top, w, bottom."""
        c = self.c
        c.setFillColor(GOLD); c.rect(x, ytop - 4.4 * mm, 2.2 * mm, 4.0 * mm, stroke=0, fill=1)
        c.setFillColor(NAVY); c.setFont("SH", 10.5)
        c.drawString(x + 3.8 * mm, ytop - 3.8 * mm, title)
        if hint:
            tx = x + 3.8 * mm + c.stringWidth(title, "SH", 10.5) + 3 * mm
            c.setFont("P", 8); c.setFillColor(GREY)
            c.drawString(tx, ytop - 3.8 * mm, hint)
        btop = ytop - T
        c.setStrokeColor(LINE); c.setLineWidth(0.7)
        c.roundRect(x, ytop - h, w, h - T, 1.5 * mm, stroke=1, fill=0)
        return x + 3 * mm, btop, w - 6 * mm, ytop - h

    def footer(self):
        c = self.c
        c.setFillColor(GOLD); c.rect(self.W / 2 - 10 * mm, M + 4.0 * mm, 20 * mm, 0.6 * mm, stroke=0, fill=1)
        c.setFont("P", 7.2); c.setFillColor(GREY)
        c.drawCentredString(self.W / 2, M + 0.8 * mm, "\u00a9 " + FOOTER)

    def tickbox(self, x, y, s=3.4 * mm):
        c = self.c
        c.setStrokeColor(TEAL); c.setLineWidth(0.9); c.setFillColor(white)
        c.rect(x, y, s, s, stroke=1, fill=1)


def page_one(sh):
    c, W, CW = sh.c, sh.W, sh.CW
    y = sh.header_bar("ONE-ON-ONE MEETING", "Their agenda first. Clear actions.")
    FOOT = M + 7 * mm

    # Fixed heights (everything that is not a write-in row)
    CALLOUT = 6.2 * mm
    SCALE = 12.5 * mm      # scale label + circle row inside Check-in
    ACT_HDR = 5.8 * mm
    n_rows = 2 + 4 + 1 + 3 + 5 + 2 + 1   # header fields, agenda, why, well/hard, actions, feedback/growth, sign-off
    fixed = (VGAP + CALLOUT + VGAP          # callout under header fields
             + 6 * T + 6 * PAD + 5 * VGAP + 1.0 * mm   # six box rows
             + SCALE + ACT_HDR)
    avail = y - FOOT
    S = min(9.5 * mm, (avail - fixed) / n_rows)
    assert S >= MIN_ROW, f"row height {S / mm:.2f} mm < 8 mm"
    sh.row = S

    # Header fields: two rows of three
    cw3 = (CW - 2 * GAP) / 3
    for r, labels in enumerate((("Name", "Role", "Manager"), ("Date", "Last 1:1", "Next 1:1"))):
        yy = y - (r + 1) * S
        for k, lab in enumerate(labels):
            sh.label_line(M + k * (cw3 + GAP), yy, cw3, lab)
    y -= 2 * S + VGAP

    # Callout (Day 3 delta 4)
    c.setStrokeColor(TEAL); c.setLineWidth(0.8); c.setFillColor(white)
    c.roundRect(M, y - CALLOUT, CW, CALLOUT, 1.5 * mm, stroke=1, fill=0)
    c.setFillColor(TEAL); c.rect(M, y - CALLOUT, 1.6 * mm, CALLOUT, stroke=0, fill=1)
    c.setFont("PM", 8.5); c.setFillColor(TEAL)
    c.drawString(M + 4.5 * mm, y - CALLOUT + 2.1 * mm,
                 "Not an HR rating form. Private between manager and team member.")
    y -= CALLOUT + VGAP

    # Box A: Their agenda first (+ follow-up from last 1:1, critique 2)
    h = T + 4 * S + PAD
    ix, it, iw, ib = sh.section(M, y, CW, h, "Their agenda first",
                                "What do you want to raise today? Team member fills this in before the meeting.")
    sh.label_line(ix, it - S, iw, "Follow-up from last 1:1:")
    for n in range(1, 4):
        yy = it - (n + 1) * S
        c.setFont("PB", 8.5); c.setFillColor(TEAL); c.drawString(ix, yy + 1.0 * mm, str(n))
        sh.rule(ix + 4.5 * mm, ix + iw, yy)
    y -= h + VGAP

    # Box B: Check-in scales with a "why" line (critique 1, delta 2)
    h = T + SCALE + S + PAD
    ix, it, iw, ib = sh.section(M, y, CW, h, "Check-in", "Circle 1 (low) to 5 (high) for each.")
    colw = (iw - 2 * GAP) / 3
    D = 7 * mm; G = 3 * mm
    for k, lab in enumerate(("Workload", "Energy", "Clarity on what's expected")):
        x0 = ix + k * (colw + GAP)
        c.setFont("PM", 8.5); c.setFillColor(NAVY)
        c.drawString(x0, it - 3.8 * mm, lab)
        cy = it - 4.8 * mm - D / 2 - 0.4 * mm
        for i in range(5):
            cx = x0 + D / 2 + i * (D + G)
            c.setStrokeColor(TEAL); c.setLineWidth(0.9); c.setFillColor(white)
            c.circle(cx, cy, D / 2, stroke=1, fill=1)
            c.setFont("PB", 9); c.setFillColor(NAVY)
            c.drawCentredString(cx, cy - 1.1 * mm, str(i + 1))
        sh.label_line(x0, it - SCALE - S, colw, "In a word, why?", size=8)
    y -= h + VGAP

    # Box C: going well | hard right now
    half = (CW - GAP) / 2
    h = T + 3 * S + PAD
    for k, title in enumerate(("What's going well", "What's hard right now")):
        ix, it, iw, ib = sh.section(M + k * (half + GAP), y, half, h, title)
        for n in range(1, 4):
            sh.rule(ix, ix + iw, it - n * S)
    y -= h + VGAP

    # Box F: Actions table (delta 3 moves it before feedback; critique 4: 5 rows)
    h = T + ACT_HDR + 5 * S + PAD
    ix, it, iw, ib = sh.section(M, y, CW, h, "Actions",
                                "Who does what, by when. Check these first at the next 1:1.")
    top_t = it - 1.0 * mm
    c.setFillColor(CREAM); c.rect(ix, top_t - ACT_HDR, iw, ACT_HDR, stroke=0, fill=1)
    fr = (0.22, 0.58, 0.20)
    xs = [ix]
    for f in fr:
        xs.append(xs[-1] + iw * f)
    c.setFont("PM", 8.5); c.setFillColor(NAVY)
    for i, col in enumerate(("Who", "What", "By when")):
        c.drawString(xs[i] + 1.8 * mm, top_t - ACT_HDR + 1.8 * mm, col)
    bot_t = top_t - ACT_HDR - 5 * S
    c.setStrokeColor(LINE); c.setLineWidth(0.5)
    c.rect(ix, bot_t, iw, top_t - bot_t, stroke=1, fill=0)
    for r in range(5):
        c.line(ix, top_t - ACT_HDR - r * S, ix + iw, top_t - ACT_HDR - r * S)
    for xx in xs[1:-1]:
        c.line(xx, bot_t, xx, top_t)
    y -= h + VGAP

    # Box D | Box E: feedback both ways | growth
    h = T + 2 * S + PAD
    ix, it, iw, ib = sh.section(M, y, half, h, "Feedback both ways", "One thing each way.")
    sh.label_line(ix, it - S, iw, "Manager to them:")
    sh.label_line(ix, it - 2 * S, iw, "Them to manager:")
    ix, it, iw, ib = sh.section(M + half + GAP, y, half, h, "Growth", "One skill before the next 1:1.")
    sh.label_line(ix, it - S, iw, "Skill to build:")
    sh.label_line(ix, it - 2 * S, iw, "How we'll practise it:")
    y -= h + VGAP

    # Sign-off with next 1:1 date (critique 3)
    h = T + S + PAD
    ix, it, iw, ib = sh.section(M, y, CW, h, "Sign-off", "We both agree these actions.")
    yy = it - S
    parts = (("Manager", 0.30), ("Team member", 0.30), ("Date", 0.17), ("Next 1:1", 0.23))
    x0 = ix
    for lab, f in parts:
        w = iw * f
        sh.label_line(x0, yy, w - 3 * mm, lab)
        x0 += w
    y -= h

    assert y >= FOOT - 0.5 * mm, f"page 1 overflows by {(FOOT - y) / mm:.1f} mm"
    sh.footer()
    return S, y - FOOT


def page_two(sh):
    c, W, CW = sh.c, sh.W, sh.CW
    y = sh.header_bar("12-MONTH 1:1 TRACKER", "Reschedule, don't skip.")
    FOOT = M + 7 * mm
    c.setFont("ST", 15); c.setFillColor(NAVY)
    c.drawString(M, y - 8.5 * mm, "Bring this page to every 1:1.")
    y -= 10.5 * mm
    cw3 = (CW - 2 * GAP) / 3
    S0 = 9 * mm
    for k, lab in enumerate(("Name", "Role", "Manager")):
        sh.label_line(M + k * (cw3 + GAP), y - S0, cw3, lab)
    y -= S0 + 4 * mm

    CALL = 11 * mm
    HDR = 7 * mm
    rows = 12
    S = (y - FOOT - CALL - 4 * mm - HDR) / rows
    assert S >= MIN_ROW
    fr = (0.07, 0.15, 0.16, 0.34, 0.12, 0.16)
    cols = ("#", "Month", "Date held", "Key theme", "Action done", "Next 1:1 booked")
    xs = [M]
    for f in fr:
        xs.append(xs[-1] + CW * f)
    top_t = y
    c.setFillColor(CREAM); c.rect(M, top_t - HDR, CW, HDR, stroke=0, fill=1)
    c.setFont("PM", 8.5); c.setFillColor(NAVY)
    for i, col in enumerate(cols):
        c.drawString(xs[i] + 1.8 * mm, top_t - HDR + 2.3 * mm, col)
    bot = top_t - HDR - rows * S
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.rect(M, bot, CW, top_t - bot, stroke=1, fill=0)
    for r in range(rows):
        yy = top_t - HDR - r * S
        c.setStrokeColor(LINE); c.setLineWidth(0.6)
        c.line(M, yy, M + CW, yy)
        c.setFont("PB", 9); c.setFillColor(TEAL)
        c.drawCentredString((xs[0] + xs[1]) / 2, yy - S / 2 - 1.2 * mm, str(r + 1))
        bx = (xs[4] + xs[5]) / 2 - 1.9 * mm
        sh.tickbox(bx, yy - S / 2 - 1.9 * mm, 3.8 * mm)
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    for xx in xs[1:-1]:
        c.line(xx, bot, xx, top_t)
    y = bot - 4 * mm

    # teal callout
    c.setStrokeColor(TEAL); c.setLineWidth(0.9); c.setFillColor(white)
    c.roundRect(M, y - CALL, CW, CALL, 1.5 * mm, stroke=1, fill=0)
    c.setFillColor(TEAL); c.rect(M, y - CALL, 1.6 * mm, CALL, stroke=0, fill=1)
    c.setFont("SH", 10.5); c.setFillColor(TEAL)
    c.drawString(M + 5 * mm, y - CALL / 2 - 1.3 * mm,
                 "A gap in this table is a conversation that didn't happen. Reschedule, don't skip.")
    y -= CALL
    assert y >= FOOT - 0.5 * mm, f"page 2 overflows by {(FOOT - y) / mm:.1f} mm"
    sh.footer()
    return S


def build(pagesize, fname):
    W, H = pagesize
    c = canvas.Canvas(str(OUT / fname), pagesize=pagesize, initialFontName="P")
    c.setTitle("One-on-One Meeting Template"); c.setAuthor("Kevin Britz / Leadership by Design")
    c.setSubject("Printable one-on-one meeting sheet and 12-month tracker")
    sh = Sheet(c, W, H)
    s1, spare = page_one(sh); c.showPage()
    s2 = page_two(sh); c.showPage()
    c.save()
    print(f"{fname}: page 1 row {s1 / mm:.2f} mm (spare {spare / mm:.1f} mm), page 2 row {s2 / mm:.2f} mm")


if __name__ == "__main__":
    register_fonts()
    build(A4, "one-on-one-meeting-template-A4.pdf")
    build(letter, "one-on-one-meeting-template-Letter.pdf")
