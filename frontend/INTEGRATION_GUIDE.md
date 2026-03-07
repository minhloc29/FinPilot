# Connecting React Frontend to FastAPI Backend

## Setup Complete! 🎉

I've successfully configured your React app to connect to the FastAPI chat endpoint.

## What Was Changed:

### 1. **Created API Service** [`src/services/api.ts`](src/services/api.ts)
   - Centralized API client for backend communication
   - TypeScript interfaces matching your FastAPI schemas
   - Error handling and response parsing
   - Methods for chat, conversation history, and health checks

### 2. **Updated ChatPanel** [`src/components/chat/ChatPanel.tsx`](src/components/chat/ChatPanel.tsx)
   - Replaced mock responses with real API calls
   - Added conversation ID tracking
   - Error handling with toast notifications
   - Maintains user messages during API calls

### 3. **Environment Configuration**
   - Created [`.env.development`](.env.development) with `VITE_API_URL`
   - Created [`.env.example`](.env.example) for reference
   - API URL defaults to `http://localhost:8000`

## How to Use:

### 1. **Start the Backend:**
```bash
cd backend
python app/main.py
# Or with uvicorn:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. **Start the Frontend:**
```bash
cd frontend
npm run dev
# Or with bun:
bun run dev
```

### 3. **Test the Connection:**
The app will automatically connect to `http://localhost:8000/api/v1/chat`

## API Endpoints Used:

- **POST** `/api/v1/chat` - Send chat messages
- **GET** `/api/v1/conversations/{id}` - Get conversation history
- **GET** `/api/v1/health` - Health check

## Request/Response Flow:

```typescript
// When user sends a message:
{
  message: "What stocks should I buy?",
  conversation_id: "abc123", // optional, for continuing conversations
  user_id: "default-user"
}

// Backend responds:
{
  message: "Based on market analysis...",
  conversation_id: "abc123",
  sources: [],
  metadata: {
    model: "Qwen3-32B",
    message_count: 2
  }
}
```

## Features Implemented:

✅ Real-time chat with PlannerAgent orchestration  
✅ Conversation history persistence  
✅ Automatic intent detection (market, portfolio, risk, news)  
✅ Error handling with user-friendly messages  
✅ Loading states while waiting for responses  
✅ TypeScript type safety  
✅ CORS configured (check `ALLOWED_ORIGINS` in backend config)  

## Environment Variables:

Create a `.env` file in the frontend directory:
```env
VITE_API_URL=http://localhost:8000
```

For production, update to your deployed backend URL.

## Troubleshooting:

**CORS Errors?**  
Check `ALLOWED_ORIGINS` in `backend/app/core/config.py`:
```python
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite default
    "http://localhost:8000"
]
```

**Connection Refused?**  
Make sure the backend is running on port 8000

**API Not Found?**   
Verify the API prefix is `/api/v1` in your FastAPI routes

## Try These Queries:

- "What's the price of AAPL?"
- "Analyze my portfolio"
- "Show me market news"
- "What's my risk exposure?"

The PlannerAgent will automatically route to the appropriate specialized agent!
