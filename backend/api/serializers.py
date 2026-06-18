from rest_framework import serializers

from .models import (
    ArchiveRecord,
    Character,
    CharacterScenario,
    ChatMessage,
    EmotionAxis,
    LandingContent,
    Memory,
    RelationshipEdge,
    RelationshipEvent,
    World,
)


class WorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = World
        fields = ['id', 'name', 'genre', 'character_count', 'cover', 'studio_meta']


class StudioWorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = World
        fields = ['id', 'name', 'genre', 'character_count', 'cover', 'studio_meta']


class CharacterSerializer(serializers.ModelSerializer):
    world_id = serializers.CharField(read_only=True)
    world_name = serializers.CharField(source='world.name', read_only=True)

    class Meta:
        model = Character
        fields = [
            'id',
            'name',
            'title',
            'world_id',
            'world_name',
            'tags',
            'genre',
            'likes',
            'views',
            'description',
            'personality',
            'occupation',
            'race',
            'age',
            'gender',
            'quote',
            'memory_summary',
            'avatar',
            'cover',
        ]


class CharacterListSerializer(serializers.ModelSerializer):
    world = serializers.CharField(source='world.name', read_only=True)
    world_id = serializers.CharField(read_only=True)

    class Meta:
        model = Character
        fields = [
            'id',
            'name',
            'title',
            'world',
            'world_id',
            'tags',
            'genre',
            'likes',
            'views',
            'description',
            'personality',
            'occupation',
            'race',
            'age',
            'gender',
            'quote',
            'memory_summary',
            'avatar',
            'cover',
        ]


class MemorySerializer(serializers.ModelSerializer):
    character_id = serializers.CharField(read_only=True)

    class Meta:
        model = Memory
        fields = [
            'id',
            'character_id',
            'title',
            'summary',
            'detail',
            'emotion',
            'date',
            'importance',
            'tags',
            'quote',
            'location',
            'thumbnail',
            'dday',
            'stats',
        ]


class EmotionAxisSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionAxis
        fields = ['key', 'label', 'value', 'color']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'timestamp', 'emotion_delta', 'interaction_type', 'created_at']
        read_only_fields = ['id', 'created_at']


class MemoryCreateSerializer(serializers.ModelSerializer):
    character_id = serializers.SlugField(write_only=True)

    class Meta:
        model = Memory
        fields = [
            'id',
            'character_id',
            'title',
            'summary',
            'detail',
            'emotion',
            'date',
            'importance',
            'tags',
            'quote',
            'location',
        ]
        extra_kwargs = {
            'id': {'required': False},
            'detail': {'required': False, 'allow_blank': True},
            'emotion': {'required': False, 'default': '따뜻함'},
            'importance': {'required': False, 'default': 'medium'},
            'tags': {'required': False},
            'quote': {'required': False, 'allow_blank': True},
            'location': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        import uuid
        from datetime import date

        character_id = validated_data.pop('character_id')
        character = Character.objects.get(pk=character_id)
        memory_id = validated_data.get('id') or str(uuid.uuid4())[:8]
        return Memory.objects.create(
            id=memory_id,
            character=character,
            date=validated_data.get('date') or date.today(),
            **{k: v for k, v in validated_data.items() if k not in ('id', 'date')},
        )


class ArchiveRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveRecord
        fields = [
            'id',
            'object_key',
            'source_type',
            'source_id',
            'character_id',
            'content_type',
            'metadata',
            'created_at',
        ]


class RagSearchSerializer(serializers.Serializer):
    character_id = serializers.CharField(max_length=64)
    query = serializers.CharField(max_length=2000)
    top_k = serializers.IntegerField(min_value=1, max_value=20, required=False, default=5)


class FirebaseLoginSerializer(serializers.Serializer):
    id_token = serializers.CharField()


class ChatSendSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=4000)


class StudioCharacterSerializer(serializers.ModelSerializer):
    """스튜디오용: world_id를 입력으로 허용."""

    world_id = serializers.SlugField(write_only=True, required=False)
    world_name = serializers.CharField(source='world.name', read_only=True)

    class Meta:
        model = Character
        fields = [
            'id',
            'name',
            'title',
            'world_id',
            'world_name',
            'tags',
            'genre',
            'likes',
            'views',
            'description',
            'personality',
            'occupation',
            'race',
            'age',
            'gender',
            'quote',
            'memory_summary',
            'avatar',
            'cover',
            'studio_meta',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['world_id'] = instance.world_id
        return data

    def create(self, validated_data):
        world_id = validated_data.pop('world_id', 'arcadia')
        world = World.objects.get(pk=world_id)
        return Character.objects.create(world=world, **validated_data)

    def update(self, instance, validated_data):
        world_id = validated_data.pop('world_id', None)
        if world_id:
            instance.world = World.objects.get(pk=world_id)
        return super().update(instance, validated_data)


class LandingContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingContent
        fields = ['key', 'payload', 'updated_at']


class CharacterScenarioSerializer(serializers.ModelSerializer):
    character_id = serializers.CharField(read_only=True)

    class Meta:
        model = CharacterScenario
        fields = [
            'character_id',
            'scenario_id',
            'title',
            'description',
            'prompt',
            'is_default',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class RelationshipEdgeSerializer(serializers.ModelSerializer):
    world_id = serializers.CharField(read_only=True)
    source_id = serializers.CharField(read_only=True)
    target_id = serializers.CharField(read_only=True)

    class Meta:
        model = RelationshipEdge
        fields = [
            'id',
            'world_id',
            'source_id',
            'target_id',
            'type',
            'label',
            'weight',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class RelationshipEventSerializer(serializers.ModelSerializer):
    world_id = serializers.CharField(read_only=True)
    center_id = serializers.CharField(read_only=True)

    class Meta:
        model = RelationshipEvent
        fields = [
            'id',
            'world_id',
            'center_id',
            'title',
            'date',
            'summary',
            'delta',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
