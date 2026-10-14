# FEAT-03 — Instant Search & Multi-Tag Filtering

> Implementation plan. Source: [docs/MISSING_FEATURES.md](../MISSING_FEATURES.md) §section.

## Metadata

| Field | Value |
|---|---|
| **Feature ID** | FEAT-03 |
| **Section** | Navigation & Search |
| **Severity** | MAJOR |
| **Markets** | Global/Web Archive 
| **Status (today)** | MISSING |
| **Estimated effort** | S(1w) |
| **Owner (proposed)** | Frontend Engineer |
| **Depends on** | FEAT-02 |
| **Unblocks** | Production Public Launch |

---

## 1. Problem Statement

With over 300 characters in the catalog, users cannot easily locate specific characters or isolate distinct sub-groups like enemies or spin-off staples. Manually scanning cards across the full grid is slow and tedious. Providing an instant search input and multi-tag filtering controls allows users to find characters and isolate targeted sub-groups in milliseconds.

## 2. Goals

- Provide a real-time name search bar that updates catalog cards instantly as the user types.
- Provide tag-based filter toggles for roles (hero, enemy, boss, etc.).
- Allow combining text search and tag filters simultaneously without conflicts.
- Display a dynamic result counter reflecting the active filter state.

## 3. Non-Goals

- Complex fuzzy regex search syntax or server-side database query processing.
- Saving search history or personal filter presets across browser sessions.
- Autocomplete search suggestions dropdown.

## 4. Personas & User Stories

- **As a video essayist**, I want to search for "Shy Guy" so that I can immediately pull up their stats without scrolling.
- **As a researcher**, I want to filter by the "Enemy" role tag so that I can analyze only non-playable obstacles.
- **As a casual fan**, I want to clear all filters with a single click so that I can easily reset my view.



## 5. Functional Requirements

Numbered, testable, written in MUST / SHOULD / MAY (RFC 2119) form.

- **FR-1.** The search input MUST normalize query strings (trimming whitespace and lowercasing) and filter displayed cards in real time using case-insensitive substring matching.
- **FR-2.** The system MUST support single-select and multi-select filtering across character roles.
- **FR-3.** The system MUST update the visible card list in under 50 ms upon any filter or search state change.
- **FR-4.** he system MUST display an active results counter (e.g., "Showing 12 of 314 characters").
- **FR-5.** A "Reset Filters" action MUST restore the catalog to the full, unfiltered dataset and clear the search input.

## 6. Non-Functional Requirements

- **Performance** — Filtering and search execution p95 latency MUST be under 50 ms.
- **Security** — Search query strings MUST be sanitized to prevent client-side script injection
- **Privacy & Compliance** — Search terms are evaluated strictly in client memory and never logged, stored, or tracked.
- **Accessibility** — Search input MUST have an explicit aria-label and announce updated result counts via an aria-live polite region.
- **Scalability** — Search logic MUST run efficiently against arrays up to 2,000 items without UI lag.
- **Reliability** — Typing non-alphanumeric characters or special symbols must not trigger unhandled JavaScript errors.
- **Observability** — None (client-side state).
- **Maintainability** — Filter state logic MUST be decoupled from visual card rendering components.
- **Internationalization** — Search matching must handle standard unicode characters and accented Latin letters.
- **Backward compatibility** — Handles records with missing role tags without crashing the filter logic.

## 7. Acceptance Criteria

Concrete, testable, Given/When/Then format. Each AC SHOULD map to at least one automated test.

- **AC-1.** *Given* the full catalog is displayed, *When* the user types "Bowser" into the search box, *Then* only cards containing "Bowser" in their display name remain visible.
- **AC-2.** *Given* the catalog is displayed, *When* the user clicks the "Boss" filter chip, *Then* only characters with type: "boss" are displayed in the grid.
- **AC-3.** *Given* a search term with zero matches (e.g., "Zelda"), *When* evaluated, *Then* the catalog displays a clear "No characters found" state with a button to reset search.


## 8. Data Model

- New tables / columns / enums.
Reactive client state:
  interface FilterState {
    searchTerm: string;
    selectedRoles: Set<string>;
  }
- Indexes & constraints.
None
- Migration file naming convention used by the repo (`server/migrations/NNN_*.sql`).
N/A (client-side in-memory filtering).
- Backfill strategy for existing rows.
None

## 9. API Surface

- New / changed HTTP routes (path, verb, auth scope).
None (pure client-side state manipulation).
- Request & response shapes (JSON schema or pseudo-TypeScript).
None
- Rate-limit / quota considerations.
None
- OpenAPI documentation requirement.
None

## 10. UI / UX

- New pages, modified pages, new components.
SearchBar, FilterButtonGroup, ResultsCounter
- Key user flows (numbered).
  1. Enter search term in text box.
  2. Toggle one or more role filter chips.
  3. Observe instant grid updates and counter changes.
  4. Click "Reset" or inline clear icon (×) to restore the default view.
- Empty / loading / error / offline states.
"No characters match your search" screen with a prominent "Clear Search" button.
- Mobile / responsive behaviour.
Filter chips wrap cleanly or use horizontal swipe scrolling on mobile viewports.
- Accessibility annotations (focus order, ARIA).
Search input has role="searchbox", filter chips have aria-pressed="true|false", and counter uses aria-live="polite".
- Copy & i18n keys.
"Search characters...", "Filter by role", "Reset", "Showing X of Y", "No characters found".