import React from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import ChatWindow from '../components/ChatWindow';
import { useChat } from '../hooks/useChat';

const Home: NextPage = () => {
  const { messages, sendMessage, isLoading } = useChat();

  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>AI Financial Copilot</title>
        <meta name="description" content="AI-powered financial assistant" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AI Financial Copilot
          </h1>
          <p className="text-gray-600">
            Your intelligent assistant for financial analysis and portfolio management
          </p>
        </header>

        {/* Chat Interface */}
        <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg h-[600px]">
          <ChatWindow
            messages={messages}
            onSendMessage={sendMessage}
            isLoading={isLoading}
          />
        </div>

        {/* Quick Actions */}
        <div className="max-w-4xl mx-auto mt-6 grid grid-cols-3 gap-4">
          <button className="p-4 bg-white rounded-lg shadow hover:shadow-md transition">
            <div className="text-sm font-semibold text-gray-700">Market Overview</div>
          </button>
          <button className="p-4 bg-white rounded-lg shadow hover:shadow-md transition">
            <div className="text-sm font-semibold text-gray-700">Portfolio Analysis</div>
          </button>
          <button className="p-4 bg-white rounded-lg shadow hover:shadow-md transition">
            <div className="text-sm font-semibold text-gray-700">Risk Assessment</div>
          </button>
        </div>
      </main>
    </div>
  );
};

export default Home;
