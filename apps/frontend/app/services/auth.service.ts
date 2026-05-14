import { apiClient } from "./api";

export interface SignInRequest {
  login: string;
  password: string;
}

export interface SignInResponse {
  access_token: string;
  token_type: string;
}

export interface SignUpRequest {
  email: string;
  password: string;
  full_name: string;
}

export interface SignUpResponse {
  success: boolean;
  message?: string | null;
  id: string;
  email: string;
  full_name: string;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface SetNewPasswordRequest {
  token: string;
  new_password: string;
}

export interface BaseResponse {
  success: boolean;
  message?: string | null;
}

export const authService = {
  signIn: (body: SignInRequest) =>
    apiClient.post<SignInResponse>("/auth/sign-in", body, { auth: false, skipAuthRedirect: true }),

  signUp: (body: SignUpRequest) =>
    apiClient.post<SignUpResponse>("/auth/sign-up", body, { auth: false }),

  forgotPassword: (body: ForgotPasswordRequest) =>
    apiClient.post<BaseResponse>("/auth/forgot-password", body, { auth: false }),

  resetPassword: (body: SetNewPasswordRequest) =>
    apiClient.post<BaseResponse>("/auth/reset-password", body, { auth: false }),
};
