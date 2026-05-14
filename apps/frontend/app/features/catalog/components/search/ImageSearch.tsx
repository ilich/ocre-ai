import { useRef, useState } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import UploadFileIcon from "@mui/icons-material/UploadFile";

export default function ImageSearch() {
  const [file, setFile] = useState<File | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    setFile(e.target.files?.[0] ?? null);
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
      <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
        <Button
          variant="outlined"
          startIcon={<UploadFileIcon />}
          onClick={() => inputRef.current?.click()}
        >
          Select image
        </Button>
        {file && (
          <Typography variant="body2" color="text.secondary" noWrap>
            {file.name}
          </Typography>
        )}
      </Box>
      {!file && (
        <Typography variant="body2" color="text.secondary">
          Select a coin image to search by visual similarity.
        </Typography>
      )}
    </Box>
  );
}
