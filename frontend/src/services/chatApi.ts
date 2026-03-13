import { request } from "./client";

export interface ChatRequest {
  message: string
  conversation_id?: string
  user_id?: string
  system_prompt?: string
}

export interface ChatResponse {
  message: string
  conversation_id: string
  sources?: string[]
  metadata?: Record<string, any>
}

export async function sendChatMessage(data: ChatRequest) {
  return request<ChatResponse>("/api/v1/chat", {
    method: "POST",
    body: JSON.stringify(data)
  })
}

export async function sendAuthenticatedChatMessage(
  data: ChatRequest,
  token: string
) {
  return request<ChatResponse>("/api/v1/chat", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(data)
  })
}