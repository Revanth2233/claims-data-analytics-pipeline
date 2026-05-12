USE ClaimsDB;
GO

-- Get denial breakdown by reason code and month
CREATE OR ALTER PROCEDURE analytics.usp_GetDenialBreakdown
    @StartDate  DATE,
    @EndDate    DATE
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        DenialReasonCode,
        ServiceYear,
        ServiceMonth,
        COUNT(*) AS DenialCount,
        SUM(AllowedAmount) AS DeniedAmount,
        CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS PctOfTotal
    FROM analytics.ClaimsDetail
    WHERE IsDenied = 1
      AND ServiceDate BETWEEN @StartDate AND @EndDate
    GROUP BY DenialReasonCode, ServiceYear, ServiceMonth
    ORDER BY DenialCount DESC;
END;
GO

-- KPI summary for dashboard
CREATE OR ALTER PROCEDURE analytics.usp_GetKPISummary
    @StartDate  DATE,
    @EndDate    DATE
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        COUNT(*)                                AS TotalClaims,
        SUM(SubmittedAmount)                    AS TotalSubmitted,
        SUM(PaidAmount)                         AS TotalCollected,
        SUM(CASE WHEN IsDenied=1 THEN 1 ELSE 0 END) AS TotalDenied,
        CAST(AVG(CollectionRate)*100 AS DECIMAL(5,2)) AS AvgCollectionPct,
        CAST(SUM(CASE WHEN IsDenied=1 THEN 1 ELSE 0 END)*100.0/COUNT(*) AS DECIMAL(5,2)) AS DenialRatePct
    FROM analytics.ClaimsDetail
    WHERE ServiceDate BETWEEN @StartDate AND @EndDate;
END;
GO
