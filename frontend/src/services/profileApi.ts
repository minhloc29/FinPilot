import { OnboardingData } from "@/components/onboarding/OnboardingWizard";
import { request } from "./client";

export async function updateUserProfile(
  data: Partial<OnboardingData>,
  token: string
) {

  console.log(data)
  return request("/api/v1/user-profile", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(data)
  });
}