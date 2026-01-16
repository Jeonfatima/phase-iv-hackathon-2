import { ChatRequest, ChatResponse } from '../src/types/chat';

class ChatService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || '';
  }

  async sendMessage(userId: string, request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('auth-token') || ''}`, // Adjust based on your auth method
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getConversations(userId: string): Promise<{ conversations: any[]; total_count: number }> {
    const response = await fetch(`${this.baseUrl}/api/chat?userId=${userId}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('auth-token') || ''}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getConversationMessages(
    userId: string,
    conversationId: number,
    limit: number = 50,
    offset: number = 0
  ): Promise<{ messages: any[]; conversation_id: number }> {
    const response = await fetch(
      `${this.baseUrl}/api/chat?userId=${userId}&conversationId=${conversationId}&limit=${limit}&offset=${offset}`,
      {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth-token') || ''}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
}

export default new ChatService();