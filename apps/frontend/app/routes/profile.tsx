import { useAuthStore } from "~/store/auth";

export function meta() {
  return [{ title: "Profile — The AI-Based Roman Coin Identification System" }];
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
