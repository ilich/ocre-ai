import { useState } from "react";
import { chatService } from "~/services/chat.service";
import { useChatStore } from "~/store/chat";

export function useChat() {
  const [loading, setLoading] = useState(false);
  const { history, coinsContext, appendMessage } = useChatStore();

  async function sendMessage(text: string) {
    const trimmed = text.trim();
    if (!trimmed || loading) return;

    const previousHistory = [...history];
    appendMessage({ role: "user", content: trimmed });
    setLoading(true);

    try {
      const res = await chatService.chat({
        message: trimmed,
        history: previousHistory.length ? previousHistory : null,
        coins_context: coinsContext.length ? coinsContext : null,
      });
      appendMessage({ role: "assistant", content: res.message });
    } catch (err) {
      appendMessage({
        role: "assistant",
        content: err instanceof Error ? `⚠ ${err.message}` : "⚠ Something went wrong.",
      });
    } finally {
      setLoading(false);
    }
  }

  return { sendMessage, loading };
}
