import { request } from "./client";

export interface ChatRequest {
  message: string
  conversation_id?: number
  user_id?: number
  system_prompt?: string
  response_mode?: "standard" | "brief" | "detailed" | "debate" | "risk" | "educational" | "compare"
}

export interface ChatResponse {
  message: string
  conversation_id?: number
  sources?: string[]
  metadata?: Record<string, any>
}

export async function sendChatMessage(data: ChatRequest) {
  console.log(data)
  return request<ChatResponse>("/api/v1/chat", {
    method: "POST",
    body: JSON.stringify(data)
  })
}

export async function sendAuthenticatedChatMessage(
  data: ChatRequest,
  token: string
) {
  console.log("Request: ", data)
  return request<ChatResponse>("/api/v1/chat", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(data)
  })
}