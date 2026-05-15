import { useState } from "react";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import ImageSearch from "./ImageSearch";
import KeywordSearch from "./KeywordSearch";
import type { KeywordSearchState } from "../../types";

interface SearchPanelProps {
  state: KeywordSearchState;
  onChange: (state: KeywordSearchState) => void;
  onSearch: () => void;
  onImageSearchResult: (description: string) => void;
  searchDisabled?: boolean;
}

export default function SearchPanel({
  state,
  onChange,
  onSearch,
  onImageSearchResult,
  searchDisabled,
}: SearchPanelProps) {
  const [tab, setTab] = useState(0);

  function handleImageSearchResult(description: string) {
    onImageSearchResult(description);
    setTab(0); // switch to Keyword Search so user sees the populated query
  }

  return (
    <Paper elevation={0} sx={{ border: 1, borderColor: "divider", borderRadius: 3, p: 3 }}>
      <Tabs
        value={tab}
        onChange={(_, v) => setTab(v)}
        sx={{ mb: 3, borderBottom: 1, borderColor: "divider" }}
      >
        <Tab label="Keyword Search" />
        <Tab label="Image Search" />
      </Tabs>

      <Box>
        {tab === 0 && (
          <KeywordSearch
            state={state}
            onChange={onChange}
            onSearch={onSearch}
            searchDisabled={searchDisabled}
          />
        )}
        {tab === 1 && (
          <ImageSearch onSearchResult={handleImageSearchResult} disabled={searchDisabled} />
        )}
      </Box>
    </Paper>
  );
}
