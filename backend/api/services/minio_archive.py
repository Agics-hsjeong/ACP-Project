from __future__ import annotations

import io
import json
import logging
import uuid
from pathlib import Path
from typing import Any

from django.conf import settings
from minio import Minio
from minio.error import S3Error

logger = logging.getLogger(__name__)

_client: Minio | None = None
_bucket_ready = False


def _client_instance() -> Minio:
    global _client
    if _client is None:
        _client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
    return _client


def ensure_bucket() -> None:
    global _bucket_ready
    if _bucket_ready:
        return
    ensure_archive_layout()
    client = _client_instance()
    bucket = settings.MINIO_BUCKET
    try:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
    except S3Error as exc:
        logger.warning('MinIO bucket setup failed: %s', exc)
        return
    _bucket_ready = True


def ensure_archive_layout() -> None:
    """DoRaGi-LM 과 동일: /ARCHIVE/{project}/minio|data|models 디렉터리 보장."""
    base = Path(settings.ARCHIVE_BASE)
    data_root = Path(settings.ARCHIVE_ROOT)
    models_root = Path(settings.ARCHIVE_MODELS_ROOT)
    for path in (base, data_root, models_root, models_root / 'hub'):
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            logger.warning('Archive layout mkdir failed (%s): %s', path, exc)


def archive_relative_path(source_type: str, character_id: str, record_id: str, ext: str = 'json') -> str:
    char_part = character_id or '_global'
    return f'{source_type}/{char_part}/{record_id}.{ext}'


def archive_object_key(source_type: str, character_id: str, record_id: str, ext: str = 'json') -> str:
    prefix = settings.ARCHIVE_PREFIX
    return f'{prefix}/{archive_relative_path(source_type, character_id, record_id, ext)}'


def archive_local_path(source_type: str, character_id: str, record_id: str, ext: str = 'json') -> Path:
    root = Path(settings.ARCHIVE_ROOT)
    return root / archive_relative_path(source_type, character_id, record_id, ext)


def _write_local_archive(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def put_archive_json(
    source_type: str,
    character_id: str,
    record_id: str,
    payload: dict[str, Any],
) -> str:
    key = archive_object_key(source_type, character_id, record_id)
    data = json.dumps(payload, ensure_ascii=False, default=str).encode('utf-8')

    local_path = archive_local_path(source_type, character_id, record_id)
    try:
        _write_local_archive(local_path, data)
    except OSError as exc:
        logger.warning('Local archive write failed (%s): %s', local_path, exc)

    ensure_bucket()
    try:
        _client_instance().put_object(
            settings.MINIO_BUCKET,
            key,
            io.BytesIO(data),
            length=len(data),
            content_type='application/json',
        )
    except S3Error as exc:
        logger.warning('MinIO archive write failed (%s): %s', key, exc)

    return key


def get_archive_json(object_key: str) -> dict[str, Any]:
    root = Path(settings.ARCHIVE_ROOT)
    prefix = settings.ARCHIVE_PREFIX
    # 신규: data/chat/...  /  구버전: ARCHIVE/chat/...
    for pfx in (prefix, 'ARCHIVE'):
        if object_key.startswith(f'{pfx}/'):
            local_path = root / object_key[len(pfx) + 1 :]
            if local_path.is_file():
                return json.loads(local_path.read_text(encoding='utf-8'))
            # 구버전 flat 경로 (/ARCHIVE/chat/...)
            legacy = Path(settings.ARCHIVE_BASE).parent / object_key
            if legacy.is_file():
                return json.loads(legacy.read_text(encoding='utf-8'))

    ensure_bucket()
    response = _client_instance().get_object(settings.MINIO_BUCKET, object_key)
    try:
        return json.loads(response.read().decode('utf-8'))
    finally:
        response.close()
        response.release_conn()


def new_record_id() -> str:
    return str(uuid.uuid4())
