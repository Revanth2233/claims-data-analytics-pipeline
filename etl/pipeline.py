"""
Claims Data Analytics ETL Pipeline
Processes 500K+ records from raw SQL Server tables into analytics-ready datasets.
"""
import os
import sys
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# ── Logging ──────────────────────────────────────────────────────────────────
logger.add(
    "logs/pipeline_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)


def get_engine(connection_string: Optional[str] = None):
    """Create SQLAlchemy engine from env or explicit connection string."""
    conn = connection_string or os.getenv(
        "DB_CONNECTION",
        "mssql+pyodbc://sa:Password123!@localhost:1433/ClaimsDB?driver=ODBC+Driver+17+for+SQL+Server",
    )
    return create_engine(conn, fast_executemany=True)


def extract_claims(engine, start_date: str, end_date: str) -> pd.DataFrame:
    """Extract raw claims from source tables."""
    logger.info(f"Extracting claims: {start_date} → {end_date}")
    query = text("""
        SELECT
            c.ClaimID,
            c.PatientID,
            c.ProviderID,
            c.ServiceDate,
            c.SubmittedAmount,
            c.AllowedAmount,
            c.PaidAmount,
            c.ClaimStatus,
            c.DenialReasonCode,
            c.DiagnosisCode,
            c.ProcedureCode,
            c.InsurancePlanID,
            p.FirstName + ' ' + p.LastName AS PatientName,
            p.DateOfBirth,
            pr.ProviderName,
            pr.ProviderSpecialty,
            ip.PlanName,
            ip.PlanType
        FROM dbo.Claims c
        JOIN dbo.Patients p ON p.PatientID = c.PatientID
        JOIN dbo.Providers pr ON pr.ProviderID = c.ProviderID
        JOIN dbo.InsurancePlans ip ON ip.PlanID = c.InsurancePlanID
        WHERE c.ServiceDate BETWEEN :start_date AND :end_date
          AND c.IsDeleted = 0
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"start_date": start_date, "end_date": end_date})
    logger.info(f"Extracted {len(df):,} raw claim records")
    return df


def transform_claims(df: pd.DataFrame) -> pd.DataFrame:
    """Apply business rules, enrichment, and KPI calculations."""
    logger.info("Transforming claims data...")

    # Standardise dates
    df["ServiceDate"] = pd.to_datetime(df["ServiceDate"])
    df["DateOfBirth"] = pd.to_datetime(df["DateOfBirth"])
    df["PatientAge"] = ((datetime.now() - df["DateOfBirth"]).dt.days / 365.25).astype(int)

    # Financial KPIs
    df["AllowedAmount"] = df["AllowedAmount"].fillna(0)
    df["PaidAmount"] = df["PaidAmount"].fillna(0)
    df["WriteOffAmount"] = df["SubmittedAmount"] - df["AllowedAmount"]
    df["DeniedAmount"] = df["AllowedAmount"] - df["PaidAmount"]
    df["CollectionRate"] = (df["PaidAmount"] / df["AllowedAmount"].replace(0, pd.NA)).round(4)
    df["IsDenied"] = df["ClaimStatus"].isin(["Denied", "Partially Denied"])
    df["IsHighValue"] = df["SubmittedAmount"] > 5000

    # Service date parts for time-series analysis
    df["ServiceYear"] = df["ServiceDate"].dt.year
    df["ServiceMonth"] = df["ServiceDate"].dt.month
    df["ServiceQuarter"] = df["ServiceDate"].dt.quarter
    df["DayOfWeek"] = df["ServiceDate"].dt.day_name()

    # Clean denial codes
    df["DenialReasonCode"] = df["DenialReasonCode"].fillna("N/A")

    logger.info(f"Transformed {len(df):,} records | Denial rate: {df['IsDenied'].mean():.1%}")
    return df


def aggregate_by_provider(df: pd.DataFrame) -> pd.DataFrame:
    """Roll up claims to provider-level analytics."""
    return (
        df.groupby(["ProviderID", "ProviderName", "ProviderSpecialty"])
        .agg(
            TotalClaims=("ClaimID", "count"),
            TotalSubmitted=("SubmittedAmount", "sum"),
            TotalAllowed=("AllowedAmount", "sum"),
            TotalPaid=("PaidAmount", "sum"),
            TotalDenied=("IsDenied", "sum"),
            DenialRate=("IsDenied", "mean"),
            AvgCollectionRate=("CollectionRate", "mean"),
        )
        .reset_index()
        .round({"DenialRate": 4, "AvgCollectionRate": 4})
    )


def aggregate_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly trend aggregation for dashboard charts."""
    return (
        df.groupby(["ServiceYear", "ServiceMonth"])
        .agg(
            TotalClaims=("ClaimID", "count"),
            TotalRevenue=("PaidAmount", "sum"),
            TotalDenied=("IsDenied", "sum"),
            DenialRate=("IsDenied", "mean"),
        )
        .reset_index()
        .sort_values(["ServiceYear", "ServiceMonth"])
    )


def load_to_analytics(engine, df_detail: pd.DataFrame, df_provider: pd.DataFrame, df_monthly: pd.DataFrame):
    """Load transformed data into analytics schema."""
    logger.info("Loading data to analytics tables...")
    with engine.begin() as conn:
        # Truncate and reload (full refresh for date range)
        conn.execute(text("TRUNCATE TABLE analytics.ClaimsDetail"))
        conn.execute(text("TRUNCATE TABLE analytics.ProviderSummary"))
        conn.execute(text("TRUNCATE TABLE analytics.MonthlyTrends"))

        df_detail.to_sql("ClaimsDetail", conn, schema="analytics", if_exists="append", index=False, chunksize=5000)
        df_provider.to_sql("ProviderSummary", conn, schema="analytics", if_exists="append", index=False)
        df_monthly.to_sql("MonthlyTrends", conn, schema="analytics", if_exists="append", index=False)

    logger.info(
        f"Loaded: {len(df_detail):,} detail rows | "
        f"{len(df_provider):,} provider rows | "
        f"{len(df_monthly):,} monthly rows"
    )


def run_pipeline(start_date: Optional[str] = None, end_date: Optional[str] = None):
    """Main pipeline entry point."""
    if not start_date:
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    logger.info(f"=== Claims ETL Pipeline START | Range: {start_date} to {end_date} ===")
    try:
        engine = get_engine()
        df_raw = extract_claims(engine, start_date, end_date)
        df_clean = transform_claims(df_raw)
        df_provider = aggregate_by_provider(df_clean)
        df_monthly = aggregate_monthly(df_clean)
        load_to_analytics(engine, df_clean, df_provider, df_monthly)
        logger.info("=== Pipeline completed SUCCESSFULLY ===")
    except Exception as exc:
        logger.exception(f"Pipeline FAILED: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Claims ETL Pipeline")
    parser.add_argument("--start-date", help="Start date YYYY-MM-DD")
    parser.add_argument("--end-date", help="End date YYYY-MM-DD")
    args = parser.parse_args()
    run_pipeline(args.start_date, args.end_date)
