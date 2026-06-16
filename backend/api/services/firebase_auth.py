from __future__ import annotations

import json
import logging

from django.conf import settings

logger = logging.getLogger(__name__)

_app = None


def is_configured() -> bool:
    """프로젝트 ID만 있어도 공개키 검증 모드로 동작 가능."""
    return bool(settings.FIREBASE_PROJECT_ID)


def _has_admin_credentials() -> bool:
    if settings.FIREBASE_SERVICE_ACCOUNT_JSON:
        return True
    path = settings.FIREBASE_SERVICE_ACCOUNT_PATH
    return bool(path and path.exists())


def _load_credentials():
    from firebase_admin import credentials

    if settings.FIREBASE_SERVICE_ACCOUNT_JSON:
        data = json.loads(settings.FIREBASE_SERVICE_ACCOUNT_JSON)
        return credentials.Certificate(data)
    path = settings.FIREBASE_SERVICE_ACCOUNT_PATH
    if path and path.exists():
        return credentials.Certificate(str(path))
    raise RuntimeError('Firebase service account is not configured')


def _get_admin_app():
    global _app
    if _app is not None:
        return _app
    import firebase_admin

    if not firebase_admin._apps:
        cred = _load_credentials()
        _app = firebase_admin.initialize_app(
            cred,
            {'projectId': settings.FIREBASE_PROJECT_ID},
        )
    else:
        _app = firebase_admin.get_app()
    return _app


def _normalize_claims(decoded: dict) -> dict:
    uid = decoded.get('uid') or decoded.get('sub') or decoded.get('user_id')
    if not uid:
        raise ValueError('Token missing user id')
    return {
        'uid': uid,
        'email': decoded.get('email', ''),
        'name': decoded.get('name', ''),
        'picture': decoded.get('picture', ''),
    }


def _verify_with_admin(id_token: str) -> dict:
    from firebase_admin import auth

    _get_admin_app()
    decoded = auth.verify_id_token(id_token, check_revoked=True)
    return _normalize_claims(decoded)


def _verify_with_public_keys(id_token: str) -> dict:
    """서비스 계정 없이 Google 공개키로 Firebase ID 토큰 검증."""
    from google.auth.transport import requests as google_requests
    from google.oauth2 import id_token as google_id_token

    req = google_requests.Request()
    decoded = google_id_token.verify_firebase_token(
        id_token,
        req,
        audience=settings.FIREBASE_PROJECT_ID,
    )
    return _normalize_claims(decoded)


def verify_id_token(id_token: str) -> dict:
    if _has_admin_credentials():
        try:
            return _verify_with_admin(id_token)
        except Exception as exc:
            logger.warning('Admin SDK verify failed, trying public keys: %s', exc)

    if not settings.FIREBASE_PROJECT_ID:
        raise RuntimeError('FIREBASE_PROJECT_ID is not configured')

    return _verify_with_public_keys(id_token)
