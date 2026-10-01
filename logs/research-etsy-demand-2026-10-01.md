# Etsy demand check: next 3 printables for LBDShopSA (2026-10-01)

Date of research: Thursday 1 Oct 2026, roughly 03:30 to 04:00 SAST. Done by the Printables agent (Grok Bot executor). Read-only research: nothing was listed, published, bought, favourited or added to a basket, and no account was signed in to anywhere.

Earlier baseline: `logs/research-etsy-demand.md` (27 Sep 2026, live Etsy browsing from South Africa).

---

## 1. How the evidence was gathered, and how far to trust it

**Etsy itself could not be read directly today.** Every direct route to etsy.com returned a DataDome bot check ("Please enable JS and disable any ad blocker" / captcha-delivery.com):
- `curl` on search, market, shop and listing pages: HTTP 403.
- WebFetch on search, market and listing pages: timed out.
- Headless Chrome and a normal (headed) Chrome window with a fresh, signed-out profile: captcha page.
- A public reader proxy (r.jina.ai): "page maybe requiring CAPTCHA".
- Internet Archive (Wayback) was offline ("Temporarily Offline").
The captcha was not solved or bypassed. So **no live Etsy result count was visible today** for any term.

**What was used instead (all indirect, labelled per row):**
- **[IDX]** Search-engine index snapshots of real Etsy pages (listing pages and etsy.com/market pages), returned as page text by the WebSearch tool. These are the actual Etsy page text at the time the search engine crawled it. Crawl date is not shown. Prices are in whatever currency the crawler saw (GBP, EUR, PLN, CAD, NZD, AUD, SEK or USD). On Etsy search and market cards, the number in brackets, for example "(492)", is the **shop's** total review count, not the listing's.
- **[SUM]** Figures that appeared only in the WebSearch tool's machine-written summary of a listing page, not in the quoted page text. Lower confidence. Treat as "probably right, check before relying on it".
- **[MW]** MakerWords (makerwords.com), a public third-party Etsy keyword and shop research site (no sign-in needed). Pages state "As of October 2026". Their "sales" figure is **shop-level** total sales, not sales of that listing. Favourites are listing-level. Prices are USD. Note: several MakerWords keyword pages returned obvious placeholder data (0 shops, generic titles such as "Eco-Friendly Organic Product", averages like $2,666). Those pages were **discarded**: 1-on-1-meeting, 1-on-1-meeting-template, meeting-agenda, meeting-notes, huddle, huddle-board, onboarding-checklist, onboarding-template, pto-tracker, hr-templates, rn-handoff-sheet, cna-shift-report and others. Only pages with real shop data were used.
- **[LOG]** Kevin's own repo baseline from 27 Sep 2026 (`logs/research-etsy-demand.md`), which was a live Etsy session.

**Titles.** Etsy titles use the pipe character as a separator. In the tables below, pipes are shown as commas so the tables render; wording is otherwise as shown.

**Currency conversion.** Non-USD prices are converted to USD at the Banque de France reference rates for 30 Sep 2026 (EUR 1 = USD 1.1355; GBP 0.8546, PLN 4.3690, CAD 1.6105, NZD 2.0115, AUD 1.6297, SEK 11.3310 per EUR). That gives roughly GBP 1 = USD 1.33, EUR 1 = USD 1.14, PLN 1 = USD 0.26, CAD 1 = USD 0.71, NZD 1 = USD 0.56, AUD 1 = USD 0.70, SEK 1 = USD 0.10. Etsy's localised prices can include VAT/GST, so converted USD figures are approximate ("~").
Source: https://www.banque-france.fr/en/statistics/rates-and-prices/exchange-rates-daily-parities-2026-09-30

---

## 2. Evidence by candidate

### 2.1 One-on-One Meeting Template (already drafted) - PICK

Search terms: "one on one meeting template", "1:1 manager meeting template", "one on one meeting".
Result count: not visible today (Etsy blocked). [LOG] 27 Sep live count: "1,000+" (Etsy's display cap), top-3 listings had 11, 2 and 1 reviews.

| # | Shop | Listing title (as shown) | Price | Reviews / favourites / sales | Source | URL |
|---|---|---|---|---|---|---|
| 1 | HREducationEdge | Manager One-on-One Meeting Agenda Template: HR Forms, Human Resource Documents, Google Docs & Sheets | USD 5.00 | 400 favourites on the listing; shop 26.5K sales, 1.8K reviews, 4.8 rating | [MW] | https://makerwords.com/shop/hreducationedge (shop: https://www.etsy.com/shop/HREducationEdge) |
| 2 | TheFocusedForm | One on One Meeting notes, Printable Manager Template, Team Check-in form, PDF Download | USD 3.29 | 1 review (5.0), 26 favourites, "Listed on Sep 2, 2026", 1 PDF | [IDX] | https://www.etsy.com/listing/4330862859/one-on-one-meeting-notes-printable |
| 3 | ManagerMindMappingCo (Etsy ad) | Printable, Fillable, One-on-One Meeting Template, Manager Coaching Agenda PDF | GBP 5.89 (~USD 7.83); also seen as EUR 7.11 (~USD 8.07) and PLN 30.32 (~USD 7.88) | shop (2) reviews | [IDX] | https://www.etsy.com/market/1%3A1_manager_meeting_template and https://www.etsy.com/market/one_on_one_meeting |
| 4 | shop not shown in snippet | Manager 1-On-1 Meeting Agenda Template, Supervisor One-on-One Meeting Agenda, Managerial Meeting Format, Staff Meeting, Project Meeting | EUR 3.05 (~USD 3.46) | shop (492) reviews in one snapshot, (472) in another | [IDX] | https://www.etsy.com/market/one_on_one_meeting |
| 5 | shop not shown in snippet | 1-On-1 Manager Meeting Agenda Template 1:1 Meeting Format Managerial Meeting Agenda Team Leader Agenda Template Professional Meeting Agenda | sale price garbled in snippet; original EUR 5.68 (~USD 6.45), shown "48% off" | shop (531) reviews | [IDX] | https://www.etsy.com/market/one_on_one_meeting |
| 6 | shop not shown in snippet | One on One Meeting Template for Microsoft and Google, Staff Meeting Agenda Template, Leadership Meeting Agenda, 1 on 1 meeting agenda, Touch Base Meeting Agenda | PLN 9.69 (~USD 2.52) | shop (50) reviews | [IDX] | https://www.etsy.com/market/one_on_one_meeting_template |
| 7 | watercolortheme | meeting agenda template, one on one meeting template (MS Word + Google Docs, US Letter) | CA$ 3.90 (~USD 2.75) [SUM] | 1 item review, 4.0 [SUM]; shop 12.8K sales, 664 reviews [MW] | [IDX] + [SUM] + [MW] | https://www.etsy.com/ca/listing/1794573573/meeting-agenda-templatemeeting-agenda |
| 8 | 37DesignClub | 1:1 Meeting Agenda Template, Simple Meeting Template, One on One Meeting Agenda, Meeting Agenda Word | SEK 19.39 (~USD 1.94) [SUM] | shop 383 sales, 31 reviews [MW] | [SUM] + [MW] | https://www.etsy.com/listing/1519686003/11-meeting-agenda-template-simple |

Read: the strongest demand signal of everything checked. Several established shops (hundreds to 1.8K shop reviews) sell 1:1 templates, and one listing has 400 favourites. Most competitors are editable Word/Google Docs files; print-and-write PDFs are fewer (TheFocusedForm, ManagerMindMappingCo). Price band for singles: about USD 2 to 8, with the big-shop leader at USD 5.00.
Not verified: the 27 Sep note that JPSDigitalPages ranked top-3 with a 1:1 dashboard. MakerWords shows JPSDigitalPages (9.7K sales, 696 reviews) but its tracked top listings are an Employee Schedule Template (USD 24.00, 296 favourites), a Net Worth Tracker and a Macro Tracker, so the 1:1 listing could not be re-confirmed today.

### 2.2 Shift Incident / Issue Log (already drafted) - PICK (re-aimed at "incident report form")

Search terms: "incident report form", "incident report", "injury report form", "near miss report form".
Result counts [MW, as of Oct 2026]: "incident report form" 1.1K active listings, average price USD 8.38, 20 shops in results (https://makerwords.com/keyword/incident-report-form). "incident report" 1.6K listings, average USD 10.35 (https://makerwords.com/keyword/incident-report). "injury report form" 279 listings, average USD 5.27 (https://makerwords.com/keyword/injury-report-form). Averages are pulled up by big bundles (USD 59 to 300); single forms sit at USD 2 to 6.

| # | Shop | Listing title | Price | Reviews / favourites / sales | Source | URL |
|---|---|---|---|---|---|---|
| 1 | ProBizTemplates | Workplace Incident Report Form Template, Workplace Accident Report Form, Worksite Incident Report Template | USD 3.74 | 14 favourites; ranks #3 of 236 for "injury report form"; shop 17.8K sales, 757 reviews, 4.8 | [MW] | https://makerwords.com/shop/probiztemplates (shop: https://www.etsy.com/shop/ProBizTemplates) |
| 2 | SubtlePlans | Printable Accident / Incident Report Form, Record All Incidents in Your Business, Industry, and More, PDF, A4/Letter | USD 1.99 | 19 favourites; shop 3.2K sales, 158 reviews, 4.8 (keyword page shows 1.7K sales, a different snapshot) | [MW] | https://makerwords.com/shop/subtleplans and https://makerwords.com/keyword/injury-report-form |
| 3 | JDSHPDesigns (listing text says "JDDesign") | Accident and Incident Report Template (MS Word & PDF) | USD 3.00 [MW]; EUR 3.30 incl. VAT [SUM] | 5 favourites; #1 of 1.1K for "incident report" [MW]; no item reviews yet [SUM]; shop 353 sales, 13 reviews | [MW] + [IDX] | https://www.etsy.com/listing/1117821311/accident-and-incident-report-template-ms |
| 4 | ScribblingBumblebee | Incident Witness Statement Form, Job Site Safety Documentation, Printable PDF | NZ$ 8.23 incl. GST (~USD 4.65) | no reviews shown | [IDX] | https://www.etsy.com/nz/listing/4436865463/incident-witness-statement-form-job-site |
| 5 | HREducationEdge | (ranks #10 of 776 for "incident report form"; its Workers Compensation Policy Template is USD 3.00, 20 favourites) | USD 3.00 | shop 26.5K sales | [MW] | https://makerwords.com/shop/hreducationedge |
| 6 | TheHustlingCatLady | Home Daycare ouch report, injury report, Incident report form, child incident form | USD 2.99 | 148 favourites; shop 40.6K sales | [MW] | https://makerwords.com/keyword/incident-report-form |
| 7 | shop not confirmed (Canva template) | Editable Incident Report Form Template: Workplace Safety (PDF) | AU$ 19.37 sale, from AU$ 32.28 (~USD 13.50 from ~22.49) [SUM] | not shown | [IDX] + [SUM] | https://www.etsy.com/au/listing/1799476163/editable-incident-report-form-template |
| 8 | ShaiRaePrints [SUM] | Incident Report Form (1-page printable PDF) | USD 2.50 [SUM] | not shown | [IDX] + [SUM] | https://www.etsy.com/listing/1409227789/incident-report-form |

Read: real, steady demand for printable incident forms, with established shops (3.2K to 40K shop sales) selling single forms at USD 2 to 4. The top of "incident report form" is skewed to childcare, home care and co-parenting buyers, but workplace forms (ProBizTemplates, SubtlePlans, JDSHPDesigns) rank too. Gap: nobody found sells a **shift supervisor** incident sheet with an open-incidents tracker that feeds a handover. Re-aim the existing draft's title and tags at "incident report form" / "incident report" (where the volume is) while keeping the shift angle.

### 2.3 New Manager 30-60-90 Day Plan (new) - PICK (replaces Weekly Team Check-in)

Search terms: "30 60 90 day plan", "30 60 90 day plans", "new manager first 90 days".
Result count: not visible today. [SUM] a summary of https://www.etsy.com/market/30_60_90_day_plan said "roughly 850 relevant results"; unverified.

| # | Shop | Listing title | Price | Reviews / favourites / sales | Source | URL |
|---|---|---|---|---|---|---|
| 1 | ManagerHacks (Etsy ad) | 30-60-90 Day Onboarding Plan Template, Editable Word and Google Docs, New Hire Objectives Planner for HR & Managers | GBP 3.19 sale (~USD 4.24), from GBP 4.26 (~USD 5.66), 25% off | shop (27) reviews | [IDX] | https://www.etsy.com/uk/market/30_60_90_day_plans |
| 2 | LBResumes (Etsy ad) | Executive 30 60 90 Day Plan for New Job, Manager Prep for Interview, Best 90 Day Plan for Sales and Marketing with Guide | GBP 18.68 (~USD 24.82) | shop (41) reviews | [IDX] | https://www.etsy.com/uk/market/30_60_90_day_plans |
| 3 | LBResumes (Etsy ad) | 30-60-90 Day Plan for New Job and Interview, Simple 306090 for Interviewing and New Job Prep, Instant Digital Download | GBP 18.68 (~USD 24.82) | shop (41) reviews | [IDX] | https://www.etsy.com/uk/market/30_60_90_day_plans |
| 4 | LBResumes | Modern Template for 30 60 90 Day Plan, Interview Prep for New Job, Best Digital Download for 90 Day Plan | USD 20.00 [SUM] | 5.0 rating [SUM] | [IDX] + [SUM] | https://www.etsy.com/listing/719732752/modern-template-for-30-60-90-day-plan |
| 5 | shop not shown in snippet | New Hire 30-60-90 Day Plan Template, Employee Onboarding Guide, Editable Google Doc + PDF | GBP 16.81 (~USD 22.34) | not shown | [IDX] | https://www.etsy.com/uk/market/30_60_90_day_plans |
| 6 | shop not shown in snippet | New Manager Leadership Workbook: First 100 Days Plan (Digital Download) 40+ templates | GBP 10.70 (~USD 14.22) [SUM] | shop 5.0 from 32 reviews, Star Seller [SUM]; the listing's own description text includes the word "Bestseller" [IDX] | [IDX] + [SUM] | https://www.etsy.com/listing/1582949791/new-manager-leadership-workbook-first |

Read: proven buyers and higher prices than the other niches (most comps USD 14 to 25). Two distinct buyer groups: (a) job seekers preparing for interviews (LBResumes), and (b) managers onboarding a new hire or starting as a new manager (ManagerHacks, the 100-day workbook). Almost all comps are editable Word/Docs/Slides files. A simple **print-and-write** 30-60-90 plan aimed at newly promoted team leaders and shift supervisors is not obviously present. Risk: evidence is all [IDX]/[SUM]; no live count; a print-and-write PDF may convert worse than an editable file for the job-seeker group, so the copy targets new managers, not interviews.

### 2.4 Weekly Team Check-in Sheet (already drafted) - NOT PICKED this round

Search terms: "team check in template", "weekly team check in", "team meeting agenda".
Result count: [LOG] 27 Sep live: "1,000+", price range ~USD 1.75 to 16, top-3 listings had 1, 0 and 1 reviews.
Today: no dedicated weekly team check-in listing with a visible price and review count could be found through the indirect routes. Only adjacent items: TheFocusedForm's 1:1 sheet (its title includes "Team Check-in form", USD 3.29), watercolortheme's meeting agenda (CA$ 3.90 [SUM]) and an untitled-price "Meeting Minutes Template, Meeting Agenda Printable" listing (https://www.etsy.com/ca/listing/1804373831/meeting-minutes-template-meeting-agenda). MakerWords pages for "meeting agenda" and "huddle" were placeholders and were discarded.
Verdict: weakest proof of demand of the three drafted products. Keep the existing draft (`etsy/LISTING_WEEKLY_CHECK_IN.md`, unchanged) as a bundle add-on for a New Manager Starter Toolkit, not a standalone priority.

### 2.5 Other candidates checked

| Candidate | Search term(s) | What was found | Verdict |
|---|---|---|---|
| Shift Handover Sheet (built) and Handover + Incident bundle | "shift handover sheet", "shift report forms", "rn handoff sheet" | Results dominated by nursing: ThePedsNurse "Pediatric Nurse Report + Shift Sheet" USD 5.00, 6 reviews [IDX] https://www.etsy.com/listing/791629503/pediatric-nurse-report-shift-sheet ; NursEdStudio "Nursing Brains Report Sheet: Shift Organizer Worksheet" USD 2.99 [IDX] https://www.etsy.com/listing/1885229428/nursing-brains-report-sheet-shift ; AusNurseCompanion "Australian Nurse ISBAR Handover Template" USD 5.88, no reviews [IDX] https://www.etsy.com/listing/4536551468/australian-nurse-isbar-handover-template . No bundle-specific evidence. | Already built. Keep "nurse handover" out of tags unless the sheet is adapted. Bundle stays a later step (USD 9 to 12). |
| Toolbox talk / safety briefing sheet | "toolbox talk", "toolbox meeting" | Etsy market pages exist (https://www.etsy.com/market/toolbox_talk , https://www.etsy.com/market/toolbox_meeting) but no listing detail came through. backofficeblueprint "Contractor Safety Binder, OSHA-Ready Safety System ... Toolbox Talks" USD 59.00, 2 shop sales [MW]. [LOG] 27 Sep: 893 results, top-3 reviews 0, 0, 1. | Insufficient evidence today. |
| Shift huddle / start-of-shift briefing | "team huddle template", "huddle board template" | Market pages exist (https://www.etsy.com/market/huddle_board_template , https://www.etsy.com/market/huddle_board_in_excel), no listing detail. MakerWords pages were placeholders. | Insufficient evidence. |
| Staff rota / shift schedule | "employee schedule", "roster template", "weekly employee work schedule" | JPSDigitalPages "Employee Schedule Template: Monthly Work Shift Planner, Google Sheets" USD 24.00, 296 favourites [MW]. "roster template" 1.7K listings, avg USD 18.82, but top results are sports rosters [MW] https://makerwords.com/keyword/roster-template . | Demand is for spreadsheets, not print-and-write. Not picked. |
| Employee onboarding checklist | "new hire onboarding checklist" | "New Hire Orientation Checklist, HR Guide, Feedback Form (printable PDF & Word)" [IDX] https://www.etsy.com/au/listing/4453279058/new-hire-orientation-checklist-day-1 (no price or reviews visible). MakerWords pages were placeholders. | Insufficient evidence. |
| Performance conversation / feedback log | "feedback form", "feedback template" | "feedback form" 1.8K listings, avg USD 5.13, but dominated by real-estate showing feedback [MW] https://makerwords.com/keyword/feedback-form . Closest: WilderPages "Performance Review Form: Employee Evaluation Google Doc Template" USD 8.00, 76 favourites [MW]; HREducationEdge "Employee Suggestion Box Form" USD 4.00, 91 favourites [MW]. | Mixed. Possible later 1:1 companion, not top 3. |
| Team skills matrix | "skills matrix excel" | 163 listings, avg USD 18.67, 18 shops [MW] https://makerwords.com/keyword/skills-matrix-excel . GlobalPMHub "HR Management Template Bundle ... Employee Training and Employee Skills Ma..." USD 11.70, 432 favourites; ExcelatSpreadSheet "Employee Training Tracker Excel Spreadsheet" USD 18.99, 198 favourites; BusinessInTemplates "Skills Matrix Excel Template" USD 20.50, 105 favourites; BlueTigerSystems "Professional Skills Matrix Excel Template" USD 2.00 [MW]. | Strong demand but for Excel/Sheets with formulas, not print-and-write. Worth a separate question to Kevin if he wants a spreadsheet line. Not picked. |
| Leave tracker | "request time off sheet", "pto tracker" | "request time off sheet" only 30 listings, HREducationEdge ranks #1 [MW]. "pto tracker" page was a placeholder. | Thin. Not picked. |

---

## 3. Picks and why

| Pick | Listing file | Why (one line) | Key evidence | Price |
|---|---|---|---|---|
| 1. One-on-One Meeting Template | `etsy/LISTING_ONE_ON_ONE.md` (refreshed) | Strongest proof: established shops with hundreds to 1.8K shop reviews sell it, one listing has 400 favourites. | HREducationEdge USD 5.00 (400 favs); TheFocusedForm USD 3.29; ManagerMindMappingCo ~USD 7.83; shop-(492) listing ~USD 3.46 | USD 4.00 |
| 2. Shift Incident Log (as incident report form) | `etsy/LISTING_SHIFT_INCIDENT_LOG.md` (refreshed) | 1.1K to 1.6K active listings and big-shop sellers at USD 2 to 4 show steady demand, and no shift-supervisor version with a handover tracker was found. | ProBizTemplates USD 3.74; SubtlePlans USD 1.99; JDSHPDesigns USD 3.00 (#1 for "incident report"); ScribblingBumblebee ~USD 4.65 | USD 3.50 |
| 3. New Manager 30-60-90 Day Plan | `etsy/LISTING_30_60_90_DAY_PLAN.md` (new) | Named shops sell it at higher prices (mostly USD 14 to 25) and the print-and-write, team-leader angle looks open. | ManagerHacks ~USD 4.24 sale; LBResumes ~USD 24.82 and USD 20.00 [SUM]; New Hire 30-60-90 ~USD 22.34; 100-day workbook ~USD 14.22 [SUM] | USD 5.00 |

Dropped from the top 3: Weekly Team Check-in Sheet (no new listing-level evidence today; 27 Sep top results had 0 to 1 reviews). Its draft stays on main unchanged as a bundle candidate.

## 4. What could not be verified
- No live Etsy result counts today for any term (bot check). The only counts are MakerWords [MW] (incident terms), a [SUM] figure (~850 for 30-60-90) and the 27 Sep live log.
- Shop names for three of the one-on-one listings (the shop-(492), shop-(531) and shop-(50) cards) were not in the snippets.
- [SUM] figures (watercolortheme CA$ 3.90, 37DesignClub SEK 19.39, JDSHPDesigns EUR 3.30, the AU$ 19.37 Canva form, ShaiRaePrints USD 2.50, LBResumes USD 20.00, the 100-day workbook GBP 10.70 and 32 reviews, "~850 results") come from a machine summary, not quoted page text.
- Crawl dates of the [IDX] snapshots are unknown; prices, ads and review counts may have changed.
- MakerWords shop "sales" are shop-level; no per-listing sales numbers were available anywhere.

Recommended next step for Kevin (or an interactive agent with a normal browser session): open the three search terms on Etsy from South Africa, note the live result count and the top 5 listings, and paste them under this section before publishing.

## 5. Sources (all accessed 1 Oct 2026)
- https://www.etsy.com/listing/4330862859/one-on-one-meeting-notes-printable
- https://www.etsy.com/market/one_on_one_meeting_template
- https://www.etsy.com/market/one_on_one_meeting
- https://www.etsy.com/market/1%3A1_manager_meeting_template
- https://www.etsy.com/ca/listing/1794573573/meeting-agenda-templatemeeting-agenda
- https://www.etsy.com/listing/1519686003/11-meeting-agenda-template-simple
- https://makerwords.com/shop/hreducationedge
- https://makerwords.com/shop/watercolortheme
- https://makerwords.com/shop/37designclub
- https://makerwords.com/shop/jpsdigitalpages
- https://makerwords.com/keyword/incident-report-form
- https://makerwords.com/keyword/incident-report
- https://makerwords.com/keyword/injury-report-form
- https://makerwords.com/shop/probiztemplates
- https://makerwords.com/shop/subtleplans
- https://makerwords.com/shop/jdshpdesigns
- https://www.etsy.com/listing/1117821311/accident-and-incident-report-template-ms
- https://www.etsy.com/nz/listing/4436865463/incident-witness-statement-form-job-site
- https://www.etsy.com/au/listing/1799476163/editable-incident-report-form-template
- https://www.etsy.com/listing/1409227789/incident-report-form
- https://www.etsy.com/uk/market/30_60_90_day_plans
- https://www.etsy.com/market/30_60_90_day_plan
- https://www.etsy.com/listing/719732752/modern-template-for-30-60-90-day-plan
- https://www.etsy.com/listing/1582949791/new-manager-leadership-workbook-first
- https://www.etsy.com/ca/listing/1804373831/meeting-minutes-template-meeting-agenda
- https://www.etsy.com/listing/791629503/pediatric-nurse-report-shift-sheet
- https://www.etsy.com/listing/1885229428/nursing-brains-report-sheet-shift
- https://www.etsy.com/listing/4536551468/australian-nurse-isbar-handover-template
- https://www.etsy.com/market/toolbox_talk
- https://www.etsy.com/market/toolbox_meeting
- https://www.etsy.com/market/huddle_board_template
- https://www.etsy.com/au/listing/4453279058/new-hire-orientation-checklist-day-1
- https://makerwords.com/keyword/roster-template
- https://makerwords.com/keyword/feedback-form
- https://makerwords.com/keyword/skills-matrix-excel
- https://www.banque-france.fr/en/statistics/rates-and-prices/exchange-rates-daily-parities-2026-09-30
- Baseline: `logs/research-etsy-demand.md` (27 Sep 2026)

Nothing was listed, published, purchased, favourited or sent. No account was signed in to.
