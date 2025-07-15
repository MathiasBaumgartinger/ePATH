from django.shortcuts import render
from django.views import View
from questionnaire.models import QuestionnaireDefinition, QuestionnaireRecord
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from questionnaire.serializers import QuestionnaireDefinitionSerializer, QuestionnaireRecordSerializer


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
        # TODO: Implement JSON schema validation here
        if not isinstance(definition_json, dict):
            return Response(
                {"error": "Invalid questionnaire definition format. Expected a JSON object."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return definition_json
    
    def post(self, request, *args, **kwargs):
        definition_or_response = self._verify_country(request)
        # If _verify_country returned a Response, bail out early
        if isinstance(definition_or_response, Response):
            return definition_or_response

        # Create a new questionnaire definition for the specified country
        serializer = QuestionnaireDefinitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(definition=definition_or_response)
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
        questionnaire_def = QuestionnaireDefinition.objects.get(request.data.get('questionnaire_def_fk'))
        if not questionnaire_def:
            return Response(
                {"error": "Invalid or missing questionnaire definition."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not self._validate_answers(questionnaire_def.definition, request.data.get('answers', {})):
            return Response(
                {"error": "Answers do not match the questionnaire definition."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(status=status.HTTP_200_OK)
        
    def _get_questionnaire_status(self, request):
        for category in request.data.get('answers', {}).keys():
            for question in request.data['answers'][category]["questions"]:
                if question.get("answer") is None:
                    return QuestionnaireRecord.EARLY_EXITED
        return QuestionnaireRecord.COMPLETED
    
    
    def post(self, request, *args, **kwargs) -> Response:
        # Verify the request
        verification_response = self._verify(request)
        if verification_response and verification_response.status_code != status.HTTP_200_OK:
            return verification_response
        
        # Create a new questionnaire definition
        serializer = QuestionnaireRecordSerializer(
            data=request.data, 
            status=self._get_questionnaire_status(request))
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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

class HelloWorldView(View):
  def get(self, request, *args, **kwargs):
        return render(request, "base.html")