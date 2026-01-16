// Define the Message interface for chat functionality
export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string; // ISO date string
}

// Define the Conversation interface
export interface Conversation {
  id: number;
  user_id: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

// Define the Chat API Response interface
export interface ChatResponse {
  conversation_id: number;
  response: string;
  message_id: number;
  tool_calls?: Array<any>; // Specific to tool usage
}

// Define the Chat API Request interface
export interface ChatRequest {
  message: string;
  conversation_id?: number;
}

// Define Chat State
export interface ChatState {
  messages: Message[];
  currentConversationId?: number;
  isLoading: boolean;
  error: string | null;
}