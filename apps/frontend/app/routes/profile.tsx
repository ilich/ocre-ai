import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import ChangePasswordPanel from "~/features/profile/components/ChangePasswordPanel";
import ProfileInfoPanel from "~/features/profile/components/ProfileInfoPanel";

export function meta() {
  return [{ title: "Profile — The AI-Based Roman Coin Identification System" }];
}

export default function ProfilePage() {
  return (
    <Container maxWidth="sm" sx={{ py: 4 }}>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: 600 }}>
        Profile
      </Typography>

      <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
        <ProfileInfoPanel />
        <ChangePasswordPanel />
      </Box>
    </Container>
  );
}
