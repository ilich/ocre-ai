import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { ChatHistoryItem } from "~/services/chat.service";

interface ChatState {
  isOpen: boolean;
  history: ChatHistoryItem[];
  coinsContext: string[];

  toggle: () => void;
  close: () => void;
  clearHistory: () => void;
  setCoinsContext: (ids: string[]) => void;
  appendMessage: (msg: ChatHistoryItem) => void;
}

export const useChatStore = create<ChatState>()(
  persist(
    (set) => ({
      isOpen: false,
      history: [],
      coinsContext: [],

      toggle: () => set((s) => ({ isOpen: !s.isOpen })),
      close: () => set({ isOpen: false }),
      clearHistory: () => set({ history: [] }),
      setCoinsContext: (ids) => set({ coinsContext: ids }),
      appendMessage: (msg) => set((s) => ({ history: [...s.history, msg] })),
    }),
    {
      name: "chat",
      // Only history is persisted; open state and context reset each session
      partialize: (s) => ({ history: s.history }),
    }
  )
);
