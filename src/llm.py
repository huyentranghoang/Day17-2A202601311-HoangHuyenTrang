"""Thin Gemini wrapper for the demo UI chat reply.

This is the ONLY place the lab calls a generative LLM. Benchmark scoring never
uses an LLM (see LAB.md): retrieval evidence is graded deterministically. Here
Gemini only turns retrieved memory context into a grounded assistant reply so
the mini-product feels real.

Default model: gemini-flash-lite-latest (override with GEMINI_MODEL).
"""

from __future__ import annotations

from typing import Any

from .config import settings

SYSTEM_INSTRUCTION = (
    "You are Memora, a concise memory agent for VinUni Lab 17.\n"
    "Rules:\n"
    "1) Answer ONLY from the retrieved memory context. Never invent facts.\n"
    "2) Reply in the user's language (Vietnamese or English).\n"
    "3) Keep answers SHORT: 1-3 sentences, or a tiny bullet list (max 4 lines).\n"
    "4) Do NOT repeat the user's question. Do NOT dump the raw memory context.\n"
    "5) Do NOT paste <LONG_TERM>/<EPISODIC>/<SEMANTIC> blocks or full transcripts.\n"
    "6) Mention at most 1-3 concrete markers/ids (e.g. ORCHID-27, ASYNC-FIX-20).\n"
    "7) If context is insufficient, say so in one short sentence."
)


def gemini_available() -> bool:
    """True when a key is configured. UI uses this to show status."""
    return bool(settings.gemini_api_key)


def _to_contents(history: list[dict[str, str]]) -> list[dict[str, Any]]:
    """Map chat history to google-genai `contents` turns.

    Roles: user -> "user", everything else (assistant/model) -> "model".
    """
    contents: list[dict[str, Any]] = []
    for msg in history:
        role = "user" if msg.get("role") == "user" else "model"
        text = msg.get("content", "")
        if not text:
            continue
        contents.append({"role": role, "parts": [{"text": text}]})
    return contents


def generate_reply(
    memory_context: str,
    history: list[dict[str, str]],
    user_message: str,
    *,
    model: str | None = None,
) -> str:
    """Generate a grounded assistant reply with Gemini.

    Raises RuntimeError if no key, and lets SDK/network errors bubble up so the
    UI can surface them. `history` should include the latest user turn or not —
    `user_message` is appended as the final user turn regardless.
    """
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Copy .env.example to .env and add a "
            "Google AI Studio key to enable chat replies."
        )

    # Lazy import so the rest of the package works without google-genai installed
    # (tests, report generation, retrieval benchmarks never need it).
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.gemini_api_key)
    primary = model or settings.gemini_model
    # Prefer configured model; fall back if Google retired an alias for new keys.
    model_candidates = [
        primary,
        "gemini-flash-lite-latest",
        "gemini-flash-latest",
        "gemini-3.1-flash-lite",
    ]
    seen: set[str] = set()
    models = [m for m in model_candidates if m and not (m in seen or seen.add(m))]

    # Keep only recent turns so the model does not echo the whole chat.
    recent = history[-6:] if history else []
    clipped = (memory_context or "").strip()
    if len(clipped) > 3500:
        clipped = clipped[:3500] + "\n[...trimmed...]"

    grounding = (
        "Use the memory notes below as private grounding. "
        "Write a short direct answer to the user. "
        "Never reprint the notes or the question.\n\n"
        f"<memory_notes>\n{clipped or '(empty)'}\n</memory_notes>\n\n"
        f"<user_question>\n{user_message}\n</user_question>"
    )

    contents = _to_contents(recent)
    contents.append({"role": "user", "parts": [{"text": grounding}]})
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.2,
        max_output_tokens=220,
    )

    last_error: Exception | None = None
    for model_name in models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
            )
            text = (getattr(response, "text", "") or "").strip()
            return _clean_reply(text)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            continue
    raise RuntimeError(f"Gemini reply failed: {last_error}")


def _clean_reply(text: str) -> str:
    """Drop accidental dumps of context tags / echoed questions."""
    if not text:
        return "Xin lỗi, mình chưa lấy được câu trả lời ngắn từ memory."
    banned_starts = (
        "retrieved memory",
        "<long_term>",
        "<short_term>",
        "<episodic>",
        "<semantic>",
        "user message:",
        "memory context",
    )
    lines = []
    for line in text.splitlines():
        low = line.strip().casefold()
        if any(low.startswith(b) for b in banned_starts):
            continue
        lines.append(line)
    cleaned = "\n".join(lines).strip()
    return cleaned or text.strip()
