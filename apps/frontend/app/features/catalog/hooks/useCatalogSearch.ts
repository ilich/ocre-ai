import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router";
import { useGridApiRef } from "@mui/x-data-grid";
import type { GridSortModel } from "@mui/x-data-grid";
import { catalogService } from "~/services/catalog.service";
import type { CatalogOrderBy } from "~/services/catalog.service";
import type { CatalogFilters, CoinModel, KeywordSearchState } from "../types";

const SORTABLE_FIELDS = new Set<string>([
  "id", "title", "object_type", "denomination",
  "manufacturer", "material", "authority", "geographic",
]);

export interface PaginationModel { page: number; pageSize: number }

export interface UseCatalogSearchReturn {
  searchState: KeywordSearchState;
  setSearchState: (s: KeywordSearchState) => void;
  commitSearch: () => void;
  onPaginationModelChange: (m: PaginationModel) => void;
  onSortModelChange: (m: GridSortModel) => void;
  gridApiRef: ReturnType<typeof useGridApiRef>;
  rows: CoinModel[];
  total: number;
  loading: boolean;
  error: string | null;
}

function getFiltersFromUrl(p: URLSearchParams): CatalogFilters {
  return {
    material:     p.get("material")     ?? "",
    denomination: p.get("denomination") ?? "",
    object_type:  p.get("object_type")  ?? "",
    manufacturer: p.get("manufacturer") ?? "",
    authority:    p.get("authority")    ?? "",
    geographic:   p.get("geographic")   ?? "",
  };
}

export function useCatalogSearch(): UseCatalogSearchReturn {
  const [searchParams, setSearchParams] = useSearchParams();

  // apiRef lets us programmatically reset the DataGrid's internal page
  const gridApiRef = useGridApiRef();

  // Filters and committed query live in the URL
  const committedQuery = searchParams.get("q") ?? "";
  const filters        = getFiltersFromUrl(searchParams);
  const myCollection   = searchParams.get("my") === "1";

  // Live text field — local only
  const [liveQuery, setLiveQuery] = useState(committedQuery);

  // Pagination and sort — local state, never synced to URL
  const [page, setPage]           = useState(0);
  const [pageSize, setPageSize]   = useState(25);
  const [sortField, setSortField] = useState("");
  const [sortDir, setSortDir]     = useState<"asc" | "desc">("asc");

  // API results
  const [rows, setRows]       = useState<CoinModel[]>([]);
  const [total, setTotal]     = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState<string | null>(null);
  const fetchIdRef            = useRef(0);

  useEffect(() => {
    const id = ++fetchIdRef.current;
    setLoading(true);
    setError(null);

    const orderBy = SORTABLE_FIELDS.has(sortField)
      ? (sortField as CatalogOrderBy)
      : undefined;

    catalogService
      .findCoins({
        search:       committedQuery || null,
        material:     filters.material     || null,
        denomination: filters.denomination || null,
        object_type:  filters.object_type  || null,
        manufacturer: filters.manufacturer || null,
        authority:    filters.authority    || null,
        geographic:   filters.geographic   || null,
        my:           myCollection || undefined,
        order_by:     orderBy,
        order_direction: orderBy ? sortDir : undefined,
        skip:  page * pageSize,
        limit: pageSize,
      })
      .then((res) => {
        if (id !== fetchIdRef.current) return;
        setRows(res.items);
        setTotal(res.total);
      })
      .catch((err) => {
        if (id !== fetchIdRef.current) return;
        setError(err instanceof Error ? err.message : "Failed to load coins");
      })
      .finally(() => {
        if (id === fetchIdRef.current) setLoading(false);
      });
  }, [
    committedQuery,
    filters.material, filters.denomination, filters.object_type,
    filters.manufacturer, filters.authority, filters.geographic,
    myCollection,
    page, pageSize, sortField, sortDir,
  ]);

  // Reset both our state and the DataGrid's internal page counter
  function resetPage() {
    setPage(0);
    gridApiRef.current?.setPage?.(0);
  }

  function writeUrl(q: string, f: CatalogFilters, my: boolean) {
    const next = new URLSearchParams();
    if (q)              next.set("q",            q);
    if (f.material)     next.set("material",     f.material);
    if (f.denomination) next.set("denomination", f.denomination);
    if (f.object_type)  next.set("object_type",  f.object_type);
    if (f.manufacturer) next.set("manufacturer", f.manufacturer);
    if (f.authority)    next.set("authority",    f.authority);
    if (f.geographic)   next.set("geographic",   f.geographic);
    if (my)             next.set("my",           "1");
    setSearchParams(next, { replace: true });
  }

  function setSearchState(newState: KeywordSearchState) {
    setLiveQuery(newState.query);

    const filtersChanged =
      JSON.stringify(newState.filters) !== JSON.stringify(filters) ||
      newState.myCollection !== myCollection;

    if (filtersChanged) {
      resetPage();
      writeUrl(committedQuery, newState.filters, newState.myCollection);
    }
  }

  function commitSearch() {
    resetPage();
    writeUrl(liveQuery, filters, myCollection);
  }

  function onPaginationModelChange(m: PaginationModel) {
    setPage(m.page);
    setPageSize(m.pageSize);
  }

  function onSortModelChange(m: GridSortModel) {
    const first = m[0];
    setSortField(first?.field ?? "");
    setSortDir(first?.sort === "desc" ? "desc" : "asc");
    resetPage();
  }

  const searchState: KeywordSearchState = { query: liveQuery, filters, myCollection };

  return {
    searchState, setSearchState, commitSearch,
    onPaginationModelChange, onSortModelChange,
    gridApiRef,
    rows, total, loading, error,
  };
}
