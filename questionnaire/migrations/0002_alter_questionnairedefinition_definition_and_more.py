# Generated by Django 5.2.4 on 2025-07-15 19:27

import django_jsonform.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnairedefinition',
            name='definition',
            field=django_jsonform.models.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='questionnairerecord',
            name='answers',
            field=django_jsonform.models.fields.JSONField(),
        ),
    ]
