import { useState, useRef, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { useAuth } from "@/contexts/AuthContext";
import { sendAuthenticatedChatMessage, sendChatMessage } from "@/services/chatApi";
import { useToast } from "@/hooks/use-toast";
import { Bot } from "lucide-react";

interface Message {
  id: number;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export function ChatPanel() {
  const location = useLocation();
  const firstMessage = location.state?.firstMessage;

  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | undefined>();

  const scrollRef = useRef<HTMLDivElement>(null);
  const { user, token } = useAuth();
  const { toast } = useToast();

  // 🔥 Send first message automatically
  useEffect(() => {
    if (firstMessage) {
      handleSend(firstMessage);
    }
  }, [firstMessage]);

  // 🔥 Auto scroll
  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  const handleSend = async (content: string) => {
    const userMsg: Message = {
      id: Date.now(),
      role: "user",
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = token
        ? await sendAuthenticatedChatMessage(
            {
              message: content,
              conversation_id: conversationId,
              user_id: user?.id,
            },
            token
          )
        : await sendChatMessage({
            message: content,
            conversation_id: conversationId,
          });

      setConversationId(response.conversation_id);

      const botMsg: Message = {
        id: Date.now() + 1,
        role: "assistant",
        content: response.message,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (error: any) {
      toast({
        title: "Error",
        description: error.message || "Failed to send message",
        variant: "destructive",
      });

      setMessages((prev) => prev.filter((msg) => msg.id !== userMsg.id));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">

      {/* ===== MESSAGES ===== */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto px-4 pt-6 pb-32 space-y-6"
      >
        {messages.map((msg) => (
          <ChatMessage key={msg.id} {...msg} />
        ))}

        {isLoading && (
          <div className="flex gap-3">
            <Bot className="h-5 w-5 text-primary" />
            <div className="text-sm text-muted-foreground">
              Thinking...
            </div>
          </div>
        )}
      </div>

      {/* ===== INPUT ===== */}
      <div className="fixed bottom-0 left-0 w-full border-t bg-background/80 backdrop-blur p-4">
        <div className="max-w-3xl mx-auto">
          <ChatInput onSend={handleSend} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
}