import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import type { OnboardingData } from "../OnboardingWizard";

interface Props {
  data: OnboardingData;
  update: (d: Partial<OnboardingData>) => void;
}

const RISK_OPTIONS = [
  {
    value: "conservative",
    label: "🛡️ Conservative",
    desc: "Bonds, dividend stocks. Stability first.",
    color: "border-green-300 bg-green-50",
  },
  {
    value: "moderate",
    label: "⚖️ Moderate",
    desc: "Mix of ETFs & stocks. Balanced growth.",
    color: "border-yellow-300 bg-yellow-50",
  },
  {
    value: "aggressive",
    label: "🔥 Aggressive",
    desc: "Growth stocks, crypto. High risk, high reward.",
    color: "border-red-300 bg-red-50",
  },
];

export function StepRisk({ data, update }: Props) {
  return (
    <div className="space-y-6">
      <div className="space-y-3">
        <Label className="text-sm font-semibold">Risk Profile</Label>
        <RadioGroup
          value={data.risk_profile}
          onValueChange={(v) => update({ risk_profile: v as OnboardingData["risk_profile"] })}
          className="grid gap-3"
        >
          {RISK_OPTIONS.map((opt) => (
            <label
              key={opt.value}
              className={`flex items-center gap-3 rounded-xl border p-4 cursor-pointer transition-all hover:shadow-sm ${
                data.risk_profile === opt.value ? opt.color + " shadow-sm" : "border-border bg-background"
              }`}
            >
              <RadioGroupItem value={opt.value} />
              <div>
                <p className="font-medium text-sm text-foreground">{opt.label}</p>
                <p className="text-xs text-muted-foreground">{opt.desc}</p>
              </div>
            </label>
          ))}
        </RadioGroup>
      </div>

      <div className="space-y-3">
        <Label className="text-sm font-semibold">
          Max Drawdown Tolerance: <span className="text-primary">{data.max_drawdown_tolerance}%</span>
        </Label>
        <p className="text-xs text-muted-foreground">
          If your portfolio drops this much, what would you do?
        </p>
        <Slider
          value={[data.max_drawdown_tolerance]}
          onValueChange={([v]) => update({ max_drawdown_tolerance: v })}
          min={5}
          max={50}
          step={5}
        />
        <div className="flex justify-between text-[10px] text-muted-foreground">
          <span>5% — Sell everything</span>
          <span>50% — Buy more!</span>
        </div>
      </div>

      <div className="space-y-3">
        <Label className="text-sm font-semibold">
          Investment Horizon: <span className="text-primary">{data.investment_horizon_years} years</span>
        </Label>
        <Slider
          value={[data.investment_horizon_years]}
          onValueChange={([v]) => update({ investment_horizon_years: v })}
          min={1}
          max={30}
          step={1}
        />
        <div className="flex justify-between text-[10px] text-muted-foreground">
          <span>1 year</span>
          <span>30 years</span>
        </div>
      </div>
    </div>
  );
}