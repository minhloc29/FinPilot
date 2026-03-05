import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ChatMessage {
  message: string;
  conversation_id?: string;
  user_id?: string;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  sources: string[];
  metadata: Record<string, any>;
}

export const chatAPI = {
  sendMessage: async (data: ChatMessage): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/chat', data);
    return response.data;
  },

  getConversation: async (conversationId: string) => {
    const response = await api.get(`/conversations/${conversationId}`);
    return response.data;
  },
};

export interface Portfolio {
  id: string;
  user_id: string;
  name: string;
  holdings: Array<{
    symbol: string;
    shares: number;
    average_cost?: number;
  }>;
  total_value?: number;
}

export const portfolioAPI = {
  create: async (data: Omit<Portfolio, 'id'>): Promise<Portfolio> => {
    const response = await api.post<Portfolio>('/portfolio', data);
    return response.data;
  },

  get: async (portfolioId: string): Promise<Portfolio> => {
    const response = await api.get<Portfolio>(`/portfolio/${portfolioId}`);
    return response.data;
  },

  list: async (userId: string): Promise<Portfolio[]> => {
    const response = await api.get<Portfolio[]>('/portfolios', {
      params: { user_id: userId },
    });
    return response.data;
  },

  analyze: async (portfolioId: string) => {
    const response = await api.post(`/portfolio/${portfolioId}/analyze`);
    return response.data;
  },
};

export const healthAPI = {
  check: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
