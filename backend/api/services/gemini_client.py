from __future__ import annotations

import logging
from typing import Generator

from django.conf import settings
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

_client: genai.Client | None = None


def is_configured() -> bool:
    return bool(settings.GEMINI_API_KEY)


def _client_instance() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def embed_text(text: str, task_type: str = 'RETRIEVAL_DOCUMENT') -> list[float]:
    if not is_configured():
        raise RuntimeError('GEMINI_API_KEY is not configured')

    result = _client_instance().models.embed_content(
        model=settings.GEMINI_EMBED_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=settings.GEMINI_EMBED_DIM,
            task_type=task_type,
        ),
    )
    return list(result.embeddings[0].values)


def embed_query(text: str) -> list[float]:
    return embed_text(text, task_type='RETRIEVAL_QUERY')


def stream_chat(
    system_instruction: str,
    user_message: str,
    history: list[dict[str, str]] | None = None,
) -> Generator[str, None, None]:
    if not is_configured():
        raise RuntimeError('GEMINI_API_KEY is not configured')

    contents: list[types.Content] = []
    for item in history or []:
        role = 'user' if item['role'] in ('user', 'narration') else 'model'
        contents.append(types.Content(role=role, parts=[types.Part(text=item['content'])]))
    contents.append(types.Content(role='user', parts=[types.Part(text=user_message)]))

    stream = _client_instance().models.generate_content_stream(
        model=settings.GEMINI_LLM_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=system_instruction),
    )
    for chunk in stream:
        if chunk.text:
            yield chunk.text


def generate_chat(
    system_instruction: str,
    user_message: str,
    history: list[dict[str, str]] | None = None,
) -> str:
    return ''.join(stream_chat(system_instruction, user_message, history))
