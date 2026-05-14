import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Checkbox from "@mui/material/Checkbox";
import CircularProgress from "@mui/material/CircularProgress";
import FormControlLabel from "@mui/material/FormControlLabel";
import TextField from "@mui/material/TextField";
import FilterBar from "./FilterBar";
import { useMetadata } from "../../hooks/useMetadata";
import type { KeywordSearchState } from "../../types";

interface KeywordSearchProps {
  state: KeywordSearchState;
  onChange: (state: KeywordSearchState) => void;
}

export default function KeywordSearch({ state, onChange }: KeywordSearchProps) {
  const { metadata, loading, error } = useMetadata();

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
      <TextField
        placeholder="Search coins…"
        value={state.query}
        onChange={(e) => onChange({ ...state, query: e.target.value })}
        fullWidth
        size="small"
      />

      {error && <Alert severity="warning">{error}</Alert>}

      {loading ? (
        <CircularProgress size={20} />
      ) : (
        <FilterBar
          metadata={metadata}
          filters={state.filters}
          onChange={(filters) => onChange({ ...state, filters })}
        />
      )}

      <FormControlLabel
        control={
          <Checkbox
            checked={state.myCollection}
            onChange={(e) =>
              onChange({ ...state, myCollection: e.target.checked })
            }
            size="small"
          />
        }
        label="My Collection only"
      />
    </Box>
  );
}
