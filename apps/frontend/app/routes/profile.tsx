import { redirect } from "react-router";
import { isAuthenticated } from "~/lib/auth";
import { useAuthStore } from "~/store/auth";

export async function clientLoader() {
  if (!isAuthenticated()) {
    return redirect("/");
  }
  return null;
}

export function meta() {
  return [{ title: "Profile" }];
}

export default function ProfilePage() {
  const user = useAuthStore((s) => s.user);

  return (
    <main>
      <h1>Profile</h1>
      {user && (
        <p>
          {user.full_name} ({user.email})
        </p>
      )}
      <p>Profile page — content coming soon.</p>
    </main>
  );
}
