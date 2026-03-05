"""
Helper utilities
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any
import re


def parse_date_range(range_str: str) -> tuple:
    """
    Parse date range string (e.g., '1w', '1m', '3m', '1y')
    """
    now = datetime.utcnow()

    pattern = r'(\d+)([dwmy])'
    match = re.match(pattern, range_str.lower())

    if not match:
        return now - timedelta(days=30), now

    value, unit = match.groups()
    value = int(value)

    if unit == 'd':
        start_date = now - timedelta(days=value)
    elif unit == 'w':
        start_date = now - timedelta(weeks=value)
    elif unit == 'm':
        start_date = now - timedelta(days=value * 30)
    elif unit == 'y':
        start_date = now - timedelta(days=value * 365)
    else:
        start_date = now - timedelta(days=30)

    return start_date, now


def format_currency(amount: float) -> str:
    """
    Format amount as currency
    """
    return f"${amount:,.2f}"


def extract_tickers(text: str) -> List[str]:
    """
    Extract stock ticker symbols from text
    """
    # Match patterns like $AAPL or AAPL (1-5 uppercase letters)
    pattern = r'\$?([A-Z]{1,5})\b'
    matches = re.findall(pattern, text)
    return list(set(matches))


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change
    """
    if old_value == 0:
        return 0.0

    change = ((new_value - old_value) / old_value) * 100
    return round(change, 2)


def remove_reasoning_tags(text: str) -> str:
    """
    Remove reasoning/thinking tags from model output.
    Handles patterns like:
    - think> ... </think>
    - <think> ... </think>
    - <thinking> ... </thinking>
    """
    if not text:
        return text

    # Remove thinking blocks with various tag formats
    patterns = [
        r'think>.*?</think>',  # Missing opening bracket
        r'<think>.*?</think>',  # Standard think tags
        r'<thinking>.*?</thinking>',  # Thinking tags
    ]

    cleaned_text = text
    for pattern in patterns:
        cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.DOTALL)

    # Clean up extra whitespace left behind
    cleaned_text = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_text)
    cleaned_text = cleaned_text.strip()

    return cleaned_text
