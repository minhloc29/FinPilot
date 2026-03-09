"""
Conversation service for managing multi-turn conversations
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.db.redis_client import redis_client
from app.models.conversation import Conversation, Message
from app.core.logger import logger
import uuid
import json

class ConversationService:

    CACHE_TTL = 3600
    MAX_CACHE_MESSAGES = 20
    
    @staticmethod
    def _redis_key(conversation_id: str) -> str:
        return f"chat:conversation:{conversation_id}"
    
    @staticmethod
    def create_conversation(db: Session, user_id: Optional[str] = None) -> str:
        """
        Create a new conversation
        """
        conversation = Conversation(
            id=str(uuid.uuid4()),
            user_id=user_id or "anonymous",
            title="New Conversation"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation.id

    @staticmethod
    def get_conversation_history(
        db: Session,
        conversation_id: str
    ) -> List[Dict[str, str]]:
        """
        Get conversation message history in the format required by base_agent
        Returns list of {"role": "user/assistant", "content": "message"}
        """
        
        redis_key = ConversationService._redis_key(conversation_id)
        cached = redis_client.get(redis_key)
        if cached:
            print(f"Detech redis cache: {cached}")
            return json.loads(cached)
        
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found")
            return []

        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()

        history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        redis_client.set(
            redis_key,
            json.dumps(history[-ConversationService.MAX_CACHE_MESSAGES:]),
            ex=ConversationService.CACHE_TTL
        )

        return history

    @staticmethod
    def add_message(
        db: Session,
        conversation_id: str,
        role: str,
        content: str
    ) -> None:
        
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        db.add(message)
        db.commit()
        
        redis_key = ConversationService._redis_key(conversation_id)
        cached = redis_client.get(redis_key)
        
        if cached:
            print(f"Detech redis cache: {cached}")
            history = json.loads(cached)

            history.append({
                "role": role,
                "content": content
            })

            history = history[-ConversationService.MAX_CACHE_MESSAGES:]

            redis_client.set(
                redis_key,
                json.dumps(history),
                ex=ConversationService.CACHE_TTL
            )

    @staticmethod
    def get_or_create_conversation(
        db: Session,
        conversation_id: Optional[str],
        user_id: Optional[str] = None
    ) -> str:
        
        if conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            if conversation:
                return conversation_id

        return ConversationService.create_conversation(db, user_id)

    @staticmethod
    def update_conversation_title(
        db: Session,
        conversation_id: str,
        title: str
    ) -> None:
        
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        if conversation:
            conversation.title = title
            db.commit()
