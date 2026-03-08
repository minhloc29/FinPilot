import { Navbar } from "@/components/layout/Navbar";
import { OnboardingWizard, OnboardingData } from "@/components/onboarding/OnboardingWizard";
import { useNavigate } from "react-router-dom";

const Onboarding = () => {
  const navigate = useNavigate();

  const handleComplete = (data: OnboardingData) => {
    // Store profile data and redirect to chat
    localStorage.setItem("finassist_profile", JSON.stringify(data));
    navigate("/");
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
