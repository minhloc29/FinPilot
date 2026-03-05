# Multi-Turn Chat API - FastAPI with BaseAgent

This implementation connects FastAPI to the BaseAgent and enables multi-turn conversations with persistent history.

## Overview

The system now supports:
- **Multi-turn conversations** with persistent history
- **Automatic conversation management** (create/retrieve)
- **Database-backed message storage**
- **Configurable system prompts**
- **Conversation history retrieval**

## Architecture

```
User Request → FastAPI Route → ConversationService → BaseAgent → OpenAI API
                    ↓                    ↓
                Database          Conversation History
```

## API Endpoints

### 1. Chat Endpoint (POST /api/v1/chat)

Send a message and get a response. Maintains conversation context automatically.

**Request:**
```json
{
  "message": "What's the current market sentiment?",
  "conversation_id": "optional-uuid",
  "user_id": "user123",
  "system_prompt": "You are a financial advisor"
}
```

**Response:**
```json
{
  "message": "Based on recent data...",
  "conversation_id": "abc-123-def",
  "sources": [],
  "metadata": {
    "model": "gpt-4",
    "message_count": 3
  }
}
```

### 2. Get Conversation (GET /api/v1/conversations/{conversation_id})

Retrieve entire conversation history.

**Response:**
```json
{
  "conversation_id": "abc-123-def",
  "messages": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"}
  ],
  "message_count": 2
}
```

## Usage Examples

### Starting a New Conversation

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Analyze AAPL stock performance",
    "user_id": "user123"
  }'
```

**Response includes a `conversation_id` - save this for the next request!**

### Continuing a Conversation

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What about its competitors?",
    "conversation_id": "abc-123-def",
    "user_id": "user123"
  }'
```

The agent will have full context from previous messages.

### Retrieving Conversation History

```bash
curl -X GET http://localhost:8000/api/v1/conversations/abc-123-def
```

## Configuration

Set these environment variables in your `.env` file:

```env
# Required: OpenAI API Key
OPENAI_API_KEY=sk-your-api-key-here

# Optional: Custom OpenAI Base URL (default: https://api.openai.com/v1)
OPENAI_BASE_URL=https://api.openai.com/v1

# Optional: Model selection (default: gpt-4)
DEFAULT_MODEL=gpt-4o-mini

# Database URL for conversation storage
DATABASE_URL=postgresql://user:password@localhost/financial_copilot
```

## Key Features

### 1. Automatic Conversation Management
- If no `conversation_id` is provided, a new conversation is created
- If `conversation_id` is provided, the existing conversation continues
- All messages are automatically saved to the database

### 2. Multi-Turn Context
- Full conversation history is loaded before each request
- BaseAgent receives complete context from all previous turns
- Enables natural, contextual conversations

### 3. Flexible System Prompts
- Default: "You are a helpful AI financial assistant..."
- Can be customized per request using `system_prompt` field
- Useful for different agent personalities or specialized tasks

### 4. Database Integration
- Conversations stored with UUIDs
- Messages linked to conversations
- Easy retrieval of full conversation history

## Implementation Details

### Files Modified/Created:

1. **`app/services/conversation_service.py`** (NEW)
   - Manages conversation creation and retrieval
   - Handles message storage
   - Provides conversation history in BaseAgent format

2. **`app/api/routes/chat.py`** (UPDATED)
   - Integrates BaseAgent with FastAPI
   - Loads conversation history before each turn
   - Saves messages after each turn

3. **`app/models/conversation.py`** (UPDATED)
   - Uses String IDs (UUIDs) for conversations
   - Proper foreign key relationships

4. **`app/schemas/chat_schema.py`** (UPDATED)
   - Added `system_prompt` field
   - Support for optional conversation parameters

5. **`app/core/config.py`** (UPDATED)
   - Added `OPENAI_BASE_URL` configuration

## Running the Application

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
export OPENAI_API_KEY="your-key-here"
export DATABASE_URL="postgresql://user:password@localhost/financial_copilot"
```

3. **Run database migrations:**
```bash
# Initialize database tables
python -m app.db.init_db
```

4. **Start the server:**
```bash
python app/main.py
```

Or with uvicorn:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. **Test the endpoint:**
```bash
# Start a conversation
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, explain portfolio diversification"}'
```

## Frontend Integration

For a React/Next.js frontend:

```javascript
const sendMessage = async (message, conversationId = null) => {
  const response = await fetch('http://localhost:8000/api/v1/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
      user_id: 'user123'
    })
  });
  
  const data = await response.json();
  
  // Save conversation_id for next message
  return {
    message: data.message,
    conversationId: data.conversation_id
  };
};

// Usage
let convId = null;

// First message
const result1 = await sendMessage("What's diversification?");
convId = result1.conversationId;

// Second message (continues conversation)
const result2 = await sendMessage("Give me an example", convId);
```

## Troubleshooting

### Issue: "Conversation not found"
- The conversation_id doesn't exist in the database
- Solution: Don't provide conversation_id for new conversations

### Issue: "OpenAI API key not set"
- Missing OPENAI_API_KEY environment variable
- Solution: Set it in .env file or environment

### Issue: "Database connection error"
- Database not running or wrong credentials
- Solution: Check DATABASE_URL and ensure PostgreSQL is running

## Next Steps

Consider adding:
- **Streaming responses** for real-time message display
- **Conversation titles** auto-generated from first message
- **User authentication** for multi-user support
- **Message search** across conversations
- **Conversation deletion** endpoint
- **Rate limiting** per user
- **Token usage tracking** for cost management
