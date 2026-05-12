using ClaimsAnalytics.API.Services;
using Microsoft.AspNetCore.Mvc;

namespace ClaimsAnalytics.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AnalyticsController(IClaimsAnalyticsService svc, ILogger<AnalyticsController> logger)
    : ControllerBase
{
    /// <summary>Get KPI summary for a date range.</summary>
    [HttpGet("kpi")]
    public async Task<IActionResult> GetKpi(
        [FromQuery] DateOnly? startDate,
        [FromQuery] DateOnly? endDate)
    {
        var start = startDate ?? DateOnly.FromDateTime(DateTime.Today.AddDays(-90));
        var end = endDate ?? DateOnly.FromDateTime(DateTime.Today);
        var result = await svc.GetKpiSummaryAsync(start, end);
        return Ok(result);
    }

    /// <summary>Get top N providers by claim volume.</summary>
    [HttpGet("providers/top")]
    public async Task<IActionResult> GetTopProviders([FromQuery] int topN = 10)
    {
        if (topN < 1 || topN > 100) return BadRequest("topN must be between 1 and 100");
        return Ok(await svc.GetTopProvidersAsync(topN));
    }

    /// <summary>Get monthly revenue and denial trends for a year.</summary>
    [HttpGet("trends/monthly")]
    public async Task<IActionResult> GetMonthlyTrends([FromQuery] int? year)
    {
        var targetYear = year ?? DateTime.Today.Year;
        return Ok(await svc.GetMonthlyTrendsAsync(targetYear));
    }

    /// <summary>Get providers filtered by specialty.</summary>
    [HttpGet("providers/specialty/{specialty}")]
    public async Task<IActionResult> GetBySpecialty(string specialty)
    {
        if (string.IsNullOrWhiteSpace(specialty)) return BadRequest();
        return Ok(await svc.GetProvidersBySpecialtyAsync(specialty));
    }
}
