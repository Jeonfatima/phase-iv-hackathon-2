import { useState, useCallback } from 'react';
import { ChatState, Message, ChatRequest, ChatResponse } from '../src/types/chat';

const useChat = (userId: string) => {
  const [state, setState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    conversationId: undefined,
    error: undefined,
  });

  const sendMessage = useCallback(async (message: string) => {
    // Check if userId is valid
    if (!userId || userId === 'undefined' || userId === '') {
      console.error('Invalid userId provided to useChat:', userId);
      setState(prev => ({
        ...prev,
        error: 'User not authenticated. Please log in.',
      }));
      return;
    }

    console.log('Sending message with userId:', userId);

    // Optimistic update: Add user message immediately
    const tempUserId = Date.now();
    const userMessage: Message = {
      id: tempUserId,
      conversationId: state.conversationId || Date.now(),
      role: 'user',
      content: message,
      timestamp: new Date(),
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: undefined
    }));

    try {
      const requestBody: ChatRequest = {
        message,
        ...(state.conversationId && { conversationId: state.conversationId })
      };

      // Determine the API base URL
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

      console.log('Making fetch request to:', `${apiBaseUrl}/api/${userId}/chat`, 'with body:', requestBody);

      const response = await fetch(`${apiBaseUrl}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('auth-token') || ''}` // Adjust based on your auth method
        },
        body: JSON.stringify(requestBody),
      });

      console.log('Response status:', response.status);

      if (!response.ok) {
        // Even if API fails, keep the user message and add an error message
        const errorText = await response.text();
        console.error('API error:', response.status, errorText);

        const errorMessage: Message = {
          id: Date.now(),
          conversationId: state.conversationId || Date.now(),
          role: 'assistant',
          content: `Sorry, I couldn't process your message. Error: ${response.status}`,
          timestamp: new Date(),
        };

        setState(prev => ({
          messages: [...prev.messages, errorMessage], // Add error message to existing messages
          isLoading: false,
          error: `HTTP error! status: ${response.status}`,
          conversationId: prev.conversationId
        }));

        return;
      }

      const data: ChatResponse = await response.json();
      console.log('API response data:', data);

      // Add assistant message to replace the temporary user message handling
      const assistantMessage: Message = {
        id: data.messageId,
        conversationId: data.conversationId,
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      };

      setState(prev => ({
        messages: [...prev.messages.slice(0, -1), userMessage, assistantMessage], // Replace the error handling, just append assistant
        isLoading: false,
        conversationId: data.conversationId || prev.conversationId,
      }));
    } catch (error) {
      console.error('Network error sending message:', error);

      // Add an error message to show user that there was a problem
      const errorMessage: Message = {
        id: Date.now(),
        conversationId: state.conversationId || Date.now(),
        role: 'assistant',
        content: "Sorry, I'm having trouble connecting right now. Please check your connection and try again.",
        timestamp: new Date(),
      };

      setState(prev => ({
        messages: [...prev.messages, errorMessage],
        isLoading: false,
        error: 'Network error. Please try again.',
      }));
    }
  }, [state.conversationId, userId, state.messages.length]); // Added state.messages.length to dependency array

  const addMessage = useCallback((message: Message) => {
    setState(prev => ({
      ...prev,
      messages: [...prev.messages, message]
    }));
  }, []);

  const clearMessages = useCallback(() => {
    setState(prev => ({
      ...prev,
      messages: [],
      conversationId: undefined
    }));
  }, []);

  return {
    ...state,
    sendMessage,
    addMessage,
    clearMessages,
  };
};

export default useChat;