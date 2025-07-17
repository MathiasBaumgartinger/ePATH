from django.shortcuts import render
from django.views import View
from .serializers import ChatUserMessageSerializer, ChatBotResponseSerializer
from .models import ChatUserMessage, ChatBotResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import logging
import os


logger = logging.getLogger(__name__)

class LLMAPIView(APIView):
    CHATBOT_MODEL = "gpt-4o"

    def post(self, request, *args, **kwargs):
        client = OpenAI(
            api_key = os.environ.get("OPENAI_API_KEY"),
        )
        
        # expecting a list of messages in OpenAI chat format:
        # [{"role": "system", "content": "You are a helpful assistant."}, ...]
        messages = request.data.get("messages", [])
        if not messages:
            return Response(
                {"error": "No messages provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        completion = client.chat.completions.create(
            model=self.CHATBOT_MODEL,
            messages=messages
        )

        try:
            chatbot_data = {
                "user_uuid": request.data.get("user_uuid", "default-uuid"),
                "llm_model": self.CHATBOT_MODEL,
                "content": completion.choices[0].message.content
            }
            serializer = ChatBotResponseSerializer(data=chatbot_data)
            if serializer.is_valid():
                serializer.save()  # id auto-generated in model.save()
        except Exception as e:
            logger.error(f"Error saving chatbot response: {e}", exc_info=True)
        finally:
            return Response(
                {
                    "response": completion.choices[0].message.content
                },
                status=status.HTTP_200_OK
            )


class ChatAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        if request.data.get('type') == 'message':
            del request.data['type']
            return _handle_post_message(request)
        elif request.data.get('type') == 'response':
            del request.data['type']
            return _handle_post_response(request)
        
        return Response(
            {"error": "Invalid type. Expected 'message' or 'response'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, *args, **kwargs):
        # Fetch the entire chat history for a user
        user_uuid = request.query_params.get('user_uuid')
        if not user_uuid:
            return Response(
                {"error": "Missing required query parameter: 'user_uuid'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        messages = ChatUserMessage.objects.filter(user_uuid=user_uuid).order_by('timestamp')
        responses = ChatBotResponse.objects.filter(user_uuid=user_uuid).order_by('timestamp')
        if not messages and not responses:
            return Response(
                {"error": "No chat history found for this user."},
                status=status.HTTP_204_NO_CONTENT
            )

        messages_serializer = ChatBotResponseSerializer(messages)
        responses_serializer = ChatBotResponseSerializer(responses, many=True)
        data = {
            "messages": messages_serializer.data,
            "responses": responses_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

def _handle_post_message(request):
    """Handle the POST request for chat messages."""
    print("Handling message")
    serializer = ChatUserMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # id auto-generated in model.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def _handle_post_response(request):
    """Handle the POST request for chatbot responses."""
    serializer = ChatBotResponseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # id auto-generated in model.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatInterfaceView(View):
  def get(self, request, *args, **kwargs):
        return render(request, "chat.html")