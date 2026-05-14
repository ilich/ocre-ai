import { useState } from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import SearchPanel from "~/features/catalog/components/search/SearchPanel";
import { DEFAULT_SEARCH_STATE, type KeywordSearchState } from "~/features/catalog/types";

export function meta() {
  return [{ title: "Catalog — The AI-Based Roman Coin Identification System" }];
}

export default function CatalogPage() {
  const [searchState, setSearchState] = useState<KeywordSearchState>(DEFAULT_SEARCH_STATE);

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
        <SearchPanel state={searchState} onChange={setSearchState} />
      </Box>
    </Container>
  );
}
