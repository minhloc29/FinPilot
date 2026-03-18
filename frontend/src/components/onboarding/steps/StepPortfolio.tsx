import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";
import type { OnboardingData, PortfolioItem } from "../OnboardingWizard";

interface Props {
  data: OnboardingData;
  update: (d: Partial<OnboardingData>) => void;
}

export function StepPortfolio({ data, update }: Props) {

  const updateItem = (index: number, field: keyof PortfolioItem, value: string | number) => {
    const newPortfolio = data.portfolio.map((item, i) =>
      i === index ? { ...item, [field]: value } : item
    );

    update({ portfolio: newPortfolio });
  };

  const addRow = () => {
    update({
      portfolio: [...data.portfolio, { ticker: "", shares: 0, avg_price: 0 }]
    });
  };

  const removeItem = (index: number) => {
    update({
      portfolio: data.portfolio.filter((_, i) => i !== index)
    });
  };

  const total = data.portfolio.reduce(
    (s, i) => s + i.shares * i.avg_price,
    0
  );

  return (
    <div className="space-y-6">

      <p className="text-sm text-muted-foreground">
        Add the stocks or assets you currently own. This helps the AI provide
        better portfolio advice.
      </p>

      <div className="space-y-3">

        {data.portfolio.map((item, i) => (
          <div
            key={i}
            className="grid grid-cols-4 gap-3 items-center rounded-xl border border-border p-3"
          >

            <Input
              placeholder="AAPL"
              value={item.ticker}
              onChange={(e) =>
                updateItem(i, "ticker", e.target.value.toUpperCase())
              }
              className="font-mono uppercase"
            />

            <Input
              type="number"
              min={0}
              placeholder="Shares"
              value={item.shares || ""}
              onChange={(e) =>
                updateItem(i, "shares", Number(e.target.value))
              }
            />

            <Input
              type="number"
              min={0}
              placeholder="Avg Price"
              value={item.avg_price || ""}
              onChange={(e) =>
                updateItem(i, "avg_price", Number(e.target.value))
              }
            />

            <Button
              variant="ghost"
              size="icon"
              onClick={() => removeItem(i)}
              className="text-muted-foreground hover:text-destructive"
            >
              <Trash2 className="h-4 w-4" />
            </Button>

          </div>
        ))}

      </div>

      <Button
        variant="outline"
        size="sm"
        onClick={addRow}
        className="rounded-full"
      >
        Add Asset
      </Button>

      {data.portfolio.length > 0 && (
        <div className="text-right text-sm font-semibold text-muted-foreground">
          Total Value: ${total.toLocaleString()}
        </div>
      )}

    </div>
  );
}