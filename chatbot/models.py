from django.db import models


class ChatUserMessage(models.Model):
    """A model to store chat messages in a conversation."""
    id = models.AutoField(primary_key=True)
    user_uuid = models.CharField(max_length=36, db_index=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'chatbot'
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Message-user:{self.user_uuid}-{self.timestamp}"


class ChatBotResponse(models.Model):
    """A model to store responses from the chatbot."""
    id = models.AutoField(primary_key=True)
    user_uuid = models.CharField(max_length=36, db_index=True)
    llm_model = models.CharField(max_length=100, default='gpt-3.5-turbo')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'chatbot'
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Response-user:{self.user_uuid}-{self.timestamp}"