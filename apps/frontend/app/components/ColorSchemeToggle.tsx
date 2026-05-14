import IconButton from "@mui/material/IconButton";
import Tooltip from "@mui/material/Tooltip";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import LightModeIcon from "@mui/icons-material/LightMode";
import { useColorScheme } from "@mui/material/styles";

interface ColorSchemeToggleProps {
  size?: "small" | "medium" | "large";
  color?: "inherit" | "default" | "primary" | "secondary";
}

export default function ColorSchemeToggle({
  size = "small",
  color = "inherit",
}: ColorSchemeToggleProps) {
  const { mode, setMode } = useColorScheme();
  const isDark = mode === "dark";

  return (
    <Tooltip title={isDark ? "Switch to light mode" : "Switch to dark mode"}>
      <IconButton
        color={color}
        size={size}
        onClick={() => setMode(isDark ? "light" : "dark")}
      >
        {isDark ? (
          <LightModeIcon fontSize={size} />
        ) : (
          <DarkModeIcon fontSize={size} />
        )}
      </IconButton>
    </Tooltip>
  );
}
