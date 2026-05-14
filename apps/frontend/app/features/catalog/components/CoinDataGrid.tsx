import { useNavigate, Link } from "react-router";
import { DataGrid, useGridApiRef } from "@mui/x-data-grid";
import type { GridColDef, GridSortModel } from "@mui/x-data-grid";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Tooltip from "@mui/material/Tooltip";
import StarIcon from "@mui/icons-material/Star";
import StarBorderIcon from "@mui/icons-material/StarBorder";
import type { CoinModel } from "../types";
import type { PaginationModel } from "../hooks/useCatalogSearch";

interface CoinDataGridProps {
  rows: CoinModel[];
  total: number;
  loading: boolean;
  apiRef: ReturnType<typeof useGridApiRef>;
  onPaginationModelChange: (m: PaginationModel) => void;
  onSortModelChange: (m: GridSortModel) => void;
  collectionIds: Set<string>;
  collectionLoading: boolean;
  onAddToCollection: (id: string) => Promise<void>;
  onRemoveFromCollection: (id: string) => Promise<void>;
}

export default function CoinDataGrid({
  rows,
  total,
  loading,
  apiRef,
  onPaginationModelChange,
  onSortModelChange,
  collectionIds,
  collectionLoading,
  onAddToCollection,
  onRemoveFromCollection,
}: CoinDataGridProps) {
  const navigate = useNavigate();

  const columns: GridColDef<CoinModel>[] = [
    {
      field: "id",
      headerName: "Record ID",
      width: 130,
      renderCell: ({ row }) => (
        <Link
          to={`/catalog/${row.id}`}
          style={{ color: "inherit" }}
          onClick={(e) => e.stopPropagation()}
        >
          {row.id}
        </Link>
      ),
    },
    { field: "title",       headerName: "Title",       width: 220 },
    { field: "object_type", headerName: "Object Type", width: 140 },
    { field: "date_range",  headerName: "Issue Date",  width: 130, sortable: false },
    {
      field: "denomination",
      headerName: "Denomination",
      width: 160,
      valueFormatter: (value: string[]) => value?.join(", ") ?? "",
    },
    {
      field: "material",
      headerName: "Material",
      width: 140,
      valueFormatter: (value: string[]) => value?.join(", ") ?? "",
    },
    {
      field: "authority",
      headerName: "Authority",
      width: 170,
      valueFormatter: (value: string[]) => value?.join(", ") ?? "",
    },
    {
      field: "geographic",
      headerName: "Mint Location",
      width: 170,
      valueFormatter: (value: string[]) => value?.join(", ") ?? "",
    },
    {
      field: "actions",
      headerName: "Actions",
      width: 220,
      sortable: false,
      renderCell: ({ row }) => {
        const inCollection = collectionIds.has(row.id);
        return (
          <Box sx={{ display: "flex", gap: 0.5, alignItems: "center", height: "100%" }}>
            <Tooltip title={inCollection ? "Remove from collection" : "Add to collection"}>
              <span>
                <IconButton
                  size="small"
                  disabled={collectionLoading}
                  onClick={(e) => {
                    e.stopPropagation();
                    inCollection
                      ? onRemoveFromCollection(row.id)
                      : onAddToCollection(row.id);
                  }}
                  color={inCollection ? "warning" : "default"}
                >
                  {inCollection ? <StarIcon fontSize="small" /> : <StarBorderIcon fontSize="small" />}
                </IconButton>
              </span>
            </Tooltip>
            <Button
              size="small"
              onClick={(e) => {
                e.stopPropagation();
                navigate(`/catalog/${row.id}`);
              }}
            >
              Details
            </Button>
          </Box>
        );
      },
    },
  ];

  return (
    <DataGrid
      apiRef={apiRef}
      rows={rows}
      columns={columns}
      getRowId={(row) => row.id}
      rowCount={total}
      loading={loading}
      paginationMode="server"
      sortingMode="server"
      // initialState — DataGrid owns its pagination/sort state internally.
      // We never pass paginationModel/sortModel as controlled props, which
      // prevents the DataGrid from firing spurious onPaginationModelChange
      // resets when rows or loading state changes.
      initialState={{
        pagination: { paginationModel: { pageSize: 25, page: 0 } },
      }}
      pageSizeOptions={[10, 25, 50]}
      onPaginationModelChange={onPaginationModelChange}
      onSortModelChange={onSortModelChange}
      disableColumnFilter
      disableRowSelectionOnClick
      autoHeight
    />
  );
}
