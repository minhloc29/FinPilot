from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.agents.planner_agent import PlannerAgent
from app.services.conversation_service import ConversationService
from app.core.config import settings
from app.core.logger import logger
from app.db.session import get_db

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):

    try:
        logger.info(f"Received chat request: {request.message[:50]}...")
        conversation_id = ConversationService.get_or_create_conversation(
            db=db,
            conversation_id=request.conversation_id,
            user_id=request.user_id
        )

        chat_history = ConversationService.get_conversation_history(
            db=db,
            conversation_id=conversation_id
        )

        chat_history.append({
            "role": "user",
            "content": request.message
        })

        agent = PlannerAgent()

        response = await agent.chat(chat_history)

        ConversationService.add_message(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )

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
