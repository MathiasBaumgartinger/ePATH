from django.urls import path
from .views import HelloWorldView, QuestionnaireDefinitionView, QuestionnaireRecordView, QuestionnaireDefinitionManagementView 

urlpatterns = [
    # Test endpoint
    path('world/', HelloWorldView.as_view(), name='hello_world_api'),
    path('definitions/', QuestionnaireDefinitionView.as_view(), name='questionnaire_definition'),
    path('records/', QuestionnaireRecordView.as_view(), name='questionnaire_record'),
    # Management view for questionnaire definitions
    path('definition-management/', QuestionnaireDefinitionManagementView.as_view(), name='questionnaire_management'),
]