from rest_framework import serializers
from .models import ChatUserMessage, ChatBotResponse

class ChatUserMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatUserMessage
        fields = [
            'id',
            'user_uuid',
            'content',
            'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class ChatBotResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotResponse
        fields = [
            'id',                       # Primary key
            'user_uuid',
            'llm_model',
            'content',
            'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']