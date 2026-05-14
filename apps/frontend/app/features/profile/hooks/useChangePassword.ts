import { useState } from "react";
import { userService } from "~/services/user.service";
import type { UseFormReset } from "react-hook-form";
import type { ChangePasswordFormValues } from "../schemas/change-password.schema";

export function useChangePassword() {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  async function submit(
    values: ChangePasswordFormValues,
    reset: UseFormReset<ChangePasswordFormValues>
  ) {
    setError(null);
    setSuccess(false);
    setLoading(true);
    try {
      await userService.changePassword({
        old_password: values.currentPassword,
        new_password: values.newPassword,
      });
      setSuccess(true);
      reset();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to change password");
    } finally {
      setLoading(false);
    }
  }

  return { submit, loading, error, success };
}
