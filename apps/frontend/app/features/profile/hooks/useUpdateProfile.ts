import { useState } from "react";
import { userService } from "~/services/user.service";
import { useAuthStore } from "~/store/auth";
import type { UpdateProfileFormValues } from "../schemas/update-profile.schema";

export function useUpdateProfile() {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const { user, setAuth } = useAuthStore();

  async function submit(values: UpdateProfileFormValues) {
    setError(null);
    setSuccess(false);
    setLoading(true);
    try {
      const updated = await userService.updateProfile({
        full_name: values.fullName,
      });
      // Preserve the existing token when updating user data in the store
      const token = useAuthStore.getState().token!;
      setAuth(token, { id: updated.id, email: updated.email, full_name: updated.full_name });
      setSuccess(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update profile");
    } finally {
      setLoading(false);
    }
  }

  return { submit, loading, error, success, user };
}
