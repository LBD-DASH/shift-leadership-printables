# PDF QA checklist (go-live gate for LBDShopSA)

Kevin's standing rules (6 Oct 2026): (1) a thorough PDF QA check passes before any listing goes live; (2) a listing is auto-approved for publish only when that QA passes; (3) money-back guarantee if anything is wrong with a sold PDF. Passing QA does not publish anything: listings stay drafts until Kevin's final yes, and only Kevin lists in Etsy.

This file is model-agnostic. Any agent or person (Claude, ChatGPT, Grok Bot, Kevin) can run it.

## How to run

```
pip install pypdf pdfminer.six        # free, open source
python3 scripts/pdf_qa.py             # checks every products/<slug>/<slug>-A4.pdf and -Letter.pdf
```

Output: `logs/qa/YYYY-MM-DD-pdf-qa.csv` (one row per file plus one PAIR row per product) and `logs/qa/YYYY-MM-DD-pdf-qa-summary.txt`. Exit code 1 if anything is BLOCKED. Re-run after any PDF changes, and paste the summary into that day's log.

Also run by hand, once per product, before Kevin lists it (poppler-utils): `pdfinfo` (pages, page size, not encrypted), `pdffonts` (every font `emb yes`), `pdftotext` (brand line present, no em or en dashes), and look at a 75 dpi render of every page (`pdftoppm -r 75 -png`).

## Result rule

| Status | Rule |
|---|---|
| APPROVED_FOR_PUBLISH | Every Critical check passes for both files and for the product pair. |
| BLOCKED | Any Critical check fails. Record the check id and reason in the day's log. Fix, rebuild, re-run. |

Warnings do not block, but fix them before the listing goes live.

## Per-file checks (each `<slug>-A4.pdf` and `<slug>-Letter.pdf`)

| ID | Severity | Check | Pass |
|---|---|---|---|
| C01 | Critical | Opens as a PDF | pypdf and pdfinfo read it |
| C02 | Critical | Not encrypted | `Encrypted: no` |
| C03 | Critical | Page count | At least the expected count (Handover 1, One-on-One 2, Incident Log 2, 30-60-90 3, Feedback Log 2, Weekly Check-in 2, Starter Toolkit 9) and equal to the listing's "WHAT YOU GET" |
| C04 | Critical | Page size | A4 files 595.28 x 841.89 pt, Letter files 612 x 792 pt (within 2 pt) on every page; file name matches size |
| C05 | Critical | Margins | Content stays 12 mm from every edge (0.5 mm tolerance for stroke width; the generators assert 12 mm exactly) |
| C06 | Critical | Text not cut off | Text extracts; no glyph outside the page box |
| C07 | Critical | Fonts embedded | Every font embedded or subset-embedded |
| C08 | Critical | File size | 2 KB to 20 MB (Etsy's per-file limit) |
| C09 | Critical | Handwriting rows | Stacked write-in rules and table rows at least 8 mm apart. The runner measures rules at least 25% of page width; the product scripts assert every row at 8 mm or more. A thin legend strip under a table header is not a write-in row (see logs/2026-10-07.md for the 30-60-90 page 3 note) |
| W01 | Warning | AI disclosure | The listing copy has Kevin's AI disclosure line, or he has said AI was not used |
| W02 | Warning | Metadata | PDF title set; author "Kevin Britz / Leadership by Design" |
| W03 | Warning | Manual row check | If C09 could not measure rows, check a print preview by eye |

## Product checks

| ID | Severity | Check |
|---|---|---|
| P01 | Critical | Both A4 and Letter files exist when the listing says "A4 & Letter" |
| P02 | Critical | A4 and Letter have the same page count |
| P03 | Critical | A4 file is A4 and Letter file is Letter (no swap) |
| P04 | Warning | Naming: `products/<slug>/<slug>-A4.pdf` and `-Letter.pdf` |

## Listing-level checks (by hand, before Kevin's final yes)

- [ ] Brand line on every page: `Designed by Kevin Britz / Leadership by Design · leadershipbydesign.co · For use within one workplace`.
- [ ] Listing images in `etsy/<key>/` were rendered from the current PDFs (re-run `etsy/src/make_product_images.py <key>` after any PDF change).
- [ ] Title up to 140 characters, exactly 13 tags of up to 20 characters, listing type Digital files, price inside the USD 3 to 5 single or USD 9 to 15 bundle guide (`docs/ETSY_SETUP_CHECKLIST.md`).
- [ ] "WHAT YOU GET" file names, sizes and page counts match the files.
- [ ] AI disclosure line filled in (Kevin's wording), and the money-back line below is in the description.
- [ ] No em or en dashes, no invented reviews, stars or sales counts.

## Money-back line for listings (Kevin's rule 3)

```
RETURNS AND FAULTY FILES
Digital downloads can't be returned for a change of mind. If anything is wrong with your PDF (it won't download or open, the page size is wrong, a page is missing or text is unreadable), message me with your order number and I'll refund you in full. You can keep the file.
```
