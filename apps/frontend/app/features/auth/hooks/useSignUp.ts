import { useState } from "react";
import { useNavigate } from "react-router";
import { authService } from "~/services/auth.service";
import { userService } from "~/services/user.service";
import { useAuthStore } from "~/store/auth";
import type { SignUpFormValues } from "../schemas/sign-up.schema";

export function useSignUp() {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const setAuth = useAuthStore((s) => s.setAuth);
  const navigate = useNavigate();

  async function signUp(values: SignUpFormValues) {
    setError(null);
    setLoading(true);
    try {
      await authService.signUp({
        email: values.email,
        password: values.password,
        full_name: values.fullName,
      });
      const { access_token } = await authService.signIn({
        login: values.email,
        password: values.password,
      });
      const { id, email, full_name } = await userService.getMe(access_token);
      setAuth(access_token, { id, email, full_name });
      navigate("/catalog");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sign up failed");
    } finally {
      setLoading(false);
    }
  }

  return { signUp, loading, error };
}
