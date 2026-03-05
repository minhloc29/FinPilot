// TypeScript type definitions

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  metadata?: {
    sources?: string[];
    [key: string]: any;
  };
}

export interface Portfolio {
  id: string;
  user_id: string;
  name: string;
  total_value?: number;
  holdings: Holding[];
  created_at: string;
}

export interface Holding {
  symbol: string;
  shares: number;
  average_cost?: number;
  value?: number;
  change?: number;
  changePercent?: number;
}

export interface User {
  id: string;
  email: string;
  full_name?: string;
  is_active: boolean;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  sources: string[];
  metadata: Record<string, any>;
}
