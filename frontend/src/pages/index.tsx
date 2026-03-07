import { ChatPanel } from "@/components/chat/ChatPanel";
import { Navbar } from "@/components/layout/Navbar";

import { AboutSection } from "@/components/landing/AboutSection";
import { FeatureCard } from "@/components/landing/FeatureCard";
import { Step } from "@/components/landing/Step";

const Index = () => {
  return (
    <div className="flex flex-col min-h-screen w-full 
    bg-gradient-to-br from-purple-50 via-blue-50 to-orange-50">

      <Navbar />

      <main className="flex flex-col items-center px-6 pt-24">

        {/* HERO */}
        <div className="text-center mb-12 max-w-2xl">
          <h1 className="text-4xl font-semibold text-gray-900">
            Your AI Financial Analyst
          </h1>

          <p className="mt-3 text-gray-500">
            Analyze portfolios, market trends, and investment risk in one conversation.
          </p>
        </div>

        <div className="w-full max-w-2xl mb-24">
          <ChatPanel />
        </div>

        {/* FEATURES */}
        <AboutSection />
        
         

      </main>

    </div>
  );
};

export default Index;