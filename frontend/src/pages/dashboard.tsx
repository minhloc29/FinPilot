import React from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import PortfolioPanel from '../components/PortfolioPanel';
import { usePortfolio } from '../hooks/usePortfolio';

const Dashboard: NextPage = () => {
  const { holdings, totalValue, totalChange } = usePortfolio();

  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>Dashboard - AI Financial Copilot</title>
        <meta name="description" content="Portfolio dashboard" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">
            Monitor your portfolio and market performance
          </p>
        </header>

        {/* Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Portfolio Panel */}
          <div className="lg:col-span-2">
            <PortfolioPanel
              holdings={holdings}
              totalValue={totalValue}
              totalChange={totalChange}
            />
          </div>

          {/* Stats Panel */}
          <div className="space-y-6">
            {/* Performance Card */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                Performance
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Today</span>
                  <span className="text-green-600">+2.45%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">This Week</span>
                  <span className="text-green-600">+5.12%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">This Month</span>
                  <span className="text-red-600">-1.23%</span>
                </div>
              </div>
            </div>

            {/* Market News Card */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                Market News
              </h3>
              <div className="space-y-3 text-sm">
                <div className="pb-3 border-b">
                  <p className="text-gray-700 font-medium">
                    Tech stocks rally...
                  </p>
                  <p className="text-gray-500 text-xs mt-1">2 hours ago</p>
                </div>
                <div className="pb-3 border-b">
                  <p className="text-gray-700 font-medium">
                    Fed maintains rates...
                  </p>
                  <p className="text-gray-500 text-xs mt-1">4 hours ago</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
