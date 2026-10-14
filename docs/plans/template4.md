# FEAT-04 — Multi-Field Sorting

> Implementation plan. Source: [docs/MISSING_FEATURES.md](../MISSING_FEATURES.md) §section.

## Metadata

| Field | Value |
|---|---|
| **Feature ID** | FEAT-04 |
| **Section** | Navigation & Search |
| **Severity** | MINOR |
| **Markets** | Global/Web Archive 
| **Status (today)** | MISSING |
| **Estimated effort** | S (1w) |
| **Owner (proposed)** | Frontend Engineer |
| **Depends on** | FEAT-02 |
| **Unblocks** | Production Public Launch |

---

## 1. Problem Statement

Browsing characters without flexible sorting options makes it difficult to discover who has appeared the most, find specific names alphabetically, or view historical progression chronologically. Users need quick sorting controls to answer different analytical questions without refreshing the page.

## 2. Goals

- Provide sorting by total appearances (highest to lowest and lowest to highest).
- Provide alphabetical sorting by character name (A–Z and Z–A).
- Provide chronological sorting by debut year (oldest to newest).
- Ensure sort order applies seamlessly on top of active search and filter results.

## 3. Non-Goals

- Multi-column complex custom sorting algorithms.
- Server-side database ordering queries.
- Persisting sort preferences to user accounts.

## 4. Personas & User Stories

- **As a trivia buff**, I want to sort by total appearances so that I can immediately see the most ubiquitous characters in the franchise.
- **As an archivist**, I want to sort by debut year so that I can trace character introductions from 1981 to the present.
- **As a casual user**, I want to sort alphabetically so that that I can look up characters like a traditional encyclopedia.


## 5. Functional Requirements

Numbered, testable, written in MUST / SHOULD / MAY (RFC 2119) form.

- **FR-1.** The system MUST provide a sort dropdown selector with the following options:
    Most Appearances (default)
    Fewest Appearances
    Name (A–Z)
    Name (Z–A)
    Debut Year (Oldest First)
    Debut Year (Newest First)
- **FR-2.** Applying a sort option MUST instantly reorder the currently visible cards without resetting active search or filter criteria.
- **FR-3.** The sorting engine MUST use canonical character name (A–Z) as a deterministic secondary tie-breaker whenever numerical counts or debut years are identical.
- **FR-4.** The sorting execution MUST run in under 30 ms across the entire catalog.

## 6. Non-Functional Requirements

- **Performance** — Client-side array sort execution p95 latency MUST be under 30 ms for 300+ items.
- **Security** — Sort criteria parameters evaluated against a strict whitelist of approved keys
- **Privacy & Compliance** — No user sorting choices are tracked or recorded.
- **Accessibility** — Sort control implemented as a standard semantic <select> element or accessible ARIA combobox.
- **Scalability** — Array sorting scales cleanly up to 5,000 items in memory without frame drops.
- **Reliability** — Characters with missing or "Unknown" debut dates sort gracefully to the end of chronological lists.
- **Observability** — None (client-side state).
- **Maintainability** — Sorting comparator functions isolated in a pure utility module (`src/utils/sortUtils.js`).
- **Internationalization** — Alphabetical sorting uses localeCompare to handle accents and non-ASCII characters correctly.
- **Backward compatibility** — Safely handles missing count fields by defaulting their numerical value to 0.

## 7. Acceptance Criteria

Concrete, testable, Given/When/Then format. Each AC SHOULD map to at least one automated test.

- **AC-1.** *Given* the catalog is displayed, *When* the user selects "Name (A–Z)", *Then* the first card displayed is alphabetically first and all subsequent cards follow alphabetical ordering.
- **AC-2.** *Given* a filtered list of "Boss" characters, *When* the user switches to "Most Appearances", *Then* the boss with the highest total_games is displayed first while retaining the boss-only filter.
- **AC-3.** *Given* the catalog sorted by debut year, *When* evaluated, *Then* early 1980s characters (e.g., Mario, Donkey Kong) appear before 1990s and 2000s introductions.

## 8. Data Model

- New tables / columns / enums.
type SortOption = 
  | 'COUNT_DESC' 
  | 'COUNT_ASC' 
  | 'NAME_ASC' 
  | 'NAME_DESC' 
  | 'DEBUT_ASC' 
  | 'DEBUT_DESC';
- Indexes & constraints.
None
- Migration file naming convention used by the repo (`server/migrations/NNN_*.sql`).
N/A (client-side in-memory sorting).
- Backfill strategy for existing rows.
None

## 9. API Surface

- New / changed HTTP routes (path, verb, auth scope).
None (client-side array sorting)
- Request & response shapes (JSON schema or pseudo-TypeScript).
None
- Rate-limit / quota considerations.
None
- OpenAPI documentation requirement.
None

## 10. UI / UX

- New pages, modified pages, new components.
SortDropdown component placed adjacent to search controls.
- Key user flows (numbered).
Select dropdown option → Catalog cards re-order instantly with smooth CSS transition.
- Empty / loading / error / offline states.
Disabled during initial JSON load.
- Mobile / responsive behaviour.
Dropdown wraps cleanly below search input on narrow mobile viewports (<640px).
- Accessibility annotations (focus order, ARIA).
Accessible <label> or aria-label="Sort characters by" linked to the form control.
- Copy & i18n keys.
"Sort By", "Most Appearances", "Fewest Appearances", "Name (A–Z)", "Name (Z–A)", "Debut (Oldest)", "Debut (Newest)".