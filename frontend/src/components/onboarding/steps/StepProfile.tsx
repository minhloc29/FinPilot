import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type { OnboardingData } from "../OnboardingWizard";

interface Props {
  data: OnboardingData;
  update: (d: Partial<OnboardingData>) => void;
}

const GOALS = [
  { value: "wealth_growth", label: "💹 Wealth Growth" },
  { value: "retirement", label: "🏖️ Retirement" },
  { value: "passive_income", label: "💵 Passive Income" },
  { value: "saving_house", label: "🏠 Saving for House" },
  { value: "education_fund", label: "🎓 Education Fund" },
];

export function StepProfile({ data, update }: Props) {
  return (
    <div className="space-y-5">
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label>Age</Label>
          <Input
            type="number"
            min={18}
            max={100}
            value={data.age || ""}
            onChange={(e) => update({ age: Number(e.target.value) })}
            placeholder="28"
          />
        </div>
        <div className="space-y-2">
          <Label>Country</Label>
          <Input
            value={data.country}
            onChange={(e) => update({ country: e.target.value })}
            placeholder="Vietnam"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label>Investment Experience</Label>
        <Select
          value={data.investment_experience}
          onValueChange={(v) => update({ investment_experience: v as OnboardingData["investment_experience"] })}
        >
          <SelectTrigger><SelectValue /></SelectTrigger>
          <SelectContent>
            <SelectItem value="beginner">🌱 Beginner</SelectItem>
            <SelectItem value="intermediate">📈 Intermediate</SelectItem>
            <SelectItem value="advanced">🚀 Advanced</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label>Annual Income ($)</Label>
          <Input
            type="number"
            min={0}
            value={data.annual_income || ""}
            onChange={(e) => update({ annual_income: Number(e.target.value) })}
            placeholder="50,000"
          />
        </div>
        <div className="space-y-2">
          <Label>Monthly Savings ($)</Label>
          <Input
            type="number"
            min={0}
            value={data.monthly_savings || ""}
            onChange={(e) => update({ monthly_savings: Number(e.target.value) })}
            placeholder="500"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label>Financial Goal</Label>
        <Select value={data.financial_goal} onValueChange={(v) => update({ financial_goal: v })}>
          <SelectTrigger><SelectValue /></SelectTrigger>
          <SelectContent>
            {GOALS.map((g) => (
              <SelectItem key={g.value} value={g.value}>{g.label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
