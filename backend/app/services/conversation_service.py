from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.conversation import Conversation, Message
from app.models.user import User
from app.core.logger import logger
import uuid


class ConversationService:

    ANONYMOUS_EMAIL = "anonymous@finpilot.local"

    @staticmethod
    def _get_or_create_anonymous_user(db: Session) -> User:
        user = db.query(User).filter(User.email == ConversationService.ANONYMOUS_EMAIL).first()
        if user:
            return user

        user = User(
            email=ConversationService.ANONYMOUS_EMAIL,
            hashed_password="anonymous-not-used",
            username="anonymous",
            full_name="Anonymous User",
            is_active=True,
            is_superuser=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def create_conversation(db: Session, user_id: Optional[int] = None) -> int:
        resolved_user_id = user_id
        if resolved_user_id is None:
            resolved_user_id = ConversationService._get_or_create_anonymous_user(db).id

        conversation = Conversation(
            user_id=resolved_user_id,
            title="New Conversation",
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation.id

    @staticmethod
    def get_conversation_history(
        db: Session,
        conversation_id: int,
    ) -> List[Dict[str, str]]:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

        if not conversation:
            logger.warning("Conversation %s not found", conversation_id)
            return []

        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).all()

        return [{"role": msg.role, "content": msg.content} for msg in messages]

    @staticmethod
    def add_message(
        db: Session,
        conversation_id: int,
        role: str,
        content: str,
    ) -> None:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        db.add(message)
        db.commit()

    @staticmethod
    def get_or_create_conversation(
        db: Session,
        conversation_id: Optional[int],
        user_id: Optional[int] = None,
    ) -> int:
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
        title: str,
    ) -> None:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        if conversation:
            conversation.title = title
            db.commit()
