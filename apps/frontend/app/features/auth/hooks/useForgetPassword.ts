import { useState } from "react";
import { authService } from "~/services/auth.service";
import type { ForgetPasswordFormValues } from "../schemas/forget-password.schema";

export function useForgetPassword() {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  async function submit(values: ForgetPasswordFormValues) {
    setError(null);
    setLoading(true);
    try {
      await authService.forgotPassword({ email: values.email });
      setSubmitted(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return { submit, loading, error, submitted };
}
