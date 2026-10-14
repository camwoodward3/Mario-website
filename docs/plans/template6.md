# FEAT-06 — Pre-Aggregated Leaderboards & Curated Views

> Implementation plan. Source: [docs/MISSING_FEATURES.md](../MISSING_FEATURES.md) §section.

## Metadata

| Field | Value |
|---|---|
| **Feature ID** | FEAT-06 |
| **Section** | Analytics & Leaderboards |
| **Severity** | MAJOR |
| **Markets** | Global/Web Archive 
| **Status (today)** | MISSING |
| **Estimated effort** | S (1w) |
| **Owner (proposed)** | Frontend Engineer |
| **Depends on** | FEAT-01 |
| **Unblocks** | Production Public Launch |

---

## 1. Problem Statement

Users often want quick, authoritative answers to specific ranking questions ("Who are the Top 10 characters?", "Which enemy has the most appearances?", or "Which characters appeared only once?"). Forcing users to manually configure multiple filters to answer these questions is frustrating. A dedicated leaderboards page provides instant, curated tables for franchise power rankings.

## 2. Goals

- Render a dedicated Top 10 / Top 20 overall leaderboard ranked by total product appearances.
- Provide a curated "Most Physical Merchandise" board ranking characters across LEGO, K'Nex, and Amiibo.
- Provide an "Obscurity Club" showcase highlighting characters with exactly one appearance.
- Enable direct navigation from any leaderboard row to that character's detail view.

## 3. Non-Goals

- User-submitted votes, upvoting, or popularity polling.
- Live competitive gaming scoreboards or speedrun leaderboards.
- Dynamically editable leaderboard thresholds.

## 4. Personas & User Stories

- **As a video essayist**, I want to cite a verified Top 10 list so that my video scripts contain accurate franchise appearance rankings.
- **As a toy collector**, I want to see which characters have the most physical merchandise appearances so that I can prioritize my collection goals.
- **As a trivia buff**, I want to browse the "Obscurity Club" so that I can discover obscure one-off characters.


## 5. Functional Requirements

Numbered, testable, written in MUST / SHOULD / MAY (RFC 2119) form.

- **FR-1.** The system MUST render an overall Top 10 leaderboard sorted descending by total_games.
- **FR-2.** The system MUST render a dedicated merchandise leaderboard sorting characters by the sum of their lego, knex, and amiibo counts.
- **FR-3.** The system MUST display an "Obscurity Club" table containing only characters whose total_games equals exactly 1.
- **FR-4.** Each leaderboard entry MUST show rank number, character name, role badge, and relevant count metric.
- **FR-5.** Clicking any character entry on a leaderboard MUST open that character's detail modal.

## 6. Non-Functional Requirements

- **Performance** — Leaderboard rendering time MUST be under 50 ms.
- **Security** — Read-only presentation; sanitized table inputs.
- **Privacy & Compliance** — Zero personal data collection.
- **Accessibility** — Rendered using semantic HTML <table> elements with proper <thead>, <th>, scope="col", and scope="row" attributes.
- **Scalability** — Computes leaderboards cleanly in memory from the base 300+ dataset.
- **Reliability** — Tied counts are handled deterministically using alphabetical secondary sorting.
- **Observability** — None
- **Maintainability** — Leaderboard derivation functions isolated in a pure helper module (src/utils/leaderboardUtils.js).
- **Internationalization** — Number counts formatted using standard locale formatting (e.g., commas for thousands).
- **Backward compatibility** — Number counts formatted using standard locale formatting (e.g., commas for thousands).

## 7. Acceptance Criteria

Concrete, testable, Given/When/Then format. Each AC SHOULD map to at least one automated test.

- **AC-1.** *Given* the Leaderboards view is loaded, *When* inspecting the Top 10 table, *Then* exactly 10 characters are shown, ordered strictly from Rank 1 to Rank 10 by total appearance count.
- **AC-2.** *Given* the Merchandise leaderboard, *When* rendered, *Then* ranks are calculated strictly from the sum of physical merch categories and not general video games.
- **AC-3.** *Given* the Obscurity Club section, *When* inspected, *Then* every character listed has a total count of exactly 1.

## 8. Data Model

- New tables / columns / enums
Reads processed_characters.json
- Indexes & constraints.
In-memory sorted arrays for Top 10, Merch Top 10, and Count == 1.
- Migration file naming convention used by the repo (`server/migrations/NNN_*.sql`).
N/A
- Backfill strategy for existing rows.
None

## 9. API Surface

- New / changed HTTP routes (path, verb, auth scope).
None (client-side data derivation from static JSON)
- Request & response shapes (JSON schema or pseudo-TypeScript).
None
- Rate-limit / quota considerations.
None
- OpenAPI documentation requirement.
None

## 10. UI / UX

- New pages, modified pages, new components.
LeaderboardsView, RankTable, ObscurityClubGrid
- Key user flows (numbered).
Switch from Catalog tab to Leaderboards tab → Browse rankings → Click row to view details.
- Empty / loading / error / offline states.
Clean skeleton table loaders while data loads.
- Mobile / responsive behaviour.
Tables convert to compact card lists or support horizontal scrolling on mobile viewports.
- Accessibility annotations (focus order, ARIA).
Tables marked with caption elements; ranking numbers labeled with aria-label="Rank X".
- Copy & i18n keys.
"All-Time Franchise Leaders", "Top Physical Merchandise", "The Obscurity Club", "Rank"
