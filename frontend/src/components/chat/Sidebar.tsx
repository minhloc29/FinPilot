import { MessageSquare, Plus } from "lucide-react";
import { useState } from "react";

export function Sidebar() {
  const [active, setActive] = useState(0);

 
  return (
    <div className="flex flex-col h-full p-3">

      {/* ===== LOGO / BRAND ===== */}
      <div className="px-3 py-2 mb-4">
        <h1 className="text-lg font-bold text-foreground">
          AlphaLens
        </h1>
        <p className="text-xs text-muted-foreground">
          Trợ lý AI tài chính
        </p>
      </div>

      {/* ===== NEW CHAT BUTTON ===== */}
      <button
        className="flex items-center gap-2 px-3 py-2 mb-4 
        rounded-xl bg-purple-600 text-white 
        hover:bg-purple-700 transition shadow-md"
      >
        <Plus className="w-4 h-4" />
        New chat
      </button>

      {/* ===== CONVERSATION LIST ===== */}
     

      {/* ===== FOOTER ===== */}
      <div className="pt-3 mt-3 border-t text-xs text-muted-foreground px-2">
        <p>© 2026 AlphaLens</p>
      </div>
    </div>
  );
}