import type { Route } from "./+types/reset-password";
import AuthCard from "~/features/auth/components/AuthCard";
import ResetPasswordForm from "~/features/auth/components/ResetPasswordForm";

export function meta() {
  return [{ title: "Reset Password — The AI-Based Roman Coin Identification System" }];
}

export default function ResetPasswordPage({ params }: Route.ComponentProps) {
  return (
    <AuthCard title="Set a new password">
      <ResetPasswordForm token={params.token} />
    </AuthCard>
  );
}
