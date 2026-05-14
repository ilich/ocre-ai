import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import CoinDataGrid from "~/features/catalog/components/CoinDataGrid";
import SearchPanel from "~/features/catalog/components/search/SearchPanel";
import { useCollection } from "~/features/catalog/hooks/useCollection";
import { useCatalogSearch } from "~/features/catalog/hooks/useCatalogSearch";

export function meta() {
  return [{ title: "Catalog — The AI-Based Roman Coin Identification System" }];
}

export default function CatalogPage() {
  const {
    searchState, setSearchState, commitSearch,
    onPaginationModelChange, onSortModelChange,
    gridApiRef,
    rows, total, loading, error,
  } = useCatalogSearch();

  const {
    collectionIds,
    loading: collectionLoading,
    addToCollection,
    removeFromCollection,
  } = useCollection();

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
        <SearchPanel
          state={searchState}
          onChange={setSearchState}
          onSearch={commitSearch}
          searchDisabled={loading}
        />

        {error && <Alert severity="error">{error}</Alert>}

        <CoinDataGrid
          rows={rows}
          total={total}
          loading={loading}
          apiRef={gridApiRef}
          onPaginationModelChange={onPaginationModelChange}
          onSortModelChange={onSortModelChange}
          collectionIds={collectionIds}
          collectionLoading={collectionLoading}
          onAddToCollection={addToCollection}
          onRemoveFromCollection={removeFromCollection}
        />
      </Box>
    </Container>
  );
}
