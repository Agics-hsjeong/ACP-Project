from django.conf import settings
from django.db import models
from pgvector.django import HnswIndex, VectorField


class World(models.Model):
    id = models.SlugField(primary_key=True, max_length=64)
    name = models.CharField(max_length=200)
    genre = models.JSONField(default=list)
    character_count = models.PositiveIntegerField(default=0)
    cover = models.URLField(max_length=500)
    studio_meta = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='worlds_created',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Character(models.Model):
    id = models.SlugField(primary_key=True, max_length=64)
    name = models.CharField(max_length=120)
    title = models.CharField(max_length=200)
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='characters')
    tags = models.JSONField(default=list)
    genre = models.JSONField(default=list, blank=True)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    description = models.TextField()
    personality = models.JSONField(default=list)
    occupation = models.CharField(max_length=120)
    race = models.CharField(max_length=80)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    quote = models.TextField(blank=True)
    memory_summary = models.TextField(blank=True)
    avatar = models.URLField(max_length=500)
    cover = models.URLField(max_length=500)
    studio_meta = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='characters_created',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Memory(models.Model):
    IMPORTANCE_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    id = models.SlugField(primary_key=True, max_length=64)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='memories')
    title = models.CharField(max_length=200)
    summary = models.TextField()
    detail = models.TextField(blank=True)
    emotion = models.CharField(max_length=80)
    date = models.DateField()
    importance = models.CharField(max_length=10, choices=IMPORTANCE_CHOICES, default='medium')
    tags = models.JSONField(default=list, blank=True)
    quote = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    thumbnail = models.URLField(max_length=500, blank=True)
    dday = models.PositiveSmallIntegerField(null=True, blank=True)
    stats = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title


class EmotionAxis(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='emotions')
    key = models.CharField(max_length=32)
    label = models.CharField(max_length=32)
    value = models.FloatField(default=0)
    color = models.CharField(max_length=16)

    class Meta:
        unique_together = [('character', 'key')]
        ordering = ['id']

    def __str__(self):
        return f'{self.character_id}:{self.key}'


class ChatSession(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='chat_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('character', 'Character'),
        ('narration', 'Narration'),
        ('system', 'System'),
    ]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=16, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.CharField(max_length=32, blank=True)
    emotion_delta = models.CharField(max_length=32, blank=True)
    interaction_type = models.CharField(max_length=16, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class ArchiveRecord(models.Model):
    """/ARCHIVE/acp/data MinIO 메타데이터."""

    SOURCE_TYPES = [
        ('chat', 'Chat'),
        ('memory', 'Memory'),
        ('character', 'Character'),
        ('world', 'World'),
        ('emotion', 'Emotion'),
        ('session', 'Session'),
        ('interaction', 'Interaction'),
        ('content', 'Content'),
        ('scenario', 'Scenario'),
        ('relationship', 'Relationship'),
        ('studio', 'Studio'),
    ]

    id = models.UUIDField(primary_key=True, editable=False)
    object_key = models.CharField(max_length=512, unique=True)
    source_type = models.CharField(max_length=32, choices=SOURCE_TYPES)
    source_id = models.CharField(max_length=128)
    character_id = models.CharField(max_length=64, blank=True, db_index=True)
    content_type = models.CharField(max_length=64, default='application/json')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['source_type', 'character_id']),
        ]

    def __str__(self):
        return self.object_key


class RagChunk(models.Model):
    """RAG 검색용 임베딩 청크."""

    archive = models.ForeignKey(
        ArchiveRecord, on_delete=models.CASCADE, related_name='chunks', null=True, blank=True
    )
    character_id = models.CharField(max_length=64, db_index=True)
    source_type = models.CharField(max_length=32)
    source_id = models.CharField(max_length=128)
    chunk_text = models.TextField()
    embedding = VectorField(dimensions=768)
    importance = models.FloatField(default=0.5)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            HnswIndex(
                name='rag_chunk_embedding_hnsw',
                fields=['embedding'],
                m=16,
                ef_construction=64,
                opclasses=['vector_cosine_ops'],
            ),
        ]

    def __str__(self):
        return f'{self.character_id}:{self.source_type}:{self.source_id}'


class LandingContent(models.Model):
    """간단 CMS (랜딩 등) + ARCHIVE 스냅샷용."""

    key = models.SlugField(primary_key=True, max_length=64)
    payload = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['key']


class CharacterScenario(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='scenarios')
    scenario_id = models.SlugField(max_length=64)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    prompt = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='scenarios_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('character', 'scenario_id')]
        ordering = ['character_id', 'scenario_id']


class RelationshipEdge(models.Model):
    """관계도 엣지 (1차: 캐릭터-캐릭터)."""

    REL_TYPES = [
        ('friend', 'Friend'),
        ('alliance', 'Alliance'),
        ('enemy', 'Enemy'),
        ('lover', 'Lover'),
        ('family', 'Family'),
        ('ex_lover', 'ExLover'),
        ('neutral', 'Neutral'),
    ]

    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='relationship_edges')
    source = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='relationship_edges_out')
    target = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='relationship_edges_in')
    type = models.CharField(max_length=16, choices=REL_TYPES, default='friend')
    label = models.CharField(max_length=80, blank=True)
    weight = models.PositiveSmallIntegerField(default=50)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='relationship_edges_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['world_id', 'source_id'])]


class RelationshipEvent(models.Model):
    """관계 히스토리(타임라인)."""

    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='relationship_events')
    center = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='relationship_events_center')
    title = models.CharField(max_length=200)
    date = models.DateField()
    summary = models.TextField(blank=True)
    delta = models.CharField(max_length=32, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='relationship_events_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
