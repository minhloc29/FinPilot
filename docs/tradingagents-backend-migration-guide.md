# FinPilot Backend Migration Guide: Replace Legacy Agents with TradingAgents

## 1. Goal

Replace the old backend agent logic in `backend/app/agents` with the new TradingAgents pipeline in `tradingagents`, while preserving the frontend API contract currently used by `frontend/src/services`.

This guide is based on the current repository state.

## 2. Reality Check on Debate Design

Your idea is mostly right, but there is one correction:

- You are right that there is a 2-side investment debate in TradingAgents: Bull vs Bear.
- There is also a second debate stage with 3 risk personas: Aggressive, Conservative, Neutral.
- Final decisions are synthesized by manager nodes.

Evidence in code:

- Investment debate flow: `tradingagents/graph/conditional_logic.py`
- Bull side: `tradingagents/agents/researchers/bull_researcher.py`
- Bear side: `tradingagents/agents/researchers/bear_researcher.py`
- Risk debate flow: `tradingagents/graph/conditional_logic.py`
- Risk debaters: `tradingagents/agents/risk_mgmt/*.py`
- Final portfolio decision node: `tradingagents/agents/managers/portfolio_manager.py`

## 3. Current Backend and Frontend Contracts

### 3.1 Frontend contract currently expected

- Chat request/response shape is defined in:
  - `frontend/src/services/chatApi.ts`
  - `frontend/src/components/chat/ChatPanel.tsx`
- FE expects:
  - request: `message`, optional `conversation_id`, optional `user_id`
  - response: `message`, `conversation_id`, optional `sources`, optional `metadata`

### 3.2 Backend route currently serving FE

- Chat endpoint:
  - `backend/app/api/routes/chat.py`
- Schema:
  - `backend/app/schemas/chat_schema.py`
- Current implementation uses old planner path:
  - `PlannerAgent` from `backend/app/agents/planner_agent.py`

### 3.3 TradingAgents output shape

- Main entrypoint:
  - `tradingagents/graph/trading_graph.py`
- Return from `propagate(company_name, trade_date)`:
  - tuple `(final_state, signal)`
- `final_state` includes rich fields:
  - `market_report`, `sentiment_report`, `news_report`, `fundamentals_report`
  - `investment_debate_state`, `risk_debate_state`
  - `investment_plan`, `trader_investment_plan`, `final_trade_decision`
- `signal` is normalized as one of:
  - `BUY`, `OVERWEIGHT`, `HOLD`, `UNDERWEIGHT`, `SELL`

## 4. Migration Strategy (Recommended)

Do not let FE call TradingAgents directly.

Reason:

- FE is browser TypeScript; TradingAgents runs Python and needs server-side API keys.
- FE should continue calling FastAPI endpoints.

Recommended architecture:

1. Keep FE unchanged for phase 1.
2. Replace backend internals behind existing endpoints.
3. Add adapter layer that maps TradingAgents output to existing FE response schema.

## 5. Step-by-Step Plan

## Step 0: Safety branch and rollback point

- Create migration branch:
  - `git checkout -b feat/migrate-backend-to-tradingagents`
- Tag current working point:
  - `git tag backup/pre-tradingagents-migration`

## Step 1: Add required dependencies for TradingAgents runtime

Current `backend/requirements.txt` is missing several TradingAgents runtime deps.

Add at least:

- `langgraph`
- `langchain-openai`
- `langchain-anthropic`
- `langchain-google-genai`
- `langchain-core`
- `rank-bm25`
- `stockstats`
- `python-dateutil`

Keep existing libs already used by backend routes/auth/db.

## Step 2: Standardize backend config for new runtime

Extend `backend/app/core/config.py` with TradingAgents settings:

- `TRADINGAGENTS_ENABLED: bool = True`
- `TRADINGAGENTS_LLM_PROVIDER: str = "openai"`
- `TRADINGAGENTS_DEEP_MODEL: str = "gpt-5.2"`
- `TRADINGAGENTS_QUICK_MODEL: str = "gpt-5-mini"`
- `TRADINGAGENTS_BACKEND_URL: str = "https://api.openai.com/v1"`
- `TRADINGAGENTS_SELECTED_ANALYSTS: str = "market,social,news,fundamentals"`
- `TRADINGAGENTS_MAX_DEBATE_ROUNDS: int = 1`
- `TRADINGAGENTS_MAX_RISK_DISCUSS_ROUNDS: int = 1`
- `TRADINGAGENTS_OPENAI_REASONING_EFFORT: str | None = None`
- `TRADINGAGENTS_GOOGLE_THINKING_LEVEL: str | None = None`
- `TRADINGAGENTS_ANTHROPIC_EFFORT: str | None = None`

Environment variables for secrets and providers:

- `OPENAI_API_KEY`
- `ALPHA_VANTAGE_API_KEY`
- optional: `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `XAI_API_KEY`, `OPENROUTER_API_KEY`

## Step 3: Build TradingAgents runtime service in backend

Create new service file:

- `backend/app/services/tradingagents_service.py`

Responsibilities:

1. Build and cache a singleton `TradingAgentsGraph`.
2. Construct config by merging:
   - `tradingagents/default_config.py`
   - backend env settings from `backend/app/core/config.py`
3. Run blocking graph call in thread from async routes:
   - `await asyncio.to_thread(graph.propagate, ticker, trade_date)`
4. Return normalized dict for adapters.

Suggested service API:

- `run_single_ticker(ticker: str, trade_date: str | None) -> dict`
- `run_portfolio(holdings: list[dict], trade_date: str | None) -> dict`

## Step 4: Add adapter to preserve FE chat contract

Create adapter file:

- `backend/app/services/tradingagents_adapter.py`

Map TradingAgents output to current schema in `backend/app/schemas/chat_schema.py`:

- `ChatResponse.message`: compose concise human-readable summary from:
  - `signal`
  - `final_trade_decision`
  - `market_report` and `news_report` short excerpts
- `ChatResponse.sources`: list which reports were used
- `ChatResponse.metadata`: include raw rich fields for future FE upgrade

This lets `frontend/src/components/chat/ChatPanel.tsx` continue working unchanged.

## Step 5: Replace `/api/v1/chat` internals

Edit route:

- `backend/app/api/routes/chat.py`

New behavior:

1. Keep conversation persistence via `ConversationService`.
2. Parse ticker(s) from user message.
3. Call TradingAgents adapter/service.
4. Return same `ChatResponse` model.

Important:

- If no ticker is found, return a guided message asking user for ticker.
- Do not fallback to legacy planner if your objective is full replacement.

## Step 6: Replace `/api/v1/portfolio/{id}/analyze`

Edit route:

- `backend/app/api/routes/portfolio.py`

Current code uses legacy `PortfolioAgent` with mock logic.

New behavior:

1. Read actual holdings from DB (`PortfolioService`).
2. Run TradingAgents per holding (possibly with concurrency limit).
3. Build `PortfolioAnalysis` schema:
   - `total_value`
   - `asset_allocation`
   - `diversification_score`
   - `recommendations`

Add strict timeout and failure handling per symbol.

## Step 7: Remove legacy backend agent code (after green tests)

Candidates to remove:

- `backend/app/agents/base_agent.py`
- `backend/app/agents/planner_agent.py`
- `backend/app/agents/market_data_agent.py`
- `backend/app/agents/news_agent.py`
- `backend/app/agents/portfolio_agent.py`
- `backend/app/agents/risk_agent.py`
- `backend/app/agents/query_parser_agent.py`
- `backend/app/agents/explaination_agent.py`

Likely removable dependencies after migration completion:

- `backend/app/engines/indicator_engine.py`
- `backend/app/engines/ranking_engine.py`
- `backend/app/services/market_data_service.py`
- utilities only used by old agent path

Do not remove until imports are fully cleaned and tests are green.

## Step 8: Clean and rebuild test suite

Current tests include stale or unsafe patterns and should be replaced.

Examples to fix/remove:

- `backend/tests/test_agents.py` (interactive loop, not CI-safe)
- `backend/tests/test_services.py` (references missing services)
- `backend/tests/test_db.py` (hard-coded external DB credentials; security risk)

New tests to add:

1. Unit tests for adapter mapping:
   - TradingAgents output -> ChatResponse
2. Unit tests for ticker extraction
3. Route tests for `/api/v1/chat` with mocked TradingAgents service
4. Route tests for `/api/v1/portfolio/{id}/analyze` with mocked service
5. Integration smoke test with real TradingAgents in non-live mode

## Step 9: Security hardening checklist

1. Secret management

- Never commit `.env`.
- Keep `.env` ignored in both root and backend `.gitignore`.
- Rotate any leaked keys immediately.

2. Remove sensitive test artifacts

- Delete hard-coded DB URL and keys from test files.
- Use environment-injected test credentials.

3. Logging safety

- Avoid logging full prompts with user PII or API keys.
- Truncate long model outputs in logs.

4. CORS and auth

- Restrict `ALLOWED_ORIGINS` in production.
- Keep JWT validation path in `backend/app/api/dependencies.py` unchanged.

5. LLM egress control

- Explicitly control provider base URL via env.
- Validate provider and model allowlist before runtime.

## Step 10: FE integration path

Phase 1 (recommended):

- Keep FE unchanged.
- Keep endpoint `/api/v1/chat` unchanged.
- Backend adapter provides old response shape.

Phase 2 (optional):

- Add a new endpoint `/api/v1/chat/rich` that returns full report object.
- Upgrade FE UI to show structured cards:
  - Market
  - Sentiment
  - News
  - Fundamentals
  - Debate highlights
  - Final signal

## Step 11: Deployment and rollback

Deployment order:

1. Merge backend migration with feature flag default off in production.
2. Enable on staging with real API keys.
3. Run smoke tests and latency checks.
4. Enable in production gradually.

Rollback:

- Keep legacy branch/tag.
- Feature flag `TRADINGAGENTS_ENABLED=false` to switch back quickly.

## 6. Suggested Implementation Order (Practical)

1. Add dependencies and config fields.
2. Add TradingAgents runtime service.
3. Add adapter.
4. Switch chat route.
5. Switch portfolio analyze route.
6. Add tests.
7. Remove old agent code.
8. Final cleanup and docs.

## 7. Definition of Done

Migration is complete when:

- FE chat works without FE code changes.
- `/api/v1/chat` and `/api/v1/portfolio/{id}/analyze` both use TradingAgents internally.
- Legacy agent modules are removed.
- CI tests pass.
- No secrets in repo history.
- Staging load/latency is acceptable.

## 8. Known Risks and Mitigations

Risk: runtime latency is higher than old planner path.

- Mitigation: cache graph instance, add timeout, and optionally reduce debate rounds.

Risk: missing ticker in user prompt.

- Mitigation: deterministic ticker parser + ask-back prompt.

Risk: provider/API downtime.

- Mitigation: fail gracefully and return fallback user message.

Risk: cost increase due to multi-agent pipeline.

- Mitigation: use cheaper quick model for non-critical stages and strict token budget.

## 9. Minimal Env Example (backend/.env)

Example values (do not commit real secrets):

```env
APP_NAME=AI Financial Copilot
DEBUG=false
DATABASE_URL=postgresql://user:password@localhost:5432/financial_copilot
REDIS_URL=redis://localhost:6379
SECRET_KEY=change-this-to-a-long-random-secret
ALLOWED_ORIGINS=["http://localhost:5173","http://localhost:3000"]

TRADINGAGENTS_ENABLED=true
TRADINGAGENTS_LLM_PROVIDER=openai
TRADINGAGENTS_DEEP_MODEL=gpt-5.2
TRADINGAGENTS_QUICK_MODEL=gpt-5-mini
TRADINGAGENTS_BACKEND_URL=https://api.openai.com/v1
TRADINGAGENTS_SELECTED_ANALYSTS=market,social,news,fundamentals
TRADINGAGENTS_MAX_DEBATE_ROUNDS=1
TRADINGAGENTS_MAX_RISK_DISCUSS_ROUNDS=1

OPENAI_API_KEY=YOUR-API-KEY
ALPHA_VANTAGE_API_KEY=YOUR-API-KEY
ANTHROPIC_API_KEY=YOUR-API-KEY
GOOGLE_API_KEY=YOUR-API-KEY
XAI_API_KEY=YOUR-API-KEY
OPENROUTER_API_KEY=YOUR-API-KEY
```

---

If you want, the next step is to execute this guide directly in code as a phased migration PR set.
