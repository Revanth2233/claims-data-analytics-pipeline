-- ============================================================
-- Claims Analytics DB Schema
-- Run in order: 001 → 002 → 003
-- ============================================================
USE ClaimsDB;
GO

-- Source tables
CREATE TABLE dbo.Patients (
    PatientID       INT PRIMARY KEY IDENTITY(1,1),
    FirstName       NVARCHAR(100) NOT NULL,
    LastName        NVARCHAR(100) NOT NULL,
    DateOfBirth     DATE NOT NULL,
    Gender          CHAR(1),
    ZipCode         VARCHAR(10),
    CreatedAt       DATETIME2 DEFAULT GETUTCDATE(),
    IsDeleted       BIT DEFAULT 0
);

CREATE TABLE dbo.Providers (
    ProviderID          INT PRIMARY KEY IDENTITY(1,1),
    ProviderName        NVARCHAR(200) NOT NULL,
    ProviderSpecialty   NVARCHAR(100),
    NPI                 VARCHAR(20),
    TaxID               VARCHAR(20),
    IsActive            BIT DEFAULT 1
);

CREATE TABLE dbo.InsurancePlans (
    PlanID      INT PRIMARY KEY IDENTITY(1,1),
    PlanName    NVARCHAR(200) NOT NULL,
    PlanType    NVARCHAR(50),   -- PPO, HMO, EPO
    PayerID     VARCHAR(50)
);

CREATE TABLE dbo.Claims (
    ClaimID             BIGINT PRIMARY KEY IDENTITY(1,1),
    PatientID           INT NOT NULL REFERENCES dbo.Patients(PatientID),
    ProviderID          INT NOT NULL REFERENCES dbo.Providers(ProviderID),
    InsurancePlanID     INT NOT NULL REFERENCES dbo.InsurancePlans(PlanID),
    ServiceDate         DATE NOT NULL,
    SubmittedDate       DATETIME2 DEFAULT GETUTCDATE(),
    SubmittedAmount     DECIMAL(10,2) NOT NULL,
    AllowedAmount       DECIMAL(10,2),
    PaidAmount          DECIMAL(10,2),
    ClaimStatus         NVARCHAR(50) NOT NULL DEFAULT 'Pending',
    DenialReasonCode    NVARCHAR(20),
    DiagnosisCode       NVARCHAR(20),
    ProcedureCode       NVARCHAR(20),
    IsDeleted           BIT DEFAULT 0,
    INDEX IX_Claims_ServiceDate (ServiceDate),
    INDEX IX_Claims_ProviderID (ProviderID),
    INDEX IX_Claims_Status (ClaimStatus)
);

-- Analytics schema
CREATE SCHEMA analytics;
GO

CREATE TABLE analytics.ClaimsDetail (
    ClaimID             BIGINT,
    PatientID           INT,
    ProviderID          INT,
    ProviderName        NVARCHAR(200),
    ProviderSpecialty   NVARCHAR(100),
    ServiceDate         DATE,
    ServiceYear         INT,
    ServiceMonth        INT,
    ServiceQuarter      INT,
    SubmittedAmount     DECIMAL(10,2),
    AllowedAmount       DECIMAL(10,2),
    PaidAmount          DECIMAL(10,2),
    WriteOffAmount      DECIMAL(10,2),
    CollectionRate      DECIMAL(6,4),
    IsDenied            BIT,
    DenialReasonCode    NVARCHAR(20),
    PatientAge          INT,
    PlanName            NVARCHAR(200),
    PlanType            NVARCHAR(50),
    LoadedAt            DATETIME2 DEFAULT GETUTCDATE()
);

CREATE TABLE analytics.ProviderSummary (
    ProviderID          INT,
    ProviderName        NVARCHAR(200),
    ProviderSpecialty   NVARCHAR(100),
    TotalClaims         INT,
    TotalSubmitted      DECIMAL(12,2),
    TotalAllowed        DECIMAL(12,2),
    TotalPaid           DECIMAL(12,2),
    TotalDenied         INT,
    DenialRate          DECIMAL(6,4),
    AvgCollectionRate   DECIMAL(6,4),
    LoadedAt            DATETIME2 DEFAULT GETUTCDATE()
);

CREATE TABLE analytics.MonthlyTrends (
    ServiceYear     INT,
    ServiceMonth    INT,
    TotalClaims     INT,
    TotalRevenue    DECIMAL(14,2),
    TotalDenied     INT,
    DenialRate      DECIMAL(6,4),
    LoadedAt        DATETIME2 DEFAULT GETUTCDATE()
);
