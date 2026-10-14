# FEAT-07 — Read-Only Edge Deployment & Accessibility(WCAG)

> Implementation plan. Source: [docs/MISSING_FEATURES.md](../MISSING_FEATURES.md) §section.

## Metadata

| Field | Value |
|---|---|
| **Feature ID** | FEAT-07 |
| **Section** | Infrastructure & Accessibility |
| **Severity** | MAJOR |
| **Markets** | Global/Video Game Fandom & Educational Web 
| **Status (today)** | MISSING |
| **Estimated effort** | S(1w) |
| **Owner (proposed)** | Frontend/DevOps Lead |
| **Depends on** | FEAT-01 - FEAT-06 |
| **Unblocks** | FEAT02, FEAT-05, FEAT-06 |

---

## 1. Problem Statement

Without a globally distributed edge host and deliberate accessibility standards, high-traffic spikes from gaming communities can cause slowdowns, while users relying on keyboard navigation or screen readers are completely locked out of exploring the archive. This gap frustrates community enthusiasts, researchers with disabilities, and mobile visitors with limited network speeds. Delivering an ad-free, statically cached edge site that conforms to WCAG 2.1 AA provides sub-second global access, guarantees inclusive usability, and establishes the archive as a durable, dependable public reference tool.

## 2. Goals

- Achieve sub-2-second global page loads by serving pre-rendered static assets and compressed JSON via a Content Delivery Network (CDN) edge cache.
- Attain 100% compliance with WCAG 2.1 Level AA standards across all catalog controls, cards, and modal dialogs.
- Provide seamless, trap-free keyboard navigation (Tab, Shift+Tab, Enter, Space, Escape) across the entire user experience.
- Maintain a zero-downtime, ad-free, read-only surface that safely withstands viral traffic spikes without origin server costs.

## 3. Non-Goals

- User account registration, login portals, or personalized bookmark databases.
- Multi-region database replication or server-side dynamic rendering setups.
- Commercial ad network integrations, third-party analytics trackers, or affiliate cookies.
- Automated real-time translation pipelines for international languages outside static UTF-8 support.

## 4. Personas & User Stories

- **As a student researcher with visual impairments**, I want to navigate the catalog using a screen reader so that I can listen to character counts and debut years without encountering missing image labels or broken button states.
- **As a keyboard-only user(self-learner)**, I want clear, visible focus rings and logical tab ordering so that I can filter characters and close modal dialogs without a mouse.
- **As a site admin/maintainer**, I want the site deployed as an immutable static edge bundle so that viral traffic spikes never crash a server or run up high hosting bills..

## 5. Functional Requirements

Numbered, testable, written in MUST / SHOULD / MAY (RFC 2119) form.

- **FR-1.** The deployment pipeline MUST publish the built application as static HTML, CSS, JavaScript, and JSON assets to a CDN edge provider.
- **FR-2.** The system MUST maintain complete read-only operation and refuse all unauthenticated HTTP state-mutation verbs (POST, PUT, PATCH, DELETE).
- **FR-3.** All interactive UI components (buttons, links, search fields, checkboxes) MUST be fully focusable and operable via standard keyboard inputs (Tab, Shift+Tab, Enter, Space, Escape).
- **FR-4.** The detail modal MUST trap keyboard focus within its perimeter while open and return focus to the triggering element upon dismissal via the Escape key or close button.
- **FR-5.** The interface MUST provide ARIA attributes (aria-expanded, aria-label, aria-haspopup, role="dialog") for dynamic states like search queries and modal popups.
- **FR-6.** The UI MUST maintain a minimum color contrast ratio of 4.5:1 for standard body text and 3:1 for large text, badges, and primary interactive boundaries.

## 6. Non-Functional Requirements

- **Performance** — p95 edge latency MUST remain under 150 ms; static asset payloads MUST remain under 500 KB uncompressed (under 120 KB gzip/brotli).
- **Security** — Read-only public surface; transport MUST enforce HTTPS via TLS 1.3; response headers MUST include strict Content-Security-Policy, X-Content-Type-Options: nosniff, and X-Frame-Options: DENY.
- **Privacy & Compliance** — Full compliance by design with COPPA, GDPR, and FERPA by strictly collecting zero personal user data, IP logs, or tracking cookies.
- **Accessibility** — Full conformance to WCAG 2.1 Level AA across every interactive view.
- **Scalability** — Edge caching MUST sustain over 1,000 requests per second with zero origin server compute degradation.
- **Reliability** — Availability target of 99.9% uptime powered by multi-region CDN failover.
- **Observability** — Real-time CDN edge analytics tracking HTTP status distributions (2xx, 4xx, 5xx) and page-load Core Web Vitals.
- **Maintainability** — Clean deployment scripts automated via GitHub Actions, enforcing automated linter checks and lighthouse accessibility audits prior to deployment.
- **Internationalization** — All textual content and JSON data MUST be served in UTF-8 encoding to preserve special characters and Japanese titles.
- **Backward compatibility** — Static build paths MUST preserve standard root routing (/) and permanent link conventions to prevent broken bookmarks across revisions.

## 7. Acceptance Criteria

Concrete, testable, Given/When/Then format. Each AC SHOULD map to at least one automated test.

- **AC-1.** *Given* a user visiting the production URL on any modern browser, *When* the root index page is requested, *Then* the page is served over HTTPS via edge cache with an LCP (Largest Contentful Paint) under 1.8 seconds.
- **AC-2.** *Given* a user using only keyboard navigation, *When* they press Tab repeatedly through the catalog grid, *Then* every card button receives a prominent visual focus ring in logical reading order without skipping elements.
- **AC-3.** *Given* an open character detail modal, *When* the user presses the Escape key, *Then* the modal immediately closes and keyboard focus returns directly to the card button that initiated it.
- **AC-4.** *Given* an automated accessibility scan using Axe-core or Lighthouse, *When* run against all production views (catalog, leaderboards, detail modal), *Then* the test suite reports zero WCAG 2.1 AA violations.

## 8. Data Model

- New tables / columns / enums.
None (static edge site reading pre-compiled processed_characters.json).
- Indexes & constraints.
Not applicable (client-side in-memory array filtering).
- Migration file naming convention used by the repo (`server/migrations/NNN_*.sql`).
Not applicable; data updates are versioned via static release files (`public/data/processed_characters_v1.json`).
- Backfill strategy for existing rows.
Not applicable; static JSON regeneration via thread.py build step.

## 9. API Surface

- New / changed HTTP routes (path, verb, auth scope).
• GET / — Serves static index HTML.
• GET /data/processed_characters.json — Static JSON payload containing pre-aggregated character records.
• GET /health — Edge status check (returns HTTP 200 "status": "healthy").
- Request & response shapes (JSON schema or pseudo-TypeScript).
None (public read-only).
- Rate-limit / quota considerations.
Handled at edge layer (standard CDN burst protection: 100 requests/minute per IP).
- OpenAPI documentation requirement.
Not required for static file delivery.

## 10. UI / UX

- New pages, modified pages, new components.
• SkipToContent link pinned to top of DOM for keyboard navigators.
• Global FocusRing CSS styles.
• High-contrast tag badges and status indicators.
- Key user flows (numbered).
1. User lands on page → Presses Tab → Selects "Skip to catalog" → Enters search criteria.
2. User selects character card with Enter → Modal opens with focus trapped → Reads stats → Dismisses via Escape → Focus returns to original card.
- Empty / loading / error / offline states.
• Loading: Lightweight skeleton placeholder cards while the 100 KB JSON payload downloads.
• Error: Clean fallback card stating "Archive data could not be reached. Check network connection." with a retry button.
- Mobile / responsive behaviour.
Fully responsive grid adapting from 1 column (mobile) to 4 columns (desktop widescreen).
- Accessibility annotations (focus order, ARIA).
ARIA live regions (aria-live="polite") announcing search result counts when filters change.
- Copy & i18n keys.
Strings centralized in a dedicated src/constants/uiCopy.js file for clean separation.
