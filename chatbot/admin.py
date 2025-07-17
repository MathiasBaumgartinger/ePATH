from django.contrib import admin
from .models import ChatUserMessage, ChatBotResponse


admin.site.register(ChatUserMessage)
admin.site.register(ChatBotResponse)