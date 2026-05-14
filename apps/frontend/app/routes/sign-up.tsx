import AuthCard from "~/features/auth/components/AuthCard";
import SignUpForm from "~/features/auth/components/SignUpForm";

export function meta() {
  return [{ title: "Create Account — The AI-Based Roman Coin Identification System" }];
}

export default function SignUpPage() {
  return (
    <AuthCard title="Create your account">
      <SignUpForm />
    </AuthCard>
  );
}
