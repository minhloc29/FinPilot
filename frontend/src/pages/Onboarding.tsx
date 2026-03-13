import { Navbar } from "@/components/layout/Navbar";
import { OnboardingWizard, OnboardingData } from "@/components/onboarding/OnboardingWizard";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { createPortfolio } from "@/services/portfolioApi";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";

const Onboarding = () => {
  const navigate = useNavigate();
  const { token } = useAuth();
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleComplete = async (data: OnboardingData) => {
    setIsSubmitting(true);
    
    try {
      // Store profile data locally
      localStorage.setItem("finassist_profile", JSON.stringify(data));
      
      // If user is authenticated and has portfolio items, create portfolio in backend
      if (token && data.portfolio.length > 0) {
        try {
          const portfolioData = {
            name: "My Portfolio",
            description: `Investment portfolio with ${data.risk_profile} risk profile`,
            holdings: data.portfolio.map(item => ({
              symbol: item.ticker,
              shares: item.shares,
              average_cost: item.avg_price
            }))
          };
          
          await createPortfolio(portfolioData, token);
          toast({
            title: "Success!",
            description: "Portfolio saved successfully!",
          });
        } catch (error) {
          console.error("Failed to save portfolio to backend:", error);
          toast({
            title: "Warning",
            description: "Failed to save portfolio. Data saved locally.",
            variant: "destructive",
          });
        }
      }
      
      // Redirect to chat
      navigate("/");
    } catch (error) {
      console.error("Error completing onboarding:", error);
      toast({
        title: "Error",
        description: "Something went wrong. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen w-full bg-background">
      <Navbar />
      <main className="flex flex-1 items-start justify-center px-4 pt-10 pb-8">
        <OnboardingWizard onComplete={handleComplete} />
      </main>
    </div>
  );
};

export default Onboarding;
