import type { Route } from "./+types/reset-password";

export function meta() {
  return [{ title: "Reset Password" }];
}

export default function ResetPasswordPage({ params }: Route.ComponentProps) {
  return (
    <main>
      <h1>Reset Password</h1>
      <p>Token: {params.token}</p>
      <p>Reset password page — form coming soon.</p>
    </main>
  );
}
