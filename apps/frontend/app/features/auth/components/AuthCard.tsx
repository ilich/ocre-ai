import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

interface AuthCardProps {
  title: string;
  children: React.ReactNode;
}

export default function AuthCard({ title, children }: AuthCardProps) {
  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        bgcolor: "background.default",
        px: 2,
      }}
    >
      <Card
        elevation={0}
        sx={{
          width: "100%",
          maxWidth: 400,
          border: 1,
          borderColor: "divider",
          borderRadius: 3,
        }}
      >
        <CardContent sx={{ p: 4 }}>
          <Box sx={{ mb: 4, textAlign: "center" }}>
            <Typography
              component="span"
              sx={{
                display: "inline-block",
                fontSize: 28,
                fontWeight: 800,
                letterSpacing: "-0.5px",
                color: "primary.main",
              }}
            >
              OCRE.AI
            </Typography>
            <Typography variant="h5" sx={{ mt: 2, fontWeight: 600 }}>
              {title}
            </Typography>
          </Box>

          {children}
        </CardContent>
      </Card>
    </Box>
  );
}
