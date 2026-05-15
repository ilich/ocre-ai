import { useRef, useState } from "react";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import Typography from "@mui/material/Typography";
import ImageSearchIcon from "@mui/icons-material/ImageSearch";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import { catalogService } from "~/services/catalog.service";

interface ImageSearchProps {
  onSearchResult: (description: string) => void;
  disabled?: boolean;
}

export default function ImageSearch({ onSearchResult, disabled }: ImageSearchProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    setFile(e.target.files?.[0] ?? null);
    setError(null);
  }

  async function handleSearch() {
    if (!file || loading) return;
    setLoading(true);
    setError(null);
    try {
      const { description } = await catalogService.describeImage(file);
      onSearchResult(description);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to analyse image");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        style={{ display: "none" }}
        onChange={handleFileChange}
      />

      <Box sx={{ display: "flex", alignItems: "center", gap: 2, flexWrap: "wrap" }}>
        <Button
          variant="outlined"
          startIcon={<UploadFileIcon />}
          onClick={() => inputRef.current?.click()}
          disabled={loading || disabled}
        >
          Select image
        </Button>

        {file && (
          <>
            <Typography variant="body2" color="text.secondary" noWrap sx={{ flex: 1, minWidth: 0 }}>
              {file.name}
            </Typography>
            <Button
              variant="contained"
              startIcon={
                loading ? <CircularProgress size={16} color="inherit" /> : <ImageSearchIcon />
              }
              onClick={handleSearch}
              disabled={loading || disabled}
            >
              {loading ? "Analysing…" : "Search by image"}
            </Button>
          </>
        )}
      </Box>

      {!file && (
        <Typography variant="body2" color="text.secondary">
          Select a coin image to search by visual similarity.
        </Typography>
      )}

      {error && <Alert severity="error">{error}</Alert>}
    </Box>
  );
}
