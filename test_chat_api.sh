#!/bin/bash
# Test script for AI Financial Copilot Chat API

BASE_URL="http://localhost:8000"

echo "==================================="
echo "AI Financial Copilot - API Test"
echo "==================================="

# Test 1: Health Check
echo -e "\n1. Testing Health Endpoint..."
curl -X GET "${BASE_URL}/api/v1/health" \
  -H "Content-Type: application/json"

# Test 2: Simple Chat Request (New Conversation)
echo -e "\n\n2. Testing Chat Endpoint (New Conversation)..."
RESPONSE=$(curl -s -X POST "${BASE_URL}/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the current price of AAPL?"
  }')

echo "$RESPONSE" | python3 -m json.tool

# Extract conversation_id for next request
CONVERSATION_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('conversation_id', ''))" 2>/dev/null)

# Test 3: Continue Existing Conversation
if [ ! -z "$CONVERSATION_ID" ]; then
  echo -e "\n\n3. Testing Chat Endpoint (Continue Conversation)..."
  curl -s -X POST "${BASE_URL}/api/v1/chat" \
    -H "Content-Type: application/json" \
    -d "{
      \"message\": \"What about its P/E ratio?\",
      \"conversation_id\": \"$CONVERSATION_ID\",
      \"user_id\": \"test_user_123\"
    }" | python3 -m json.tool

  # Test 4: Retrieve Conversation History
  echo -e "\n\n4. Testing Get Conversation History..."
  curl -s -X GET "${BASE_URL}/api/v1/conversations/${CONVERSATION_ID}" \
    -H "Content-Type: application/json" | python3 -m json.tool
fi

# Test 5: Financial Analysis Request
echo -e "\n\n5. Testing Financial Analysis Request..."
curl -s -X POST "${BASE_URL}/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Analyze the risk profile of a portfolio with 60% stocks and 40% bonds",
    "user_id": "test_user_123"
  }' | python3 -m json.tool

# Test 6: Market Data Request
echo -e "\n\n6. Testing Market Data Request..."
curl -s -X POST "${BASE_URL}/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Get me the latest market news about Tesla",
    "user_id": "test_user_123"
  }' | python3 -m json.tool

# Test 7: Portfolio Management Request
echo -e "\n\n7. Testing Portfolio Management Request..."
curl -s -X POST "${BASE_URL}/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to create a diversified portfolio with $10,000",
    "user_id": "test_user_123",
    "system_prompt": "You are a helpful financial advisor."
  }' | python3 -m json.tool

echo -e "\n\n==================================="
echo "Tests Completed!"
echo "==================================="
