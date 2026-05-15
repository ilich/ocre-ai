import { Outlet, redirect } from "react-router";
import AppHeader from "~/components/layout/AppHeader";
import ChatFab from "~/features/chat/components/ChatFab";
import ChatPopup from "~/features/chat/components/ChatPopup";
import { isAuthenticated } from "~/lib/auth";
import { useLocation } from "react-router";

export async function clientLoader() {
  if (!isAuthenticated()) {
    return redirect("/");
  }
  return null;
}

export default function PrivateLayout() {
  const location = useLocation();
  const showChat = location.pathname.startsWith("/catalog");
  return (
    <>
      <AppHeader />
      <Outlet />
      {showChat && (
        <>
          <ChatFab />
          <ChatPopup />
        </>
      )}
    </>
  );
}
