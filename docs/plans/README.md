# Implementation Roadmap & Architecture Dependencies

## 1. Recommended Implementation Order

The project features should be rolled out across sequential milestones to ensure continuous integration without blockers:

1. **FEAT-01: Pre-Calculated Data Pipeline (`thread.py`)** — *Infrastructure/Data*
2. **FEAT-02: Main Catalog Grid & Character Cards** — *Core UI & Fetch Lifecycle*
3. **FEAT-05: Character Detail Modal & Breakdown View** — *Leaf UI Component* (Can be built in parallel with FEAT-02)
4. **FEAT-03: Instant Search & Multi-Tag Filtering** — *Client-side Navigation*
5. **FEAT-04: Multi-Field Sorting** — *Client-side Navigation*
6. **FEAT-06: Pre-Aggregated Leaderboards & Curated Views** — *Analytics Views*
7. **FEAT-07: Read-Only Edge Deployment & Accessibility (WCAG AA)** — *Compliance & Production Launch*

---

## 2. Dependency Map (What Blocks What)

### Detailed Blocking Relationships:
* **FEAT-01 blocks FEAT-02, FEAT-05, and FEAT-06:** The frontend UI components, data structures, and leaderboard calculations require the normalized schema exported by `thread.py` (`processed_characters.json`).
* **FEAT-02 blocks FEAT-03 and FEAT-04:** Search and sorting manipulate the active character card array rendered within the catalog grid.
* **FEAT-01 through FEAT-06 block FEAT-07:** The global accessibility audit, automated testing passes, and CDN deployment bundle all finalized components for launch.

---

## 3. First Feature to Implement and Why

### First Feature: **FEAT-01 (Pre-Calculated Data Pipeline)**

**Why:**
* **Establishes the Data Contract:** FEAT-01 defines the single source of truth for the entire application. The data types, category breakdowns, and `total_games` metric determine how the rest of the application is designed.
* **Unblocks Parallel Work:** Once `processed_characters.json` is exported, frontend team members can immediately build UI layouts (`FEAT-02`), detail views (`FEAT-05`), and analytics dashboards (`FEAT-06`) concurrently without waiting on backend infrastructure.
* **Eliminates Technical Debt Early:** Catching bad schemas, duplicate tags, or corrupted entity records at the ingestion stage prevents writing defensive workarounds into multiple UI components later.

---

## 4. Risks That Could Delay Multiple Features

| Risk | Impacted Features | Impact Description | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Source Schema Volatility** | FEAT-01, FEAT-02, FEAT-05, FEAT-06 | Breaking changes or inconsistent keys in `characters.json` or `enemies.json` break normalization scripts and UI bindings. | Lock the raw JSON schema early; write schema validation assertions in `thread.py` to flag malformed fields immediately. |
| **Client-Side Rendering Lag** | FEAT-02, FEAT-03, FEAT-04 | Rendering 300+ DOM cards simultaneously on lower-end mobile devices can cause input latency during live searches. | Keep the DOM tree light; use CSS Grid without heavy layout wrappers; decouple filter recalculations from render passes. |
| **Modal Focus Trapping Failures** | FEAT-05, FEAT-07 | Improper focus handling or keyboard leaks in modal components will fail WCAG 2.1 AA audits late in development. | Use a proven accessibility dialog pattern from day one; test with keyboard navigation (`Tab`, `Escape`) before expanding layout styling. |
| **Pipeline Drift / Unstable Counts** | FEAT-01, FEAT-04, FEAT-06 | Non-deterministic script execution or inconsistent tie-breaking creates drifting appearance totals across pages. | Ensure `thread.py` is fully idempotent with automated unit tests for tie-breaking and deduplication logic. |
Next steps to complete your documentation:


[ FEAT-01: Data Pipeline ]
│
├───► [ FEAT-06: Leaderboards ] ──────────────┐
│                                             │
▼                                             ▼
[ FEAT-02: Catalog Grid ]                      [ FEAT-05: Detail Modal ]
│                                             ▲
├───► [ FEAT-03: Search & Filters ]           │
│                                             │
└───► [ FEAT-04: Multi-Field Sorting ]        │
│                                             │
└─────────────────────────────────────────────┘
│
▼
[ FEAT-07: Production Edge Deployment & WCAG AA ]