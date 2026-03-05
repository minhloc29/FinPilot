"""
Conversation service for managing multi-turn conversations
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.conversation import Conversation, Message
from app.core.logger import logger
import uuid


class ConversationService:
    """
    Service for managing conversations and message history
    """

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
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found")
            return []

        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()

        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

    @staticmethod
    def add_message(
        db: Session,
        conversation_id: str,
        role: str,
        content: str
    ) -> None:
        """
        Add a message to the conversation
        """
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
        conversation_id: Optional[str],
        user_id: Optional[str] = None
    ) -> str:
        """
        Get existing conversation or create a new one if it doesn't exist
        """
        if conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            if conversation:
                return conversation_id

        # Create new conversation if not found or not provided
        return ConversationService.create_conversation(db, user_id)

    @staticmethod
    def update_conversation_title(
        db: Session,
        conversation_id: str,
        title: str
    ) -> None:
        """
        Update conversation title
        """
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        if conversation:
            conversation.title = title
            db.commit()
