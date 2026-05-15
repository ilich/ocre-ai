import { z } from "zod";

export const updateProfileSchema = z.object({
  fullName: z.string().min(2, "Full name must be at least 2 characters"),
});

export type UpdateProfileFormValues = z.infer<typeof updateProfileSchema>;
