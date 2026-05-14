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
  resetPasswordSchema,
  type ResetPasswordFormValues,
} from "../schemas/reset-password.schema";
import { useResetPassword } from "../hooks/useResetPassword";

interface ResetPasswordFormProps {
  token: string;
}

export default function ResetPasswordForm({ token }: ResetPasswordFormProps) {
  const { submit, loading, error } = useResetPassword(token);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ResetPasswordFormValues>({
    resolver: zodResolver(resetPasswordSchema),
  });

  return (
    <Box
      component="form"
      onSubmit={handleSubmit(submit)}
      noValidate
      sx={{ display: "flex", flexDirection: "column", gap: 2 }}
    >
      {error && <Alert severity="error">{error}</Alert>}

      <TextField
        label="New Password"
        type="password"
        autoComplete="new-password"
        autoFocus
        fullWidth
        error={Boolean(errors.password)}
        helperText={errors.password?.message}
        {...register("password")}
      />

      <TextField
        label="Confirm New Password"
        type="password"
        autoComplete="new-password"
        fullWidth
        error={Boolean(errors.confirmPassword)}
        helperText={errors.confirmPassword?.message}
        {...register("confirmPassword")}
      />

      <Button
        type="submit"
        variant="contained"
        size="large"
        fullWidth
        loading={loading}
        sx={{ mt: 1 }}
      >
        Set new password
      </Button>

      <Typography
        variant="body2"
        color="text.secondary"
        sx={{ textAlign: "center" }}
      >
        <MuiLink component={Link} to="/" variant="body2">
          Back to sign in
        </MuiLink>
      </Typography>
    </Box>
  );
}
