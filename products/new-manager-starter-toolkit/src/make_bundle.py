"""Build the New Manager Starter Toolkit bundle PDFs (A4 and US Letter), 9 pages each.

Run from anywhere:  python3 products/new-manager-starter-toolkit/src/make_bundle.py
Needs: pypdf (pip install pypdf; free, open source).

No re-rendering: the script joins the four built product PDFs, in this order:
  1. New Manager 30-60-90 Day Plan (3 pages)
  2. One-on-One Meeting Template (2 pages)
  3. Weekly Team Check-in (2 pages)
  4. Feedback Conversation Log (2 pages)
One combined file per paper size, because Etsy allows at most 5 files per listing.
Spec: logs/2026-10-06.md section 3 item 2 and logs/2026-10-05.md section 3.

Checks (asserted): each source has the expected page count, every page of an output file has
the same size (A4 595.28 x 841.89 pt or Letter 612 x 792 pt, within 1 pt), and each output
has exactly 9 pages. Rebuild this bundle whenever one of the four source PDFs changes.
"""
from pathlib import Path

from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "products" / "new-manager-starter-toolkit"
PARTS = (
    ("new-manager-30-60-90-day-plan", 3),
    ("one-on-one-meeting-template", 2),
    ("weekly-team-check-in", 2),
    ("feedback-conversation-log", 2),
)
SIZES = {"A4": (595.28, 841.89), "Letter": (612.0, 792.0)}


def build(size):
    w = PdfWriter()
    want_w, want_h = SIZES[size]
    for slug, n in PARTS:
        src = ROOT / "products" / slug / f"{slug}-{size}.pdf"
        r = PdfReader(str(src))
        assert len(r.pages) == n, f"{src.name} has {len(r.pages)} pages, expected {n}"
        for p in r.pages:
            pw, ph = float(p.mediabox.width), float(p.mediabox.height)
            assert abs(pw - want_w) <= 1 and abs(ph - want_h) <= 1, f"{src.name} page is {pw} x {ph} pt"
            w.add_page(p)
    assert len(w.pages) == 9, f"{size}: {len(w.pages)} pages, expected 9"
    w.add_metadata({
        "/Title": "New Manager Starter Toolkit",
        "/Author": "Kevin Britz / Leadership by Design",
        "/Subject": "30-60-90 Day Plan, One-on-One Meeting Template, Weekly Team Check-in and "
                    "Feedback Conversation Log for new managers",
    })
    out = OUT / f"new-manager-starter-toolkit-{size}.pdf"
    with open(out, "wb") as f:
        w.write(f)
    print(f"{out.name}: {len(w.pages)} pages, {size}")


if __name__ == "__main__":
    for s in ("A4", "Letter"):
        build(s)
