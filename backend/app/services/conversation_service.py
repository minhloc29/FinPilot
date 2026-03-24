"""
Conversation service for managing multi-turn conversations
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.conversation import Conversation, Message
from app.core.logger import logger
import uuid
import json
import random
class ConversationService:

    CACHE_TTL = 3600
    MAX_CACHE_MESSAGES = 20
    
    @staticmethod
    def _redis_key(conversation_id: int) -> str:
        return f"chat:conversation:{conversation_id}"
    
    @staticmethod
    def create_conversation(db: Session, user_id: Optional[int] = None) -> str:
        """
        Create a new conversation
        """
        conversation = Conversation(
            id=random.randint(1, 10**9),
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
        conversation_id: int
    ) -> List[Dict[str, str]]:
        
        redis_key = ConversationService._redis_key(conversation_id)
        
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found")
            return []

        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        )

        history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]


        return history

    @staticmethod
    def add_message(
        db: Session,
        conversation_id: int,
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
        
    
    @staticmethod
    def get_or_create_conversation(
        db: Session,
        conversation_id: Optional[int],
        user_id: Optional[int] = None
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
        conversation_id: int,
        title: str
    ) -> None:
        
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        if conversation:
            conversation.title = title
            db.commit()
