export interface CoinModel {
  id: string;
  title: string;
  description: string | null;
  object_type: string;
  date_range: string | null;
  denomination: string[];
  manufacturer: string[];
  material: string[];
  authority: string[];
  geographic: string[];
  images: string[];
}

export interface CoinListResponse {
  items: CoinModel[];
  total: number;
}

export interface CoinImageDescriptionResponse {
  description: string;
}

export interface MetadataItem {
  key: string;
  values: string[];
}

export type MetadataMap = Partial<Record<string, string[]>>;

export interface CatalogFilters {
  material: string;
  denomination: string;
  object_type: string;
  manufacturer: string;
  authority: string;
  geographic: string;
}

export interface KeywordSearchState {
  query: string;
  filters: CatalogFilters;
  myCollection: boolean;
}

export const DEFAULT_FILTERS: CatalogFilters = {
  material: "",
  denomination: "",
  object_type: "",
  manufacturer: "",
  authority: "",
  geographic: "",
};

export const DEFAULT_SEARCH_STATE: KeywordSearchState = {
  query: "",
  filters: DEFAULT_FILTERS,
  myCollection: false,
};
