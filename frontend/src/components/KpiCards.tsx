import { Grid, Card, CardContent, Typography, Skeleton, Box } from '@mui/material';
import { useKpi } from '../hooks/useAnalytics';

interface KpiCardProps {
  label: string;
  value: string;
  color?: string;
}

const KpiCard = ({ label, value, color = '#1976d2' }: KpiCardProps) => (
  <Card elevation={2} sx={{ borderTop: `4px solid ${color}` }}>
    <CardContent>
      <Typography variant="body2" color="text.secondary" gutterBottom>{label}</Typography>
      <Typography variant="h5" fontWeight={700} color={color}>{value}</Typography>
    </CardContent>
  </Card>
);

const fmt = (n: number, style: 'currency' | 'percent' | 'decimal' = 'decimal') => {
  if (style === 'currency') return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n);
  if (style === 'percent') return `${n.toFixed(1)}%`;
  return new Intl.NumberFormat('en-US').format(n);
};

export const KpiCards = () => {
  const { data, isLoading } = useKpi();

  if (isLoading) return (
    <Grid container spacing={2}>
      {[...Array(6)].map((_, i) => (
        <Grid item xs={12} sm={6} md={2} key={i}>
          <Skeleton variant="rectangular" height={100} />
        </Grid>
      ))}
    </Grid>
  );

  if (!data) return null;

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} sm={6} md={2}>
        <KpiCard label="Total Claims" value={fmt(data.totalClaims)} color="#1976d2" />
      </Grid>
      <Grid item xs={12} sm={6} md={2}>
        <KpiCard label="Submitted" value={fmt(data.totalSubmitted, 'currency')} color="#388e3c" />
      </Grid>
      <Grid item xs={12} sm={6} md={2}>
        <KpiCard label="Collected" value={fmt(data.totalCollected, 'currency')} color="#2e7d32" />
      </Grid>
      <Grid item xs={12} sm={6} md={2}>
        <KpiCard label="Denied" value={fmt(data.totalDenied)} color="#d32f2f" />
      </Grid>
      <Grid item xs={12} sm={6} md={2}>
        <KpiCard label="Collection Rate" value={fmt(data.avgCollectionPct, 'percent')} color="#7b1fa2" />
      </Grid>
      <Grid item xs={12} sm={6} md={2}>
        <KpiCard label="Denial Rate" value={fmt(data.denialRatePct, 'percent')} color="#f57c00" />
      </Grid>
    </Grid>
  );
};
