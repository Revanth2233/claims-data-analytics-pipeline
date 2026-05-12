namespace ClaimsAnalytics.API.Models;

public class ProviderSummary
{
    public int ProviderID { get; set; }
    public string ProviderName { get; set; } = string.Empty;
    public string ProviderSpecialty { get; set; } = string.Empty;
    public int TotalClaims { get; set; }
    public decimal TotalSubmitted { get; set; }
    public decimal TotalAllowed { get; set; }
    public decimal TotalPaid { get; set; }
    public int TotalDenied { get; set; }
    public decimal DenialRate { get; set; }
    public decimal AvgCollectionRate { get; set; }
    public DateTime LoadedAt { get; set; }
}
