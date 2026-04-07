"""Format TradingAgents output into user-facing text responses."""

from __future__ import annotations

import json
from typing import Any, Dict, List
import httpx

from openai import OpenAI

from app.core.config import settings
from app.core.logger import logger


def _excerpt(value: Any, max_chars: int = 420) -> str:
    text = str(value or "").strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


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

    last_error: Exception | None = None
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


# --- Template composers ---

def _compose_standard(ticker: str, signal: str, state: Dict[str, Any]) -> str:
    return (
        f"## TradingAgents Analysis for {ticker}\n"
        f"- Signal: **{signal}**\n"
        f"- Final decision: {_excerpt(state.get('final_trade_decision'), 650)}\n\n"
        f"### Snapshot\n"
        f"1. Market: {_excerpt(state.get('market_report'), 320)}\n"
        f"2. Sentiment: {_excerpt(state.get('sentiment_report'), 260)}\n"
        f"3. News: {_excerpt(state.get('news_report'), 260)}\n"
        f"4. Fundamentals: {_excerpt(state.get('fundamentals_report'), 260)}"
    )


def _compose_brief(ticker: str, signal: str, state: Dict[str, Any]) -> str:
    return (
        f"{ticker}: **{signal}**\n"
        f"Decision summary: {_excerpt(state.get('final_trade_decision'), 320)}"
    )


def _compose_detailed(ticker: str, signal: str, state: Dict[str, Any]) -> str:
    return (
        f"## Detailed Analysis for {ticker}\n"
        f"### Final signal\n- **{signal}**\n\n"
        f"### Final decision\n{_excerpt(state.get('final_trade_decision'), 900)}\n\n"
        f"### Investment plan\n"
        f"- Research manager plan: {_excerpt(state.get('investment_plan'), 700)}\n"
        f"- Trader plan: {_excerpt(state.get('trader_investment_plan'), 700)}\n\n"
        f"### Research reports\n"
        f"- Market: {_excerpt(state.get('market_report'), 600)}\n"
        f"- Sentiment: {_excerpt(state.get('sentiment_report'), 500)}\n"
        f"- News: {_excerpt(state.get('news_report'), 500)}\n"
        f"- Fundamentals: {_excerpt(state.get('fundamentals_report'), 500)}"
    )


def _compose_debate(ticker: str, signal: str, state: Dict[str, Any]) -> str:
    invest = state.get("investment_debate_state", {})
    risk = state.get("risk_debate_state", {})
    return (
        f"## Debate View for {ticker}\n"
        f"- Final signal: **{signal}**\n\n"
        f"### Bull thesis\n{_excerpt(invest.get('bull_history'), 500)}\n\n"
        f"### Bear thesis\n{_excerpt(invest.get('bear_history'), 500)}\n\n"
        f"### Debate judgement\n{_excerpt(invest.get('judge_decision'), 550)}\n\n"
        f"### Risk judgement\n{_excerpt(risk.get('judge_decision'), 550)}"
    )


def _compose_risk(ticker: str, signal: str, state: Dict[str, Any]) -> str:
    risk = state.get("risk_debate_state", {})
    return (
        f"## Risk-focused View for {ticker}\n"
        f"- Signal: **{signal}**\n\n"
        f"### Risk committee judgement\n{_excerpt(risk.get('judge_decision'), 700)}\n\n"
        f"### Final action\n{_excerpt(state.get('final_trade_decision'), 600)}"
    )


def _compose_educational(ticker: str, signal: str, state: Dict[str, Any]) -> str:
    return (
        f"## Giai thich don gian cho {ticker}\n"
        f"- Tin hieu hien tai: **{signal}**\n"
        f"- Vi sao: {_excerpt(state.get('final_trade_decision'), 450)}\n\n"
        f"### Dieu can hieu nhanh\n"
        f"- Thi truong: {_excerpt(state.get('market_report'), 240)}\n"
        f"- Nen tang doanh nghiep: {_excerpt(state.get('fundamentals_report'), 240)}\n"
        f"- Day la noi dung tham khao, khong phai loi khuyen dau tu."
    )


def compose_single_ticker(ticker: str, signal: str, state: Dict[str, Any], response_mode: str) -> str:
    composers = {
        "brief": _compose_brief,
        "detailed": _compose_detailed,
        "debate": _compose_debate,
        "risk": _compose_risk,
        "educational": _compose_educational,
    }
    fn = composers.get(response_mode, _compose_standard)
    return fn(ticker, signal, state)


def compose_compare(analyses: List[Dict[str, Any]], failures: List[Dict[str, str]]) -> str:
    if not analyses and not failures:
        return "Khong co du lieu de so sanh."

    lines = ["## So sanh nhieu ma", ""]

    if analyses:
        lines.append("### Ket qua theo ma")
        for item in analyses:
            ticker = str(item.get("ticker") or "UNKNOWN").upper()
            signal = str(item.get("signal") or "HOLD").upper()
            decision = _excerpt(item.get("final_state", {}).get("final_trade_decision"), 260)
            lines.append(f"- {ticker}: **{signal}**")
            lines.append(f"  - Tom tat: {decision}")
        lines.append("")

    if failures:
        lines.append("### Ma phan tich that bai")
        for failure in failures:
            ticker = failure.get("symbol", "UNKNOWN")
            error = _excerpt(failure.get("error", "Unknown error"), 160)
            lines.append(f"- {ticker}: {error}")

    return "\n".join(lines)


# --- LLM output model ---

def _call_output_model(payload: Dict[str, Any]) -> str:
    request_payload = {
        "model": settings.CHAT_OUTPUT_MODEL_NAME,
        "temperature": 0.25,
        "max_tokens": 520,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an output normalizer for a financial assistant. "
                    "Convert structured JSON to final user-facing markdown text. "
                    "Rules: keep the result readable, concise, and factual; no JSON; "
                    "no decorative icons; avoid exposing internal logs or system details."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(payload, ensure_ascii=True),
            },
        ],
    }

    try:
        client = OpenAI(
            api_key=settings.effective_openai_api_key,
            base_url=settings.effective_chat_backend_url,
        )
        response = client.chat.completions.create(
            model=request_payload["model"],
            temperature=request_payload["temperature"],
            max_tokens=request_payload["max_tokens"],
            timeout=settings.CHAT_MODEL_TIMEOUT_SECONDS,
            messages=request_payload["messages"],
        )
        message = response.choices[0].message
    except TypeError as exc:
        if "proxies" not in str(exc).lower():
            raise
        raw = _call_chat_completion_http(request_payload)
        message = (raw.get("choices") or [{}])[0].get("message", {})

    return _extract_message_text(message)


def _looks_like_json(text: str) -> bool:
    s = text.strip()
    return (s.startswith("{") and s.endswith("}")) or (s.startswith("[") and s.endswith("]"))


def _normalize_with_model(payload: Dict[str, Any], fallback_text: str) -> Dict[str, str]:
    if not settings.CHAT_OUTPUT_MODEL_ENABLED or not settings.effective_openai_api_key:
        return {"text": fallback_text, "source": "template_fallback"}

    try:
        text = _call_output_model(payload)
        if not text or _looks_like_json(text):
            return {"text": fallback_text, "source": "template_fallback"}
        return {"text": text, "source": "llm"}
    except Exception as exc:
        logger.warning("Output model normalization failed, using fallback. Error: {}", exc)
        return {"text": fallback_text, "source": "template_fallback"}


def format_single_ticker(
    user_message: str,
    ticker: str,
    signal: str,
    state: Dict[str, Any],
    response_mode: str,
) -> Dict[str, str]:
    """Format single-ticker analysis to text output, using LLM if available."""
    fallback_text = compose_single_ticker(ticker, signal, state, response_mode)

    payload = {
        "user_message": user_message,
        "ticker": ticker,
        "signal": signal,
        "response_mode": response_mode,
        "final_trade_decision": _excerpt(state.get("final_trade_decision"), 720),
        "investment_plan": _excerpt(state.get("investment_plan"), 520),
        "trader_investment_plan": _excerpt(state.get("trader_investment_plan"), 520),
        "reports": {
            "market_report": _excerpt(state.get("market_report"), 360),
            "sentiment_report": _excerpt(state.get("sentiment_report"), 300),
            "news_report": _excerpt(state.get("news_report"), 300),
            "fundamentals_report": _excerpt(state.get("fundamentals_report"), 300),
        },
        "investment_debate": {
            "bull": _excerpt(state.get("investment_debate_state", {}).get("bull_history"), 260),
            "bear": _excerpt(state.get("investment_debate_state", {}).get("bear_history"), 260),
            "judge": _excerpt(state.get("investment_debate_state", {}).get("judge_decision"), 260),
        },
        "risk_debate_judge": _excerpt(state.get("risk_debate_state", {}).get("judge_decision"), 260),
    }

    return _normalize_with_model(payload, fallback_text)


def format_compare(
    user_message: str,
    analyses: List[Dict[str, Any]],
    failures: List[Dict[str, str]],
    response_mode: str,
) -> Dict[str, str]:
    """Format multi-ticker comparison to text output, using LLM if available."""
    fallback_text = compose_compare(analyses, failures)

    compact = [
        {
            "ticker": str(item.get("ticker") or "").upper(),
            "signal": str(item.get("signal") or "HOLD").upper(),
            "decision": _excerpt(item.get("final_state", {}).get("final_trade_decision"), 360),
        }
        for item in analyses
    ]

    payload = {
        "user_message": user_message,
        "response_mode": response_mode,
        "analyses": compact,
        "failures": failures,
    }

    return _normalize_with_model(payload, fallback_text)
