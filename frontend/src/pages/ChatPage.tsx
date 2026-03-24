import { ChatPanel } from "@/components/chat/ChatPanel";
import { Sidebar } from "@/components/chat/Sidebar";

export default function ChatPage() {
  return (
    <div className="relative flex h-screen w-full overflow-hidden 
    bg-gradient-to-br from-purple-50 via-blue-50 to-orange-50">

      {/* ===== BACKGROUND BLOBS (same as landing) ===== */}
      <div className="absolute w-[500px] h-[500px] 
      bg-purple-300 rounded-full blur-[120px] opacity-20 
      top-10 left-[-150px]" />

      <div className="absolute w-[400px] h-[400px] 
      bg-blue-300 rounded-full blur-[120px] opacity-20 
      top-40 right-[-120px]" />

      <div className="absolute w-[350px] h-[350px] 
      bg-orange-200 rounded-full blur-[120px] opacity-20 
      bottom-0 left-[30%]" />

      {/* ===== MAIN LAYOUT ===== */}
      <div className="relative z-10 flex w-full h-full">

        {/* ===== SIDEBAR ===== */}
        <div className="w-72 h-full border-r 
        bg-white/70 backdrop-blur-xl 
        flex flex-col shadow-lg">

          <Sidebar />

        </div>

        {/* ===== CHAT AREA ===== */}
        <div className="flex-1 flex flex-col items-center justify-center">

          {/* Chat container */}
          <div className="w-full max-w-4xl h-full flex flex-col">

            <ChatPanel />

          </div>

        </div>
      </div>
    </div>
  );
}