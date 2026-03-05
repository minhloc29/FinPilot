"""
Script to seed initial data into the database
"""
from app.core.security import get_password_hash
from app.models.portfolio import Portfolio, Holding
from app.models.user import User
from app.db.session import SessionLocal
import sys
sys.path.append('../backend')


def seed_data():
    """Seed initial data"""
    db = SessionLocal()

    try:
        # Create demo user
        demo_user = User(
            email="demo@example.com",
            hashed_password=get_password_hash("demo123"),
            full_name="Demo User",
            is_active=True
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

        print(f"Created demo user: {demo_user.email}")

        # Create demo portfolio
        portfolio = Portfolio(
            user_id=demo_user.id,
            name="My Portfolio",
            description="Demo portfolio",
            total_value=7000.0
        )
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)

        print(f"Created portfolio: {portfolio.name}")

        # Add holdings
        holdings_data = [
            {"symbol": "AAPL", "shares": 10, "average_cost": 150.0},
            {"symbol": "GOOGL", "shares": 5, "average_cost": 140.0},
            {"symbol": "MSFT", "shares": 15, "average_cost": 280.0}
        ]

        for holding_data in holdings_data:
            holding = Holding(
                portfolio_id=portfolio.id,
                **holding_data
            )
            db.add(holding)
            print(f"Added holding: {holding_data['symbol']}")

        db.commit()
        print("\nData seeded successfully!")

    except Exception as e:
        print(f"Error seeding data: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
