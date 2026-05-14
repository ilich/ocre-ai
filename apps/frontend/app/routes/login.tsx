import { redirect } from "react-router";
import { isAuthenticated } from "~/lib/auth";

export async function clientLoader() {
  if (isAuthenticated()) {
    return redirect("/catalog");
  }
  return null;
}

export function meta() {
  return [{ title: "Sign In" }];
}

export default function LoginPage() {
  return (
    <main>
      <h1>Sign In</h1>
      <p>Login page — form coming soon.</p>
    </main>
  );
}
