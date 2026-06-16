import json
import logging
from datetime import datetime

from django.contrib.auth import authenticate, get_user_model
from django.http import StreamingHttpResponse
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    ArchiveRecord,
    Character,
    CharacterScenario,
    ChatMessage,
    ChatSession,
    EmotionAxis,
    LandingContent,
    Memory,
    RagChunk,
    RelationshipEdge,
    RelationshipEvent,
    World,
)
from .serializers import (
    ArchiveRecordSerializer,
    CharacterListSerializer,
    CharacterSerializer,
    StudioCharacterSerializer,
    CharacterScenarioSerializer,
    ChatMessageSerializer,
    ChatSendSerializer,
    EmotionAxisSerializer,
    FirebaseLoginSerializer,
    LandingContentSerializer,
    MemoryCreateSerializer,
    MemorySerializer,
    RagSearchSerializer,
    RelationshipEdgeSerializer,
    RelationshipEventSerializer,
    WorldSerializer,
)
from .services import firebase_auth as firebase_service
from .services import gemini_client, rag
from .services import minio_archive

User = get_user_model()
logger = logging.getLogger(__name__)

REPLY_TEMPLATES = [
    '…그렇게 말해주니, 조금은 마음이 놓이네요.',
    '흥미로운 이야기예요. 더 들려주실 수 있나요?',
    '오늘 밤하늘처럼, 당신의 말도 참 고요하고 따뜻하네요.',
]


def _fallback_reply() -> str:
    import random

    return random.choice(REPLY_TEMPLATES)


def _save_user_message(session: ChatSession, content: str) -> ChatMessage | None:
    now = datetime.now().strftime('%p %I:%M')
    if content.startswith('*') and content.endswith('*'):
        return ChatMessage.objects.create(
            session=session,
            role='narration',
            content=content[1:-1],
        )
    return ChatMessage.objects.create(
        session=session,
        role='user',
        content=content,
        timestamp=now,
    )


def _recent_history(session: ChatSession, limit: int = 8) -> list[dict[str, str]]:
    msgs = session.messages.order_by('-created_at')[:limit]
    history = []
    for msg in reversed(list(msgs)):
        if msg.role in ('user', 'character', 'narration'):
            history.append({'role': msg.role, 'content': msg.content})
    return history


def _generate_reply(character: Character, session: ChatSession, user_content: str) -> str:
    memories = rag.retrieve_context(character.id, user_content)
    system_prompt = rag.build_system_prompt(character, memories)
    history = _recent_history(session)

    if gemini_client.is_configured():
        try:
            return gemini_client.generate_chat(system_prompt, user_content, history)
        except Exception as exc:
            logger.warning('Gemini generate failed: %s', exc)
    return _fallback_reply()


class WorldViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = World.objects.all()
    serializer_class = WorldSerializer
    lookup_field = 'id'


class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Character.objects.select_related('world').all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return CharacterListSerializer
        return CharacterSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(description__icontains=q)
        world = self.request.query_params.get('world')
        if world:
            qs = qs.filter(world_id=world)
        return qs.distinct()


class MemoryViewSet(viewsets.ModelViewSet):
    queryset = Memory.objects.select_related('character').all()
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'create':
            return MemoryCreateSerializer
        return MemorySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        character_id = self.request.query_params.get('character')
        if character_id:
            qs = qs.filter(character_id=character_id)
        importance = self.request.query_params.get('importance')
        if importance:
            qs = qs.filter(importance=importance)
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(summary__icontains=q)
        return qs

    def perform_create(self, serializer):
        memory = serializer.save()
        rag.archive_memory_record(memory)


class ArchiveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArchiveRecord.objects.all()
    serializer_class = ArchiveRecordSerializer
    lookup_field = 'id'

    def get_queryset(self):
        qs = super().get_queryset()
        character_id = self.request.query_params.get('character')
        source_type = self.request.query_params.get('source_type')
        if character_id:
            qs = qs.filter(character_id=character_id)
        if source_type:
            qs = qs.filter(source_type=source_type)
        return qs


class RagSearchView(APIView):
    def post(self, request):
        serializer = RagSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        character_id = serializer.validated_data['character_id']
        query = serializer.validated_data['query']
        top_k = serializer.validated_data.get('top_k', 5)

        chunks = rag.retrieve_context(character_id, query, top_k=top_k)
        return Response({
            'character_id': character_id,
            'query': query,
            'results': [
                {
                    'id': c.id,
                    'source_type': c.source_type,
                    'source_id': c.source_id,
                    'chunk_text': c.chunk_text,
                    'importance': c.importance,
                    'archive_key': c.archive.object_key if c.archive_id else None,
                }
                for c in chunks
            ],
        })


class ChatSessionsListView(APIView):
    """최근 대화 세션 목록 (사이드바·홈용)."""

    def get(self, request):
        sessions = (
            ChatSession.objects.select_related('character')
            .prefetch_related('messages')
            .order_by('-updated_at')[:20]
        )
        results = []
        for session in sessions:
            last = session.messages.order_by('-created_at').first()
            preview = ''
            if last:
                preview = last.content[:80] + ('…' if len(last.content) > 80 else '')
            results.append({
                'id': session.character_id,
                'name': session.character.name,
                'avatar': session.character.avatar,
                'preview': preview or '대화를 시작해 보세요',
                'time': session.updated_at.isoformat(),
            })
        return Response(results)


class EmotionView(APIView):
    def get(self, request, character_id):
        try:
            character = Character.objects.get(pk=character_id)
        except Character.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        axes = EmotionAxis.objects.filter(character=character)
        data = EmotionAxisSerializer(axes, many=True).data
        affection = next((a['value'] for a in data if a['key'] == 'affection'), 0)
        trust = next((a['value'] for a in data if a['key'] == 'trust'), 0)
        return Response({
            'character_id': character_id,
            'axes': data,
            'intimacy': round((affection + trust) / 2),
        })


class ChatViewSet(viewsets.ViewSet):

    def _get_or_create_session(self, character_id: str) -> ChatSession:
        character = Character.objects.get(pk=character_id)
        session, _ = ChatSession.objects.get_or_create(character=character)
        return session

    def list(self, request, character_id=None):
        try:
            session = self._get_or_create_session(character_id)
        except Character.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        messages = session.messages.all()
        return Response(ChatMessageSerializer(messages, many=True).data)

    def create(self, request, character_id=None):
        serializer = ChatSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data['content'].strip()
        if not content:
            return Response({'detail': 'Empty message'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            character = Character.objects.get(pk=character_id)
            session = self._get_or_create_session(character_id)
        except Character.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        user_msg = _save_user_message(session, content)
        if user_msg:
            rag.archive_chat_message(user_msg, character.id)

        now = datetime.now().strftime('%p %I:%M')
        reply_text = _generate_reply(character, session, content)
        char_msg = ChatMessage.objects.create(
            session=session,
            role='character',
            content=reply_text,
            timestamp=now,
            emotion_delta='애정 +2',
        )
        rag.archive_chat_message(char_msg, character.id)

        return Response({
            'messages': ChatMessageSerializer([user_msg, char_msg], many=True).data,
        })

    def stream(self, request, character_id=None):
        serializer = ChatSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data['content'].strip()
        if not content:
            return Response({'detail': 'Empty message'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            character = Character.objects.get(pk=character_id)
            session = self._get_or_create_session(character_id)
        except Character.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        user_msg = _save_user_message(session, content)
        if user_msg:
            rag.archive_chat_message(user_msg, character.id)

        memories = rag.retrieve_context(character.id, content)
        system_prompt = rag.build_system_prompt(character, memories)
        history = _recent_history(session)
        now = datetime.now().strftime('%p %I:%M')

        def event_stream():
            yield f'data: {json.dumps({"type": "start"})}\n\n'
            partial = ''
            full_reply = ''

            if gemini_client.is_configured():
                try:
                    for token in gemini_client.stream_chat(system_prompt, content, history):
                        partial += token
                        full_reply = partial
                        yield f'data: {json.dumps({"type": "token", "content": token, "partial": partial})}\n\n'
                except Exception as exc:
                    logger.warning('Gemini stream failed: %s', exc)
                    full_reply = ''

            if not full_reply:
                full_reply = _fallback_reply()
                partial = ''
                for ch in full_reply:
                    partial += ch
                    yield f'data: {json.dumps({"type": "token", "content": ch, "partial": partial})}\n\n'

            msg = ChatMessage.objects.create(
                session=session,
                role='character',
                content=full_reply,
                timestamp=now,
                emotion_delta='애정 +2',
            )
            rag.archive_chat_message(msg, character.id)
            yield f'data: {json.dumps({"type": "done", "message": ChatMessageSerializer(msg).data})}\n\n'

        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email', 'user@acp.local')
        password = request.data.get('password', '')
        provider = request.data.get('provider')

        if provider:
            user, _ = User.objects.get_or_create(
                username=provider,
                defaults={'email': f'{provider}@acp.local'},
            )
        else:
            user, created = User.objects.get_or_create(
                username=email,
                defaults={'email': email},
            )
            if created:
                user.set_password(password or 'acp1234')
                user.save()
            elif password:
                auth_user = authenticate(username=email, password=password)
                if auth_user:
                    user = auth_user

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {'email': user.email or email, 'name': user.username},
        })


class FirebaseLoginView(APIView):
    """Firebase Google 로그인 — 프론트에서 받은 ID 토큰 검증 후 DRF 토큰 발급."""

    def post(self, request):
        if not firebase_service.is_configured():
            return Response(
                {'detail': 'Firebase is not configured on the server'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        serializer = FirebaseLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_token = serializer.validated_data['id_token']

        try:
            decoded = firebase_service.verify_id_token(id_token)
        except Exception as exc:
            logger.warning('Firebase token verification failed: %s', exc)
            return Response(
                {'detail': f'Invalid Firebase token: {exc}'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        uid = decoded['uid']
        email = decoded.get('email') or f'{uid}@firebase.local'
        name = decoded.get('name') or email.split('@')[0] or 'User'
        picture = decoded.get('picture', '')

        user, created = User.objects.get_or_create(
            username=f'firebase_{uid}',
            defaults={'email': email, 'first_name': name[:150]},
        )
        if not created:
            updated = False
            if email and user.email != email:
                user.email = email
                updated = True
            if name and user.first_name != name[:150]:
                user.first_name = name[:150]
                updated = True
            if updated:
                user.save(update_fields=['email', 'first_name'])

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'email': user.email,
                'name': user.first_name or user.username,
                'picture': picture,
                'provider': 'google',
            },
        })


class MeView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'user': None})
        return Response({
            'user': {
                'email': request.user.email,
                'name': request.user.first_name or request.user.username,
                'provider': 'firebase' if request.user.username.startswith('firebase_') else 'local',
            },
        })


class MemoryStatsView(APIView):
    def get(self, request):
        character_id = request.query_params.get('character', 'elia')
        qs = Memory.objects.filter(character_id=character_id)
        archive_count = ArchiveRecord.objects.filter(character_id=character_id).count()
        rag_count = RagChunk.objects.filter(character_id=character_id).count()
        return Response({
            'total': qs.count(),
            'important': qs.filter(importance='high').count(),
            'days_together': 128,
            'story_volume': '382K',
            'fidelity': min(99, 70 + rag_count * 2),
            'archive_count': archive_count,
            'rag_chunks': rag_count,
        })


def _archive_simple(
    *,
    source_type: str,
    source_id: str,
    character_id: str = '',
    payload: dict,
    metadata: dict | None = None,
) -> None:
    """ARCHIVE 저장 + ArchiveRecord upsert (RAG 인덱싱 없이)."""

    import uuid

    object_key = minio_archive.put_archive_json(source_type, character_id or '_global', source_id, payload)
    rec = ArchiveRecord.objects.filter(
        source_type=source_type, source_id=source_id, character_id=character_id or ''
    ).first()
    if rec:
        if rec.object_key != object_key:
            rec.object_key = object_key
            rec.save(update_fields=['object_key'])
        return
    ArchiveRecord.objects.create(
        id=uuid.uuid4(),
        object_key=object_key,
        source_type=source_type,
        source_id=source_id,
        character_id=character_id or '',
        metadata=metadata or {},
    )


class LandingContentView(APIView):
    """랜딩/마케팅 콘텐츠 (1차: 단일 key=landing)."""

    permission_classes = [AllowAny]

    def get(self, request):
        obj, _ = LandingContent.objects.get_or_create(
            key='landing',
            defaults={
                'payload': {
                    'features': [
                        {
                            'key': 'memory',
                            'title': '기억하는 캐릭터',
                            'description': '대화와 사건을 장기 기억으로 저장하고, 다음 이야기에서 자연스럽게 이어집니다.',
                        },
                        {
                            'key': 'emotion',
                            'title': '감정과 관계',
                            'description': '6축 감정 시스템과 관계 변화를 통해 캐릭터가 함께 성장합니다.',
                        },
                        {
                            'key': 'world',
                            'title': '살아있는 세계관',
                            'description': '세계관/세력/이벤트가 쌓이며, 당신만의 연대기가 완성됩니다.',
                        },
                    ]
                }
            },
        )
        return Response(LandingContentSerializer(obj).data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        payload = request.data.get('payload')
        if not isinstance(payload, dict):
            return Response({'detail': 'payload must be an object'}, status=status.HTTP_400_BAD_REQUEST)
        obj, _ = LandingContent.objects.get_or_create(key='landing')
        obj.payload = payload
        obj.save(update_fields=['payload', 'updated_at'])
        _archive_simple(source_type='content', source_id='landing', payload={'key': 'landing', 'payload': payload})
        return Response(LandingContentSerializer(obj).data)


class ExploreMetaView(APIView):
    """탐색 UI용 메타(장르/태그)."""

    permission_classes = [AllowAny]

    def get(self, request):
        genres = set()
        tags = set()
        for c in Character.objects.all().only('genre', 'tags'):
            for g in (c.genre or []):
                genres.add(str(g))
            for t in (c.tags or []):
                tags.add(str(t).replace('#', ''))
        # UI에서 쓰는 '전체' 포함
        genre_list = ['전체'] + sorted(genres)
        tag_list = sorted(tags)[:24]
        return Response({'genres': genre_list, 'tags': tag_list})


class CharacterScenarioListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, character_id: str):
        qs = CharacterScenario.objects.filter(character_id=character_id).order_by('-is_default', 'scenario_id')
        return Response(CharacterScenarioSerializer(qs, many=True).data)

    def post(self, request, character_id: str):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            character = Character.objects.get(pk=character_id)
        except Character.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data or {}
        scenario_id = str(data.get('scenario_id') or '').strip() or None
        title = str(data.get('title') or '').strip()
        if not title:
            return Response({'detail': 'title is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not scenario_id:
            scenario_id = title.lower().replace(' ', '-')[:32] or 'scenario'
        obj, _ = CharacterScenario.objects.update_or_create(
            character=character,
            scenario_id=scenario_id,
            defaults={
                'title': title,
                'description': str(data.get('description') or ''),
                'prompt': str(data.get('prompt') or ''),
                'is_default': bool(data.get('is_default') or False),
                'created_by': request.user,
            },
        )
        _archive_simple(
            source_type='scenario',
            source_id=f'{character_id}_{scenario_id}',
            character_id=character_id,
            payload=CharacterScenarioSerializer(obj).data,
        )
        return Response(CharacterScenarioSerializer(obj).data, status=status.HTTP_201_CREATED)


class RelationshipGraphView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        world_id = request.query_params.get('world')
        center = request.query_params.get('center', 'elia')
        if not world_id:
            world_id = Character.objects.filter(pk=center).values_list('world_id', flat=True).first()
        if not world_id:
            return Response({'detail': 'world is required'}, status=status.HTTP_400_BAD_REQUEST)

        nodes = []
        for c in Character.objects.filter(world_id=world_id).select_related('world'):
            nodes.append(
                {
                    'id': c.id,
                    'label': c.name,
                    'kind': 'character',
                    'avatar': c.avatar,
                    'subtitle': c.world.name,
                    'tags': c.tags,
                    'worldId': c.world_id,
                    'isCenter': c.id == center,
                }
            )

        edges_qs = RelationshipEdge.objects.filter(world_id=world_id)
        edges = [
            {
                'id': str(e.id),
                'source': e.source_id,
                'target': e.target_id,
                'type': e.type,
                'label': e.label or '',
                'weight': e.weight,
            }
            for e in edges_qs
        ]
        return Response({'world': world_id, 'center': center, 'nodes': nodes, 'edges': edges})


class RelationshipHistoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        center = request.query_params.get('center', 'elia')
        world_id = request.query_params.get('world')
        if not world_id:
            world_id = Character.objects.filter(pk=center).values_list('world_id', flat=True).first()
        if not world_id:
            return Response({'detail': 'world is required'}, status=status.HTTP_400_BAD_REQUEST)

        events = list(
            RelationshipEvent.objects.filter(world_id=world_id, center_id=center).order_by('-date')[:50]
        )
        if not events:
            # fallback: memories 기반 간단 이벤트
            for m in Memory.objects.filter(character_id=center).order_by('-date')[:12]:
                events.append(
                    RelationshipEvent(
                        world_id=world_id,
                        center_id=center,
                        title=m.title,
                        date=m.date,
                        summary=m.summary,
                        delta=m.emotion,
                    )
                )
        data = RelationshipEventSerializer(events, many=True).data
        return Response(data)


class RelationshipEdgeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data or {}
        world_id = str(data.get('world_id') or '').strip()
        source_id = str(data.get('source_id') or '').strip()
        target_id = str(data.get('target_id') or '').strip()
        rel_type = str(data.get('type') or 'friend').strip()
        label = str(data.get('label') or '').strip()
        weight = int(data.get('weight') or 50)

        if not (world_id and source_id and target_id):
            return Response({'detail': 'world_id/source_id/target_id are required'}, status=400)

        try:
            world = World.objects.get(pk=world_id)
            source = Character.objects.get(pk=source_id)
            target = Character.objects.get(pk=target_id)
        except (World.DoesNotExist, Character.DoesNotExist):
            return Response({'detail': 'Not found'}, status=404)

        edge = RelationshipEdge.objects.create(
            world=world,
            source=source,
            target=target,
            type=rel_type,
            label=label,
            weight=max(0, min(100, weight)),
            created_by=request.user,
        )
        payload = RelationshipEdgeSerializer(edge).data
        _archive_simple(
            source_type='relationship',
            source_id=f'edge_{edge.id}',
            character_id=source_id,
            payload=payload,
        )
        return Response(payload, status=201)


class StudioCharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.select_related('world').all()
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return StudioCharacterSerializer
        return CharacterSerializer

    def get_permissions(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE'):
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        obj = serializer.save(created_by=self.request.user)
        _archive_simple(source_type='studio', source_id=f'character_{obj.id}', character_id=obj.id, payload=serializer.data)

    def perform_update(self, serializer):
        obj = serializer.save()
        _archive_simple(source_type='studio', source_id=f'character_{obj.id}', character_id=obj.id, payload=serializer.data)


class StudioWorldViewSet(viewsets.ModelViewSet):
    queryset = World.objects.all()
    serializer_class = WorldSerializer
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE'):
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        obj = serializer.save(created_by=self.request.user)
        _archive_simple(source_type='studio', source_id=f'world_{obj.id}', payload=serializer.data)

    def perform_update(self, serializer):
        obj = serializer.save()
        _archive_simple(source_type='studio', source_id=f'world_{obj.id}', payload=serializer.data)
