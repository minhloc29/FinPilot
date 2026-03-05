"""
Chat API routes for conversational interface with multi-turn support
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.agents.base_agent import BaseAgent
from app.services.conversation_service import ConversationService
from app.core.config import settings
from app.core.logger import logger
from app.db.session import get_db

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Process user message and return AI response with multi-turn support
    """
    try:
        logger.info(f"Received chat request: {request.message[:50]}...")

        # Get or create conversation
        conversation_id = ConversationService.get_or_create_conversation(
            db=db,
            conversation_id=request.conversation_id,
            user_id=request.user_id
        )

        # Load conversation history
        chat_history = ConversationService.get_conversation_history(
            db=db,
            conversation_id=conversation_id
        )

        # Add user message to history
        chat_history.append({
            "role": "user",
            "content": request.message
        })

        # Initialize base agent with config
        agent = BaseAgent(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            model=settings.DEFAULT_MODEL,
            system_prompt=request.system_prompt or "You are a helpful AI financial assistant. Provide clear, accurate, and actionable financial advice.",
            max_iterations=1
        )

        # Get response from agent
        response = await agent.chat(chat_history)

        # Save user message to database
        ConversationService.add_message(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )

        # Save assistant response to database
        ConversationService.add_message(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=response
        )

        return ChatResponse(
            message=response,
            conversation_id=conversation_id,
            sources=[],
            metadata={
                "model": settings.DEFAULT_MODEL,
                "message_count": len(chat_history) + 1
            }
        )

    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """
    Retrieve conversation history
    """
    try:
        history = ConversationService.get_conversation_history(
            db=db,
            conversation_id=conversation_id
        )

        return {
            "conversation_id": conversation_id,
            "messages": history,
            "message_count": len(history)
        }
    except Exception as e:
        logger.error(f"Error retrieving conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
