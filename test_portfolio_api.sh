#!/bin/bash

# Portfolio API Testing Script
# Make sure to set your JWT token first

BASE_URL="http://localhost:8000"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsInVzZXJfaWQiOjEsImV4cCI6MTc3MzgyNDkxOX0.uhrsnBWtgQntEj3P2JfEnVh9K5Tt2oyd6G4e6RXXp3o"

echo "=== Portfolio API Tests ==="
echo ""

# 1. Create a new portfolio
echo "1. Creating a new portfolio..."
curl -X POST "http://localhost:8000/api/v1/portfolio" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsInVzZXJfaWQiOjEsImV4cCI6MTc3MzgyNDkxOX0.uhrsnBWtgQntEj3P2JfEnVh9K5Tt2oyd6G4e6RXXp3o" \
  -d '{
    "name": "My Investment Portfolio",
    "description": "Tech stocks and ETFs",
    "holdings": [
      {
        "symbol": "AAPL",
        "shares": 10,
        "average_cost": 150.50
      },
      {
        "symbol": "GOOGL",
        "shares": 5,
        "average_cost": 2800.00
      },
      {
        "symbol": "MSFT",
        "shares": 15,
        "average_cost": 350.75
      }
    ]
  }'

curl -X POST http://localhost:8000/api/v1/user-profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsInVzZXJfaWQiOjEsImV4cCI6MTc3MzgyNDkxOX0.uhrsnBWtgQntEj3P2JfEnVh9K5Tt2oyd6G4e6RXXp3o" \
  -d '{
    "age": 30,
    "country": "USA",
    "investment_experience": "intermediate",
    "annual_income": 75000,
    "monthly_savings": 2000,
    "financial_goal": "Retirement planning and wealth accumulation",
    "risk_profile": "moderate",
    "max_drawdown_tolerance": 20.0,
    "investment_horizon_years": 15,
    "capital": 50000,
    "monthly_investment": 1500,
    "rebalance_frequency": "quarterly",
    "preferred_sectors": ["Technology", "Healthcare", "Finance"],
    "avoid_sectors": ["Tobacco", "Gambling"],
    "dividend_preference": true,
    "esg_preference": true,
    "emergency_fund_months": 6,
    "portfolio": [
      {
        "ticker": "AAPL",
        "shares": 10,
        "avg_price": 150.50
      },
      {
        "ticker": "MSFT",
        "shares": 5,
        "avg_price": 300.00
      }
    ]
  }'

# 2. Get portfolio by ID (replace 1 with actual portfolio_id)
echo "2. Getting portfolio details..."
curl -X GET "$BASE_URL/portfolio/1" \
  -H "Authorization: Bearer $TOKEN"
echo -e "\n"

# 3. List all portfolios
echo "3. Listing all portfolios..."
curl -X GET "$BASE_URL/portfolios" \
  -H "Authorization: Bearer $TOKEN"
echo -e "\n"

# 4. Add a holding to portfolio
echo "4. Adding a new holding to portfolio..."
curl -X POST "$BASE_URL/portfolio/1/holdings" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "symbol": "TSLA",
    "shares": 8,
    "average_cost": 650.25
  }'
echo -e "\n"

# 5. Analyze portfolio
echo "5. Analyzing portfolio..."
curl -X POST "$BASE_URL/portfolio/1/analyze" \
  -H "Authorization: Bearer $TOKEN"
echo -e "\n"

# 6. Delete a holding (replace 1 with actual holding_id)
echo "6. Deleting a holding..."
curl -X DELETE "$BASE_URL/holdings/1" \
  -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "=== Tests Complete ==="
