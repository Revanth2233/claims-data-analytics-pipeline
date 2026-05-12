"""Unit tests for ETL pipeline transformations (no DB required)."""
import pandas as pd
import pytest
from datetime import datetime
from pipeline import transform_claims, aggregate_by_provider, aggregate_monthly


@pytest.fixture
def sample_claims():
    return pd.DataFrame({
        "ClaimID": [1, 2, 3, 4],
        "PatientID": [101, 102, 103, 104],
        "ProviderID": [10, 10, 11, 11],
        "ProviderName": ["Dr. Smith", "Dr. Smith", "Dr. Jones", "Dr. Jones"],
        "ProviderSpecialty": ["Cardiology", "Cardiology", "Orthopedics", "Orthopedics"],
        "ServiceDate": ["2024-01-15", "2024-02-20", "2024-01-10", "2024-03-05"],
        "SubmittedAmount": [1000.0, 5500.0, 800.0, 3200.0],
        "AllowedAmount": [900.0, 5000.0, 750.0, 0.0],
        "PaidAmount": [900.0, 4500.0, 750.0, 0.0],
        "ClaimStatus": ["Paid", "Partially Denied", "Paid", "Denied"],
        "DenialReasonCode": [None, "CO-97", None, "CO-4"],
        "DiagnosisCode": ["I21.0", "I21.9", "M54.5", "M17.11"],
        "ProcedureCode": ["93010", "93000", "27447", "27447"],
        "InsurancePlanID": [1, 2, 1, 3],
        "PatientName": ["John Doe", "Jane Smith", "Bob Brown", "Alice Green"],
        "DateOfBirth": ["1970-05-01", "1985-08-15", "1960-03-20", "1990-11-30"],
        "PlanName": ["Blue Shield", "Aetna", "Blue Shield", "Cigna"],
        "PlanType": ["PPO", "HMO", "PPO", "EPO"],
    })


def test_transform_adds_kpi_columns(sample_claims):
    result = transform_claims(sample_claims)
    assert "CollectionRate" in result.columns
    assert "IsDenied" in result.columns
    assert "WriteOffAmount" in result.columns
    assert "PatientAge" in result.columns


def test_denial_flag_correct(sample_claims):
    result = transform_claims(sample_claims)
    assert result.loc[result["ClaimID"] == 1, "IsDenied"].values[0] == False
    assert result.loc[result["ClaimID"] == 2, "IsDenied"].values[0] == True
    assert result.loc[result["ClaimID"] == 4, "IsDenied"].values[0] == True


def test_denial_code_null_filled(sample_claims):
    result = transform_claims(sample_claims)
    assert result["DenialReasonCode"].isna().sum() == 0


def test_provider_aggregation(sample_claims):
    df = transform_claims(sample_claims)
    agg = aggregate_by_provider(df)
    assert len(agg) == 2  # 2 providers
    smith = agg[agg["ProviderName"] == "Dr. Smith"].iloc[0]
    assert smith["TotalClaims"] == 2
    assert smith["TotalDenied"] == 1


def test_monthly_aggregation(sample_claims):
    df = transform_claims(sample_claims)
    monthly = aggregate_monthly(df)
    assert "TotalRevenue" in monthly.columns
    # Jan has 2 claims, Feb has 1, Mar has 1
    jan = monthly[(monthly["ServiceYear"] == 2024) & (monthly["ServiceMonth"] == 1)]
    assert jan["TotalClaims"].values[0] == 2
