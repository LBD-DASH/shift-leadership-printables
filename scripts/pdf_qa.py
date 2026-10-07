#!/usr/bin/env python3
"""LBDShopSA PDF QA runner: Critical checks that approve or block a product for Etsy publish.

Status: APPROVED_FOR_PUBLISH only if all Critical file and product checks PASS.
Checklist and check ids (C01 to C09, W01 to W03, P01 to P04): docs/PDF_QA_CHECKLIST.md.
Does not publish anything. Writes a CSV (default logs/qa/YYYY-MM-DD-pdf-qa.csv) and a summary.

Run from the repo root:  python3 scripts/pdf_qa.py
Needs: pypdf and pdfminer.six (pip install pypdf pdfminer.six; both free, open source).
Exit code 1 if any file or product is BLOCKED.
Origin: Grok Bot's box runner /workspace/etsy-qa/run_pdf_qa.py (2026-10-06), made repo-relative.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

from pypdf import PdfReader
from pypdf.generic import IndirectObject

try:
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import (
        LTAnno,
        LTChar,
        LTCurve,
        LTLine,
        LTRect,
        LTTextBox,
        LTTextLine,
        LTFigure,
        LTImage,
    )
except ImportError as e:  # pragma: no cover
    print("pdfminer.six required:", e, file=sys.stderr)
    sys.exit(2)

PT_PER_MM = 72.0 / 25.4
A4 = (595.28, 841.89)
LETTER = (612.0, 792.0)
SIZE_TOL_PT = 2.0
MARGIN_MM = 12.0
MARGIN_TOL_MM = 0.5
ROW_MIN_MM = 8.0
ROW_TOL_MM = 0.5
MIN_BYTES = 2 * 1024
MAX_BYTES = 20 * 1024 * 1024

MIN_PAGES = {
    "shift-handover-sheet": 1,
    "one-on-one-meeting-template": 2,
    "shift-incident-log": 2,
    "new-manager-30-60-90-day-plan": 3,
    "feedback-conversation-log": 2,
    "weekly-team-check-in": 2,
    "new-manager-starter-toolkit": 9,
}

STANDARD_FONTS = {
    "Helvetica",
    "Helvetica-Bold",
    "Helvetica-Oblique",
    "Helvetica-BoldOblique",
    "Times-Roman",
    "Times-Bold",
    "Times-Italic",
    "Times-BoldItalic",
    "Courier",
    "Courier-Bold",
    "Courier-Oblique",
    "Courier-BoldOblique",
    "Symbol",
    "ZapfDingbats",
}


def mm_to_pt(mm: float) -> float:
    return mm * PT_PER_MM


def pt_to_mm(pt: float) -> float:
    return pt / PT_PER_MM


def resolve(obj):
    while isinstance(obj, IndirectObject):
        obj = obj.get_object()
    return obj


def infer_format(path: Path) -> str | None:
    name = path.name
    if re.search(r"(?i)[-_]a4\.pdf$", name) or name.upper().endswith("-A4.PDF"):
        return "A4"
    if re.search(r"(?i)[-_]letter\.pdf$", name):
        return "Letter"
    return None


def product_slug_from_path(path: Path, products_root: Path) -> str:
    try:
        rel = path.relative_to(products_root)
        return rel.parts[0]
    except Exception:
        stem = path.stem
        stem = re.sub(r"(?i)[-_](a4|letter)$", "", stem)
        return stem


def walk_layout(layout):
    stack = [layout]
    while stack:
        el = stack.pop()
        yield el
        if isinstance(el, (LTTextBox, LTTextLine, LTFigure)) or (
            hasattr(el, "__iter__")
            and not isinstance(el, (LTChar, LTAnno, str, bytes))
        ):
            try:
                for child in el:
                    stack.append(child)
            except TypeError:
                pass


def content_bbox_and_rows(pdf_path: Path):
    """Return per-page content bbox (x0,y0,x1,y1) in PDF pts and row-gap mm list."""
    pages_info = []
    for layout in extract_pages(str(pdf_path)):
        pw, ph = layout.bbox[2], layout.bbox[3]
        min_x, min_y = pw, ph
        max_x, max_y = 0.0, 0.0
        has_content = False
        hlines = []  # (y, x0, x1)
        outside_chars = 0
        char_count = 0

        for el in walk_layout(layout):
            if isinstance(el, LTChar):
                char_count += 1
                x0, y0, x1, y1 = el.bbox
                has_content = True
                min_x, min_y = min(min_x, x0), min(min_y, y0)
                max_x, max_y = max(max_x, x1), max(max_y, y1)
                if x0 < -0.5 or y0 < -0.5 or x1 > pw + 0.5 or y1 > ph + 0.5:
                    outside_chars += 1
            elif isinstance(el, (LTLine, LTRect, LTCurve)):
                x0, y0, x1, y1 = el.bbox
                # stroked content
                if abs(x1 - x0) > 0.5 or abs(y1 - y0) > 0.5:
                    has_content = True
                    min_x, min_y = min(min_x, x0), min(min_y, y0)
                    max_x, max_y = max(max_x, x1), max(max_y, y1)
                # horizontal write/table rules (columns OK at ≥25% page width)
                height = abs(y1 - y0)
                width = abs(x1 - x0)
                is_line = isinstance(el, LTLine)
                is_hairline_rect = isinstance(el, LTRect) and height <= 1.2
                if (is_line or is_hairline_rect) and height <= 2.0 and width >= 0.25 * pw:
                    y_mid = (y0 + y1) / 2.0
                    hlines.append((y_mid, min(x0, x1), max(x0, x1)))
            elif isinstance(el, LTImage):
                x0, y0, x1, y1 = el.bbox
                has_content = True
                min_x, min_y = min(min_x, x0), min(min_y, y0)
                max_x, max_y = max(max_x, x1), max(max_y, y1)

        if not has_content:
            bbox = None
        else:
            bbox = (min_x, min_y, max_x, max_y)

        # Row gaps: group rules by column (similar x0/x1), require ≥3 aligned
        # lines, keep regular write-in steps (4.5 to 20 mm). Avoids mixing two
        # columns or one-off section spacers with true handwriting rows.
        gaps_mm = []
        if len(hlines) >= 3:
            clusters = []
            x_tol = mm_to_pt(3.0)
            for y, x0, x1 in sorted(hlines, key=lambda t: (t[1], t[2], t[0])):
                placed = False
                for cluster in clusters:
                    _, cx0, cx1 = cluster[0]
                    if abs(x0 - cx0) <= x_tol and abs(x1 - cx1) <= x_tol:
                        cluster.append((y, x0, x1))
                        placed = True
                        break
                if not placed:
                    clusters.append([(y, x0, x1)])
            for cluster in clusters:
                if len(cluster) < 3:
                    continue
                ys = []
                for y, _, _ in sorted(cluster, key=lambda t: t[0]):
                    if not ys or abs(y - ys[-1]) > mm_to_pt(1.0):
                        ys.append(y)
                if len(ys) < 3:
                    continue
                raw = [pt_to_mm(b - a) for a, b in zip(ys, ys[1:])]
                cand = [g for g in raw if 4.5 <= g <= 20.0]
                if len(cand) < 2:
                    continue
                med = sorted(cand)[len(cand) // 2]
                if med <= 0:
                    continue
                regular = [g for g in cand if abs(g - med) / med <= 0.25]
                gaps_mm.extend(regular if len(regular) >= 2 else cand)

        pages_info.append(
            {
                "bbox": bbox,
                "page_w": pw,
                "page_h": ph,
                "gaps_mm": gaps_mm,
                "outside_chars": outside_chars,
                "char_count": char_count,
                "hline_count": len(hlines),
            }
        )
    return pages_info


def fonts_embedded(reader: PdfReader) -> tuple[bool, str]:
    missing = []
    seen = set()
    for page in reader.pages:
        resources = resolve(page.get("/Resources")) or {}
        font_dict = resolve(resources.get("/Font")) or {}
        if not isinstance(font_dict, dict):
            continue
        for _name, font_ref in font_dict.items():
            font = resolve(font_ref)
            if not isinstance(font, dict):
                continue
            base = str(resolve(font.get("/BaseFont")) or "")
            base_clean = base.lstrip("/")
            # strip subset prefix ABCDEF+
            if "+" in base_clean:
                base_clean = base_clean.split("+", 1)[1]
            key = base_clean
            if key in seen:
                continue
            seen.add(key)
            if key in STANDARD_FONTS or base_clean in STANDARD_FONTS:
                continue
            descendant = resolve(font.get("/DescendantFonts"))
            descriptor = resolve(font.get("/FontDescriptor"))
            embedded = False
            if descriptor:
                for k in ("/FontFile", "/FontFile2", "/FontFile3"):
                    if descriptor.get(k) is not None:
                        embedded = True
                        break
            if not embedded and descendant:
                # CID fonts
                try:
                    first = resolve(descendant[0]) if len(descendant) else None
                except Exception:
                    first = None
                if first:
                    desc2 = resolve(first.get("/FontDescriptor"))
                    if desc2:
                        for k in ("/FontFile", "/FontFile2", "/FontFile3"):
                            if desc2.get(k) is not None:
                                embedded = True
                                break
            # ReportLab often embeds via FontDescriptor on Type0/TrueType
            if not embedded:
                # If BaseFont has subset prefix in original, usually embedded
                if "+" in base.lstrip("/"):
                    # still require descriptor file if present; ReportLab embeds
                    if descriptor:
                        for k in ("/FontFile", "/FontFile2", "/FontFile3"):
                            if descriptor.get(k) is not None:
                                embedded = True
                                break
                if not embedded:
                    missing.append(base or str(_name))
    if missing:
        return False, "missing embed: " + ", ".join(missing[:8])
    return True, "ok"


def check_file(path: Path, products_root: Path) -> dict:
    slug = product_slug_from_path(path, products_root)
    fmt = infer_format(path)
    size = path.stat().st_size
    fails = []
    warns = []
    details = {
        "path": str(path),
        "product": slug,
        "format": fmt or "?",
        "file_size_bytes": size,
        "pages": "",
        "page_size": "",
        "min_margin_mm": "",
        "min_row_gap_mm": "",
        "title": "",
        "author": "",
    }

    # C08 size
    if size < MIN_BYTES or size > MAX_BYTES:
        fails.append(f"C08 file size {size} bytes out of range")

    # C01 open
    try:
        reader = PdfReader(str(path))
    except Exception as e:
        fails.append(f"C01 cannot open PDF: {e}")
        details["status"] = "BLOCKED"
        details["fail_reasons"] = "; ".join(fails)
        details["warn_reasons"] = ""
        details["checks_pass"] = "C01=FAIL"
        return details

    # C02 encryption
    if reader.is_encrypted:
        fails.append("C02 encrypted/passworded")
        try:
            reader.decrypt("")
        except Exception:
            details["status"] = "BLOCKED"
            details["fail_reasons"] = "; ".join(fails)
            details["warn_reasons"] = ""
            details["checks_pass"] = "C02=FAIL"
            return details

    n_pages = len(reader.pages)
    details["pages"] = n_pages

    # C03 page count
    if n_pages < 1:
        fails.append("C03 empty PDF (0 pages)")
    min_expected = MIN_PAGES.get(slug)
    if min_expected is not None and n_pages < min_expected:
        fails.append(f"C03 pages {n_pages} < expected min {min_expected} for {slug}")

    # C04 page size vs filename
    sizes = []
    for i, page in enumerate(reader.pages):
        mb = page.mediabox
        w, h = float(mb.width), float(mb.height)
        sizes.append((w, h))
        if fmt == "A4":
            if abs(w - A4[0]) > SIZE_TOL_PT or abs(h - A4[1]) > SIZE_TOL_PT:
                # allow landscape swap? printables are portrait
                fails.append(
                    f"C04 page {i+1} size {w:.2f}x{h:.2f} not A4 ({A4[0]}x{A4[1]})"
                )
        elif fmt == "Letter":
            if abs(w - LETTER[0]) > SIZE_TOL_PT or abs(h - LETTER[1]) > SIZE_TOL_PT:
                fails.append(
                    f"C04 page {i+1} size {w:.2f}x{h:.2f} not Letter ({LETTER[0]}x{LETTER[1]})"
                )
        else:
            fails.append("C04 cannot infer A4/Letter from filename")
    if sizes:
        details["page_size"] = f"{sizes[0][0]:.2f}x{sizes[0][1]:.2f}"

    # text extract for C06
    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            texts.append("")
    full_text = "\n".join(texts).strip()
    if not full_text:
        fails.append("C06 no extractable text")

    # C07 fonts
    ok_fonts, font_msg = fonts_embedded(reader)
    if not ok_fonts:
        fails.append(f"C07 {font_msg}")

    # metadata W02
    meta = reader.metadata or {}
    title = (meta.title or "") if meta else ""
    author = (meta.author or "") if meta else ""
    details["title"] = title or ""
    details["author"] = author or ""
    if not title:
        warns.append("W02 missing PDF title")
    if not author or not re.search(r"(?i)(lbd|leadership|kevin|britz|design)", author):
        warns.append("W02 author should identify LBD / Kevin Britz")

    # C05 margins + C06 clip + C09 rows via pdfminer
    try:
        layout_pages = content_bbox_and_rows(path)
    except Exception as e:
        fails.append(f"C05/C09 layout parse failed: {e}")
        layout_pages = []

    min_margins = []
    min_gaps = []
    row_measured = False
    for i, info in enumerate(layout_pages):
        bbox = info["bbox"]
        pw, ph = info["page_w"], info["page_h"]
        if bbox is None:
            fails.append(f"C05 page {i+1} no measurable content")
            continue
        x0, y0, x1, y1 = bbox
        left = pt_to_mm(x0)
        bottom = pt_to_mm(y0)
        right = pt_to_mm(pw - x1)
        top = pt_to_mm(ph - y1)
        m = min(left, bottom, right, top)
        min_margins.append(m)
        limit = MARGIN_MM - MARGIN_TOL_MM
        if m < limit:
            fails.append(
                f"C05 page {i+1} margin {m:.2f}mm < {MARGIN_MM}mm (L{left:.1f} B{bottom:.1f} R{right:.1f} T{top:.1f})"
            )
        if info["outside_chars"] > 0:
            fails.append(
                f"C06 page {i+1} {info['outside_chars']} glyphs outside mediabox"
            )
        gaps = info["gaps_mm"]
        if gaps:
            row_measured = True
            mg = min(gaps)
            min_gaps.append(mg)
            if mg < ROW_MIN_MM - ROW_TOL_MM:
                fails.append(
                    f"C09 page {i+1} min write-row gap {mg:.2f}mm < {ROW_MIN_MM}mm"
                )

    if min_margins:
        details["min_margin_mm"] = f"{min(min_margins):.2f}"
    if min_gaps:
        details["min_row_gap_mm"] = f"{min(min_gaps):.2f}"
    if not row_measured:
        warns.append("W03 C09 could not auto-measure handwriting rows, manual check")

    # W01 is listing-level; note as warning reminder once per file
    warns.append("W01 confirm AI disclosure on Etsy listing copy")

    status = "APPROVED_FOR_PUBLISH" if not fails else "BLOCKED"
    details["status"] = status
    details["fail_reasons"] = "; ".join(fails)
    details["warn_reasons"] = "; ".join(warns)
    details["checks_pass"] = (
        "CRITICAL_PASS" if not fails else "CRITICAL_FAIL"
    )
    return details


def check_products(products_root: Path) -> list[dict]:
    rows = []
    product_dirs = sorted(
        [p for p in products_root.iterdir() if p.is_dir() and not p.name.startswith(".")]
    )
    if not product_dirs:
        # maybe products_root itself is a single product? or flat pdfs
        pdfs = sorted(products_root.glob("*.pdf"))
        if pdfs:
            product_dirs = [products_root]

    file_rows_by_product: dict[str, list[dict]] = defaultdict(list)

    for pdir in product_dirs:
        pdfs = sorted(pdir.rglob("*.pdf")) if pdir != products_root else sorted(
            products_root.glob("*.pdf")
        )
        # Prefer direct children
        direct = sorted(pdir.glob("*.pdf"))
        if direct:
            pdfs = direct
        for pdf in pdfs:
            row = check_file(pdf, products_root)
            rows.append(row)
            file_rows_by_product[row["product"]].append(row)

    # Product-level P01 to P04
    for slug, frows in file_rows_by_product.items():
        formats = {r["format"] for r in frows}
        a4 = [r for r in frows if r["format"] == "A4"]
        letter = [r for r in frows if r["format"] == "Letter"]
        prod_fails = []
        prod_warns = []
        # Assume listings claim both sizes for all SLP products
        if "A4" not in formats or "Letter" not in formats:
            prod_fails.append("P01 missing A4 or Letter pair")
        if a4 and letter:
            try:
                if int(a4[0]["pages"]) != int(letter[0]["pages"]):
                    prod_fails.append(
                        f"P02 page count mismatch A4={a4[0]['pages']} Letter={letter[0]['pages']}"
                    )
            except Exception:
                prod_fails.append("P02 cannot compare page counts")
            # P03: sizes already checked per file; flag if any C04 fail
            if any("C04" in (r["fail_reasons"] or "") for r in a4 + letter):
                prod_fails.append("P03 size/name mismatch (see C04)")
        # P04 naming
        for r in frows:
            name = Path(r["path"]).name
            expect_a4 = f"{slug}-A4.pdf"
            expect_letter = f"{slug}-Letter.pdf"
            if r["format"] == "A4" and name != expect_a4:
                prod_warns.append(f"P04 expected {expect_a4} got {name}")
            if r["format"] == "Letter" and name != expect_letter:
                prod_warns.append(f"P04 expected {expect_letter} got {name}")

        # attach product check to each file row
        for r in frows:
            if prod_fails:
                r["status"] = "BLOCKED"
                extra = "; ".join(prod_fails)
                r["fail_reasons"] = (
                    (r["fail_reasons"] + "; " if r["fail_reasons"] else "") + extra
                )
                r["checks_pass"] = "CRITICAL_FAIL"
            if prod_warns:
                r["warn_reasons"] = (
                    (r["warn_reasons"] + "; " if r["warn_reasons"] else "")
                    + "; ".join(prod_warns)
                )
        file_blocked = any(r["status"] == "BLOCKED" for r in frows)
        if file_blocked and not any("file-level Critical failure" in x for x in prod_fails):
            prod_fails.append("file-level Critical failure (see per-file rows)")
        # summary product row
        rows.append(
            {
                "path": f"[PRODUCT] {slug}",
                "product": slug,
                "format": "PAIR",
                "file_size_bytes": "",
                "pages": "",
                "page_size": "",
                "min_margin_mm": "",
                "min_row_gap_mm": "",
                "title": "",
                "author": "",
                "status": "BLOCKED" if (prod_fails or file_blocked) else "APPROVED_FOR_PUBLISH",
                "fail_reasons": "; ".join(prod_fails),
                "warn_reasons": "; ".join(prod_warns),
                "checks_pass": "CRITICAL_FAIL" if (prod_fails or file_blocked) else "CRITICAL_PASS",
            }
        )
    return rows


def main():
    ap = argparse.ArgumentParser(description="LBDShopSA PDF QA")
    ap.add_argument(
        "--products-path",
        default=str(Path(__file__).resolve().parents[1] / "products"),
        help="Path to products/ directory (one subfolder per product)",
    )
    ap.add_argument(
        "--out",
        default="",
        help="CSV output path (default logs/qa/YYYY-MM-DD-pdf-qa.csv in the repo)",
    )
    args = ap.parse_args()
    products_root = Path(args.products_path).resolve()
    if not products_root.is_dir():
        print(f"Not a directory: {products_root}", file=sys.stderr)
        sys.exit(1)

    rows = check_products(products_root)
    today = dt.date.today().isoformat()
    out = Path(args.out) if args.out else Path(__file__).resolve().parents[1] / "logs" / "qa" / f"{today}-pdf-qa.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    for r in rows:
        p = str(r.get("path") or "")
        r["file"] = Path(p).name if p and not p.startswith("[PRODUCT]") else p
        if p and not p.startswith("[PRODUCT]"):
            try:  # repo-relative paths in the CSV, so reports are the same on every machine
                r["path"] = str(Path(p).resolve().relative_to(products_root.parent))
            except ValueError:
                pass
        fails = r.get("fail_reasons") or ""
        warns = r.get("warn_reasons") or ""
        bits = []
        if r.get("pages") not in ("", None):
            bits.append(f"pages={r['pages']}")
        if r.get("page_size"):
            bits.append(f"size={r['page_size']}")
        if r.get("min_margin_mm") not in ("", None):
            bits.append(f"margin_mm={r['min_margin_mm']}")
        if r.get("min_row_gap_mm") not in ("", None):
            bits.append(f"row_gap_mm={r['min_row_gap_mm']}")
        if fails:
            bits.append("FAIL:" + fails)
        if warns:
            bits.append("WARN:" + warns)
        if not fails and r.get("checks_pass") == "CRITICAL_PASS":
            bits.append("all Critical PASS")
        r["checks"] = " | ".join(bits)
        r["pass_fail"] = "PASS" if r.get("status") == "APPROVED_FOR_PUBLISH" else "FAIL"
        r["overall"] = r.get("status")

    fields = [
        "product",
        "file",
        "checks",
        "pass_fail",
        "overall",
        "path",
        "format",
        "file_size_bytes",
        "pages",
        "page_size",
        "min_margin_mm",
        "min_row_gap_mm",
        "title",
        "author",
        "fail_reasons",
        "warn_reasons",
        "checks_pass",
    ]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    approved = sum(1 for r in rows if r["status"] == "APPROVED_FOR_PUBLISH" and not str(r["path"]).startswith("[PRODUCT]"))
    blocked = sum(1 for r in rows if r["status"] == "BLOCKED" and not str(r["path"]).startswith("[PRODUCT]"))
    prod_ok = sum(1 for r in rows if str(r["path"]).startswith("[PRODUCT]") and r["status"] == "APPROVED_FOR_PUBLISH")
    prod_bad = sum(1 for r in rows if str(r["path"]).startswith("[PRODUCT]") and r["status"] == "BLOCKED")

    # Top Critical failures
    from collections import Counter
    fail_counter = Counter()
    for r in rows:
        if str(r["path"]).startswith("[PRODUCT]"):
            continue
        for part in (r.get("fail_reasons") or "").split("; "):
            part = part.strip()
            if not part:
                continue
            # normalize to check id prefix
            key = part.split()[0] if part.split()[0].startswith("C") or part.split()[0].startswith("P") else part
            # better: extract C0x / P0x
            import re as _re
            m = _re.match(r"(C\d+|P\d+)", part)
            key = m.group(1) if m else part[:60]
            fail_counter[key] += 1
            fail_counter[part[:100]] += 0  # keep detailed separately below
    detail_fails = Counter()
    for r in rows:
        if str(r["path"]).startswith("[PRODUCT]"):
            continue
        for part in (r.get("fail_reasons") or "").split("; "):
            part = part.strip()
            if part:
                detail_fails[part] += 1

    summary = out.parent / f"{today}-pdf-qa-summary.txt"
    with open(summary, "w", encoding="utf-8") as sf:
        sf.write(f"report={out.name}\n")
        sf.write(f"files_approved={approved}\n")
        sf.write(f"files_blocked={blocked}\n")
        sf.write(f"products_approved={prod_ok}\n")
        sf.write(f"products_blocked={prod_bad}\n")
        sf.write("top_failures:\n")
        for msg, cnt in detail_fails.most_common(10):
            sf.write(f"  {cnt}x {msg}\n")
        sf.write("by_product:\n")
        for r in rows:
            if str(r["path"]).startswith("[PRODUCT]"):
                sf.write(f"  {r['overall']}\t{r['product']}\t{r.get('fail_reasons','')}\n")

    print(f"Wrote {out}")
    print(f"Summary {summary}")
    print(f"Files: APPROVED_FOR_PUBLISH={approved} BLOCKED={blocked}")
    print(f"Products: APPROVED_FOR_PUBLISH={prod_ok} BLOCKED={prod_bad}")
    if detail_fails:
        print("Top Critical failures:")
        for msg, cnt in detail_fails.most_common(10):
            print(f"  {cnt}x {msg}")
    else:
        print("Top Critical failures: none")
    # exit 1 if any blocked
    if blocked or prod_bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
