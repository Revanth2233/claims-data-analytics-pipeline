# Claims Data Analytics Pipeline

> **Python · SQL Server · Pandas · Matplotlib · ASP.NET Core · React**

End-to-end data pipeline that processes **500K+ healthcare claims records** from SQL Server, surfaces denial trends, payer performance breakdowns, and processing time distributions — all previously buried in raw billing tables.

---

## 🏗️ Architecture

```
SQL Server (Raw Claims Data)
        │
        ▼
Python + Pandas (ETL Layer)
  - Extract & clean 500K+ records
  - Aggregate denial rates by payer
  - Compute processing time distributions
  - Generate monthly trend reports
        │
        ▼
ASP.NET Core Web API
  - Exposes /analytics endpoints
  - JWT auth + response caching
  - Swagger UI for external consumers
        │
        ▼
React Dashboard
  - Month-over-month claim outcomes
  - Denial rate trends by payer
  - Self-serve for finance team (no SQL access needed)
```

---

## ✨ Key Features

- **500K+ records** processed end-to-end per run
- **Denial rate trends** surfaced by payer and date range
- **Payer performance breakdowns** — average processing time, acceptance rate
- **Self-serve React dashboard** — finance team access without SQL knowledge
- **Secure API** — JWT auth, response caching, Swagger UI for integration

---

## 📊 Impact

| Metric | Result |
|--------|--------|
| Records processed | 500K+ claims |
| Data access model | Self-serve (no SQL required) |
| Pipeline architecture | ETL → REST API → Dashboard |
| Previous state | Insights buried in raw billing tables |

---

## 🗂️ Project Structure

```
claims-data-analytics-pipeline/
├── etl/
│   ├── extract.py          # SQL Server extraction via pyodbc
│   ├── transform.py        # Pandas cleaning & aggregation
│   ├── load.py             # Output to staging tables
│   └── reports/
│       ├── denial_rates.py
│       └── payer_performance.py
├── api/
│   ├── Controllers/
│   │   └── AnalyticsController.cs
│   ├── Services/
│   │   └── ClaimsAnalyticsService.cs
│   └── Program.cs
├── dashboard/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DenialTrendChart.tsx
│   │   │   └── PayerBreakdownTable.tsx
│   │   └── App.tsx
│   └── package.json
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Data extraction | Python, pyodbc, SQL Server |
| Transformation | Pandas, NumPy |
| Visualization | Matplotlib |
| API | ASP.NET Core Web API (C#) |
| Auth | JWT Bearer tokens |
| Frontend | React, TypeScript, Recharts |
| Database | MS SQL Server |

---

## 🚀 Getting Started

```bash
# ETL pipeline
cd etl
pip install -r requirements.txt
python run_pipeline.py --date-range 2024-01-01:2024-12-31

# API
cd api
dotnet restore
dotnet run

# Dashboard
cd dashboard
npm install
npm start
```

---

*Built as part of the healthcare RCM analytics platform at Newport Med India.*
