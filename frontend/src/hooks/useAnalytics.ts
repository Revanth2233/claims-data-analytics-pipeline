import { useQuery } from '@tanstack/react-query';
import { analyticsApi } from '../services/analyticsApi';

export const useKpi = (startDate?: string, endDate?: string) =>
  useQuery({
    queryKey: ['kpi', startDate, endDate],
    queryFn: () => analyticsApi.getKpi(startDate, endDate),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

export const useTopProviders = (topN = 10) =>
  useQuery({
    queryKey: ['providers', 'top', topN],
    queryFn: () => analyticsApi.getTopProviders(topN),
    staleTime: 5 * 60 * 1000,
  });

export const useMonthlyTrends = (year?: number) =>
  useQuery({
    queryKey: ['trends', 'monthly', year],
    queryFn: () => analyticsApi.getMonthlyTrends(year),
    staleTime: 5 * 60 * 1000,
  });
