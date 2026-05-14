import { Link } from "react-router";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import type { Route } from "./+types/catalog-detail";

export function meta() {
  return [{ title: "Coin Detail — The AI-Based Roman Coin Identification System" }];
}

export default function CatalogDetailPage({ params }: Route.ComponentProps) {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Button
        component={Link}
        to="/catalog"
        startIcon={<ArrowBackIcon />}
        sx={{ mb: 3 }}
      >
        Back to Catalog
      </Button>
      <Box>
        <Typography variant="h5" sx={{ fontWeight: 600 }}>
          Coin Record: {params.id}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          Detail view — coming soon.
        </Typography>
      </Box>
    </Container>
  );
}
