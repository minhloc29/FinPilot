import { motion } from "framer-motion";
import { TrendingUp, BarChart3, Shield, RefreshCcw } from "lucide-react";
import { ChatInput } from "./ChatInput";

const GOALS = [
  {
    label: "Phân tích danh mục",
    icon: BarChart3,
    prompt: "Analyze my investment portfolio",
  },
  {
    label: "Insight thị trường",
    icon: TrendingUp,
    prompt: "Give me market insights",
  },
  {
    label: "Đánh giá rủi ro",
    icon: Shield,
    prompt: "Assess my portfolio risk",
  },
  {
    label: "Tái cân bằng",
    icon: RefreshCcw,
    prompt: "Help me rebalance my portfolio",
  },
];

export function LandingChatPanel({
  onSend,
}: {
  onSend: (message: string) => void;
}) {
  return (
    <div className="flex flex-col items-center">

      {/* HERO */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col items-center pt-16 pb-10"
      >
        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10 mb-6">
          <TrendingUp className="h-7 w-7 text-primary" />
        </div>

        <h1 className="text-4xl font-bold text-foreground">
          AlphaLens
        </h1>

        <p className="mt-3 text-muted-foreground max-w-md text-center text-sm">
          Trợ lý AI giúp bạn phân tích danh mục đầu tư và ra quyết định tài chính thông minh.
        </p>
      </motion.div>

      {/* INPUT */}
      <div className="w-full mb-8">
        <ChatInput onSend={onSend} />
      </div>

      {/* GOALS */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15 }}
        className="rounded-2xl border border-border bg-card p-6 shadow-sm"
      >
        <h3 className="text-sm font-semibold mb-4">
          Bạn muốn làm gì?
        </h3>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {GOALS.map((goal) => {
            const Icon = goal.icon;

            return (
              <button
                key={goal.label}
                onClick={() => onSend(goal.prompt)}
                className="flex flex-col items-center gap-2 rounded-xl border p-4 hover:bg-accent transition"
              >
                <div className="w-10 h-10 flex items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <Icon className="w-5 h-5" />
                </div>

                <span className="text-xs font-medium text-center">
                  {goal.label}
                </span>
              </button>
            );
          })}
        </div>
      </motion.div>
    </div>
  );
}