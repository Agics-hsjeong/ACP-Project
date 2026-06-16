from datetime import date

from django.core.management.base import BaseCommand

from api.models import (
    Character,
    CharacterScenario,
    ChatMessage,
    ChatSession,
    EmotionAxis,
    LandingContent,
    Memory,
    RelationshipEdge,
    RelationshipEvent,
    World,
)

WORLDS = [
    {
        'id': 'arcadia',
        'name': '아르카디아 연대기',
        'genre': ['판타지', '중세'],
        'character_count': 24,
        'cover': 'https://api.dicebear.com/9.x/shapes/svg?seed=arcadia&backgroundColor=4338ca',
    },
    {
        'id': 'galaxy',
        'name': '은하 연합 연대기',
        'genre': ['SF', '우주'],
        'character_count': 18,
        'cover': 'https://api.dicebear.com/9.x/shapes/svg?seed=galaxy&backgroundColor=1e293b',
    },
    {
        'id': 'moonforest',
        'name': '달빛 숲의 전설',
        'genre': ['판타지', '자연'],
        'character_count': 12,
        'cover': 'https://api.dicebear.com/9.x/shapes/svg?seed=moonforest&backgroundColor=312e81',
    },
    {
        'id': 'neon',
        'name': '네온 시티 2087',
        'genre': ['사이버펑크', '스릴러'],
        'character_count': 15,
        'cover': 'https://api.dicebear.com/9.x/shapes/svg?seed=neon&backgroundColor=06b6d4',
    },
]

CHARACTERS = [
    {
        'id': 'elia',
        'name': '엘리아',
        'title': '아르카디아 왕국의 공주',
        'world_id': 'arcadia',
        'tags': ['여성', '2세', '왕족', '츤데레', '기사'],
        'genre': ['판타지', '로맨스'],
        'likes': 98,
        'views': 12400,
        'description': '차가운 외면과 따뜻한 내면을 가진 아르카디아 왕국의 공주.',
        'personality': ['차분함', '지적', '호기심', '고독'],
        'occupation': '공주',
        'race': '인간',
        'age': 21,
        'gender': '여성',
        'quote': '"밤하늘을 함께 바라볼 수 있다면, 왕궁의 고독도 견딜 수 있을 것 같아요."',
        'memory_summary': '달빛 아래의 대화, 왕궁 정원에서의 첫 만남',
        'avatar': 'https://api.dicebear.com/9.x/notionists/svg?seed=elia&backgroundColor=6366f1',
        'cover': 'https://api.dicebear.com/9.x/shapes/svg?seed=elia-world&backgroundColor=312e81',
    },
    {
        'id': 'kael',
        'name': '카엘',
        'title': '은하 연합의 파일럿',
        'world_id': 'galaxy',
        'tags': ['남성', 'SF', '전투'],
        'genre': ['SF'],
        'likes': 92,
        'views': 9800,
        'description': '냉철한 판단력을 가진 은하 연합 최연소 파일럿.',
        'personality': ['냉정', '책임감', '유머'],
        'occupation': '파일럿',
        'race': '인간',
        'avatar': 'https://api.dicebear.com/9.x/notionists/svg?seed=kael&backgroundColor=4f46e5',
        'cover': 'https://api.dicebear.com/9.x/shapes/svg?seed=kael-world&backgroundColor=1e293b',
    },
    {
        'id': 'luna',
        'name': '루나',
        'title': '달빛 숲의 수호자',
        'world_id': 'moonforest',
        'tags': ['여성', '판타지', '엘프'],
        'genre': ['판타지'],
        'likes': 95,
        'views': 11200,
        'description': '고대 숲을 지키는 엘프 수호자.',
        'personality': ['신비로움', '온화', '결단력'],
        'occupation': '수호자',
        'race': '엘프',
        'avatar': 'https://api.dicebear.com/9.x/notionists/svg?seed=luna&backgroundColor=8b5cf6',
        'cover': 'https://api.dicebear.com/9.x/shapes/svg?seed=luna-world&backgroundColor=4338ca',
    },
    {
        'id': 'mira',
        'name': '미라',
        'title': '마법 학원의 신입',
        'world_id': 'arcadia',
        'tags': ['여성', '마법', '신입'],
        'genre': ['판타지', '학원'],
        'likes': 90,
        'views': 8900,
        'description': '마법 재능은 뛰어나지만 자신감이 부족한 신입 마법사.',
        'personality': ['수줍음', '성실', '호기심'],
        'occupation': '마법사',
        'race': '인간',
        'age': 19,
        'gender': '여성',
        'quote': '"저… 저도 할 수 있어요!"',
        'memory_summary': '마법 시험, 첫 주문, 도서관 실수',
        'avatar': 'https://api.dicebear.com/9.x/notionists/svg?seed=mira&backgroundColor=ec4899',
        'cover': 'https://api.dicebear.com/9.x/shapes/svg?seed=mira-world&backgroundColor=334155',
    },
]

EMOTIONS = [
    ('affection', '애정', 72, '#ec4899'),
    ('trust', '신뢰', 65, '#6366f1'),
    ('respect', '존경', 58, '#8b5cf6'),
    ('anger', '분노', 12, '#ef4444'),
    ('fear', '공포', 8, '#94a3b8'),
    ('jealousy', '질투', 15, '#f59e0b'),
]

MEMORIES = [
    {
        'id': '1',
        'character_id': 'elia',
        'title': '달빛 아래의 대화',
        'summary': '성 탑에서 엘리아와 밤하늘을 함께 바라보며 깊은 대화를 나눴다.',
        'detail': '왕궁의 화려함과 달리 고요한 탑 방에서 엘리아는 처음으로 진심을 털어놓았다.',
        'emotion': '애정 +15',
        'date': date(2026, 6, 14),
        'importance': 'high',
        'tags': ['#달빛', '#탑', '#고백'],
        'quote': '"당신과 함께라면 이 밤이 덜 외로울 것 같아요."',
        'location': '아르카디아 성 탑',
        'dday': 1,
        'stats': {'affection': 15, 'trust': 8},
    },
    {
        'id': '2',
        'character_id': 'elia',
        'title': '첫 만남 — 왕궁 정원',
        'summary': '정원에서 우연히 마주친 엘리아.',
        'detail': '왕궁 정원의 장미 덤불 사이에서 마주친 엘리아.',
        'emotion': '신뢰 +10',
        'date': date(2026, 6, 10),
        'importance': 'high',
        'tags': ['#첫만남', '#정원'],
        'location': '왕궁 정원',
        'dday': 5,
        'stats': {'trust': 10, 'respect': 5},
    },
]

SEED_MESSAGES = [
    ('narration', '달빛이 성의 창문을 통해 스며들었다. 엘리아는 창밖의 별빛을 바라보며 한숨을 쉬었다.', ''),
    ('character', '또 이런 밤이네요... 왕궁은 화려하지만, 때로는 이 탑이 더 편안해요.', '오후 9:32'),
    ('user', '밤하늘이 정말 아름답네요. 같이 보면 더 좋을 것 같아요.', '오후 9:33'),
    (
        'character',
        '...그렇게 말해주시니, 조금은 마음이 따뜻해지네요. 당신과 함께라면 이 밤이 덜 외로울 것 같아요.',
        '오후 9:34',
    ),
]

LANDING_FEATURES = [
    {'title': 'Living Memory', 'description': 'AI가 당신과의 모든 순간을 기억하고 이어갑니다.'},
    {'title': 'Emotion Engine', 'description': '6축 감정 시스템으로 깊이 있는 관계를 형성하세요.'},
    {'title': 'World Studio', 'description': '세계관·캐릭터·관계를 직접 창작하고 공유하세요.'},
]

SCENARIOS = {
    'elia': [
        {'scenario_id': 'default', 'title': '기본 시나리오', 'description': '왕궁에서의 일상 대화'},
        {'scenario_id': 'moon', 'title': '달빛의 밤', 'description': '성 탑에서 밤하늘을 함께 바라본다'},
        {'scenario_id': 'garden', 'title': '왕궁 정원', 'description': '장미 덤불 사이에서 우연한 만남'},
    ]
}

RELATIONSHIPS = [
    {
        'world_id': 'arcadia',
        'source_id': 'elia',
        'target_id': 'mira',
        'type': 'alliance',
        'label': '학원 선후배',
        'weight': 65,
    },
]


class Command(BaseCommand):
    help = 'Seed database with ACP mock data'

    def handle(self, *args, **options):
        if World.objects.exists():
            self.stdout.write('Data already seeded, ensuring extra seed content...')
            self._ensure_extra_seed_content()
            self.stdout.write('Running archive/RAG sync...')
            self._archive_all()
            return

        for w in WORLDS:
            World.objects.create(**w)

        for c in CHARACTERS:
            world_id = c.pop('world_id')
            Character.objects.create(world_id=world_id, **c)

        for m in MEMORIES:
            char_id = m.pop('character_id')
            Memory.objects.create(character_id=char_id, **m)

        # Landing content
        LandingContent.objects.create(key='landing_features', payload={'features': LANDING_FEATURES})

        # Scenarios
        for char_id, items in SCENARIOS.items():
            for item in items:
                CharacterScenario.objects.create(character_id=char_id, **item)

        elia = Character.objects.get(pk='elia')
        for key, label, value, color in EMOTIONS:
            EmotionAxis.objects.create(
                character=elia, key=key, label=label, value=value, color=color
            )

        session, _ = ChatSession.objects.get_or_create(character=elia)
        for role, content, ts in SEED_MESSAGES:
            ChatMessage.objects.create(session=session, role=role, content=content, timestamp=ts)

        # Relationship seed
        for edge in RELATIONSHIPS:
            RelationshipEdge.objects.create(**edge)
        RelationshipEvent.objects.create(
            world_id='arcadia',
            center_id='elia',
            title='첫 관계 설정',
            date=date(2026, 6, 16),
            summary='초기 관계도가 생성되었습니다.',
            delta='+seed',
        )

        self.stdout.write(self.style.SUCCESS('Seed complete.'))
        self._archive_all()

    def _ensure_extra_seed_content(self):
        # Worlds / Characters (create missing only; keep existing intact)
        for w in WORLDS:
            World.objects.get_or_create(id=w['id'], defaults=w)

        for c in CHARACTERS:
            payload = dict(c)
            world_id = payload.pop('world_id')
            Character.objects.get_or_create(id=payload['id'], defaults={**payload, 'world_id': world_id})

        # Landing content
        LandingContent.objects.get_or_create(
            key='landing_features', defaults={'payload': {'features': LANDING_FEATURES}}
        )

        # Scenarios (idempotent-ish: avoid duplicates by (character_id,title))
        for char_id, items in SCENARIOS.items():
            for item in items:
                scenario_id = item.get('scenario_id') or item['title']
                # Legacy rows might have blank scenario_id; fix them if title matches.
                legacy = CharacterScenario.objects.filter(
                    character_id=char_id, scenario_id='', title=item['title']
                ).first()
                if legacy is not None:
                    legacy.scenario_id = scenario_id
                    legacy.description = item['description']
                    legacy.save(update_fields=['scenario_id', 'description'])
                    continue

                obj, created = CharacterScenario.objects.get_or_create(
                    character_id=char_id,
                    scenario_id=scenario_id,
                    defaults={'title': item['title'], 'description': item['description']},
                )
                if not created and (obj.title != item['title'] or obj.description != item['description']):
                    obj.title = item['title']
                    obj.description = item['description']
                    obj.save(update_fields=['title', 'description'])

        # Relationship edges (avoid duplicates by (source,target,type,label))
        for edge in RELATIONSHIPS:
            RelationshipEdge.objects.get_or_create(
                world_id=edge['world_id'],
                source_id=edge['source_id'],
                target_id=edge['target_id'],
                type=edge['type'],
                label=edge['label'],
                defaults={
                    'weight': edge.get('weight', 50),
                },
            )

        RelationshipEvent.objects.get_or_create(
            title='첫 관계 설정',
            world_id='arcadia',
            center_id='elia',
            date=date(2026, 6, 16),
            defaults={'summary': '초기 관계도가 생성되었습니다.', 'delta': '+seed'},
        )

    def _archive_all(self):
        from api.services import rag
        from api.views import _archive_simple

        self.stdout.write('Archiving to /ARCHIVE/acp/data + MinIO and indexing RAG...')
        for char in Character.objects.all():
            rag.archive_character_bundle(char)
        for mem in Memory.objects.all():
            rag.archive_memory_record(mem)
        for msg in ChatMessage.objects.select_related('session__character'):
            rag.archive_chat_message(msg, msg.session.character_id)

        # Non-RAG archives (simple snapshots)
        for content in LandingContent.objects.all():
            _archive_simple(
                source_type='content',
                source_id=str(content.key),
                payload={'key': content.key, 'payload': content.payload},
            )
        for scenario in CharacterScenario.objects.all():
            _archive_simple(
                source_type='scenario',
                source_id=f'{scenario.character_id}_{scenario.scenario_id}',
                character_id=scenario.character_id,
                payload={
                    'character_id': scenario.character_id,
                    'scenario_id': scenario.scenario_id,
                    'title': scenario.title,
                    'description': scenario.description,
                },
            )
        for edge in RelationshipEdge.objects.all():
            _archive_simple(
                source_type='relationship',
                source_id=str(edge.id),
                payload={
                    'id': edge.id,
                    'world_id': edge.world_id,
                    'source_id': edge.source_id,
                    'target_id': edge.target_id,
                    'type': edge.type,
                    'label': edge.label,
                    'weight': edge.weight,
                },
            )
        for evt in RelationshipEvent.objects.all():
            _archive_simple(
                source_type='relationship',
                source_id=f'event_{evt.id}',
                payload={
                    'id': evt.id,
                    'world_id': evt.world_id,
                    'center_id': evt.center_id,
                    'title': evt.title,
                    'date': evt.date.isoformat() if evt.date else None,
                    'summary': evt.summary,
                    'delta': evt.delta,
                    'created_at': evt.created_at.isoformat() if evt.created_at else None,
                },
            )

        self.stdout.write(self.style.SUCCESS('Archive + RAG indexing complete.'))
