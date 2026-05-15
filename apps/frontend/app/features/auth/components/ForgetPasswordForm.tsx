import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link } from "react-router";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import MuiLink from "@mui/material/Link";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";

import {
  forgetPasswordSchema,
  type ForgetPasswordFormValues,
} from "../schemas/forget-password.schema";
import { useForgetPassword } from "../hooks/useForgetPassword";

export default function ForgetPasswordForm() {
  const { submit, loading, error, submitted } = useForgetPassword();

  const {
    register,
    handleSubmit,
    getValues,
    formState: { errors },
  } = useForm<ForgetPasswordFormValues>({
    resolver: zodResolver(forgetPasswordSchema),
  });

  if (submitted) {
    return (
      <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        <Alert severity="success">
          We sent a password reset link to <strong>{getValues("email")}</strong>. Check your inbox.
        </Alert>
        <Typography variant="body2" color="text.secondary" sx={{ textAlign: "center" }}>
          <MuiLink component={Link} to="/" variant="body2">
            Back to sign in
          </MuiLink>
        </Typography>
      </Box>
    );
  }

  return (
    <Box
      component="form"
      onSubmit={handleSubmit(submit)}
      noValidate
      sx={{ display: "flex", flexDirection: "column", gap: 2 }}
    >
      <Typography variant="body2" color="text.secondary">
        Enter your email and we&apos;ll send you a link to reset your password.
      </Typography>

      {error && <Alert severity="error">{error}</Alert>}

      <TextField
        label="Email"
        type="email"
        autoComplete="email"
        autoFocus
        fullWidth
        error={Boolean(errors.email)}
        helperText={errors.email?.message}
        {...register("email")}
      />

      <Button
        type="submit"
        variant="contained"
        size="large"
        fullWidth
        loading={loading}
        sx={{ mt: 1 }}
      >
        Send reset link
      </Button>

      <Typography variant="body2" color="text.secondary" sx={{ textAlign: "center" }}>
        <MuiLink component={Link} to="/" variant="body2">
          Back to sign in
        </MuiLink>
      </Typography>
    </Box>
  );
}
