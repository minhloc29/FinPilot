"""vnstock-based news data fetching with yfinance fallback."""

from datetime import datetime
from dateutil.relativedelta import relativedelta

from .yfinance_news import (
    get_news_yfinance,
    get_global_news_yfinance,
)


def _parse_vnstock_public_date(raw_value):
    if raw_value is None:
        return None

    if isinstance(raw_value, (int, float)):
        timestamp = float(raw_value)
        if timestamp > 1e12:
            timestamp = timestamp / 1000.0
        try:
            return datetime.fromtimestamp(timestamp)
        except (ValueError, OSError):
            return None

    if isinstance(raw_value, str):
        for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
            try:
                return datetime.strptime(raw_value, fmt)
            except ValueError:
                continue

    return None


def _fetch_vnstock_news_records(ticker: str) -> list[dict]:
    from vnstock import Company

    company = Company(symbol=ticker.upper(), source="VCI")
    news_df = company.news()

    if news_df is None or news_df.empty:
        return []

    records = []
    for _, row in news_df.iterrows():
        pub_date = _parse_vnstock_public_date(row.get("public_date"))
        records.append(
            {
                "title": row.get("news_title") or row.get("title") or "No title",
                "summary": row.get("news_short_content") or "",
                "publisher": "VNStock",
                "link": row.get("news_source_link") or "",
                "pub_date": pub_date,
            }
        )

    return records


def get_news_vnstock(
    ticker: str,
    start_date: str,
    end_date: str,
) -> str:
    """Retrieve ticker news from vnstock and fallback to yfinance if unavailable."""
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        records = _fetch_vnstock_news_records(ticker)
        if not records:
            return get_news_yfinance(ticker, start_date, end_date)

        news_str = ""
        filtered_count = 0

        for article in records:
            pub_date = article.get("pub_date")
            if pub_date and not (start_dt <= pub_date <= end_dt + relativedelta(days=1)):
                continue

            news_str += f"### {article['title']} (source: {article['publisher']})\n"
            if article["summary"]:
                news_str += f"{article['summary']}\n"
            if article["link"]:
                news_str += f"Link: {article['link']}\n"
            news_str += "\n"
            filtered_count += 1

        if filtered_count == 0:
            return get_news_yfinance(ticker, start_date, end_date)

        return f"## {ticker} News, from {start_date} to {end_date}:\n\n{news_str}"

    except Exception:
        return get_news_yfinance(ticker, start_date, end_date)


def get_global_news_vnstock(
    curr_date: str,
    look_back_days: int = 7,
    limit: int = 10,
) -> str:
    """Use yfinance global news endpoint for broad market coverage."""
    return get_global_news_yfinance(curr_date, look_back_days, limit)
