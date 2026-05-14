import { redirect } from "react-router";
import AuthCard from "~/features/auth/components/AuthCard";
import LoginForm from "~/features/auth/components/LoginForm";
import { isAuthenticated } from "~/lib/auth";

export async function clientLoader() {
  if (isAuthenticated()) {
    return redirect("/catalog");
  }
  return null;
}

export function meta() {
  return [{ title: "Sign In — The AI-Based Roman Coin Identification System" }];
}

export default function LoginPage() {
  return (
    <AuthCard title="Sign in to your account">
      <LoginForm />
    </AuthCard>
  );
}
