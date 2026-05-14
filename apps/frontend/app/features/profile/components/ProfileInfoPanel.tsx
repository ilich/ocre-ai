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
  updateProfileSchema,
  type UpdateProfileFormValues,
} from "../schemas/update-profile.schema";
import { useUpdateProfile } from "../hooks/useUpdateProfile";

export default function ProfileInfoPanel() {
  const { submit, loading, error, success, user } = useUpdateProfile();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<UpdateProfileFormValues>({
    resolver: zodResolver(updateProfileSchema),
    defaultValues: {
      fullName: user?.full_name ?? "",
    },
  });

  return (
    <Card elevation={0} sx={{ border: 1, borderColor: "divider", borderRadius: 3 }}>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
          Profile Information
        </Typography>

        <Box
          component="form"
          onSubmit={handleSubmit(submit)}
          noValidate
          sx={{ display: "flex", flexDirection: "column", gap: 2 }}
        >
          {error && <Alert severity="error">{error}</Alert>}
          {success && <Alert severity="success">Profile updated successfully.</Alert>}

          <TextField
            label="Email"
            type="email"
            value={user?.email ?? ""}
            disabled
            fullWidth
            slotProps={{ input: { readOnly: true } }}
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

          <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
            <Button
              type="submit"
              variant="contained"
              loading={loading}
            >
              Save
            </Button>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}
