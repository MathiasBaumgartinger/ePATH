from django.urls import path, re_path
from .views import QuestionnaireView, QuestionnaireDefinitionView, QuestionnaireRecordView, QuestionnaireDefinitionManagementView 

urlpatterns = [
    # SPA entry point for questionnaire
    path('', QuestionnaireView.as_view(), name='questionnaire'),

    path('definitions/', QuestionnaireDefinitionView.as_view(), name='questionnaire_definition'),
    path('records/', QuestionnaireRecordView.as_view(), name='questionnaire_record'),
    path('definition-management/', QuestionnaireDefinitionManagementView.as_view(), name='questionnaire_management'),
    # Handle category-specific routes (with or without trailing slash)
    re_path(r'^category/(?P<category_id>\d+)/?$', QuestionnaireView.as_view(), name='questionnaire_category')
]