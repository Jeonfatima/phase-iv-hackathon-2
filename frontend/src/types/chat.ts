export interface Conversation {
  id: number;
  userId: string;
  createdAt: Date;
}

export interface Message {
  id: number;
  conversationId: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  conversationId?: number;
  message: string;
}

export interface ChatResponse {
  conversationId: number;
  response: string;
  toolCalls?: Array<any>;
  messageId: number;
}

export interface ChatState {
  messages: Message[];
  isLoading: boolean;
  conversationId?: number;
  error?: string;
}