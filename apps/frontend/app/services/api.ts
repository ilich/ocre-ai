import { useAuthStore } from "~/store/auth";

const BASE_URL = "http://localhost:8000";

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

interface RequestOptions {
  method?: HttpMethod;
  body?: unknown;
  token?: string;
  skipAuthRedirect?: boolean;
}

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message: string,
    public readonly data?: unknown
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(
  path: string,
  { method = "GET", body, token, skipAuthRedirect = false }: RequestOptions = {}
): Promise<T> {
  const isFormData = body instanceof FormData;
  const headers: Record<string, string> = isFormData ? {} : { "Content-Type": "application/json" };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body instanceof FormData ? body : body !== undefined ? JSON.stringify(body) : undefined,
  });

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    if ((res.status === 401 || res.status === 403) && !skipAuthRedirect) {
      useAuthStore.getState().clearAuth();
      window.location.href = "/";
    }
    const message = (data as { detail?: string })?.detail ?? res.statusText;
    throw new ApiError(res.status, message, data);
  }

  return data as T;
}

function getStoredToken(): string | undefined {
  try {
    const raw = localStorage.getItem("auth");
    if (!raw) return undefined;
    const { state } = JSON.parse(raw) as { state?: { token?: string | null } };
    return state?.token ?? undefined;
  } catch {
    return undefined;
  }
}

export const apiClient = {
  get: <T>(path: string, opts?: { token?: string }) =>
    request<T>(path, { token: opts?.token ?? getStoredToken() }),

  post: <T>(path: string, body: unknown, opts?: { auth?: boolean; skipAuthRedirect?: boolean }) =>
    request<T>(path, {
      method: "POST",
      body,
      token: opts?.auth !== false ? getStoredToken() : undefined,
      skipAuthRedirect: opts?.skipAuthRedirect ?? opts?.auth === false,
    }),

  put: <T>(path: string, body: unknown) =>
    request<T>(path, { method: "PUT", body, token: getStoredToken() }),

  postForm: <T>(path: string, body: FormData) =>
    request<T>(path, { method: "POST", body, token: getStoredToken() }),

  delete: <T>(path: string) => request<T>(path, { method: "DELETE", token: getStoredToken() }),
};
