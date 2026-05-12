namespace ClaimsAnalytics.API.Models;

public class MonthlyTrend
{
    public int ServiceYear { get; set; }
    public int ServiceMonth { get; set; }
    public int TotalClaims { get; set; }
    public decimal TotalRevenue { get; set; }
    public int TotalDenied { get; set; }
    public decimal DenialRate { get; set; }
}
