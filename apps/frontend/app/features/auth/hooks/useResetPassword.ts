import { useState } from "react";
import { useNavigate } from "react-router";
import { authService } from "~/services/auth.service";
import type { ResetPasswordFormValues } from "../schemas/reset-password.schema";

export function useResetPassword(token: string) {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function submit(values: ResetPasswordFormValues) {
    setError(null);
    setLoading(true);
    try {
      await authService.resetPassword({ token, new_password: values.password });
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return { submit, loading, error };
}
