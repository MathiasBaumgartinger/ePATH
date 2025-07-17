from django.shortcuts import render
from django.views import View
from questionnaire.models import QuestionnaireDefinition, QuestionnaireRecord
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from questionnaire.serializers import QuestionnaireDefinitionSerializer, QuestionnaireRecordSerializer
import os
import json
from django.conf import settings


class SystemPromptView(APIView):
    def get(self, request, user_uuid, *args, **kwargs):
        try:
            latest_record = QuestionnaireRecord.objects.filter(user_uuid=user_uuid).latest('date')
        except QuestionnaireRecord.DoesNotExist:
            return Response(
                {"error": "No questionnaire record found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # Corrected path to the system prompt
            prompt_template_path = os.path.join(settings.BASE_DIR, 'questionnaire', 'resources', 'SYSTEM_PROMPT.md')
            with open(prompt_template_path, 'r') as f:
                prompt_template = f.read()
        except FileNotFoundError:
            return Response(
                {"error": "System prompt template not found."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Get the questionnaire definition and answers
        definition = latest_record.questionnaire_def_fk.definition
        answers = latest_record.answers

        # Create a lookup for questions to build a readable summary
        questions_map = {}
        for category in definition:
            cat_title = category.get('category_title')
            questions_map[cat_title] = {}
            for i, q_item in enumerate(category.get('questions', [])):
                question_text = q_item.get('question')
                questions_map[cat_title][f"{cat_title}-{i}"] = question_text

        # Build the human-readable summary
        summary_lines = []
        for category_title, category_answers in answers.items():
            summary_lines.append(f"Category: {category_title}")
            for answer_key, answer_value in category_answers.items():
                question = questions_map.get(category_title, {}).get(answer_key, "Unknown Question")
                summary_lines.append(f"  - {question}: {answer_value}")
        
        questionnaire_summary = "\n".join(summary_lines)
        questionnaire_definition = json.dumps(definition, indent=2)
        
        # Format the final prompt with both summary and definition
        formatted_prompt = prompt_template.format(
            questionnaire_summary=questionnaire_summary,
            questionnaire_definition=questionnaire_definition
        )

        return Response(
            {
                "role": "system",
                "content": formatted_prompt
            },
            status=status.HTTP_200_OK
        )


class QuestionnaireDefinitionView(APIView):
    def _verify_country(self, request):
        country = request.query_params.get('country')
        if not country:
            return Response(
                {"error": "Missing required query parameter: 'country'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return country
    
    def _verify_definition_json(self, request):
        definition_json = request.data.get('definition')
        # Ensure definition is an array of category objects
        if not isinstance(definition_json, list):
            return Response(
                {"error": "Invalid questionnaire definition format. Expected a JSON array."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return definition_json
    
    def post(self, request, *args, **kwargs):
        # Validate input definition JSON
        definition_or_response = self._verify_definition_json(request)
        if isinstance(definition_or_response, Response):
            return definition_or_response

        # Create a new questionnaire definition
        serializer = QuestionnaireDefinitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # id auto-generated in model.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        country_or_response = self._verify_country(request)
        # If _verify_request returned a Response, bail out early
        if isinstance(country_or_response, Response):
            return country_or_response

        # Fetch most recent questionnaire for this country
        questionnaire = (
            QuestionnaireDefinition.objects
            .filter(country=country_or_response)
            .order_by('version')
            .first()
        )
        if not questionnaire:
            return Response(
                {"error": f"No questionnaire found for country '{country_or_response}'."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = QuestionnaireDefinitionSerializer(questionnaire)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuestionnaireRecordView(APIView):
    def _validate_answers(self, definition, answers):
        if not isinstance(definition, dict) or not isinstance(answers, dict):
            return False
        
        definition_keys = set(definition.keys())
        answers_keys = set(answers.keys())
        
        # Check if all keys in answers are present in the definition
        if not answers_keys == definition_keys:
            return False
        
        for key in answers_keys:
            # Optionally, check for specific value types or structures based on the definition
            # For example, if the definition specifies a list of options for a question
            if isinstance(definition[key], list) and not isinstance(answers[key], list):
                return False
        
        # Optionally, check for additional validation rules here
        return True
    
    def _verify(self, request) -> Response:
        questionnaire_def = QuestionnaireDefinition.objects.get(id=request.data.get('questionnaire_def_fk'))
        if not questionnaire_def:
            return Response(
                {"error": "Invalid or missing questionnaire definition."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: Validate the answers against the questionnaire definition
        # if not self._validate_answers(questionnaire_def.definition, request.data.get('answers', {})):
        #     return Response(
        #         {"error": "Answers do not match the questionnaire definition."},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        
        return Response(status=status.HTTP_200_OK)
        
    def _get_questionnaire_status(self, request):
        for category in request.data.get('answers', {}).keys():
            for question in request.data['answers'][category]["questions"]:
                if question.get("answer") is None:
                    return QuestionnaireRecord.EARLY_EXITED
        return QuestionnaireRecord.COMPLETED
    
    
    def post(self, request, *args, **kwargs) -> Response:
        # Verify the request
        print(request.data)
        verification_response = self._verify(request)
        if verification_response and verification_response.status_code != status.HTTP_200_OK:
            return verification_response
        
        # Create a new questionnaire definition
        serializer = QuestionnaireRecordSerializer(
            data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs) -> Response:
        user_uuid = request.query_params.get('user_uuid')
        if not user_uuid:
            return Response(
                {"error": "Missing required query parameter: 'user_uuid'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Fetch all records for this user
        records = QuestionnaireRecord.objects.filter(user_uuid=user_uuid).order_by('-date')
        serializer = QuestionnaireRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class QuestionnaireDefinitionManagementView(CreateView):
    """
    A standard Django view to handle the creation and listing of
    QuestionnaireDefinition objects.
    
    Inherits from CreateView to get form handling for creating new objects,
    and we add a list of existing objects to the context.
    """
    model = QuestionnaireDefinition
    template_name = "questionnaire/definition_management.html"
    success_url = reverse_lazy("questionnaire:definition_management")
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the definitions to display in a table
        context["object_list"] = self.get_queryset().order_by('-release_date')
        context["page_title"] = "Questionnaire Definitions"
        return context

class QuestionnaireView(View):
  def get(self, request, *args, **kwargs):
        return render(request, "questionnaire.html")