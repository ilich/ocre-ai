import { useEffect, useState } from "react";
import { catalogService } from "~/services/catalog.service";
import type { MetadataMap } from "../types";

export function useMetadata() {
  const [metadata, setMetadata] = useState<MetadataMap>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    catalogService
      .getMetadata()
      .then((items) => {
        const map: MetadataMap = {};
        for (const item of items) {
          map[item.key] = item.values;
        }
        setMetadata(map);
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Failed to load filters");
      })
      .finally(() => setLoading(false));
  }, []);

  return { metadata, loading, error };
}
