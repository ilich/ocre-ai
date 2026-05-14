import { apiClient } from "./api";
import type { AuthUser } from "~/store/auth";

export interface UpdateProfileRequest {
  full_name: string;
}

export interface ChangePasswordRequest {
  old_password: string;
  new_password: string;
}

export interface BaseResponse {
  message: string;
}

export const userService = {
  getMe: (token?: string) =>
    apiClient.get<AuthUser>("/user/me", { token }),

  // Stub — replace with real endpoint once backend is ready
  updateProfile: (_body: UpdateProfileRequest): Promise<AuthUser> =>
    Promise.reject(new Error("updateProfile: backend not implemented yet")),

  changePassword: (body: ChangePasswordRequest) =>
    apiClient.post<BaseResponse>("/user/change-password", body),
};
