using ClaimsAnalytics.API.Models;
using Microsoft.EntityFrameworkCore;

namespace ClaimsAnalytics.API.Data;

public class ClaimsDbContext(DbContextOptions<ClaimsDbContext> options) : DbContext(options)
{
    public DbSet<ProviderSummary> ProviderSummaries => Set<ProviderSummary>();
    public DbSet<MonthlyTrend> MonthlyTrends => Set<MonthlyTrend>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<ProviderSummary>().ToTable("ProviderSummary", "analytics").HasKey(x => x.ProviderID);
        modelBuilder.Entity<MonthlyTrend>().ToTable("MonthlyTrends", "analytics").HasKey(x => new { x.ServiceYear, x.ServiceMonth });
    }
}
