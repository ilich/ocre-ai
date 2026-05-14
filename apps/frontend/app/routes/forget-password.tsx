import AuthCard from "~/features/auth/components/AuthCard";
import ForgetPasswordForm from "~/features/auth/components/ForgetPasswordForm";

export function meta() {
  return [{ title: "Forgot Password — OCRE.AI" }];
}

export default function ForgetPasswordPage() {
  return (
    <AuthCard title="Forgot your password?">
      <ForgetPasswordForm />
    </AuthCard>
  );
}
