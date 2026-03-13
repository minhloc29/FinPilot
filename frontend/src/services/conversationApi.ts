import { request } from "./client";

export interface ConversationHistory {
  conversation_id: string
  messages: {
    role: "user" | "assistant"
    content: string
  }[]
  message_count: number
}

export async function getConversation(conversationId: string) {
  return request<ConversationHistory>(
    `/api/v1/conversations/${conversationId}`
  )
}