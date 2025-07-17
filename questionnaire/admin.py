from django.contrib import admin
from . import models as questionnaire_models


admin.site.register(questionnaire_models.QuestionnaireDefinition)
admin.site.register(questionnaire_models.QuestionnaireRecord)