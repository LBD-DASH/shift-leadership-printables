"""Build the Shift Handover + Incident 2-Pack PDFs (A4 and US Letter), 3 pages each.

Run from anywhere:  python3 products/shift-handover-incident-2-pack/src/make_bundle.py
Needs: pypdf (pip install pypdf; free, open source).

No re-rendering: the script joins the two built product PDFs, in this order:
  1. Shift Handover Sheet v3 (1 page)
  2. Shift Incident Log (2 pages)
One combined file per paper size, because Etsy allows at most 5 files per listing.
Spec: logs/2026-10-09.md Next content section 2.

Checks (asserted): each source has the expected page count (1 + 2), every page of an
output file has the same size (A4 595.28 x 841.89 pt or Letter 612 x 792 pt, within 1 pt),
and each output has exactly 3 pages. Rebuild this bundle whenever one of the source PDFs changes.
"""
from pathlib import Path

from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "products" / "shift-handover-incident-2-pack"
PARTS = (
    ("shift-handover-sheet", 1),
    ("shift-incident-log", 2),
)
SIZES = {"A4": (595.28, 841.89), "Letter": (612.0, 792.0)}


def build(size):
    w = PdfWriter()
    want_w, want_h = SIZES[size]
    readers = []
    for slug, n in PARTS:
        src = ROOT / "products" / slug / f"{slug}-{size}.pdf"
        r = PdfReader(str(src))
        readers.append(r)
        assert len(r.pages) == n, f"{src.name} has {len(r.pages)} pages, expected {n}"
        for p in r.pages:
            pw, ph = float(p.mediabox.width), float(p.mediabox.height)
            assert abs(pw - want_w) <= 1 and abs(ph - want_h) <= 1, f"{src.name} page is {pw} x {ph} pt"
            w.add_page(p)
    assert len(w.pages) == 3, f"{size}: {len(w.pages)} pages, expected 3"
    widths = {round(float(p.mediabox.width), 2) for p in w.pages}
    heights = {round(float(p.mediabox.height), 2) for p in w.pages}
    assert len(widths) == 1 and len(heights) == 1, f"{size}: mixed page sizes {widths} x {heights}"
    w.add_metadata({
        "/Title": "Shift Handover + Incident 2-Pack",
        "/Author": "Kevin Britz / Leadership by Design",
        "/Subject": "Shift Handover Sheet and Shift Incident Log for supervisors",
    })
    out = OUT / f"shift-handover-incident-2-pack-{size}.pdf"
    with open(out, "wb") as f:
        w.write(f)
    print(f"{out.name}: {len(w.pages)} pages, {size}")
    return readers


if __name__ == "__main__":
    for s in ("A4", "Letter"):
        build(s)
