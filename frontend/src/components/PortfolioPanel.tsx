import React from 'react';

interface Holding {
  symbol: string;
  shares: number;
  value: number;
  change: number;
  changePercent: number;
}

interface PortfolioPanelProps {
  holdings: Holding[];
  totalValue: number;
  totalChange: number;
}

const PortfolioPanel: React.FC<PortfolioPanelProps> = ({
  holdings,
  totalValue,
  totalChange,
}) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Portfolio</h2>
        <div className="mt-2">
          <div className="text-3xl font-bold text-gray-900">
            ${totalValue.toLocaleString('en-US', { minimumFractionDigits: 2 })}
          </div>
          <div
            className={`text-sm ${
              totalChange >= 0 ? 'text-green-600' : 'text-red-600'
            }`}
          >
            {totalChange >= 0 ? '+' : ''}
            {totalChange.toFixed(2)}%
          </div>
        </div>
      </div>

      {/* Holdings List */}
      <div className="space-y-3">
        {holdings.map((holding) => (
          <div
            key={holding.symbol}
            className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
          >
            <div>
              <div className="font-semibold text-gray-800">{holding.symbol}</div>
              <div className="text-sm text-gray-500">
                {holding.shares} shares
              </div>
            </div>
            <div className="text-right">
              <div className="font-semibold text-gray-900">
                ${holding.value.toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </div>
              <div
                className={`text-sm ${
                  holding.change >= 0 ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {holding.change >= 0 ? '+' : ''}
                {holding.changePercent.toFixed(2)}%
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {holdings.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <p>No holdings yet</p>
          <p className="text-sm mt-2">Add stocks to your portfolio to get started</p>
        </div>
      )}

      {/* Add Button */}
      <button className="w-full mt-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        Add Holding
      </button>
    </div>
  );
};

export default PortfolioPanel;
