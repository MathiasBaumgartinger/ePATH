from django.db import models
from django.db.models import JSONField
from django_countries.fields import CountryField


class QuestionnaireDefinition(models.Model):
    """A model to define the structure of a version/country combination of a questionnaire.
    """
    id = models.CharField(max_length=50, primary_key=True)  # Custom ID format: country-code-version
    version = models.CharField(max_length=20, default='1.0')
    country = CountryField()
    release_date = models.DateField(auto_now_add=True)
    definition = JSONField()

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
    
    answers = JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=IN_PROGRESS)
    
    class Meta:
        app_label = 'questionnaire'
        
    def __str__(self):
        return f"questionnaire-record-{self.user_uuid}-{self.questionnaire_version.version}"
