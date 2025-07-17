from django.urls import path, re_path
from .views import ChatAPIView, ChatInterfaceView, LLMAPIView

urlpatterns = [
    # SPA entry point for chat
    path('', ChatInterfaceView.as_view(), name='chat'),
    path('api/', ChatAPIView.as_view(), name='chat_api'),
    path('llm_api/', LLMAPIView.as_view(), name='llm_api'),
]