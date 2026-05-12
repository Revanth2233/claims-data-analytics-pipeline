using ClaimsAnalytics.API.Data;
using ClaimsAnalytics.API.Models;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;

namespace ClaimsAnalytics.API.Services;

public class ClaimsAnalyticsService(ClaimsDbContext db, ILogger<ClaimsAnalyticsService> logger)
    : IClaimsAnalyticsService
{
    public async Task<KpiSummary> GetKpiSummaryAsync(DateOnly startDate, DateOnly endDate)
    {
        logger.LogInformation("Fetching KPI summary {Start} to {End}", startDate, endDate);
        var result = await db.Database
            .SqlQueryRaw<KpiSummary>(
                "EXEC analytics.usp_GetKPISummary @StartDate, @EndDate",
                new SqlParameter("@StartDate", startDate.ToString("yyyy-MM-dd")),
                new SqlParameter("@EndDate", endDate.ToString("yyyy-MM-dd")))
            .FirstOrDefaultAsync();
        return result ?? new KpiSummary();
    }

    public async Task<IEnumerable<ProviderSummary>> GetTopProvidersAsync(int topN = 10)
    {
        return await db.ProviderSummaries
            .OrderByDescending(p => p.TotalClaims)
            .Take(topN)
            .ToListAsync();
    }

    public async Task<IEnumerable<MonthlyTrend>> GetMonthlyTrendsAsync(int year)
    {
        return await db.MonthlyTrends
            .Where(t => t.ServiceYear == year)
            .OrderBy(t => t.ServiceMonth)
            .ToListAsync();
    }

    public async Task<IEnumerable<ProviderSummary>> GetProvidersBySpecialtyAsync(string specialty)
    {
        return await db.ProviderSummaries
            .Where(p => p.ProviderSpecialty == specialty)
            .OrderByDescending(p => p.TotalClaims)
            .ToListAsync();
    }
}
