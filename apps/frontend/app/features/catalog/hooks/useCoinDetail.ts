import { useEffect, useState } from "react";
import { catalogService } from "~/services/catalog.service";
import type { CoinModel } from "../types";

export interface UseCoinDetailReturn {
  coin: CoinModel | null;
  loading: boolean;
  error: string | null;
}

export function useCoinDetail(id: string): UseCoinDetailReturn {
  const [coin, setCoin]       = useState<CoinModel | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    catalogService
      .getCoinById(id)
      .then(setCoin)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load coin"))
      .finally(() => setLoading(false));
  }, [id]);

  return { coin, loading, error };
}
