import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link } from "react-router";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";
import MuiLink from "@mui/material/Link";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";

import { loginSchema, type LoginFormValues } from "../schemas/login.schema";
import { useLogin } from "../hooks/useLogin";

export default function LoginForm() {
  const { login, loading, error } = useLogin();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  return (
    <Box
      component="form"
      onSubmit={handleSubmit(login)}
      noValidate
      sx={{ display: "flex", flexDirection: "column", gap: 2 }}
    >
      {error && (
        <Alert severity="error" sx={{ mb: 1 }}>
          {error}
        </Alert>
      )}

      <TextField
        label="Login"
        type="text"
        autoFocus
        fullWidth
        error={Boolean(errors.login)}
        helperText={errors.login?.message}
        {...register("login")}
      />

      <TextField
        label="Password"
        type="password"
        autoComplete="current-password"
        fullWidth
        error={Boolean(errors.password)}
        helperText={errors.password?.message}
        {...register("password")}
      />

      <Box sx={{ textAlign: "right", mt: -1 }}>
        <MuiLink component={Link} to="/forget-password" variant="body2">
          Forgot password?
        </MuiLink>
      </Box>

      <Button
        type="submit"
        variant="contained"
        size="large"
        fullWidth
        loading={loading}
        sx={{ mt: 1 }}
      >
        Sign in
      </Button>

      <Divider sx={{ my: 1 }} />

      <Typography variant="body2" color="text.secondary" sx={{ textAlign: "center" }}>
        Don&apos;t have an account?{" "}
        <MuiLink component={Link} to="/sign-up" variant="body2" sx={{ fontWeight: 500 }}>
          Sign up
        </MuiLink>
      </Typography>
    </Box>
  );
}
