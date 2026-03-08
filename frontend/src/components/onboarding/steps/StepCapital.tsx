import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type { OnboardingData } from "../OnboardingWizard";

interface Props {
  data: OnboardingData;
  update: (d: Partial<OnboardingData>) => void;
}

export function StepCapital({ data, update }: Props) {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <Label>Total Investment Capital ($)</Label>
        <Input
          type="number"
          min={0}
          value={data.capital || ""}
          onChange={(e) => update({ capital: Number(e.target.value) })}
          placeholder="100,000"
        />
      </div>

      <div className="space-y-2">
        <Label>Monthly Investment ($)</Label>
        <Input
          type="number"
          min={0}
          value={data.monthly_investment || ""}
          onChange={(e) => update({ monthly_investment: Number(e.target.value) })}
          placeholder="1,000"
        />
      </div>

      <div className="space-y-2">
        <Label>Rebalance Frequency</Label>
        <Select value={data.rebalance_frequency} onValueChange={(v) => update({ rebalance_frequency: v })}>
          <SelectTrigger><SelectValue /></SelectTrigger>
          <SelectContent>
            <SelectItem value="monthly">📅 Monthly</SelectItem>
            <SelectItem value="quarterly">📆 Quarterly</SelectItem>
            <SelectItem value="semi-annually">🗓️ Semi-Annually</SelectItem>
            <SelectItem value="annually">📋 Annually</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-3">
        <Label className="text-sm font-semibold">
          Emergency Fund: <span className="text-primary">{data.emergency_fund_months} months</span>
        </Label>
        <p className="text-xs text-muted-foreground">
          How many months of expenses do you keep as emergency savings?
        </p>
        <Slider
          value={[data.emergency_fund_months]}
          onValueChange={([v]) => update({ emergency_fund_months: v })}
          min={0}
          max={24}
          step={1}
        />
        <div className="flex justify-between text-[10px] text-muted-foreground">
          <span>None</span>
          <span>24 months</span>
        </div>
      </div>
    </div>
  );
}
