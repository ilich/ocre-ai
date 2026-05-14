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
  success: boolean;
  message?: string | null;
}

export const userService = {
  getMe: (token?: string) =>
    apiClient.get<AuthUser>("/user/me", { token }),

  updateProfile: (body: UpdateProfileRequest) =>
    apiClient.put<AuthUser>("/user/me", body),

  changePassword: (body: ChangePasswordRequest) =>
    apiClient.post<BaseResponse>("/user/change-password", body),

  addToCollection: (record_id: string) =>
    apiClient.post<BaseResponse>("/user/collection", { record_id }),

  removeFromCollection: (record_id: string) =>
    apiClient.delete<BaseResponse>(`/user/collection/${record_id}`),
};
