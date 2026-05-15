import { useEffect, useState } from "react";
import { userService } from "~/services/user.service";
import type { AuthUser } from "~/store/auth";

type UserWithCollection = AuthUser & { collection?: string[] };

export interface UseCollectionReturn {
  collectionIds: Set<string>;
  loading: boolean;
  addToCollection: (id: string) => Promise<void>;
  removeFromCollection: (id: string) => Promise<void>;
}

export function useCollection(): UseCollectionReturn {
  const [collectionIds, setCollectionIds] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    userService
      .getMe()
      .then((me) => {
        const user = me as UserWithCollection;
        setCollectionIds(new Set(user.collection ?? []));
      })
      .catch(() => {
        // non-fatal — collection management degrades gracefully
      })
      .finally(() => setLoading(false));
  }, []);

  async function addToCollection(id: string) {
    setCollectionIds((prev) => new Set([...prev, id]));
    try {
      await userService.addToCollection(id);
    } catch {
      setCollectionIds((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }
  }

  async function removeFromCollection(id: string) {
    setCollectionIds((prev) => {
      const next = new Set(prev);
      next.delete(id);
      return next;
    });
    try {
      await userService.removeFromCollection(id);
    } catch {
      setCollectionIds((prev) => new Set([...prev, id]));
    }
  }

  return { collectionIds, loading, addToCollection, removeFromCollection };
}
