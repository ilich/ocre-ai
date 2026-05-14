import { redirect } from "react-router";
import { isAuthenticated } from "~/lib/auth";

export async function clientLoader() {
  if (!isAuthenticated()) {
    return redirect("/");
  }
  return null;
}

export function meta() {
  return [{ title: "Catalog" }];
}

export default function CatalogPage() {
  return (
    <main>
      <h1>Catalog</h1>
      <p>Coin catalog — content coming soon.</p>
    </main>
  );
}
