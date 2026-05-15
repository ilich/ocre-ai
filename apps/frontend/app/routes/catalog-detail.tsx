import { useEffect } from "react";
import { useNavigate } from "react-router";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Chip from "@mui/material/Chip";
import Container from "@mui/material/Container";
import Divider from "@mui/material/Divider";
import Paper from "@mui/material/Paper";
import Skeleton from "@mui/material/Skeleton";
import Typography from "@mui/material/Typography";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { useCoinDetail } from "~/features/catalog/hooks/useCoinDetail";
import { useChatStore } from "~/store/chat";
import type { Route } from "./+types/catalog-detail";

export function meta() {
  return [{ title: "Coin Detail — The AI-Based Roman Coin Identification System" }];
}

interface FieldRowProps {
  label: string;
  value: string | string[] | null | undefined;
}

function FieldRow({ label, value }: FieldRowProps) {
  const isEmpty = !value || (Array.isArray(value) && value.length === 0);
  if (isEmpty) return null;

  const content =
    Array.isArray(value) && value.length > 1 ? (
      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
        {value.map((v) => (
          <Chip key={v} label={v} size="small" />
        ))}
      </Box>
    ) : (
      <Typography variant="body1">{Array.isArray(value) ? value[0] : value}</Typography>
    );

  return (
    <Box>
      <Typography
        variant="caption"
        color="text.secondary"
        sx={{ fontWeight: 600, textTransform: "uppercase", letterSpacing: 0.5 }}
      >
        {label}
      </Typography>
      <Box sx={{ mt: 0.5 }}>{content}</Box>
    </Box>
  );
}

export default function CatalogDetailPage({ params }: Route.ComponentProps) {
  const navigate = useNavigate();
  const { coin, loading, error } = useCoinDetail(params.id);
  const { setCoinsContext, clearHistory } = useChatStore();
  useEffect(() => {
    clearHistory();
  }, [clearHistory]);
  useEffect(() => {
    setCoinsContext([params.id]);
  }, [params.id, setCoinsContext]);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate(-1)} sx={{ mb: 3 }}>
        Back to Catalog
      </Button>

      {error && <Alert severity="error">{error}</Alert>}

      {loading && (
        <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
          <Skeleton variant="text" width="60%" height={40} />
          <Skeleton variant="rectangular" height={200} sx={{ borderRadius: 2 }} />
          <Skeleton variant="text" width="40%" />
          <Skeleton variant="text" width="50%" />
        </Box>
      )}

      {!loading && coin && (
        <Paper elevation={0} sx={{ border: 1, borderColor: "divider", borderRadius: 3, p: 4 }}>
          {/* Title + Record ID */}
          <Typography variant="h5" sx={{ fontWeight: 600 }}>
            {coin.title}
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5, mb: 3 }}>
            Record ID: {coin.id}
          </Typography>

          <Divider sx={{ mb: 3 }} />

          {/* Metadata fields */}
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2.5 }}>
            <FieldRow label="Object Type" value={coin.object_type} />
            <FieldRow label="Issue Date" value={coin.date_range} />
            <FieldRow label="Authority" value={coin.authority} />
            <FieldRow label="Denomination" value={coin.denomination} />
            <FieldRow label="Material" value={coin.material} />
            <FieldRow label="Manufacturer" value={coin.manufacturer} />
            <FieldRow label="Mint Location" value={coin.geographic} />

            {coin.description && (
              <>
                <Divider />
                <Box>
                  <Typography
                    variant="caption"
                    color="text.secondary"
                    sx={{ fontWeight: 600, textTransform: "uppercase", letterSpacing: 0.5 }}
                  >
                    Description
                  </Typography>
                  <Typography variant="body1" sx={{ mt: 0.5, whiteSpace: "pre-wrap" }}>
                    {coin.description}
                  </Typography>
                </Box>
              </>
            )}

            {/* Images */}
            {coin.images.length > 0 && (
              <>
                <Divider />
                <Box>
                  <Typography
                    variant="caption"
                    color="text.secondary"
                    sx={{ fontWeight: 600, textTransform: "uppercase", letterSpacing: 0.5 }}
                  >
                    Images
                  </Typography>
                  <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap", mt: 1 }}>
                    {coin.images.map((src, i) => (
                      <Box
                        key={i}
                        component="img"
                        src={src}
                        alt={`${coin.title} — image ${i + 1}`}
                        sx={{
                          maxHeight: 220,
                          maxWidth: "100%",
                          objectFit: "contain",
                          borderRadius: 2,
                          border: 1,
                          borderColor: "divider",
                        }}
                      />
                    ))}
                  </Box>
                </Box>
              </>
            )}
          </Box>
        </Paper>
      )}
    </Container>
  );
}
