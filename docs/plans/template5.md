# FEAT-05 — Character Detail Modal/Breakdown View

> Implementation plan. Source: [docs/MISSING_FEATURES.md](../MISSING_FEATURES.md) §section.

## Metadata

| Field | Value |
|---|---|
| **Feature ID** | FEAT-05 |
| **Section** | Character Profiles |
| **Severity** | MAJOR |
| **Markets** | Global/Web Archive 
| **Status (today)** | MISSING |
| **Estimated effort** | S (1w) |
| **Owner (proposed)** | Frontend Engineer |
| **Depends on** | None(Independent UI component; connects to FEAT-01/02) |
| **Unblocks** | Production Public Launch |

---

## 1. Problem Statement

Character cards only provide high-level summary counts, preventing users from seeing the exact games, toys, and media that make up a character's total. Without a breakdown view, researchers cannot verify individual appearance milestones. Building a detail modal displays full debut context, category distribution bars, and itemized product codes.

## 2. Goals

- Open a focused detail modal overlay when any character card is selected.
- Display a categorized distribution breakdown (e.g., Mainline vs. Spin-offs vs. Toys).
- Provide an itemized list of specific product releases and media credits.
- Support complete keyboard dismissal via the Escape key and close button.

## 3. Non-Goals

- Full lore biographies, strategy guides, or gameplay videos.
- User commenting or community review sections.
- Links to external e-commerce shops or purchase platforms.

## 4. Personas & User Stories

- **As a collector**, I want to inspect a character's modal so that I can see the exact list of LEGO sets and Amiibos they appeared in.
- **As a researcher**, I want to view a character's category distribution so that I can understand their balance between main games and spin-offs.
- **As a user**, I want to dismiss the modal by tapping outside or pressing `Escape` so that I can quickly return to browsing.


## 5. Functional Requirements

Numbered, testable, written in MUST / SHOULD / MAY (RFC 2119) form.

- **FR-1.** Selecting a card MUST open a modal displaying that character's detailed metrics.
- **FR-2.** The modal MUST display character name, role badge, debut details, and total product count.
- **FR-3.** The modal MUST display category sub-totals using simple visual CSS distribution bars.
- **FR-4.** The modal MUST render itemized lists of all product codes associated with each category.
- **FR-5.** The modal MUST close immediately when the user clicks the close button, clicks the backdrop overlay, or presses Escape.

## 6. Non-Functional Requirements

- **Performance** — Modal open/close animation MUST run at 60 FPS with no layout thrashing.
- **Security** — All rendered modal text is sanitized against XSS.
- **Privacy & Compliance** — No user click tracking or individual character view metrics collected.
- **Accessibility** — Traps keyboard focus while active; includes role="dialog", aria-modal="true", and aria-labelledby.
- **Scalability** — Renders product code lists up to 300+ items per character cleanly using scrollable panels.
- **Reliability** — Gracefully hides empty categories when a character has zero appearances in that category.
- **Observability** — None
- **Maintainability** — Modular separation between modal shell, distribution bar, and itemized list components.
- **Internationalization** — Formats debut strings and labels according to browser locale.
- **Backward compatibility** — Handles missing category keys by treating them as empty arrays.

## 7. Acceptance Criteria

Concrete, testable, Given/When/Then format. Each AC SHOULD map to at least one automated test.

- **AC-1.** *Given* a user browsing character cards, *When* they click on Mario's card, *Then* a modal opens displaying Mario's complete category breakdown and itemized appearances.
- **AC-2.** *Given* an active detail modal, *When* the user presses the Escape key, *Then* the modal closes and focus returns to the card that opened it.
- **AC-3.** *Given* a character with 0 physical merchandise appearances, *When* their modal opens, *Then* the merchandise section displays "None recorded" or is cleanly hidden.

## 8. Data Model

- New tables / columns / enums.
Active character selection state (selectedCharacterId: string | null) and selected character object interface.
- Indexes & constraints.
None
- Migration file naming convention used by the repo (`server/migrations/NNN_*.sql`).
N/A (Client-side UI component consuming local state).
- Backfill strategy for existing rows.
None

## 9. API Surface

- New / changed HTTP routes (path, verb, auth scope).
None (reads from client-side selected object).
- Request & response shapes (JSON schema or pseudo-TypeScript).
None
- Rate-limit / quota considerations.
None
- OpenAPI documentation requirement.
None

## 10. UI / UX

- New pages, modified pages, new components.
CharacterDetailModal, CategoryProgressBar, ProductListSection.
- Key user flows (numbered).
Click character card → Modal slides/fades in → Scroll breakdown → Press Esc to exit.
- Empty / loading / error / offline states.
Product lists with 0 items display a muted empty indicator.
- Mobile / responsive behaviour.
Fits full screen on mobile devices with an accessible sticky close button.
- Accessibility annotations (focus order, ARIA).
Focus is trapped inside the modal; background page content receives aria-hidden="true".
- Copy & i18n keys.
"Category Breakdown", "Appearance Credits", "Close", "Debut Product".
