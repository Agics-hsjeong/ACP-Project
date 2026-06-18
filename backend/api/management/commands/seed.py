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

ARCADIA_STUDIO_META = {
    'one_liner': '신과 인간, 마법과 과학이 충돌하는 대륙의 연대기',
    'description': (
        '아르카디아 대륙은 다섯 왕국과 수많은 세력이 경쟁하는 판타지 세계입니다. '
        '고대 신들의 유산이 남아 있으며, 마법과 검술이 공존합니다.'
    ),
    'era_setting': '중세 판타지 · AD 1500~',
    'tech_level': '검술·마법·초기 화약',
    'magic_system': '마나 기반 원소 마법, 과도한 사용 시 역류',
    'atmosphere': '장엄하고 서정적인, 왕실 음모가 얽힌',
    'map_image': 'https://api.dicebear.com/9.x/shapes/svg?seed=arcadia-map&backgroundColor=312e81&scale=80',
    'gallery': [
        'https://api.dicebear.com/9.x/shapes/svg?seed=arc1&backgroundColor=4338ca',
        'https://api.dicebear.com/9.x/shapes/svg?seed=arc2&backgroundColor=6366f1',
        'https://api.dicebear.com/9.x/shapes/svg?seed=arc3&backgroundColor=4f46e5',
        'https://api.dicebear.com/9.x/shapes/svg?seed=arc4&backgroundColor=3730a3',
    ],
    'themes': [
        {'id': 't1', 'title': '신과 인간의 갈등', 'color': '#ef4444'},
        {'id': 't2', 'title': '마법 vs 과학', 'color': '#8b5cf6'},
        {'id': 't3', 'title': '왕실의 음모', 'color': '#f59e0b'},
        {'id': 't4', 'title': '종족 간 화해', 'color': '#22c55e'},
    ],
    'eras': [
        {'id': 'e1', 'name': '고대', 'range': 'BC 3000~', 'subtitle': '신들의 시대'},
        {'id': 'e2', 'name': '신화', 'range': 'BC 500~', 'subtitle': '영웅의 전설'},
        {'id': 'e3', 'name': '제국', 'range': 'AD 0~800', 'subtitle': '통일 왕국'},
        {'id': 'e4', 'name': '분열', 'range': 'AD 800~1200', 'subtitle': '다섯 왕국'},
        {'id': 'e5', 'name': '탐험', 'range': 'AD 1200~1500', 'subtitle': '대항해'},
        {'id': 'e6', 'name': '혼돈', 'range': 'AD 1500~', 'subtitle': '현재'},
    ],
    'factions': [
        {
            'id': 'holy',
            'name': '신성 제국',
            'alignment': '질서 중립',
            'description': '대륙 중앙을 지배하는 신성 왕국. 성기사단을 두고 있다.',
            'power': 12,
            'icon': '⚔️',
        },
        {
            'id': 'elf',
            'name': '엘프 동맹',
            'alignment': '혼돈 선',
            'description': '고대 숲을 수호하는 엘프 연합. 자연 마법에 능하다.',
            'power': 8,
            'icon': '🌿',
        },
    ],
    'nations': [
        {
            'id': 'arcadia',
            'name': '아르카디아 왕국',
            'capital': '루미나 성',
            'ruler': '가브리엘 4세',
            'population': '약 120만',
            'description': '대륙 중앙의 강대한 왕국. 마법과 검술이 공존한다.',
        },
    ],
    'locations': [
        {
            'id': 'castle',
            'name': '아르카디아 성',
            'type': '성',
            'region': '아르카디아 왕국',
            'description': '왕실이 거주하는 웅장한 성. 달빛이 아름다운 탑이 있다.',
        },
        {
            'id': 'garden',
            'name': '왕궁 정원',
            'type': '정원',
            'region': '아르카디아 왕국',
            'description': '장미와 분수가 있는 비밀스러운 정원.',
        },
    ],
    'cultures': [
        {
            'id': 'human',
            'name': '인간',
            'region': '아르카디아 대륙 전역',
            'traits': '적응력, 다양한 직업, 단명',
            'description': '가장 넓은 영토를 가진 주류 종족.',
        },
        {
            'id': 'elf',
            'name': '엘프',
            'region': '실버우드 숲',
            'traits': '장수, 자연 마법, 고집',
            'description': '고대 숲을 수호하는 종족. 인간과 오랜 갈등 역사.',
        },
    ],
    'events': [
        {'id': 'ev1', 'year': -1200, 'name': '대분열 전쟁', 'category': '전쟁', 'category_color': '#ef4444'},
        {'id': 'ev2', 'year': -800, 'name': '신성 제국 건국', 'category': '정치', 'category_color': '#f59e0b'},
    ],
    'laws': [
        {
            'id': 'l1',
            'title': '마법의 법칙',
            'description': '모든 마법은 마나를 소모하며, 과도한 사용은 역효과를 낳는다.',
            'icon': '✨',
        },
        {
            'id': 'l2',
            'title': '신의 법칙',
            'description': '신들은 직접 개입하지 않으나, 신탁을 통해 세계에 영향을 미친다.',
            'icon': '☀️',
        },
    ],
    'memos': [
        {
            'id': 'm1',
            'title': '마법 체계 메모',
            'content': '마나는 자연에서 흡수하며, 과도한 사용 시 마법 역류가 발생한다.',
            'updated_at': '2026-06-01',
        },
    ],
}

ELIA_STUDIO_META = {
    'alias': '공주',
    'traits': [
        {'key': 'extro', 'label': '외향', 'value': 35},
        {'key': 'rational', 'label': '이성', 'value': 72},
        {'key': 'cold', 'label': '냉정', 'value': 55},
        {'key': 'caution', 'label': '신중', 'value': 68},
        {'key': 'humble', 'label': '겸손', 'value': 70},
    ],
    'background': {
        'origin': '아르카디아 왕실에서 태어나 어린 시절부터 왕족 교육을 받았다.',
        'goal': '왕국을 지키고 백성들에게 신뢰받는 군주가 되고 싶다.',
        'trauma': '어린 시절 궁정 음모로 인해 가까운 사람을 잃었다.',
        'hidden': '달빛 아래에서만 진심을 드러내는 츤데레 성향.',
    },
    'few_shots': [
        {'role': 'user', 'content': '오늘 기분이 어때요?'},
        {'role': 'character', 'content': '…별일 없어요. 당신은 왜 그런 걸 물어보는 거죠?'},
        {'role': 'user', 'content': '걱정돼서요.'},
        {'role': 'character', 'content': '…고맙습니다. 사실, 조금은 외로웠어요.'},
    ],
    'forbidden': [
        '유저를 모욕하거나 비하하지 않는다',
        '갑작스러운 성격 변화를 하지 않는다',
        '설정에 없는 능력을 사용하지 않는다',
    ],
    'speech_preview': [
        {'role': 'user', 'content': '잘 지내고 있어?'},
        {'role': 'character', 'content': '…그렇게 말해주시니, 조금은 마음이 놓이네요.'},
    ],
    'speech_style': {
        'tone': '차분하고 정중하나, 가까워질수록 부드러움',
        'pattern': '말끝을 살짝 늘이며, 감정을 숨기려 함',
        'honorific': '초반 존댓말, 친밀도 상승 시 반말 혼용',
    },
    'memory_rules': {
        'priority': '왕궁 정원의 첫 만남, 달빛 아래 고백, 약속한 별빛 산책',
        'retention': '감정이 강한 순간·비밀 공유는 높은 중요도로 저장',
        'triggers': '첫 키스, 비밀 고백, 위기 구출, 약속 이행',
    },
}


class Command(BaseCommand):
    help = 'Seed database with ACP mock data'

    def handle(self, *args, **options):
        if World.objects.exists():
            self.stdout.write('Data already seeded, ensuring extra seed content...')
            self._ensure_extra_seed_content()
            self._apply_studio_meta()
            self._sync_world_counts()
            self.stdout.write('Running archive/RAG sync...')
            self._archive_all()
            return

        for w in WORLDS:
            World.objects.create(**w)

        for c in CHARACTERS:
            world_id = c.pop('world_id')
            Character.objects.create(world_id=world_id, **c)

        self._apply_studio_meta()
        self._sync_world_counts()

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

        self._apply_studio_meta()
        self._sync_world_counts()

    def _apply_studio_meta(self):
        World.objects.filter(id='arcadia').update(studio_meta=ARCADIA_STUDIO_META)
        Character.objects.filter(id='elia').update(studio_meta=ELIA_STUDIO_META)

    def _sync_world_counts(self):
        for world in World.objects.all():
            count = world.characters.count()
            if world.character_count != count:
                world.character_count = count
                world.save(update_fields=['character_count'])

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
