# Information Architecture Improvement Proposal

## Scope

This proposal reorganizes the current 129-page sitemap into a clearer, task-based structure with fewer top-level categories, consistent labeling, and predictable URL groupings. The goal is to reduce navigation depth, cluster similar content, and separate program content from administrative/form pages.

## Observed IA Issues (Current State)

- **Duplicate or near-duplicate landing pages**: e.g., `/home-202111`, `/home-copy-1`, `/funded-programmes-1`, `/corporate-training-1` create ambiguity about the canonical entry point.
- **Mixed content types in navigation**: programme pages sit alongside forms, funding info, and internal/utility pages, which dilutes task-based navigation.
- **Inconsistent URL families for similar content**: course catalogues spread across `/bsm/*`, `/ctw/*`, `/ftv/*`, `/rsd/*`, `/nmt/*`, `/sms/*`, `/sfdw-courses/*` without a unifying hub.
- **Form sprawl**: multiple enquiry forms are exposed as standalone pages without a clear decision path.
- **Low-signal pages surfaced**: temporary or utility pages (gallery, message info) appear at the same level as core programmes.

## Before vs. After (Top-level)

| Before (current top-level) | Representative content | After (proposed top-level) | Rationale |
| --- | --- | --- | --- |
| Home | `/home`, `/home-202111`, `/home-copy-1` | Home | Keep a single canonical home; archive or redirect variants. |
| Funded Programmes | WSQ, SGUS, SFM course pages | Programmes | Single entry point for all funded programmes with sub-categories. |
| Funded Mentorship Support | `/mentorship-support-grant` | Programmes → Mentorship Support | Group with funded offerings. |
| Corporate Training | `/corporate-training`, `/corporate-training-1`, `/corporate-training-courses/*` | Corporate Training | Separate a “Solutions” landing page and “Courses” listings. |
| Masterclasses | `/masterclasses`, `/mcs/*` | Masterclasses | Preserve as a distinct catalogue. |
| Workshops & Seminars | `/workshops-seminars`, `/wks/*` | Workshops & Seminars | Preserve as a distinct catalogue. |
| Forms & Enquiries | `/funding-information`, multiple enquiry forms | Contact & Enquiries | Collect all forms and funding info under a single utility section. |
| Other Pages | About, FAQ, Vision/Mission, etc. | About SMA | Consolidate about/credibility content. |

## Before vs. After (Key groupings)

| Current grouping | Pages | Proposed grouping | Changes |
| --- | --- | --- | --- |
| Funded Programmes | WSQ (`/bsm/*`, `/ctw/*`, `/ftv/*`, `/rsd/*`, `/nmt/*`), SGUS (`/sgus*`, `/sgunited-courses/*`), SFM (`/sms/*`, `/sfdw-courses/*`) | Programmes → WSQ, SGUS, SFM, SkillsFuture for Digital Workplace | Keep all funded training under one hub with clear sub-categories. |
| Forms & Enquiries | Funding information, 9+ enquiry forms | Contact & Enquiries → Funding, Corporate Enquiry, Course Enquiry, General Enquiry, Form Templates | Normalize the form taxonomy and add clearer labels. |
| About/Info (scattered) | `/board-of-directors`, `/vision-mission-values`, `/edutrust-certification`, `/organisation-chart`, `/campus-facilities`, `/faq` | About SMA → Leadership, Accreditation, Campus, FAQ, Vision & Values | Merge into an About section with consistent subpages. |
| Homepage Variants | `/home-202111`, `/home-copy-1`, `/homepage-*-slider` | Home → Archive (internal only) | Keep a single public home; archive or redirect older variants. |
| Miscellaneous | `/new-gallery-1`, `/new-page-kr`, `/msg-info` | Resources → News & Updates (or Archive) | Move low-signal pages into a resource/archive bucket. |

## Proposed Navigation (After)

1. **Home**
   - `/home` (canonical)
   - *Archive:* `/home-202111`, `/home-copy-1`, `/homepage-desktop-slider`, `/homepage-mobile-slider`

2. **Programmes**
   - **Funded Programmes Overview** (`/funded-programmes`)
   - **WSQ Programmes** (`/bsm/*`, `/ctw/*`, `/ftv/*`, `/rsd/*`, `/nmt/*`)
   - **SGUS Programmes** (`/sgus`, `/sgus-*`, `/sgunited-courses/*`)
   - **SFM Programmes** (`/sms/*`)
   - **SkillsFuture for Digital Workplace** (`/skillsfuture-for-digital-workplace`, `/sfdw-courses/*`)
   - **Mentorship Support** (`/mentorship-support-grant`)

3. **Corporate Training**
   - **Corporate Training Overview** (`/corporate-training`)
   - **Solutions** (`/corporate-training-1`)
   - **Corporate Training Courses** (`/corporate-training-courses/*`)

4. **Masterclasses**
   - **Masterclasses Overview** (`/masterclasses`)
   - **Masterclasses Catalogue** (`/mcs/*`)

5. **Workshops & Seminars**
   - **Workshops Overview** (`/workshops-seminars`)
   - **Workshops Catalogue** (`/wks/*`)

6. **About SMA**
   - **Vision & Values** (`/vision-mission-values`)
   - **Leadership** (`/board-of-directors`, `/organisation-chart`)
   - **Accreditation** (`/edutrust-certification`)
   - **Campus** (`/campus-facilities`)
   - **FAQ** (`/faq`)
   - **Accelerated Industry-centric Training Pathway** (`/aitp`)

7. **Contact & Enquiries**
   - **Funding Information** (`/funding-information`)
   - **Corporate Enquiry** (`/ct-form`)
   - **Course Enquiry** (`/smeocm-form` and other course forms)
   - **General Enquiry** (`/enquire-now`)
   - **Form Templates** (`/form-template`, `/form-template-msg`)

8. **Resources**
   - **News/Updates/Info** (`/msg-info`)
   - **Miscellaneous/Archive** (`/new-gallery-1`, `/new-page-kr`)

## Redirect & Canonicalization Summary (Key Moves)

| Current URL | Proposed canonical location | Action |
| --- | --- | --- |
| `/home-202111`, `/home-copy-1` | `/home` | 301 redirect to canonical home. |
| `/homepage-desktop-slider`, `/homepage-mobile-slider` | `/home` (or internal archive) | Remove from public nav; archive or 301. |
| `/funded-programmes-1` | `/funded-programmes` | 301 redirect to canonical funded programmes hub. |
| `/corporate-training-1` | `/corporate-training` | 301 redirect unless kept as “Solutions” subpage. |
| Course enquiry forms (multiple) | `/contact-enquiries` + sublinks | Consolidate navigation access while preserving URLs. |

## Content Normalization Recommendations

- **Normalize naming**: use consistent pluralization (e.g., “Programmes” across all funded sections).
- **Remove duplicate landing pages**: treat `/funded-programmes-1` and `/corporate-training-1` as variants and fold into canonical landing pages unless content is distinct.
- **Unify course naming**: use consistent prefixes (WSQ, SGUS, SFM, SFDW) across page titles and URLs.
- **Consolidate forms**: use a single “Contact & Enquiries” landing page with a short decision tree to reduce the number of similar form pages shown in nav.
- **Archive low-signal pages**: move “gallery” or “temporary” pages out of primary navigation.

## Implementation Notes

- This proposal is structure-only. It does not alter the existing markdown content.
- Redirects should be planned for any URL removals or consolidations.
- Navigation and sitemap updates should align to the “After” grouping above.
