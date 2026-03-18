import { useState, useRef, useEffect } from "react";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { Bot, TrendingUp } from "lucide-react";
import { motion } from "framer-motion";
import { useAuth } from "@/contexts/AuthContext";
import { sendAuthenticatedChatMessage, sendChatMessage } from "@/services/chatApi";
import { useToast } from "@/hooks/use-toast";

interface Message {
  id: number;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | undefined>();
  const scrollRef = useRef<HTMLDivElement>(null);
  const { user, token } = useAuth();
  const { toast } = useToast();

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async (content: string) => {
    console.log("Content: ", content)
    const userMsg: Message = {
      id: Date.now(),
      role: "user",
      content,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      // Call backend API
      const response = token 
  ? await sendAuthenticatedChatMessage(
      { 
        message: content, 
        conversation_id: conversationId,
        user_id: user?.id
      },
      token
    )
  : await sendChatMessage({ 
      message: content,
      conversation_id: conversationId
    });

      // Store conversation ID for continuity
      setConversationId(response.conversation_id);

      const assistantMsg: Message = {
        id: Date.now() + 1,
        role: "assistant",
        content: response.message,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (error: any) {
      console.error("Chat error:", error);
      toast({
        title: "Error",
        description: error.message || "Failed to send message. Please try again.",
        variant: "destructive",
      });
      
      // Remove the user message if there was an error
      setMessages((prev) => prev.filter((msg) => msg.id !== userMsg.id));
    } finally {
      setIsLoading(false);
    }
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
            Mở khóa tiềm năng tài chính của bạn
          </p>
          {user ? (
            <p className="mt-4 text-center text-muted-foreground max-w-md text-sm leading-relaxed">
              Welcome back, <span className="font-semibold text-foreground">{user.full_name || user.username}</span>! 
              Ready to analyze your portfolio and explore market opportunities?
            </p>
          ) : (
            <p className="mt-4 text-center text-muted-foreground max-w-md text-sm leading-relaxed">
              AlphaLens là trợ lý AI giúp bạn phân tích danh mục đầu tư một cách cá nhân hóa, dựa trên mục tiêu tài chính, khẩu vị rủi ro và tài sản hiện tại của bạn.
            </p>
          )}
        </motion.div>
      )}

      {!hasMessages && (
        <div className="mb-8">
          <ChatInput onSend={handleSend} isLoading={isLoading} />
        </div>
      )}

      {!hasMessages && (
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="rounded-2xl border border-border bg-card p-6 shadow-sm"
        >
          <h3 className="text-sm font-semibold text-foreground mb-4">Mục tiêu của bạn</h3>
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
