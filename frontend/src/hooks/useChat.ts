import { useState, useCallback } from 'react';
import { chatAPI } from '../services/api';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  metadata?: {
    sources?: string[];
    [key: string]: any;
  };
}

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    // Add user message
    const userMessage: Message = {
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Call API
      const response = await chatAPI.sendMessage({
        message: content,
        conversation_id: conversationId || undefined,
        user_id: 'demo_user', // TODO: Get from auth
      });

      // Add assistant message
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString(),
        metadata: {
          sources: response.sources,
          ...response.metadata,
        },
      };
      setMessages((prev) => [...prev, assistantMessage]);

      // Update conversation ID
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [conversationId]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setConversationId(null);
  }, []);

  return {
    messages,
    sendMessage,
    clearMessages,
    isLoading,
    conversationId,
  };
};
