from datetime import datetime, timedelta
from typing import List
import re


def parse_date_range(range_str: str) -> tuple:
    now = datetime.utcnow()
    match = re.match(r'(\d+)([dwmy])', range_str.lower())

    if not match:
        return now - timedelta(days=30), now

    value, unit = match.groups()
    value = int(value)

    if unit == 'd':
        start = now - timedelta(days=value)
    elif unit == 'w':
        start = now - timedelta(weeks=value)
    elif unit == 'm':
        start = now - timedelta(days=value * 30)
    elif unit == 'y':
        start = now - timedelta(days=value * 365)
    else:
        start = now - timedelta(days=30)

    return start, now


def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    if old_value == 0:
        return 0.0
    return round(((new_value - old_value) / old_value) * 100, 2)


def remove_reasoning_tags(text: str) -> str:
    if not text:
        return text

    patterns = [
        r'think>.*?</think>',
        r'<think>.*?</think>',
        r'<thinking>.*?</thinking>',
    ]

    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.DOTALL)

    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    return text.strip()
