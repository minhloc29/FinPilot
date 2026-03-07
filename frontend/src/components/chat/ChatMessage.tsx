import ReactMarkdown from "react-markdown";
import { motion } from "framer-motion";
import { Bot, User } from "lucide-react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  timestamp?: Date;
}

export function ChatMessage({ role, content, timestamp }: ChatMessageProps) {
  const isAssistant = role === "assistant";

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 ${isAssistant ? "" : "flex-row-reverse"}`}
    >
      <div
        className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${
          isAssistant
            ? "bg-primary/10 text-primary"
            : "bg-secondary text-secondary-foreground"
        }`}
      >
        {isAssistant ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
      </div>

      <div
        className={`max-w-[75%] rounded-xl px-4 py-3 ${
          isAssistant
            ? "bg-card border border-border shadow-sm"
            : "bg-primary text-primary-foreground"
        }`}
      >
        <div className={`prose prose-sm max-w-none text-sm leading-relaxed ${
          isAssistant 
            ? "[&_p]:text-foreground [&_strong]:text-foreground [&_h1]:text-foreground [&_h2]:text-foreground [&_h3]:text-foreground [&_li]:text-foreground [&_a]:text-primary [&_code]:text-primary [&_code]:bg-muted"
            : "[&_p]:text-primary-foreground [&_strong]:text-primary-foreground [&_li]:text-primary-foreground [&_code]:text-primary-foreground"
        } [&_code]:font-mono [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:rounded`}>
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
        {timestamp && (
          <p className={`mt-2 text-xs font-mono ${isAssistant ? "text-muted-foreground" : "text-primary-foreground/70"}`}>
            {timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
          </p>
        )}
      </div>
    </motion.div>
  );
}
