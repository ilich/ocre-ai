// Runs at module load time (before React renders).
// If the user has no stored preference, resolve the system value and persist it
// so MUI's useColorScheme always returns "light" | "dark", never "system".
if (typeof window !== "undefined" && localStorage.getItem("mui-mode") === null) {
  const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  localStorage.setItem("mui-mode", systemDark ? "dark" : "light");
}
