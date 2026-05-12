using ClaimsAnalytics.API.Models;

namespace ClaimsAnalytics.API.Services;

public interface IClaimsAnalyticsService
{
    Task<KpiSummary> GetKpiSummaryAsync(DateOnly startDate, DateOnly endDate);
    Task<IEnumerable<ProviderSummary>> GetTopProvidersAsync(int topN = 10);
    Task<IEnumerable<MonthlyTrend>> GetMonthlyTrendsAsync(int year);
    Task<IEnumerable<ProviderSummary>> GetProvidersBySpecialtyAsync(string specialty);
}
