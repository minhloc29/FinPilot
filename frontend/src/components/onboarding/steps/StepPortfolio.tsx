import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Plus, Trash2 } from "lucide-react";
import type { OnboardingData, PortfolioItem } from "../OnboardingWizard";

interface Props {
  data: OnboardingData;
  update: (d: Partial<OnboardingData>) => void;
}

export function StepPortfolio({ data, update }: Props) {
  const [draft, setDraft] = useState<PortfolioItem>({ ticker: "", shares: 0, avg_price: 0 });

  const addItem = () => {
    if (!draft.ticker.trim() || draft.shares <= 0) return;
    update({ portfolio: [...data.portfolio, { ...draft, ticker: draft.ticker.toUpperCase().trim() }] });
    setDraft({ ticker: "", shares: 0, avg_price: 0 });
  };

  const removeItem = (idx: number) => {
    update({ portfolio: data.portfolio.filter((_, i) => i !== idx) });
  };

  return (
    <div className="space-y-5">
      <p className="text-sm text-muted-foreground">
        Add the stocks or assets you currently own. This is optional but helps the AI give better advice.
      </p>

      {/* Existing items */}
      {data.portfolio.length > 0 && (
        <div className="space-y-2">
          {data.portfolio.map((item, i) => (
            <div
              key={i}
              className="flex items-center gap-3 rounded-xl border border-border bg-background p-3"
            >
              <span className="font-mono font-semibold text-sm text-primary w-16">{item.ticker}</span>
              <span className="text-sm text-muted-foreground flex-1">
                {item.shares} shares @ ${item.avg_price}
              </span>
              <span className="text-sm font-medium text-foreground">
                ${(item.shares * item.avg_price).toLocaleString()}
              </span>
              <Button variant="ghost" size="icon" onClick={() => removeItem(i)} className="h-7 w-7 text-muted-foreground hover:text-destructive">
                <Trash2 className="h-3.5 w-3.5" />
              </Button>
            </div>
          ))}
          <div className="text-right text-xs font-medium text-muted-foreground">
            Total: ${data.portfolio.reduce((s, i) => s + i.shares * i.avg_price, 0).toLocaleString()}
          </div>
        </div>
      )}

      {/* Add form */}
      <div className="rounded-xl border border-dashed border-border p-4 space-y-3">
        <Label className="text-xs font-semibold text-muted-foreground">Add Asset</Label>
        <div className="grid grid-cols-3 gap-3">
          <Input
            placeholder="AAPL"
            value={draft.ticker}
            onChange={(e) => setDraft({ ...draft, ticker: e.target.value })}
            className="font-mono uppercase"
            maxLength={10}
          />
          <Input
            type="number"
            placeholder="Shares"
            min={0}
            value={draft.shares || ""}
            onChange={(e) => setDraft({ ...draft, shares: Number(e.target.value) })}
          />
          <Input
            type="number"
            placeholder="Avg Price"
            min={0}
            value={draft.avg_price || ""}
            onChange={(e) => setDraft({ ...draft, avg_price: Number(e.target.value) })}
          />
        </div>
        <Button variant="outline" size="sm" onClick={addItem} className="gap-1.5 rounded-full">
          <Plus className="h-3.5 w-3.5" /> Add to Portfolio
        </Button>
      </div>
    </div>
  );
}