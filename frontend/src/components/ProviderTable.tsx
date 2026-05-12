import {
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Chip, Typography
} from '@mui/material';
import { useTopProviders } from '../hooks/useAnalytics';

export const ProviderTable = ({ topN = 10 }: { topN?: number }) => {
  const { data, isLoading } = useTopProviders(topN);

  if (isLoading) return <Typography>Loading providers...</Typography>;
  if (!data?.length) return <Typography>No providers found</Typography>;

  return (
    <>
      <Typography variant="h6" gutterBottom>Top Providers by Claim Volume</Typography>
      <TableContainer component={Paper} elevation={1}>
        <Table size="small">
          <TableHead sx={{ bgcolor: '#f5f5f5' }}>
            <TableRow>
              <TableCell><b>Provider</b></TableCell>
              <TableCell><b>Specialty</b></TableCell>
              <TableCell align="right"><b>Claims</b></TableCell>
              <TableCell align="right"><b>Revenue</b></TableCell>
              <TableCell align="right"><b>Collection Rate</b></TableCell>
              <TableCell align="right"><b>Denial Rate</b></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map(p => (
              <TableRow key={p.providerID} hover>
                <TableCell>{p.providerName}</TableCell>
                <TableCell>{p.providerSpecialty}</TableCell>
                <TableCell align="right">{p.totalClaims.toLocaleString()}</TableCell>
                <TableCell align="right">${p.totalPaid.toLocaleString()}</TableCell>
                <TableCell align="right">
                  <Chip
                    label={`${(p.avgCollectionRate * 100).toFixed(1)}%`}
                    size="small"
                    color={p.avgCollectionRate > 0.9 ? 'success' : p.avgCollectionRate > 0.75 ? 'warning' : 'error'}
                  />
                </TableCell>
                <TableCell align="right">
                  <Chip
                    label={`${(p.denialRate * 100).toFixed(1)}%`}
                    size="small"
                    color={p.denialRate < 0.1 ? 'success' : p.denialRate < 0.2 ? 'warning' : 'error'}
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
};
