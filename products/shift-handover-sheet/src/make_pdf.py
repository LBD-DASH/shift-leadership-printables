from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# v2: Leadership by Design brand (www.leadershipbydesign.co)
# Static instances of the Google variable fonts (made with fontTools.instancer) live in src/fonts/.
FD = "/workspace/side-ventures/printables/etsy/src/fonts/"
pdfmetrics.registerFont(TTFont("P", FD + "SourceSans3-w400.ttf"))    # body
pdfmetrics.registerFont(TTFont("PM", FD + "SourceSans3-w600.ttf"))   # field labels
pdfmetrics.registerFont(TTFont("PB", FD + "SourceSans3-w700.ttf"))   # numbers
pdfmetrics.registerFont(TTFont("SH", FD + "PlayfairDisplay-w600.ttf"))  # section headings
pdfmetrics.registerFont(TTFont("ST", FD + "PlayfairDisplay-w700.ttf"))  # title
NAVY = HexColor("#0F1F2E"); GOLD = HexColor("#C8A864"); TEAL = HexColor("#2A7B88")
CREAM = HexColor("#F8F6F1")
GREY = HexColor("#5F6A73")      # --lbd-ink-muted (navy 65%) on white
LIGHT = CREAM                   # table header fill (very light, prints cleanly)
LINE = HexColor("#B7BEC4")      # navy-tinted rule, visible when printed
YEL = GOLD                      # accents formerly yellow
OUT = "/workspace/side-ventures/printables/etsy/"
MARK = "/workspace/side-ventures/printables/etsy/brand/lbd-mark-reversed-cream.png"

def build(pagesize, fname):
    W, H = pagesize
    c = canvas.Canvas(OUT + fname, pagesize=pagesize, initialFontName="P")
    c.setTitle("Shift Handover Sheet"); c.setAuthor("Leadership by Design")
    c.setSubject("Printable shift handover sheet")
    M = 12 * mm
    CW = W - 2 * M
    GAP = 4 * mm

    # header bar
    bh = 15 * mm
    top = H - M
    c.setFillColor(NAVY); c.roundRect(M, top - bh, CW, bh, 2 * mm, stroke=0, fill=1)
    c.setFillColor(YEL); c.rect(M, top - bh, 3 * mm, bh, stroke=0, fill=1)
    c.setFillColor(CREAM); c.setFont("ST", 18)
    c.drawString(M + 8 * mm, top - bh + 5.0 * mm, "Shift Handover Sheet")
    # L|BD mark (cream reversed) at the right, thin gold divider, then brand text
    mh = 9 * mm
    from PIL import Image as _I
    _im = _I.open(MARK); mw = mh * _im.width / _im.height
    mx = M + CW - 6 * mm - mw
    c.drawImage(MARK, mx, top - bh + (bh - mh) / 2, mw, mh, mask="auto")
    dx = mx - 3.5 * mm
    c.setStrokeColor(GOLD); c.setLineWidth(0.6)
    c.line(dx, top - bh + 3.5 * mm, dx, top - 3.5 * mm)
    c.setFont("PM", 9); c.setFillColor(GOLD)
    c.drawRightString(dx - 3.5 * mm, top - bh + 8.3 * mm, "Leadership by Design")
    c.setFont("P", 7.5); c.setFillColor(CREAM)
    c.drawRightString(dx - 3.5 * mm, top - bh + 4.3 * mm, "Clear handovers. Safer shifts.")
    y = top - bh - 5 * mm

    def label_line(x, yb, w, label, font="PM", size=8.5):
        c.setFont(font, size); c.setFillColor(NAVY)
        c.drawString(x, yb, label)
        lw = c.stringWidth(label, font, size) + 1.5 * mm
        c.setStrokeColor(LINE); c.setLineWidth(0.6)
        c.line(x + lw, yb - 0.8 * mm, x + w, yb - 0.8 * mm)

    def tick(x, yb, label):
        s = 3.2 * mm
        c.setStrokeColor(TEAL); c.setLineWidth(0.9); c.setFillColor(white)
        c.rect(x, yb - 0.6 * mm, s, s, stroke=1, fill=1)
        c.setFont("P", 8.5); c.setFillColor(NAVY)
        c.drawString(x + s + 1.4 * mm, yb, label)
        return x + s + 1.4 * mm + c.stringWidth(label, "P", 8.5) + 4 * mm

    # header fields
    rowh = 8 * mm
    yb = y - 4 * mm
    label_line(M, yb, CW * 0.30, "Date")
    x = M + CW * 0.34
    c.setFont("PM", 8.5); c.setFillColor(NAVY); c.drawString(x, yb, "Shift:")
    x += c.stringWidth("Shift:", "PM", 8.5) + 3 * mm
    x = tick(x, yb, "Day"); x = tick(x, yb, "Night"); x = tick(x, yb, "Other")
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.line(x - 3 * mm, yb - 0.8 * mm, M + CW, yb - 0.8 * mm)
    yb -= rowh
    cw3 = (CW - 2 * GAP) / 3
    label_line(M, yb, cw3, "Outgoing leader")
    label_line(M + cw3 + GAP, yb, cw3, "Incoming leader")
    label_line(M + 2 * (cw3 + GAP), yb, cw3, "Area / Line")
    y = yb - 6 * mm

    FOOT = M + 7 * mm  # bottom of content
    TITLE_H = 7 * mm

    def section(x, ytop, w, h, title):
        # title with gold marker
        c.setFillColor(YEL); c.rect(x, ytop - 4.6 * mm, 2.2 * mm, 4.2 * mm, stroke=0, fill=1)
        c.setFillColor(NAVY); c.setFont("SH", 10.5)
        c.drawString(x + 3.8 * mm, ytop - 3.8 * mm, title)
        c.setStrokeColor(LINE); c.setLineWidth(0.7); c.setFillColor(white)
        c.roundRect(x, ytop - h, w, h - TITLE_H + 1 * mm, 1.5 * mm, stroke=1, fill=0)
        return x + 3 * mm, ytop - TITLE_H - 1 * mm, w - 6 * mm, ytop - h + 2 * mm  # inner x, top, w, bottom

    def lines(ix, itop, iw, ibot, step=6.2 * mm):
        c.setStrokeColor(LINE); c.setLineWidth(0.5)
        n = max(1, int((itop - ibot) // step)); yy = itop - step
        while yy >= ibot - 0.1:
            c.line(ix, yy, ix + iw, yy); yy -= step

    def sublabel(ix, yy, text):
        c.setFont("PM", 8); c.setFillColor(NAVY); c.drawString(ix, yy, text)

    def table(ix, itop, iw, ibot, cols, fr, hdr_h=5.5 * mm, rows=None, step=6.2 * mm):
        c.setFillColor(LIGHT); c.rect(ix, itop - hdr_h, iw, hdr_h, stroke=0, fill=1)
        xs = [ix]
        for f in fr: xs.append(xs[-1] + iw * f)
        c.setFont("PM", 8); c.setFillColor(NAVY)
        for i, col in enumerate(cols):
            c.drawString(xs[i] + 1.5 * mm, itop - hdr_h + 1.7 * mm, col)
        space = itop - hdr_h - ibot
        n = rows or max(1, round(space / step))
        step = space / n
        yb_ = ibot
        c.setStrokeColor(LINE); c.setLineWidth(0.5)
        c.rect(ix, yb_, iw, itop - yb_, stroke=1, fill=0)
        for r in range(n):
            yy = itop - hdr_h - r * step
            c.line(ix, yy, ix + iw, yy)
        for xx in xs[1:-1]: c.line(xx, yb_, xx, itop)
        return yb_

    avail = y - FOOT
    SIGN_H = 22 * mm
    flex = avail - SIGN_H - 4 * GAP
    hA, hB, hC, hD = [flex * f for f in (0.27, 0.245, 0.255, 0.23)]
    half = (CW - GAP) / 2

    # Row A: staffing | safety
    ix, it, iw, ib = section(M, y, half, hA, "Staffing")
    yy = it - 4.5 * mm
    q = (iw - 4 * mm) / 2
    label_line(ix, yy, q, "Planned headcount", "PM", 8)
    label_line(ix + q + 4 * mm, yy, q, "Actual headcount", "PM", 8)
    yy -= 7 * mm
    sublabel(ix, yy, "Absences / late (name, reason)")
    rest = yy - ib
    ab_bot = yy - rest * 0.52
    lines(ix, yy + 1.5 * mm, iw, ab_bot + 1 * mm, 5.8 * mm)
    yy2 = ab_bot - 1.5 * mm
    sublabel(ix, yy2, "Overtime / cover arranged")
    lines(ix, yy2 + 1.5 * mm, iw, ib, 5.8 * mm)

    ix, it, iw, ib = section(M + half + GAP, y, half, hA, "Safety & incidents")
    yy = it - 3.5 * mm
    sublabel(ix, yy, "Incidents / near misses this shift")
    mid = yy - (yy - ib) * 0.52
    lines(ix, yy + 1.5 * mm, iw, mid + 1 * mm, 5.8 * mm)
    sublabel(ix, mid - 1.5 * mm, "Open safety actions / hazards to watch")
    lines(ix, mid, iw, ib, 5.8 * mm)
    y -= hA + GAP

    # Row B: production | equipment
    ix, it, iw, ib = section(M, y, half, hB, "Production / output vs target")
    tb = table(ix, it - 1 * mm, iw, ib + 8 * mm, ["Measure", "Target", "Actual", "Variance"],
               [0.40, 0.20, 0.20, 0.20], rows=3)
    lines(ix, tb, iw, ib, 5.8 * mm) if False else None
    label_line(ix, ib + 1.5 * mm, iw, "Reason for variance", "PM", 8)

    ix, it, iw, ib = section(M + half + GAP, y, half, hB, "Equipment & maintenance")
    tb = table(ix, it - 1 * mm, iw, ib, ["Equipment / asset", "Issue", "Job no. / status"],
               [0.32, 0.40, 0.28], step=5.8 * mm)
    y -= hB + GAP

    # Row C: open tasks full width
    ix, it, iw, ib = section(M, y, CW, hC, "Open tasks carried over")
    table(ix, it - 1 * mm, iw, ib, ["Task / action", "Owner", "Due", "Status"],
          [0.55, 0.18, 0.12, 0.15], step=6 * mm)
    y -= hC + GAP

    # Row D: quality | key messages
    ix, it, iw, ib = section(M, y, half, hD, "Quality or customer issues")
    lines(ix, it + 1 * mm, iw, ib)
    ix, it, iw, ib = section(M + half + GAP, y, half, hD, "Key messages for next shift")
    # numbered lines
    step = 6.2 * mm; yy = it + 1 * mm - step; n = 1
    c.setStrokeColor(LINE); c.setLineWidth(0.5)
    while yy >= ib:
        c.setFont("PB", 8.5); c.setFillColor(TEAL)
        c.drawString(ix, yy + 1.2 * mm, f"{n}")
        c.line(ix + 4 * mm, yy, ix + iw, yy); yy -= step; n += 1
    y -= hD + GAP

    # sign-off
    ix, it, iw, ib = section(M, y, CW, SIGN_H, "Handover sign-off")
    yy = it - 8 * mm
    q = (iw - 6 * mm) / 2
    for k, who in enumerate(["Outgoing leader", "Incoming leader"]):
        x0 = ix + k * (q + 6 * mm)
        label_line(x0, yy, q * 0.68, who + " signature", "PM", 8)
        label_line(x0 + q * 0.72, yy, q * 0.28, "Time", "PM", 8)

    # footer
    c.setFont("P", 7.5); c.setFillColor(GREY)
    c.drawCentredString(W / 2, M + 1 * mm, "© Leadership by Design · For use within one workplace")
    c.setFillColor(YEL); c.rect(W / 2 - 10 * mm, M + 4.2 * mm, 20 * mm, 0.6 * mm, stroke=0, fill=1)
    c.showPage(); c.save()

build(A4, "shift-handover-sheet-A4.pdf")
build(letter, "shift-handover-sheet-Letter.pdf")
