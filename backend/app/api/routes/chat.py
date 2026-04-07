import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.conversation_service import ConversationService
from app.core.config import settings
from app.core.logger import logger
from app.db.session import get_db
from app.services.chat_parser import parse_chat_message, build_no_ticker_payload
from app.services.tradingagents_adapter import TradingAgentsAdapter
from app.services.tradingagents_service import TradingAgentsService

router = APIRouter()

trading_agents_service = TradingAgentsService()
trading_agents_adapter = TradingAgentsAdapter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        if not settings.TRADINGAGENTS_ENABLED:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="TradingAgents pipeline is disabled by configuration.",
            )

        logger.info("Received AI-Orchestrated chat request: {}...", request.message[:50])

        # Keep chat usable in local Swagger testing even when DB is unavailable.
        conversation_id = request.conversation_id or 0
        persist_messages = False
        try:
            conversation_id = ConversationService.get_or_create_conversation(
                db=db,
                conversation_id=request.conversation_id,
                user_id=request.user_id,
            )
            persist_messages = True
        except Exception as exc:
            logger.warning("Conversation persistence disabled for this request: {}", exc)

        # 1. AI Orchestrator phân tích ý định và chọn Agent
        parse_result = await asyncio.to_thread(
            parse_chat_message,
            request.message,
            request.response_mode,
            request.system_prompt,
        )

        tickers = parse_result["tickers"]
        response_mode = parse_result["response_mode"]
        selected_analysts = parse_result["selected_analysts"]
        
        parser_metadata = {
            "source": parse_result["parser_source"],
            "analysis_scope": parse_result["analysis_scope"],
            "analysts_selected": selected_analysts,
        }

        # 2. Xử lý logic dựa trên phân tích của AI
        if parse_result["should_use_fallback"]:
            fallback = build_no_ticker_payload(request.message, response_mode)
            response_message = fallback["message"]
            response_sources = fallback["sources"]
            response_metadata = {**fallback["metadata"], "input_parser": parser_metadata}

        elif parse_result["analysis_scope"] == "compare" and len(tickers) >= 2:
            comparison_result = await asyncio.to_thread(
                trading_agents_service.run_many_tickers,
                tickers,
                None,
                selected_analysts, # Chỉ chạy các Agent mà AI chọn
            )
            mapped = trading_agents_adapter.build_compare_chat_payload(
                request.message,
                comparison_result,
                response_mode,
            )
            response_message = mapped["message"]
            response_sources = mapped["sources"]
            response_metadata = {**mapped["metadata"], "input_parser": parser_metadata}

        else:
            # Single ticker hoặc default
            ticker = tickers[0] if tickers else "FPT"
            analysis = await asyncio.to_thread(
                trading_agents_service.run_single_ticker,
                ticker,
                None,
                selected_analysts, # Chỉ chạy các Agent mà AI chọn
            )
            mapped = trading_agents_adapter.build_chat_payload(
                request.message,
                ticker,
                analysis,
                response_mode,
            )
            response_message = mapped["message"]
            response_sources = mapped["sources"]
            response_metadata = {**mapped["metadata"], "input_parser": parser_metadata}

        # 3. Lưu lịch sử
        if persist_messages:
            try:
                ConversationService.add_message(db, conversation_id, "user", request.message)
                ConversationService.add_message(db, conversation_id, "assistant", response_message)
            except Exception as exc:
                logger.warning("Failed to persist chat messages: {}", exc)

        return ChatResponse(
            message=response_message,
            conversation_id=conversation_id,
            sources=response_sources,
            metadata=response_metadata,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in Orchestrated Chat: {}", str(e))
        raise HTTPException(status_code=500, detail="Internal analysis error")
