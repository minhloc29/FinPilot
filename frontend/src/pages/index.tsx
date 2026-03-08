import { ChatPanel } from "@/components/chat/ChatPanel";
import { Navbar } from "@/components/layout/Navbar";
import { TrendingUp, DollarSign, BarChart3, Wallet } from "lucide-react";
import { AboutSection } from "@/components/landing/AboutSection";


const Index = () => {
  return (
    <div className="flex flex-col min-h-screen w-full 
    bg-gradient-to-br from-purple-50 via-blue-50 to-orange-50">

      <Navbar />

      <main className="relative flex flex-1 flex-col items-center justify-start pt-24 px-6 overflow-hidden">
      {/* Decorative floating icons */}
      {/* Background glow blobs */}

<div className="absolute w-[500px] h-[500px] 
bg-purple-300 rounded-full blur-[120px] opacity-20 
top-10 left-[-150px] animate-float"></div>

<div className="absolute w-[400px] h-[400px] 
bg-blue-300 rounded-full blur-[120px] opacity-20 
top-40 right-[-120px] animate-float"></div>

<div className="absolute w-[350px] h-[350px] 
bg-orange-200 rounded-full blur-[120px] opacity-20 
bottom-0 left-[30%] animate-float"></div>
<div className="absolute top-20 left-10 text-purple-400 opacity-60">
  <TrendingUp size={32} />
</div>

<div className="absolute top-28 right-16 text-blue-400 opacity-60">
  <DollarSign size={32} />
</div>

<div className="absolute top-[360px] left-20 text-purple-400 opacity-60">
  <BarChart3 size={32} />
</div>

<div className="absolute top-[340px] right-20 text-blue-400 opacity-60">
  <Wallet size={32} />
</div>
        {/* HERO */}
        

        <div className="relative z-10 w-full max-w-2xl mb-24">

  {/* glow background */}
  <div className="absolute inset-0 bg-gradient-to-r from-purple-300 via-blue-300 to-orange-200 
  blur-3xl opacity-30 rounded-full"></div>

  <div className="relative">
    <ChatPanel />
  </div>

</div>

        {/* FEATURES */}
        <AboutSection />
        
         

      </main>

    </div>
  );
};

export default Index;