"""Build the Shift Incident / Issue Log print-and-write PDFs (A4 and US Letter).

Run from anywhere:  python3 products/shift-incident-log/src/make_pdf.py
Needs: reportlab, fontTools, Pillow (pip install reportlab fonttools pillow).

Self-contained: every path is relative to the repo root.
- Fonts: assets/fonts/ (Google Fonts variable fonts, SIL OFL 1.1, licence text next to each font).
  Static weights are instanced into a temporary folder at build time and only subsets are
  embedded in the PDFs. The vendored font files themselves are left unmodified.
- Logo: assets/brand/lbd-mark-reversed-cream.png (Leadership by Design L|BD mark, cream for dark bars).

Layout follows the build-ready brief in logs/2026-10-02.md (Day 4 layout from logs/2026-09-30.md plus
the five fixes in logs/critique-shift-incident-log-2026-09-30.md): two-row header fields, a fixed
3 + 2 break for the Type ticks, an Impact table with 3 rows and an on-page symbol legend, and a
page-height budget that is asserted below. Styling matches
products/one-on-one-meeting-template/src/make_pdf.py.

Page 1 uses a left label column (teal section label plus the prompt) instead of a title band above
each box. That keeps every write-in row at 8 mm or more on US Letter without cutting rows.

Rules (asserted): 12 mm margins, every write-in line and table row at least 8 mm tall, every
label fits its cell, nothing runs past the footer, no full-bleed fills.
"""
import tempfile
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
OUT = ROOT / "products" / "shift-incident-log"

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

    def status_dot(self, cx, cy, r, kind):
        """kind: full (OK), half (Watch), empty (Down). Vector shapes, so no glyph is needed."""
        c = self.c
        c.setStrokeColor(NAVY); c.setLineWidth(0.7); c.setFillColor(white)
        c.circle(cx, cy, r, stroke=1, fill=1)
        c.setFillColor(NAVY)
        if kind == "full":
            c.circle(cx, cy, r, stroke=0, fill=1)
        elif kind == "half":
            p = c.beginPath()
            p.moveTo(cx, cy - r)
            p.arcTo(cx - r, cy - r, cx + r, cy + r, startAng=-90, extent=180)
            p.close()
            c.drawPath(p, stroke=0, fill=1)

    def labelled_box(self, ytop, h, title, prompt=None, accent=None):
        """Full-width outlined box with a left label column. Returns (x0, x1) of the writing area."""
        c, CW = self.c, self.CW
        c.setStrokeColor(LINE); c.setLineWidth(0.7)
        c.roundRect(M, ytop - h, CW, h, 1.5 * mm, stroke=1, fill=0)
        xs = M + LBL
        c.line(xs, ytop - h, xs, ytop)
        if accent is not None:   # gold-accent left rule (Escalation), clipped to the rounded box
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
    y = sh.header_bar("SHIFT INCIDENT / ISSUE LOG", "One incident per sheet. Facts first.")
    FOOT = M + 10.5 * mm            # teal handover note + brand line

    # Page-height budget (logs/2026-10-02.md). Rows are the only thing that flexes.
    HDR_D = 8.6 * mm                # Impact header: column name + legend / hint sub-line
    HDR_G = 6.0 * mm                # Actions header
    ROWS = {"header fields": 2, "A Type": 2, "B What happened": 4, "C Immediate action": 3,
            "D Impact": 3, "E Likely cause": 2, "F Escalation": 2, "G Actions to close": 5,
            "Sign-off": 1}
    n_rows = sum(ROWS.values())     # 24
    n_gaps = len(ROWS) - 1          # gap after every block except the last
    n_pad = 6                       # write-in boxes A, B, C, E, F, sign-off
    fixed = n_gaps * VGAP + n_pad * PAD + HDR_D + HDR_G
    avail = y - FOOT
    S = min(MAX_ROW, (avail - fixed) / n_rows)
    assert S >= MIN_ROW, f"page 1 row height {S / mm:.2f} mm < 8 mm (avail {avail / mm:.1f} mm)"

    # Header fields: two rows (critique fix 1)
    w = CW - 2 * GAP
    # columns line up across both rows: 0.45 | 0.32 | 0.23
    row1 = (("Site / Area", 0.45), ("Date", 0.32), ("Time found", 0.23))
    x = M
    for lab, f in row1:
        sh.label_line(x, y - S, w * f, lab); x += w * f + GAP
    sh.row(S, "header row 1")
    yy = y - 2 * S
    sw = w * 0.45
    c.setFont("PM", 8.5); c.setFillColor(NAVY); c.drawString(M, yy + 1.0 * mm, "Shift")
    x = M + c.stringWidth("Shift", "PM", 8.5) + 2.5 * mm
    for lab in ("Day", "Swing", "Night"):
        x = sh.tick(x, yy + 0.8 * mm, lab) + 3.2 * mm
    x = sh.tick(x, yy + 0.8 * mm)
    assert M + sw - x >= 12 * mm, "no room for the other-shift write-in"
    sh.rule(x + 0.6 * mm, M + sw, yy)
    x = M + sw + GAP
    for lab, f in (("Reported by", 0.32), ("Role", 0.23)):  # same split as row 1
        sh.label_line(x, yy, w * f, lab); x += w * f + GAP
    sh.row(S, "header row 2")
    y -= 2 * S + VGAP

    # Box A: Type, fixed 3 + 2 break (critique fix 3)
    h = 2 * S + PAD
    x0, x1 = sh.labelled_box(y, h, "Type",
                             "One primary type. If it spans two, pick the one that needs action first.")
    cw = (x1 - x0 - 6 * mm) / 3
    for r, opts in enumerate((("Safety / near miss", "Equipment", "Quality / customer"),
                              ("Staffing / people",))):
        yy = y - (r + 1) * S
        for k, lab in enumerate(opts):
            sh.fits(lab, "P", 8.5, cw - 6 * mm, "Type tick")
            sh.tick(x0 + 3 * mm + k * cw, yy + 1.0 * mm, lab)
        sh.row(S, f"A Type row {r + 1}")
    xo = sh.tick(x0 + 3 * mm + cw, y - 2 * S + 1.0 * mm, "Other:")
    sh.rule(xo + 1.5 * mm, x1 - 3 * mm, y - 2 * S + 0.4 * mm)
    y -= h + VGAP

    def lined_box(y, n, title, prompt, labels=(), accent=None, what=""):
        h = n * S + PAD
        x0, x1 = sh.labelled_box(y, h, title, prompt, accent)
        for k in range(n):
            yy = y - (k + 1) * S
            if k < len(labels) and labels[k]:
                sh.label_line(x0 + 3 * mm, yy, x1 - x0 - 6 * mm, labels[k])
            else:
                sh.rule(x0 + 3 * mm, x1 - 3 * mm, yy)
            sh.row(S, f"{what} line {k + 1}")
        return y - h - VGAP

    # Box B and C
    y = lined_box(y, ROWS["B What happened"], "What happened",
                  "Facts only. What did you see or hear? Who was involved (roles, not gossip)?",
                  what="B What happened")
    y = lined_box(y, ROWS["C Immediate action"], "Immediate action",
                  "What did you do right away to make it safe or stop the loss?",
                  what="C Immediate action")

    # Box D: Impact, 3 rows (critique fix 5) with a legend under the header (critique fix 4)
    n = ROWS["D Impact"]
    h = HDR_D + n * S
    x0, x1 = sh.labelled_box(y, h, "Impact",
                             "One impact per row. More than 3? Continue in What happened and write \"see What happened\".")

    def legend(x, ybase, room):
        r = 1.15 * mm
        size = 7
        parts = (("full", "OK"), ("half", "Watch"), ("empty", "Down"))
        total = sum(2 * r + 1.0 * mm + c.stringWidth(t, "P", size) for _, t in parts) + 2 * 2.6 * mm
        assert total <= room, f"Impact legend {total / mm:.1f} mm wider than {room / mm:.1f} mm"
        xx = x
        for kind, t in parts:
            sh.status_dot(xx + r, ybase + 0.85 * mm, r, kind)
            xx += 2 * r + 1.0 * mm
            c.setFont("P", size); c.setFillColor(GREY); c.drawString(xx, ybase, t)
            xx += c.stringWidth(t, "P", size) + 2.6 * mm

    sh.table(x0, x1, y, HDR_D,
             ("People affected", "Output / quality hit", "Equipment status", "Est. downtime / delay"),
             (0.22, 0.24, 0.28, 0.26), n, S, "D Impact",
             sub=("who, how many", "units, batch, order", legend, "minutes or hours"))
    y -= h + VGAP

    # Box E: Likely cause
    y = lined_box(y, ROWS["E Likely cause"], "Likely cause",
                  "Best guess for now: process, tool, training, communication or other?",
                  labels=("Likely cause:", "Evidence / why:"), what="E Likely cause")

    # Box F: Escalation, gold-accent left rule
    n = ROWS["F Escalation"]
    h = n * S + PAD
    x0, x1 = sh.labelled_box(y, h, "Escalation", "Who knows about it beyond this shift?", accent=GOLD)
    iw = x1 - x0 - 6 * mm
    xa = x0 + 3 * mm
    yy = y - S
    sh.label_line(xa, yy, iw * 0.34, "Escalated to")
    xh = xa + iw * 0.34 + GAP
    c.setFont("PM", 8.5); c.setFillColor(NAVY); c.drawString(xh, yy + 1.0 * mm, "How:")
    xx = xh + c.stringWidth("How:", "PM", 8.5) + 2 * mm
    for lab in ("Call", "Radio", "Ticket"):
        xx = sh.tick(xx, yy + 0.8 * mm, lab) + 3.0 * mm
    xt = xa + iw * 0.79
    assert xx + 1 * mm <= xt, "How ticks collide with Time"
    sh.label_line(xt, yy, xa + iw - xt, "Time")
    sh.row(S, "F Escalation line 1")
    yy = y - 2 * S
    sh.label_line(xa, yy, iw * 0.40, "Ticket / ref no.")
    xn = sh.tick(xa + iw * 0.40 + GAP, yy + 0.8 * mm, "Not escalated. Reason:")
    sh.rule(xn + 1.8 * mm, xa + iw, yy)
    assert xa + iw - xn >= 30 * mm, "no room for the not-escalated reason"
    sh.row(S, "F Escalation line 2")
    y -= h + VGAP

    # Box G: Actions to close
    n = ROWS["G Actions to close"]
    h = HDR_G + n * S
    x0, x1 = sh.labelled_box(y, h, "Actions to close",
                             "Who does what, by when. Tick Done only when it is finished.")
    xs = sh.table(x0, x1, y, HDR_G, ("Owner", "What", "Due", "Status"),
                  (0.22, 0.46, 0.13, 0.19), n, S, "G Actions")
    sw = xs[4] - xs[3]
    for r in range(n):
        yb = y - HDR_G - (r + 1) * S + (S - 3.4 * mm) / 2
        xx = sh.tick(xs[3] + 2.0 * mm, yb, "Open", size=8) + 2.4 * mm
        xx = sh.tick(xx, yb, "Done", size=8)
        assert xx <= xs[4] - 1 * mm, f"Status ticks {xx - xs[3]:.1f} wider than column {sw:.1f}"
    y -= h + VGAP

    # Sign-off
    h = S + PAD
    x0, x1 = sh.labelled_box(y, h, "Sign-off")
    iw = x1 - x0 - 6 * mm
    xx = x0 + 3 * mm
    for lab, f in (("Reported by", 0.37), ("Supervisor reviewed", 0.41), ("Date", 0.22)):
        sh.label_line(xx, y - S, iw * f - (3 * mm if f != 0.22 else 0), lab)
        xx += iw * f
    sh.row(S, "Sign-off line")
    y -= h

    assert y >= FOOT - 0.01, f"page 1 overflows by {(FOOT - y) / mm:.2f} mm"
    sh.footer("Carry open actions into the Shift Handover Sheet. Do not leave them only on this page.")
    return S, (y - FOOT)


# ---------------------------------------------------------------- page 2
def page_two(sh):
    c, CW = sh.c, sh.CW
    y = sh.header_bar("OPEN INCIDENTS TRACKER", "Bring this page to every handover.")
    FOOT = M + 10.5 * mm
    c.setFont("ST", 15); c.setFillColor(NAVY)
    c.drawString(M, y - 8.0 * mm, "Open incidents this week")
    c.setFont("P", 9); c.setFillColor(GREY)
    c.drawString(M, y - 12.6 * mm, "Update at each handover. Close only when Done is ticked on the incident sheet.")
    y -= 14.5 * mm
    S0 = 9 * mm
    w = CW - 2 * GAP
    x = M
    for lab, f in (("Site / Area", 0.38), ("Week of", 0.26), ("Supervisor", 0.36)):
        sh.label_line(x, y - S0, w * f, lab); x += w * f + GAP
    sh.row(S0, "p2 header fields")
    y -= S0 + 4 * mm

    HDR = 8.6 * mm
    KEY = 6.5 * mm
    CALL = 11 * mm
    rows = 10
    S = (y - FOOT - HDR - KEY - 3 * mm - CALL) / rows
    assert S >= MIN_ROW, f"page 2 row {S / mm:.2f} mm < 8 mm"
    cols = ("#", "Date", "Type", "One-line summary", "Owner", "Due", "Status", "Handover ref")
    subs = ("", "", "circle one", "", "", "", "circle one", "sheet / item")
    fr = (0.045, 0.09, 0.115, 0.295, 0.13, 0.08, 0.135, 0.11)
    xs = [M]
    for f in fr:
        xs.append(xs[-1] + CW * f)
    assert abs(xs[-1] - (M + CW)) < 0.01
    top = y
    c.setFillColor(CREAM); c.rect(M, top - HDR, CW, HDR, stroke=0, fill=1)
    for i, col in enumerate(cols):
        cw = xs[i + 1] - xs[i] - 2.4 * mm
        sh.fits(col, "PM", 8.5, cw, "tracker header")
        c.setFont("PM", 8.5); c.setFillColor(NAVY)
        c.drawString(xs[i] + 1.4 * mm, top - HDR + (4.6 * mm if subs[i] else 3.0 * mm), col)
        if subs[i]:
            sh.fits(subs[i], "P", 7, cw, "tracker sub-header")
            c.setFont("P", 7); c.setFillColor(GREY)
            c.drawString(xs[i] + 1.4 * mm, top - HDR + 1.5 * mm, subs[i])
    bot = top - HDR - rows * S
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.rect(M, bot, CW, top - bot, stroke=1, fill=0)
    for r in range(rows):
        yy = top - HDR - r * S
        c.setStrokeColor(LINE); c.setLineWidth(0.6)
        c.line(M, yy, M + CW, yy)
        sh.row(S, f"p2 tracker row {r + 1}")
        c.setFont("PB", 9); c.setFillColor(TEAL)
        c.drawCentredString((xs[0] + xs[1]) / 2, yy - S / 2 - 1.2 * mm, str(r + 1))
        # circle-one options, grey, centred in the cell
        mid = yy - S / 2
        c.setFont("PM", 8.5); c.setFillColor(GREY)
        opts = "S   E   Q   P   O"
        sh.fits(opts, "PM", 8.5, xs[3] - xs[2] - 2.8 * mm, "type options")
        c.drawCentredString((xs[2] + xs[3]) / 2, mid - 1.1 * mm, opts)
        c.setFont("P", 7.5)
        status = ("Open", "Handed over", "Closed")
        lh = 3.3 * mm
        assert (len(status) - 1) * lh + 2.6 * mm <= S - 2 * mm, "status options do not fit the row"
        for k, t in enumerate(status):
            sh.fits(t, "P", 7.5, xs[7] - xs[6] - 2.8 * mm, "status options")
            c.drawCentredString((xs[6] + xs[7]) / 2, mid + lh - 1.0 * mm - k * lh, t)
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    for xx in xs[1:-1]:
        c.line(xx, bot, xx, top)
    y = bot

    key = ("Type key:  S = Safety / near miss  \u00b7  E = Equipment  \u00b7  Q = Quality / customer  "
           "\u00b7  P = Staffing / people  \u00b7  O = Other")
    sh.fits(key, "P", 8, CW, "type key")
    c.setFont("P", 8); c.setFillColor(NAVY)
    c.drawString(M, y - 4.4 * mm, key)
    y -= KEY + 3 * mm

    # teal callout
    msg = "If Status is Open at shift change, copy the # and Owner onto the Shift Handover open-items log."
    c.setStrokeColor(TEAL); c.setLineWidth(0.9)
    c.roundRect(M, y - CALL, CW, CALL, 1.5 * mm, stroke=1, fill=0)
    c.setFillColor(TEAL); c.rect(M, y - CALL, 1.6 * mm, CALL, stroke=0, fill=1)
    sh.fits(msg, "PM", 9.5, CW - 8 * mm, "callout")
    c.setFont("PM", 9.5); c.setFillColor(TEAL)
    c.drawString(M + 5 * mm, y - CALL / 2 - 1.2 * mm, msg)
    y -= CALL
    assert y >= FOOT - 0.01, f"page 2 overflows by {(FOOT - y) / mm:.2f} mm"
    sh.footer("This is an ops log, not a formal HR or legal investigation form.")
    return S, (y - FOOT)


def build(pagesize, fname):
    W, H = pagesize
    c = canvas.Canvas(str(OUT / fname), pagesize=pagesize, initialFontName="P")
    c.setTitle("Shift Incident / Issue Log"); c.setAuthor("Kevin Britz / Leadership by Design")
    c.setSubject("Printable shift incident report form and weekly open-incidents tracker")
    sh = Sheet(c, W, H)
    s1, spare1 = page_one(sh); c.showPage()
    s2, spare2 = page_two(sh); c.showPage()
    c.save()
    low = min(h for _, h in sh.rows)
    assert low >= MIN_ROW - 1e-6
    print(f"{fname}: page 1 row {s1 / mm:.2f} mm (spare {spare1 / mm:.1f} mm), "
          f"page 2 row {s2 / mm:.2f} mm (spare {spare2 / mm:.1f} mm), "
          f"{len(sh.rows)} rows checked, smallest {low / mm:.2f} mm, margins {M / mm:.0f} mm")


if __name__ == "__main__":
    register_fonts()
    build(A4, "shift-incident-log-A4.pdf")
    build(letter, "shift-incident-log-Letter.pdf")
