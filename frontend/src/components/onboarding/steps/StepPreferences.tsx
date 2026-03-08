import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import type { OnboardingData } from "../OnboardingWizard";

interface Props {
  data: OnboardingData;
  update: (d: Partial<OnboardingData>) => void;
}

const SECTORS = [
  "AI", "Technology", "Healthcare", "Finance", "Energy",
  "Real Estate", "Consumer", "Crypto", "Green Energy", "Commodities",
];

export function StepPreferences({ data, update }: Props) {
  const toggleSector = (sector: string, list: "preferred_sectors" | "avoid_sectors") => {
    const current = data[list];
    const other = list === "preferred_sectors" ? "avoid_sectors" : "preferred_sectors";
    if (current.includes(sector)) {
      update({ [list]: current.filter((s) => s !== sector) });
    } else {
      update({
        [list]: [...current, sector],
        [other]: data[other].filter((s) => s !== sector),
      });
    }
  };

  return (
    <div className="space-y-6">
      <div className="space-y-3">
        <Label className="text-sm font-semibold">Preferred Sectors</Label>
        <p className="text-xs text-muted-foreground">Tap to select sectors you'd like to invest in.</p>
        <div className="flex flex-wrap gap-2">
          {SECTORS.map((s) => (
            <button
              key={s}
              onClick={() => toggleSector(s, "preferred_sectors")}
              className={`rounded-full px-3 py-1.5 text-xs font-medium border transition-colors ${
                data.preferred_sectors.includes(s)
                  ? "bg-primary text-primary-foreground border-primary"
                  : "bg-background text-muted-foreground border-border hover:border-primary/50"
              }`}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-3">
        <Label className="text-sm font-semibold">Sectors to Avoid</Label>
        <div className="flex flex-wrap gap-2">
          {SECTORS.map((s) => (
            <button
              key={s}
              onClick={() => toggleSector(s, "avoid_sectors")}
              className={`rounded-full px-3 py-1.5 text-xs font-medium border transition-colors ${
                data.avoid_sectors.includes(s)
                  ? "bg-destructive text-destructive-foreground border-destructive"
                  : "bg-background text-muted-foreground border-border hover:border-destructive/50"
              }`}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-4 pt-2">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-foreground">Dividend Preference</p>
            <p className="text-xs text-muted-foreground">Prefer stocks that pay dividends</p>
          </div>
          <Switch
            checked={data.dividend_preference}
            onCheckedChange={(v) => update({ dividend_preference: v })}
          />
        </div>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-foreground">ESG / Sustainable Investing</p>
            <p className="text-xs text-muted-foreground">Focus on environmentally responsible companies</p>
          </div>
          <Switch
            checked={data.esg_preference}
            onCheckedChange={(v) => update({ esg_preference: v })}
          />
        </div>
      </div>
    </div>
  );
}