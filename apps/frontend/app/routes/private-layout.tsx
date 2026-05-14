import { Outlet, redirect } from "react-router";
import AppHeader from "~/components/layout/AppHeader";
import { isAuthenticated } from "~/lib/auth";

export async function clientLoader() {
  if (!isAuthenticated()) {
    return redirect("/");
  }
  return null;
}

export default function PrivateLayout() {
  return (
    <>
      <AppHeader />
      <Outlet />
    </>
  );
}
