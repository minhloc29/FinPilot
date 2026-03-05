import { useState, useEffect } from 'react';
import { portfolioAPI } from '../services/api';

interface Holding {
  symbol: string;
  shares: number;
  value: number;
  change: number;
  changePercent: number;
}

export const usePortfolio = () => {
  const [holdings, setHoldings] = useState<Holding[]>([]);
  const [totalValue, setTotalValue] = useState(0);
  const [totalChange, setTotalChange] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadPortfolio();
  }, []);

  const loadPortfolio = async () => {
    setIsLoading(true);
    try {
      // TODO: Replace with actual user ID from auth
      const portfolios = await portfolioAPI.list('demo_user');
      
      if (portfolios.length > 0) {
        const portfolio = portfolios[0];
        
        // Mock data - in production, fetch real-time prices
        const mockHoldings: Holding[] = [
          {
            symbol: 'AAPL',
            shares: 10,
            value: 1750,
            change: 25,
            changePercent: 1.45,
          },
          {
            symbol: 'GOOGL',
            shares: 5,
            value: 750,
            change: -12,
            changePercent: -1.57,
          },
          {
            symbol: 'MSFT',
            shares: 15,
            value: 4500,
            change: 85,
            changePercent: 1.92,
          },
        ];

        setHoldings(mockHoldings);
        
        const total = mockHoldings.reduce((sum, h) => sum + h.value, 0);
        setTotalValue(total);
        
        const avgChange =
          mockHoldings.reduce((sum, h) => sum + h.changePercent, 0) /
          mockHoldings.length;
        setTotalChange(avgChange);
      }
    } catch (error) {
      console.error('Error loading portfolio:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    holdings,
    totalValue,
    totalChange,
    isLoading,
    reload: loadPortfolio,
  };
};
