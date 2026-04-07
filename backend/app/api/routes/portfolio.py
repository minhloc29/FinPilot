import asyncio

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session
from app.schemas.portfolio_schema import (
    PortfolioCreate, PortfolioResponse, PortfolioAnalysis, HoldingBase
)
from app.core.config import settings
from app.core.logger import logger
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.services.portfolio_service import PortfolioService
from app.services.tradingagents_adapter import TradingAgentsAdapter
from app.services.tradingagents_service import TradingAgentsService
from datetime import datetime

router = APIRouter()

trading_agents_service = TradingAgentsService()
trading_agents_adapter = TradingAgentsAdapter()


@router.post("/portfolio", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
async def create_portfolio(
    portfolio: PortfolioCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        portfolio_obj = PortfolioService.create_portfolio(
            db=db,
            portfolio_data=portfolio,
            user_id=current_user.id,
        )

        holdings = [
            HoldingBase(
                symbol=h.ticker,
                shares=h.shares,
                average_cost=h.average_cost,
            )
            for h in portfolio_obj.holdings
        ]

        return PortfolioResponse(
            id=str(portfolio_obj.id),
            user_id=str(current_user.id),
            name=portfolio_obj.name,
            holdings=holdings,
            created_at=portfolio_obj.created_at.isoformat() if hasattr(portfolio_obj, "created_at") else datetime.now().isoformat(),
            total_value=portfolio_obj.total_value,
        )
    except Exception as e:
        logger.error("Error creating portfolio: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/portfolio/{portfolio_id}", response_model=PortfolioResponse)
async def get_portfolio(
    portfolio_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    portfolio = PortfolioService.get_portfolio(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id,
    )

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )

    holdings = [
        HoldingBase(symbol=h.ticker, shares=h.shares, average_cost=h.average_cost)
        for h in portfolio.holdings
    ]

    return PortfolioResponse(
        id=str(portfolio.id),
        user_id=str(current_user.id),
        name=portfolio.name,
        holdings=holdings,
        created_at=portfolio.created_at.isoformat() if hasattr(portfolio, "created_at") else datetime.now().isoformat(),
        total_value=portfolio.total_value,
    )


@router.post("/portfolio/{portfolio_id}/analyze", response_model=PortfolioAnalysis)
async def analyze_portfolio(
    portfolio_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        if not settings.TRADINGAGENTS_ENABLED:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="TradingAgents pipeline is disabled by configuration.",
            )

        portfolio = PortfolioService.get_portfolio(
            db=db,
            portfolio_id=portfolio_id,
            user_id=current_user.id,
        )

        if not portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found",
            )

        holdings_payload = [
            {
                "symbol": h.ticker,
                "shares": h.shares,
                "average_cost": h.average_cost,
                "current_value": h.current_value,
            }
            for h in portfolio.holdings
        ]

        trading_result = await asyncio.to_thread(
            trading_agents_service.run_portfolio,
            holdings_payload,
            None,
        )

        analysis = trading_agents_adapter.build_portfolio_analysis(
            portfolio_id=str(portfolio_id),
            holdings=holdings_payload,
            portfolio_result=trading_result,
        )

        return PortfolioAnalysis(**analysis)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error analyzing portfolio: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/portfolios", response_model=List[PortfolioResponse])
async def list_portfolios(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    portfolios = PortfolioService.get_user_portfolios(
        db=db,
        user_id=current_user.id,
    )

    return [
        PortfolioResponse(
            id=str(p.id),
            user_id=str(current_user.id),
            name=p.name,
            holdings=[
                HoldingBase(symbol=h.ticker, shares=h.shares, average_cost=h.average_cost)
                for h in p.holdings
            ],
            created_at=p.created_at.isoformat() if hasattr(p, "created_at") else datetime.now().isoformat(),
            total_value=p.total_value,
        )
        for p in portfolios
    ]


@router.post("/portfolio/{portfolio_id}/holdings", status_code=status.HTTP_201_CREATED)
async def add_holding(
    portfolio_id: int,
    holding: HoldingBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        holding_obj = PortfolioService.add_holding(
            db=db,
            portfolio_id=portfolio_id,
            user_id=current_user.id,
            holding_data=holding,
        )

        return {
            "id": holding_obj.id,
            "ticker": holding_obj.ticker,
            "shares": holding_obj.shares,
            "average_cost": holding_obj.average_cost,
            "current_value": holding_obj.current_value,
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error("Error adding holding: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/holdings/{holding_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_holding(
    holding_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        success = PortfolioService.delete_holding(
            db=db,
            holding_id=holding_id,
            user_id=current_user.id,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Holding not found",
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error("Error deleting holding: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
