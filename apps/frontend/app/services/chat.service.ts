import { apiClient } from "./api";

export interface ChatHistoryItem {
  role: "user" | "assistant";
  content: string;
}

export interface ChatAttachment {
  filename: string;
  content_type: string;
  data: string;
}

export interface ChatRequest {
  message: string;
  history?: ChatHistoryItem[] | null;
  coins_context?: string[] | null;
  attachment?: ChatAttachment | null;
}

export interface ChatResponse {
  message: string;
}

export const chatService = {
  chat: (body: ChatRequest) =>
    apiClient.post<ChatResponse>("/chat", body),
};
