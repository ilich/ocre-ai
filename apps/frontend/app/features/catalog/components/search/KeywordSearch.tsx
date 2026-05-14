import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Checkbox from "@mui/material/Checkbox";
import CircularProgress from "@mui/material/CircularProgress";
import FormControlLabel from "@mui/material/FormControlLabel";
import TextField from "@mui/material/TextField";
import SearchIcon from "@mui/icons-material/Search";
import FilterBar from "./FilterBar";
import { useMetadata } from "../../hooks/useMetadata";
import type { KeywordSearchState } from "../../types";

interface KeywordSearchProps {
  state: KeywordSearchState;
  onChange: (state: KeywordSearchState) => void;
  onSearch: () => void;
  searchDisabled?: boolean;
}

export default function KeywordSearch({
  state,
  onChange,
  onSearch,
  searchDisabled,
}: KeywordSearchProps) {
  const { metadata, loading, error } = useMetadata();

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
      <Box sx={{ display: "flex", gap: 1 }}>
        <TextField
          placeholder="Search coins…"
          value={state.query}
          onChange={(e) => onChange({ ...state, query: e.target.value })}
          onKeyDown={(e) => e.key === "Enter" && onSearch()}
          size="small"
          sx={{ flex: 1 }}
        />
        <Button
          variant="contained"
          startIcon={<SearchIcon />}
          onClick={onSearch}
          disabled={searchDisabled}
        >
          Search
        </Button>
      </Box>

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
