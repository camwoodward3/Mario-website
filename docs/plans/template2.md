# {FEAT-02} — {Main Category Grid & Character Cards}

> Implementation plan. Source: [docs/MISSING_FEATURES.md](../MISSING_FEATURES.md) §{section}.

## Metadata

| Field | Value |
|---|---|
| **Feature ID** | FEAT-02 |
| **Section** | Presentation Layer |
| **Severity** | BLOCKER |
| **Markets** | Global/Web Archive
| **Status (today)** | MISSING |
| **Estimated effort** | S (1w) |
| **Owner (proposed)** | Frontend engineer |
| **Depends on** | FEAT-01 |
| **Unblocks** | FEAT-03, FEAT-04 |

---

## 1. Problem Statement

Visitors currently have no structured interface to browse the 300+ characters in the franchise, forcing them to sift through raw data files. This creates friction for fans and collectors looking for high-level summaries. Building a responsive card grid presents every character with their name, role, debut year, and total appearances in a scannable, responsive layout."

## 2. Goals

- Render a responsive grid container that loads and displays all records from processed_characters.json.
- Present character cards displaying name, debut year, role badge, and total count.
- Implement responsive layout rules adapting smoothly across mobile, tablet, and desktop viewports.
- Maintain sub-100ms render performance on initial catalog mount.

## 3. Non-Goals

- In-place editing of character card information.
- Image hosting and photo rendering on card thumbnails for the MVP.
- Draggable or customizable card rearrangement by the user.

## 4. Personas & User Stories

- **As a {casual fan}**, I want to {see character cards laid out in a clean grid} so that {I can quickly spot familiar faces and compare their numbers}.
- **As an {educator}**, As an educator, I want to view key data points (debut year, role) directly on each card so that students can reference milestones at a glance.
- **As a {mobile visitor}**, I want the catalog to collapse into a single-column layout so that I can browse comfortably on a phone without horizontal scrolling.


## 5. Functional Requirements

Numbered, testable, written in MUST / SHOULD / MAY (RFC 2119) form.

- **FR-1.** The system MUST fetch and parse processed_characters.json on initial view load.
- **FR-2.** each card MUST display the character's canonical name, debut year, role, and pre-computed total appearances.
- **FR-3.** The grid MUST support rendering 300+ cards simultaneously without page freezing.
- **FR-4.** Each card MUST include an interactive action (button or card click) to trigger the detail modal.

## 6. Non-Functional Requirements

- **Performance** — Catalog grid render time MUST be under 100 ms after JSON load.
- **Security** — Character card text MUST be escaped prior to DOM injection to prevent XSS
- **Privacy & Compliance** — No user interaction data or card view counts are tracked.
- **Accessibility** — Cards MUST use semantic markup (<article> or <li>) with focusable button triggers.
- **Scalability** — Layout container MUST handle CSS grid auto-fill up to 4K display resolutions.
- **Reliability** — Missing attributes (e.g., unknown debut) fall back to "Unknown" without breaking card borders.
- **Observability** — Unhandled JSON fetch errors trigger a visible UI fallback message.
- **Maintainability** — Card components MUST be modular and isolated in a separate component file.
- **Internationalization** — Character names support full UTF-8 character rendering.
- **Backward compatibility** — Component adapts gracefully if additional category tags are added in future schemas.

## 7. Acceptance Criteria

Concrete, testable, Given/When/Then format. Each AC SHOULD map to at least one automated test.

- **AC-1.** *Given* processed_characters.json contains 300 valid character objects, *When* catalog page loads, *Then* exactly 300 character cards are rendered within the responsive grid container.
- **AC-2.** *Given* a character card on the screen, *When* inspected, *Then* the card clearly displays the character name, role badge, debut year, and total appearance count.
- **AC-3.** *Given* a user resizing their browser from 1200px to 375px width, *When* the viewport width narrows, *Then* the layout switches from a multi-column grid to a single-column layout without horizontal scrollbars.

## 8. Data Model

- New tables / columns / enums
Reads id, name, type, debut, total_games from pre-calculated JSON.
- Indexes & constraints.
None
- Migration file naming convention used by the repo (`server/migrations/NNN_*.sql`).
Client-side component files (`src/components/CatalogGrid.js`).
- Backfill strategy for existing rows.
None

## 9. API Surface

- New / changed HTTP routes (path, verb, auth scope).
    GET /data/processed_characters.json
- Request & response shapes (JSON schema or pseudo-TypeScript).
    Array of character summary objects
- Rate-limit / quota considerations.
    Standard static file caching
- OpenAPI documentation requirement.
    None

## 10. UI / UX

- New pages, modified pages, new components.
CatalogGrid, CharacterCard
- Key user flows (numbered).
Land on home page → View total record count header → Scroll through cards.
- Empty / loading / error / offline states.
Skeleton loading cards; error banner displayed if JSON fails to fetch.
- Mobile / responsive behaviour.
1 column on mobile, 2 columns on tablet, 3-4 columns on desktop.
- Accessibility annotations (focus order, ARIA).
role="region", aria-label="Character Catalog"
- Copy & i18n keys.
"Total Appearances", "Debut", "View Details"
