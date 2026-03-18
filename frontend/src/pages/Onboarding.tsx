import { Navbar } from "@/components/layout/Navbar";
import { OnboardingWizard, OnboardingData } from "@/components/onboarding/OnboardingWizard";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";
import { updateUserProfile } from "@/services/profileApi";

const Onboarding = () => {
  const navigate = useNavigate();
  const { token } = useAuth();
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleComplete = async (data: OnboardingData) => {
  setIsSubmitting(true);

  try {
    localStorage.setItem("finassist_profile", JSON.stringify(data));

    if (!token) throw new Error("Not authenticated");

    await updateUserProfile(data, token);


    toast({
      title: "Success!",
      description: "Your profile has been saved.",
    });

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
