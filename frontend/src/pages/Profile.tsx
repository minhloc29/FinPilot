import { useEffect, useState } from "react";
import { Navbar } from "@/components/layout/Navbar";
import { OnboardingData } from "@/components/onboarding/OnboardingWizard";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Link } from "react-router-dom";
import { User, Shield, Briefcase, DollarSign, Settings2, AlertTriangle } from "lucide-react";

const RISK_COLORS: Record<string, string> = {
  conservative: "bg-green-100 text-green-700 border-green-200",
  moderate: "bg-yellow-100 text-yellow-700 border-yellow-200",
  aggressive: "bg-red-100 text-red-700 border-red-200",
};

const GOAL_LABELS: Record<string, string> = {
  wealth_growth: "💹 Wealth Growth",
  retirement: "🏖️ Retirement",
  passive_income: "💵 Passive Income",
  saving_house: "🏠 Saving for House",
  education_fund: "🎓 Education Fund",
};

export default function Profile() {
  const [data, setData] = useState<OnboardingData | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem("finassist_profile");
    if (stored) setData(JSON.parse(stored));
  }, []);

  if (!data) {
    return (
      <div className="flex flex-col min-h-screen w-full bg-background">
        <Navbar />
        <main className="flex flex-1 flex-col items-center justify-center gap-4 px-4">
          <AlertTriangle className="h-12 w-12 text-muted-foreground" />
          <h2 className="text-xl font-bold text-foreground">No Profile Found</h2>
          <p className="text-sm text-muted-foreground">Complete the onboarding to see your profile.</p>
          <Link to="/onboarding">
            <Button className="rounded-full">Get Started</Button>
          </Link>
        </main>
      </div>
    );
  }

  const totalPortfolioValue = data.portfolio.reduce((s, i) => s + i.shares * i.avg_price, 0);

  return (
    <div className="flex flex-col min-h-screen w-full bg-background">
      <Navbar />
      <main className="flex flex-1 justify-center px-4 pt-8 pb-12">
        <div className="w-full max-w-3xl space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-foreground">Hồ sơ</h1>
              <p className="text-sm text-muted-foreground mt-1">Tổng quan tài chính và sở thích đầu tư của bạn</p>
            </div>
            <Link to="/onboarding">
              <Button variant="outline" className="rounded-full gap-2">
                <Settings2 className="h-4 w-4" /> Chỉnh sửa
              </Button>
            </Link>
          </div>

          {/* Personal Info */}
          <Card className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary/10">
                <User className="h-4.5 w-4.5 text-primary" />
              </div>
              <h2 className="text-lg font-semibold text-foreground">Thông tin cá nhân</h2>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              <InfoItem label="Age" value={`${data.age} years`} />
              <InfoItem label="Country" value={data.country || "—"} />
              <InfoItem label="Experience" value={capitalize(data.investment_experience)} />
              <InfoItem label="Annual Income" value={`$${data.annual_income.toLocaleString()}`} />
              <InfoItem label="Monthly Savings" value={`$${data.monthly_savings.toLocaleString()}`} />
              <InfoItem label="Financial Goal" value={GOAL_LABELS[data.financial_goal] || data.financial_goal} />
            </div>
          </Card>

          {/* Risk Profile */}
          <Card className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary/10">
                <Shield className="h-4.5 w-4.5 text-primary" />
              </div>
              <h2 className="text-lg font-semibold text-foreground">Risk Profile</h2>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              <div>
                <p className="text-xs text-muted-foreground mb-1">Risk Tolerance</p>
                <Badge variant="outline" className={RISK_COLORS[data.risk_profile]}>
                  {capitalize(data.risk_profile)}
                </Badge>
              </div>
              <InfoItem label="Max Drawdown" value={`${data.max_drawdown_tolerance}%`} />
              <InfoItem label="Investment Horizon" value={`${data.investment_horizon_years} years`} />
            </div>
          </Card>

          {/* Portfolio */}
          <Card className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary/10">
                  <Briefcase className="h-4.5 w-4.5 text-primary" />
                </div>
                <h2 className="text-lg font-semibold text-foreground">Danh mục đầu tư</h2>
              </div>
              <span className="text-sm font-bold text-foreground">
                ${totalPortfolioValue.toLocaleString()}
              </span>
            </div>

            {data.portfolio.length === 0 ? (
              <p className="text-sm text-muted-foreground">Chưa có danh mục nào được thêm vào.</p>
            ) : (
              <div className="space-y-2">
                <div className="grid grid-cols-4 text-xs font-medium text-muted-foreground px-3 pb-1">
                  <span>Ticker</span>
                  <span className="text-right">Shares</span>
                  <span className="text-right">Avg Price</span>
                  <span className="text-right">Value</span>
                </div>
                <Separator />
                {data.portfolio.map((item, i) => (
                  <div key={i} className="grid grid-cols-4 items-center px-3 py-2.5 rounded-lg hover:bg-accent/50 transition-colors">
                    <span className="font-mono font-semibold text-sm text-primary">{item.ticker}</span>
                    <span className="text-right text-sm text-foreground">{item.shares}</span>
                    <span className="text-right text-sm text-muted-foreground">${item.avg_price.toLocaleString()}</span>
                    <span className="text-right text-sm font-medium text-foreground">
                      ${(item.shares * item.avg_price).toLocaleString()}
                    </span>
                  </div>
                ))}
                <Separator />
                <div className="grid grid-cols-4 items-center px-3 pt-1">
                  <span className="text-xs font-semibold text-foreground">Total</span>
                  <span />
                  <span />
                  <span className="text-right text-sm font-bold text-foreground">
                    ${totalPortfolioValue.toLocaleString()}
                  </span>
                </div>
              </div>
            )}
          </Card>

          {/* Capital & Plan */}
          <Card className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary/10">
                <DollarSign className="h-4.5 w-4.5 text-primary" />
              </div>
              <h2 className="text-lg font-semibold text-foreground">Kế hoạch đầu tư</h2>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              <InfoItem label="Capital" value={`$${data.capital.toLocaleString()}`} />
              <InfoItem label="Monthly Investment" value={`$${data.monthly_investment.toLocaleString()}`} />
              <InfoItem label="Rebalance" value={capitalize(data.rebalance_frequency)} />
              <InfoItem label="Emergency Fund" value={`${data.emergency_fund_months} months`} />
              <InfoItem label="Dividend Pref." value={data.dividend_preference ? "Yes" : "No"} />
              <InfoItem label="ESG Preference" value={data.esg_preference ? "Yes" : "No"} />
            </div>

            {(data.preferred_sectors.length > 0 || data.avoid_sectors.length > 0) && (
              <div className="mt-4 space-y-3">
                {data.preferred_sectors.length > 0 && (
                  <div>
                    <p className="text-xs text-muted-foreground mb-1.5">Preferred Sectors</p>
                    <div className="flex flex-wrap gap-1.5">
                      {data.preferred_sectors.map((s) => (
                        <Badge key={s} variant="secondary" className="text-xs">{s}</Badge>
                      ))}
                    </div>
                  </div>
                )}
                {data.avoid_sectors.length > 0 && (
                  <div>
                    <p className="text-xs text-muted-foreground mb-1.5">Avoid Sectors</p>
                    <div className="flex flex-wrap gap-1.5">
                      {data.avoid_sectors.map((s) => (
                        <Badge key={s} variant="outline" className="text-xs text-destructive border-destructive/30">{s}</Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </Card>
        </div>
      </main>
    </div>
  );
}

function InfoItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs text-muted-foreground mb-0.5">{label}</p>
      <p className="text-sm font-medium text-foreground">{value}</p>
    </div>
  );
}

function capitalize(s: string) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}