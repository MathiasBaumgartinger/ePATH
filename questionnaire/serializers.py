from rest_framework import serializers
from .models import QuestionnaireDefinition, QuestionnaireRecord

class QuestionnaireDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireDefinition
        fields = [
            'id',           # Primary key
            'version',
            'country',
            'release_date',
            'definition',
        ]
        read_only_fields = ['id', 'release_date']


class QuestionnaireRecordSerializer(serializers.ModelSerializer):
    # nested read‐only representation
    questionnaire_definition = QuestionnaireDefinitionSerializer(
        source='questionnaire_def_fk',
        read_only=True
    )
    # write‐only field for creating/updating
    questionnaire_def_fk = serializers.PrimaryKeyRelatedField(
        queryset=QuestionnaireDefinition.objects.all(),
        write_only=True
    )

    class Meta:
        model = QuestionnaireRecord
        fields = [
            'id',                       # Primary key
            'user_uuid',
            'date',
            'questionnaire_def_fk',     # write-only
            'questionnaire_definition', # nested read-only
            'answers',
            'status',
        ]
        read_only_fields = ['id', 'date']