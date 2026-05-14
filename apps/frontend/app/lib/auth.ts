// Read auth state directly from localStorage so clientLoaders can check it
// synchronously before the Zustand store hydrates.
export function getToken(): string | null {
  try {
    const raw = localStorage.getItem("auth");
    if (!raw) return null;
    const { state } = JSON.parse(raw) as { state?: { token?: string | null } };
    return state?.token ?? null;
  } catch {
    return null;
  }
}

export function isAuthenticated(): boolean {
  return Boolean(getToken());
}
