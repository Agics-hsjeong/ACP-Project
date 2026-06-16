from __future__ import annotations

import logging
import uuid
from typing import Any

from django.db import transaction
from pgvector.django import CosineDistance

from api.models import ArchiveRecord, Character, RagChunk
from api.services import gemini_client, minio_archive

logger = logging.getLogger(__name__)

IMPORTANCE_MAP = {'high': 0.9, 'medium': 0.6, 'low': 0.3}


def chunk_text_for_rag(text: str, max_len: int = 800) -> str:
    cleaned = ' '.join(text.split())
    if len(cleaned) <= max_len:
        return cleaned
    return cleaned[:max_len] + '…'


@transaction.atomic
def archive_and_index(
    *,
    source_type: str,
    source_id: str,
    character_id: str,
    payload: dict[str, Any],
    chunk_text: str,
    importance: float = 0.5,
    metadata: dict[str, Any] | None = None,
) -> ArchiveRecord:
    # source_id 기반 고정 경로 → /ARCHIVE/acp/data/{type}/{char}/{source_id}.json
    object_key = minio_archive.put_archive_json(source_type, character_id, source_id, payload)

    archive = ArchiveRecord.objects.filter(
        source_type=source_type,
        source_id=source_id,
        character_id=character_id,
    ).first()
    if archive:
        if archive.object_key != object_key:
            archive.object_key = object_key
            archive.save(update_fields=['object_key'])
    else:
        archive = ArchiveRecord.objects.create(
            id=uuid.uuid4(),
            object_key=object_key,
            source_type=source_type,
            source_id=source_id,
            character_id=character_id,
            metadata=metadata or {},
        )

    if RagChunk.objects.filter(
        source_type=source_type, source_id=source_id, character_id=character_id
    ).exists():
        return archive

    if gemini_client.is_configured() and chunk_text.strip():
        try:
            vector = gemini_client.embed_text(chunk_text)
            RagChunk.objects.create(
                archive=archive,
                character_id=character_id,
                source_type=source_type,
                source_id=source_id,
                chunk_text=chunk_text,
                embedding=vector,
                importance=importance,
                metadata=metadata or {},
            )
        except Exception as exc:
            logger.warning('RAG indexing failed for %s: %s', object_key, exc)

    return archive


def retrieve_context(character_id: str, query: str, top_k: int = 5) -> list[RagChunk]:
    if not gemini_client.is_configured() or not query.strip():
        return list(
            RagChunk.objects.filter(character_id=character_id).order_by('-importance', '-created_at')[:top_k]
        )

    try:
        query_vec = gemini_client.embed_query(query)
        return list(
            RagChunk.objects.filter(character_id=character_id)
            .order_by(CosineDistance('embedding', query_vec))
            [:top_k]
        )
    except Exception as exc:
        logger.warning('RAG retrieval failed: %s', exc)
        return list(
            RagChunk.objects.filter(character_id=character_id).order_by('-importance', '-created_at')[:top_k]
        )


def build_system_prompt(character: Character, memories: list[RagChunk]) -> str:
    personality = ', '.join(character.personality) if character.personality else ''
    memory_lines = []
    for idx, chunk in enumerate(memories, 1):
        memory_lines.append(f'{idx}. [{chunk.source_type}] {chunk.chunk_text}')

    memory_block = '\n'.join(memory_lines) if memory_lines else '(아직 저장된 기억이 없습니다)'

    return f"""당신은 AI 캐릭터 롤플레이 어시스턴트입니다.
캐릭터 이름: {character.name}
직함: {character.title}
성격: {personality}
설명: {character.description}
대표 대사: {character.quote or ''}

아래는 RAG로 검색된 관련 기억입니다. 반드시 참고하되 캐릭터 말투를 유지하세요.
{memory_block}

규칙:
- 한국어로 자연스럽게 대답합니다.
- 1~3문장, 감정이 드러나는 대사 위주로 답합니다.
- 사용자를 존중하고 세계관을 유지합니다.
"""


def archive_character_bundle(character: Character) -> None:
    payload = {
        'id': character.id,
        'name': character.name,
        'title': character.title,
        'description': character.description,
        'personality': character.personality,
        'world_id': character.world_id,
    }
    text = f'{character.name} {character.title}. {character.description}'
    archive_and_index(
        source_type='character',
        source_id=character.id,
        character_id=character.id,
        payload=payload,
        chunk_text=chunk_text_for_rag(text),
        importance=0.7,
    )


def archive_memory_record(memory) -> None:
    payload = {
        'id': memory.id,
        'title': memory.title,
        'summary': memory.summary,
        'detail': memory.detail,
        'emotion': memory.emotion,
        'importance': memory.importance,
        'tags': memory.tags,
    }
    text = f'{memory.title}. {memory.summary}. {memory.detail}'
    archive_and_index(
        source_type='memory',
        source_id=memory.id,
        character_id=memory.character_id,
        payload=payload,
        chunk_text=chunk_text_for_rag(text),
        importance=IMPORTANCE_MAP.get(memory.importance, 0.5),
        metadata={'emotion': memory.emotion},
    )


def archive_chat_message(message, character_id: str) -> None:
    source_id = str(message.id)
    payload = {
        'id': message.id,
        'role': message.role,
        'content': message.content,
        'timestamp': message.timestamp,
        'emotion_delta': message.emotion_delta,
    }
    text = f'[{message.role}] {message.content}'
    archive_and_index(
        source_type='chat',
        source_id=source_id,
        character_id=character_id,
        payload=payload,
        chunk_text=chunk_text_for_rag(text),
        importance=0.55,
    )
