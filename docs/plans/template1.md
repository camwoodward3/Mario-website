# FEAT-01 — Pre-Calculated Data Pipeline

> Implementation plan. Source: [docs/MISSING_FEATURES.md](../MISSING_FEATURES.md) §{section}.

## Metadata

| Field | Value |
|---|---|
| **Feature ID** | FEAT-01 |
| **Section** | Data Pipeline & Ingestion |
| **Severity** | BLOCKER |
| **Markets** | Global/Web Archive 
| **Status (today)** | PARTIAL |
| **Estimated effort** | S(1w) |
| **Owner (proposed)** | Data Engineer/Backend Lead |
| **Depends on** | {None(Independent Baseline)} |
| **Unblocks** | FEAT02, FEAT-05, FEAT-06 |

---

## 1. Problem Statement

Raw franchise records are split between disparate, unstructured JSON files containing unvalidated types, nested lists, and duplicate entries. Loading and parsing these files on every client visit causes slow performance and inaccurate counts. Building an offline Pythion aggregation script normalizes data, deduplicates appearances, and outputs a fast, pre-calculated JSON asset ready for the web.

## 2. Goals

- Ingest and merge entity records from characters.json and enemies.json without data corruption.
- Filter out unapproved entity types using a strict ALLOWED_TYPES set.
- Pre-compute total_products and category sub-totals while eliminating duplicate tags.
- Export an aggregated, web-ready processed_characters.json in under 1 second.

## 3. Non-Goals

- Writing data directly into an active relational SQL database.
- Web scraping external wikis or automated fetching of new assets during runtime.
- In-browser data editing or dynamic server-side mutation endpoints.

## 4. Personas & User Stories

- As an archivist admin, I want to run a fast Python script over updated raw data files so that totals are recalculated accurately without manual math.
- As a developer, I want pre-calculated counts exported to a single clean file so that the frontend code remains lightweight and snappy.
- As a content researcher, I want duplicate product tags eliminated automatically so that appearance counts are never artificially inflated.

## 5. Functional Requirements

Numbered, testable, written in MUST / SHOULD / MAY (RFC 2119) form.

- **FR-1.** The script MUST … ingest both characters.json and enemies.json using UTF-9 encoding.
- **FR-2.** The system MUST … drop or skip records whose type attribute is not in ALLOWED_TYPES (hero, ally, anti-hero, boss, sub-boss, antagonist)
- **FR-3.** The script MUST … calculate total_products as the sum of unique product tokens across all predefined categories(nes, n64, ngc, etc.).
- **FR-4.** The script MUST … preserve an itemized category_counts object for every record.
- **FR-5.** The script MUST … export the sorted results (descending by total_games) into processed_characters.json

## 6. Non-Functional Requirements

- **Performance** — Execution time to process 300+ records MUST complete in under 500 ms.
- **Security** — Pipeline runs strictly offline in local/CI environments with no write permissions to external networks.
- **Privacy & Compliance** — Process exclusively public gaming metadata; no personal user information is ingested or exported.
- **Accessibility** — Console must provide high-contrast, clear terminal status summaries.
- **Scalability** — Data structures MUST scale to process 5,000+ entries without exceeding 100 MB of system RAM.
- **Reliability** — The script MUST be idempotent; identical inputs must produce identical JSON outputs.
- **Observability** — Script logs elapsed execution time, total processed records, and warnings for missing files.
- **Maintainability** — Code MUST adhere to PEP 8 standards with full type annotations.
- **Internationalization** — Handles UTF-8 strings cleanly for Japanese names and accented Latin characters
- **Backward compatibility** — Ingestion logic defaults missing debut years or categories to clean fallbacks without crashing.

## 7. Acceptance Criteria

Concrete, testable, Given/When/Then format. Each AC SHOULD map to at least one automated test.

- **AC-1.** *Given* valid characters.json and enemies.json files, *When* python thread.py is executed *Then* valid processed_characters.json file is generated containing all approved entities sorted by total count. 
- **AC-2.** *Given* an entry with duplicate entries in a category (e.g., ["SMW", "SMW"]), *When* the script aggregates category occurrences, *Then* Then total_games counts the duplicate token only once.
- **AC-3.** *Given* an entity with an unrecognized type like "vehicle", *When* When the data pipeline processes the input, *Then* that entity is skipped and not exported to the final dataset.

## 8. Data Model

- ALLOWED_TYPES set (hero, ally, anti-hero, boss, sub-boss, antagonist, enemy).
- Pre-sorted descending by total_products.
- (`scripts/thread.py`) updating (`public/data/processed_characters.json`).
- Full deterministic rebuild on every script execution.

## 9. API Surface

- New / changed HTTP routes (path, verb, auth scope).
    None(offline data generation script)
- Request & response shapes (JSON schema or pseudo-TypeScript).
    CLI output printing elapsed time and record counts.
- Rate-limit / quota considerations.
    None
- OpenAPI documentation requirement.
    None

## 10. UI / UX

- New pages, modified pages, new components
    Terminal CLI output
- Key user flows (numbered).
    Admin runs python thread.py --> Review terminal logs --> Commit generated JSON.
- Empty / loading / error / offline states.
    Missing input file logs a clean warning rather than a stack trace.
- Mobile / responsive behaviour.
    Not applicable
- Accessibility annotations (focus order, ARIA).
    Not applicable
- Copy & i18n keys.
    Standardized console log strings
