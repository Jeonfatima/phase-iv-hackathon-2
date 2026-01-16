import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    // Parse the request body
    const { userId, message, conversationId } = await req.json();

    // Validate required fields
    if (!userId || !message) {
      return NextResponse.json(
        { error: 'userId and message are required' },
        { status: 400 }
      );
    }

    // Forward the request to the backend API
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const response = await fetch(`${backendUrl}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${req.headers.get('authorization')?.replace('Bearer ', '') || ''}`,
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId || null
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return NextResponse.json(
        { error: errorData.detail || 'Failed to get response from chat service' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET(req: NextRequest) {
  try {
    // Extract userId from query parameters
    const url = new URL(req.url);
    const userId = url.searchParams.get('userId');
    const conversationId = url.searchParams.get('conversationId');
    const limit = url.searchParams.get('limit') || '50';
    const offset = url.searchParams.get('offset') || '0';

    if (!userId) {
      return NextResponse.json(
        { error: 'userId is required' },
        { status: 400 }
      );
    }

    // Determine which endpoint to call based on presence of conversationId
    let backendEndpoint;
    if (conversationId) {
      // Get messages for a specific conversation
      backendEndpoint = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/${userId}/conversations/${conversationId}/messages?limit=${limit}&offset=${offset}`;
    } else {
      // Get all conversations for the user
      backendEndpoint = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/${userId}/conversations`;
    }

    // Forward the request to the backend API
    const response = await fetch(backendEndpoint, {
      headers: {
        'Authorization': `Bearer ${req.headers.get('authorization')?.replace('Bearer ', '') || ''}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const errorMessage = conversationId
        ? 'Failed to get conversation messages from backend'
        : 'Failed to get conversations from backend';

      return NextResponse.json(
        { error: errorData.detail || errorMessage },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Get Conversations/Messages API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}