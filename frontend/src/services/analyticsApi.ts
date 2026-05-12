import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:5000/api',
  timeout: 10000,
});

export interface KpiSummary {
  totalClaims: number;
  totalSubmitted: number;
  totalCollected: number;
  totalDenied: number;
  avgCollectionPct: number;
  denialRatePct: number;
}

export interface ProviderSummary {
  providerID: number;
  providerName: string;
  providerSpecialty: string;
  totalClaims: number;
  totalPaid: number;
  denialRate: number;
  avgCollectionRate: number;
}

export interface MonthlyTrend {
  serviceYear: number;
  serviceMonth: number;
  totalClaims: number;
  totalRevenue: number;
  totalDenied: number;
  denialRate: number;
}

export const analyticsApi = {
  getKpi: (startDate?: string, endDate?: string) =>
    api.get<KpiSummary>('/analytics/kpi', { params: { startDate, endDate } }).then(r => r.data),

  getTopProviders: (topN = 10) =>
    api.get<ProviderSummary[]>('/analytics/providers/top', { params: { topN } }).then(r => r.data),

  getMonthlyTrends: (year?: number) =>
    api.get<MonthlyTrend[]>('/analytics/trends/monthly', { params: { year } }).then(r => r.data),
};
