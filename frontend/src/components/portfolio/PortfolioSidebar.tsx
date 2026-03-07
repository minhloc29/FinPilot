import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, PieChart, Activity, Wallet, ChevronRight } from "lucide-react";

interface Holding {
  symbol: string;
  name: string;
  value: number;
  change: number;
  allocation: number;
}

const holdings: Holding[] = [
  { symbol: "AAPL", name: "Apple Inc.", value: 14280, change: 1.2, allocation: 22.4 },
  { symbol: "MSFT", name: "Microsoft", value: 11860, change: 0.8, allocation: 18.6 },
  { symbol: "VOO", name: "S&P 500 ETF", value: 22330, change: 0.5, allocation: 35.0 },
  { symbol: "BTC", name: "Bitcoin", value: 7650, change: -2.1, allocation: 12.0 },
  { symbol: "USD", name: "Cash Reserve", value: 7650, change: 0, allocation: 12.0 },
];

const totalValue = holdings.reduce((sum, h) => sum + h.value, 0);
const totalChange = 1.42;

function HoldingCard({ holding, index }: { holding: Holding; index: number }) {
  const isPositive = holding.change > 0;
  const isNeutral = holding.change === 0;

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.08 }}
      className="group flex items-center justify-between rounded-lg border border-border bg-muted/30 px-3 py-2.5 transition-colors hover:bg-muted/60 cursor-pointer"
    >
      <div className="flex items-center gap-3">
        <div className="flex h-8 w-8 items-center justify-center rounded-md bg-secondary text-xs font-bold font-mono text-secondary-foreground">
          {holding.symbol.slice(0, 2)}
        </div>
        <div>
          <p className="text-sm font-medium text-foreground">{holding.symbol}</p>
          <p className="text-xs text-muted-foreground">{holding.name}</p>
        </div>
      </div>
      <div className="text-right">
        <p className="text-sm font-mono font-medium text-foreground">
          ${holding.value.toLocaleString()}
        </p>
        {!isNeutral && (
          <p className={`text-xs font-mono ${isPositive ? "text-gain" : "text-loss"}`}>
            {isPositive ? "+" : ""}{holding.change}%
          </p>
        )}
      </div>
    </motion.div>
  );
}

export function PortfolioSidebar() {
  return (
    <div className="flex h-full w-80 flex-col border-l border-border bg-card/30">
      {/* Header */}
      <div className="border-b border-border p-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Wallet className="h-4 w-4 text-primary" />
            <h3 className="text-sm font-semibold text-foreground">Portfolio</h3>
          </div>
          <span className="rounded-md bg-primary/10 px-2 py-0.5 text-xs font-mono text-primary">
            Live
          </span>
        </div>

        {/* Total Value */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="mt-4"
        >
          <p className="text-xs text-muted-foreground uppercase tracking-wider">Total Value</p>
          <p className="mt-1 text-2xl font-bold font-mono text-foreground">
            ${totalValue.toLocaleString()}
          </p>
          <div className="mt-1 flex items-center gap-1">
            <TrendingUp className="h-3 w-3 text-gain" />
            <span className="text-sm font-mono text-gain">+{totalChange}%</span>
            <span className="text-xs text-muted-foreground ml-1">today</span>
          </div>
        </motion.div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 gap-2 border-b border-border p-4">
        <div className="rounded-lg bg-muted/40 p-3">
          <div className="flex items-center gap-1.5">
            <Activity className="h-3 w-3 text-muted-foreground" />
            <span className="text-xs text-muted-foreground">Sharpe</span>
          </div>
          <p className="mt-1 text-sm font-mono font-semibold text-foreground">1.82</p>
        </div>
        <div className="rounded-lg bg-muted/40 p-3">
          <div className="flex items-center gap-1.5">
            <PieChart className="h-3 w-3 text-muted-foreground" />
            <span className="text-xs text-muted-foreground">Assets</span>
          </div>
          <p className="mt-1 text-sm font-mono font-semibold text-foreground">5</p>
        </div>
      </div>

      {/* Holdings */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="flex items-center justify-between mb-3">
          <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Holdings
          </p>
          <ChevronRight className="h-3 w-3 text-muted-foreground" />
        </div>
        <div className="space-y-2">
          {holdings.map((holding, i) => (
            <HoldingCard key={holding.symbol} holding={holding} index={i} />
          ))}
        </div>
      </div>

      {/* Allocation Bar */}
      <div className="border-t border-border p-4">
        <p className="text-xs text-muted-foreground mb-2">Allocation</p>
        <div className="flex h-2 overflow-hidden rounded-full">
          {holdings.map((h, i) => {
            const colors = [
              "bg-primary",
              "bg-primary/70",
              "bg-primary/50",
              "bg-warning",
              "bg-muted-foreground/30",
            ];
            return (
              <div
                key={h.symbol}
                className={`${colors[i]} transition-all`}
                style={{ width: `${h.allocation}%` }}
              />
            );
          })}
        </div>
        <div className="mt-2 flex flex-wrap gap-x-3 gap-y-1">
          {holdings.map((h, i) => {
            const dotColors = [
              "bg-primary",
              "bg-primary/70",
              "bg-primary/50",
              "bg-warning",
              "bg-muted-foreground/30",
            ];
            return (
              <div key={h.symbol} className="flex items-center gap-1">
                <span className={`h-1.5 w-1.5 rounded-full ${dotColors[i]}`} />
                <span className="text-xs text-muted-foreground font-mono">
                  {h.symbol} {h.allocation}%
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
