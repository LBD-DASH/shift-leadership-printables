"""Build the New Manager 30-60-90 Day Plan print-and-write PDFs (A4 and US Letter).

Run from anywhere:  python3 products/new-manager-30-60-90-day-plan/src/make_pdf.py
Needs: reportlab, fontTools, Pillow (pip install reportlab fonttools pillow).

Self-contained: every path is relative to the repo root.
- Fonts: assets/fonts/ (Google Fonts variable fonts, SIL OFL 1.1, licence text next to each font).
  Static weights are instanced into a temporary folder at build time and only subsets are
  embedded in the PDFs. The vendored font files themselves are left unmodified.
- Logo: assets/brand/lbd-mark-reversed-cream.png (Leadership by Design L|BD mark, cream for dark bars).

Layout follows the build-ready brief in logs/2026-10-03.md (Day 5 layout from logs/2026-10-01.md and
etsy/LISTING_30_60_90_DAY_PLAN.md). Styling matches products/shift-incident-log/src/make_pdf.py and
products/one-on-one-meeting-template/src/make_pdf.py.

Pages:
1. Plan on a page: identity block, By day 90 I want..., People I must meet (8-row table),
   How I'll know it's working, sign-off.
2. The three phases: three equal columns (Days 1-30, 31-60, 61-90), 5 tick-box actions each,
   What I learned lines and a phase check-in date.
3. 13-week check-in: one row per week, energy 1 to 5, weeks 4, 8 and 13 shaded as 30 / 60 / 90 markers.

Rules (asserted): 12 mm margins, every write-in line and table row at least 8 mm tall, every
label fits its cell, each page's zone heights sum to no more than the usable page height
(A4 about 273 mm, US Letter about 255 mm), nothing runs past the footer, no full-bleed fills.
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
OUT = ROOT / "products" / "new-manager-30-60-90-day-plan"

PLAYFAIR = FONTS / "playfair-display" / "PlayfairDisplay[wght].ttf"
SOURCE = FONTS / "source-sans-3" / "SourceSans3[wght].ttf"

# alias -> (variable font, weight)
WEIGHTS = {
    "P": (SOURCE, 400),     # body
    "PM": (SOURCE, 600),    # field labels
    "PB": (SOURCE, 700),    # numbers
    "SH": (PLAYFAIR, 600),  # section headings
    "ST": (PLAYFAIR, 700),  # titles
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
SHADE = HexColor("#F1F2F3")  # about 6% navy on white: 30 / 60 / 90 marker rows

M = 12 * mm          # margins, all sides
GAP = 4 * mm         # gutter between side-by-side fields and between the page 2 columns
VGAP = 2.5 * mm      # minimum gap between stacked boxes
T = 6.5 * mm         # section title band above each page 1 box
PAD = 1.2 * mm       # space under the last write-in line inside a box
MIN_ROW = 8 * mm     # handwriting rule
BAR = 13 * mm        # navy header bar (page 1)
FOOTER = "Designed by Kevin Britz / Leadership by Design  \u00b7  leadershipbydesign.co  \u00b7  For use within one workplace"
PRODUCT = "New Manager 30-60-90 Day Plan"


class Sheet:
    def __init__(self, c, W, H):
        self.c, self.W, self.H = c, W, H
        self.CW = W - 2 * M
        self.USABLE = H - 2 * M
        self.rows = []          # every write-in row / table row height drawn, for the report
        self.budget = {}        # page -> (sum of zone heights, usable height)

    # ---------- checks ----------
    def fits(self, text, font, size, maxw, what=""):
        w = self.c.stringWidth(text, font, size)
        assert w <= maxw + 0.01, f"'{text}' {what} is {w / mm:.1f} mm wide, room {maxw / mm:.1f} mm"

    def row(self, h, what):
        assert h >= MIN_ROW - 1e-6, f"{what}: row {h / mm:.2f} mm < 8 mm"
        self.rows.append((what, h))

    def check_budget(self, page, zones):
        """zones: list of (name, height). Sum must fit the usable height inside the margins."""
        total = sum(h for _, h in zones)
        assert total <= self.USABLE + 0.01, (
            f"page {page} budget {total / mm:.1f} mm > usable {self.USABLE / mm:.1f} mm: "
            + ", ".join(f"{n} {h / mm:.1f}" for n, h in zones))
        self.budget[page] = (total, self.USABLE, zones)

    # ---------- primitives ----------
    def header_bar(self, title):
        """Page 1 navy bar: cream title, gold edge, brand name and L|BD mark on the right."""
        c, CW = self.c, self.CW
        bh = BAR
        top = self.H - M
        c.setFillColor(NAVY); c.roundRect(M, top - bh, CW, bh, 2 * mm, stroke=0, fill=1)
        c.setFillColor(GOLD); c.rect(M, top - bh, 3 * mm, bh, stroke=0, fill=1)
        c.setFillColor(CREAM); c.setFont("ST", 16)
        c.drawString(M + 8 * mm, top - bh + 4.5 * mm, title)
        mh = 8 * mm
        im = Image.open(MARK); mw = mh * im.width / im.height
        mx = M + CW - 5 * mm - mw
        c.drawImage(str(MARK), mx, top - bh + (bh - mh) / 2, mw, mh, mask="auto")
        dx = mx - 3.5 * mm
        c.setStrokeColor(GOLD); c.setLineWidth(0.6)
        c.line(dx, top - bh + 3.0 * mm, dx, top - 3.0 * mm)
        c.setFont("PM", 9); c.setFillColor(GOLD)
        c.drawRightString(dx - 3.5 * mm, top - bh + 5.0 * mm, "Leadership by Design")
        tw = c.stringWidth(title, "ST", 16)
        rw = c.stringWidth("Leadership by Design", "PM", 9)
        assert M + 8 * mm + tw + 6 * mm < dx - 3.5 * mm - rw, "header bar text collides"
        c.setFillColor(GOLD); c.rect(M, top - bh - 1.2 * mm, CW, 0.5 * mm, stroke=0, fill=1)
        return top - bh - 1.2 * mm

    def page_header(self, title, subline, page):
        """Pages 2 and 3: navy Playfair title, gold underline, grey subline. Returns y below it."""
        c, CW = self.c, self.CW
        top = self.H - M
        c.setFont("ST", 18); c.setFillColor(NAVY)
        c.drawString(M, top - 6.6 * mm, title)
        right = f"{PRODUCT}  \u00b7  Page {page} of 3"
        c.setFont("PM", 8); c.setFillColor(GREY)
        c.drawRightString(M + CW, top - 6.0 * mm, right)
        assert c.stringWidth(title, "ST", 18) + 8 * mm + c.stringWidth(right, "PM", 8) < CW, \
            "page header title collides with page label"
        c.setFillColor(GOLD); c.rect(M, top - 9.0 * mm, CW, 0.5 * mm, stroke=0, fill=1)
        lines = simpleSplit(subline, "P", 9, CW)
        assert len(lines) <= 2, "page header subline wraps to more than 2 lines"
        c.setFont("P", 9); c.setFillColor(NAVY)
        yy = top - 13.4 * mm
        for ln in lines:
            c.drawString(M, yy, ln); yy -= 4.0 * mm
        return top - (16.0 * mm if len(lines) == 1 else 20.0 * mm)

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

    def fields(self, y, S, parts, what):
        """One row of label + write-in fields across the content width. parts: (label, fraction)."""
        w = self.CW - (len(parts) - 1) * GAP
        x = M
        assert abs(sum(f for _, f in parts) - 1) < 1e-6
        for lab, f in parts:
            self.label_line(x, y - S, w * f, lab); x += w * f + GAP
        self.row(S, what)

    def tickbox(self, x, y, s=3.4 * mm):
        c = self.c
        c.setStrokeColor(TEAL); c.setLineWidth(0.9); c.setFillColor(white)
        c.rect(x, y, s, s, stroke=1, fill=1)

    def check_mark(self, cx, cy, s=2.6 * mm):
        """Vector tick, so no font glyph is needed."""
        c = self.c
        c.setStrokeColor(NAVY); c.setLineWidth(1.1); c.setLineCap(1); c.setLineJoin(1)
        p = c.beginPath()
        p.moveTo(cx - s * 0.5, cy + s * 0.02)
        p.lineTo(cx - s * 0.15, cy - s * 0.35)
        p.lineTo(cx + s * 0.5, cy + s * 0.42)
        c.drawPath(p, stroke=1, fill=0)
        c.setLineCap(0); c.setLineJoin(0)

    def section(self, ytop, h, title, prompt):
        """Teal title band with gold marker and grey prompt, then an outlined box below it.
        Returns the inner x0, x1 and the box top."""
        c, CW = self.c, self.CW
        c.setFillColor(GOLD); c.rect(M, ytop - 4.6 * mm, 2.2 * mm, 4.0 * mm, stroke=0, fill=1)
        c.setFillColor(TEAL); c.setFont("SH", 11)
        c.drawString(M + 3.8 * mm, ytop - 4.0 * mm, title)
        tx = M + 3.8 * mm + c.stringWidth(title, "SH", 11) + 3 * mm
        self.fits(prompt, "P", 8.5, M + CW - tx, f"prompt for {title}")
        c.setFont("P", 8.5); c.setFillColor(GREY)
        c.drawString(tx, ytop - 4.0 * mm, prompt)
        btop = ytop - T
        c.setStrokeColor(LINE); c.setLineWidth(0.7)
        c.roundRect(M, ytop - h, CW, h - T, 1.5 * mm, stroke=1, fill=0)
        return M + 3 * mm, M + CW - 3 * mm, btop

    def callout(self, y, h, msg, size=9.5):
        c, CW = self.c, self.CW
        c.setStrokeColor(TEAL); c.setLineWidth(0.9)
        c.roundRect(M, y - h, CW, h, 1.5 * mm, stroke=1, fill=0)
        c.saveState()
        p = c.beginPath(); p.roundRect(M, y - h, CW, h, 1.5 * mm)
        c.clipPath(p, stroke=0, fill=0)
        c.setFillColor(TEAL); c.rect(M, y - h, 1.6 * mm, h, stroke=0, fill=1)
        c.restoreState()
        self.fits(msg, "PM", size, CW - 8 * mm, "callout")
        c.setFont("PM", size); c.setFillColor(TEAL)
        c.drawString(M + 5 * mm, y - h / 2 - 1.2 * mm, msg)

    def footer(self, note=None, rule=False):
        c = self.c
        if rule:
            c.setStrokeColor(NAVY); c.setLineWidth(0.5)
            c.line(M, M + 10.2 * mm, M + self.CW, M + 10.2 * mm)
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
    top = sh.H - M
    y = sh.header_bar("NEW MANAGER 30-60-90 DAY PLAN")
    c.setFont("PM", 10); c.setFillColor(NAVY)
    c.drawString(M, y - 5.4 * mm, "Listen first. Fix the basics. Then lead.")
    y -= 7.6 * mm
    HEAD = top - y
    FOOT = 10.5 * mm                # teal note + brand line, above the bottom margin

    # Page-height budget (logs/2026-10-03.md). Rows flex between 8 mm and S_MAX; spare goes to gaps.
    S_MAX = 10.5 * mm
    HDR_B = 6.5 * mm                # People table header
    ROWS = {"identity": 2, "A By day 90": 3, "B People": 8, "C Signs": 3, "sign-off": 1}
    n_rows = sum(ROWS.values())     # 17
    n_gaps = 4                      # identity|A, A|B, B|C, C|sign-off
    fixed = HEAD + FOOT + 3 * T + 2 * PAD + HDR_B + 3 * mm   # 3 mm: sign-off to footer note
    S = min(S_MAX, (sh.USABLE - fixed - n_gaps * VGAP) / n_rows)
    assert S >= MIN_ROW, f"page 1 row height {S / mm:.2f} mm < 8 mm"
    G = (sh.USABLE - fixed - n_rows * S) / n_gaps
    G = min(G, 8 * mm)
    assert G >= VGAP - 1e-6
    zones = [("header", HEAD), ("identity", 2 * S), ("gap", G),
             ("A By day 90", T + 3 * S + PAD), ("gap", G),
             ("B People", T + HDR_B + 8 * S), ("gap", G),
             ("C Signs", T + 3 * S + PAD), ("gap", G),
             ("sign-off", S + 3 * mm), ("footer", FOOT)]
    sh.check_budget(1, zones)

    # Identity block: two rows
    sh.fields(y, S, (("Name", 0.55), ("New role", 0.45)), "identity row 1")
    sh.fields(y - S, S, (("Team or shift", 0.40), ("Start date", 0.27), ("Manager", 0.33)), "identity row 2")
    y -= 2 * S + G

    def numbered(y, title, prompt, what):
        h = T + 3 * S + PAD
        x0, x1, bt = sh.section(y, h, title, prompt)
        for n in range(1, 4):
            yy = bt - n * S
            c.setFont("PB", 9); c.setFillColor(TEAL); c.drawString(x0, yy + 1.0 * mm, str(n))
            sh.rule(x0 + 5 * mm, x1, yy)
            sh.row(S, f"{what} line {n}")
        return y - h - G

    # Box A
    y = numbered(y, "By day 90 I want...",
                 "Three outcomes. Be specific enough that your manager can see them.", "A By day 90")

    # Box B: People I must meet, 8 rows
    h = T + HDR_B + 8 * S
    x0, x1, bt = sh.section(y, h, "People I must meet", "Names and roles. Tick when you have met them.")
    xl, xr = M, M + CW
    fr = (0.40, 0.33, 0.17, 0.10)
    xs = [xl]
    for f in fr:
        xs.append(xs[-1] + CW * f)
    assert abs(xs[-1] - xr) < 0.01
    c.saveState()
    p = c.beginPath(); p.roundRect(M, y - h, CW, h - T, 1.5 * mm)
    c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(CREAM); c.rect(xl, bt - HDR_B, CW, HDR_B, stroke=0, fill=1)
    c.restoreState()
    c.setStrokeColor(LINE); c.setLineWidth(0.7)
    c.roundRect(M, y - h, CW, h - T, 1.5 * mm, stroke=1, fill=0)
    for i, col in enumerate(("Name", "Role", "Date met")):
        sh.fits(col, "PM", 8.5, xs[i + 1] - xs[i] - 3 * mm, "people header")
        c.setFont("PM", 8.5); c.setFillColor(NAVY)
        c.drawString(xs[i] + 3 * mm, bt - HDR_B + 2.1 * mm, col)
    sh.check_mark((xs[3] + xs[4]) / 2, bt - HDR_B / 2)
    for r in range(8):
        yy = bt - HDR_B - r * S
        c.setStrokeColor(LINE); c.setLineWidth(0.5)
        c.line(xl, yy, xr, yy)
        sh.row(S, f"B People row {r + 1}")
        sh.tickbox((xs[3] + xs[4]) / 2 - 1.9 * mm, yy - S / 2 - 1.9 * mm, 3.8 * mm)
    c.setStrokeColor(LINE); c.setLineWidth(0.5)
    for xx in xs[1:-1]:
        c.line(xx, y - h, xx, bt)
    y -= h + G

    # Box C
    y = numbered(y, "How I'll know it's working",
                 "Three signs you (and your team) will notice.", "C Signs")

    # Sign-off
    sh.fields(y, S, (("Shared with my manager on", 0.55), ("Next check-in", 0.45)), "sign-off")
    y -= S + 3 * mm

    assert y >= M + FOOT - 0.01, f"page 1 overflows by {(M + FOOT - y) / mm:.2f} mm"
    sh.footer("Fill this page in week one. Bring it to your 30, 60 and 90-day conversations.")
    return S, G


# ---------------------------------------------------------------- page 2
PHASES = (
    ("DAYS 1-30", "Listen and learn",
     "No big changes yet. Learn the people, the routines and the numbers.",
     ("Meet every team member (use Page 1 list)",
      "Learn the shift routines end to end",
      "Sit in on a full handover (or run one with a buddy)",
      "Learn the safety rules that apply on this site",
      "Learn the numbers that matter this week (output, quality, absences)")),
    ("DAYS 31-60", "Fix the basics",
     "Start the habits. Win two small, visible improvements.",
     ("Start regular 1:1s (use the One-on-One Meeting Template)",
      "Set one clear team routine (start, mid-shift or end)",
      "Sort quick win #1:",
      "Sort quick win #2:",
      "Clear one open issue left from Days 1-30")),
    ("DAYS 61-90", "Lead and improve",
     "Agree direction. Handle one hard issue. Plan the next quarter.",
     ("Agree 2-3 team goals with your manager",
      "Deal with one hard issue (performance, process or conflict)",
      "Plan the next quarter with the team (one page is enough)",
      "Review open actions from Pages 1-2; close or reassign",
      "Write three things you will keep doing after day 90")),
)
WRITE_IN = {"Sort quick win #1:", "Sort quick win #2:"}   # these actions get a write-in rule


def page_two(sh):
    c, CW = sh.c, sh.CW
    top = sh.H - M
    y = sh.page_header("THE THREE PHASES",
                       "Tick actions as you finish them. Write what you learned. "
                       "Book a check-in with your manager at the end of each phase.", 2)
    HEAD = top - y
    FOOT = 13.0 * mm                # navy rule + note + brand line
    S0 = 9 * mm
    sh.fields(y, S0, (("Name", 0.40), ("Role", 0.33), ("Start date", 0.27)), "p2 identity")
    y -= S0 + 4 * mm
    IDENT = S0 + 4 * mm

    colw = (CW - 2 * GAP) / 3
    iw = colw - 6 * mm              # inner writing width
    tw = iw - 3.4 * mm - 1.8 * mm   # action text width after the tick box
    LH = 3.7 * mm                   # action text leading
    PLH = 3.5 * mm                  # purpose text leading

    wraps = [[simpleSplit(a, "P", 8.5, tw) for a in ph[3]] for ph in PHASES]
    purpose = [simpleSplit(ph[2], "P", 8, iw) for ph in PHASES]
    for ph, w in zip(PHASES, wraps):
        for a, lines in zip(ph[3], w):
            assert len(lines) <= 3, f"action '{a}' wraps to {len(lines)} lines"
        sh.fits(ph[1], "SH", 13, iw, "phase label")
    n_purpose = max(len(p) for p in purpose)
    max_text = max(len(l) for w in wraps for l in w)

    # Column zones. TOPZ: gold bar, DAYS label, phase label, purpose lines, rule.
    TOPZ = 1.4 * mm + 5.0 * mm + 6.2 * mm + n_purpose * PLH + 1.8 * mm
    LEARN_LBL = 6.5 * mm
    CHECK_LBL = 6.0 * mm
    S = 10 * mm                     # What I learned and check-in date rows
    BOT = 2.0 * mm                  # inner padding under the date row
    # Every action row holds up to max_text lines plus breathing room. Write-in actions need
    # 8 mm of handwriting space between their text and their rule, so rows hold that too.
    RA_MIN = max(14 * mm, 2.2 * mm + max_text * LH + 1.5 * mm, 2.2 * mm + LH + MIN_ROW)
    RA_MAX = 16 * mm
    col_avail = sh.USABLE - HEAD - IDENT - FOOT - 2 * mm   # 2 mm: column bottom to footer rule
    fixed = TOPZ + LEARN_LBL + CHECK_LBL + S + BOT
    n_learn = int((col_avail - fixed - 5 * RA_MIN) // S)
    assert n_learn >= 2, f"only {n_learn} What I learned lines fit"
    RA = min(RA_MAX, (col_avail - fixed - n_learn * S) / 5)
    COLH = fixed + 5 * RA + n_learn * S
    assert COLH <= col_avail + 0.01
    zones = [("header", HEAD), ("identity", IDENT), ("columns", COLH),
             ("gap", col_avail - COLH + 2 * mm), ("footer", FOOT)]
    sh.check_budget(2, zones)

    ytop = y
    for k, (days, label, _, actions) in enumerate(PHASES):
        x = M + k * (colw + GAP)
        x0 = x + 3 * mm
        c.setStrokeColor(LINE); c.setLineWidth(0.7)
        c.roundRect(x, ytop - COLH, colw, COLH, 1.5 * mm, stroke=1, fill=0)
        # gold-accent top rule, clipped to the rounded box
        c.saveState()
        p = c.beginPath(); p.roundRect(x, ytop - COLH, colw, COLH, 1.5 * mm)
        c.clipPath(p, stroke=0, fill=0)
        c.setFillColor(GOLD); c.rect(x, ytop - 1.4 * mm, colw, 1.4 * mm, stroke=0, fill=1)
        c.restoreState()
        yy = ytop - 1.4 * mm - 5.0 * mm
        c.setFont("PB", 8.5); c.setFillColor(NAVY); c.drawString(x0, yy + 1.2 * mm, days)
        yy -= 6.2 * mm
        c.setFont("SH", 13); c.setFillColor(TEAL); c.drawString(x0, yy + 1.0 * mm, label)
        c.setFont("P", 8); c.setFillColor(GREY)
        for ln in purpose[k]:
            yy -= PLH
            c.drawString(x0, yy + 0.6 * mm, ln)
        yy = ytop - TOPZ
        c.setStrokeColor(NAVY); c.setLineWidth(0.5); c.line(x0, yy, x0 + iw, yy)
        # actions
        for a, lines in zip(actions, wraps[k]):
            rt = yy
            sh.tickbox(x0, rt - 2.2 * mm - 3.0 * mm)
            c.setFont("P", 8.5); c.setFillColor(NAVY)
            ty = rt - 2.2 * mm - 2.6 * mm
            for ln in lines:
                c.drawString(x0 + 3.4 * mm + 1.8 * mm, ty, ln); ty -= LH
            yy -= RA
            if a in WRITE_IN:
                space = (rt - 2.2 * mm - 2.6 * mm - (len(lines) - 1) * LH) - yy
                assert space >= MIN_ROW, f"write-in under '{a}' only {space / mm:.1f} mm"
                sh.rule(x0 + 5.2 * mm, x0 + iw, yy + 0.8 * mm, width=0.6)
                sh.row(space, f"p2 {days} {a}")
            else:
                c.setStrokeColor(LINE); c.setLineWidth(0.35); c.setDash(1, 1.5)
                c.line(x0, yy, x0 + iw, yy); c.setDash()
            sh.row(RA, f"p2 {days} action")
        # What I learned
        c.setFont("PM", 9); c.setFillColor(TEAL)
        c.drawString(x0, yy - LEARN_LBL + 1.6 * mm, "What I learned")
        yy -= LEARN_LBL
        for n in range(n_learn):
            yy -= S
            sh.rule(x0, x0 + iw, yy)
            sh.row(S, f"p2 {days} learned line {n + 1}")
        # Phase check-in
        lab = "Phase check-in with my manager"
        sh.fits(lab, "PM", 8.5, iw, "check-in label")
        c.setFont("PM", 8.5); c.setFillColor(NAVY)
        c.drawString(x0, yy - CHECK_LBL + 1.4 * mm, lab)
        yy -= CHECK_LBL
        sh.label_line(x0, yy - S, iw, "Date")
        sh.row(S, f"p2 {days} check-in date")
        yy -= S + BOT
        assert abs(yy - (ytop - COLH)) < 0.01, "column content does not match its box"
    y = ytop - COLH
    assert y >= M + FOOT - 0.01, f"page 2 overflows by {(M + FOOT - y) / mm:.2f} mm"
    sh.footer("If a tick-box does not fit your workplace, rewrite it on the 'What I learned' line. "
              "Keep the phase order.", rule=True)
    return RA, S, n_learn


# ---------------------------------------------------------------- page 3
def page_three(sh):
    c, CW = sh.c, sh.CW
    top = sh.H - M
    y = sh.page_header("13-WEEK CHECK-IN",
                       "Five minutes every Friday. Take this page to your 30, 60 and 90-day conversations.", 3)
    HEAD = top - y
    S0 = 9 * mm
    sh.fields(y, S0, (("Name", 0.40), ("Role", 0.33), ("Week 1 starts", 0.27)), "p3 identity")
    y -= S0 + 4 * mm
    IDENT = S0 + 4 * mm

    HDR = 7.0 * mm
    LEG = 5.5 * mm
    CALL = 11 * mm
    FOOT = 7.0 * mm                 # brand line
    rows = 13
    S_MAX = 16 * mm
    fixed = HEAD + IDENT + HDR + LEG + 4 * mm + CALL + 2 * mm + FOOT
    S = min(S_MAX, (sh.USABLE - fixed) / rows)
    assert S >= MIN_ROW, f"page 3 row {S / mm:.2f} mm < 8 mm"
    zones = [("header", HEAD), ("identity", IDENT), ("table header", HDR), ("energy legend", LEG),
             ("13 rows", rows * S), ("gap", 4 * mm), ("callout", CALL), ("gap", 2 * mm), ("footer", FOOT)]
    sh.check_budget(3, zones)

    cols = ("Wk", "What I did", "What I learned", "What's next", "Energy (1-5)")
    fr = (0.085, 0.27, 0.27, 0.245, 0.13)
    xs = [M]
    for f in fr:
        xs.append(xs[-1] + CW * f)
    assert abs(xs[-1] - (M + CW)) < 0.01
    ttop = y
    bot = ttop - HDR - LEG - rows * S
    c.setFillColor(CREAM); c.rect(M, ttop - HDR, CW, HDR, stroke=0, fill=1)
    for i, col in enumerate(cols):
        sh.fits(col, "PM", 8.5, xs[i + 1] - xs[i] - 3 * mm, "tracker header")
        c.setFont("PM", 8.5); c.setFillColor(NAVY)
        c.drawString(xs[i] + 1.8 * mm, ttop - HDR + 2.4 * mm, col)
    # energy legend strip under the header
    leg = "Energy  1 = drained  \u00b7  3 = steady  \u00b7  5 = strong"
    sh.fits(leg, "P", 8, CW - 4 * mm, "energy legend")
    c.setFont("P", 8); c.setFillColor(GREY)
    c.drawRightString(M + CW - 2 * mm, ttop - HDR - LEG + 1.7 * mm, leg)
    markers = {4: "30-day", 8: "60-day", 13: "90-day"}
    r0 = ttop - HDR - LEG
    for r in range(rows):
        wk = r + 1
        yt = r0 - r * S
        if wk in markers:
            c.setFillColor(SHADE); c.rect(M, yt - S, CW, S, stroke=0, fill=1)
        sh.row(S, f"p3 week {wk}")
        cx = (xs[0] + xs[1]) / 2
        if wk in markers:
            c.setFont("PB", 10); c.setFillColor(TEAL)
            c.drawCentredString(cx, yt - S / 2 + 0.6 * mm, str(wk))
            sh.fits(markers[wk], "PB", 7, xs[1] - xs[0] - 2 * mm, "marker label")
            c.setFont("PB", 7); c.setFillColor(TEAL)
            c.drawCentredString(cx, yt - S / 2 - 3.4 * mm, markers[wk])
        else:
            c.setFont("PB", 10); c.setFillColor(TEAL)
            c.drawCentredString(cx, yt - S / 2 - 1.3 * mm, str(wk))
        # circle-one energy numbers
        opts = "1    2    3    4    5"
        sh.fits(opts, "PM", 9, xs[5] - xs[4] - 3 * mm, "energy options")
        c.setFont("PM", 9); c.setFillColor(GREY)
        c.drawCentredString((xs[4] + xs[5]) / 2, yt - S / 2 - 1.2 * mm, opts)
    # grid
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.rect(M, bot, CW, ttop - bot, stroke=1, fill=0)
    c.line(M, ttop - HDR, M + CW, ttop - HDR)
    for r in range(rows):
        c.line(M, r0 - r * S, M + CW, r0 - r * S)
    c.line(M, r0, M + CW, r0)
    for xx in xs[1:-1]:          # verticals skip the legend strip so its text stays clear
        c.line(xx, bot, xx, r0)
        c.line(xx, ttop - HDR, xx, ttop)
    y = bot - 4 * mm
    sh.callout(y, CALL, "A blank week is a week you did not review. Catch up on Monday; do not skip two in a row.")
    y -= CALL + 2 * mm
    assert y >= M + FOOT - 0.01, f"page 3 overflows by {(M + FOOT - y) / mm:.2f} mm"
    sh.footer()
    return S


def build(pagesize, fname):
    W, H = pagesize
    c = canvas.Canvas(str(OUT / fname), pagesize=pagesize, initialFontName="P", invariant=1)
    c.setTitle(PRODUCT); c.setAuthor("Kevin Britz / Leadership by Design")
    c.setSubject("Printable first 90 days plan for new managers, team leaders and shift supervisors")
    sh = Sheet(c, W, H)
    s1, g1 = page_one(sh); c.showPage()
    ra, s2, n2 = page_two(sh); c.showPage()
    s3 = page_three(sh); c.showPage()
    c.save()
    low = min(h for _, h in sh.rows)
    assert low >= MIN_ROW - 1e-6
    print(f"{fname}: margins {M / mm:.0f} mm, usable height {sh.USABLE / mm:.1f} mm")
    for p in sorted(sh.budget):
        total, usable, _ = sh.budget[p]
        print(f"  page {p} budget {total / mm:.1f} / {usable / mm:.1f} mm")
    print(f"  page 1 rows {s1 / mm:.2f} mm (gaps {g1 / mm:.2f} mm); page 2 action rows {ra / mm:.2f} mm, "
          f"write-in rows {s2 / mm:.2f} mm, {n2} What I learned lines per phase; page 3 rows {s3 / mm:.2f} mm")
    print(f"  {len(sh.rows)} rows checked, smallest {low / mm:.2f} mm")


if __name__ == "__main__":
    register_fonts()
    build(A4, "new-manager-30-60-90-day-plan-A4.pdf")
    build(letter, "new-manager-30-60-90-day-plan-Letter.pdf")
