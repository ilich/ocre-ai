import AuthCard from "~/features/auth/components/AuthCard";
import ForgetPasswordForm from "~/features/auth/components/ForgetPasswordForm";

export function meta() {
  return [{ title: "Forgot Password — The AI-Based Roman Coin Identification System" }];
}

export default function ForgetPasswordPage() {
  return (
    <AuthCard title="Forgot your password?">
      <ForgetPasswordForm />
    </AuthCard>
  );
}
