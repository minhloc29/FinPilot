from typing import Annotated, Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

import pandas as pd

from .config import get_config
from .stockstats_utils import StockstatsUtils, _clean_dataframe
from .y_finance import (
    get_YFin_data_online,
    get_stockstats_indicator,
    get_stock_stats_indicators_window as get_stock_stats_indicators_window_yfinance,
    get_fundamentals as get_fundamentals_yfinance,
    get_balance_sheet as get_balance_sheet_yfinance,
    get_cashflow as get_cashflow_yfinance,
    get_income_statement as get_income_statement_yfinance,
    get_insider_transactions as get_insider_transactions_yfinance,
)


def _normalize_ohlcv_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    """Normalize vnstock OHLCV columns to stockstats-compatible schema."""
    rename_map = {
        "time": "Date",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
    available_map = {k: v for k, v in rename_map.items() if k in data.columns}
    normalized = data.rename(columns=available_map).copy()

    if "Date" not in normalized.columns:
        raise ValueError("vnstock OHLCV response has no time/date column")

    return normalized


def _fetch_vnstock_history(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    from vnstock import Quote

    quote = Quote(symbol=symbol.upper(), source="VCI")
    data = quote.history(start=start_date, end=end_date, interval="1D")

    if data is None or data.empty:
        raise ValueError(
            f"No VNStock data found for symbol '{symbol}' between {start_date} and {end_date}"
        )

    return data


def get_stock_data_vnstock(
    symbol: Annotated[str, "ticker symbol of the company"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
):
    """Get OHLCV data from vnstock and fallback to yfinance if unavailable."""
    datetime.strptime(start_date, "%Y-%m-%d")
    datetime.strptime(end_date, "%Y-%m-%d")

    try:
        data = _fetch_vnstock_history(symbol, start_date, end_date)
        data = _normalize_ohlcv_dataframe(data)

        numeric_columns = ["Open", "High", "Low", "Close"]
        for col in numeric_columns:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors="coerce").round(2)

        csv_string = data.to_csv(index=False)

        header = f"# Stock data for {symbol.upper()} from {start_date} to {end_date} (source: vnstock)\n"
        header += f"# Total records: {len(data)}\n"
        header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        return header + csv_string
    except Exception:
        return get_YFin_data_online(symbol, start_date, end_date)


def get_stock_stats_indicators_window_vnstock(
    symbol: Annotated[str, "ticker symbol of the company"],
    indicator: Annotated[str, "technical indicator to get the analysis and report of"],
    curr_date: Annotated[
        str, "The current trading date you are trading on, YYYY-mm-dd"
    ],
    look_back_days: Annotated[int, "how many days to look back"],
) -> str:
    """Calculate technical indicators with vnstock OHLCV and fallback to yfinance."""

    best_ind_params = {
        "close_50_sma": "50 SMA: A medium-term trend indicator.",
        "close_200_sma": "200 SMA: A long-term trend benchmark.",
        "close_10_ema": "10 EMA: A responsive short-term average.",
        "macd": "MACD: Computes momentum via differences of EMAs.",
        "macds": "MACD Signal: An EMA smoothing of the MACD line.",
        "macdh": "MACD Histogram: Shows the gap between MACD and signal.",
        "rsi": "RSI: Measures momentum to flag overbought/oversold conditions.",
        "boll": "Bollinger Middle: A 20 SMA serving as the basis for bands.",
        "boll_ub": "Bollinger Upper Band: Potential overbought zone.",
        "boll_lb": "Bollinger Lower Band: Potential oversold zone.",
        "atr": "ATR: True range-based volatility indicator.",
        "vwma": "VWMA: A moving average weighted by volume.",
        "mfi": "MFI: Momentum indicator using both price and volume.",
    }

    if indicator not in best_ind_params:
        raise ValueError(
            f"Indicator {indicator} is not supported. Please choose from: {list(best_ind_params.keys())}"
        )

    end_date = curr_date
    curr_date_dt = datetime.strptime(curr_date, "%Y-%m-%d")
    before = curr_date_dt - relativedelta(days=look_back_days)

    try:
        indicator_data = _get_stock_stats_bulk_vnstock(symbol, indicator, curr_date)

        current_dt = curr_date_dt
        ind_string = ""

        while current_dt >= before:
            date_str = current_dt.strftime("%Y-%m-%d")
            if date_str in indicator_data:
                indicator_value = indicator_data[date_str]
            else:
                indicator_value = "N/A: Not a trading day (weekend or holiday)"
            ind_string += f"{date_str}: {indicator_value}\n"
            current_dt = current_dt - relativedelta(days=1)

        result_str = (
            f"## {indicator} values from {before.strftime('%Y-%m-%d')} to {end_date}:\n\n"
            + ind_string
            + "\n\n"
            + best_ind_params.get(indicator, "No description available.")
        )

        return result_str

    except Exception:
        return get_stock_stats_indicators_window_yfinance(
            symbol,
            indicator,
            curr_date,
            look_back_days,
        )


def _get_stock_stats_bulk_vnstock(
    symbol: Annotated[str, "ticker symbol of the company"],
    indicator: Annotated[str, "technical indicator to calculate"],
    curr_date: Annotated[str, "current date for reference"],
) -> dict:
    """Bulk indicator computation using vnstock OHLCV data."""
    from stockstats import wrap

    config = get_config()

    today_date = pd.Timestamp.today()
    end_date = today_date.strftime("%Y-%m-%d")
    start_date = (today_date - pd.DateOffset(years=15)).strftime("%Y-%m-%d")

    os.makedirs(config["data_cache_dir"], exist_ok=True)

    data_file = os.path.join(
        config["data_cache_dir"],
        f"{symbol.upper()}-VNStock-data-{start_date}-{end_date}.csv",
    )

    if os.path.exists(data_file):
        data = pd.read_csv(data_file, on_bad_lines="skip")
    else:
        data = _fetch_vnstock_history(symbol, start_date, end_date)
        data.to_csv(data_file, index=False)

    normalized = _normalize_ohlcv_dataframe(data)
    cleaned = _clean_dataframe(normalized)

    df = wrap(cleaned)
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    df[indicator]

    result_dict = {}
    for _, row in df.iterrows():
        date_str = row["Date"]
        value = row[indicator]
        if pd.isna(value):
            result_dict[date_str] = "N/A"
        else:
            result_dict[date_str] = str(value)

    return result_dict


def get_stockstats_indicator_vnstock(
    symbol: Annotated[str, "ticker symbol of the company"],
    indicator: Annotated[str, "technical indicator to get the analysis and report of"],
    curr_date: Annotated[
        str, "The current trading date you are trading on, YYYY-mm-dd"
    ],
) -> str:
    """Single-date indicator lookup, with fallback to yfinance behavior."""
    curr_date_dt = datetime.strptime(curr_date, "%Y-%m-%d")
    curr_date = curr_date_dt.strftime("%Y-%m-%d")

    try:
        indicator_data = _get_stock_stats_bulk_vnstock(symbol, indicator, curr_date)
        return indicator_data.get(curr_date, "N/A: Not a trading day (weekend or holiday)")
    except Exception:
        return str(get_stockstats_indicator(symbol, indicator, curr_date))


def _safe_to_csv(data: pd.DataFrame) -> str:
    if data is None or data.empty:
        raise ValueError("Empty dataframe")
    return data.to_csv(index=False)


def get_fundamentals(
    ticker: Annotated[str, "ticker symbol of the company"],
    curr_date: Annotated[Optional[str], "current date (not used for vnstock)"] = None,
):
    """Get company fundamentals from vnstock and fallback to yfinance."""
    try:
        from vnstock import Company

        company = Company(symbol=ticker.upper(), source="VCI")
        overview = company.overview()

        if overview is None or overview.empty:
            raise ValueError("No vnstock overview data")

        row = overview.iloc[0].to_dict()
        fields = [
            ("Symbol", row.get("symbol")),
            ("Company ID", row.get("id")),
            ("Sector", row.get("icb_name2")),
            ("Industry", row.get("icb_name3")),
            ("Sub-Industry", row.get("icb_name4")),
            ("Issue Share", row.get("issue_share")),
            ("Charter Capital", row.get("charter_capital")),
            ("Company Profile", row.get("company_profile")),
        ]

        lines = [f"{label}: {value}" for label, value in fields if value not in (None, "")]

        if not lines:
            raise ValueError("No vnstock fundamentals fields available")

        header = f"# Company Fundamentals for {ticker.upper()} (source: vnstock)\n"
        header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        return header + "\n".join(lines)
    except Exception:
        return get_fundamentals_yfinance(ticker, curr_date or "")


def _normalize_freq(freq: str) -> str:
    return "quarter" if freq.lower() == "quarterly" else "year"


def get_balance_sheet(
    ticker: Annotated[str, "ticker symbol of the company"],
    freq: Annotated[str, "frequency of data: 'annual' or 'quarterly'"] = "quarterly",
    curr_date: Annotated[Optional[str], "current date (not used for vnstock)"] = None,
):
    """Get balance sheet from vnstock and fallback to yfinance."""
    try:
        from vnstock import Finance

        data = Finance(source="VCI", symbol=ticker.upper(), period=_normalize_freq(freq)).balance_sheet()
        csv_string = _safe_to_csv(data)

        header = f"# Balance Sheet data for {ticker.upper()} ({freq}) (source: vnstock)\n"
        header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        return header + csv_string
    except Exception:
        return get_balance_sheet_yfinance(ticker, freq, curr_date or "")


def get_cashflow(
    ticker: Annotated[str, "ticker symbol of the company"],
    freq: Annotated[str, "frequency of data: 'annual' or 'quarterly'"] = "quarterly",
    curr_date: Annotated[Optional[str], "current date (not used for vnstock)"] = None,
):
    """Get cash flow from vnstock and fallback to yfinance."""
    try:
        from vnstock import Finance

        data = Finance(source="VCI", symbol=ticker.upper(), period=_normalize_freq(freq)).cash_flow()
        csv_string = _safe_to_csv(data)

        header = f"# Cash Flow data for {ticker.upper()} ({freq}) (source: vnstock)\n"
        header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        return header + csv_string
    except Exception:
        return get_cashflow_yfinance(ticker, freq, curr_date or "")


def get_income_statement(
    ticker: Annotated[str, "ticker symbol of the company"],
    freq: Annotated[str, "frequency of data: 'annual' or 'quarterly'"] = "quarterly",
    curr_date: Annotated[Optional[str], "current date (not used for vnstock)"] = None,
):
    """Get income statement from vnstock and fallback to yfinance."""
    try:
        from vnstock import Finance

        data = Finance(source="VCI", symbol=ticker.upper(), period=_normalize_freq(freq)).income_statement()
        csv_string = _safe_to_csv(data)

        header = f"# Income Statement data for {ticker.upper()} ({freq}) (source: vnstock)\n"
        header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        return header + csv_string
    except Exception:
        return get_income_statement_yfinance(ticker, freq, curr_date or "")


def get_insider_transactions(
    ticker: Annotated[str, "ticker symbol of the company"],
):
    """Get insider transactions from vnstock if possible, otherwise yfinance."""
    try:
        from vnstock import Trading

        last_error = None
        for source in ["VCI", "TCBS"]:
            try:
                data = Trading(symbol=ticker.upper(), source=source).insider_deal()
                csv_string = _safe_to_csv(data)

                header = (
                    f"# Insider Transactions data for {ticker.upper()} "
                    f"(source: vnstock/{source})\n"
                )
                header += (
                    f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )
                return header + csv_string
            except Exception as ex:
                last_error = ex
                continue

        if last_error:
            raise last_error
        raise ValueError("No vnstock source supports insider_deal")
    except Exception:
        return get_insider_transactions_yfinance(ticker)
