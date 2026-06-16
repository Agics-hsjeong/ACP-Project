from django.contrib import admin

from .models import Character, ChatMessage, ChatSession, EmotionAxis, Memory, World

admin.site.register(World)
admin.site.register(Character)
admin.site.register(Memory)
admin.site.register(EmotionAxis)
admin.site.register(ChatSession)
admin.site.register(ChatMessage)
