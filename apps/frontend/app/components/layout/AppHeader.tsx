import { useNavigate, Link } from "react-router";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import LogoutIcon from "@mui/icons-material/Logout";
import { useAuthStore } from "~/store/auth";
import ColorSchemeToggle from "~/components/ColorSchemeToggle";

export default function AppHeader() {
  const user = useAuthStore((s) => s.user);
  const clearAuth = useAuthStore((s) => s.clearAuth);
  const navigate = useNavigate();
  function handleLogout() {
    clearAuth();
    navigate("/");
  }

  return (
    <AppBar position="sticky" elevation={0} sx={{ borderBottom: 1, borderColor: "divider" }}>
      <Toolbar>
        <Typography
          component={Link}
          to="/catalog"
          sx={{
            fontWeight: 800,
            fontSize: 20,
            letterSpacing: "-0.5px",
            color: "inherit",
            textDecoration: "none",
            flexGrow: 1,
          }}
        >
          OCRE.AI
        </Typography>

        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          <ColorSchemeToggle />
          {user && (
            <Button
              component={Link}
              to="/profile"
              color="inherit"
              startIcon={<AccountCircleIcon />}
              size="small"
              sx={{ opacity: 0.85, "&:hover": { opacity: 1 } }}
            >
              {user.full_name}
            </Button>
          )}
          <Button color="inherit" startIcon={<LogoutIcon />} onClick={handleLogout} size="small">
            Sign out
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
