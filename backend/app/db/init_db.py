from app.models.base import Base
from app.models.user import User
from app.models.risk_profile import RiskProfile
from app.models.conversation import Conversation, Message
from app.models.portfolio import Portfolio, Holding
from app.db.session import engine
from app.core.logger import logger


def init_db():
   
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")


if __name__ == "__main__":
    init_db()
