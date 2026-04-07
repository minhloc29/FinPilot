"""Utilities for extracting ticker symbols from user text."""

from __future__ import annotations

import re
from typing import List, Optional

_TICKER_PATTERN = re.compile(r"\b[A-Za-z]{1,5}(?:\.[A-Za-z]{1,4})?\b")

# Filter common words that are often captured by regex but are not tickers.
_STOPWORDS = {
    "AN",
    "AND",
    "ARE",
    "BAN",
    "CO",
    "BUY",
    "CAN",
    "CHO",
    "DANH",
    "DO",
    "DUA",
    "GIA",
    "GI",
    "HAY",
    "HOLD",
    "HOI",
    "KHONG",
    "LA",
    "LAI",
    "MA",
    "MINH",
    "MUA",
    "MUON",
    "NAY",
    "NAO",
    "PHAN",
    "SAU",
    "SELL",
    "STOCK",
    "TICKER",
    "THE",
    "THI",
    "TICH",
    "TOI",
    "TRUONG",
    "VA",
    "VE",
    "VOI",
    "WHAT",
    "XEM",
}


def extract_ticker_candidates(text: str) -> List[str]:
    """Extract likely ticker symbols from free-form text."""
    if not text:
        return []

    seen = set()
    candidates: List[str] = []

    for token in _TICKER_PATTERN.findall(text):
        normalized = token.upper()
        stripped = normalized.replace(".", "")

        if normalized in _STOPWORDS:
            continue

        if len(stripped) < 2 or len(stripped) > 5:
            continue

        if normalized not in seen:
            seen.add(normalized)
            candidates.append(normalized)

    return candidates


def extract_primary_ticker(text: str) -> Optional[str]:
    """Get the first ticker candidate if available."""
    candidates = extract_ticker_candidates(text)
    return candidates[0] if candidates else None


def extract_unique_tickers(text: str) -> List[str]:
    """Extract unique tickers preserving order."""
    return extract_ticker_candidates(text)
