import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";

import {
  changePasswordSchema,
  type ChangePasswordFormValues,
} from "../schemas/change-password.schema";
import { useChangePassword } from "../hooks/useChangePassword";

export default function ChangePasswordPanel() {
  const { submit, loading, error, success } = useChangePassword();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ChangePasswordFormValues>({
    resolver: zodResolver(changePasswordSchema),
  });

  return (
    <Card elevation={0} sx={{ border: 1, borderColor: "divider", borderRadius: 3 }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
          Change Password
        </Typography>

        <Box
          component="form"
          onSubmit={handleSubmit((values) => submit(values, reset))}
          noValidate
          sx={{ display: "flex", flexDirection: "column", gap: 2 }}
        >
          {error && <Alert severity="error">{error}</Alert>}
          {success && <Alert severity="success">Password changed successfully.</Alert>}

          <TextField
            label="Current Password"
            type="password"
            autoComplete="current-password"
            fullWidth
            error={Boolean(errors.currentPassword)}
            helperText={errors.currentPassword?.message}
            {...register("currentPassword")}
          />

          <TextField
            label="New Password"
            type="password"
            autoComplete="new-password"
            fullWidth
            error={Boolean(errors.newPassword)}
            helperText={errors.newPassword?.message}
            {...register("newPassword")}
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

          <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
            <Button type="submit" variant="contained" loading={loading}>
              Save
            </Button>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}
