from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    ArchiveViewSet,
    CharacterViewSet,
    CharacterScenarioListCreateView,
    ChatSessionsListView,
    ChatViewSet,
    EmotionView,
    ExploreMetaView,
    FirebaseLoginView,
    LandingContentView,
    LoginView,
    MeView,
    MemoryStatsView,
    MemoryViewSet,
    RagSearchView,
    RelationshipEdgeCreateView,
    RelationshipGraphView,
    RelationshipHistoryView,
    StudioCharacterViewSet,
    StudioWorldViewSet,
    WorldViewSet,
)

router = DefaultRouter()
router.register('worlds', WorldViewSet, basename='world')
router.register('characters', CharacterViewSet, basename='character')
router.register('memories', MemoryViewSet, basename='memory')
router.register('archive', ArchiveViewSet, basename='archive')
router.register('studio/characters', StudioCharacterViewSet, basename='studio-character')
router.register('studio/worlds', StudioWorldViewSet, basename='studio-world')

chat_messages = ChatViewSet.as_view({'get': 'list', 'post': 'create'})
chat_stream = ChatViewSet.as_view({'post': 'stream'})

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/firebase/', FirebaseLoginView.as_view(), name='auth-firebase'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    path('content/landing/', LandingContentView.as_view(), name='content-landing'),
    path('meta/explore/', ExploreMetaView.as_view(), name='meta-explore'),
    path('characters/<slug:character_id>/scenarios/', CharacterScenarioListCreateView.as_view(), name='character-scenarios'),
    path('relationship/graph/', RelationshipGraphView.as_view(), name='relationship-graph'),
    path('relationship/history/', RelationshipHistoryView.as_view(), name='relationship-history'),
    path('relationship/edges/', RelationshipEdgeCreateView.as_view(), name='relationship-edge-create'),
    path('emotion/<slug:character_id>/', EmotionView.as_view(), name='emotion'),
    path('memory-stats/', MemoryStatsView.as_view(), name='memory-stats'),
    path('rag/search/', RagSearchView.as_view(), name='rag-search'),
    path('chat-sessions/', ChatSessionsListView.as_view(), name='chat-sessions'),
    path('chat/<slug:character_id>/', chat_messages, name='chat-messages'),
    path('chat/<slug:character_id>/stream/', chat_stream, name='chat-stream'),
] + router.urls
