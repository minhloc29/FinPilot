import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowLeft, ArrowRight, Sparkles } from "lucide-react";
import { StepProfile } from "./steps/StepProfile";
import { StepRisk } from "./steps/StepRisk";
import { StepPortfolio } from "./steps/StepPortfolio";
import { StepCapital } from "./steps/StepCapital";
import { StepPreferences } from "./steps/StepPreferences";

export interface PortfolioItem {
  ticker: string;
  shares: number;
  avg_price: number;
}

export interface OnboardingData {
  // Hồ sơ cá nhân
  age: number;
  country: string;
  investment_experience: "beginner" | "intermediate" | "advanced";
  annual_income: number;
  monthly_savings: number;
  financial_goal: string;

  // Rủi ro
  risk_profile: "conservative" | "moderate" | "aggressive";
  max_drawdown_tolerance: number;
  investment_horizon_years: number;

  // Danh mục đầu tư
  portfolio: PortfolioItem[];

  // Vốn đầu tư
  capital: number;
  monthly_investment: number;
  rebalance_frequency: string;

  // Sở thích
  preferred_sectors: string[];
  avoid_sectors: string[];
  dividend_preference: boolean;
  esg_preference: boolean;

  // Thanh khoản
  emergency_fund_months: number;
}

const DEFAULT_DATA: OnboardingData = {
  age: 30,
  country: "",
  investment_experience: "beginner",
  annual_income: 0,
  monthly_savings: 0,
  financial_goal: "tăng_trưởng_tài_sản",

  risk_profile: "moderate",
  max_drawdown_tolerance: 20,
  investment_horizon_years: 5,

  portfolio: [],

  capital: 0,
  monthly_investment: 0,
  rebalance_frequency: "quarterly",

  preferred_sectors: [],
  avoid_sectors: [],
  dividend_preference: false,
  esg_preference: false,

  emergency_fund_months: 6,
};

const STEPS = [
  {
    title: "Hồ sơ cá nhân",
    subtitle: "Hãy cho chúng tôi biết một chút về bạn",
    icon: "👤",
  },
  {
    title: "Khả năng chịu rủi ro",
    subtitle: "Bạn có thể chịu mức rủi ro như thế nào?",
    icon: "🛡️",
  },
  {
    title: "Danh mục đầu tư",
    subtitle: "Bạn đang sở hữu những tài sản nào?",
    icon: "📊",
  },
  {
    title: "Kế hoạch đầu tư",
    subtitle: "Vốn đầu tư và chiến lược của bạn",
    icon: "💰",
  },
  {
    title: "Tùy chọn cá nhân",
    subtitle: "Cá nhân hóa trải nghiệm đầu tư",
    icon: "⚙️",
  },
];

interface OnboardingWizardProps {
  onComplete: (data: OnboardingData) => void;
}

export function OnboardingWizard({ onComplete }: OnboardingWizardProps) {
  const [step, setStep] = useState(0);
  const [data, setData] = useState<OnboardingData>(DEFAULT_DATA);
  
  const updateData = (partial: Partial<OnboardingData>) => {
    setData((prev) => ({ ...prev, ...partial }));
  };

  const next = () => {
    if (step < STEPS.length - 1) setStep(step + 1);
  };

  const prev = () => {
    if (step > 0) setStep(step - 1);
  };

  const finish = () => {
    console.log("FINAL DATA:", data);
    onComplete(data);
  };

  return (
    <div className="w-full max-w-2xl mx-auto">

      {/* Thanh tiến trình */}
      <div className="flex items-center gap-1 mb-8">
        {STEPS.map((s, i) => (
          <div key={i} className="flex-1 flex flex-col items-center gap-1.5">
            <div
              className={`h-1.5 w-full rounded-full transition-colors ${
                i <= step ? "bg-primary" : "bg-muted"
              }`}
            />
            <span
              className={`text-[10px] font-medium hidden sm:block ${
                i === step ? "text-primary" : "text-muted-foreground"
              }`}
            >
              {s.title}
            </span>
          </div>
        ))}
      </div>

      {/* Tiêu đề step */}
      <div className="text-center mb-6">
        <span className="text-3xl mb-2 block">{STEPS[step].icon}</span>

        <h2 className="text-xl font-bold text-foreground">
          {STEPS[step].title}
        </h2>

        <p className="text-sm text-muted-foreground mt-1">
          {STEPS[step].subtitle}
        </p>
      </div>

      {/* Nội dung step */}
      <div className="rounded-2xl border border-border bg-card p-6 shadow-sm min-h-[320px]">
        <AnimatePresence mode="wait">
          <motion.div
            key={step}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.2 }}
          >
            {step === 0 && <StepProfile data={data} update={updateData} />}
            {step === 1 && <StepRisk data={data} update={updateData} />}
            {step === 2 && <StepPortfolio data={data} update={updateData} />}
            {step === 3 && <StepCapital data={data} update={updateData} />}
            {step === 4 && <StepPreferences data={data} update={updateData} />}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Điều hướng */}
      <div className="flex justify-between mt-6">
        <Button
          variant="outline"
          onClick={prev}
          disabled={step === 0}
          className="gap-2 rounded-full"
        >
          <ArrowLeft className="h-4 w-4" />
          Quay lại
        </Button>

        {step < STEPS.length - 1 ? (
          <Button onClick={next} className="gap-2 rounded-full">
            Tiếp tục
            <ArrowRight className="h-4 w-4" />
          </Button>
        ) : (
          <Button
            onClick={finish}
            className="gap-2 rounded-full bg-primary"
          >
            <Sparkles className="h-4 w-4" />
            Phân tích bằng AI
          </Button>
        )}
      </div>
    </div>
  );
}