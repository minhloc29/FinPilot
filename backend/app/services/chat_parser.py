"""Pure AI-driven intent parsing and routing for the financial assistant."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional
import httpx

from openai import OpenAI
from app.core.config import settings
from app.core.logger import logger


def _extract_message_text(message: Any) -> str:
    if isinstance(message, dict):
        content = message.get("content")
        if isinstance(content, str) and content.strip():
            return content.strip()
        reasoning = message.get("reasoning_content")
        if isinstance(reasoning, str) and reasoning.strip():
            return reasoning.strip()
        return ""

    content = getattr(message, "content", None)
    if isinstance(content, str) and content.strip():
        return content.strip()
    reasoning = getattr(message, "reasoning_content", None)
    if isinstance(reasoning, str) and reasoning.strip():
        return reasoning.strip()
    return ""


def _extract_json_payload(text: str) -> Dict[str, Any]:
    if not text:
        return {}

    stripped = text.strip()
    try:
        parsed = json.loads(stripped)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    first = stripped.find("{")
    last = stripped.rfind("}")
    if first >= 0 and last > first:
        try:
            parsed = json.loads(stripped[first : last + 1])
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            return {}
    return {}


def _call_chat_completion_http(payload: Dict[str, Any]) -> Dict[str, Any]:
    api_key = settings.effective_openai_api_key
    if not api_key:
        raise ValueError("Missing API key for HTTP fallback call")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    base = settings.effective_chat_backend_url.rstrip("/")
    candidates = [f"{base}/chat/completions"]
    if base.endswith("/v1"):
        candidates.append(f"{base[:-3]}/chat/completions")
    if settings.MODAS_API_ENDPOINT:
        candidates.append(f"{settings.MODAS_API_ENDPOINT.rstrip('/')}/chat/completions")

    last_error: Optional[Exception] = None
    seen = set()
    for url in candidates:
        if not url or url in seen:
            continue
        seen.add(url)
        try:
            response = httpx.post(
                url,
                headers=headers,
                json=payload,
                timeout=settings.CHAT_MODEL_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as exc:
            last_error = exc
            continue
        except Exception as exc:
            last_error = exc
            continue

    if last_error:
        raise last_error
    raise RuntimeError("HTTP fallback failed with unknown error")


def answer_educational_query(user_message: str) -> str:
    """Directly answer knowledge questions that don't need a ticker."""
    payload = {
        "model": settings.CHAT_OUTPUT_MODEL_NAME,
        "temperature": 0.4,
        "max_tokens": 600,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a financial education assistant. "
                    "Explain financial concepts clearly and concisely in the same language as the user. "
                    "Use markdown formatting. No decorative icons. No generic disclaimers."
                ),
            },
            {"role": "user", "content": user_message},
        ],
    }

    try:
        client = OpenAI(
            api_key=settings.effective_openai_api_key,
            base_url=settings.effective_chat_backend_url,
        )
        response = client.chat.completions.create(
            model=payload["model"],
            temperature=payload["temperature"],
            max_tokens=payload["max_tokens"],
            timeout=settings.CHAT_MODEL_TIMEOUT_SECONDS,
            messages=payload["messages"],
        )
        message = response.choices[0].message
    except TypeError as exc:
        if "proxies" not in str(exc).lower():
            raise
        raw = _call_chat_completion_http(payload)
        message = (raw.get("choices") or [{}])[0].get("message", {})

    return _extract_message_text(message)

def _call_input_model(user_message: str, system_prompt: Optional[str]) -> Dict[str, Any]:
    """Call the LLM to determine intent, tickers, and required analysts."""

    # Prompt định nghĩa quyền hạn và các Agent hiện có
    orchestrator_prompt = f"""
    You are the Senior Orchestrator for FinPilot, a multi-agent financial analysis system.
    Your job is to parse the user's request and decide which specialized agents (analysts) to activate.

    AVAILABLE ANALYSTS:
    - "market": Real-time stock prices, technical indicators (RSI, MACD, MA), and price trends.
    - "social": Market sentiment and social media buzz.
    - "news": Latest news articles, global events, and insider transactions (buy/sell by directors).
    - "fundamentals": Balance sheets, income statements, cash flows, revenue, earnings (P/E, EPS).

    RESPONSE MODES:
    - "standard": Balanced analysis (default).
    - "brief": Quick summary for fast reading.
    - "detailed": In-depth report with all details.
    - "debate": Focus on the conflict between Bull and Bear arguments.
    - "risk": Focus on potential downsides, volatility, and safety.
    - "educational": Explain financial concepts simply.

    CONSTRAINTS:
    - Extract ticker symbols (e.g., AAPL, FPT, VNM). Format: uppercase.
    - If the user asks for news/events, activate ["news"].
    - If the user asks for technical/charts, activate ["market"].
    - If the user asks for financial health/reports, activate ["fundamentals"].
    - If the user asks for a general analysis or 'compare', activate all or relevant ones.
    - If NO TICKER is found but the topic is financial, set tickers: [] and response_mode: "educational".

    System Context: {system_prompt or "None"}

    Return ONLY strict JSON with this schema:
    {{
        "tickers": string[],
        "selected_analysts": string[],
        "response_mode": string,
        "analysis_scope": "single" | "compare" | "general",
        "parameters": {{
            "look_back_days": int,
            "limit": int
        }}
    }}
    """

    payload = {
        "model": settings.CHAT_INPUT_MODEL_NAME,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": orchestrator_prompt},
            {"role": "user", "content": user_message},
        ],
    }

    try:
        client = OpenAI(
            api_key=settings.effective_openai_api_key,
            base_url=settings.effective_chat_backend_url,
        )
        response = client.chat.completions.create(
            model=payload["model"],
            temperature=payload["temperature"],
            response_format=payload["response_format"],
            messages=payload["messages"],
        )
        message = response.choices[0].message
    except TypeError as exc:
        if "proxies" not in str(exc).lower():
            raise
        raw = _call_chat_completion_http(payload)
        message = (raw.get("choices") or [{}])[0].get("message", {})

    text = _extract_message_text(message)
    return _extract_json_payload(text)

def parse_chat_message(
    user_message: str,
    requested_mode: Optional[str] = None,
    system_prompt: Optional[str] = None,
) -> Dict[str, Any]:
    """Identify user intent strictly using the AI input model."""
    try:
        # Nếu không có API key, trả về mặc định an toàn (hoặc báo lỗi)
        if not settings.effective_openai_api_key:
            raise ValueError("OpenAI API Key is missing for Input Model")

        result = _call_input_model(user_message, system_prompt)
        
        # Đảm bảo các field tối thiểu tồn tại
        return {
            "tickers": result.get("tickers", []),
            "selected_analysts": result.get("selected_analysts", ["market", "news", "fundamentals"]),
            "response_mode": result.get("response_mode", requested_mode or "standard"),
            "analysis_scope": result.get("analysis_scope", "general"),
            "should_use_fallback": len(result.get("tickers", [])) == 0,
            "parameters": result.get("parameters", {}),
            "parser_source": "ai_orchestrator"
        }
    except Exception as exc:
        logger.error("AI Orchestrator failed: {}", exc)
        # Fallback tối thiểu khi nổ lỗi AI
        return {
            "tickers": [],
            "selected_analysts": ["market", "news"],
            "response_mode": "standard",
            "analysis_scope": "general",
            "should_use_fallback": True,
            "parser_source": "error_fallback"
        }

def build_no_ticker_payload(user_message: str, response_mode: str) -> Dict[str, Any]:
    """Answer educational queries directly. For other missing-ticker cases, prompt the user."""
    if response_mode == "educational":
        try:
            answer = answer_educational_query(user_message)
            return {
                "message": answer,
                "sources": [],
                "metadata": {"engine": "llm_direct", "reason": "educational_no_ticker"},
            }
        except Exception as exc:
            logger.warning("Educational direct answer failed: %s", exc)

    return {
        "message": (
            "Toi can ma co phieu de phan tich sau. Vi du: 'Phan tich FPT' hoac 'Tin tuc VNM gan day'."
        ),
        "sources": [],
        "metadata": {"engine": "tradingagents", "reason": "no_ticker"},
    }
