import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, ResponsiveContainer
} from 'recharts';
import { Box, Typography, CircularProgress } from '@mui/material';
import { useMonthlyTrends } from '../hooks/useAnalytics';

const MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

export const RevenueTrendChart = ({ year = new Date().getFullYear() }) => {
  const { data, isLoading } = useMonthlyTrends(year);

  if (isLoading) return <Box display="flex" justifyContent="center" p={4}><CircularProgress /></Box>;
  if (!data?.length) return <Typography>No data available</Typography>;

  const chartData = data.map(d => ({
    month: MONTH_NAMES[d.serviceMonth - 1],
    revenue: Math.round(d.totalRevenue),
    claims: d.totalClaims,
    denialRate: +(d.denialRate * 100).toFixed(1),
  }));

  return (
    <Box>
      <Typography variant="h6" gutterBottom>Monthly Revenue & Denial Rate — {year}</Typography>
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis yAxisId="left" tickFormatter={v => `$${(v/1000).toFixed(0)}k`} />
          <YAxis yAxisId="right" orientation="right" tickFormatter={v => `${v}%`} />
          <Tooltip
            formatter={(value, name) =>
              name === 'revenue'
                ? [`$${Number(value).toLocaleString()}`, 'Revenue']
                : name === 'denialRate'
                ? [`${value}%`, 'Denial Rate']
                : [value, 'Claims']
            }
          />
          <Legend />
          <Line yAxisId="left" type="monotone" dataKey="revenue" stroke="#1976d2" strokeWidth={2} dot={false} />
          <Line yAxisId="right" type="monotone" dataKey="denialRate" stroke="#d32f2f" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
};
