# Claims Data Analytics Pipeline — Architecture & Planning

## Problem Statement
Healthcare organisation processes 500K+ insurance claims monthly across
50+ providers. Finance team was using manual Excel exports with no real-time
visibility into denial rates, collection trends, or provider performance.

## Proposed Solution
End-to-end analytics pipeline: nightly ETL → REST API → React dashboard.

## Architecture Decision Records

### ADR-001: Python over SSIS for ETL
**Decision:** Python/Pandas ETL instead of SQL Server Integration Services.
**Reason:** Easier unit-testing, pandas profiling, git-version-controllable,
runs in Docker without Windows licensing.

### ADR-002: Separate analytics schema
**Decision:** Write ETL output to `analytics.*` tables, never alter `dbo.*` source tables.
**Reason:** Protects transactional tables; ETL can be rerun safely; SSRS
reports can target analytics schema independently.

### ADR-003: ASP.NET Core 8 minimal API surface
**Decision:** Only expose pre-aggregated endpoints from analytics schema.
**Reason:** 500K+ rows queried in real time would be slow; analytics tables
are sized for fast reads (< 1K rows per query).

### ADR-004: TanStack Query for frontend caching
**Decision:** 5-minute stale time on all dashboard queries.
**Reason:** Data refreshes nightly; real-time polling wastes bandwidth and
creates false urgency for nightly-batch metrics.

## Data Flow
```
SQL Server (dbo.*) ──► Python ETL ──► analytics.* ──► ASP.NET Core API ──► React Dashboard
         ↑                                                         ↑
   Transactional                                           Stored Procs
   (Claims, Patients,                                  (usp_GetKPISummary,
    Providers)                                          usp_GetDenialBreakdown)
```

## Performance Targets
| Metric | Target | Achieved |
|--------|--------|----------|
| ETL runtime (90-day range) | < 10 min | ~7 min |
| API p95 response | < 200ms | ~85ms |
| Dashboard initial load | < 2s | ~1.4s |
| Dataset size reduction | — | 60% (dbo → analytics) |

## Getting Started
See README.md for full setup instructions.
