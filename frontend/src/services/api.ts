/**
 * API client for backend communication
 */

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/";

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  user_id?: string;
  system_prompt?: string;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  sources?: string[];
  metadata?: Record<string, any>;
}

export interface ConversationHistory {
  conversation_id: string;
  messages: Array<{
    role: "user" | "assistant";
    content: string;
  }>;
  message_count: number;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  /**
   * Send a chat message to the backend
   */
  async sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/api/v1/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Unknown error" }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  /**
   * Get conversation history
   */
  async getConversation(conversationId: string): Promise<ConversationHistory> {
    const response = await fetch(`${this.baseUrl}/api/v1/conversations/${conversationId}`);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Unknown error" }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  /**
   * Check backend health
   */
  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseUrl}/api/v1/health`);
    
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }

    return response.json();
  }
}

export const apiClient = new ApiClient(API_URL);
