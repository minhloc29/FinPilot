"""
Portfolio service for managing portfolios and holdings
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.portfolio import Portfolio, Holding
from app.schemas.portfolio_schema import PortfolioCreate, HoldingBase
from app.core.logger import logger


class PortfolioService:
    """Service for portfolio operations"""

    @staticmethod
    def create_portfolio(db: Session, portfolio_data: PortfolioCreate, user_id: int) -> Portfolio:
        """
        Create a new portfolio with holdings

        Args:
            db: Database session
            portfolio_data: Portfolio creation data
            user_id: ID of the user creating the portfolio

        Returns:
            Created portfolio with holdings
        """
        try:
            # Create portfolio
            portfolio = Portfolio(
                user_id=user_id,
                name=portfolio_data.name,
                description=portfolio_data.description or "",
                total_value=0.0
            )
            db.add(portfolio)
            db.flush()  # Get the portfolio ID

            # Create holdings
            total_value = 0.0
            for holding_data in portfolio_data.holdings:
                current_value = holding_data.shares * \
                    (holding_data.average_cost or 0)
                total_value += current_value

                holding = Holding(
                    portfolio_id=portfolio.id,
                    ticker=holding_data.symbol.upper(),
                    shares=holding_data.shares,
                    average_cost=holding_data.average_cost,
                    current_value=current_value
                )
                db.add(holding)

            # Update portfolio total value
            portfolio.total_value = total_value

            db.commit()
            db.refresh(portfolio)

            logger.info(
                f"Created portfolio {portfolio.id} for user {user_id} with {len(portfolio_data.holdings)} holdings")
            return portfolio

        except Exception as e:
            db.rollback()
            logger.error(f"Error creating portfolio: {str(e)}")
            raise

    @staticmethod
    def get_portfolio(db: Session, portfolio_id: int, user_id: int) -> Optional[Portfolio]:
        """
        Get a portfolio by ID for a specific user

        Args:
            db: Database session
            portfolio_id: Portfolio ID
            user_id: User ID

        Returns:
            Portfolio if found, None otherwise
        """
        return db.query(Portfolio).filter(
            Portfolio.id == portfolio_id,
            Portfolio.user_id == user_id
        ).first()

    @staticmethod
    def get_user_portfolios(db: Session, user_id: int) -> List[Portfolio]:
        """
        Get all portfolios for a user

        Args:
            db: Database session
            user_id: User ID

        Returns:
            List of portfolios
        """
        return db.query(Portfolio).filter(Portfolio.user_id == user_id).all()

    @staticmethod
    def update_portfolio_value(db: Session, portfolio_id: int) -> Portfolio:
        """
        Recalculate and update portfolio total value based on holdings

        Args:
            db: Database session
            portfolio_id: Portfolio ID

        Returns:
            Updated portfolio
        """
        portfolio = db.query(Portfolio).filter(
            Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise ValueError(f"Portfolio {portfolio_id} not found")

        total_value = sum(
            holding.current_value or 0
            for holding in portfolio.holdings
        )

        portfolio.total_value = total_value
        db.commit()
        db.refresh(portfolio)

        return portfolio

    @staticmethod
    def add_holding(
        db: Session,
        portfolio_id: int,
        user_id: int,
        holding_data: HoldingBase
    ) -> Holding:
        """
        Add a new holding to a portfolio

        Args:
            db: Database session
            portfolio_id: Portfolio ID
            user_id: User ID (for authorization)
            holding_data: Holding data

        Returns:
            Created holding
        """
        portfolio = PortfolioService.get_portfolio(db, portfolio_id, user_id)
        if not portfolio:
            raise ValueError(
                f"Portfolio {portfolio_id} not found or unauthorized")

        current_value = holding_data.shares * (holding_data.average_cost or 0)

        holding = Holding(
            portfolio_id=portfolio_id,
            ticker=holding_data.symbol.upper(),
            shares=holding_data.shares,
            average_cost=holding_data.average_cost,
            current_value=current_value
        )

        db.add(holding)
        db.commit()
        db.refresh(holding)

        # Update portfolio total value
        PortfolioService.update_portfolio_value(db, portfolio_id)

        logger.info(
            f"Added holding {holding.ticker} to portfolio {portfolio_id}")
        return holding

    @staticmethod
    def delete_holding(db: Session, holding_id: int, user_id: int) -> bool:
        """
        Delete a holding

        Args:
            db: Database session
            holding_id: Holding ID
            user_id: User ID (for authorization)

        Returns:
            True if deleted, False otherwise
        """
        holding = db.query(Holding).filter(Holding.id == holding_id).first()
        if not holding:
            return False

        # Verify portfolio ownership
        portfolio = PortfolioService.get_portfolio(
            db, holding.portfolio_id, user_id)
        if not portfolio:
            raise ValueError("Unauthorized to delete this holding")

        portfolio_id = holding.portfolio_id
        db.delete(holding)
        db.commit()

        # Update portfolio total value
        PortfolioService.update_portfolio_value(db, portfolio_id)

        logger.info(
            f"Deleted holding {holding_id} from portfolio {portfolio_id}")
        return True
