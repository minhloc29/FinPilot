import { useState, useRef, useEffect } from "react";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { Bot, TrendingUp } from "lucide-react";
import { motion } from "framer-motion";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

const MOCK_RESPONSES: Record<string, string> = {
  default: `Based on your current portfolio allocation, here's my analysis:

| Asset | Weight | 1D Change |
|-------|--------|-----------|
| AAPL  | 22.4%  | +1.2%     |
| MSFT  | 18.6%  | +0.8%     |
| VOO   | 35.0%  | +0.5%     |
| BTC   | 12.0%  | -2.1%     |
| Cash  | 12.0%  | —         |

Your portfolio is **up 0.6% today**. The tech-heavy allocation is performing well, but I'd recommend considering more diversification into international markets. Would you like me to suggest some rebalancing options?`,
};

export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = (content: string) => {
    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    setTimeout(() => {
      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: MOCK_RESPONSES.default,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
      setIsLoading(false);
    }, 1200);
  };

  const hasMessages = messages.length > 0;

  return (
    <div className="flex flex-col">
      {/* Hero / Welcome area */}
      {!hasMessages && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col items-center pt-16 pb-10"
        >
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10 glow-primary mb-6">
            <TrendingUp className="h-7 w-7 text-primary" />
          </div>
          <h1 className="text-4xl font-bold text-foreground tracking-tight">AlphaLens</h1>
          <p className="mt-2 text-sm font-semibold uppercase tracking-[0.2em] text-primary">
            Unlock Your Financial Potential
          </p>
          <p className="mt-4 text-center text-muted-foreground max-w-md text-sm leading-relaxed">
            AI-powered portfolio analysis, market insights, risk assessment, and rebalancing — all in one conversation.
          </p>
        </motion.div>
      )}

      {/* Search / Input when no messages */}
      {!hasMessages && (
        <div className="mb-8">
          <ChatInput onSend={handleSend} isLoading={isLoading} />
        </div>
      )}

      {/* Goal section when no messages */}
      {!hasMessages && (
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="rounded-2xl border border-border bg-card p-6 shadow-sm"
        >
          <h3 className="text-sm font-semibold text-foreground mb-4">What's your goal?</h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Portfolio Analysis", emoji: "📊" },
              { label: "Market Insights", emoji: "📈" },
              { label: "Risk Assessment", emoji: "🛡️" },
              { label: "Rebalancing", emoji: "⚖️" },
            ].map((goal) => (
              <button
                key={goal.label}
                onClick={() => handleSend(`Help me with ${goal.label.toLowerCase()}`)}
                className="flex flex-col items-center gap-2 rounded-xl border border-border bg-background p-4 text-sm text-foreground hover:border-primary hover:bg-accent transition-colors"
              >
                <span className="text-2xl">{goal.emoji}</span>
                <span className="font-medium text-xs">{goal.label}</span>
              </button>
            ))}
          </div>
        </motion.div>
      )}

      {/* Messages */}
      {hasMessages && (
        <>
          <div ref={scrollRef} className="flex-1 overflow-y-auto space-y-6 mb-4 max-h-[60vh]">
            {messages.map((msg) => (
              <ChatMessage
                key={msg.id}
                role={msg.role}
                content={msg.content}
                timestamp={msg.timestamp}
              />
            ))}
            {isLoading && (
              <div className="flex gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <Bot className="h-4 w-4" />
                </div>
                <div className="rounded-xl border border-border bg-card px-4 py-3">
                  <div className="flex gap-1">
                    <span className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: "0ms" }} />
                    <span className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: "150ms" }} />
                    <span className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                </div>
              </div>
            )}
          </div>
          <ChatInput onSend={handleSend} isLoading={isLoading} />
        </>
      )}
    </div>
  );
}
