# Chat API Test Commands

Quick reference for testing the AI Financial Copilot Chat API.

## Base URL
```bash
BASE_URL="http://localhost:8000"
```

## 1. Health Check
```bash
curl -X GET http://localhost:8000/api/v1/health \
  -H "Content-Type: application/json"
```

## 2. Simple Chat Request (New Conversation)
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the current price of AAPL?"
  }'
```

## 3. Chat with User ID
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Analyze TSLA stock performance",
    "user_id": "user_123"
  }'
```

## 4. Continue Existing Conversation
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What about its P/E ratio?",
    "conversation_id": "YOUR_CONVERSATION_ID",
    "user_id": "user_123"
  }'
```

## 5. Chat with Custom System Prompt
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Give me investment advice for retirement",
    "user_id": "user_123",
    "system_prompt": "You are a conservative financial advisor focused on retirement planning."
  }'
```

## 6. Get Conversation History
```bash
curl -X GET http://localhost:8000/api/v1/conversations/YOUR_CONVERSATION_ID \
  -H "Content-Type: application/json"
```

## Example Financial Queries

### Market Data
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Get me the latest market news about Tesla and Apple"
  }'
```

### Portfolio Analysis
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Analyze the risk profile of a portfolio with 60% stocks, 30% bonds, and 10% commodities"
  }'
```

### Investment Planning
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have $50,000 to invest with a 5-year time horizon. What would you recommend?"
  }'
```

### Technical Analysis
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Perform technical analysis on Bitcoin for the last 30 days"
  }'
```

### Risk Assessment
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Calculate Value at Risk (VaR) for my portfolio: 100 shares of AAPL, 50 shares of GOOGL"
  }'
```

## Response Format

The API returns a JSON response with:
```json
{
  "message": "String containing the AI response",
  "conversation_id": "unique-conversation-id",
  "sources": [],
  "metadata": {
    "model": "gemma-3-27b-it",
    "message_count": 2
  }
}
```

## Pretty Print JSON (Optional)

Add `| jq` or `| python3 -m json.tool` to format output:
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test"}' | jq
```

## Run Automated Test Script

Execute all tests at once:
```bash
./test_chat_api.sh
```
