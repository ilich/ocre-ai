import { apiClient } from "./api";
import type { AuthUser } from "~/store/auth";

export const userService = {
  getMe: (token?: string) =>
    apiClient.get<AuthUser>("/user/me", { token }),
};
