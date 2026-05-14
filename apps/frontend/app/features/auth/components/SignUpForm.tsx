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

import { signUpSchema, type SignUpFormValues } from "../schemas/sign-up.schema";
import { useSignUp } from "../hooks/useSignUp";

export default function SignUpForm() {
  const { signUp, loading, error } = useSignUp();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignUpFormValues>({
    resolver: zodResolver(signUpSchema),
  });

  return (
    <Box
      component="form"
      onSubmit={handleSubmit(signUp)}
      noValidate
      sx={{ display: "flex", flexDirection: "column", gap: 2 }}
    >
      {error && (
        <Alert severity="error" sx={{ mb: 1 }}>
          {error}
        </Alert>
      )}

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

      <TextField
        label="Full Name"
        type="text"
        autoComplete="name"
        fullWidth
        error={Boolean(errors.fullName)}
        helperText={errors.fullName?.message}
        {...register("fullName")}
      />

      <TextField
        label="Password"
        type="password"
        autoComplete="new-password"
        fullWidth
        error={Boolean(errors.password)}
        helperText={errors.password?.message}
        {...register("password")}
      />

      <TextField
        label="Confirm Password"
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
        Create account
      </Button>

      <Divider sx={{ my: 1 }} />

      <Typography
        variant="body2"
        color="text.secondary"
        sx={{ textAlign: "center" }}
      >
        Already have an account?{" "}
        <MuiLink
          component={Link}
          to="/"
          variant="body2"
          sx={{ fontWeight: 500 }}
        >
          Sign in
        </MuiLink>
      </Typography>
    </Box>
  );
}
