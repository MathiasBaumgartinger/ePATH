from django.db import models
from django_jsonform.models.fields import JSONField
from django_countries.fields import CountryField


class QuestionnaireDefinition(models.Model):
    """A model to define the structure of a version/country combination of a questionnaire.
    """
    id = models.CharField(max_length=50, editable=False, primary_key=True)  # Custom ID format: country-code-version
    version = models.CharField(max_length=20, default='1.0')
    country = CountryField()
    release_date = models.DateField(auto_now_add=True)

    DEFINITION_SCHEMA = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "category_title": {"type": "string"},
                "category_description": {"type": "string"},
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "question_type": {
                                "type": "string",
                                "enum": ["textarea", "range", "radio", "checkbox"]
                            },
                            "params": {
                                "oneOf": [
                                    {"title": "Textarea parameters", "$ref": "#/$defs/textarea_params"},
                                    {"title": "Range parameters", "$ref": "#/$defs/range_params"},
                                    {"title": "Radio parameters", "$ref": "#/$defs/radio_params"},
                                    {"title": "Checkbox parameters", "$ref": "#/$defs/checkbox_params"}
                                ]
                            },
                            "required": {"type": ["boolean", "null"]}
                        },
                        "required": ["question", "question_type", "params"]
                    }
                }
            },
            "required": ["category_title", "questions"]
        },
        "$defs": {
            "textarea_params": {
                "type": "object",
                "properties": {
                    "max_length": {"type": "integer"},
                    "placeholder": {"type": "string"}
                },
                "required": ["max_length"],
                "additionalProperties": False
            },
            "range_params": {
                "type": "object",
                "properties": {
                    "min": {"type": "number"},
                    "max": {"type": "number"},
                    "step": {"type": "number"}
                },
                "required": ["min", "max"],
                "additionalProperties": False
            },
            "radio_params": {
                "type": "object",
                "properties": {
                    "options": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["options"],
                "additionalProperties": False
            },
            "checkbox_params": {
                "type": "object",
                "properties": {
                    "options": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "min_select": {"type": "integer"},
                    "max_select": {"type": "integer"}
                },
                "required": ["options"],
                "additionalProperties": False
            },
            "address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                    "state": {"type": "string"}
                }
            }
        }
    }
    definition = JSONField(
        schema=DEFINITION_SCHEMA,
        default=list,
        blank=True,
        help_text="Define questionnaire as an array of category objects."
    )

    def save(self, *args, **kwargs):
        self.id = f"{self.country.code}-{self.version}"
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'questionnaire'
        constraints = [
            models.UniqueConstraint(
                fields=['country', 'version'],
                name='uq_questionnaire_country_version'
            )
        ]
    
    def __str__(self):
        return f"questionnaire-version-{self.country}/{self.version}"


class QuestionnaireRecord(models.Model):
    COMPLETED = 'completed'
    IN_PROGRESS = 'in_progress'
    EARLY_EXITED = 'early_exited'
    
    STATUS_CHOICES = [
        (COMPLETED, 'Completed'),
        (IN_PROGRESS, 'In Progress'),
        (EARLY_EXITED, 'Early Exited'),
    ]
    
    user_uuid = models.CharField(max_length=36, db_index=True)
    date = models.DateTimeField(auto_now_add=True)
    questionnaire_def_fk = models.ForeignKey(QuestionnaireDefinition, on_delete=models.PROTECT)
    
    answers = JSONField(
        schema={
            "type": "object",
            "properties": {},
            "additionalProperties": True
        },
        default=dict,
        blank=True,
        help_text="Store questionnaire answers as a flat mapping of questionID→value"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=IN_PROGRESS)
    
    class Meta:
        app_label = 'questionnaire'
        
    def __str__(self):
        return f"questionnaire-record-user:{self.user_uuid}-{self.questionnaire_def_fk}"
