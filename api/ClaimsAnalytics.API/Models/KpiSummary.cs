namespace ClaimsAnalytics.API.Models;

public class KpiSummary
{
    public int TotalClaims { get; set; }
    public decimal TotalSubmitted { get; set; }
    public decimal TotalCollected { get; set; }
    public int TotalDenied { get; set; }
    public decimal AvgCollectionPct { get; set; }
    public decimal DenialRatePct { get; set; }
}
