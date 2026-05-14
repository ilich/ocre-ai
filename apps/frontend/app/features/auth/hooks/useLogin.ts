import { useState } from "react";
import { useNavigate } from "react-router";
import { authService } from "~/services/auth.service";
import { userService } from "~/services/user.service";
import { useAuthStore } from "~/store/auth";
import type { LoginFormValues } from "../schemas/login.schema";

export function useLogin() {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const setAuth = useAuthStore((s) => s.setAuth);
  const navigate = useNavigate();

  async function login(values: LoginFormValues) {
    setError(null);
    setLoading(true);
    try {
      const { access_token } = await authService.signIn(values);
      // Fetch the full user profile so the store has complete data
      const user = await userService.getMe(access_token);
      setAuth(access_token, user);
      navigate("/catalog");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sign in failed");
    } finally {
      setLoading(false);
    }
  }

  return { login, loading, error };
}
