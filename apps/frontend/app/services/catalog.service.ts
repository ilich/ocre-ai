import { apiClient } from "./api";
import type {
  CoinImageDescriptionResponse,
  CoinListResponse,
  MetadataItem,
} from "~/features/catalog/types";

export type CatalogOrderBy =
  | "relevance"
  | "id"
  | "title"
  | "from_year"
  | "to_year"
  | "object_type"
  | "denomination"
  | "manufacturer"
  | "material"
  | "authority"
  | "geographic";

export interface FindCoinsParams {
  my?: boolean;
  search?: string | null;
  from_year?: number | null;
  to_year?: number | null;
  denomination?: string | null;
  manufacturer?: string | null;
  material?: string | null;
  authority?: string | null;
  geographic?: string | null;
  order_by?: CatalogOrderBy;
  order_direction?: "asc" | "desc";
  skip?: number;
  limit?: number;
}

export const catalogService = {
  getMetadata: () => apiClient.get<MetadataItem[]>("/catalog/metadata"),

  findCoins: (params: FindCoinsParams = {}) => {
    const query = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== null && value !== "") {
        query.set(key, String(value));
      }
    }
    const qs = query.toString();
    return apiClient.get<CoinListResponse>(`/catalog${qs ? `?${qs}` : ""}`);
  },

  describeImage: (image: File) => {
    const form = new FormData();
    form.append("image", image);
    return apiClient.postForm<CoinImageDescriptionResponse>("/catalog/image", form);
  },
};
